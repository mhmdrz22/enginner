from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

User = get_user_model()

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_register_user(self):
        url = reverse('accounts:register')
        data = {
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password2': 'newpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['email'], data['email'])

    def test_register_duplicate_email(self):
        url = reverse('accounts:register')
        data = {
            'email': self.user_data['email'],
            'password': 'newpass123',
            'password2': 'newpass123',
            'first_name': 'Another',
            'last_name': 'User'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user(self):
        """Test user login returns Token."""
        url = reverse('accounts:login')
        data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)

    def test_login_invalid_credentials(self):
        url = reverse('accounts:login')
        data = {'email': self.user_data['email'], 'password': 'wrongpassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profile_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('accounts:profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_get_profile_unauthenticated(self):
        url = reverse('accounts:profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_profile(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('accounts:profile')
        data = {'first_name': 'Updated', 'last_name': 'Name'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')

    def test_logout(self):
        """Test logout endpoint."""
        Token.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)
        
        url = reverse('accounts:logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
