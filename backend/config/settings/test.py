"""Test settings for CI/CD and pytest.

Optimized for testing with PostgreSQL.
Use: DJANGO_SETTINGS_MODULE=config.settings.test
"""
import os
import dj_database_url
import urllib.parse
from .base import *

# Debug ON for testing (avoid static file issues)
DEBUG = True

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
# Ensure we prioritize the environment variables for host/port if set, defaulting to localhost if not.
_postgres_user = urllib.parse.quote_plus(os.environ.get('POSTGRES_USER', 'postgres'))
_postgres_password = urllib.parse.quote_plus(os.environ.get('POSTGRES_PASSWORD', 'postgres'))
_postgres_host = os.environ.get('POSTGRES_HOST', 'localhost')
_postgres_port = os.environ.get('POSTGRES_PORT', '5432')
_postgres_db = os.environ.get('POSTGRES_DB', 'test_taskboard')

DATABASES = {
    'default': dj_database_url.config(
        default=f"postgres://{_postgres_user}:{_postgres_password}@{_postgres_host}:{_postgres_port}/{_postgres_db}",
        conn_max_age=0,
    )
}
DATABASES['default']['ATOMIC_REQUESTS'] = True
DATABASES['default']['TEST'] = {
    'NAME': 'test_taskboard_test',
}

# Cache - Use local memory cache for tests (no Redis needed)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'test-cache',
    }
}

# Session - Use database backend for tests (simpler than cache)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

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
STATIC_URL = '/static/'

# Media files - Use temporary directory
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles_test')
MEDIA_URL = '/media/'

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
