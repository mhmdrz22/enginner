import uuid
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    """Provides a REST framework test client"""
    return APIClient()


@pytest.fixture
def unique_email():
    """Generate unique email for each test"""
    unique_id = uuid.uuid4().hex[:8]
    return f'test_{unique_id}@example.com'


@pytest.fixture
def user_factory(db):
    """Factory for creating test users with unique emails"""
    def _create_user(
        email=None,
        password='TestPass123!',
        first_name='Test',
        last_name='User',
        is_staff=False,
        is_superuser=False,
        **extra_fields
    ):
        # Generate unique email if not provided
        if email is None:
            unique_id = uuid.uuid4().hex[:8]
            email = f'test_{unique_id}@example.com'
        
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
        
        if is_superuser:
            user.is_staff = True
            user.is_superuser = True
        
        user.save()
        
        # Store raw password for login tests
        user.raw_password = password
        return user
    
    return _create_user


@pytest.fixture
def user(user_factory):
    """Create a single test user"""
    return user_factory()


@pytest.fixture
def authenticated_client(api_client, user):
    """Provides an authenticated API client"""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_user(user_factory):
    """Create an admin user"""
    unique_id = uuid.uuid4().hex[:8]
    return user_factory(
        email=f'admin_{unique_id}@example.com',
        is_staff=True,
        is_superuser=True
    )


@pytest.fixture
def admin_client(api_client, admin_user):
    """Provides an admin authenticated API client"""
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def multiple_users(user_factory):
    """Creates multiple test users with unique emails"""
    users = []
    for i in range(3):
        unique_id = uuid.uuid4().hex[:8]
        user = user_factory(
            email=f'user_{unique_id}_{i}@example.com',
            first_name=f'User{i}',
            last_name=f'Test{i}'
        )
        users.append(user)
    return users


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Enable database access for all tests automatically"""
    pass
