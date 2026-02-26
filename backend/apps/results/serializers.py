from rest_framework import serializers
from .models import CareerRecommendation, UserProgress


class CareerRecommendationSerializer(serializers.ModelSerializer):
    """Serializes career recommendations from ML model."""
    
    class Meta:
        model = CareerRecommendation
        fields = [
            'id', 'session_id', 'primary_career', 'primary_compatibility',
            'top_recommendations', 'abilities', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class UserProgressSerializer(serializers.ModelSerializer):
    """Serializes user progress and quiz tracking."""
    
    class Meta:
        model = UserProgress
        fields = [
            'id', 'session_id', 'quiz_attempt', 'viewed_careers',
            'saved_careers', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
