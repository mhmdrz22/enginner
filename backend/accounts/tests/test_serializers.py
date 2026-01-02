"""Tests for accounts serializers."""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from accounts.serializers import UserSerializer, RegisterSerializer


User = get_user_model()


class UserSerializerTests(TestCase):
    """Test suite for UserSerializer."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='TestPass123!'
        )

    def test_user_serialization(self):
        """Test serializing user data."""
        serializer = UserSerializer(instance=self.user)
        data = serializer.data
        
        self.assertEqual(data['email'], 'test@example.com')
        self.assertEqual(data['username'], 'testuser')
        self.assertNotIn('password', data)  # Password should not be exposed

    def test_user_deserialization(self):
        """Test deserializing user data."""
        data = {
            'email': 'new@example.com',
            'username': 'newuser'
        }
        serializer = UserSerializer(data=data)
        
        self.assertTrue(serializer.is_valid())


class RegisterSerializerTests(TestCase):
    """Test suite for RegisterSerializer."""

    def test_valid_registration_data(self):
        """Test registration with valid data."""
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'StrongPass123!',
            'password2': 'StrongPass123!'
        }
        serializer = RegisterSerializer(data=data)
        
        self.assertTrue(serializer.is_valid())

    def test_password_mismatch(self):
        """Test registration fails when passwords don't match."""
        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'Pass123!',
            'password2': 'DifferentPass123!'
        }
        serializer = RegisterSerializer(data=data)
        
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_weak_password_validation(self):
        """Test registration fails with weak password."""
        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': '123',
            'password2': '123'
        }
        serializer = RegisterSerializer(data=data)
        
        self.assertFalse(serializer.is_valid())

    def test_invalid_email_format(self):
        """Test registration fails with invalid email."""
        data = {
            'email': 'invalid-email',
            'username': 'testuser',
            'password': 'Pass123!',
            'password2': 'Pass123!'
        }
        serializer = RegisterSerializer(data=data)
        
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_duplicate_email_validation(self):
        """Test registration fails with existing email."""
        User.objects.create_user(
            email='existing@example.com',
            password='pass123'
        )
        
        data = {
            'email': 'existing@example.com',
            'username': 'newuser',
            'password': 'Pass123!',
            'password2': 'Pass123!'
        }
        serializer = RegisterSerializer(data=data)
        
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_create_user_from_serializer(self):
        """Test creating user through serializer."""
        data = {
            'email': 'create@example.com',
            'username': 'createuser',
            'password': 'CreatePass123!',
            'password2': 'CreatePass123!'
        }
        serializer = RegisterSerializer(data=data)
        
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        
        self.assertEqual(user.email, 'create@example.com')
        self.assertEqual(user.username, 'createuser')
        self.assertTrue(user.check_password('CreatePass123!'))
