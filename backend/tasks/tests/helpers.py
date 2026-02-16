import datetime
from django.utils import timezone
from tasks.models import Task
from accounts.models import User

def create_test_user(email='test@example.com', password='password123'):
    """Create a user for testing."""
    return User.objects.create_user(
        email=email,
        password=password,
        first_name='Test',
        last_name='User'
    )

def create_task(user, title='Test Task', **kwargs):
    """Create a task for testing."""
    defaults = {
        'description': 'Test Description',
        'priority': 'MEDIUM',
        'status': 'TODO'
    }
    defaults.update(kwargs)
    return Task.objects.create(user=user, title=title, **defaults)

def create_task_with_past_due_date(user):
    """Create a task with a past due date."""
    past_date = timezone.now().date() - datetime.timedelta(days=1)
    
    # First create the task with a valid due_date (e.g. tomorrow) or no due date
    # to pass the initial creation constraint check if it applies on insert
    task = Task.objects.create(
        user=user,
        title='Past Due Task',
        description='This task is past due',
        due_date=timezone.now().date() + datetime.timedelta(days=1)
    )
    
    # We need to forcefully update created_at to be in the past
    # so that when we update due_date to yesterday, it doesn't violate
    # the check constraint "due_date_after_creation"
    
    older_creation_date = timezone.now() - datetime.timedelta(days=2)
    Task.objects.filter(pk=task.pk).update(created_at=older_creation_date)

    # Now update the due_date to the past
    task.due_date = past_date
    task.save(update_fields=['due_date'])

    # Refresh to get the updated values
    task.refresh_from_db()
    
    return task
