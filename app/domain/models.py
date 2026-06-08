from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from .common.models import TimeStampedModel


class Task(TimeStampedModel):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    PRIORITY_QUADRANT_CHOICES = [
        ('urgent_important', 'Urgent & Important'),
        ('not_urgent_important', 'Not Urgent & Important'),
        ('urgent_not_important', 'Urgent & Not Important'),
        ('not_urgent_not_important', 'Not Urgent & Not Important'),
    ]

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    priority_quadrant = models.CharField(max_length=50, choices=PRIORITY_QUADRANT_CHOICES, null=True, blank=True)
    story_points = models.IntegerField(null=True, blank=True)
    estimated_hours = models.FloatField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    sprint = models.ForeignKey('Sprint', null=True, blank=True, on_delete=models.SET_NULL, related_name='tasks')
    blocked_by = models.ManyToManyField('self', symmetrical=False, related_name='blocks', blank=True)

    def __str__(self):
        return self.title


from .project.models import Project  # noqa
from .sprint.models import Sprint, SprintMetrics  # noqa
