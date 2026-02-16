from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from tasks.models import Task
from django.urls import reverse

User = get_user_model()

class UserTaskFlowIntegrationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='flow@example.com',
            password='testpass123',
            first_name='Flow',
            last_name='User'
        )
        self.client.force_authenticate(user=self.user)

    def test_complete_user_journey(self):
        # 1. Create Task
        create_url = reverse('tasks:task-list')
        data = {'title': 'Journey Task', 'priority': 'HIGH'}
        response = self.client.post(create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        task_id = response.data['id']

        # 2. Get Task
        detail_url = reverse('tasks:task-detail', kwargs={'pk': task_id})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Journey Task')

    def test_user_isolation(self):
        # User 1 creates task
        Task.objects.create(user=self.user, title="User 1 Task")

        # User 2
        user2 = User.objects.create_user(email='user2@example.com', password='p')
        client2 = APIClient()
        client2.force_authenticate(user=user2)

        # User 2 lists tasks
        url = reverse('tasks:task-list')
        response = client2.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)


class TaskWorkflowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='workflow@example.com',
            password='pass'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_task_lifecycle(self):
        task = Task.objects.create(user=self.user, title="Lifecycle Task")
        self.assertEqual(task.status, 'TODO')
        
        task.status = 'DONE'
        task.save()
        self.assertEqual(task.status, 'DONE')

    def test_bulk_task_creation(self):
        tasks = [Task(user=self.user, title=f"Task {i}") for i in range(5)]
        Task.objects.bulk_create(tasks)
        self.assertEqual(Task.objects.count(), 5)

    def test_priority_based_workflow(self):
        Task.objects.create(user=self.user, title="High", priority="HIGH")
        Task.objects.create(user=self.user, title="Low", priority="LOW")
        
        url = reverse('tasks:task-list')
        response = self.client.get(url, {'ordering': 'priority'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
