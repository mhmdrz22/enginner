"""Tests to verify fixtures work correctly."""

import pytest
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from tasks.models import Task


User = get_user_model()


@pytest.mark.django_db
def test_user_fixture(user):
    """Test user fixture creates valid user."""
    assert user.email == 'testuser@example.com'
    assert user.username == 'testuser'
    assert user.check_password('TestPass123!')
    assert user.is_active
    assert not user.is_staff


@pytest.mark.django_db
def test_another_user_fixture(another_user):
    """Test another_user fixture creates different user."""
    assert another_user.email == 'another@example.com'
    assert another_user.username == 'anotheruser'


@pytest.mark.django_db
def test_superuser_fixture(superuser):
    """Test superuser fixture creates admin user."""
    assert superuser.is_staff
    assert superuser.is_superuser
    assert superuser.email == 'admin@example.com'


@pytest.mark.django_db
def test_user_token_fixture(user_token, user):
    """Test token fixture creates valid token."""
    assert user_token.user == user
    assert Token.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_authenticated_client_fixture(authenticated_client):
    """Test authenticated client has credentials."""
    assert 'HTTP_AUTHORIZATION' in authenticated_client._credentials


@pytest.mark.django_db
def test_task_fixture(task, user):
    """Test task fixture creates valid task."""
    assert task.user == user
    assert task.title == 'Test Task'
    assert task.status == 'TODO'
    assert task.priority == 'MEDIUM'


@pytest.mark.django_db
def test_multiple_tasks_fixture(multiple_tasks, user):
    """Test multiple_tasks fixture creates 5 tasks."""
    assert len(multiple_tasks) == 5
    for task in multiple_tasks:
        assert task.user == user
        assert Task.objects.filter(id=task.id).exists()


def test_task_data_fixture(task_data):
    """Test task_data fixture returns valid dict."""
    assert 'title' in task_data
    assert 'description' in task_data
    assert 'status' in task_data
    assert 'priority' in task_data


def test_user_data_fixture(user_data):
    """Test user_data fixture returns valid dict."""
    assert 'email' in user_data
    assert 'username' in user_data
    assert 'password' in user_data
    assert 'password2' in user_data
