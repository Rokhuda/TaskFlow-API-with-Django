from django.db import models
from django.utils import timezone
from ..common.models import TimeStampedModel


class Sprint(TimeStampedModel):
    STATUS_PLANNED = 'planned'
    STATUS_ACTIVE = 'active'
    STATUS_COMPLETED = 'completed'
    STATUS_ARCHIVED = 'archived'

    STATUS_CHOICES = [
        (STATUS_PLANNED, 'Planned'),
        (STATUS_ACTIVE, 'Active'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_ARCHIVED, 'Archived'),
    ]

    name = models.CharField(max_length=255)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='sprints')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PLANNED)
    goal = models.TextField(blank=True)
    capacity = models.IntegerField(default=0, help_text='Team capacity in story points')

    class Meta:
        ordering = ['-start_date']
        unique_together = ('project', 'name')
        indexes = [
            models.Index(fields=['project', '-start_date']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.name} - {self.project.name}"

    @property
    def is_active(self):
        return self.status == self.STATUS_ACTIVE

    @property
    def days_remaining(self):
        if self.status == self.STATUS_ACTIVE:
            return max(0, (self.end_date - timezone.now()).days)
        return 0

    @property
    def progress_percent(self):
        if self.start_date >= self.end_date:
            return 0
        total_days = max(1, (self.end_date - self.start_date).days)
        elapsed_days = (timezone.now() - self.start_date).days
        return min(100, max(0, int((elapsed_days / total_days) * 100)))

    def get_metrics(self):
        tasks = self.tasks.all()
        total_points = tasks.aggregate(total=models.Sum('story_points'))['total'] or 0
        completed_points = tasks.filter(completed=True).aggregate(total=models.Sum('story_points'))['total'] or 0
        return {
            'total_tasks': tasks.count(),
            'completed_tasks': tasks.filter(completed=True).count(),
            'in_progress_tasks': tasks.filter(completed=False).count(),
            'total_story_points': total_points,
            'completed_story_points': completed_points,
            'remaining_story_points': total_points - completed_points,
            'progress_percent': self.progress_percent,
            'days_remaining': self.days_remaining,
        }


class SprintMetrics(TimeStampedModel):
    sprint = models.OneToOneField(Sprint, on_delete=models.CASCADE, related_name='metrics')
    burndown_data = models.JSONField(default=list, blank=True)
    velocity = models.FloatField(null=True, blank=True)
    completion_rate = models.FloatField(default=0)
    on_time_rate = models.FloatField(default=0)

    def __str__(self):
        return f"Metrics for {self.sprint.name}"
