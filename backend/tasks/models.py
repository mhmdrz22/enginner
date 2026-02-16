from django.conf import settings
from django.db import models
from django.utils import timezone


class Task(models.Model):
    """Enhanced Task model with audit trail and soft delete.
    
    New features:
    - Soft delete functionality (is_deleted, deleted_at)
    - Task completion tracking (completed_at)
    - Tags for better organization
    - Enhanced indexes for complex queries
    - Database constraints for data integrity
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
        db_index=True,
        help_text="User who owns this task"
    )
    title = models.CharField(
        max_length=200,
        db_index=True,
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
        db_index=True,
        help_text="Current status of the task"
    )
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
        db_index=True,
        help_text="Task priority level"
    )
    due_date = models.DateField(
        null=True,
        blank=True,
        db_index=True,
        help_text="Task deadline"
    )
    
    # Audit fields
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the task was marked as completed"
    )
    
    # Soft delete fields
    is_deleted = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Soft delete flag"
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the task was deleted"
    )
    
    # Additional organization
    tags = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated tags for task organization"
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            # Composite index for user dashboard with soft delete filter
            models.Index(
                fields=['user', 'status', 'is_deleted'],
                name='task_user_status_del_idx'
            ),
            # Composite index for priority and deadline queries
            models.Index(
                fields=['priority', 'due_date', 'is_deleted'],
                name='task_priority_due_del_idx'
            ),
            # Composite index for recent active tasks
            models.Index(
                fields=['user', '-created_at', 'is_deleted'],
                name='task_user_created_del_idx'
            ),
        ]
        constraints = [
            # Ensure due_date is not before creation date
            models.CheckConstraint(
                check=models.Q(due_date__gte=models.F('created_at__date')) | models.Q(due_date__isnull=True),
                name='due_date_after_creation'
            ),
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
        if self.due_date and self.status != self.Status.DONE and not self.is_deleted:
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
    
    def soft_delete(self):
        """Soft delete the task."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=['is_deleted', 'deleted_at'])
    
    def restore(self):
        """Restore a soft-deleted task."""
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=['is_deleted', 'deleted_at'])
    
    def mark_completed(self):
        """Mark task as completed."""
        self.status = self.Status.DONE
        self.completed_at = timezone.now()
        self.save(update_fields=['status', 'completed_at'])
    
    def get_tags_list(self):
        """Return tags as a list."""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def set_tags_list(self, tags_list):
        """Set tags from a list."""
        self.tags = ','.join(tags_list)


class TaskHistory(models.Model):
    """Audit trail for task modifications.
    
    Tracks all changes made to tasks for accountability and history.
    """
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='history',
        help_text="Task this history entry belongs to"
    )
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        help_text="User who made the change"
    )
    field_name = models.CharField(
        max_length=100,
        help_text="Name of the field that was changed"
    )
    old_value = models.TextField(
        blank=True,
        help_text="Previous value of the field"
    )
    new_value = models.TextField(
        blank=True,
        help_text="New value of the field"
    )
    changed_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="When the change was made"
    )
    
    class Meta:
        ordering = ['-changed_at']
        verbose_name = "Task History"
        verbose_name_plural = "Task Histories"
        indexes = [
            models.Index(
                fields=['task', '-changed_at'],
                name='task_history_task_time_idx'
            ),
        ]
    
    def __str__(self):
        return f"{self.task.title} - {self.field_name} changed at {self.changed_at}"
