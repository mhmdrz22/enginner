# Testing Guide

This guide explains how to run tests and understand the testing infrastructure of this Django project.

## Quick Start

```bash
# Run all tests
cd backend
python manage.py test

# Run with verbose output
python manage.py test --verbosity=2

# Run specific app tests
python manage.py test accounts
python manage.py test tasks

# Run specific test file
python manage.py test accounts.tests.test_models

# Run specific test class
python manage.py test accounts.tests.test_models.UserModelTests

# Run specific test method
python manage.py test accounts.tests.test_models.UserModelTests.test_create_user_with_email
```

## Test Structure

### Directory Layout

```
backend/
├── accounts/
│   └── tests/
│       ├── __init__.py
│       ├── test_models.py
│       ├── test_views.py
│       ├── test_serializers.py
│       └── test_authentication.py
├── tasks/
│   └── tests/
│       ├── __init__.py
│       ├── test_models.py
│       └── test_views.py
└── tests/
    ├── __init__.py
    ├── test_integration.py
    └── test_performance.py
```

## Test Types

### 1. Unit Tests
Test individual components in isolation.

**Example: `accounts/tests/test_models.py`**
```python
class UserModelTests(TestCase):
    def test_create_user_with_email(self):
        user = User.objects.create_user(
            email='test@example.com',
            password='pass123'
        )
        self.assertTrue(user.is_active)
```

### 2. API Tests
Test REST API endpoints.

**Example: `tasks/tests/test_views.py`**
```python
class TaskAPITests(TestCase):
    def test_create_task_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
```

### 3. Integration Tests
Test complete user workflows.

**Example: `tests/test_integration.py`**
```python
class UserTaskFlowIntegrationTests(TestCase):
    def test_complete_user_journey(self):
        # Register -> Login -> Create Task -> Complete Task
        ...
```

### 4. Performance Tests
Test system performance and scalability.

**Example: `tests/test_performance.py`**
```python
class PerformanceTests(TestCase):
    def test_bulk_task_creation_performance(self):
        start_time = time.time()
        # Create 100 tasks
        duration = time.time() - start_time
        self.assertLess(duration, 1.0)
```

## Test Isolation Strategy

### Problem: Test Interference
Tests were failing due to:
- Shared database state between tests
- User ID conflicts
- Email/username duplicates

### Solution: UUID-Based Isolation

**Before (❌ Bad):**
```python
class MyTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',  # ❌ Conflicts!
            password='pass123'
        )
```

**After (✅ Good):**
```python
import uuid

class MyTests(TestCase):
    def setUp(self):
        User.objects.all().delete()  # Clean state
        unique_id = uuid.uuid4().hex[:8]
        self.user = User.objects.create_user(
            email=f'test_{unique_id}@example.com',  # ✅ Unique!
            password='pass123'
        )
    
    def tearDown(self):
        User.objects.all().delete()  # Cleanup
```

## Best Practices

### 1. Always Use TestCase (Not TransactionTestCase)

✅ **DO:**
```python
from django.test import TestCase

class MyTests(TestCase):  # Automatic rollback
    ...
```

❌ **DON'T:**
```python
from django.test import TransactionTestCase

class MyTests(TransactionTestCase):  # Slow, manual cleanup
    ...
```

### 2. Clean Database in setUp/tearDown

```python
def setUp(self):
    """Clean database before test."""
    Task.objects.all().delete()
    User.objects.all().delete()

def tearDown(self):
    """Clean database after test."""
    Task.objects.all().delete()
    User.objects.all().delete()
```

### 3. Use UUID for Unique Data

```python
import uuid

unique_id = uuid.uuid4().hex[:8]  # e.g., 'a1b2c3d4'
email = f'user_{unique_id}@example.com'
username = f'user_{unique_id}'
```

### 4. Test Both Success and Failure Cases

```python
def test_login_success(self):
    """Test successful login."""
    response = self.client.post(url, valid_data)
    self.assertEqual(response.status_code, 200)

def test_login_invalid_credentials(self):
    """Test login fails with wrong password."""
    response = self.client.post(url, invalid_data)
    self.assertEqual(response.status_code, 400)
```

### 5. Use Descriptive Test Names

✅ **Good:**
```python
def test_user_cannot_delete_other_user_task(self):
    ...
```

❌ **Bad:**
```python
def test_delete(self):
    ...
```

## Coverage

### Generate Coverage Report

```bash
# Install coverage
pip install coverage

# Run tests with coverage
coverage run --source='.' manage.py test

# View report in terminal
coverage report

# Generate HTML report
coverage html
open htmlcov/index.html
```

### Target Coverage
- **Minimum:** 80%
- **Target:** 90%+
- **Critical paths:** 100%

## Debugging Failed Tests

### 1. Run with Verbose Output

```bash
python manage.py test --verbosity=2
```

### 2. Run Specific Failing Test

```bash
python manage.py test accounts.tests.test_models.UserModelTests.test_create_user_with_email
```

### 3. Use PDB for Debugging

```python
def test_something(self):
    import pdb; pdb.set_trace()  # Breakpoint
    user = User.objects.create_user(...)
    ...
```

### 4. Print Database State

```python
def test_something(self):
    print(f"Users: {User.objects.count()}")
    print(f"Tasks: {Task.objects.count()}")
    ...
```

## CI/CD Integration

Tests run automatically on GitHub Actions:

```yaml
- name: Run tests
  run: |
    cd backend
    python manage.py test --verbosity=2
```

### Pre-Commit Hook

Run tests before committing:

```bash
# .git/hooks/pre-commit
#!/bin/bash
cd backend
python manage.py test
if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi
```

## Performance Benchmarks

| Metric | Value |
|--------|-------|
| Total Test Count | ~50 tests |
| Execution Time | ~12 seconds |
| Average per Test | ~0.24 seconds |
| Coverage | 85%+ |

## Common Issues & Solutions

### Issue: IntegrityError - duplicate key

**Cause:** Tests using same email/username

**Solution:** Use UUID for unique values

```python
unique_id = uuid.uuid4().hex[:8]
email = f'test_{unique_id}@example.com'
```

### Issue: Tests pass individually but fail together

**Cause:** Test isolation problems

**Solution:** Add setUp/tearDown cleanup

```python
def setUp(self):
    User.objects.all().delete()

def tearDown(self):
    User.objects.all().delete()
```

### Issue: Slow test execution

**Cause:** Using TransactionTestCase

**Solution:** Switch to TestCase

```python
from django.test import TestCase  # Fast!
```

### Issue: Random test failures

**Cause:** Race conditions or shared state

**Solution:** Ensure complete isolation with UUID

## Testing Checklist

Before pushing code:

- [ ] All tests pass locally
- [ ] New features have tests
- [ ] Tests use UUID for isolation
- [ ] Coverage is maintained/improved
- [ ] No TransactionTestCase used
- [ ] setUp/tearDown properly clean database

## Resources

- [Django Testing Documentation](https://docs.djangoproject.com/en/4.2/topics/testing/)
- [Django REST Framework Testing](https://www.django-rest-framework.org/api-guide/testing/)
- [Python unittest Documentation](https://docs.python.org/3/library/unittest.html)

## Getting Help

If tests are failing:

1. Check error message carefully
2. Run specific failing test with verbosity
3. Check database state in setUp/tearDown
4. Verify UUID is being used for unique data
5. Check CI/CD logs on GitHub Actions

---

**Last Updated:** January 2026
