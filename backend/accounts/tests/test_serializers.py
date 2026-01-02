"""Tests for accounts serializers."""

import uuid
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from accounts.serializers import UserSerializer, RegisterSerializer


User = get_user_model()


class UserSerializerTests(TestCase):
    """Test suite for UserSerializer."""

    def setUp(self):
        """Set up test data."""
        User.objects.all().delete()
        unique_id = uuid.uuid4().hex[:8]
        self.user = User.objects.create_user(
            email=f'test_{unique_id}@example.com',
            username=f'testuser_{unique_id}',
            password='TestPass123!'
        )

    def tearDown(self):
        """Clean up after test."""
        User.objects.all().delete()

    def test_user_serialization(self):
        """Test serializing user data."""
        serializer = UserSerializer(instance=self.user)
        data = serializer.data
        
        self.assertEqual(data['email'], self.user.email)
        self.assertEqual(data['username'], self.user.username)
        self.assertNotIn('password', data)  # Password should not be exposed

    def test_user_deserialization(self):
        """Test deserializing user data."""
        unique_id = uuid.uuid4().hex[:8]
        data = {
            'email': f'new_{unique_id}@example.com',
            'username': f'newuser_{unique_id}'
        }
        serializer = UserSerializer(data=data)
        
        self.assertTrue(serializer.is_valid())


class RegisterSerializerTests(TestCase):
    """Test suite for RegisterSerializer."""

    def setUp(self):
        """Clean database before test."""
        User.objects.all().delete()

    def tearDown(self):
        """Clean up after test."""
        User.objects.all().delete()

    def test_valid_registration_data(self):
        """Test registration with valid data."""
        unique_id = uuid.uuid4().hex[:8]
        data = {
            'email': f'newuser_{unique_id}@example.com',
            'username': f'newuser_{unique_id}',
            'password': 'StrongPass123!',
            'password2': 'StrongPass123!'
        }
        serializer = RegisterSerializer(data=data)
        
        self.assertTrue(serializer.is_valid())

    def test_password_mismatch(self):
        """Test registration fails when passwords don't match."""
        unique_id = uuid.uuid4().hex[:8]
        data = {
            'email': f'test_{unique_id}@example.com',
            'username': f'testuser_{unique_id}',
            'password': 'Pass123!',
            'password2': 'DifferentPass123!'
        }
        serializer = RegisterSerializer(data=data)
        
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_weak_password_validation(self):
        """Test registration fails with weak password."""
        unique_id = uuid.uuid4().hex[:8]
        data = {
            'email': f'test_{unique_id}@example.com',
            'username': f'testuser_{unique_id}',
            'password': '123',
            'password2': '123'
        }
        serializer = RegisterSerializer(data=data)
        
        self.assertFalse(serializer.is_valid())

    def test_invalid_email_format(self):
        """Test registration fails with invalid email."""
        unique_id = uuid.uuid4().hex[:8]
        data = {
            'email': 'invalid-email',
            'username': f'testuser_{unique_id}',
            'password': 'Pass123!',
            'password2': 'Pass123!'
        }
        serializer = RegisterSerializer(data=data)
        
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_duplicate_email_validation(self):
        """Test registration fails with existing email."""
        unique_id = uuid.uuid4().hex[:8]
        email = f'existing_{unique_id}@example.com'
        User.objects.create_user(
            email=email,
            password='pass123'
        )
        
        data = {
            'email': email,
            'username': f'newuser_{unique_id}',
            'password': 'Pass123!',
            'password2': 'Pass123!'
        }
        serializer = RegisterSerializer(data=data)
        
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_create_user_from_serializer(self):
        """Test creating user through serializer."""
        unique_id = uuid.uuid4().hex[:8]
        data = {
            'email': f'create_{unique_id}@example.com',
            'username': f'createuser_{unique_id}',
            'password': 'CreatePass123!',
            'password2': 'CreatePass123!'
        }
        serializer = RegisterSerializer(data=data)
        
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.username, data['username'])
        self.assertTrue(user.check_password('CreatePass123!'))
