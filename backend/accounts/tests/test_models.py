from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

User = get_user_model()


class UserModelTests(TestCase):
    """Test suite for User model."""

    def setUp(self):
        """Set up test data."""
        self.user_data = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpass123'
        }

    def test_create_user(self):
        """Test creating a regular user."""
        user = User.objects.create_user(**self.user_data)
        
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123'
        )
        
        self.assertEqual(user.email, 'admin@example.com')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_email_normalization(self):
        """Test email is normalized."""
        email = 'test@EXAMPLE.COM'
        user = User.objects.create_user(
            email=email,
            password='testpass123'
        )
        
        self.assertEqual(user.email, email.lower())

    def test_email_required(self):
        """Test that email is required."""
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email='',
                password='testpass123'
            )

    def test_unique_email(self):
        """Test that email must be unique."""
        User.objects.create_user(**self.user_data)
        
        with self.assertRaises(IntegrityError):
            User.objects.create_user(**self.user_data)

    def test_user_str_method(self):
        """Test string representation of user."""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), self.user_data['email'])

    def test_full_name_property(self):
        """Test full_name property."""
        user = User.objects.create_user(**self.user_data)
        expected_full_name = f"{self.user_data['first_name']} {self.user_data['last_name']}"
        self.assertEqual(user.full_name, expected_full_name)

    def test_full_name_with_empty_names(self):
        """Test full_name when names are empty."""
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.full_name, '')

    def test_user_ordering(self):
        """Test default ordering of users."""
        user1 = User.objects.create_user(
            email='user1@example.com',
            password='pass123'
        )
        user2 = User.objects.create_user(
            email='user2@example.com',
            password='pass123'
        )
        
        users = User.objects.all()
        # Should be ordered by date_joined descending
        self.assertEqual(users[0], user2)
        self.assertEqual(users[1], user1)
