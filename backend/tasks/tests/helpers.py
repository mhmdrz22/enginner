"""Test helpers for tasks app."""
from django.utils import timezone
from datetime import timedelta


def create_task_with_past_due_date(user, title, days_overdue=1, **kwargs):
    """Helper to create a task with a due_date in the past.
    
    This bypasses the database constraint by creating the task first,
    then updating the due_date field separately.
    
    Args:
        user: The user who owns the task
        title: Task title
        days_overdue: Number of days in the past for due_date (default: 1)
        **kwargs: Additional task fields (status, priority, description, etc.)
    
    Returns:
        Task: The created task with past due_date
    
    Example:
        task = create_task_with_past_due_date(
            user=user,
            title='Overdue Task',
            status='TODO',
            priority='HIGH',
            days_overdue=3
        )
    """
    from tasks.models import Task
    
    # Separate due_date from other kwargs
    task_kwargs = {k: v for k, v in kwargs.items() if k != 'due_date'}
    
    # Create task without due_date first
    task = Task.objects.create(
        user=user,
        title=title,
        **task_kwargs
    )
    
    # Then update with past due_date
    if 'due_date' in kwargs:
        task.due_date = kwargs['due_date']
    else:
        past_date = timezone.now() - timedelta(days=days_overdue)
        task.due_date = past_date
    
    task.save(update_fields=['due_date'])
    task.refresh_from_db()
    
    return task


def create_future_task(user, title, days_future=7, **kwargs):
    """Helper to create a task with a future due_date.
    
    Args:
        user: The user who owns the task
        title: Task title
        days_future: Number of days in the future for due_date (default: 7)
        **kwargs: Additional task fields
    
    Returns:
        Task: The created task with future due_date
    """
    from tasks.models import Task
    
    future_date = timezone.now() + timedelta(days=days_future)
    
    return Task.objects.create(
        user=user,
        title=title,
        due_date=future_date,
        **kwargs
    )
