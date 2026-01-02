"""Tests for accounts serializers."""

import uuid
from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.serializers import RegisterSerializer, UserSerializer


User = get_user_model()


class RegisterSerializerTests(TestCase):
    """Test suite for RegisterSerializer."""

    def test_valid_registration_data(self):
        """Test registration with valid data."""
        uid = uuid.uuid4().hex[:8]
        data = {
            'email': f'test_{uid}@example.com',
            'username': f'testuser_{uid}',
            'password': 'StrongPass123!',
            'password2': 'StrongPass123!'
        }
        
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_password_mismatch(self):
        """Test registration fails when passwords don't match."""
        uid = uuid.uuid4().hex[:8]
        data = {
            'email': f'test_{uid}@example.com',
            'username': f'testuser_{uid}',
            'password': 'Pass123!',
            'password2': 'DifferentPass123!'
        }
        
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_invalid_email_format(self):
        """Test registration fails with invalid email."""
        uid = uuid.uuid4().hex[:8]
        data = {
            'email': 'invalid-email',
            'username': f'testuser_{uid}',
            'password': 'Pass123!',
            'password2': 'Pass123!'
        }
        
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_weak_password_validation(self):
        """Test registration fails with weak password."""
        uid = uuid.uuid4().hex[:8]
        data = {
            'email': f'test_{uid}@example.com',
            'username': f'testuser_{uid}',
            'password': '123',
            'password2': '123'
        }
        
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_duplicate_email_validation(self):
        """Test registration fails with existing email."""
        uid = uuid.uuid4().hex[:8]
        email = f'existing_{uid}@example.com'
        
        User.objects.create_user(
            email=email,
            username=f'existing_{uid}',
            password='Pass123!'
        )
        
        data = {
            'email': email,
            'username': f'newuser_{uid}',
            'password': 'Pass123!',
            'password2': 'Pass123!'
        }
        
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_create_user_from_serializer(self):
        """Test creating user through serializer."""
        uid = uuid.uuid4().hex[:8]
        data = {
            'email': f'test_{uid}@example.com',
            'username': f'testuser_{uid}',
            'password': 'Pass123!',
            'password2': 'Pass123!'
        }
        
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        user = serializer.save()
        self.assertEqual(user.email, data['email'])
        self.assertTrue(user.check_password(data['password']))


class UserSerializerTests(TestCase):
    """Test suite for UserSerializer."""

    def setUp(self):
        """Set up test user."""
        uid = uuid.uuid4().hex[:8]
        self.user = User.objects.create_user(
            email=f'test_{uid}@example.com',
            username=f'testuser_{uid}',
            password='Pass123!'
        )

    def test_user_serialization(self):
        """Test serializing user data."""
        serializer = UserSerializer(self.user)
        data = serializer.data
        
        self.assertEqual(data['email'], self.user.email)
        self.assertEqual(data['username'], self.user.username)
        self.assertNotIn('password', data)

    def test_user_deserialization(self):
        """Test deserializing user data."""
        uid = uuid.uuid4().hex[:8]
        data = {
            'email': f'new_{uid}@example.com',
            'username': f'newuser_{uid}'
        }
        
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
