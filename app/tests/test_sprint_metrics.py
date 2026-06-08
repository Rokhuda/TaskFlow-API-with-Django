import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.utils import timezone
from app.domain.models import Project, Sprint, Task


@pytest.mark.django_db
def test_sprint_burndown_and_actions():
    client = APIClient()
    User = get_user_model()
    user = User.objects.create_user(username='metricuser', password='testpass')
    project = Project.objects.create(name='Metrics Project', owner=user)
    sprint = Sprint.objects.create(
        name='Metrics Sprint',
        project=project,
        start_date=timezone.now(),
        end_date=timezone.now() + timezone.timedelta(days=5),
        status='planned',
        goal='Track progress',
        capacity=20,
    )
    task = Task.objects.create(owner=user, title='Metric Task', priority='high', story_points=5, sprint=sprint)
    client.force_authenticate(user=user)

    response = client.post(reverse('sprint-start', args=[sprint.id]))
    assert response.status_code == 200
    assert response.data['status'] == 'active'

    response = client.get(reverse('sprint-burndown', args=[sprint.id]))
    assert response.status_code == 200
    assert 'burndown_data' in response.data
    assert response.data['burndown_data'][0]['remaining_story_points'] >= response.data['burndown_data'][-1]['remaining_story_points']

    response = client.post(reverse('sprint-complete', args=[sprint.id]))
    assert response.status_code == 200
    assert response.data['status'] == 'completed'


@pytest.mark.django_db
def test_blocked_task_cannot_complete():
    client = APIClient()
    User = get_user_model()
    user = User.objects.create_user(username='blockeruser', password='testpass')
    project = Project.objects.create(name='Blocker Project', owner=user)
    task_a = Task.objects.create(owner=user, title='Blocking Task', priority='high')
    task_b = Task.objects.create(owner=user, title='Blocked Task', priority='medium')
    task_b.blocked_by.add(task_a)

    client.force_authenticate(user=user)
    response = client.patch(reverse('task-detail', args=[task_b.id]), {'completed': True})
    assert response.status_code == 400
    assert 'Cannot complete a task while its blockers are incomplete.' in str(response.data)
