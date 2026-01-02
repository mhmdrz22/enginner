"""Test utility functions."""

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from tasks.models import Task


User = get_user_model()


class TestHelpers:
    """Helper methods for tests."""

    @staticmethod
    def create_test_user(email='test@example.com', **kwargs):
        """Helper to create test user."""
        defaults = {
            'username': email.split('@')[0],
            'password': 'TestPass123!'
        }
        defaults.update(kwargs)
        return User.objects.create_user(email=email, **defaults)

    @staticmethod
    def create_test_task(user, **kwargs):
        """Helper to create test task."""
        defaults = {
            'title': 'Test Task',
            'status': 'TODO',
            'priority': 'MEDIUM'
        }
        defaults.update(kwargs)
        return Task.objects.create(user=user, **defaults)

    @staticmethod
    def get_future_date(days=7):
        """Helper to get future date."""
        return timezone.now().date() + timedelta(days=days)

    @staticmethod
    def get_past_date(days=7):
        """Helper to get past date."""
        return timezone.now().date() - timedelta(days=days)


@pytest.mark.django_db
class TestHelpersTests:
    """Tests for test helpers."""

    def test_create_test_user(self):
        """Test create_test_user helper."""
        user = TestHelpers.create_test_user('helper@example.com')
        
        assert user.email == 'helper@example.com'
        assert user.username == 'helper'
        assert user.check_password('TestPass123!')

    def test_create_test_task(self, user):
        """Test create_test_task helper."""
        task = TestHelpers.create_test_task(
            user,
            title='Helper Task',
            priority='HIGH'
        )
        
        assert task.title == 'Helper Task'
        assert task.priority == 'HIGH'
        assert task.user == user

    def test_get_future_date(self):
        """Test get_future_date helper."""
        future = TestHelpers.get_future_date(7)
        today = timezone.now().date()
        
        assert future > today
        assert (future - today).days == 7

    def test_get_past_date(self):
        """Test get_past_date helper."""
        past = TestHelpers.get_past_date(7)
        today = timezone.now().date()
        
        assert past < today
        assert (today - past).days == 7


@pytest.mark.django_db
class TestDataValidation:
    """Test data validation utilities."""

    def test_email_validation(self):
        """Test email validation."""
        with pytest.raises(ValidationError):
            user = User(email='invalid-email', username='test')
            user.full_clean()

    def test_required_fields(self):
        """Test required field validation."""
        with pytest.raises(ValidationError):
            user = User(username='test')  # Missing email
            user.full_clean()

    def test_task_title_max_length(self):
        """Test task title max length validation."""
        user = TestHelpers.create_test_user()
        
        # Title max length is 200
        long_title = 'x' * 201
        
        with pytest.raises(ValidationError):
            task = Task(user=user, title=long_title)
            task.full_clean()
