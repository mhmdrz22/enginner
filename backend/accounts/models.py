from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from datetime import timedelta
import secrets
import pyotp


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
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


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    
    # Email verification
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, blank=True)
    email_verification_sent_at = models.DateTimeField(null=True, blank=True)
    
    # Password reset
    password_reset_token = models.CharField(max_length=100, blank=True)
    password_reset_sent_at = models.DateTimeField(null=True, blank=True)
    
    # Account security
    failed_login_attempts = models.IntegerField(default=0)
    account_locked_until = models.DateTimeField(null=True, blank=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    
    # 2FA
    two_factor_enabled = models.BooleanField(default=False)
    two_factor_secret = models.CharField(max_length=32, blank=True)
    backup_codes = models.JSONField(default=list, blank=True)
    
    # GDPR
    privacy_policy_accepted = models.BooleanField(default=False)
    privacy_policy_accepted_at = models.DateTimeField(null=True, blank=True)
    data_processing_consent = models.BooleanField(default=False)
    marketing_consent = models.BooleanField(default=False)
    
    # Password history for policy enforcement
    password_history = models.JSONField(default=list, blank=True)
    password_changed_at = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def generate_email_verification_token(self):
        """Generate secure token for email verification"""
        self.email_verification_token = secrets.token_urlsafe(32)
        self.email_verification_sent_at = timezone.now()
        self.save(update_fields=['email_verification_token', 'email_verification_sent_at'])
        return self.email_verification_token
    
    def verify_email(self, token):
        """Verify email with token"""
        if self.email_verification_token != token:
            return False
        
        # Check if token is expired (24 hours)
        if self.email_verification_sent_at:
            expiry = self.email_verification_sent_at + timedelta(hours=24)
            if timezone.now() > expiry:
                return False
        
        self.email_verified = True
        self.email_verification_token = ''
        self.save(update_fields=['email_verified', 'email_verification_token'])
        return True
    
    def generate_password_reset_token(self):
        """Generate secure token for password reset"""
        self.password_reset_token = secrets.token_urlsafe(32)
        self.password_reset_sent_at = timezone.now()
        self.save(update_fields=['password_reset_token', 'password_reset_sent_at'])
        return self.password_reset_token
    
    def verify_password_reset_token(self, token):
        """Verify password reset token"""
        if self.password_reset_token != token:
            return False
        
        # Check if token is expired (1 hour)
        if self.password_reset_sent_at:
            expiry = self.password_reset_sent_at + timedelta(hours=1)
            if timezone.now() > expiry:
                return False
        
        return True
    
    def reset_password(self, token, new_password):
        """Reset password with token"""
        if not self.verify_password_reset_token(token):
            return False
        
        self.set_password(new_password)
        self.password_reset_token = ''
        self.password_changed_at = timezone.now()
        self.save()
        return True
    
    def is_account_locked(self):
        """Check if account is locked"""
        if self.account_locked_until:
            if timezone.now() < self.account_locked_until:
                return True
            else:
                # Unlock account
                self.account_locked_until = None
                self.failed_login_attempts = 0
                self.save(update_fields=['account_locked_until', 'failed_login_attempts'])
        return False
    
    def record_failed_login(self):
        """Record failed login attempt and lock if threshold exceeded"""
        self.failed_login_attempts += 1
        
        # Lock account after 5 failed attempts for 30 minutes
        if self.failed_login_attempts >= 5:
            self.account_locked_until = timezone.now() + timedelta(minutes=30)
        
        self.save(update_fields=['failed_login_attempts', 'account_locked_until'])
    
    def reset_failed_login_attempts(self):
        """Reset failed login attempts after successful login"""
        self.failed_login_attempts = 0
        self.account_locked_until = None
        self.save(update_fields=['failed_login_attempts', 'account_locked_until'])
    
    def setup_two_factor(self):
        """Setup 2FA and return secret"""
        self.two_factor_secret = pyotp.random_base32()
        self.two_factor_enabled = False  # User must verify first
        self.save(update_fields=['two_factor_secret', 'two_factor_enabled'])
        return self.two_factor_secret
    
    def get_totp_uri(self):
        """Get TOTP URI for QR code"""
        if not self.two_factor_secret:
            self.setup_two_factor()
        return pyotp.totp.TOTP(self.two_factor_secret).provisioning_uri(
            name=self.email,
            issuer_name='TaskBoard'
        )
    
    def verify_totp(self, token):
        """Verify TOTP token"""
        if not self.two_factor_secret:
            return False
        totp = pyotp.TOTP(self.two_factor_secret)
        return totp.verify(token, valid_window=1)
    
    def enable_two_factor(self, token):
        """Enable 2FA after verifying token"""
        if self.verify_totp(token):
            self.two_factor_enabled = True
            self.generate_backup_codes()
            self.save(update_fields=['two_factor_enabled'])
            return True
        return False
    
    def generate_backup_codes(self, count=10):
        """Generate backup codes for 2FA"""
        codes = [secrets.token_hex(4).upper() for _ in range(count)]
        self.backup_codes = codes
        self.save(update_fields=['backup_codes'])
        return codes
    
    def verify_backup_code(self, code):
        """Verify and consume backup code"""
        if code.upper() in self.backup_codes:
            self.backup_codes.remove(code.upper())
            self.save(update_fields=['backup_codes'])
            return True
        return False
    
    def add_password_to_history(self, password_hash):
        """Add password to history (keep last 5)"""
        if not self.password_history:
            self.password_history = []
        
        self.password_history.insert(0, password_hash)
        self.password_history = self.password_history[:5]  # Keep only last 5
        self.save(update_fields=['password_history'])
    
    def is_password_in_history(self, password):
        """Check if password was used before"""
        from django.contrib.auth.hashers import check_password
        for old_hash in self.password_history:
            if check_password(password, old_hash):
                return True
        return False


class LoginAttempt(models.Model):
    """Track login attempts for rate limiting"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    successful = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    user_agent = models.CharField(max_length=255, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['ip_address', 'timestamp']),
            models.Index(fields=['user', 'timestamp']),
        ]


class UserActivity(models.Model):
    """Track user activity for GDPR compliance"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    details = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'User activities'
