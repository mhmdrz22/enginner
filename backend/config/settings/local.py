"""Local development settings.

For faster development with minimal security restrictions.
Use: DJANGO_SETTINGS_MODULE=config.settings.local
"""
from .base import *

# Debug mode - show detailed error pages
DEBUG = True

# Allow all hosts for easy local development
ALLOWED_HOSTS = ["*"]

# CORS - Allow all origins for local development
CORS_ALLOW_ALL_ORIGINS = True

# Email - Print to console instead of sending
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Logging - More verbose in development
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
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
    },
}

# Optional: Add Django Debug Toolbar for local development
# Uncomment if you have django-debug-toolbar installed
# INSTALLED_APPS += ['debug_toolbar']
# MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
# INTERNAL_IPS = ['127.0.0.1', 'localhost']
