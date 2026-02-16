from django.utils import timezone
from datetime import timedelta

def create_task_with_past_due_date(user, title, days_overdue=1, **kwargs):
    """Helper to create a task with a due_date in the past."""
    from tasks.models import Task

    task_kwargs = {k: v for k, v in kwargs.items() if k != 'due_date'}
    
    task = Task.objects.create(
        user=user,
        title=title,
        **task_kwargs
    )
    
    if 'due_date' in kwargs:
        task.due_date = kwargs['due_date']
    else:
        past_date = timezone.now() - timedelta(days=days_overdue)
        task.due_date = past_date
    
    task.save(update_fields=['due_date'])
    task.refresh_from_db()
    
    return task

def create_future_task(user, title, days_future=7, **kwargs):
    from tasks.models import Task
    future_date = timezone.now() + timedelta(days=days_future)
    return Task.objects.create(
        user=user,
        title=title,
        due_date=future_date,
        **kwargs
    )
