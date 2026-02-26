from rest_framework import serializers
from .models import QuizQuestion, QuizAnswer, QuizSubmission


class QuizQuestionSerializer(serializers.ModelSerializer):
    """Serializes quiz questions for API responses."""
    
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = QuizQuestion
        fields = ['id', 'question_text', 'category', 'category_display', 'description', 'order']


class QuizAnswerSerializer(serializers.ModelSerializer):
    """Serializes individual quiz answers."""
    
    class Meta:
        model = QuizAnswer
        fields = ['id', 'question', 'user_response', 'session_id']


class QuizAnswerCreateSerializer(serializers.Serializer):
    """
    Handles bulk submission of quiz answers.
    Accepts array of question_id: response_value pairs.
    """
    
    session_id = serializers.CharField(max_length=255)
    answers = serializers.DictField(
        child=serializers.IntegerField(min_value=1, max_value=10),
        help_text="Dictionary mapping question_id to response value (1-10)"
    )
    
    def validate_answers(self, value):
        """Validate that all answers are valid integers in range."""
        if not value:
            raise serializers.ValidationError("At least one answer must be provided.")
        return value


class QuizSubmissionSerializer(serializers.ModelSerializer):
    """Serializes complete quiz submissions."""
    
    class Meta:
        model = QuizSubmission
        fields = ['id', 'session_id', 'submitted_at']
        read_only_fields = ['submitted_at']
