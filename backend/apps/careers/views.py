from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from .models import Career, Course, University
from .serializers import (
    CareerDetailSerializer, 
    CareerListSerializer,
    CourseSerializer,
    UniversitySerializer
)


class CareerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoints for career information.
    GET /api/careers/ - List all careers
    GET /api/careers/{id}/ - Get career details with courses and universities
    """
    
    queryset = Career.objects.filter(is_active=True)
    serializer_class = CareerDetailSerializer
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        """Use list serializer for list view, detail for retrieve."""
        if self.action == 'list':
            return CareerListSerializer
        return CareerDetailSerializer
    
    def list(self, request, *args, **kwargs):
        """Return all active careers as list."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': len(serializer.data),
            'results': serializer.data
        })
    
    def retrieve(self, request, pk=None):
        """Return detailed career information including courses and universities."""
        career = get_object_or_404(self.queryset, id=pk)
        serializer = self.get_serializer(career)
        return Response(serializer.data)


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoints for courses.
    GET /api/courses/ - List all courses
    GET /api/courses/{id}/ - Get course details
    """
    
    queryset = Course.objects.filter(is_active=True)
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]


class UniversityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoints for universities.
    GET /api/universities/ - List all universities
    GET /api/universities/{id}/ - Get university details
    """
    
    queryset = University.objects.filter(is_active=True)
    serializer_class = UniversitySerializer
    permission_classes = [AllowAny]
