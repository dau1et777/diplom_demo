from django.contrib import admin
from .models import CareerRecommendation, UserProgress


@admin.register(CareerRecommendation)
class CareerRecommendationAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'primary_career', 'primary_compatibility', 'created_at')
    list_filter = ('created_at', 'primary_career')
    search_fields = ('session_id', 'primary_career')
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'quiz_attempt', 'created_at')
    list_filter = ('created_at', 'quiz_attempt')
    search_fields = ('session_id', 'user__username')
    readonly_fields = ('id', 'created_at', 'updated_at')
