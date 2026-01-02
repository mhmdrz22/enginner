"""Tests for custom authentication backend."""

from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate
from accounts.authenticator import EmailBackend


User = get_user_model()


class EmailBackendTests(TestCase):
    """Test suite for email authentication backend."""

    def setUp(self):
        """Set up test user."""
        self.backend = EmailBackend()
        self.user = User.objects.create_user(
            email='auth@example.com',
            username='authuser',
            password='AuthPass123!'
        )

    def test_authenticate_with_valid_email_and_password(self):
        """Test authentication with correct email and password."""
        user = authenticate(
            request=None,
            username='auth@example.com',
            password='AuthPass123!'
        )
        
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'auth@example.com')

    def test_authenticate_with_invalid_password(self):
        """Test authentication fails with wrong password."""
        user = authenticate(
            request=None,
            username='auth@example.com',
            password='WrongPassword'
        )
        
        self.assertIsNone(user)

    def test_authenticate_with_nonexistent_email(self):
        """Test authentication fails with non-existent email."""
        user = authenticate(
            request=None,
            username='nonexistent@example.com',
            password='SomePassword'
        )
        
        self.assertIsNone(user)

    def test_authenticate_with_inactive_user(self):
        """Test authentication fails for inactive user."""
        self.user.is_active = False
        self.user.save()
        
        user = authenticate(
            request=None,
            username='auth@example.com',
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
