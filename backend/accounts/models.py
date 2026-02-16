from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator
import secrets
import pyotp
from datetime import timedelta


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('email_verified', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    # Email Verification
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, blank=True, null=True)
    email_verification_sent_at = models.DateTimeField(blank=True, null=True)
    
    # Password Reset
    password_reset_token = models.CharField(max_length=100, blank=True, null=True)
    password_reset_token_created = models.DateTimeField(blank=True, null=True)
    
    # Account Lockout
    failed_login_attempts = models.IntegerField(default=0)
    locked_until = models.DateTimeField(blank=True, null=True)
    
    # Password Policy
    password_changed_at = models.DateTimeField(default=timezone.now)
    password_expiry_days = models.IntegerField(default=90)
    
    # 2FA
    two_factor_enabled = models.BooleanField(default=False)
    two_factor_secret = models.CharField(max_length=32, blank=True, null=True)
    backup_codes = models.JSONField(default=list, blank=True)
    
    # GDPR
    gdpr_consent = models.BooleanField(default=False)
    gdpr_consent_date = models.DateTimeField(blank=True, null=True)
    data_processing_consent = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['-date_joined']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['email_verified']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.email
    
    # Email Verification
    def generate_verification_token(self):
        self.email_verification_token = secrets.token_urlsafe(32)
        self.email_verification_sent_at = timezone.now()
        self.save()
        return self.email_verification_token
    
    def verify_email(self, token):
        if self.email_verification_token == token:
            self.email_verified = True
            self.email_verification_token = None
            self.save()
            return True
        return False
    
    # Password Reset
    def generate_password_reset_token(self):
        self.password_reset_token = secrets.token_urlsafe(32)
        self.password_reset_token_created = timezone.now()
        self.save()
        return self.password_reset_token
    
    def verify_password_reset_token(self, token):
        if not self.password_reset_token or self.password_reset_token != token:
            return False
        
        # Token expires after 1 hour
        if timezone.now() > self.password_reset_token_created + timedelta(hours=1):
            return False
        
        return True
    
    def reset_password(self, token, new_password):
        if self.verify_password_reset_token(token):
            self.set_password(new_password)
            self.password_reset_token = None
            self.password_reset_token_created = None
            self.password_changed_at = timezone.now()
            self.save()
            return True
        return False
    
    # Account Lockout
    def is_locked(self):
        if self.locked_until and timezone.now() < self.locked_until:
            return True
        return False
    
    def increment_failed_login(self):
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:
            self.locked_until = timezone.now() + timedelta(minutes=30)
        self.save()
    
    def reset_failed_login(self):
        self.failed_login_attempts = 0
        self.locked_until = None
        self.save()
    
    # Password Policy
    def is_password_expired(self):
        expiry_date = self.password_changed_at + timedelta(days=self.password_expiry_days)
        return timezone.now() > expiry_date
    
    # 2FA
    def enable_two_factor(self):
        self.two_factor_secret = pyotp.random_base32()
        self.backup_codes = [secrets.token_hex(4) for _ in range(10)]
        self.two_factor_enabled = True
        self.save()
        return self.two_factor_secret
    
    def disable_two_factor(self):
        self.two_factor_enabled = False
        self.two_factor_secret = None
        self.backup_codes = []
        self.save()
    
    def verify_totp(self, token):
        if not self.two_factor_enabled or not self.two_factor_secret:
            return False
        totp = pyotp.TOTP(self.two_factor_secret)
        return totp.verify(token, valid_window=1)
    
    def verify_backup_code(self, code):
        if code in self.backup_codes:
            self.backup_codes.remove(code)
            self.save()
            return True
        return False
    
    def get_totp_uri(self):
        if not self.two_factor_secret:
            return None
        return pyotp.totp.TOTP(self.two_factor_secret).provisioning_uri(
            name=self.email,
            issuer_name='TaskBoard'
        )


class PasswordHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_history')
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Password histories'


class LoginAttempt(models.Model):
    email = models.EmailField()
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    success = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)
    failure_reason = models.CharField(max_length=255, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['email', 'timestamp']),
            models.Index(fields=['ip_address', 'timestamp']),
        ]


class GDPRRequest(models.Model):
    REQUEST_TYPES = [
        ('export', 'Data Export'),
        ('delete', 'Right to be Forgotten'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gdpr_requests')
    request_type = models.CharField(max_length=10, choices=REQUEST_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(blank=True, null=True)
    export_file = models.FileField(upload_to='gdpr_exports/', blank=True, null=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-requested_at']
