from django.utils import timezone
from datetime import timedelta
from tasks.models import Task

def create_task_with_past_due_date(user, title, days_overdue=1, **kwargs):
    """Helper to create a task with a due_date in the past."""
    
    # Calculate past due date
    due_date = kwargs.get('due_date') or (timezone.now() - timedelta(days=days_overdue))

    # Important trick: Set created_date to one day before due_date to pass DB constraints
    created_date = due_date - timedelta(days=1)

    # Remove conflicting args
    task_kwargs = {k: v for k, v in kwargs.items() if k != 'due_date' and k != 'created_date'}

    # Create task
    task = Task.objects.create(
        user=user,
        title=title,
        **task_kwargs
    )
    
    # Manually update dates (create usually ignores auto_now_add override)
    # Using update directly on DB bypasses Python-side restrictions
    # and updates auto_now fields too.
    Task.objects.filter(pk=task.pk).update(
        due_date=due_date,
        created_date=created_date
    )
    
    task.refresh_from_db()
    return task

def create_future_task(user, title, days_future=7, **kwargs):
    future_date = timezone.now() + timedelta(days=days_future)
    return Task.objects.create(
        user=user,
        title=title,
        due_date=future_date,
        **kwargs
    )
