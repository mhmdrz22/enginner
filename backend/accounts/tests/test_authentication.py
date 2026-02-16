from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class AuthenticationTests(TestCase):
    """Test suite for authentication endpoints."""

    def setUp(self):
        """Set up test client and user."""
        self.client = APIClient()
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_register_user(self):
        """Test user registration."""
        url = reverse('register')
        data = {
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['email'], data['email'])
        # Password should not be in response
        self.assertNotIn('password', response.data['user'])

    def test_register_duplicate_email(self):
        """Test registering with existing email fails."""
        url = reverse('register')
        data = {
            'email': self.user_data['email'],  # Duplicate
            'password': 'newpass123',
            'first_name': 'Another',
            'last_name': 'User'
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user(self):
        """Test user login returns JWT tokens."""
        url = reverse('login')
        data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials fails."""
        url = reverse('login')
        data = {
            'email': self.user_data['email'],
            'password': 'wrongpassword'
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profile_authenticated(self):
        """Test getting profile with authentication."""
        self.client.force_authenticate(user=self.user)
        url = reverse('profile')
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_get_profile_unauthenticated(self):
        """Test getting profile without authentication fails."""
        url = reverse('profile')
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_profile(self):
        """Test updating user profile."""
        self.client.force_authenticate(user=self.user)
        url = reverse('profile')
        data = {
            'first_name': 'Updated',
            'last_name': 'Name'
        }
        
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'Name')

    def test_logout(self):
        """Test logout endpoint."""
        self.client.force_authenticate(user=self.user)
        url = reverse('logout')
        
        refresh = RefreshToken.for_user(self.user)
        data = {'refresh': str(refresh)}
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_refresh(self):
        """Test JWT token refresh."""
        refresh = RefreshToken.for_user(self.user)
        url = reverse('token_refresh')
        data = {'refresh': str(refresh)}
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
