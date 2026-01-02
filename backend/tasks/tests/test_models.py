"""Tests for Task model."""

from django.test import TransactionTestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from tasks.models import Task


User = get_user_model()


class TaskModelTests(TransactionTestCase):
    """Test suite for Task model."""
    
    serialized_rollback = True

    def setUp(self):
        """Set up test data."""
        # Explicitly clean all data to ensure isolation
        Task.objects.all().delete()
        User.objects.all().delete()
        
        self.user = User.objects.create_user(
            email='taskuser@example.com',
            username='taskuser',
            password='TaskPass123!'
        )
        
        self.task_data = {
            'user': self.user,
            'title': 'Test Task',
            'description': 'Test task description',
            'status': 'TODO',
            'priority': 'MEDIUM'
        }

    def test_create_task_with_all_fields(self):
        """Test creating task with all fields."""
        due_date = timezone.now().date() + timedelta(days=7)
        
        task = Task.objects.create(
            **self.task_data,
            due_date=due_date
        )
        
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.description, 'Test task description')
        self.assertEqual(task.status, 'TODO')
        self.assertEqual(task.priority, 'MEDIUM')
        self.assertEqual(task.user, self.user)
        self.assertEqual(task.due_date, due_date)

    def test_create_task_with_minimal_fields(self):
        """Test creating task with only required fields."""
        task = Task.objects.create(
            user=self.user,
            title='Minimal Task'
        )
        
        self.assertEqual(task.title, 'Minimal Task')
        self.assertEqual(task.status, 'TODO')  # Default
        self.assertEqual(task.priority, 'MEDIUM')  # Default
        self.assertEqual(task.description, '')  # Blank default
        self.assertIsNone(task.due_date)  # Nullable

    def test_task_status_choices(self):
        """Test all valid task status choices."""
        statuses = ['TODO', 'DOING', 'DONE']
        
        for status in statuses:
            task = Task.objects.create(
                user=self.user,
                title=f'Task {status}',
                status=status
            )
            self.assertEqual(task.status, status)

    def test_task_priority_choices(self):
        """Test all valid task priority choices."""
        priorities = ['LOW', 'MEDIUM', 'HIGH']
        
        for priority in priorities:
            task = Task.objects.create(
                user=self.user,
                title=f'Task {priority}',
                priority=priority
            )
            self.assertEqual(task.priority, priority)

    def test_task_str_representation(self):
        """Test task string representation returns title."""
        task = Task.objects.create(
            user=self.user,
            title='String Test Task'
        )
        
        self.assertEqual(str(task), 'String Test Task')

    def test_task_timestamps(self):
        """Test task has created_at and updated_at timestamps."""
        task = Task.objects.create(
            user=self.user,
            title='Timestamp Task'
        )
        
        self.assertIsNotNone(task.created_at)
        self.assertIsNotNone(task.updated_at)

    def test_task_updated_at_changes(self):
        """Test updated_at changes when task is modified."""
        task = Task.objects.create(
            user=self.user,
            title='Update Test'
        )
        
        old_updated_at = task.updated_at
        
        # Small delay to ensure time difference
        import time
        time.sleep(0.1)
        
        task.title = 'Updated Title'
        task.save()
        
        self.assertNotEqual(task.updated_at, old_updated_at)
        self.assertGreater(task.updated_at, old_updated_at)

    def test_task_ordering(self):
        """Test tasks are ordered by created_at descending."""
        task1 = Task.objects.create(
            user=self.user,
            title='First Task'
        )
        
        task2 = Task.objects.create(
            user=self.user,
            title='Second Task'
        )
        
        tasks = Task.objects.all()
        self.assertEqual(tasks[0], task2)  # Most recent first
        self.assertEqual(tasks[1], task1)

    def test_task_user_relationship(self):
        """Test task relationship with user."""
        task = Task.objects.create(
            user=self.user,
            title='User Task'
        )
        
        self.assertEqual(task.user, self.user)
        self.assertIn(task, self.user.tasks.all())

    def test_delete_user_deletes_tasks(self):
        """Test cascade delete: deleting user deletes their tasks."""
        task = Task.objects.create(
            user=self.user,
            title='Cascade Test'
        )
        
        task_id = task.id
        self.user.delete()
        
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=task_id)

    def test_task_without_user(self):
        """Test creating task without user (allowed)."""
        task = Task.objects.create(
            title='No User Task',
            user=None
        )
        
        self.assertIsNone(task.user)
        self.assertEqual(task.title, 'No User Task')

    def test_multiple_tasks_per_user(self):
        """Test user can have multiple tasks."""
        Task.objects.create(user=self.user, title='Task 1')
        Task.objects.create(user=self.user, title='Task 2')
        Task.objects.create(user=self.user, title='Task 3')
        
        self.assertEqual(self.user.tasks.count(), 3)

    def test_task_status_transition(self):
        """Test task can transition through statuses."""
        task = Task.objects.create(
            user=self.user,
            title='Status Transition',
            status='TODO'
        )
        
        task.status = 'DOING'
        task.save()
        self.assertEqual(task.status, 'DOING')
        
        task.status = 'DONE'
        task.save()
        self.assertEqual(task.status, 'DONE')

    def test_overdue_task(self):
        """Test identifying overdue tasks."""
        yesterday = timezone.now().date() - timedelta(days=1)
        
        task = Task.objects.create(
            user=self.user,
            title='Overdue Task',
            due_date=yesterday,
            status='TODO'
        )
        
        self.assertLess(task.due_date, timezone.now().date())
        self.assertNotEqual(task.status, 'DONE')
