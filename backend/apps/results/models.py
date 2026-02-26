from django.db import models
import uuid


class CareerRecommendation(models.Model):
    """
    Stores ML model predictions and career recommendations.
    Links quiz submissions to recommended careers.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session_id = models.CharField(max_length=255, unique=True, db_index=True)
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='recommendations')
    
    # Top recommendation
    primary_career = models.CharField(max_length=255)
    primary_compatibility = models.FloatField(help_text="Compatibility percentage for primary career")
    
    # All top recommendations
    top_recommendations = models.JSONField(default=list, help_text="""
        List of top 5 career recommendations with compatibility scores.
        Format: [{'career': 'name', 'compatibility_score': 85.5, 'explanation': '...'}]
    """)
    
    # User abilities breakdown
    abilities = models.JSONField(default=dict, help_text="""
        User's scored abilities from quiz responses.
        Format: {'logical_thinking': 8, 'creativity': 6, ...}
    """)
    
    # Quiz feature summary
    quiz_features = models.JSONField(default=dict, help_text="""
        Extracted feature vector from quiz answers used for prediction.
    """)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Career Recommendation'
        verbose_name_plural = 'Career Recommendations'
    
    def __str__(self):
        return f"Recommendation for {self.session_id} - {self.primary_career}"


class UserProgress(models.Model):
    """
    Tracks user's quiz history and recommendations over time.
    Allows users to see their improvement and exploration.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session_id = models.CharField(max_length=255, db_index=True)
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='progress_history')
    
    recommendation = models.ForeignKey(
        CareerRecommendation, 
        on_delete=models.CASCADE, 
        related_name='user_progress',
        null=True,
        blank=True
    )
    
    quiz_attempt = models.IntegerField(default=1, help_text="Which attempt number is this")
    viewed_careers = models.JSONField(default=list, help_text="List of career IDs viewed by user")
    saved_careers = models.JSONField(default=list, help_text="List of career IDs bookmarked by user")
    take_quiz_count = models.IntegerField(default=1)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User Progress'
        verbose_name_plural = 'User Progress'
    
    def __str__(self):
        return f"Progress - {self.session_id} (Attempt {self.quiz_attempt})"
