import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from app.domain.models import Task

@pytest.mark.django_db
def test_task_permission_enforcement():
    client = APIClient()
    User = get_user_model()
    owner = User.objects.create_user(username='owner', password='pass')
    other = User.objects.create_user(username='other', password='pass')
    task = Task.objects.create(owner=owner, title='Owner Task', priority='low')

    # Other user cannot access owner's task
    client.force_authenticate(user=other)
    response = client.get(reverse('task-detail', args=[task.id]))
    assert response.status_code in [403, 404]

    # Other user cannot update owner's task
    response = client.patch(reverse('task-detail', args=[task.id]), {'title': 'Hacked'})
    assert response.status_code in [403, 404]

    # Other user cannot delete owner's task
    response = client.delete(reverse('task-detail', args=[task.id]))
    assert response.status_code in [403, 404]