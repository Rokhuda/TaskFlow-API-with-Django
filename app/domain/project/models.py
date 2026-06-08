from django.db import models
from django.contrib.auth import get_user_model
from ..common.models import TimeStampedModel


class Project(TimeStampedModel):
    """A project aggregates sprints and tasks under a single owner."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    # Link the project to its owner and allow reverse access via user.projects.
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='projects')
    # Flag projects that are completed or no longer active.
    is_archived = models.BooleanField(default=False)

    class Meta:
        # Show newest projects first in default query ordering.
        ordering = ['-created_at']
        # Add indexes for fast owner filtering and archived state checks.
        indexes = [
            models.Index(fields=['owner']),
            models.Index(fields=['is_archived']),
        ]

    def __str__(self):
        """Show the project name in admin and logs."""
        return self.name
