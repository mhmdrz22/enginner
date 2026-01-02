"""Tests for User model."""

import uuid
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError


User = get_user_model()


class UserModelTests(TestCase):
    """Test suite for custom User model."""

    def test_create_user_with_email(self):
        """Test creating a user with email successfully."""
        uid = uuid.uuid4().hex[:8]
        email = f'test_{uid}@example.com'
        username = f'testuser_{uid}'
        password = 'TestPass123!'
        
        user = User.objects.create_user(
            email=email,
            username=username,
            password=password
        )
        
        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_without_email_raises_error(self):
        """Test that creating user without email raises ValueError."""
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email='',
                username='testuser',
                password='TestPass123!'
            )

    def test_create_superuser(self):
        """Test creating a superuser."""
        uid = uuid.uuid4().hex[:8]
        email = f'admin_{uid}@example.com'
        username = f'admin_{uid}'
        password = 'AdminPass123!'
        
        user = User.objects.create_superuser(
            email=email,
            username=username,
            password=password
        )
        
        self.assertEqual(user.email, email)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_user_str_representation(self):
        """Test user string representation returns email."""
        uid = uuid.uuid4().hex[:8]
        email = f'test_{uid}@example.com'
        user = User.objects.create_user(
            email=email,
            username=f'testuser_{uid}',
            password='TestPass123!'
        )
        
        self.assertEqual(str(user), email)

    def test_user_email_normalized(self):
        """Test email is normalized (lowercase domain)."""
        uid = uuid.uuid4().hex[:8]
        email = f'test_{uid}@EXAMPLE.COM'
        user = User.objects.create_user(
            email=email,
            username=f'testuser_{uid}',
            password='TestPass123!'
        )
        
        self.assertEqual(user.email, email.lower())

    def test_duplicate_email_raises_error(self):
        """Test that duplicate email raises IntegrityError."""
        uid = uuid.uuid4().hex[:8]
        email = f'duplicate_{uid}@example.com'
        
        User.objects.create_user(
            email=email,
            username=f'user1_{uid}',
            password='Pass123!'
        )
        
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email=email,
                username=f'user2_{uid}',
                password='Pass123!'
            )

    def test_user_password_is_hashed(self):
        """Test that password is properly hashed."""
        uid = uuid.uuid4().hex[:8]
        password = 'TestPass123!'
        user = User.objects.create_user(
            email=f'test_{uid}@example.com',
            username=f'testuser_{uid}',
            password=password
        )
        
        self.assertNotEqual(user.password, password)
        self.assertTrue(user.check_password(password))

    def test_user_can_change_password(self):
        """Test user can change password."""
        uid = uuid.uuid4().hex[:8]
        old_password = 'OldPass123!'
        new_password = 'NewPass123!'
        
        user = User.objects.create_user(
            email=f'test_{uid}@example.com',
            username=f'testuser_{uid}',
            password=old_password
        )
        
        user.set_password(new_password)
        user.save()
        
        self.assertFalse(user.check_password(old_password))
        self.assertTrue(user.check_password(new_password))

    def test_inactive_user_creation(self):
        """Test creating inactive user."""
        uid = uuid.uuid4().hex[:8]
        user = User.objects.create_user(
            email=f'inactive_{uid}@example.com',
            username=f'inactive_{uid}',
            password='Pass123!',
            is_active=False
        )
        
        self.assertFalse(user.is_active)

    def test_user_timestamps(self):
        """Test user has created_date and updated_date."""
        uid = uuid.uuid4().hex[:8]
        user = User.objects.create_user(
            email=f'test_{uid}@example.com',
            username=f'testuser_{uid}',
            password='Pass123!'
        )
        
        self.assertIsNotNone(user.created_date)
        self.assertIsNotNone(user.updated_date)
