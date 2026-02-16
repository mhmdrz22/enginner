from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from tasks.models import Task, TaskHistory

User = get_user_model()


class TaskViewSetIntegrationTests(TestCase):
    """Integration tests for Task ViewSet."""

    def setUp(self):
        """Set up test client and users."""
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            email='user1@example.com',
            password='pass123'
        )
        self.user2 = User.objects.create_user(
            email='user2@example.com',
            password='pass123'
        )
        self.admin = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123'
        )

    def test_list_tasks_authenticated(self):
        """Test listing tasks requires authentication."""
        url = reverse('task-list')
        
        # Without auth
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # With auth
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_sees_only_own_tasks(self):
        """Test user can only see their own tasks."""
        Task.objects.create(user=self.user1, title='User1 Task')
        Task.objects.create(user=self.user2, title='User2 Task')
        
        self.client.force_authenticate(user=self.user1)
        url = reverse('task-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should only see pagination wrapper
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'User1 Task')

    def test_create_task(self):
        """Test creating a task."""
        self.client.force_authenticate(user=self.user1)
        url = reverse('task-list')
        data = {
            'title': 'New Task',
            'description': 'Task description',
            'status': 'TODO',
            'priority': 'HIGH'
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.first()
        self.assertEqual(task.title, 'New Task')
        self.assertEqual(task.user, self.user1)

    def test_update_own_task(self):
        """Test updating own task."""
        task = Task.objects.create(
            user=self.user1,
            title='Original Title'
        )
        
        self.client.force_authenticate(user=self.user1)
        url = reverse('task-detail', kwargs={'pk': task.pk})
        data = {'title': 'Updated Title'}
        
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, 'Updated Title')

    def test_cannot_update_others_task(self):
        """Test user cannot update another user's task."""
        task = Task.objects.create(
            user=self.user2,
            title='User2 Task'
        )
        
        self.client.force_authenticate(user=self.user1)
        url = reverse('task-detail', kwargs={'pk': task.pk})
        data = {'title': 'Hacked'}
        
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_soft_delete_task(self):
        """Test soft deleting a task."""
        task = Task.objects.create(
            user=self.user1,
            title='Task to Delete'
        )
        
        self.client.force_authenticate(user=self.user1)
        url = reverse('task-detail', kwargs={'pk': task.pk})
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        task.refresh_from_db()
        self.assertTrue(task.is_deleted)

    def test_restore_task(self):
        """Test restoring a soft-deleted task."""
        task = Task.objects.create(
            user=self.user1,
            title='Deleted Task'
        )
        task.soft_delete()
        
        self.client.force_authenticate(user=self.user1)
        url = reverse('task-restore', kwargs={'pk': task.pk})
        
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertFalse(task.is_deleted)

    def test_get_task_history(self):
        """Test getting task history."""
        task = Task.objects.create(
            user=self.user1,
            title='Task with History'
        )
        TaskHistory.objects.create(
            task=task,
            field_name='status',
            old_value='TODO',
            new_value='DOING'
        )
        
        self.client.force_authenticate(user=self.user1)
        url = reverse('task-history', kwargs={'pk': task.pk})
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['field_name'], 'status')

    def test_filter_tasks_by_status(self):
        """Test filtering tasks by status."""
        Task.objects.create(user=self.user1, title='TODO Task', status='TODO')
        Task.objects.create(user=self.user1, title='DONE Task', status='DONE')
        
        self.client.force_authenticate(user=self.user1)
        url = reverse('task-list') + '?status=TODO'
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'TODO Task')

    def test_search_tasks(self):
        """Test searching tasks by title."""
        Task.objects.create(user=self.user1, title='Important Meeting')
        Task.objects.create(user=self.user1, title='Buy groceries')
        
        self.client.force_authenticate(user=self.user1)
        url = reverse('task-list') + '?search=Meeting'
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Important Meeting')

    def test_bulk_update_tasks(self):
        """Test bulk updating tasks."""
        task1 = Task.objects.create(user=self.user1, title='Task 1', status='TODO')
        task2 = Task.objects.create(user=self.user1, title='Task 2', status='TODO')
        
        self.client.force_authenticate(user=self.user1)
        url = reverse('task-bulk-update')
        data = {
            'ids': [task1.id, task2.id],
            'status': 'DONE'
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task1.refresh_from_db()
        task2.refresh_from_db()
        self.assertEqual(task1.status, 'DONE')
        self.assertEqual(task2.status, 'DONE')

    def test_bulk_delete_tasks(self):
        """Test bulk deleting tasks."""
        task1 = Task.objects.create(user=self.user1, title='Task 1')
        task2 = Task.objects.create(user=self.user1, title='Task 2')
        
        self.client.force_authenticate(user=self.user1)
        url = reverse('task-bulk-delete')
        data = {'ids': [task1.id, task2.id]}
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        task1.refresh_from_db()
        task2.refresh_from_db()
        self.assertTrue(task1.is_deleted)
        self.assertTrue(task2.is_deleted)
