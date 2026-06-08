from django.db.models import Sum
from rest_framework import serializers
from app.domain.models import Task, Sprint, Project


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'priority',
            'priority_quadrant',
            'story_points',
            'estimated_hours',
            'due_date',
            'completed',
            'completed_at',
            'sprint',
            'blocked_by',
            'owner',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at', 'completed_at']

    def validate(self, data):
        completed = data.get('completed')
        blocked_by = data.get('blocked_by')

        if self.instance and blocked_by is None:
            blocked_by = self.instance.blocked_by.all()

        if completed and blocked_by is not None:
            for blocked_task in blocked_by:
                if not blocked_task.completed:
                    raise serializers.ValidationError('Cannot complete a task while its blockers are incomplete.')

        return data


class SprintSerializer(serializers.ModelSerializer):
    progress_percent = serializers.ReadOnlyField()
    days_remaining = serializers.ReadOnlyField()
    task_count = serializers.SerializerMethodField()
    completed_count = serializers.SerializerMethodField()
    total_story_points = serializers.SerializerMethodField()
    completed_story_points = serializers.SerializerMethodField()

    class Meta:
        model = Sprint
        fields = [
            'id',
            'name',
            'project',
            'start_date',
            'end_date',
            'status',
            'goal',
            'capacity',
            'progress_percent',
            'days_remaining',
            'task_count',
            'completed_count',
            'total_story_points',
            'completed_story_points',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_task_count(self, obj):
        return obj.tasks.count()

    def get_completed_count(self, obj):
        return obj.tasks.filter(completed=True).count()

    def get_total_story_points(self, obj):
        return obj.tasks.aggregate(total=Sum('story_points'))['total'] or 0

    def get_completed_story_points(self, obj):
        return obj.tasks.filter(completed=True).aggregate(total=Sum('story_points'))['total'] or 0


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'description',
            'owner',
            'is_archived',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']
