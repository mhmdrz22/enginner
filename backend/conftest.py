import pytest
from django.conf import settings

# Configure Django settings for pytest

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Enable database access for all tests."""
    pass


@pytest.fixture
def api_client():
    """Provide API client for tests."""
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def user(db):
    """Create a test user."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    return User.objects.create_user(
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def admin_user(db):
    """Create an admin user."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    return User.objects.create_superuser(
        email='admin@example.com',
        password='adminpass123'
    )
