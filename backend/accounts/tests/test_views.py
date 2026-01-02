"""Tests for accounts views and API endpoints."""

import uuid
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token


User = get_user_model()


class UserAuthenticationTests(TestCase):
    """Test suite for user authentication endpoints."""

    def setUp(self):
        """Set up test client and user data."""
        User.objects.all().delete()
        Token.objects.all().delete()
        
        self.client = APIClient()
        self.register_url = reverse('accounts:register')
        self.login_url = reverse('accounts:login')
        
        unique_id = uuid.uuid4().hex[:8]
        self.user_data = {
            'email': f'test_{unique_id}@example.com',
            'username': f'testuser_{unique_id}',
            'password': 'TestPass123!',
            'password2': 'TestPass123!'
        }
        
        existing_id = uuid.uuid4().hex[:8]
        self.existing_user = User.objects.create_user(
            email=f'existing_{existing_id}@example.com',
            username=f'existing_{existing_id}',
            password='ExistingPass123!'
        )

    def tearDown(self):
        """Clean up after test."""
        User.objects.all().delete()
        Token.objects.all().delete()

    def test_user_registration_success(self):
        """Test successful user registration."""
        response = self.client.post(
            self.register_url,
            self.user_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertIn('email', response.data['user'])
        self.assertEqual(response.data['user']['email'], self.user_data['email'])
        
        # Verify user was created in database
        user_exists = User.objects.filter(
            email=self.user_data['email']
        ).exists()
        self.assertTrue(user_exists)

    def test_user_registration_with_existing_email(self):
        """Test registration fails with existing email."""
        unique_id = uuid.uuid4().hex[:8]
        data = {
            'email': self.existing_user.email,
            'username': f'newuser_{unique_id}',
            'password': 'Pass123!',
            'password2': 'Pass123!'
        }
        
        response = self.client.post(
            self.register_url,
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_password_mismatch(self):
        """Test registration fails when passwords don't match."""
        data = self.user_data.copy()
        data['password2'] = 'DifferentPass123!'
        
        response = self.client.post(
            self.register_url,
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_missing_fields(self):
        """Test registration fails with missing required fields."""
        unique_id = uuid.uuid4().hex[:8]
        response = self.client.post(
            self.register_url,
            {'email': f'test_{unique_id}@example.com'},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_success(self):
        """Test successful user login."""
        data = {
            'email': self.existing_user.email,
            'password': 'ExistingPass123!'
        }
        
        response = self.client.post(
            self.login_url,
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)

    def test_user_login_invalid_credentials(self):
        """Test login fails with invalid credentials."""
        data = {
            'email': self.existing_user.email,
            'password': 'WrongPassword123!'
        }
        
        response = self.client.post(
            self.login_url,
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_nonexistent_user(self):
        """Test login fails for non-existent user."""
        unique_id = uuid.uuid4().hex[:8]
        data = {
            'email': f'nonexistent_{unique_id}@example.com',
            'password': 'SomePass123!'
        }
        
        response = self.client.post(
            self.login_url,
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AuthenticatedUserTests(TestCase):
    """Test suite for authenticated user endpoints."""

    def setUp(self):
        """Set up authenticated client."""
        User.objects.all().delete()
        Token.objects.all().delete()
        
        self.client = APIClient()
        unique_id = uuid.uuid4().hex[:8]
        self.user = User.objects.create_user(
            email=f'auth_{unique_id}@example.com',
            username=f'authuser_{unique_id}',
            password='AuthPass123!'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.profile_url = reverse('accounts:profile')

    def tearDown(self):
        """Clean up after test."""
        User.objects.all().delete()
        Token.objects.all().delete()

    def test_get_user_profile(self):
        """Test authenticated user can get their profile."""
        response = self.client.get(self.profile_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['username'], self.user.username)

    def test_unauthenticated_profile_access(self):
        """Test unauthenticated user cannot access profile."""
        self.client.credentials()  # Remove authentication
        response = self.client.get(self.profile_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_profile(self):
        """Test user can update their profile."""
        unique_id = uuid.uuid4().hex[:8]
        data = {'username': f'updateduser_{unique_id}'}
        response = self.client.patch(
            self.profile_url,
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, f'updateduser_{unique_id}')
