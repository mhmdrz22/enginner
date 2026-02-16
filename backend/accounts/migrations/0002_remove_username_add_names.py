# Generated migration to remove username and add first_name, last_name
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        # Add first_name and last_name fields
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, help_text="User's first name", max_length=150, verbose_name='first name'),
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, help_text="User's last name", max_length=150, verbose_name='last name'),
        ),
        
        # Add last_login_date field
        migrations.AddField(
            model_name='user',
            name='last_login_date',
            field=models.DateTimeField(blank=True, help_text='Last time user logged in', null=True, verbose_name='last login'),
        ),
        
        # Remove username field
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        
        # Update Meta options
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        
        # Add new indexes
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['email', 'is_active'], name='user_email_active_idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['-created_date'], name='user_created_idx'),
        ),
        
        # Alter email field to add db_index
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(db_index=True, help_text="User's email address (used for login)", max_length=254, unique=True, verbose_name='email address'),
        ),
        
        # Alter created_date to add db_index
        migrations.AlterField(
            model_name='user',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='date joined'),
        ),
        
        # Update field help texts
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates whether the user can log into the admin site.', verbose_name='staff status'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active.', verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_verified',
            field=models.BooleanField(default=False, help_text='Designates whether this user has verified their email.', verbose_name='verified'),
        ),
        migrations.AlterField(
            model_name='user',
            name='updated_date',
            field=models.DateTimeField(auto_now=True, verbose_name='date updated'),
        ),
    ]
