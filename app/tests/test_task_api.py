import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from app.domain.models import Task

@pytest.mark.django_db
def test_task_crud_flow():
    client = APIClient()
    User = get_user_model()
    user = User.objects.create_user(username='testuser', password='testpass')
    client.force_authenticate(user=user)

    # Create
    response = client.post(reverse('task-list'), {
        'title': 'Test Task',
        'description': 'Test Description',
        'priority': 'high',
    })
    assert response.status_code == 201
    task_id = response.data['id']

    # Read
    response = client.get(reverse('task-detail', args=[task_id]))
    assert response.status_code == 200
    assert response.data['title'] == 'Test Task'

    # Update
    response = client.patch(reverse('task-detail', args=[task_id]), {'completed': True})
    assert response.status_code == 200
    assert response.data['completed'] is True

    # Delete
    response = client.delete(reverse('task-detail', args=[task_id]))
    assert response.status_code == 204
    assert Task.objects.count() == 0
