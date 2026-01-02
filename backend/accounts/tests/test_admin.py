from django.test import TestCase
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
        
        # Create regular user
        self.user = User.objects.create_user(
            email='user@example.com',
            username='user',
            password='UserPass123!'
        )
        
        # Create admin user
        self.admin = User.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='AdminPass123!'
        )
        
        # Create tasks for user
        Task.objects.create(
            user=self.user,
            title='Task 1',
            status='TODO'
        )
        Task.objects.create(
            user=self.user,
            title='Task 2',
            status='DONE'
        )

    def test_overview_requires_authentication(self):
        """Test that overview endpoint requires authentication."""
        response = self.client.get('/api/accounts/admin/overview/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_overview_requires_admin(self):
        """Test that regular user cannot access overview."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/accounts/admin/overview/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_overview_success_for_admin(self):
        """Test that admin can access overview."""
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/api/accounts/admin/overview/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('users', response.data)
        self.assertIn('total_users', response.data)
        self.assertIn('active_users', response.data)

    def test_overview_includes_user_data(self):
        """Test that overview includes correct user data."""
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/api/accounts/admin/overview/')
        
        users = response.data['users']
        user_data = next((u for u in users if u['email'] == 'user@example.com'), None)
        
        self.assertIsNotNone(user_data)
        self.assertEqual(user_data['total_tasks'], 2)
        self.assertEqual(user_data['open_tasks'], 1)  # Only TODO task

    def test_overview_structure(self):
        """Test that overview returns correct data structure."""
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/api/accounts/admin/overview/')
        
        self.assertIsInstance(response.data['users'], list)
        
        if response.data['users']:
            user = response.data['users'][0]
            self.assertIn('id', user)
            self.assertIn('email', user)
            self.assertIn('username', user)
            self.assertIn('total_tasks', user)
            self.assertIn('open_tasks', user)


class AdminNotifyTests(TestCase):
    """Tests for admin notify endpoint."""

    def setUp(self):
        self.client = APIClient()
        
        # Create regular user
        self.user = User.objects.create_user(
            email='user@example.com',
            username='user',
            password='UserPass123!'
        )
        
        # Create admin user
        self.admin = User.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='AdminPass123!'
        )

    def test_notify_requires_authentication(self):
        """Test that notify endpoint requires authentication."""
        response = self.client.post('/api/accounts/admin/notify/', {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_notify_requires_admin(self):
        """Test that regular user cannot send notifications."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/accounts/admin/notify/', {
            'recipients': ['test@example.com'],
            'message': 'Test message'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch('accounts.views.send_email_task.apply_async')
    def test_notify_success(self, mock_task):
        """Test successful email notification queueing."""
        mock_task.return_value.id = 'test-task-id'
        
        self.client.force_authenticate(user=self.admin)
        response = self.client.post('/api/accounts/admin/notify/', {
            'recipients': ['user1@example.com', 'user2@example.com'],
            'subject': 'Test Subject',
            'message': 'Test message'
        })
        
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIn('job_id', response.data)
        self.assertIn('task_id', response.data)
        self.assertEqual(response.data['status'], 'queued')
        
        # Verify task was called
        mock_task.assert_called_once()

    def test_notify_requires_recipients(self):
        """Test that recipients are required."""
        self.client.force_authenticate(user=self.admin)
        response = self.client.post('/api/accounts/admin/notify/', {
            'message': 'Test message'
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_notify_requires_message(self):
        """Test that message is required."""
        self.client.force_authenticate(user=self.admin)
        response = self.client.post('/api/accounts/admin/notify/', {
            'recipients': ['test@example.com']
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_notify_with_empty_recipients(self):
        """Test that empty recipients list is rejected."""
        self.client.force_authenticate(user=self.admin)
        response = self.client.post('/api/accounts/admin/notify/', {
            'recipients': [],
            'message': 'Test message'
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CeleryTaskTests(TestCase):
    """Tests for Celery email tasks."""

    @patch('accounts.tasks.send_mail')
    def test_send_email_task_success(self, mock_send_mail):
        """Test successful email sending task."""
        from accounts.tasks import send_email_task
        
        recipients = ['user1@example.com', 'user2@example.com']
        subject = 'Test Subject'
        message = 'Test message'
        
        result = send_email_task(recipients, subject, message)
        
        self.assertEqual(result['sent_count'], 2)
        self.assertEqual(result['failed_count'], 0)
        self.assertEqual(result['total'], 2)
        self.assertEqual(mock_send_mail.call_count, 2)

    @patch('accounts.tasks.send_mail')
    def test_send_email_task_partial_failure(self, mock_send_mail):
        """Test email task with partial failures."""
        from accounts.tasks import send_email_task
        
        # First call succeeds, second fails
        mock_send_mail.side_effect = [None, Exception('Email failed')]
        
        recipients = ['success@example.com', 'fail@example.com']
        subject = 'Test Subject'
        message = 'Test message'
        
        result = send_email_task(recipients, subject, message)
        
        self.assertEqual(result['sent_count'], 1)
        self.assertEqual(result['failed_count'], 1)
        self.assertIn('fail@example.com', result['failed_emails'])
