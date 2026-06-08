from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from .common.models import TimeStampedModel


class Task(TimeStampedModel):
    """Represents a task in the TaskFlow workflow."""

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
    completed_at = models.DateTimeField(null=True, blank=True)
    sprint = models.ForeignKey('Sprint', null=True, blank=True, on_delete=models.SET_NULL, related_name='tasks')
    # A task may depend on other tasks. `blocked_by` stores its blockers.
    blocked_by = models.ManyToManyField('self', symmetrical=False, related_name='blocks', blank=True)

    def __str__(self):
        """Show the task title in admin and debug output."""
        return self.title

    @property
    def is_blocked(self):
        """Returns True when this task is blocked by any incomplete parent tasks."""
        return self.blocked_by.filter(completed=False).exists()

    def mark_completed(self):
        """Mark the task as complete and record the completion timestamp."""
        if not self.completed:
            self.completed = True
            self.completed_at = timezone.now()
            self.save(update_fields=['completed', 'completed_at'])

    def clean(self):
        """Prevent marking a blocked task complete until blockers are resolved."""
        if self.completed and self.is_blocked:
            raise ValueError('A blocked task cannot be completed until all blocking tasks are finished.')


from .project.models import Project  # noqa
from .sprint.models import Sprint, SprintMetrics  # noqa
