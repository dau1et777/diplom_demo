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


class CareerRecommendationViewSet(viewsets.ViewSet):
    """
    API endpoints for career recommendations.
    POST /api/results/recommend/ - Generate recommendations from quiz answers
    GET /api/results/{session_id}/ - Retrieve saved recommendations
    """
    
    permission_classes = [AllowAny]
    inference_service = None
    
    def __init__(self, *args, **kwargs):
        """Initialize with ML inference service."""
        super().__init__(*args, **kwargs)
        if CareerRecommendationViewSet.inference_service is None:
            try:
                CareerRecommendationViewSet.inference_service = CareerInferenceService()
            except Exception as e:
                logger.error(f"Failed to initialize inference service: {e}")
    
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
        top_n = request.data.get('top_n', 5)
        
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
            
            # Generate recommendations
            recommendations = self.inference_service.predict_careers(answers_dict, top_n=top_n)
            
            # Calculate ability scores
            ability_scores = self.inference_service.calculate_ability_scores(answers_dict)
            
            # Save recommendation to database
            primary_career = recommendations[0]['career'] if recommendations else 'Unknown'
            primary_compatibility = recommendations[0]['compatibility_score'] if recommendations else 0
            
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
        
        if not session_id or not career_id:
            return Response(
                {'error': 'session_id and career_id are required'},
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
        
        if not session_id or not career_id:
            return Response({'error': 'session_id and career_id required'}, status=400)
        
        try:
            progress, _ = UserProgress.objects.get_or_create(session_id=session_id)
            
            if career_id not in progress.viewed_careers:
                progress.viewed_careers.append(career_id)
                progress.save()
            
            return Response({'success': True})
        except Exception as e:
            return Response({'error': str(e)}, status=500)
