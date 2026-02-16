# Generated migration for enhanced Task and User models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Add new fields to Task model
        migrations.AddField(
            model_name='task',
            name='completed_at',
            field=models.DateTimeField(blank=True, help_text='When the task was marked as completed', null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='is_deleted',
            field=models.BooleanField(db_index=True, default=False, help_text='Soft delete flag'),
        ),
        migrations.AddField(
            model_name='task',
            name='deleted_at',
            field=models.DateTimeField(blank=True, help_text='When the task was deleted', null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='tags',
            field=models.CharField(blank=True, help_text='Comma-separated tags for task organization', max_length=500),
        ),
        
        # Remove old indexes
        migrations.RemoveIndex(
            model_name='task',
            name='task_user_status_idx',
        ),
        migrations.RemoveIndex(
            model_name='task',
            name='task_priority_due_idx',
        ),
        migrations.RemoveIndex(
            model_name='task',
            name='task_user_created_idx',
        ),
        
        # Add new indexes with soft delete awareness
        migrations.AddIndex(
            model_name='task',
            index=models.Index(fields=['user', 'status', 'is_deleted'], name='task_user_status_del_idx'),
        ),
        migrations.AddIndex(
            model_name='task',
            index=models.Index(fields=['priority', 'due_date', 'is_deleted'], name='task_priority_due_del_idx'),
        ),
        migrations.AddIndex(
            model_name='task',
            index=models.Index(fields=['user', '-created_at', 'is_deleted'], name='task_user_created_del_idx'),
        ),
        
        # Add database constraint
        migrations.AddConstraint(
            model_name='task',
            constraint=models.CheckConstraint(
                check=models.Q(('due_date__gte', models.F('created_at__date')), ('due_date__isnull', True), _connector='OR'),
                name='due_date_after_creation'
            ),
        ),
        
        # Create TaskHistory model
        migrations.CreateModel(
            name='TaskHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.CharField(help_text='Name of the field that was changed', max_length=100)),
                ('old_value', models.TextField(blank=True, help_text='Previous value of the field')),
                ('new_value', models.TextField(blank=True, help_text='New value of the field')),
                ('changed_at', models.DateTimeField(auto_now_add=True, db_index=True, help_text='When the change was made')),
                ('changed_by', models.ForeignKey(help_text='User who made the change', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(help_text='Task this history entry belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='history', to='tasks.task')),
            ],
            options={
                'verbose_name': 'Task History',
                'verbose_name_plural': 'Task Histories',
                'ordering': ['-changed_at'],
            },
        ),
        migrations.AddIndex(
            model_name='taskhistory',
            index=models.Index(fields=['task', '-changed_at'], name='task_history_task_time_idx'),
        ),
    ]
