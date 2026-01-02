#!/bin/sh

set -e

echo "Waiting for database..."
while ! nc -z $DB_HOST ${DB_PORT:-5432}; do
  sleep 0.5
done
echo "Database is ready!"

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers ${GUNICORN_WORKERS:-3} \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
