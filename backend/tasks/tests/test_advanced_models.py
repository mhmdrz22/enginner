from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date, timedelta
from tasks.models import Task

User = get_user_model()


class TaskModelAdvancedTests(TestCase):
    """Advanced tests for Task model features."""

    def setUp(self):
        """Set up test user."""
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )

    def test_is_overdue_property(self):
        """Test is_overdue property."""
        yesterday = date.today() - timedelta(days=1)
        task = Task.objects.create(
            user=self.user,
            title='Overdue Task',
            status=Task.Status.TODO,
            due_date=yesterday
        )
        
        self.assertTrue(task.is_overdue)

    def test_is_not_overdue_future_date(self):
        """Test task with future due date is not overdue."""
        tomorrow = date.today() + timedelta(days=1)
        task = Task.objects.create(
            user=self.user,
            title='Future Task',
            status=Task.Status.TODO,
            due_date=tomorrow
        )
        
        self.assertFalse(task.is_overdue)

    def test_is_not_overdue_when_done(self):
        """Test completed task is not overdue even with past date."""
        yesterday = date.today() - timedelta(days=1)
        task = Task.objects.create(
            user=self.user,
            title='Completed Task',
            status=Task.Status.DONE,
            due_date=yesterday
        )
        
        self.assertFalse(task.is_overdue)

    def test_is_not_overdue_when_deleted(self):
        """Test deleted task is not overdue."""
        yesterday = date.today() - timedelta(days=1)
        task = Task.objects.create(
            user=self.user,
            title='Deleted Task',
            status=Task.Status.TODO,
            due_date=yesterday
        )
        task.soft_delete()
        
        self.assertFalse(task.is_overdue)

    def test_mark_completed_method(self):
        """Test mark_completed() method."""
        task = Task.objects.create(
            user=self.user,
            title='Task to Complete',
            status=Task.Status.TODO
        )
        
        self.assertIsNone(task.completed_at)
        
        task.mark_completed()
        
        self.assertEqual(task.status, Task.Status.DONE)
        self.assertIsNotNone(task.completed_at)
        self.assertIsInstance(task.completed_at, timezone.datetime)

    def test_get_tags_list(self):
        """Test get_tags_list() method."""
        task = Task.objects.create(
            user=self.user,
            title='Tagged Task',
            tags='urgent,work,important'
        )
        
        tags = task.get_tags_list()
        
        self.assertEqual(tags, ['urgent', 'work', 'important'])

    def test_get_tags_list_with_spaces(self):
        """Test get_tags_list() handles spaces."""
        task = Task.objects.create(
            user=self.user,
            title='Tagged Task',
            tags='urgent, work , important'
        )
        
        tags = task.get_tags_list()
        
        self.assertEqual(tags, ['urgent', 'work', 'important'])

    def test_get_tags_list_empty(self):
        """Test get_tags_list() with empty tags."""
        task = Task.objects.create(
            user=self.user,
            title='No Tags',
            tags=''
        )
        
        tags = task.get_tags_list()
        
        self.assertEqual(tags, [])

    def test_set_tags_list(self):
        """Test set_tags_list() method."""
        task = Task.objects.create(
            user=self.user,
            title='Task'
        )
        
        task.set_tags_list(['python', 'django', 'testing'])
        
        self.assertEqual(task.tags, 'python,django,testing')

    def test_status_display_property(self):
        """Test status_display property."""
        task = Task.objects.create(
            user=self.user,
            title='Task',
            status=Task.Status.TODO
        )
        
        self.assertEqual(task.status_display, 'To Do')

    def test_priority_display_property(self):
        """Test priority_display property."""
        task = Task.objects.create(
            user=self.user,
            title='Task',
            priority=Task.Priority.HIGH
        )
        
        self.assertEqual(task.priority_display, 'High')

    def test_task_repr(self):
        """Test __repr__ method."""
        task = Task.objects.create(
            user=self.user,
            title='Test Task',
            status=Task.Status.DOING
        )
        
        repr_str = repr(task)
        
        self.assertIn('Task', repr_str)
        self.assertIn(str(task.id), repr_str)
        self.assertIn('Test Task', repr_str)
        self.assertIn('DOING', repr_str)

    def test_due_date_constraint(self):
        """Test due_date cannot be before creation date."""
        # This is enforced at database level
        # Just verify the constraint exists in Meta
        self.assertEqual(len(Task._meta.constraints), 1)
        self.assertEqual(
            Task._meta.constraints[0].name,
            'due_date_after_creation'
        )
