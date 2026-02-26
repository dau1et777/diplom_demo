from django.contrib import admin
from .models import Career, Course, University


@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'is_active')
        }),
        ('Career Details', {
            'fields': ('required_skills', 'suitable_for', 'required_education', 'related_careers')
        }),
        ('Market Information', {
            'fields': ('average_salary_range', 'job_growth', 'typical_companies')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'career', 'provider', 'difficulty_level', 'is_active')
    list_filter = ('career', 'difficulty_level', 'is_active', 'created_at')
    search_fields = ('name', 'career__name', 'provider')
    readonly_fields = ('id', 'created_at')


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'career', 'location', 'program_name', 'ranking')
    list_filter = ('career', 'location', 'created_at')
    search_fields = ('name', 'career__name', 'location', 'program_name')
    readonly_fields = ('id', 'created_at')
