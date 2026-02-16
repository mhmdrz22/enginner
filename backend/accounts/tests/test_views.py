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
        """Set up test client and user data with unique identifiers."""
        self.client = APIClient()
        self.register_url = reverse('accounts:register')
        self.login_url = reverse('accounts:login')
        
        # Generate unique IDs
        uid_new = uuid.uuid4().hex[:8]
        uid_existing = uuid.uuid4().hex[:8]
        
        self.user_data = {
            'email': f'test_{uid_new}@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'TestPass123!',
            'password2': 'TestPass123!'
        }
        
        self.existing_user = User.objects.create_user(
            email=f'existing_{uid_existing}@example.com',
            password='ExistingPass123!',
            first_name='Existing',
            last_name='User'
        )

    def test_user_registration_success(self):
        """Test successful user registration."""
        response = self.client.post(
            self.register_url,
            self.user_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['user']['email'], self.user_data['email'])
        
        # Verify user was created in database
        user_exists = User.objects.filter(
            email=self.user_data['email']
        ).exists()
        self.assertTrue(user_exists)

    def test_user_registration_with_existing_email(self):
        """Test registration fails with existing email."""
        data = {
            'email': self.existing_user.email,  # Use existing email
            'first_name': 'New',
            'last_name': 'User',
            'password': 'Pass123!',
            'password2': 'Pass123!'
        }
        
        response = self.client.post(
            self.register_url,
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

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
        self.assertIn('password', response.data)

    def test_user_registration_missing_fields(self):
        """Test registration fails with missing required fields."""
        uid = uuid.uuid4().hex[:8]
        response = self.client.post(
            self.register_url,
            {'email': f'test_{uid}@example.com'},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_success(self):
        """Test successful user login returns token."""
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
        
        # Verify token exists in database
        token_exists = Token.objects.filter(user=self.existing_user).exists()
        self.assertTrue(token_exists)

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
        self.assertIn('error', response.data)

    def test_user_login_nonexistent_user(self):
        """Test login fails for non-existent user."""
        uid = uuid.uuid4().hex[:8]
        data = {
            'email': f'nonexistent_{uid}@example.com',
            'password': 'SomePass123!'
        }
        
        response = self.client.post(
            self.login_url,
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)


class AuthenticatedUserTests(TestCase):
    """Test suite for authenticated user endpoints."""

    def setUp(self):
        """Set up authenticated client with unique user."""
        self.client = APIClient()
        uid = uuid.uuid4().hex[:8]
        self.user = User.objects.create_user(
            email=f'auth_{uid}@example.com',
            password='AuthPass123!',
            first_name='Auth',
            last_name='User'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.profile_url = reverse('accounts:profile')
        self.logout_url = reverse('accounts:logout')

    def test_get_user_profile(self):
        """Test authenticated user can get their profile."""
        response = self.client.get(self.profile_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['first_name'], self.user.first_name)
        self.assertEqual(response.data['last_name'], self.user.last_name)
        self.assertIn('full_name', response.data)

    def test_unauthenticated_profile_access(self):
        """Test unauthenticated user cannot access profile."""
        self.client.credentials()  # Remove authentication
        response = self.client.get(self.profile_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_profile(self):
        """Test user can update their profile."""
        data = {
            'first_name': 'Updated',
            'last_name': 'Name'
        }
        response = self.client.patch(
            self.profile_url,
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'Name')

    def test_logout(self):
        """Test user can logout and token is deleted."""
        response = self.client.post(self.logout_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        
        # Verify token was deleted
        token_exists = Token.objects.filter(user=self.user).exists()
        self.assertFalse(token_exists)
