"""Health check URLs."""

from django.urls import path
from . import health_views


urlpatterns = [
    path("", health_views.health_check, name="health-check"),
    path("db/", health_views.database_health, name="database-health"),
    path("redis/", health_views.redis_health, name="redis-health"),
    path("detailed/", health_views.detailed_health, name="detailed-health"),
]
