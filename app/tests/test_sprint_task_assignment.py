import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.utils import timezone
from app.domain.models import Project, Sprint, Task


@pytest.mark.django_db
def test_create_task_under_sprint_autofills_quadrant():
    client = APIClient()
    User = get_user_model()
    user = User.objects.create_user(username='sprintuser', password='testpass')
    project = Project.objects.create(name='Sprint Project', owner=user)
    sprint = Sprint.objects.create(
        name='Sprint One',
        project=project,
        start_date=timezone.now(),
        end_date=timezone.now() + timezone.timedelta(days=7),
        status='planned',
        goal='Build backlog',
        capacity=20,
    )
    client.force_authenticate(user=user)

    response = client.post(reverse('sprint-tasks', args=[sprint.id]), {
        'title': 'Sprint Task',
        'description': 'Task assigned to sprint',
        'priority': 'high',
        'due_date': (timezone.now() + timezone.timedelta(days=2)).isoformat(),
    })

    assert response.status_code == 201
    assert response.data['sprint'] == sprint.id
    assert response.data['priority_quadrant'] == 'urgent_important'


@pytest.mark.django_db
def test_assign_existing_task_to_sprint():
    client = APIClient()
    User = get_user_model()
    user = User.objects.create_user(username='sprintuser2', password='testpass')
    project = Project.objects.create(name='Sprint Project', owner=user)
    sprint = Sprint.objects.create(
        name='Sprint Two',
        project=project,
        start_date=timezone.now(),
        end_date=timezone.now() + timezone.timedelta(days=10),
        status='planned',
        goal='Prepare release',
        capacity=15,
    )
    task = Task.objects.create(owner=user, title='Loose Task', priority='medium')
    client.force_authenticate(user=user)

    response = client.post(
        reverse('sprint-assign-task', args=[sprint.id]),
        {'task_id': task.id},
    )

    assert response.status_code == 200
    assert response.data['sprint'] == sprint.id
    assert Task.objects.get(id=task.id).sprint_id == sprint.id
