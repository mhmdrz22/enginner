# Generated migration for security features

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        # Email Verification
        migrations.AddField(
            model_name='user',
            name='email_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='email_verification_token',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='email_verification_sent_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        
        # Password Reset
        migrations.AddField(
            model_name='user',
            name='password_reset_token',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='password_reset_token_created',
            field=models.DateTimeField(blank=True, null=True),
        ),
        
        # Account Lockout
        migrations.AddField(
            model_name='user',
            name='failed_login_attempts',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='locked_until',
            field=models.DateTimeField(blank=True, null=True),
        ),
        
        # Password Policy
        migrations.AddField(
            model_name='user',
            name='password_changed_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='user',
            name='password_expiry_days',
            field=models.IntegerField(default=90),
        ),
        
        # 2FA
        migrations.AddField(
            model_name='user',
            name='two_factor_enabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='two_factor_secret',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='backup_codes',
            field=models.JSONField(blank=True, default=list),
        ),
        
        # GDPR
        migrations.AddField(
            model_name='user',
            name='gdpr_consent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='gdpr_consent_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='data_processing_consent',
            field=models.BooleanField(default=False),
        ),
        
        # Indexes
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['email_verified'], name='accounts_user_email_verified_idx'),
        ),
        
        # Password History Model
        migrations.CreateModel(
            name='PasswordHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password_hash', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='password_history', to='accounts.user')),
            ],
            options={
                'verbose_name_plural': 'Password histories',
                'ordering': ['-created_at'],
            },
        ),
        
        # Login Attempt Model
        migrations.CreateModel(
            name='LoginAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('ip_address', models.GenericIPAddressField()),
                ('user_agent', models.TextField(blank=True)),
                ('success', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('failure_reason', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.AddIndex(
            model_name='loginattempt',
            index=models.Index(fields=['email', 'timestamp'], name='accounts_loginattempt_email_timestamp_idx'),
        ),
        migrations.AddIndex(
            model_name='loginattempt',
            index=models.Index(fields=['ip_address', 'timestamp'], name='accounts_loginattempt_ip_timestamp_idx'),
        ),
        
        # GDPR Request Model
        migrations.CreateModel(
            name='GDPRRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_type', models.CharField(choices=[('export', 'Data Export'), ('delete', 'Right to be Forgotten')], max_length=10)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending', max_length=20)),
                ('requested_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('export_file', models.FileField(blank=True, null=True, upload_to='gdpr_exports/')),
                ('notes', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gdpr_requests', to='accounts.user')),
            ],
            options={
                'ordering': ['-requested_at'],
            },
        ),
    ]
