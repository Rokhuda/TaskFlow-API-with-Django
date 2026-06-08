from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from app.domain.models import Task, Sprint
from app.api.serializers import TaskSerializer, SprintSerializer
from rest_framework.pagination import PageNumberPagination


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsAdminOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.owner == request.user


class TaskPagination(PageNumberPagination):
    page_size = 10


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrOwner]
    pagination_class = TaskPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['priority', 'created_at', 'due_date', 'story_points']

    def get_queryset(self):
        queryset = Task.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)

        priority = self.request.query_params.get('priority')
        quadrant = self.request.query_params.get('priority_quadrant')
        sprint = self.request.query_params.get('sprint')
        completed = self.request.query_params.get('completed')

        if priority:
            queryset = queryset.filter(priority=priority)
        if quadrant:
            queryset = queryset.filter(priority_quadrant=quadrant)
        if sprint:
            queryset = queryset.filter(sprint_id=sprint)
        if completed in ['true', 'false']:
            queryset = queryset.filter(completed=(completed == 'true'))

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SprintViewSet(viewsets.ModelViewSet):
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'goal']
    ordering_fields = ['start_date', 'end_date', 'status']

    def get_queryset(self):
        if self.request.user.is_staff:
            return Sprint.objects.all()
        return Sprint.objects.filter(project__owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['get'])
    def metrics(self, request, pk=None):
        sprint = self.get_object()
        return Response(sprint.get_metrics())
