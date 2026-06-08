import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.utils import timezone
from app.domain.models import Project, Sprint


@pytest.mark.django_db
def test_sprint_crud_and_metrics():
    client = APIClient()
    User = get_user_model()
    user = User.objects.create_user(username='sprintuser', password='testpass')
    project = Project.objects.create(name='Test Project', owner=user)
    client.force_authenticate(user=user)

    start_date = timezone.now()
    end_date = start_date + timezone.timedelta(days=7)

    response = client.post(reverse('sprint-list'), {
        'name': 'Sprint 1',
        'project': project.id,
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
        'status': 'planned',
        'goal': 'Deliver MVP backlog items',
        'capacity': 20,
    })
    assert response.status_code == 201
    sprint_id = response.data['id']

    response = client.get(reverse('sprint-detail', args=[sprint_id]))
    assert response.status_code == 200
    assert response.data['name'] == 'Sprint 1'
    assert response.data['task_count'] == 0

    response = client.get(reverse('sprint-metrics', args=[sprint_id]))
    assert response.status_code == 200
    assert response.data['total_tasks'] == 0
    assert response.data['completed_tasks'] == 0
    assert response.data['remaining_story_points'] == 0

    response = client.patch(reverse('sprint-detail', args=[sprint_id]), {'status': 'active'})
    assert response.status_code == 200
    assert response.data['status'] == 'active'
