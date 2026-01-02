"""Integration tests for complete user flows."""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from tasks.models import Task


User = get_user_model()


class UserTaskFlowIntegrationTests(TestCase):
    """Test complete user journey from registration to task management."""

    def setUp(self):
        """Set up API client."""
        self.client = APIClient()

    def test_complete_user_journey(self):
        """Test full flow: register -> login -> create tasks -> manage tasks."""
        
        # Step 1: Register new user
        register_url = reverse('accounts:register')
        register_data = {
            'email': 'journey@example.com',
            'username': 'journeyuser',
            'password': 'JourneyPass123!',
            'password2': 'JourneyPass123!'
        }
        
        register_response = self.client.post(
            register_url,
            register_data,
            format='json'
        )
        
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        self.assertIn('email', register_response.data)
        
        # Step 2: Login
        login_url = reverse('accounts:login')
        login_data = {
            'email': 'journey@example.com',
            'password': 'JourneyPass123!'
        }
        
        login_response = self.client.post(
            login_url,
            login_data,
            format='json'
        )
        
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn('token', login_response.data)
        
        token = login_response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        
        # Step 3: Create multiple tasks
        tasks_url = reverse('tasks:task-list')
        
        task1_data = {
            'title': 'First Task',
            'description': 'My first task',
            'status': 'TODO',
            'priority': 'HIGH'
        }
        
        task1_response = self.client.post(
            tasks_url,
            task1_data,
            format='json'
        )
        
        self.assertEqual(task1_response.status_code, status.HTTP_201_CREATED)
        task1_id = task1_response.data['id']
        
        task2_data = {
            'title': 'Second Task',
            'status': 'TODO',
            'priority': 'MEDIUM'
        }
        
        task2_response = self.client.post(
            tasks_url,
            task2_data,
            format='json'
        )
        
        self.assertEqual(task2_response.status_code, status.HTTP_201_CREATED)
        
        # Step 4: List all tasks
        list_response = self.client.get(tasks_url)
        
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 2)
        
        # Step 5: Update task status
        task_detail_url = reverse('tasks:task-detail', kwargs={'pk': task1_id})
        update_data = {'status': 'DOING'}
        
        update_response = self.client.patch(
            task_detail_url,
            update_data,
            format='json'
        )
        
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['status'], 'DOING')
        
        # Step 6: Complete task
        complete_data = {'status': 'DONE'}
        
        complete_response = self.client.patch(
            task_detail_url,
            complete_data,
            format='json'
        )
        
        self.assertEqual(complete_response.status_code, status.HTTP_200_OK)
        self.assertEqual(complete_response.data['status'], 'DONE')
        
        # Step 7: Get user profile
        profile_url = reverse('accounts:profile')
        profile_response = self.client.get(profile_url)
        
        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)
        self.assertEqual(profile_response.data['email'], 'journey@example.com')

    def test_user_isolation(self):
        """Test that users can only see and manage their own tasks."""
        
        # Create two users
        user1_data = {
            'email': 'user1@example.com',
            'username': 'user1',
            'password': 'User1Pass123!',
            'password2': 'User1Pass123!'
        }
        
        user2_data = {
            'email': 'user2@example.com',
            'username': 'user2',
            'password': 'User2Pass123!',
            'password2': 'User2Pass123!'
        }
        
        register_url = reverse('accounts:register')
        
        # Register users
        self.client.post(register_url, user1_data, format='json')
        self.client.post(register_url, user2_data, format='json')
        
        # Login as user1
        login_url = reverse('accounts:login')
        login1_response = self.client.post(
            login_url,
            {'email': 'user1@example.com', 'password': 'User1Pass123!'},
            format='json'
        )
        
        token1 = login1_response.data['token']
        
        # User1 creates task
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token1}')
        tasks_url = reverse('tasks:task-list')
        
        task_response = self.client.post(
            tasks_url,
            {'title': 'User1 Task'},
            format='json'
        )
        
        task_id = task_response.data['id']
        
        # Login as user2
        login2_response = self.client.post(
            login_url,
            {'email': 'user2@example.com', 'password': 'User2Pass123!'},
            format='json'
        )
        
        token2 = login2_response.data['token']
        
        # User2 tries to access user1's task
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token2}')
        task_detail_url = reverse('tasks:task-detail', kwargs={'pk': task_id})
        
        response = self.client.get(task_detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # User2 lists tasks (should be empty)
        list_response = self.client.get(tasks_url)
        
        self.assertEqual(len(list_response.data), 0)


class TaskWorkflowTests(TestCase):
    """Test task workflow scenarios."""

    def setUp(self):
        """Set up authenticated user."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='workflow@example.com',
            username='workflow',
            password='WorkflowPass123!'
        )
        self.client.force_authenticate(user=self.user)
        self.tasks_url = reverse('tasks:task-list')

    def test_task_lifecycle(self):
        """Test complete task lifecycle: TODO -> DOING -> DONE."""
        
        # Create task
        task_data = {
            'title': 'Lifecycle Task',
            'status': 'TODO',
            'priority': 'HIGH'
        }
        
        create_response = self.client.post(
            self.tasks_url,
            task_data,
            format='json'
        )
        
        task_id = create_response.data['id']
        task_url = reverse('tasks:task-detail', kwargs={'pk': task_id})
        
        # Verify initial status
        self.assertEqual(create_response.data['status'], 'TODO')
        
        # Start working (TODO -> DOING)
        self.client.patch(
            task_url,
            {'status': 'DOING'},
            format='json'
        )
        
        task = Task.objects.get(id=task_id)
        self.assertEqual(task.status, 'DOING')
        
        # Complete task (DOING -> DONE)
        self.client.patch(
            task_url,
            {'status': 'DONE'},
            format='json'
        )
        
        task.refresh_from_db()
        self.assertEqual(task.status, 'DONE')

    def test_bulk_task_creation(self):
        """Test creating multiple tasks at once."""
        
        task_titles = [
            'Task 1',
            'Task 2',
            'Task 3',
            'Task 4',
            'Task 5'
        ]
        
        for title in task_titles:
            response = self.client.post(
                self.tasks_url,
                {'title': title},
                format='json'
            )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify all created
        list_response = self.client.get(self.tasks_url)
        self.assertEqual(len(list_response.data), 5)

    def test_priority_based_workflow(self):
        """Test tasks with different priorities."""
        
        # Create tasks with different priorities
        Task.objects.create(
            user=self.user,
            title='Low Priority',
            priority='LOW'
        )
        Task.objects.create(
            user=self.user,
            title='High Priority',
            priority='HIGH'
        )
        Task.objects.create(
            user=self.user,
            title='Medium Priority',
            priority='MEDIUM'
        )
        
        # Filter high priority tasks
        response = self.client.get(f'{self.tasks_url}?priority=HIGH')
        
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'High Priority')
