"""Tests for User model."""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError


User = get_user_model()


class UserModelTests(TestCase):
    """Test suite for User model."""

    def setUp(self):
        """Set up test data."""
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'TestPass123!'
        }

    def test_create_user_with_email(self):
        """Test creating a user with email successfully."""
        user = User.objects.create_user(
            email=self.user_data['email'],
            password=self.user_data['password'],
            username=self.user_data['username']
        )
        
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.username, self.user_data['username'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_verified)

    def test_create_user_without_email_raises_error(self):
        """Test that creating user without email raises ValueError."""
        with self.assertRaises(ValueError) as context:
            User.objects.create_user(email='', password='testpass123')
        
        self.assertIn('Email is required', str(context.exception))

    def test_create_superuser(self):
        """Test creating a superuser."""
        admin = User.objects.create_superuser(
            email='admin@example.com',
            password='AdminPass123!',
            username='admin'
        )
        
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_active)
        self.assertTrue(admin.is_verified)

    def test_user_email_normalized(self):
        """Test email is normalized (lowercase domain)."""
        email = 'test@EXAMPLE.COM'
        user = User.objects.create_user(
            email=email,
            password='testpass123'
        )
        
        self.assertEqual(user.email, 'test@example.com')

    def test_duplicate_email_raises_error(self):
        """Test that duplicate email raises IntegrityError."""
        User.objects.create_user(
            email='duplicate@example.com',
            password='pass123'
        )
        
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email='duplicate@example.com',
                password='pass456'
            )

    def test_user_str_representation(self):
        """Test user string representation returns email."""
        user = User.objects.create_user(
            email='test@example.com',
            password='pass123'
        )
        
        self.assertEqual(str(user), 'test@example.com')

    def test_user_password_is_hashed(self):
        """Test that password is properly hashed."""
        user = User.objects.create_user(
            email='test@example.com',
            password='plainpassword'
        )
        
        self.assertNotEqual(user.password, 'plainpassword')
        self.assertTrue(user.password.startswith('pbkdf2_sha256'))

    def test_user_can_change_password(self):
        """Test user can change password."""
        user = User.objects.create_user(
            email='test@example.com',
            password='oldpass123'
        )
        
        old_password_hash = user.password
        user.set_password('newpass456')
        user.save()
        
        self.assertNotEqual(user.password, old_password_hash)
        self.assertTrue(user.check_password('newpass456'))
        self.assertFalse(user.check_password('oldpass123'))

    def test_inactive_user_creation(self):
        """Test creating inactive user."""
        user = User.objects.create_user(
            email='inactive@example.com',
            password='pass123',
            is_active=False
        )
        
        self.assertFalse(user.is_active)

    def test_user_timestamps(self):
        """Test user has created_date and updated_date."""
        user = User.objects.create_user(
            email='timestamp@example.com',
            password='pass123'
        )
        
        self.assertIsNotNone(user.created_date)
        self.assertIsNotNone(user.updated_date)
        self.assertEqual(user.created_date.date(), user.updated_date.date())
