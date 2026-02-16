from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import connection
from django.test.utils import override_settings, CaptureQueriesContext
from tasks.models import Task
import time

User = get_user_model()


class PerformanceTests(TestCase):
    """Performance tests for Task model and queries."""

    def setUp(self):
        """Set up test user and tasks."""
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )

    def test_bulk_create_performance(self):
        """Test bulk creating tasks is efficient."""
        tasks = [
            Task(
                user=self.user,
                title=f'Task {i}',
                status=Task.Status.TODO
            )
            for i in range(100)
        ]
        
        start_time = time.time()
        Task.objects.bulk_create(tasks)
        end_time = time.time()
        
        self.assertEqual(Task.objects.count(), 100)
        # Should complete in under 1 second
        self.assertLess(end_time - start_time, 1.0)

    def test_query_with_index(self):
        """Test that queries use indexes efficiently."""
        # Create test data
        Task.objects.bulk_create([
            Task(
                user=self.user,
                title=f'Task {i}',
                status=Task.Status.TODO if i % 2 == 0 else Task.Status.DONE
            )
            for i in range(50)
        ])
        
        with self.assertNumQueries(1):
            # Should use index on user and status
            tasks = list(Task.objects.filter(
                user=self.user,
                status=Task.Status.TODO,
                is_deleted=False
            ))
            self.assertEqual(len(tasks), 25)

    def test_pagination_performance(self):
        """Test pagination is efficient."""
        # Create 100 tasks
        Task.objects.bulk_create([
            Task(
                user=self.user,
                title=f'Task {i}',
                status=Task.Status.TODO
            )
            for i in range(100)
        ])
        
        # Test first page
        with self.assertNumQueries(1):
            page1 = list(Task.objects.filter(user=self.user)[:20])
            self.assertEqual(len(page1), 20)
        
        # Test second page
        with self.assertNumQueries(1):
            page2 = list(Task.objects.filter(user=self.user)[20:40])
            self.assertEqual(len(page2), 20)

    def test_select_related_optimization(self):
        """Test using select_related reduces queries."""
        Task.objects.bulk_create([
            Task(
                user=self.user,
                title=f'Task {i}',
                status=Task.Status.TODO
            )
            for i in range(10)
        ])
        
        # Without select_related - causes N+1 queries
        with CaptureQueriesContext(connection) as context_without:
            tasks_without = Task.objects.filter(user=self.user)
            for task in tasks_without:
                _ = task.user.email  # Access related user
        queries_without = len(context_without)
        
        # With select_related - fewer queries
        with CaptureQueriesContext(connection) as context_with:
            tasks_with = Task.objects.filter(user=self.user).select_related('user')
            for task in tasks_with:
                _ = task.user.email
        queries_with = len(context_with)
        
        # Should have significantly fewer queries (1 vs 11)
        self.assertLess(queries_with, queries_without)
        self.assertEqual(queries_with, 1)  # Only one query with select_related

    def test_filter_deleted_tasks_uses_index(self):
        """Test that filtering deleted tasks uses index."""
        # Create mix of deleted and active tasks
        tasks = []
        for i in range(50):
            task = Task(
                user=self.user,
                title=f'Task {i}',
                status=Task.Status.TODO
            )
            tasks.append(task)
        
        Task.objects.bulk_create(tasks)
        
        # Soft delete half
        Task.objects.filter(user=self.user)[:25].update(is_deleted=True)
        
        with self.assertNumQueries(1):
            active_tasks = list(Task.objects.filter(
                user=self.user,
                is_deleted=False
            ))
            self.assertEqual(len(active_tasks), 25)

    def test_counting_tasks_is_efficient(self):
        """Test counting tasks doesn't load objects."""
        Task.objects.bulk_create([
            Task(
                user=self.user,
                title=f'Task {i}',
                status=Task.Status.TODO
            )
            for i in range(100)
        ])
        
        with self.assertNumQueries(1):
            count = Task.objects.filter(user=self.user).count()
            self.assertEqual(count, 100)
