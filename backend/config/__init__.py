# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.

# Make celery import optional to prevent errors when celery is not installed
try:
    from .celery import app as celery_app
    __all__ = ('celery_app',)
except ImportError:
    # Celery is optional - application will work without it
    pass
