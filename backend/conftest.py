"""Pytest configuration for Django tests."""

import pytest
from django.conf import settings
from django.core.management import call_command


@pytest.fixture(scope='session')
def django_db_setup():
    """Set up the test database."""
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Enable database access for all tests."""
    pass


@pytest.fixture(autouse=True)
def reset_sequences(django_db_blocker):
    """Reset database sequences after each test."""
    def reset():
        with django_db_blocker.unblock():
            from django.db import connection
            if connection.vendor == 'postgresql':
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT setval(pg_get_serial_sequence('\"accounts_user\"', 'id'), 1, false);"
                    )
    
    yield
    reset()
