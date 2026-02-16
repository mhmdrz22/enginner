from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from tasks.models import Task

User = get_user_model()


class SoftDeleteTests(TestCase):
    """Test suite for soft delete functionality."""

    def setUp(self):
        """Set up test user and task."""
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.task = Task.objects.create(
            user=self.user,
            title='Test Task',
            description='Test Description',
            status=Task.Status.TODO
        )

    def test_soft_delete_method(self):
        """Test soft_delete() method marks task as deleted."""
        self.assertFalse(self.task.is_deleted)
        self.assertIsNone(self.task.deleted_at)
        
        self.task.soft_delete()
        
        self.assertTrue(self.task.is_deleted)
        self.assertIsNotNone(self.task.deleted_at)
        self.assertIsInstance(self.task.deleted_at, timezone.datetime)

    def test_restore_method(self):
        """Test restore() method restores deleted task."""
        self.task.soft_delete()
        self.assertTrue(self.task.is_deleted)
        
        self.task.restore()
        
        self.assertFalse(self.task.is_deleted)
        self.assertIsNone(self.task.deleted_at)

    def test_soft_deleted_tasks_still_in_db(self):
        """Test soft deleted tasks remain in database."""
        task_id = self.task.id
        self.task.soft_delete()
        
        # Task should still exist in database
        task = Task.objects.get(id=task_id)
        self.assertTrue(task.is_deleted)

    def test_filter_active_tasks(self):
        """Test filtering active (not deleted) tasks."""
        task2 = Task.objects.create(
            user=self.user,
            title='Task 2',
            status=Task.Status.TODO
        )
        
        self.task.soft_delete()
        
        active_tasks = Task.objects.filter(is_deleted=False)
        self.assertEqual(active_tasks.count(), 1)
        self.assertEqual(active_tasks.first(), task2)

    def test_filter_deleted_tasks(self):
        """Test filtering deleted tasks."""
        task2 = Task.objects.create(
            user=self.user,
            title='Task 2',
            status=Task.Status.TODO
        )
        
        self.task.soft_delete()
        
        deleted_tasks = Task.objects.filter(is_deleted=True)
        self.assertEqual(deleted_tasks.count(), 1)
        self.assertEqual(deleted_tasks.first(), self.task)

    def test_multiple_soft_delete_calls(self):
        """Test multiple soft_delete() calls don't cause issues."""
        first_delete_time = None
        
        self.task.soft_delete()
        first_delete_time = self.task.deleted_at
        
        # Call again
        self.task.soft_delete()
        
        self.assertTrue(self.task.is_deleted)
        # deleted_at should be updated
        self.assertIsNotNone(self.task.deleted_at)

    def test_restore_non_deleted_task(self):
        """Test restore() on non-deleted task."""
        self.assertFalse(self.task.is_deleted)
        
        self.task.restore()
        
        self.assertFalse(self.task.is_deleted)
        self.assertIsNone(self.task.deleted_at)
