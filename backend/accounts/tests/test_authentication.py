"""Tests for authentication backend."""

import uuid
from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.backends import EmailBackend


User = get_user_model()


class EmailBackendTests(TestCase):
    """Test suite for email authentication backend."""

    def setUp(self):
        """Set up test user and backend."""
        self.backend = EmailBackend()
        uid = uuid.uuid4().hex[:8]
        self.user = User.objects.create_user(
            email=f'test_{uid}@example.com',
            username=f'testuser_{uid}',
            password='TestPass123!'
        )

    def test_authenticate_with_valid_email_and_password(self):
        """Test authentication with correct email and password."""
        user = self.backend.authenticate(
            request=None,
            username=self.user.email,
            password='TestPass123!'
        )
        
        self.assertEqual(user, self.user)

    def test_authenticate_with_invalid_password(self):
        """Test authentication fails with wrong password."""
        user = self.backend.authenticate(
            request=None,
            username=self.user.email,
            password='WrongPassword123!'
        )
        
        self.assertIsNone(user)

    def test_authenticate_with_nonexistent_email(self):
        """Test authentication fails with non-existent email."""
        uid = uuid.uuid4().hex[:8]
        user = self.backend.authenticate(
            request=None,
            username=f'nonexistent_{uid}@example.com',
            password='SomePass123!'
        )
        
        self.assertIsNone(user)

    def test_authenticate_with_inactive_user(self):
        """Test authentication fails for inactive user."""
        self.user.is_active = False
        self.user.save()
        
        user = self.backend.authenticate(
            request=None,
            username=self.user.email,
            password='TestPass123!'
        )
        
        self.assertIsNone(user)

    def test_get_user_by_id(self):
        """Test retrieving user by ID."""
        user = self.backend.get_user(self.user.id)
        
        self.assertEqual(user, self.user)

    def test_get_nonexistent_user(self):
        """Test retrieving non-existent user returns None."""
        user = self.backend.get_user(99999)
        
        self.assertIsNone(user)
