# 🧪 راهنمای کامل تست‌ها

## فهرست مطالب

- [نصب Dependencies](#نصب-dependencies)
- [اجرای تست‌ها](#اجرای-تست‌ها)
- [انواع تست‌ها](#انواع-تست‌ها)
- [Coverage Report](#coverage-report)
- [نوشتن تست جدید](#نوشتن-تست-جدید)
- [Best Practices](#best-practices)

---

## 📦 نصب Dependencies

```bash
cd backend

# نصب dependencies تست
pip install -r requirements-dev.txt

# یا فقط موارد ضروری
pip install pytest pytest-django pytest-cov
```

---

## 🚀 اجرای تست‌ها

### روش 1: Django Test Runner (پیشفرض)

```bash
# اجرای تمام تست‌ها
python manage.py test

# اجرای تست‌های یک app
python manage.py test accounts
python manage.py test tasks

# اجرای یک فایل تست خاص
python manage.py test accounts.tests.test_models

# اجرای یک تست خاص
python manage.py test accounts.tests.test_models.UserModelTests.test_create_user_with_email

# با verbosity بیشتر
python manage.py test --verbosity=2

# حفظ دیتابیس بعد از تست (سریع‌تر)
python manage.py test --keepdb
```

### روش 2: Pytest (پیشنهادی)

```bash
# اجرای تمام تست‌ها
pytest

# با coverage
pytest --cov

# اجرای تست‌های یک app
pytest accounts/tests/
pytest tasks/tests/

# اجرای یک فایل تست
pytest accounts/tests/test_models.py

# اجرای تست‌های با marker خاص
pytest -m auth
pytest -m integration
pytest -m "not slow"

# اجرا با verbose
pytest -v

# اجرای موازی (سریع‌تر)
pytest -n auto

# با HTML coverage report
pytest --cov --cov-report=html
```

### روش 3: Make Commands

```bash
# اجرای همه تست‌ها
make test

# فقط backend
make test-backend

# با coverage
make test-coverage
```

---

## 📊 انواع تست‌ها

### 1️⃣ Unit Tests (تست واحد)

**محل:** `accounts/tests/test_models.py`, `tasks/tests/test_models.py`

**هدف:** تست تک‌تک متدها و کلاس‌ها به صورت مجزا

```bash
# اجرای unit tests
pytest accounts/tests/test_models.py
pytest tasks/tests/test_models.py
```

**مثال‌های تست:**
- ✅ ساخت user با email
- ✅ validation فیلدها
- ✅ روابط بین مدل‌ها
- ✅ متدهای مدل

### 2️⃣ Integration Tests (تست یکپارچگی)

**محل:** `tests/test_integration.py`

**هدف:** تست کل flow از ابتدا تا انتها

```bash
# اجرای integration tests
pytest tests/test_integration.py -m integration
```

**مثال‌های تست:**
- ✅ Register → Login → Create Task → Update → Delete
- ✅ User isolation (کاربران نباید task هم رو ببینن)
- ✅ Complete task lifecycle

### 3️⃣ API Tests (تست API)

**محل:** `accounts/tests/test_views.py`, `tasks/tests/test_views.py`

**هدف:** تست endpoint‌های REST API

```bash
# اجرای API tests
pytest -m api
```

**مثال‌های تست:**
- ✅ Authentication endpoints
- ✅ CRUD operations
- ✅ Permissions و Authorization
- ✅ Error handling
- ✅ Status codes

### 4️⃣ Performance Tests (تست کارایی)

**محل:** `tests/test_performance.py`

**هدف:** بررسی performance و scalability

```bash
# اجرای performance tests
pytest tests/test_performance.py -m performance
```

**مثال‌های تست:**
- ✅ Bulk operations speed
- ✅ Query performance
- ✅ N+1 query problem
- ✅ Concurrent access

### 5️⃣ Authentication Tests

**محل:** `accounts/tests/test_authentication.py`

**هدف:** تست سیستم احراز هویت

```bash
pytest accounts/tests/test_authentication.py -m auth
```

**مثال‌های تست:**
- ✅ Email authentication
- ✅ Token generation
- ✅ Inactive user handling

---

## 📈 Coverage Report

### دریافت Coverage

```bash
# Coverage با Django
python manage.py test --with-coverage

# Coverage با pytest
pytest --cov=. --cov-report=html

# یا با make
make test-coverage
```

### مشاهده Report

```bash
# Terminal output
pytest --cov=. --cov-report=term-missing

# HTML Report (بهترین)
pytest --cov=. --cov-report=html
open htmlcov/index.html
```

### Coverage Thresholds

```bash
# فقط pass میشه اگر coverage >= 80%
pytest --cov=. --cov-fail-under=80
```

**هدف Coverage:**
- ✅ **Overall:** 80%+
- ✅ **Models:** 90%+
- ✅ **Views/APIs:** 85%+
- ✅ **Serializers:** 85%+

---

## ✍️ نوشتن تست جدید

### ساختار تست

```python
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class MyModelTests(TestCase):
    """Test suite for MyModel."""

    def setUp(self):
        """Setup test data before each test."""
        self.user = User.objects.create_user(
            email='test@example.com',
            password='pass123'
        )

    def test_something(self):
        """Test description."""
        # Arrange (آماده‌سازی)
        data = {'key': 'value'}
        
        # Act (اجرا)
        result = some_function(data)
        
        # Assert (بررسی)
        self.assertEqual(result, expected_value)

    def tearDown(self):
        """Cleanup after each test (اختیاری)."""
        pass
```

### با Pytest

```python
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_user_creation(user):
    """Test user creation with fixture."""
    assert user.email == 'testuser@example.com'
    assert user.is_active

@pytest.mark.django_db
class TestMyFeature:
    """Group related tests."""
    
    def test_feature_1(self, user):
        assert user.is_active
    
    def test_feature_2(self, user, task):
        assert task.user == user
```

### استفاده از Fixtures

**Fixtures موجود در `conftest.py`:**

```python
# استفاده
def test_with_fixtures(user, task, authenticated_client):
    # user: یک کاربر تست
    # task: یک task نمونه
    # authenticated_client: client با authentication
    
    response = authenticated_client.get('/api/tasks/')
    assert response.status_code == 200
```

---

## 🎯 Best Practices

### ✅ DO (انجام بده)

1. **نام‌گذاری واضح:**
```python
def test_user_can_create_task_with_valid_data():  # ✅ خوب
    pass

def test_task():  # ❌ بد
    pass
```

2. **یک هدف در هر تست:**
```python
def test_user_registration_success():
    # فقط تست موفقیت registration
    pass

def test_user_registration_with_duplicate_email():
    # فقط تست duplicate email
    pass
```

3. **استفاده از Fixtures:**
```python
# ✅ خوب - استفاده از fixture
def test_task_creation(user):
    task = Task.objects.create(user=user, title='Test')
    
# ❌ بد - ساخت دستی
def test_task_creation():
    user = User.objects.create_user(email='...', password='...')
    task = Task.objects.create(user=user, title='Test')
```

4. **Arrange-Act-Assert Pattern:**
```python
def test_user_login():
    # Arrange
    user = User.objects.create_user(email='...', password='...')
    
    # Act
    response = self.client.post('/api/login/', data)
    
    # Assert
    self.assertEqual(response.status_code, 200)
```

5. **تست Edge Cases:**
```python
def test_task_with_empty_title():  # Edge case
    pass

def test_task_with_very_long_title():  # Edge case
    pass

def test_task_with_past_due_date():  # Edge case
    pass
```

### ❌ DON'T (انجام نده)

1. **وابستگی به ترتیب اجرا:**
```python
# ❌ بد
class MyTests(TestCase):
    def test_1_create_user(self):
        self.user = User.objects.create(...)
    
    def test_2_use_user(self):
        # وابسته به test_1
        self.user.do_something()
```

2. **تست‌های خیلی بزرگ:**
```python
# ❌ بد - یک تست برای همه چیز
def test_everything():
    # 100 خط تست
    pass

# ✅ خوب - تقسیم به تست‌های کوچک
def test_feature_a():
    pass

def test_feature_b():
    pass
```

3. **استفاده از داده واقعی:**
```python
# ❌ بد
def test_send_email():
    send_email('real@email.com')  # واقعاً ایمیل میفرسته!

# ✅ خوب
from unittest.mock import patch

@patch('myapp.send_email')
def test_send_email(mock_send):
    send_email('test@example.com')
    mock_send.assert_called_once()
```

---

## 🔍 Debug کردن تست‌ها

### با print

```python
def test_something(user):
    print(f"User: {user}")  # Debug
    print(f"Email: {user.email}")  # Debug
    assert user.is_active
```

### با ipdb

```python
import ipdb

def test_something(user):
    ipdb.set_trace()  # Breakpoint
    assert user.is_active
```

### با pytest -s

```bash
# نمایش print ها
pytest -s

# یک تست خاص
pytest accounts/tests/test_models.py::test_create_user -s
```

---

## 📝 Test Coverage در CI/CD

**GitHub Actions** خودکار coverage رو چک می‌کنه:

```yaml
# .github/workflows/ci-cd.yml
- name: Run tests with coverage
  run: |
    cd backend
    coverage run --source='.' manage.py test
    coverage report
    coverage xml
```

---

## 🎓 مثال‌های عملی

### مثال 1: تست Model

```python
def test_task_creation(user):
    """Test creating a task."""
    task = Task.objects.create(
        user=user,
        title='My Task',
        status='TODO'
    )
    
    assert task.user == user
    assert task.title == 'My Task'
    assert task.status == 'TODO'
    assert Task.objects.count() == 1
```

### مثال 2: تست API

```python
def test_create_task_api(authenticated_client):
    """Test creating task via API."""
    url = '/api/tasks/'
    data = {
        'title': 'API Task',
        'status': 'TODO'
    }
    
    response = authenticated_client.post(url, data, format='json')
    
    assert response.status_code == 201
    assert response.data['title'] == 'API Task'
    assert Task.objects.count() == 1
```

### مثال 3: تست Permissions

```python
def test_user_cannot_access_other_user_task(user, another_user, api_client):
    """Test user isolation."""
    # User 1 creates task
    task = Task.objects.create(user=another_user, title='Secret')
    
    # User 2 tries to access
    api_client.force_authenticate(user=user)
    url = f'/api/tasks/{task.id}/'
    response = api_client.get(url)
    
    assert response.status_code == 404
```

---

## 📞 پشتیبانی

مشکل در تست‌ها؟
- 📧 ایمیل: dev@taskboard.com
- 💬 Issue در GitHub
- 📖 [Django Testing Docs](https://docs.djangoproject.com/en/4.2/topics/testing/)
- 📖 [Pytest Docs](https://docs.pytest.org/)

---

**موفق باشید! 🚀**
