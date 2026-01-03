"""Test settings for CI/CD and pytest.

Optimized for fast test execution.
Use: DJANGO_SETTINGS_MODULE=config.settings.test
"""
from .base import *

# Debug off for testing (closer to production)
DEBUG = False

# Mark that we're in testing mode
TESTING = True

# Allow all hosts for testing
ALLOWED_HOSTS = ['*', 'testserver']

# CORS - Allow all for testing
CORS_ALLOW_ALL_ORIGINS = True

# Use faster password hasher for tests (dramatically speeds up user creation)
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Email - Use in-memory backend (no actual emails sent)
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Celery - Execute tasks synchronously in tests
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Disable migrations for faster test database creation
# Uncomment if you want even faster tests
# class DisableMigrations:
#     def __contains__(self, item):
#         return True
#     def __getitem__(self, item):
#         return None
# MIGRATION_MODULES = DisableMigrations()

# Optional: Use SQLite for faster tests (if not testing PostgreSQL-specific features)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': ':memory:',
#     }
# }

# Logging - Minimal logging in tests
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'ERROR',  # Only show errors
    },
}
