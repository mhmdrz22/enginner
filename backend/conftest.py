"""Pytest configuration for Django tests.

Ensures database migrations are run before tests.
"""
import pytest
from django.core.management import call_command


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    """Run migrations before tests.
    
    This ensures all database tables are created properly.
    """
    with django_db_blocker.unblock():
        call_command('migrate', '--noinput', verbosity=0)
