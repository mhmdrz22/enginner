from django.test import TestCase
from django.contrib.auth import get_user_model
from tasks.models import Task, TaskHistory

User = get_user_model()


class TaskHistoryTests(TestCase):
    """Test suite for TaskHistory model."""

    def setUp(self):
        """Set up test user and task."""
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.task = Task.objects.create(
            user=self.user,
            title='Test Task',
            status=Task.Status.TODO
        )

    def test_create_history_entry(self):
        """Test creating a history entry."""
        history = TaskHistory.objects.create(
            task=self.task,
            changed_by=self.user,
            field_name='status',
            old_value='TODO',
            new_value='DOING'
        )
        
        self.assertEqual(history.task, self.task)
        self.assertEqual(history.changed_by, self.user)
        self.assertEqual(history.field_name, 'status')
        self.assertEqual(history.old_value, 'TODO')
        self.assertEqual(history.new_value, 'DOING')
        self.assertIsNotNone(history.changed_at)

    def test_history_str_method(self):
        """Test string representation of history."""
        history = TaskHistory.objects.create(
            task=self.task,
            changed_by=self.user,
            field_name='title',
            old_value='Old Title',
            new_value='New Title'
        )
        
        self.assertIn(self.task.title, str(history))
        self.assertIn('title', str(history))

    def test_history_ordering(self):
        """Test history entries are ordered by changed_at descending."""
        history1 = TaskHistory.objects.create(
            task=self.task,
            field_name='title',
            old_value='V1',
            new_value='V2'
        )
        history2 = TaskHistory.objects.create(
            task=self.task,
            field_name='title',
            old_value='V2',
            new_value='V3'
        )
        
        histories = TaskHistory.objects.all()
        # Most recent first
        self.assertEqual(histories[0], history2)
        self.assertEqual(histories[1], history1)

    def test_history_related_name(self):
        """Test accessing history through task.history."""
        TaskHistory.objects.create(
            task=self.task,
            field_name='status',
            old_value='TODO',
            new_value='DOING'
        )
        
        self.assertEqual(self.task.history.count(), 1)
        self.assertEqual(self.task.history.first().field_name, 'status')

    def test_cascade_delete_task(self):
        """Test that deleting task deletes its history."""
        TaskHistory.objects.create(
            task=self.task,
            field_name='title',
            old_value='Old',
            new_value='New'
        )
        
        task_id = self.task.id
        self.task.delete()  # Hard delete
        
        # History should be deleted too
        self.assertEqual(TaskHistory.objects.filter(task_id=task_id).count(), 0)

    def test_set_null_on_user_delete(self):
        """Test that deleting user cascades to task and its history.
        
        Since Task has CASCADE on user deletion, when user is deleted,
        the task is also deleted, which cascades to delete the history.
        """
        TaskHistory.objects.create(
            task=self.task,
            changed_by=self.user,
            field_name='title',
            old_value='Old',
            new_value='New'
        )
        
        task_id = self.task.id
        self.user.delete()
        
        # Task should be deleted (CASCADE)
        self.assertEqual(Task.objects.filter(id=task_id).count(), 0)
        
        # History should also be deleted (CASCADE from task)
        self.assertEqual(TaskHistory.objects.filter(task_id=task_id).count(), 0)

    def test_multiple_history_entries(self):
        """Test multiple history entries for same task."""
        TaskHistory.objects.create(
            task=self.task,
            field_name='status',
            old_value='TODO',
            new_value='DOING'
        )
        TaskHistory.objects.create(
            task=self.task,
            field_name='priority',
            old_value='MEDIUM',
            new_value='HIGH'
        )
        TaskHistory.objects.create(
            task=self.task,
            field_name='status',
            old_value='DOING',
            new_value='DONE'
        )
        
        self.assertEqual(self.task.history.count(), 3)
