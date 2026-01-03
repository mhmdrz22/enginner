from django.conf import settings
from django.db import models


class Task(models.Model):
    """Task model for task management system.
    
    Optimized with database indexes for common query patterns.
    """
    
    class Status(models.TextChoices):
        """Task status choices using TextChoices (Django 3.0+)."""
        TODO = 'TODO', 'To Do'
        DOING = 'DOING', 'Doing'
        DONE = 'DONE', 'Done'
    
    class Priority(models.TextChoices):
        """Task priority choices using TextChoices (Django 3.0+)."""
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks",
        null=True,
        blank=True,
        help_text="User who owns this task"
    )
    title = models.CharField(
        max_length=200,
        help_text="Task title"
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed task description"
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.TODO,
        db_index=True,  # Index for filtering by status (admin queries)
        help_text="Current status of the task"
    )
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
        db_index=True,  # Index for filtering by priority
        help_text="Task priority level"
    )
    due_date = models.DateField(
        null=True,
        blank=True,
        db_index=True,  # Index for deadline queries
        help_text="Task deadline"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,  # Index for sorting by creation date
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            # Composite index for common admin panel query:
            # "Show me TODO/DOING tasks for a specific user"
            models.Index(fields=['user', 'status'], name='task_user_status_idx'),
            
            # Composite index for deadline tracking:
            # "Show me high priority tasks due soon"
            models.Index(fields=['priority', 'due_date'], name='task_priority_due_idx'),
            
            # Composite index for user dashboard:
            # "Show my recent tasks by status"
            models.Index(fields=['user', '-created_at'], name='task_user_created_idx'),
        ]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return self.title
    
    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}')>"
    
    @property
    def is_overdue(self):
        """Check if task is overdue."""
        if self.due_date and self.status != self.Status.DONE:
            from django.utils import timezone
            return timezone.now().date() > self.due_date
        return False
    
    @property
    def status_display(self):
        """Get human-readable status."""
        return self.get_status_display()
    
    @property
    def priority_display(self):
        """Get human-readable priority."""
        return self.get_priority_display()
