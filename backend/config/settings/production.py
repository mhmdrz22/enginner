"""Production settings with security hardening.

Use: DJANGO_SETTINGS_MODULE=config.settings.production
"""
from .base import *
import os

# Security: Debug must be False in production
DEBUG = False

# Security: Only allow specific hosts
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

if not ALLOWED_HOSTS or ALLOWED_HOSTS == ['']:
    raise ValueError(
        "ALLOWED_HOSTS must be set in production. "
        "Example: ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com"
    )

# CORS - Only allow specific origins in production
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = os.environ.get(
    'CORS_ALLOWED_ORIGINS',
    ''
).split(',')

if not CORS_ALLOWED_ORIGINS or CORS_ALLOWED_ORIGINS == ['']:
    raise ValueError(
        "CORS_ALLOWED_ORIGINS must be set in production. "
        "Example: CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com"
    )

# Security Headers
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True') == 'True'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Security: Secret key must be set via environment variable
if SECRET_KEY == 'django-insecure-change-me-in-production':
    raise ValueError(
        "SECRET_KEY must be set in production. "
        "Generate with: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'"
    )

# Logging - Console-based for Docker (not file-based)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

# Email - Use real SMTP in production
if os.environ.get('EMAIL_HOST'):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.environ.get('EMAIL_HOST')
    EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
    EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
    DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', f'noreply@{ALLOWED_HOSTS[0]}')
else:
    # Fallback to console backend if email not configured
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Database - Conditional SSL based on environment
if 'default' in DATABASES:
    # Enable connection pooling in production
    DATABASES['default']['CONN_MAX_AGE'] = 600
    
    # Only use SSL if explicitly enabled (for managed DB services like AWS RDS)
    # Docker Postgres doesn't have SSL by default
    if os.environ.get('DB_USE_SSL', 'False') == 'True':
        DATABASES['default']['OPTIONS'] = {
            'sslmode': 'require',
            'connect_timeout': 10,
        }
    else:
        # Docker/local Postgres without SSL
        DATABASES['default']['OPTIONS'] = {
            'connect_timeout': 10,
        }
