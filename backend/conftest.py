"""Pytest configuration for Django tests.

Ensures database migrations are run before tests.
"""
import pytest
from django.core.management import call_command


@pytest.fixture(scope='session', autouse=True)
def setup_test_database(django_db_setup, django_db_blocker):
    """Ensure migrations are applied to test database.
    
    This runs once per test session before any tests execute.
    """
    with django_db_blocker.unblock():
        # Run migrations to create all tables
        call_command('migrate', '--noinput', verbosity=1)
