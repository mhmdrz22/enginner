import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    """Provides a REST framework test client"""
    return APIClient()


@pytest.fixture
def user_factory():
    """Factory for creating test users without username"""
    def _create_user(
        email='test@example.com',
        password='TestPass123!',
        first_name='Test',
        last_name='User',
        is_staff=False,
        is_admin=False,
        **extra_fields
    ):
        # Remove username if accidentally passed
        extra_fields.pop('username', None)
        
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        
        if is_staff:
            user.is_staff = True
            user.save()
        
        if is_admin:
            user.is_staff = True
            user.is_admin = True
            user.save()
        
        # Store raw password for login tests
        user.raw_password = password
        return user
    
    return _create_user


@pytest.fixture
def authenticated_client(api_client, user_factory):
    """Provides an authenticated API client"""
    user = user_factory()
    api_client.force_authenticate(user=user)
    return api_client, user


@pytest.fixture
def admin_client(api_client, user_factory):
    """Provides an admin authenticated API client"""
    admin = user_factory(
        email='admin@example.com',
        is_staff=True,
        is_admin=True
    )
    api_client.force_authenticate(user=admin)
    return api_client, admin


@pytest.fixture
def multiple_users(user_factory):
    """Creates multiple test users"""
    users = []
    for i in range(3):
        user = user_factory(
            email=f'user{i}@example.com',
            first_name=f'User{i}',
            last_name=f'Test{i}'
        )
        users.append(user)
    return users
