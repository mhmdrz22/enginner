from django.test import TestCase
from django.contrib.auth import get_user_model
from tasks.models import Task
import time

User = get_user_model()

class PerformanceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='perf@example.com', password='p')

    def test_bulk_task_creation_performance(self):
        start_time = time.time()
        tasks = [Task(user=self.user, title=f"Task {i}") for i in range(100)]
        Task.objects.bulk_create(tasks)
        duration = time.time() - start_time
        
        self.assertLess(duration, 1.0)
        self.assertEqual(Task.objects.count(), 100)

    def test_database_queries_count(self):
        Task.objects.create(user=self.user, title="Test")
        with self.assertNumQueries(1):
            list(Task.objects.filter(user=self.user))
