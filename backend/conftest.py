"""Pytest configuration and global fixtures."""

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from tasks.models import Task


User = get_user_model()


@pytest.fixture
def api_client():
    """Return API client for tests."""
    return APIClient()


@pytest.fixture
def user(db):
    """Create and return a regular user."""
    return User.objects.create_user(
        email='testuser@example.com',
        username='testuser',
        password='TestPass123!'
    )


@pytest.fixture
def another_user(db):
    """Create and return another user for isolation tests."""
    return User.objects.create_user(
        email='another@example.com',
        username='anotheruser',
        password='AnotherPass123!'
    )


@pytest.fixture
def superuser(db):
    """Create and return a superuser."""
    return User.objects.create_superuser(
        email='admin@example.com',
        username='admin',
        password='AdminPass123!'
    )


@pytest.fixture
def user_token(user):
    """Create and return authentication token for user."""
    token, created = Token.objects.get_or_create(user=user)
    return token


@pytest.fixture
def authenticated_client(api_client, user_token):
    """Return authenticated API client."""
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {user_token.key}')
    return api_client


@pytest.fixture
def task(user):
    """Create and return a sample task."""
    return Task.objects.create(
        user=user,
        title='Test Task',
        description='Test task description',
        status='TODO',
        priority='MEDIUM'
    )


@pytest.fixture
def multiple_tasks(user):
    """Create and return multiple tasks."""
    tasks = []
    for i in range(5):
        task = Task.objects.create(
            user=user,
            title=f'Task {i + 1}',
            description=f'Description {i + 1}',
            status=['TODO', 'DOING', 'DONE'][i % 3],
            priority=['LOW', 'MEDIUM', 'HIGH'][i % 3]
        )
        tasks.append(task)
    return tasks


@pytest.fixture
def task_data():
    """Return sample task data for creation."""
    return {
        'title': 'New Task',
        'description': 'New task description',
        'status': 'TODO',
        'priority': 'HIGH'
    }


@pytest.fixture
def user_data():
    """Return sample user data for registration."""
    return {
        'email': 'newuser@example.com',
        'username': 'newuser',
        'password': 'NewPass123!',
        'password2': 'NewPass123!'
    }
