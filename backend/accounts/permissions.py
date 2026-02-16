from rest_framework import permissions
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta


class IsEmailVerified(permissions.BasePermission):
    """Allow access only to users with verified email"""
    message = 'Email verification required.'
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.email_verified
        )


class IsAccountNotLocked(permissions.BasePermission):
    """Allow access only to users with unlocked accounts"""
    message = 'Account is temporarily locked due to failed login attempts.'
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return True
        return not request.user.is_account_locked()


class HasAcceptedPrivacyPolicy(permissions.BasePermission):
    """Require privacy policy acceptance for GDPR compliance"""
    message = 'You must accept the privacy policy to continue.'
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return True
        return request.user.privacy_policy_accepted


class LoginRateThrottle(AnonRateThrottle):
    """Rate limit login attempts: 5 per minute"""
    rate = '5/min'
    scope = 'login'


class RegisterRateThrottle(AnonRateThrottle):
    """Rate limit registration: 3 per hour"""
    rate = '3/hour'
    scope = 'register'


class PasswordResetRateThrottle(AnonRateThrottle):
    """Rate limit password reset: 3 per hour"""
    rate = '3/hour'
    scope = 'password_reset'


class APIRateThrottle(UserRateThrottle):
    """Rate limit API calls: 100 per minute for authenticated users"""
    rate = '100/min'
    scope = 'api'


class StrictAPIRateThrottle(UserRateThrottle):
    """Strict rate limit for sensitive operations: 10 per minute"""
    rate = '10/min'
    scope = 'api_strict'


class PerUserRateLimiter:
    """Custom per-user rate limiter using Redis/cache"""
    
    def __init__(self, key_prefix, max_attempts, time_window):
        self.key_prefix = key_prefix
        self.max_attempts = max_attempts
        self.time_window = time_window  # in seconds
    
    def is_allowed(self, user_id):
        """Check if user is allowed to make request"""
        cache_key = f'{self.key_prefix}:{user_id}'
        attempts = cache.get(cache_key, 0)
        
        if attempts >= self.max_attempts:
            return False
        
        cache.set(cache_key, attempts + 1, self.time_window)
        return True
    
    def get_remaining_attempts(self, user_id):
        """Get remaining attempts for user"""
        cache_key = f'{self.key_prefix}:{user_id}'
        attempts = cache.get(cache_key, 0)
        return max(0, self.max_attempts - attempts)
    
    def reset(self, user_id):
        """Reset rate limit for user"""
        cache_key = f'{self.key_prefix}:{user_id}'
        cache.delete(cache_key)
