# 🧪 Testing Guide

## Overview

This project has comprehensive test coverage for both backend and frontend:

- **Backend**: Django/pytest tests with 80%+ coverage target
- **Frontend**: Vitest unit tests + Playwright E2E tests with 85%+ coverage target

---

## 🚀 Quick Start

### Backend Tests (Local)

```bash
cd backend

# Install test dependencies
pip install -r requirements.txt
pip install pytest pytest-django pytest-cov pytest-xdist

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest accounts/tests/test_models.py

# Run in parallel (faster)
pytest -n auto

# Open coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Frontend Tests (Local)

```bash
cd frontend

# Install dependencies
npm install

# Run unit tests
npm run test

# Run with UI
npm run test:ui

# Run with coverage
npm run test:coverage

# Run E2E tests
npm run test:e2e

# Run E2E with UI
npm run test:e2e:ui
```

---

## 🏗️ Test Configuration

### Backend

**Main Files:**
- `backend/pytest.ini` - Pytest configuration
- `backend/conftest.py` - Shared fixtures
- `backend/config/settings/test.py` - Test settings

**Key Settings:**
- Uses **in-memory SQLite** for fast tests (default)
- Can use PostgreSQL with `USE_POSTGRES_FOR_TESTS=true`
- Parallel execution with pytest-xdist
- Coverage threshold: 80%

### Frontend

**Main Files:**
- `frontend/vitest.config.ts` - Vitest configuration
- `frontend/playwright.config.ts` - Playwright configuration
- `frontend/src/tests/setup.ts` - Test setup

**Key Settings:**
- Uses jsdom for DOM simulation
- MSW for API mocking
- Coverage threshold: 85%

---

## 🤖 CI/CD Testing

### Workflows

1. **Backend Tests** (`.github/workflows/backend-tests.yml`)
   - Runs on: Python 3.10, 3.11, 3.12
   - Database: SQLite in-memory
   - Coverage: Uploaded to Codecov

2. **Frontend Tests** (`.github/workflows/frontend-tests.yml`)
   - Runs on: Node 18.x, 20.x, 22.x
   - Unit tests + Build verification
   - E2E tests with Playwright

### Triggers

- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`
- Only when relevant files change

---

## 🔧 Troubleshooting

### Backend Issues

**Problem: Tests fail with database errors**

```bash
# Solution 1: Clear test database
rm -f db.sqlite3
pytest --create-db

# Solution 2: Use fresh migrations
pytest --create-db --migrations
```

**Problem: Tests are slow**

```bash
# Use parallel execution
pytest -n auto

# Use SQLite (faster than PostgreSQL for tests)
# Already configured by default in test.py
```

**Problem: Import errors**

```bash
# Ensure PYTHONPATH is set
export PYTHONPATH="${PWD}/backend:${PYTHONPATH}"

# Or use pytest with proper path
cd backend && pytest
```

### Frontend Issues

**Problem: Tests fail with module not found**

```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

**Problem: Playwright tests fail**

```bash
# Install browsers
npx playwright install

# Install with system dependencies
npx playwright install --with-deps
```

**Problem: Coverage not accurate**

```bash
# Clear coverage cache
rm -rf coverage/ .vitest-cache/
npm run test:coverage
```

---

## 📊 Coverage Requirements

### Backend: 80%+

- **Models**: 90%+
- **Views**: 85%+
- **Serializers**: 85%+
- **Utils/Helpers**: 80%+

### Frontend: 85%+

- **Components**: 85%+
- **Hooks**: 90%+
- **Utils**: 85%+
- **Services**: 80%+

---

## ✅ Best Practices

### Writing Tests

1. **One assertion per test** (when possible)
2. **Use descriptive test names**
3. **Arrange-Act-Assert** pattern
4. **Mock external dependencies**
5. **Test edge cases**

### Example (Backend)

```python
def test_user_creation_with_valid_data(user_factory):
    """Test that user is created successfully with valid data"""
    # Arrange
    email = 'test@example.com'
    
    # Act
    user = user_factory(email=email)
    
    # Assert
    assert user.email == email
    assert user.is_active
```

### Example (Frontend)

```typescript
test('button renders with correct text', () => {
  // Arrange
  const buttonText = 'Click me';
  
  // Act
  render(<Button>{buttonText}</Button>);
  
  // Assert
  expect(screen.getByText(buttonText)).toBeInTheDocument();
});
```

---

## 🚨 Common Errors & Solutions

### Backend

| Error | Solution |
|-------|----------|
| `django.db.utils.OperationalError` | Run migrations: `python manage.py migrate` |
| `ImportError: No module named 'xxx'` | Install: `pip install xxx` |
| `FAILED ... AssertionError` | Check test logic and fixtures |

### Frontend

| Error | Solution |
|-------|----------|
| `Cannot find module` | Run: `npm install` |
| `Test timeout` | Increase timeout in test file |
| `Playwright error` | Run: `npx playwright install` |

---

## 📚 Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Django Testing](https://docs.djangoproject.com/en/stable/topics/testing/)
- [Vitest Documentation](https://vitest.dev/)
- [Playwright Documentation](https://playwright.dev/)
- [Testing Library](https://testing-library.com/)

---

## 🎯 Coverage Reports

View coverage reports:

- **Backend**: `backend/htmlcov/index.html`
- **Frontend**: `frontend/coverage/index.html`
- **Codecov**: Available in PR checks

---

## 🔄 Continuous Integration

All tests must pass before merging:

✅ Backend tests (3 Python versions)
✅ Frontend tests (3 Node versions)
✅ Linting and type checks
✅ Coverage thresholds met
✅ Build successful

---

**Happy Testing! 🎉**
