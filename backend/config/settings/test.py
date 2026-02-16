"""Test settings for CI/CD and pytest.

Optimized for testing with PostgreSQL.
Use: DJANGO_SETTINGS_MODULE=config.settings.test
"""
import os
from .base import *

# Debug off for testing (closer to production)
DEBUG = False

# Mark that we're in testing mode
TESTING = True

# Secret key - Allow override from environment for CI
SECRET_KEY = os.environ.get('SECRET_KEY', 'test-secret-key-do-not-use-in-production-' + 'x' * 50)

# Allow all hosts for testing
ALLOWED_HOSTS = ['*', 'testserver', 'localhost', '127.0.0.1']

# CORS - Allow all for testing
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Database - Use PostgreSQL (same as production)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'test_taskboard'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        'ATOMIC_REQUESTS': True,
        'CONN_MAX_AGE': 0,  # Close connections after each request in tests
        'TEST': {
            'NAME': 'test_taskboard_test',
        },
    }
}

# Cache - Use local memory cache for tests
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'test-cache',
    }
}

# Use faster password hasher for tests (dramatically speeds up user creation)
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Email - Use in-memory backend (no actual emails sent)
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Celery - Execute tasks synchronously in tests
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Static files - Use default for tests
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_test')

# Media files - Use temporary directory
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles_test')

# Logging - Minimal logging in tests (only errors)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'ERROR',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'ERROR',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

# Security - Disable for faster tests
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
