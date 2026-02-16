"""Global pytest fixtures for the entire backend."""
import pytest
from rest_framework.test import APIClient
from accounts.models import User


@pytest.fixture
def api_client():
    """Fixture to provide DRF APIClient."""
    return APIClient()


@pytest.fixture
def create_user(db):
    """Factory fixture for creating test users.
    
    Usage:
        user = create_user()
        user = create_user(email='custom@example.com', first_name='John')
    """
    def _create_user(
        email='test@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User',
        **kwargs
    ):
        return User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            **kwargs
        )
    return _create_user


@pytest.fixture
def authenticated_client(api_client, create_user):
    """Fixture to provide an authenticated APIClient with a user.
    
    Returns:
        tuple: (APIClient, User) - authenticated client and the user
    """
    user = create_user()
    api_client.force_authenticate(user=user)
    return api_client, user


@pytest.fixture
def admin_user(create_user):
    """Fixture to create an admin user."""
    return create_user(
        email='admin@example.com',
        first_name='Admin',
        last_name='User',
        is_staff=True,
        is_superuser=True
    )


@pytest.fixture
def authenticated_admin_client(api_client, admin_user):
    """Fixture to provide an authenticated admin APIClient.
    
    Returns:
        tuple: (APIClient, User) - authenticated admin client and admin user
    """
    api_client.force_authenticate(user=admin_user)
    return api_client, admin_user
