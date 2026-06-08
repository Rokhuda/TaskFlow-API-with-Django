from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone
from app.domain.models import Task, Sprint, Project
from app.api.serializers import TaskSerializer, SprintSerializer, ProjectSerializer
from app.services.priority import PriorityMatrixService
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
    ordering_fields = ['priority', 'priority_quadrant', 'created_at', 'due_date', 'story_points']

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
        sprint = serializer.validated_data.get('sprint')
        if sprint and not self.request.user.is_staff and sprint.project.owner != self.request.user:
            raise PermissionDenied('Cannot assign a task to a sprint outside your projects.')

        task = serializer.save(owner=self.request.user)
        if not task.priority_quadrant:
            task.priority_quadrant = PriorityMatrixService.determine_quadrant(task)
            task.save(update_fields=['priority_quadrant'])

    def perform_update(self, serializer):
        task = serializer.save()
        if not task.priority_quadrant:
            task.priority_quadrant = PriorityMatrixService.determine_quadrant(task)
            task.save(update_fields=['priority_quadrant'])


class SprintViewSet(viewsets.ModelViewSet):
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'goal']
    ordering_fields = ['start_date', 'end_date', 'status']
    pagination_class = TaskPagination

    def get_queryset(self):
        if self.request.user.is_staff:
            return Sprint.objects.all()
        return Sprint.objects.filter(project__owner=self.request.user)

    def perform_create(self, serializer):
        project = serializer.validated_data.get('project')
        if project and not self.request.user.is_staff and project.owner != self.request.user:
            raise PermissionDenied('Cannot create a sprint for a project you do not own.')
        serializer.save()

    @action(detail=True, methods=['get', 'post'])
    def tasks(self, request, pk=None):
        sprint = self.get_object()

        if request.method == 'POST':
            serializer = TaskSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            task = serializer.save(owner=request.user, sprint=sprint)
            if not task.priority_quadrant:
                task.priority_quadrant = PriorityMatrixService.determine_quadrant(task)
                task.save(update_fields=['priority_quadrant'])
            return Response(TaskSerializer(task).data, status=201)

        tasks = sprint.tasks.all()
        page = self.paginate_queryset(tasks)
        if page is not None:
            serializer = TaskSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='tasks/assign')
    def assign_task(self, request, pk=None):
        sprint = self.get_object()
        task_id = request.data.get('task_id')
        if not task_id:
            return Response({'detail': 'task_id is required.'}, status=400)

        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            return Response({'detail': 'Task not found.'}, status=404)

        if not request.user.is_staff and task.owner != request.user:
            raise PermissionDenied('You do not have permission to modify this task.')
        if not request.user.is_staff and sprint.project.owner != request.user:
            raise PermissionDenied('Cannot assign tasks to a sprint outside your projects.')

        task.sprint = sprint
        task.save()
        return Response(TaskSerializer(task).data)

    @action(detail=True, methods=['post'], url_path='tasks/move')
    def move_task(self, request, pk=None):
        return self.assign_task(request, pk)

    @action(detail=True, methods=['get'])
    def metrics(self, request, pk=None):
        sprint = self.get_object()
        return Response(sprint.get_metrics())


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

    def get_queryset(self):
        if self.request.user.is_staff:
            return Project.objects.all()
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
