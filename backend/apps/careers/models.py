from django.db import models
import uuid


class Career(models.Model):
    """
    Stores career information and metadata.
    Used for displaying career details in recommendations.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, db_index=True)
    description = models.TextField()
    required_skills = models.JSONField(default=list, help_text="List of required skills")
    suitable_for = models.TextField(help_text="Description of suitable candidates")
    average_salary_range = models.CharField(max_length=100, blank=True, help_text="e.g., '$80k - $150k'")
    job_growth = models.CharField(max_length=50, blank=True, help_text="e.g., '12% annual growth'")
    typical_companies = models.JSONField(default=list, help_text="List of typical employers")
    required_education = models.CharField(max_length=255, blank=True, help_text="e.g., 'Bachelor in Computer Science'")
    related_careers = models.JSONField(default=list, help_text="List of related career names")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Career'
        verbose_name_plural = 'Careers'
    
    def __str__(self):
        return self.name


class Course(models.Model):
    """
    Stores recommended courses for each career.
    Links courses to careers for career path recommendations.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField(max_length=255)
    provider = models.CharField(max_length=255, help_text="e.g., 'Coursera', 'Udemy', 'University Name'")
    url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    duration = models.CharField(max_length=100, blank=True, help_text="e.g., '3 months', '1 year'")
    difficulty_level = models.CharField(
        max_length=20,
        choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')],
        default='intermediate'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['career', 'name']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
    
    def __str__(self):
        return f"{self.name} ({self.career.name})"


class University(models.Model):
    """
    Stores recommended universities for each career.
    Provides location and program information.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='universities')
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    program_name = models.CharField(max_length=255, help_text="e.g., 'Bachelor of Computer Science'")
    url = models.URLField(blank=True)
    ranking = models.IntegerField(blank=True, null=True, help_text="University ranking in this field")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['career', 'ranking']
        verbose_name = 'University'
        verbose_name_plural = 'Universities'
    
    def __str__(self):
        return f"{self.name} - {self.program_name}"
