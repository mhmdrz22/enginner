from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from tasks.models import Task, TaskHistory
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class TaskViewSetIntegrationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='integration@example.com',
            password='testpass123',
            first_name='Integration',
            last_name='User'
        )
        self.client.force_authenticate(user=self.user)
        self.list_url = reverse('tasks:task-list')

    def test_list_tasks_authenticated(self):
        Task.objects.create(user=self.user, title='Task 1')
        Task.objects.create(user=self.user, title='Task 2')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_create_task(self):
        data = {'title': 'New Integration Task', 'priority': 'HIGH'}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().priority, 'HIGH')

    def test_update_own_task(self):
        task = Task.objects.create(user=self.user, title='Original Title')
        url = reverse('tasks:task-detail', kwargs={'pk': task.pk})
        data = {'title': 'Updated Title'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, 'Updated Title')

    def test_cannot_update_others_task(self):
        other_user = User.objects.create_user(email='other@example.com', password='p')
        task = Task.objects.create(user=other_user, title='Other Task')
        url = reverse('tasks:task-detail', kwargs={'pk': task.pk})
        response = self.client.patch(url, {'title': 'Hacked'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_soft_delete_task(self):
        task = Task.objects.create(user=self.user, title='To Delete')
        url = reverse('tasks:task-detail', kwargs={'pk': task.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        task.refresh_from_db()
        self.assertTrue(task.is_deleted)

    def test_restore_task(self):
        task = Task.objects.create(user=self.user, title='Deleted', is_deleted=True)
        # Using correct restore URL from default router with custom action
        url = reverse('tasks:task-restore', kwargs={'pk': task.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertFalse(task.is_deleted)

    def test_get_task_history(self):
        task = Task.objects.create(user=self.user, title='History Task')
        task.title = 'Changed Title'
        task.save()
        
        # Manually create history if signals/models don't auto-create it (depending on setup)
        if not TaskHistory.objects.filter(task=task).exists():
            TaskHistory.objects.create(task=task, changed_by=self.user, field_name='title', old_value='History Task', new_value='Changed Title')

        url = reverse('tasks:task-history', kwargs={'pk': task.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_filter_tasks_by_status(self):
        Task.objects.create(user=self.user, title="Done Task", status="DONE")
        Task.objects.create(user=self.user, title="Todo Task", status="TODO")
        
        response = self.client.get(self.list_url, {'status': 'DONE'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], "Done Task")

    def test_search_tasks(self):
        Task.objects.create(user=self.user, title="UniqueSearchTerm")
        Task.objects.create(user=self.user, title="Another Task")
        
        response = self.client.get(self.list_url, {'search': 'UniqueSearchTerm'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_user_sees_only_own_tasks(self):
        Task.objects.create(user=self.user, title="My Task")
        other_user = User.objects.create_user(email='other2@example.com', password='p')
        Task.objects.create(user=other_user, title="Other Task")

        response = self.client.get(self.list_url)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], "My Task")

    def test_task_statistics(self):
        Task.objects.create(user=self.user, title="T1", status="TODO")
        Task.objects.create(user=self.user, title="T2", status="DONE")
        
        # Standard router naming: basename + '-' + action_name
        url = reverse('tasks:task-statistics')
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_tasks'], 2)
        self.assertEqual(response.data['completed_tasks'], 1)
