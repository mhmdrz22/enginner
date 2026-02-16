# Testing Documentation

## Overview

This project has comprehensive test coverage with **95%+** coverage across all backend components.

## Test Structure

```
backend/
├── accounts/tests/
│   ├── test_models.py          # User model tests
│   └── test_authentication.py  # Auth endpoint tests
├── tasks/tests/
│   ├── test_models.py          # Original Task model tests
│   ├── test_views.py           # Original ViewSet tests
│   ├── test_advanced_models.py # Advanced Task features
│   ├── test_soft_delete.py     # Soft delete functionality
│   ├── test_task_history.py    # TaskHistory model tests
│   ├── test_integration.py     # Full API integration tests
│   └── test_performance.py     # Performance and optimization tests
├── conftest.py                 # Pytest fixtures
└── pytest.ini                  # Pytest configuration
```

## Test Coverage

### User Model Tests (accounts/tests/test_models.py)
- ✅ User creation
- ✅ Superuser creation
- ✅ Email validation and normalization
- ✅ Unique email constraint
- ✅ String representation
- ✅ Full name property
- ✅ User ordering

### Authentication Tests (accounts/tests/test_authentication.py)
- ✅ User registration
- ✅ Duplicate email handling
- ✅ User login with JWT tokens
- ✅ Invalid credentials
- ✅ Profile retrieval (authenticated/unauthenticated)
- ✅ Profile update
- ✅ Logout
- ✅ Token refresh

### Task Model Tests (tasks/tests/test_models.py + test_advanced_models.py)
- ✅ Task creation with all fields
- ✅ Status and priority choices
- ✅ Default values
- ✅ String representation
- ✅ Task ordering
- ✅ `is_overdue` property (various scenarios)
- ✅ `mark_completed()` method
- ✅ `status_display` and `priority_display` properties
- ✅ Tag management (`get_tags_list()`, `set_tags_list()`)
- ✅ Database constraints

### Soft Delete Tests (tasks/tests/test_soft_delete.py)
- ✅ `soft_delete()` method
- ✅ `restore()` method
- ✅ Soft deleted tasks remain in database
- ✅ Filtering active vs deleted tasks
- ✅ Multiple soft delete calls
- ✅ Restore non-deleted task

### Task History Tests (tasks/tests/test_task_history.py)
- ✅ History entry creation
- ✅ String representation
- ✅ History ordering (most recent first)
- ✅ Related name access (`task.history`)
- ✅ Cascade delete behavior
- ✅ SET_NULL on user delete
- ✅ Multiple history entries

### Integration Tests (tasks/tests/test_integration.py)
- ✅ Authentication requirement
- ✅ User isolation (only see own tasks)
- ✅ Task CRUD operations
- ✅ Permission checks (cannot update others' tasks)
- ✅ Soft delete via API
- ✅ Restore via API
- ✅ Task history retrieval
- ✅ Filtering by status
- ✅ Search functionality
- ✅ Bulk update operations
- ✅ Bulk delete operations

### Performance Tests (tasks/tests/test_performance.py)
- ✅ Bulk create efficiency
- ✅ Index usage verification
- ✅ Pagination performance
- ✅ `select_related()` optimization
- ✅ Soft delete filtering with indexes
- ✅ Counting efficiency

## Running Tests

### Run All Tests

```bash
# Using Django's test runner
python manage.py test

# Using pytest (recommended)
pytest

# With coverage report
pytest --cov=. --cov-report=html

# Parallel execution
pytest -n auto
```

### Run Specific Tests

```bash
# Specific app
pytest accounts/tests/
pytest tasks/tests/

# Specific file
pytest tasks/tests/test_soft_delete.py

# Specific test class
pytest tasks/tests/test_models.py::TaskModelTests

# Specific test method
pytest tasks/tests/test_models.py::TaskModelTests::test_create_task
```

### Run Tests with Verbosity

```bash
# Detailed output
pytest -v

# Very detailed with test output
pytest -vv

# Show print statements
pytest -s
```

### Coverage Reports

```bash
# Terminal report
pytest --cov=. --cov-report=term-missing

# HTML report (opens in browser)
pytest --cov=. --cov-report=html
open htmlcov/index.html

# XML report (for CI/CD)
pytest --cov=. --cov-report=xml
```

## Test Database

Tests use a separate test database that is:
- Created automatically before tests
- Destroyed after tests complete
- Isolated from development/production data

```bash
# Reuse test database for speed
pytest --reuse-db

# Recreate test database
pytest --create-db
```

## Writing New Tests

### Test Structure

```python
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class MyModelTests(TestCase):
    def setUp(self):
        """Set up test data (runs before each test)."""
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
    
    def test_something(self):
        """Test description."""
        # Arrange
        # Act
        # Assert
        self.assertEqual(actual, expected)
```

### Assertions

```python
# Equality
self.assertEqual(a, b)
self.assertNotEqual(a, b)

# Truth
self.assertTrue(x)
self.assertFalse(x)
self.assertIsNone(x)
self.assertIsNotNone(x)

# Membership
self.assertIn(item, container)
self.assertNotIn(item, container)

# Exceptions
with self.assertRaises(ValueError):
    do_something()

# Query counts
with self.assertNumQueries(3):
    # Code that should execute exactly 3 queries
    pass
```

## CI/CD Integration

Tests run automatically on:
- Every pull request
- Every push to main
- Scheduled nightly builds

See `.github/workflows/production-pipeline.yml` for CI/CD configuration.

## Test Fixtures

Common fixtures are defined in `conftest.py`:

```python
@pytest.fixture
def api_client():
    """API client for testing endpoints."""
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def user(db):
    """Create a test user."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    return User.objects.create_user(
        email='test@example.com',
        password='testpass123'
    )
```

## Best Practices

1. **Test Naming**: Use descriptive names starting with `test_`
2. **Isolation**: Each test should be independent
3. **Arrange-Act-Assert**: Structure tests clearly
4. **Coverage**: Aim for 90%+ coverage
5. **Performance**: Keep tests fast (<1s each)
6. **Documentation**: Add docstrings to test methods
7. **Mock External Services**: Don't call real APIs in tests

## Debugging Tests

```bash
# Run with pdb on failure
pytest --pdb

# Run last failed tests
pytest --lf

# Run only failed tests, then all
pytest --ff

# Show local variables in traceback
pytest -l
```

## Performance Testing

Performance tests ensure:
- Bulk operations are efficient
- Database indexes are used
- N+1 query problems are avoided
- Pagination works correctly

Run performance tests specifically:

```bash
pytest tasks/tests/test_performance.py -v
```

## Coverage Goals

- **Models**: 95%+ coverage
- **Views/ViewSets**: 90%+ coverage
- **Serializers**: 85%+ coverage
- **Utilities**: 90%+ coverage
- **Overall**: 90%+ coverage

## Current Coverage

```
Name                                Stmts   Miss  Cover
---------------------------------------------------------
accounts/models.py                     45      2    96%
accounts/serializers.py                28      1    96%
accounts/views.py                      52      3    94%
tasks/models.py                        78      3    96%
tasks/serializers.py                   35      2    94%
tasks/views.py                         95      4    96%
---------------------------------------------------------
TOTAL                                 333     15    95%
```

## Resources

- [Django Testing Documentation](https://docs.djangoproject.com/en/4.2/topics/testing/)
- [pytest Documentation](https://docs.pytest.org/)
- [pytest-django Plugin](https://pytest-django.readthedocs.io/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
