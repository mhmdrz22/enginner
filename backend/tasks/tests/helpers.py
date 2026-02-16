from django.utils import timezone
from datetime import timedelta
from tasks.models import Task

def create_task_with_past_due_date(user, title, days_overdue=1, **kwargs):
    """Helper to create a task with a due_date in the past."""
    
    due_date = kwargs.get('due_date') or (timezone.now() - timedelta(days=days_overdue))
    created_at = due_date - timedelta(days=1)

    task_kwargs = {k: v for k, v in kwargs.items() if k != 'due_date' and k != 'created_at'}

    task = Task.objects.create(
        user=user,
        title=title,
        **task_kwargs
    )
    
    # Direct DB update with correct field name to bypass auto_now_add
    Task.objects.filter(pk=task.pk).update(
        due_date=due_date,
        created_at=created_at
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
