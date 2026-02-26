from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import CareerRecommendation, UserProgress
from .serializers import CareerRecommendationSerializer, UserProgressSerializer
from .inference import CareerInferenceService
from apps.quiz.models import QuizAnswer
import logging


logger = logging.getLogger(__name__)

# Import recommendation services with graceful fallback
try:
    from ml.ability_recommender import AbilityRecommendationService
except (ImportError, Exception):
    AbilityRecommendationService = None

try:
    from ml.advanced_recommender import HybridRecommendationService
except (ImportError, Exception):
    HybridRecommendationService = None


class CareerRecommendationViewSet(viewsets.ViewSet):
    """
    API endpoints for career recommendations.
    POST /api/results/recommend/ - Generate recommendations from quiz answers
    GET /api/results/{session_id}/ - Retrieve saved recommendations
    """
    
    permission_classes = [AllowAny]
    inference_service = None

    def __init__(self, *args, **kwargs):
        """Initialize with ML inference service (priority order)."""
        super().__init__(*args, **kwargs)
        if CareerRecommendationViewSet.inference_service is None:
            # Priority 1: Ability-based recommendation (best at matching user abilities)
            if AbilityRecommendationService:
                try:
                    CareerRecommendationViewSet.inference_service = AbilityRecommendationService()
                    logger.info("Using AbilityRecommendationService (ability-based matching)")
                except Exception as e:
                    logger.warning(f"AbilityRecommendationService failed ({e}), trying HybridRecommendationService")
            
            # Priority 2: Hybrid embedding-based recommender
            if CareerRecommendationViewSet.inference_service is None and HybridRecommendationService:
                try:
                    CareerRecommendationViewSet.inference_service = HybridRecommendationService()
                    logger.info("Using HybridRecommendationService (embedding-based)")
                except Exception as e:
                    logger.warning(f"HybridRecommendationService failed ({e}), falling back to CareerInferenceService")
            
            # Priority 3: Traditional ML fallback
            if CareerRecommendationViewSet.inference_service is None:
                try:
                    CareerRecommendationViewSet.inference_service = CareerInferenceService()
                    logger.info("Using CareerInferenceService (traditional ML fallback)")
                except Exception as fallback_e:
                    logger.error(f"Failed to initialize any inference service: {fallback_e}")

    
    @transaction.atomic
    def generate_recommendations(self, request):
        """
        Generate career recommendations from quiz answers.
        
        Request: {
            "session_id": "unique-session",
            "top_n": 5  // optional
        }
        
        Returns: {
            "success": true,
            "recommendations": [...],
            "abilities": {...},
            "primary_career": "Software Developer",
            "primary_compatibility": 87.5
        }
        """
        session_id = request.data.get('session_id')
        top_n = request.data.get('top_n', 10)  # Default to 10 careers instead of 5
        
        if not session_id:
            return Response(
                {'success': False, 'error': 'session_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Fetch quiz answers for this session
            quiz_answers = QuizAnswer.objects.filter(session_id=session_id)
            
            if not quiz_answers.exists():
                return Response(
                    {'success': False, 'error': 'No quiz answers found for this session'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Convert to dict for ML service
            answers_dict = {}
            for answer in quiz_answers:
                answers_dict[str(answer.question.id)] = answer.user_response
            
            # Handle different service types
            service_class_name = self.inference_service.__class__.__name__
            
            if service_class_name == 'AbilityRecommendationService':
                # New ability-based service returns AbilityRecommendation objects
                rec_objects = self.inference_service.recommend(answers_dict, top_n=top_n)
                recommendations = [r.to_dict() for r in rec_objects]
                ability_scores = {}  # Will be filled below
            elif service_class_name == 'HybridRecommendationService':
                # Hybrid service returns dataclass objects
                rec_objects = self.inference_service.recommend(answers_dict, top_n=top_n)
                recommendations = [r.to_dict() for r in rec_objects]
                ability_scores = self.inference_service.calculate_ability_scores(answers_dict) if hasattr(self.inference_service, 'calculate_ability_scores') else {}
            else:
                # Old CareerInferenceService returns dicts directly
                recommendations = self.inference_service.predict_careers(answers_dict, top_n=top_n)
                ability_scores = self.inference_service.calculate_ability_scores(answers_dict) if hasattr(self.inference_service, 'calculate_ability_scores') else {}
            
            # If ability_scores is empty (AbilityRecommendationService), compute using inference service
            if not ability_scores or service_class_name == 'AbilityRecommendationService':
                try:
                    # Use CareerInferenceService separately to get core ability scores
                    from apps.results.inference import CareerInferenceService
                    inference_service = CareerInferenceService()
                    core_abilities = inference_service.calculate_ability_scores(answers_dict)
                    ability_scores.update(core_abilities)
                except Exception as e:
                    logger.warning(f"Failed to extract core ability scores: {e}")
            
            # even if the service didn't supply interest details, compute them here
            def _extract_interest_scores(answers):
                scores = {
                    'interest_tech': 5.0,
                    'interest_business': 5.0,
                    'interest_creativity': 5.0,
                    'interest_social': 5.0,
                }
                try:
                    from apps.quiz.models import QuizQuestion
                    questions = {str(q.id): q for q in QuizQuestion.objects.all()}
                    buckets = {14: [], 15: [], 16: [], 17: []}
                    for qid, val in answers.items():
                        q = questions.get(str(qid))
                        if not q or q.category != 'interests':
                            continue
                        order = q.order
                        score = None
                        if isinstance(val, dict):
                            score = val.get('value') or val.get('score')
                        else:
                            score = val
                        try:
                            buckets[order].append(float(score))
                        except Exception:
                            pass
                    def avg(lst):
                        return round(sum(lst) / len(lst), 1) if lst else 5.0
                    scores['interest_tech'] = avg(buckets[14])
                    scores['interest_business'] = avg(buckets[15])
                    scores['interest_creativity'] = avg(buckets[16])
                    scores['interest_social'] = avg(buckets[17])
                except Exception:
                    pass
                return scores
            interest_scores = _extract_interest_scores(answers_dict)
            # merge into ability_scores (overwrites existing keys or fills missing)
            ability_scores.update(interest_scores)
            
            # Extract work style scores
            def _extract_work_style_scores(answers):
                scores = {
                    'work_style_independent': 5.0,
                    'work_style_collaborative': 5.0,
                }
                try:
                    from apps.quiz.models import QuizQuestion
                    questions = {str(q.id): q for q in QuizQuestion.objects.all()}
                    buckets = {18: [], 19: []}  # Q18: independent, Q19: collaborative
                    for qid, val in answers.items():
                        q = questions.get(str(qid))
                        if not q or q.category != 'work_style':
                            continue
                        order = q.order
                        score = None
                        if isinstance(val, dict):
                            score = val.get('value') or val.get('score')
                        else:
                            score = val
                        try:
                            buckets[order].append(float(score))
                        except Exception:
                            pass
                    def avg(lst):
                        return round(sum(lst) / len(lst), 1) if lst else 5.0
                    scores['work_style_independent'] = avg(buckets[18])
                    scores['work_style_collaborative'] = avg(buckets[19])
                except Exception:
                    pass
                return scores
            work_scores = _extract_work_style_scores(answers_dict)
            ability_scores.update(work_scores)
            
            # normalize dictionary keys so frontend can always access .career
            for rec in recommendations:
                if 'career' not in rec and 'name' in rec:
                    rec['career'] = rec['name']
                # also ensure compatibility_score present when using score
                if 'compatibility_score' not in rec and 'score' in rec:
                    rec['compatibility_score'] = rec['score']
                if 'match_score' in rec and 'compatibility_score' not in rec:
                    rec['compatibility_score'] = rec['match_score']
            
            # Save recommendation to database
            if recommendations:
                primary_career = recommendations[0].get('name') or recommendations[0].get('career', 'Unknown')
                # Handle both response formats: new has 'score', old has 'compatibility_score'
                primary_compatibility = (
                    recommendations[0].get('score') or 
                    recommendations[0].get('compatibility_score') or
                    recommendations[0].get('match_score', 0)
                )
            else:
                primary_career = 'Unknown'
                primary_compatibility = 0
            
            recommendation_obj, created = CareerRecommendation.objects.update_or_create(
                session_id=session_id,
                defaults={
                    'primary_career': primary_career,
                    'primary_compatibility': primary_compatibility,
                    'top_recommendations': recommendations,
                    'abilities': ability_scores,
                    'quiz_features': answers_dict,
                    'user': request.user if request.user.is_authenticated else None,
                }
            )
            
            # Track user progress
            UserProgress.objects.update_or_create(
                session_id=session_id,
                defaults={
                    'recommendation': recommendation_obj,
                    'user': request.user if request.user.is_authenticated else None,
                }
            )
            
            return Response({
                'success': True,
                'recommendation_id': str(recommendation_obj.id),
                'session_id': session_id,
                'primary_career': primary_career,
                'primary_compatibility': round(primary_compatibility, 2),
                'top_recommendations': recommendations[:top_n],
                'abilities': ability_scores,
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def get_recommendations(self, request, session_id=None):
        """
        Retrieve saved recommendations for a session.
        
        Returns: {
            "recommendation": {...},
            "progress": {...}
        }
        """
        try:
            recommendation = get_object_or_404(CareerRecommendation, session_id=session_id)
            progress = UserProgress.objects.filter(session_id=session_id).first()
            
            data = {
                'recommendation': CareerRecommendationSerializer(recommendation).data,
                'progress': UserProgressSerializer(progress).data if progress else None,
            }
            
            return Response(data)
        
        except Exception as e:
            logger.error(f"Error fetching recommendations: {e}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'])
    def save_career(self, request):
        """
        Save a career to user's bookmarks.
        
        Request: {
            "session_id": "session-id",
            "career_id": "career-uuid"
        }
        """
        session_id = request.data.get('session_id')
        career_id = request.data.get('career_id')
        career_name = request.data.get('career')

        # Accept career name for convenience (frontend sends name)
        if not career_id and career_name:
            try:
                from apps.careers.models import Career
                career_obj = Career.objects.filter(name__iexact=career_name).first()
                if career_obj:
                    career_id = str(career_obj.id)
            except Exception:
                pass

        if not session_id or not career_id:
            return Response(
                {'error': 'session_id and career_id or career name are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            progress, _ = UserProgress.objects.get_or_create(session_id=session_id)
            
            if career_id not in progress.saved_careers:
                progress.saved_careers.append(career_id)
                progress.save()
            
            return Response({'success': True, 'saved_careers': progress.saved_careers})
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def view_career(self, request):
        """Track career views for analytics."""
        session_id = request.data.get('session_id')
        career_id = request.data.get('career_id')
        career_name = request.data.get('career')
        
        # allow name lookup
        if not career_id and career_name:
            try:
                from apps.careers.models import Career
                career_obj = Career.objects.filter(name__iexact=career_name).first()
                if career_obj:
                    career_id = str(career_obj.id)
            except Exception:
                pass
        
        if not session_id or not career_id:
            return Response({'error': 'session_id and career_id or career name required'}, status=400)
        
        try:
            progress, _ = UserProgress.objects.get_or_create(session_id=session_id)
            
            if career_id not in progress.viewed_careers:
                progress.viewed_careers.append(career_id)
                progress.save()
            
            return Response({'success': True})
        except Exception as e:
            return Response({'error': str(e)}, status=500)
