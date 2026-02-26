from rest_framework import serializers
from .models import Career, Course, University


class CourseSerializer(serializers.ModelSerializer):
    """Serializes course information."""
    
    class Meta:
        model = Course
        fields = ['id', 'name', 'provider', 'url', 'description', 'duration', 'difficulty_level']


class UniversitySerializer(serializers.ModelSerializer):
    """Serializes university information."""
    
    class Meta:
        model = University
        fields = ['id', 'name', 'location', 'program_name', 'url', 'ranking']


class CareerDetailSerializer(serializers.ModelSerializer):
    """
    Detailed career information with related courses and universities.
    Used for career detail pages.
    """
    
    courses = CourseSerializer(many=True, read_only=True)
    universities = UniversitySerializer(many=True, read_only=True)
    
    class Meta:
        model = Career
        fields = [
            'id', 'name', 'description', 'required_skills', 'suitable_for',
            'average_salary_range', 'job_growth', 'typical_companies',
            'required_education', 'related_careers', 'courses', 'universities'
        ]


class CareerListSerializer(serializers.ModelSerializer):
    """Lightweight career serializer for list views."""
    
    class Meta:
        model = Career
        fields = ['id', 'name', 'description', 'average_salary_range', 'job_growth']
