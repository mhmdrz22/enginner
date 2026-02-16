from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """Custom user manager that uses email for authentication."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("Email is required"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Enhanced User model with email as primary identifier.
    
    Changes:
    - Removed redundant username field (email serves as unique identifier)
    - Added first_name and last_name for better user profile
    - Added last_login_date for security tracking
    - Enhanced indexes for performance
    """
    email = models.EmailField(
        _("email address"),
        unique=True,
        db_index=True,
        help_text="User's email address (used for login)"
    )
    first_name = models.CharField(
        _("first name"),
        max_length=150,
        blank=True,
        help_text="User's first name"
    )
    last_name = models.CharField(
        _("last name"),
        max_length=150,
        blank=True,
        help_text="User's last name"
    )
    
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text="Designates whether the user can log into the admin site."
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text="Designates whether this user should be treated as active."
    )
    is_verified = models.BooleanField(
        _("verified"),
        default=False,
        help_text="Designates whether this user has verified their email."
    )
    
    created_date = models.DateTimeField(
        _("date joined"),
        auto_now_add=True,
        db_index=True
    )
    updated_date = models.DateTimeField(
        _("date updated"),
        auto_now=True
    )
    last_login_date = models.DateTimeField(
        _("last login"),
        null=True,
        blank=True,
        help_text="Last time user logged in"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # Remove username from required fields

    objects = UserManager()

    class Meta:
        db_table = 'users'
        verbose_name = _("user")
        verbose_name_plural = _("users")
        indexes = [
            models.Index(fields=['email', 'is_active'], name='user_email_active_idx'),
            models.Index(fields=['-created_date'], name='user_created_idx'),
        ]

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip() or self.email
    
    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name or self.email.split('@')[0]
