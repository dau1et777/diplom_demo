from django.db import models
from django.utils import timezone
import uuid


class QuizQuestion(models.Model):
    """
    Stores quiz questions with metadata.
    Questions are categorized by the skill they test.
    """
    
    CATEGORY_CHOICES = [
        ('logic', 'Logical Thinking'),
        ('creativity', 'Creativity'),
        ('communication', 'Communication'),
        ('academic', 'Academic Performance'),
        ('interests', 'Interests'),
        ('work_style', 'Work Style'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question_text = models.CharField(max_length=500)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, help_text="Detailed explanation of what this question assesses")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Quiz Question'
        verbose_name_plural = 'Quiz Questions'
    
    def __str__(self):
        return f"{self.question_text[:50]} ({self.get_category_display()})"


class QuizAnswer(models.Model):
    """
    Stores user quiz responses and timestamps.
    Links answers to quiz questions.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name='answers')
    user_response = models.IntegerField(help_text="Rating or response value (typically 1-10 scale)")
    session_id = models.CharField(max_length=255, db_index=True, help_text="Session or user identifier")
    submitted_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ['submitted_at']
        unique_together = ['session_id', 'question']
        verbose_name = 'Quiz Answer'
        verbose_name_plural = 'Quiz Answers'
    
    def __str__(self):
        return f"Answer: {self.question.question_text[:30]} = {self.user_response}"


class QuizSubmission(models.Model):
    """
    Records complete quiz submissions with all responses.
    Parent model for collecting quiz answers.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session_id = models.CharField(max_length=255, unique=True, db_index=True)
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='quiz_submissions')
    submitted_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    def __str__(self):
        return f"Quiz Submission - {self.session_id} ({self.submitted_at.strftime('%Y-%m-%d %H:%M')})"
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Quiz Submission'
        verbose_name_plural = 'Quiz Submissions'
