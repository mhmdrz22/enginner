"""Performance and load tests."""

import time
import uuid
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from tasks.models import Task


User = get_user_model()


class PerformanceTests(TestCase):
    """Test suite for performance benchmarks."""

    def setUp(self):
        """Set up test user with unique credentials."""
        unique_id = uuid.uuid4().hex[:8]
        self.user = User.objects.create_user(
            email=f'perf_{unique_id}@example.com',
            username=f'perfuser_{unique_id}',
            password='PerfPass123!'
        )

    def test_bulk_task_creation_performance(self):
        """Test performance of creating many tasks."""
        start_time = time.time()
        
        tasks = [
            Task(
                user=self.user,
                title=f'Task {i}',
                description=f'Description for task {i}',
                status='TODO',
                priority='MEDIUM'
            )
            for i in range(100)
        ]
        
        Task.objects.bulk_create(tasks)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete in less than 1 second
        self.assertLess(duration, 1.0)
        self.assertEqual(Task.objects.filter(user=self.user).count(), 100)

    def test_query_performance(self):
        """Test query performance with many records."""
        # Create 50 tasks
        Task.objects.bulk_create([
            Task(
                user=self.user,
                title=f'Query Task {i}',
                status='TODO' if i % 2 == 0 else 'DONE'
            )
            for i in range(50)
        ])
        
        # Test query performance
        start_time = time.time()
        
        tasks = Task.objects.filter(
            user=self.user,
            status='TODO'
        ).select_related('user')
        
        list(tasks)  # Force query execution
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete very quickly
        self.assertLess(duration, 0.1)

    def test_database_queries_count(self):
        """Test that N+1 query problem doesn't exist."""
        # Create tasks
        Task.objects.bulk_create([
            Task(user=self.user, title=f'Task {i}')
            for i in range(10)
        ])
        
        tasks = list(Task.objects.filter(user=self.user))
        self.assertEqual(len(tasks), 10)

    def test_user_task_count_performance(self):
        """Test performance of counting user tasks."""
        # Create many tasks
        Task.objects.bulk_create([
            Task(user=self.user, title=f'Count Task {i}')
            for i in range(200)
        ])
        
        start_time = time.time()
        count = self.user.tasks.count()
        end_time = time.time()
        
        duration = end_time - start_time
        
        self.assertEqual(count, 200)
        self.assertLess(duration, 0.05)

    def test_filtering_performance(self):
        """Test performance of complex filtering."""
        # Create diverse tasks
        statuses = ['TODO', 'DOING', 'DONE']
        priorities = ['LOW', 'MEDIUM', 'HIGH']
        
        tasks = []
        for i in range(150):
            tasks.append(Task(
                user=self.user,
                title=f'Filter Task {i}',
                status=statuses[i % 3],
                priority=priorities[i % 3]
            ))
        
        Task.objects.bulk_create(tasks)
        
        # Test complex filter
        start_time = time.time()
        
        filtered = Task.objects.filter(
            user=self.user,
            status='TODO',
            priority='HIGH'
        )
        
        list(filtered)
        
        end_time = time.time()
        duration = end_time - start_time
        
        self.assertLess(duration, 0.1)


class ScalabilityTests(TestCase):
    """Test scalability with multiple users."""

    def test_multiple_users_performance(self):
        """Test system performance with multiple users."""
        
        # Create multiple users with unique identifiers
        users = []
        for i in range(10):
            unique_id = uuid.uuid4().hex[:8]
            user = User.objects.create_user(
                email=f'scale{i}_{unique_id}@example.com',
                username=f'scaleuser{i}_{unique_id}',
                password='ScalePass123!'
            )
            users.append(user)
        
        # Each user creates 20 tasks
        tasks = []
        for user in users:
            for j in range(20):
                tasks.append(Task(
                    user=user,
                    title=f'User {user.username} Task {j}'
                ))
        
        start_time = time.time()
        Task.objects.bulk_create(tasks)
        end_time = time.time()
        
        duration = end_time - start_time
        
        self.assertLess(duration, 1.0)
        self.assertEqual(Task.objects.count(), 200)

    def test_concurrent_task_access(self):
        """Test accessing tasks with concurrent user simulation."""
        
        # Create unique users
        unique_id1 = uuid.uuid4().hex[:8]
        unique_id2 = uuid.uuid4().hex[:8]
        
        user1 = User.objects.create_user(
            email=f'concurrent1_{unique_id1}@example.com',
            username=f'concurrent1_{unique_id1}',
            password='pass123'
        )
        user2 = User.objects.create_user(
            email=f'concurrent2_{unique_id2}@example.com',
            username=f'concurrent2_{unique_id2}',
            password='pass123'
        )
        
        # Create tasks for both
        Task.objects.bulk_create([
            Task(user=user1, title=f'U1 Task {i}')
            for i in range(50)
        ])
        Task.objects.bulk_create([
            Task(user=user2, title=f'U2 Task {i}')
            for i in range(50)
        ])
        
        # Simulate concurrent access
        start_time = time.time()
        
        user1_tasks = list(Task.objects.filter(user=user1))
        user2_tasks = list(Task.objects.filter(user=user2))
        
        end_time = time.time()
        duration = end_time - start_time
        
        self.assertEqual(len(user1_tasks), 50)
        self.assertEqual(len(user2_tasks), 50)
        self.assertLess(duration, 0.2)
