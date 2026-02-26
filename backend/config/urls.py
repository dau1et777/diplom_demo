"""
Django URL Configuration for Career Recommendation System API
Routes REST API endpoints for quiz, careers, and recommendations.
"""

from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from apps.quiz.views import QuizQuestionViewSet, QuizSubmissionViewSet
from apps.careers.views import CareerViewSet, CourseViewSet, UniversityViewSet
from apps.results.views import CareerRecommendationViewSet

# Create router for viewsets
router = DefaultRouter()

# Quiz endpoints
router.register(r'quiz/questions', QuizQuestionViewSet, basename='quiz-questions')

# Careers endpoints  
router.register(r'careers', CareerViewSet, basename='career')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'universities', UniversityViewSet, basename='university')

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),
    
    # API routes
    path('api/', include(router.urls)),
    
    # Quiz submission
    path('api/quiz/submit/', 
         QuizSubmissionViewSet.as_view({'post': 'submit_quiz'}),
         name='submit-quiz'),
    path('api/quiz/submission/<str:session_id>/', 
         QuizSubmissionViewSet.as_view({'get': 'get_submission'}),
         name='get-submission'),
    
    # Results and recommendations
    path('api/results/recommend/', 
         CareerRecommendationViewSet.as_view({'post': 'generate_recommendations'}),
         name='generate-recommendations'),
    path('api/results/<str:session_id>/', 
         CareerRecommendationViewSet.as_view({'get': 'get_recommendations'}),
         name='get-recommendations'),
    path('api/results/save-career/', 
         CareerRecommendationViewSet.as_view({'post': 'save_career'}),
         name='save-career'),
    path('api/results/view-career/', 
         CareerRecommendationViewSet.as_view({'post': 'view_career'}),
         name='view-career'),
]
