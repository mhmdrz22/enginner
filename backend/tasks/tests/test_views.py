"""Tests for task views and API endpoints."""

import uuid
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from tasks.models import Task


User = get_user_model()


class TaskAPITests(APITestCase):
    """Test suite for Task API endpoints."""

    def setUp(self):
        """Set up test client and data with unique users."""
        # DEBUG: Check initial state
        initial_count = Task.objects.count()
        print(f"\n[DEBUG setUp] Before Delete: Found {initial_count} tasks in DB.")
        
        if initial_count > 0:
            # Print details of existing tasks
            tasks_info = []
            for task in Task.objects.all():
                user_email = task.user.email if task.user else 'NO_USER'
                tasks_info.append(f"'{task.title}' (user: {user_email})")
            print(f"[DEBUG setUp] Existing tasks: {tasks_info}")
        
        # CRITICAL: Clean up any leftover data from previous tests
        deleted_count, _ = Task.objects.all().delete()
        print(f"[DEBUG setUp] Deleted {deleted_count} tasks.")
        
        # Verify deletion
        after_count = Task.objects.count()
        print(f"[DEBUG setUp] After Delete: Found {after_count} tasks in DB.")
        
        if after_count > 0:
            # ZOMBIE TASKS DETECTED!
            titles = list(Task.objects.values_list('title', flat=True))
            print(f"[DEBUG setUp] ⚠️ ZOMBIE TASKS DETECTED: {titles}")
        
        # Generate unique IDs for this test instance
        uid1 = uuid.uuid4().hex[:8]
        uid2 = uuid.uuid4().hex[:8]
        
        # Create users with unique credentials
        self.user1 = User.objects.create_user(
            email=f'user1_{uid1}@example.com',
            username=f'user1_{uid1}',
            password='User1Pass123!'
        )
        self.user2 = User.objects.create_user(
            email=f'user2_{uid2}@example.com',
            username=f'user2_{uid2}',
            password='User2Pass123!'
        )
        
        # Create tokens
        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)
        
        # URLs
        self.list_url = reverse('tasks:task-list')
        
        # Sample task data
        self.task_data = {
            'title': 'New Task',
            'description': 'Task description',
            'status': 'TODO',
            'priority': 'HIGH',
            'due_date': (timezone.now().date() + timedelta(days=7)).isoformat()
        }

    def test_list_tasks_authenticated(self):
        """Test authenticated user can list their tasks."""
        print(f"\n[DEBUG test_list_tasks_authenticated] Starting test...")
        
        # Create tasks for user1
        Task.objects.create(user=self.user1, title='Task 1')
        Task.objects.create(user=self.user1, title='Task 2')
        
        # Create task for user2 (should not appear)
        Task.objects.create(user=self.user2, title='Task 3')
        
        # Debug: Check what's in DB before API call
        total_tasks = Task.objects.count()
        user1_tasks_count = Task.objects.filter(user=self.user1).count()
        print(f"[DEBUG test_list_tasks_authenticated] Total tasks in DB: {total_tasks}")
        print(f"[DEBUG test_list_tasks_authenticated] User1 tasks in DB: {user1_tasks_count}")
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        response = self.client.get(self.list_url)
        
        print(f"[DEBUG test_list_tasks_authenticated] API returned {len(response.data)} tasks")
        if len(response.data) != 2:
            print(f"[DEBUG test_list_tasks_authenticated] ❌ EXPECTED 2, GOT {len(response.data)}")
            for task in response.data:
                print(f"  - Task: {task.get('title', 'N/A')}")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_tasks_unauthenticated(self):
        """Test unauthenticated user cannot list tasks."""
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_task_authenticated(self):
        """Test authenticated user can create task."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        response = self.client.post(
            self.list_url,
            self.task_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Task')
        self.assertEqual(response.data['status'], 'TODO')
        
        # Verify in database
        task = Task.objects.get(id=response.data['id'])
        self.assertEqual(task.user, self.user1)

    def test_create_task_without_title(self):
        """Test creating task without title fails."""
        data = self.task_data.copy()
        del data['title']
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        response = self.client.post(self.list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_task(self):
        """Test retrieving specific task."""
        task = Task.objects.create(
            user=self.user1,
            title='Retrieve Task'
        )
        
        url = reverse('tasks:task-detail', kwargs={'pk': task.id})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Retrieve Task')

    def test_update_task(self):
        """Test updating task."""
        task = Task.objects.create(
            user=self.user1,
            title='Original Title',
            status='TODO'
        )
        
        url = reverse('tasks:task-detail', kwargs={'pk': task.id})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        
        update_data = {
            'title': 'Updated Title',
            'status': 'DOING'
        }
        
        response = self.client.patch(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        task.refresh_from_db()
        self.assertEqual(task.title, 'Updated Title')
        self.assertEqual(task.status, 'DOING')

    def test_delete_task(self):
        """Test deleting task."""
        task = Task.objects.create(
            user=self.user1,
            title='Delete Task'
        )
        
        url = reverse('tasks:task-detail', kwargs={'pk': task.id})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify deleted
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=task.id)

    def test_user_cannot_access_other_user_task(self):
        """Test user cannot access another user's task."""
        task = Task.objects.create(
            user=self.user2,
            title='User2 Task'
        )
        
        url = reverse('tasks:task-detail', kwargs={'pk': task.id})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cannot_update_other_user_task(self):
        """Test user cannot update another user's task."""
        task = Task.objects.create(
            user=self.user2,
            title='User2 Task'
        )
        
        url = reverse('tasks:task-detail', kwargs={'pk': task.id})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        
        response = self.client.patch(
            url,
            {'title': 'Hacked'},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cannot_delete_other_user_task(self):
        """Test user cannot delete another user's task."""
        task = Task.objects.create(
            user=self.user2,
            title='User2 Task'
        )
        
        url = reverse('tasks:task-detail', kwargs={'pk': task.id})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # Verify not deleted
        Task.objects.get(id=task.id)

    def test_filter_tasks_by_status(self):
        """Test filtering tasks by status."""
        print(f"\n[DEBUG test_filter_tasks_by_status] Starting test...")
        
        Task.objects.create(user=self.user1, title='Todo', status='TODO')
        Task.objects.create(user=self.user1, title='Doing', status='DOING')
        Task.objects.create(user=self.user1, title='Done', status='DONE')
        
        # Debug: Check what's in DB
        total_tasks = Task.objects.count()
        todo_tasks = Task.objects.filter(user=self.user1, status='TODO').count()
        print(f"[DEBUG test_filter_tasks_by_status] Total tasks in DB: {total_tasks}")
        print(f"[DEBUG test_filter_tasks_by_status] TODO tasks for user1 in DB: {todo_tasks}")
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        response = self.client.get(f'{self.list_url}?status=TODO')
        
        print(f"[DEBUG test_filter_tasks_by_status] API returned {len(response.data)} tasks")
        if len(response.data) != 1:
            print(f"[DEBUG test_filter_tasks_by_status] ❌ EXPECTED 1, GOT {len(response.data)}")
            for task in response.data:
                print(f"  - Task: {task.get('title', 'N/A')} (status: {task.get('status', 'N/A')})")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], 'TODO')

    def test_filter_tasks_by_priority(self):
        """Test filtering tasks by priority."""
        print(f"\n[DEBUG test_filter_tasks_by_priority] Starting test...")
        
        Task.objects.create(user=self.user1, title='Low', priority='LOW')
        Task.objects.create(user=self.user1, title='High', priority='HIGH')
        
        # Debug: Check what's in DB
        total_tasks = Task.objects.count()
        high_tasks = Task.objects.filter(user=self.user1, priority='HIGH').count()
        print(f"[DEBUG test_filter_tasks_by_priority] Total tasks in DB: {total_tasks}")
        print(f"[DEBUG test_filter_tasks_by_priority] HIGH priority tasks for user1 in DB: {high_tasks}")
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        response = self.client.get(f'{self.list_url}?priority=HIGH')
        
        print(f"[DEBUG test_filter_tasks_by_priority] API returned {len(response.data)} tasks")
        if len(response.data) != 1:
            print(f"[DEBUG test_filter_tasks_by_priority] ❌ EXPECTED 1, GOT {len(response.data)}")
            for task in response.data:
                print(f"  - Task: {task.get('title', 'N/A')} (priority: {task.get('priority', 'N/A')})")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['priority'], 'HIGH')

    def test_mark_task_as_done(self):
        """Test marking task as done."""
        task = Task.objects.create(
            user=self.user1,
            title='Complete Me',
            status='TODO'
        )
        
        url = reverse('tasks:task-detail', kwargs={'pk': task.id})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        
        response = self.client.patch(
            url,
            {'status': 'DONE'},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.status, 'DONE')
