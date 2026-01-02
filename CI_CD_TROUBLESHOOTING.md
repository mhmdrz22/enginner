# CI/CD Troubleshooting Guide

## مشکلات رایج و راه حل‌ها

### ✅ تغییرات انجام شده

#### 1. مشکل Database Connection
**مشکل**: `could not translate host name "db" to address`

**راه حل**: استفاده از `DATABASE_URL` به جای متغیرهای جداگانه
```yaml
env:
  DATABASE_URL: postgresql://test_user:test_password@localhost:5432/test_db
```

#### 2. Pre-commit Warnings
**مشکل**: `deprecated stage names (commit)`

**راه حل**: اضافه کردن `stages: [pre-commit]` به تمام hooks

#### 3. ESLint & Prettier در CI
**مشکل**: نصب dependencies سنگین در CI طول می‌کشد

**راه حل**: Skip کردن این checks در CI
```bash
SKIP=hadolint-docker,eslint,prettier pre-commit run --all-files
```

---

## بررسی وضعیت Pipeline

### چک کردن GitHub Actions

1. برو به repository خودت
2. کلیک روی تب "Actions"
3. آخرین workflow run را بررسی کن

### مشاهده Logs

```bash
# در صورت fail شدن، روی job کلیک کن و logs را بخوان
```

---

## اجرای Local برای Debug

### Pre-commit Local

```bash
# نصب
pip install pre-commit
pre-commit install

# اجرا روی تمام فایل‌ها
pre-commit run --all-files

# اجرا روی فایل‌های تغییر یافته
pre-commit run

# Skip کردن checks خاص
SKIP=eslint,prettier pre-commit run --all-files
```

### Tests Local با Docker

```bash
# اجرای محیط test
docker-compose -f docker-compose.test.yml up --build

# مشاهده logs
docker-compose -f docker-compose.test.yml logs -f

# پاک کردن
docker-compose -f docker-compose.test.yml down
```

### Tests Local بدون Docker

```bash
# Backend
cd backend
pip install -r requirements.txt
python manage.py test

# با coverage
pytest --cov=. --cov-report=html

# Frontend
cd frontend
npm install
npm test
```

---

## مشکلات رایج

### 1. Pre-commit Fail می‌شود

**علت**: کد format نیست یا مشکل lint دارد

**راه حل**:
```bash
# Format کردن خودکار
cd backend
black .
isort .

cd ../frontend
npm run format

# دوباره امتحان کن
pre-commit run --all-files
```

### 2. Backend Tests Fail می‌شوند

**علت**: Database connection یا migration issue

**راه حل**:
```bash
# بررسی که PostgreSQL در حال اجرا است
docker-compose ps

# اجرای migrations
docker-compose exec backend python manage.py migrate

# اجرای tests
docker-compose exec backend python manage.py test
```

### 3. Frontend Build Fail می‌شود

**علت**: Dependency issues یا syntax errors

**راه حل**:
```bash
cd frontend

# پاک کردن node_modules
rm -rf node_modules package-lock.json

# نصب مجدد
npm install

# Build
npm run build
```

### 4. Docker Build Fail می‌شود

**علت**: Cache issues یا Dockerfile problems

**راه حل**:
```bash
# پاک کردن cache
docker system prune -a

# Build بدون cache
docker-compose build --no-cache
```

---

## Environment Variables در CI

### Backend Tests
```yaml
env:
  DATABASE_URL: postgresql://test_user:test_password@localhost:5432/test_db
  SECRET_KEY: test-secret-key
  DEBUG: "False"
  ALLOWED_HOSTS: localhost,127.0.0.1
  CELERY_BROKER_URL: redis://localhost:6379/0
  CELERY_TASK_ALWAYS_EAGER: "True"
```

### مهم
- ✅ از `DATABASE_URL` استفاده کن
- ✅ `DEBUG` باید string باشد: `"False"`
- ✅ `CELERY_TASK_ALWAYS_EAGER` برای tests: `"True"`
- ✅ SECRET_KEY می‌تواند test value باشد

---

## Coverage Requirements

### Backend
- **Target**: ≥85%
- **Command**: `pytest --cov=. --cov-fail-under=85`

### Frontend  
- **Target**: ≥80%
- **Command**: `npm run test:coverage`

---

## Security Scanning

### Bandit (Python)
```bash
cd backend
bandit -r . -ll
```

### Safety (Dependencies)
```bash
cd backend
safety check --file requirements.txt
```

### Trivy (Docker)
```bash
trivy image enginner-backend:latest
trivy image enginner-frontend:latest
```

---

## Debug Tips

### 1. بررسی Services
```bash
# وضعیت services
docker-compose ps

# Logs
docker-compose logs -f [service-name]

# Shell
docker-compose exec [service-name] /bin/bash
```

### 2. بررسی Database
```bash
# اتصال به PostgreSQL
docker-compose exec db psql -U test_user -d test_db

# لیست tables
\dt

# بررسی migrations
SELECT * FROM django_migrations;
```

### 3. بررسی Logs
```bash
# Backend logs
docker-compose logs -f backend

# Database logs
docker-compose logs -f db

# تمام logs
docker-compose logs -f
```

---

## Workflow Structure

```
CI/CD Pipeline
├── Pre-commit Checks (skip heavy tools)
├── Security Scanning
│   ├── Trivy (filesystem)
│   ├── Bandit (Python)
│   ├── Safety (dependencies)
│   └── Trufflehog (secrets)
├── Backend Tests
│   ├── PostgreSQL service
│   ├── Redis service
│   ├── Run migrations
│   ├── Run tests
│   └── Upload coverage
├── Frontend Tests
│   ├── Install dependencies
│   ├── Lint
│   ├── Test
│   └── Build
├── Docker Security Scan
│   ├── Build images
│   └── Scan with Trivy
└── Docker Build & Push (main branch only)
```

---

## Quick Commands

```bash
# Full local test suite
make test

# Pre-commit only
make pre-commit-run

# Security checks
make security-check

# Build everything
make build

# Clean everything
make clean
```

---

## منابع بیشتر

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Pre-commit Docs](https://pre-commit.com/)
- [Docker Compose Docs](https://docs.docker.com/compose/)
- [Django Testing](https://docs.djangoproject.com/en/stable/topics/testing/)
- [pytest Docs](https://docs.pytest.org/)

---

## دریافت کمک

اگر مشکلی حل نشد:

1. Logs را به دقت بخوان
2. Error message را Google کن
3. در GitHub Issues جستجو کن
4. Issue جدید باز کن با logs کامل

---

**آخرین بروزرسانی**: 2026-01-02
