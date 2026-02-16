from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator
import pyotp
import secrets
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
        extra_fields.setdefault('is_verified', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, db_index=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    # Email verification
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=64, blank=True, null=True)
    verification_token_created = models.DateTimeField(null=True, blank=True)
    
    # Password reset
    reset_token = models.CharField(max_length=64, blank=True, null=True)
    reset_token_created = models.DateTimeField(null=True, blank=True)
    
    # Account lockout
    failed_login_attempts = models.IntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)
    
    # 2FA
    two_factor_enabled = models.BooleanField(default=False)
    two_factor_secret = models.CharField(max_length=32, blank=True, null=True)
    backup_codes = models.JSONField(default=list, blank=True)
    
    # Password policy
    password_changed_at = models.DateTimeField(default=timezone.now)
    password_history = models.JSONField(default=list, blank=True)  # Store hashed passwords
    
    # GDPR
    gdpr_consent = models.BooleanField(default=False)
    gdpr_consent_date = models.DateTimeField(null=True, blank=True)
    data_processing_consent = models.BooleanField(default=False)
    
    # Rate limiting
    last_login_attempt = models.DateTimeField(null=True, blank=True)
    api_request_count = models.IntegerField(default=0)
    api_request_reset_time = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        ordering = ['-date_joined']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['is_verified']),
            models.Index(fields=['locked_until']),
        ]

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.email

    def generate_verification_token(self):
        """Generate email verification token"""
        self.verification_token = secrets.token_urlsafe(32)
        self.verification_token_created = timezone.now()
        self.save(update_fields=['verification_token', 'verification_token_created'])
        return self.verification_token

    def verify_email(self, token):
        """Verify email with token"""
        if not self.verification_token or self.verification_token != token:
            return False
        
        # Check token expiry (24 hours)
        if self.verification_token_created:
            expiry = self.verification_token_created + timedelta(hours=24)
            if timezone.now() > expiry:
                return False
        
        self.is_verified = True
        self.verification_token = None
        self.verification_token_created = None
        self.save(update_fields=['is_verified', 'verification_token', 'verification_token_created'])
        return True

    def generate_reset_token(self):
        """Generate password reset token"""
        self.reset_token = secrets.token_urlsafe(32)
        self.reset_token_created = timezone.now()
        self.save(update_fields=['reset_token', 'reset_token_created'])
        return self.reset_token

    def verify_reset_token(self, token):
        """Verify password reset token"""
        if not self.reset_token or self.reset_token != token:
            return False
        
        # Check token expiry (1 hour)
        if self.reset_token_created:
            expiry = self.reset_token_created + timedelta(hours=1)
            if timezone.now() > expiry:
                return False
        
        return True

    def reset_password(self, new_password):
        """Reset password and clear token"""
        self.set_password(new_password)
        self.reset_token = None
        self.reset_token_created = None
        self.password_changed_at = timezone.now()
        self.failed_login_attempts = 0
        self.locked_until = None
        self.save()

    def record_failed_login(self):
        """Record failed login attempt"""
        self.failed_login_attempts += 1
        self.last_login_attempt = timezone.now()
        
        # Lock account after 5 failed attempts
        if self.failed_login_attempts >= 5:
            self.locked_until = timezone.now() + timedelta(minutes=30)
        
        self.save(update_fields=['failed_login_attempts', 'last_login_attempt', 'locked_until'])

    def reset_failed_logins(self):
        """Reset failed login counter"""
        self.failed_login_attempts = 0
        self.locked_until = None
        self.save(update_fields=['failed_login_attempts', 'locked_until'])

    def is_locked(self):
        """Check if account is locked"""
        if self.locked_until and timezone.now() < self.locked_until:
            return True
        return False

    def enable_two_factor(self):
        """Enable 2FA and generate secret"""
        self.two_factor_secret = pyotp.random_base32()
        self.two_factor_enabled = True
        self.generate_backup_codes()
        self.save(update_fields=['two_factor_secret', 'two_factor_enabled', 'backup_codes'])
        return self.two_factor_secret

    def disable_two_factor(self):
        """Disable 2FA"""
        self.two_factor_enabled = False
        self.two_factor_secret = None
        self.backup_codes = []
        self.save(update_fields=['two_factor_enabled', 'two_factor_secret', 'backup_codes'])

    def generate_backup_codes(self, count=10):
        """Generate backup codes for 2FA"""
        self.backup_codes = [secrets.token_hex(4) for _ in range(count)]
        self.save(update_fields=['backup_codes'])
        return self.backup_codes

    def verify_totp(self, code):
        """Verify TOTP code"""
        if not self.two_factor_enabled or not self.two_factor_secret:
            return False
        
        totp = pyotp.TOTP(self.two_factor_secret)
        return totp.verify(code, valid_window=1)

    def verify_backup_code(self, code):
        """Verify and consume backup code"""
        if code in self.backup_codes:
            self.backup_codes.remove(code)
            self.save(update_fields=['backup_codes'])
            return True
        return False

    def get_totp_uri(self):
        """Get TOTP URI for QR code"""
        if not self.two_factor_secret:
            return None
        return pyotp.totp.TOTP(self.two_factor_secret).provisioning_uri(
            name=self.email,
            issuer_name='TaskBoard'
        )

    def add_to_password_history(self):
        """Add current password to history"""
        if not self.password_history:
            self.password_history = []
        
        # Keep last 5 passwords
        self.password_history.append(self.password)
        self.password_history = self.password_history[-5:]
        self.save(update_fields=['password_history'])

    def check_password_reuse(self, raw_password):
        """Check if password was used before"""
        from django.contrib.auth.hashers import check_password
        
        for old_hash in self.password_history:
            if check_password(raw_password, old_hash):
                return True
        return False

    def give_gdpr_consent(self):
        """Record GDPR consent"""
        self.gdpr_consent = True
        self.gdpr_consent_date = timezone.now()
        self.data_processing_consent = True
        self.save(update_fields=['gdpr_consent', 'gdpr_consent_date', 'data_processing_consent'])

    def export_personal_data(self):
        """Export user's personal data (GDPR)"""
        return {
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_joined': self.date_joined.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_verified': self.is_verified,
            'two_factor_enabled': self.two_factor_enabled,
            'gdpr_consent': self.gdpr_consent,
            'gdpr_consent_date': self.gdpr_consent_date.isoformat() if self.gdpr_consent_date else None,
        }
