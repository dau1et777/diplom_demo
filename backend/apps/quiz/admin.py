from django.contrib import admin
from .models import QuizQuestion, QuizAnswer, QuizSubmission


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'category', 'order', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('question_text', 'description')
    ordering = ('order',)
    fieldsets = (
        ('Question Details', {
            'fields': ('question_text', 'description', 'category')
        }),
        ('Configuration', {
            'fields': ('order', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at', 'id')


@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'user_response', 'session_id', 'submitted_at')
    list_filter = ('submitted_at', 'question__category')
    search_fields = ('session_id', 'question__question_text')
    readonly_fields = ('id', 'submitted_at')


@admin.register(QuizSubmission)
class QuizSubmissionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'user', 'submitted_at')
    list_filter = ('submitted_at', 'user')
    search_fields = ('session_id', 'user__username')
    readonly_fields = ('id', 'submitted_at')
