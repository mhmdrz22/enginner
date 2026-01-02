"""Tests for custom authentication backend."""

import uuid
from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate
from accounts.backends import EmailBackend


User = get_user_model()


class EmailBackendTests(TestCase):
    """Test suite for email authentication backend."""

    def setUp(self):
        """Set up test user."""
        User.objects.all().delete()
        self.backend = EmailBackend()
        unique_id = uuid.uuid4().hex[:8]
        self.user = User.objects.create_user(
            email=f'auth_{unique_id}@example.com',
            username=f'authuser_{unique_id}',
            password='AuthPass123!'
        )

    def tearDown(self):
        """Clean up after test."""
        User.objects.all().delete()

    def test_authenticate_with_valid_email_and_password(self):
        """Test authentication with correct email and password."""
        user = authenticate(
            request=None,
            username=self.user.email,
            password='AuthPass123!'
        )
        
        self.assertIsNotNone(user)
        self.assertEqual(user.email, self.user.email)

    def test_authenticate_with_invalid_password(self):
        """Test authentication fails with wrong password."""
        user = authenticate(
            request=None,
            username=self.user.email,
            password='WrongPassword'
        )
        
        self.assertIsNone(user)

    def test_authenticate_with_nonexistent_email(self):
        """Test authentication fails with non-existent email."""
        unique_id = uuid.uuid4().hex[:8]
        user = authenticate(
            request=None,
            username=f'nonexistent_{unique_id}@example.com',
            password='SomePassword'
        )
        
        self.assertIsNone(user)

    def test_authenticate_with_inactive_user(self):
        """Test authentication fails for inactive user."""
        self.user.is_active = False
        self.user.save()
        
        user = authenticate(
            request=None,
            username=self.user.email,
            password='AuthPass123!'
        )
        
        self.assertIsNone(user)

    def test_get_user_by_id(self):
        """Test retrieving user by ID."""
        user = self.backend.get_user(self.user.id)
        
        self.assertIsNotNone(user)
        self.assertEqual(user.id, self.user.id)

    def test_get_nonexistent_user(self):
        """Test retrieving non-existent user returns None."""
        user = self.backend.get_user(99999)
        
        self.assertIsNone(user)
