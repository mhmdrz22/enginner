"""Health check views for monitoring."""

import redis
from django.http import JsonResponse
from django.db import connection
from django.conf import settings
from django.utils import timezone


def health_check(request):
    """Simple health check endpoint."""
    return JsonResponse({
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'service': 'Team Task Board API',
        'version': '1.0.0'
    })


def database_health(request):
    """Check database connectivity."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        
        return JsonResponse({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': timezone.now().isoformat()
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e),
            'timestamp': timezone.now().isoformat()
        }, status=503)


def redis_health(request):
    """Check Redis connectivity."""
    try:
        # Parse Redis URL
        redis_url = settings.CELERY_BROKER_URL
        
        # Connect to Redis
        r = redis.from_url(redis_url)
        r.ping()
        
        return JsonResponse({
            'status': 'healthy',
            'redis': 'connected',
            'timestamp': timezone.now().isoformat()
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'redis': 'disconnected',
            'error': str(e),
            'timestamp': timezone.now().isoformat()
        }, status=503)


def detailed_health(request):
    """Detailed health check with all services."""
    health_status = {
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'checks': {}
    }
    
    # Check database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        health_status['checks']['database'] = {
            'status': 'healthy',
            'message': 'Database connection OK'
        }
    except Exception as e:
        health_status['status'] = 'degraded'
        health_status['checks']['database'] = {
            'status': 'unhealthy',
            'error': str(e)
        }
    
    # Check Redis
    try:
        redis_url = settings.CELERY_BROKER_URL
        r = redis.from_url(redis_url)
        r.ping()
        health_status['checks']['redis'] = {
            'status': 'healthy',
            'message': 'Redis connection OK'
        }
    except Exception as e:
        health_status['status'] = 'degraded'
        health_status['checks']['redis'] = {
            'status': 'unhealthy',
            'error': str(e)
        }
    
    # Check disk space
    import shutil
    try:
        total, used, free = shutil.disk_usage("/")
        free_gb = free // (2**30)
        health_status['checks']['disk'] = {
            'status': 'healthy' if free_gb > 1 else 'warning',
            'free_space_gb': free_gb,
            'total_space_gb': total // (2**30)
        }
    except Exception as e:
        health_status['checks']['disk'] = {
            'status': 'unknown',
            'error': str(e)
        }
    
    # Overall status code
    status_code = 200
    if health_status['status'] == 'degraded':
        status_code = 503
    elif health_status['status'] == 'unhealthy':
        status_code = 503
    
    return JsonResponse(health_status, status=status_code)
