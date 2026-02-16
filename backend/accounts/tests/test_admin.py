import uuid
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from tasks.models import Task
from unittest.mock import patch

User = get_user_model()

class AdminOverviewTests(TestCase):
    """Tests for admin overview endpoint."""

    def setUp(self):
        self.client = APIClient()
        self.overview_url = reverse('admin-overview')
        
        # Generate unique IDs
        uid_user = uuid.uuid4().hex[:8]
        uid_admin = uuid.uuid4().hex[:8]
        
        # Create regular user
        self.user = User.objects.create_user(
            email=f'user_{uid_user}@example.com',
            password='UserPass123!',
            first_name='Test',
            last_name='User'
        )
        
        # Create admin user
        self.admin = User.objects.create_superuser(
            email=f'admin_{uid_admin}@example.com',
            password='AdminPass123!',
            first_name='Admin',
            last_name='User'
        )
        
        # Create tasks
        Task.objects.create(user=self.user, title='Task 1', status='TODO')
        Task.objects.create(user=self.user, title='Task 2', status='DONE')

    def test_overview_requires_authentication(self):
        response = self.client.get(self.overview_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_overview_requires_admin(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.overview_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_overview_success_for_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.overview_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('users', response.data)

    def test_overview_includes_user_data(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.overview_url)
        
        users = response.data['users']
        user_data = next((u for u in users if u['email'] == self.user.email), None)
        
        self.assertIsNotNone(user_data)
        self.assertEqual(user_data['total_tasks'], 2)
        # Check filtered counts
        self.assertEqual(user_data['open_tasks'], 1)

    def test_overview_structure(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.overview_url)
        self.assertIsInstance(response.data['users'], list)


class AdminNotifyTests(TestCase):
    """Tests for admin notify endpoint."""

    def setUp(self):
        self.client = APIClient()
        self.notify_url = reverse('admin-notify')
        
        uid_user = uuid.uuid4().hex[:8]
        uid_admin = uuid.uuid4().hex[:8]
        
        self.user = User.objects.create_user(
            email=f'user_{uid_user}@example.com',
            password='UserPass123!',
            first_name='Test',
            last_name='User'
        )
        
        self.admin = User.objects.create_superuser(
            email=f'admin_{uid_admin}@example.com',
            password='AdminPass123!',
            first_name='Admin',
            last_name='User'
        )

    def test_notify_requires_authentication(self):
        response = self.client.post(self.notify_url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_notify_requires_admin(self):
        self.client.force_authenticate(user=self.user)
        uid = uuid.uuid4().hex[:8]
        response = self.client.post(self.notify_url, {
            'recipients': [f'test_{uid}@example.com'],
            'message': 'Test message'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch('accounts.views.send_email_task.apply_async')
    def test_notify_success(self, mock_task):
        mock_task.return_value.id = 'test-task-id'
        
        self.client.force_authenticate(user=self.admin)
        uid1 = uuid.uuid4().hex[:8]
        uid2 = uuid.uuid4().hex[:8]
        response = self.client.post(self.notify_url, {
            'recipients': [f'user1_{uid1}@example.com', f'user2_{uid2}@example.com'],
            'subject': 'Test Subject',
            'message': 'Test message'
        })
        
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIn('job_id', response.data)
        
        mock_task.assert_called_once()

    def test_notify_requires_recipients(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.notify_url, {
            'message': 'Test message'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_notify_requires_message(self):
        self.client.force_authenticate(user=self.admin)
        uid = uuid.uuid4().hex[:8]
        response = self.client.post(self.notify_url, {
            'recipients': [f'test_{uid}@example.com']
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
