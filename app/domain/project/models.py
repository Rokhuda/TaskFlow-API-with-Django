from django.db import models
from django.contrib.auth import get_user_model
from ..common.models import TimeStampedModel


class Project(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='projects')
    is_archived = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['owner']),
            models.Index(fields=['is_archived']),
        ]

    def __str__(self):
        return self.name
