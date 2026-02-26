from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import QuizQuestion, QuizAnswer, QuizSubmission
from .serializers import (
    QuizQuestionSerializer, 
    QuizAnswerCreateSerializer, 
    QuizSubmissionSerializer
)


class QuizQuestionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoints for quiz questions.
    GET /api/quiz/questions/ - List all active questions
    GET /api/quiz/questions/{id}/ - Get specific question
    """
    
    queryset = QuizQuestion.objects.filter(is_active=True)
    serializer_class = QuizQuestionSerializer
    permission_classes = [AllowAny]
    pagination_class = None
    
    def list(self, request, *args, **kwargs):
        """Return all active quiz questions ordered by sequence."""
        queryset = self.get_queryset().order_by('order')
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': len(serializer.data),
            'results': serializer.data
        })


class QuizSubmissionViewSet(viewsets.ViewSet):
    """
    API endpoints for quiz submission and retrieval.
    POST /api/quiz/submit/ - Submit quiz answers
    GET /api/quiz/submission/{session_id}/ - Get submission details
    """
    
    permission_classes = [AllowAny]
    
    @transaction.atomic
    def submit_quiz(self, request):
        """
        Handle quiz submission with multiple answers.
        
        Request payload:
        {
            "session_id": "unique-session-id",
            "answers": {
                "question-uuid": 8,
                "question-uuid": 7,
                ...
            }
        }
        
        Returns: {
            "success": true,
            "submission_id": "uuid",
            "session_id": "session-uuid",
            "message": "Quiz submitted successfully"
        }
        """
        serializer = QuizAnswerCreateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {
                    'success': False,
                    'errors': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        validated_data = serializer.validated_data
        session_id = validated_data['session_id']
        answers_data = validated_data['answers']
        
        try:
            # Create or get submission
            submission, created = QuizSubmission.objects.get_or_create(
                session_id=session_id,
                defaults={'user': request.user if request.user.is_authenticated else None}
            )
            
            # Store all answers
            for question_id, response_value in answers_data.items():
                question = get_object_or_404(QuizQuestion, id=question_id)
                QuizAnswer.objects.update_or_create(
                    session_id=session_id,
                    question=question,
                    defaults={'user_response': response_value}
                )
            
            return Response({
                'success': True,
                'submission_id': str(submission.id),
                'session_id': submission.session_id,
                'message': 'Quiz submitted successfully'
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get_submission(self, request, session_id=None):
        """
        Retrieve quiz submission and answers for a session.
        
        Returns: {
            "submission": {...},
            "answers": [...]
        }
        """
        submission = get_object_or_404(QuizSubmission, session_id=session_id)
        answers = QuizAnswer.objects.filter(session_id=session_id)
        
        quiz_data = {
            'submission': QuizSubmissionSerializer(submission).data,
            'answers': [
                {
                    'question_id': str(ans.question.id),
                    'question_text': ans.question.question_text,
                    'category': ans.question.category,
                    'response': ans.user_response
                }
                for ans in answers
            ]
        }
        
        return Response(quiz_data)
