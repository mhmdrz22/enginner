from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password as django_validate_password
from django.utils import timezone
from rest_framework.throttling import SimpleRateThrottle
from functools import wraps
import re


class PasswordPolicyValidator:
    """Custom password validator for enforcing password policy."""
    
    def __init__(self, min_length=8, require_uppercase=True, require_lowercase=True,
                 require_digit=True, require_special=True):
        self.min_length = min_length
        self.require_uppercase = require_uppercase
        self.require_lowercase = require_lowercase
        self.require_digit = require_digit
        self.require_special = require_special
    
    def validate(self, password, user=None):
        errors = []
        
        if len(password) < self.min_length:
            errors.append(f'Password must be at least {self.min_length} characters long.')
        
        if self.require_uppercase and not re.search(r'[A-Z]', password):
            errors.append('Password must contain at least one uppercase letter.')
        
        if self.require_lowercase and not re.search(r'[a-z]', password):
            errors.append('Password must contain at least one lowercase letter.')
        
        if self.require_digit and not re.search(r'\d', password):
            errors.append('Password must contain at least one digit.')
        
        if self.require_special and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append('Password must contain at least one special character.')
        
        if errors:
            raise ValidationError(errors)
    
    def get_help_text(self):
        return (
            f'Your password must be at least {self.min_length} characters long, '
            'contain uppercase and lowercase letters, digits, and special characters.'
        )


def validate_password_strength(password, user=None):
    """Validate password against policy."""
    validator = PasswordPolicyValidator()
    validator.validate(password, user)
    django_validate_password(password, user)


def check_password_history(user, password, max_history=5):
    """Check if password was used recently."""
    from .models import PasswordHistory
    from django.contrib.auth.hashers import check_password
    
    recent_passwords = PasswordHistory.objects.filter(user=user)[:max_history]
    for history in recent_passwords:
        if check_password(password, history.password_hash):
            raise ValidationError('You cannot reuse your last 5 passwords.')


def save_password_to_history(user):
    """Save current password to history."""
    from .models import PasswordHistory
    PasswordHistory.objects.create(
        user=user,
        password_hash=user.password
    )


class UserRateThrottle(SimpleRateThrottle):
    """Rate throttling per authenticated user."""
    scope = 'user'

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)
        
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }


class LoginRateThrottle(SimpleRateThrottle):
    """Rate throttling for login attempts."""
    scope = 'login'
    rate = '5/hour'

    def get_cache_key(self, request, view):
        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }


class PasswordResetRateThrottle(SimpleRateThrottle):
    """Rate throttling for password reset requests."""
    scope = 'password_reset'
    rate = '3/hour'

    def get_cache_key(self, request, view):
        email = request.data.get('email', '')
        return self.cache_format % {
            'scope': self.scope,
            'ident': email or self.get_ident(request)
        }


def rate_limit(key_prefix, limit, period):
    """Custom rate limiting decorator.
    
    Args:
        key_prefix: Prefix for cache key
        limit: Number of allowed requests
        period: Time period in seconds
    """
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                cache_key = f'{key_prefix}:{request.user.id}'
            else:
                cache_key = f'{key_prefix}:{request.META.get("REMOTE_ADDR")}'
            
            current = cache.get(cache_key, 0)
            
            if current >= limit:
                from rest_framework.exceptions import Throttled
                raise Throttled(detail=f'Rate limit exceeded. Try again in {period} seconds.')
            
            cache.set(cache_key, current + 1, period)
            return func(request, *args, **kwargs)
        
        return wrapper
    return decorator


def email_verified_required(view_func):
    """Decorator to require email verification."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.email_verified:
            from rest_framework.response import Response
            from rest_framework import status
            return Response(
                {'detail': 'Email verification required.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return view_func(request, *args, **kwargs)
    return wrapper


def two_factor_verified(view_func):
    """Decorator to require 2FA verification for sensitive operations."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.two_factor_enabled:
            # Check if 2FA was verified in this session
            if not request.session.get('2fa_verified', False):
                from rest_framework.response import Response
                from rest_framework import status
                return Response(
                    {'detail': '2FA verification required.'},
                    status=status.HTTP_403_FORBIDDEN
                )
        return view_func(request, *args, **kwargs)
    return wrapper
