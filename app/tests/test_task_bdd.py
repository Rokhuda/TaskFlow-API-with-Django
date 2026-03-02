import pytest
from pytest_bdd import scenarios, given, when, then
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from app.domain.models import Task

scenarios('task.feature')

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(username='bdduser', password='bddpass')
