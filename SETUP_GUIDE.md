# 🚀 راهنمای راه‌اندازی پروژه - Team Task Board

## 📌 فهرست مطالب

1. [پیش‌نیازها](#پیش-نیازها)
2. [راه‌اندازی اولیه](#راه-اندازی-اولیه)
3. [نصب Pre-commit Hooks](#نصب-pre-commit-hooks)
4. [محیط‌های مختلف اجرایی](#محیط-های-مختلف-اجرایی)
5. [اجرای تست‌ها](#اجرای-تست-ها)
6. [بررسی‌های امنیتی](#بررسی-های-امنیتی)
7. [دستورات مفید](#دستورات-مفید)
8. [عیب‌یابی](#عیب-یابی)

---

## پیش نیازها

### نرم‌افزارهای مورد نیاز:

```bash
# Git
git --version  # >= 2.25

# Docker & Docker Compose
docker --version  # >= 20.10
docker-compose --version  # >= 1.29

# Python (برای pre-commit)
python3 --version  # >= 3.11

# Node.js (برای frontend)
node --version  # >= 18.0
npm --version  # >= 9.0
```

---

## راه‌اندازی اولیه

### 1️⃣ کلون کردن پروژه

```bash
# کلون repository
git clone https://github.com/mhmdrz22/enginner.git
cd enginner
```

### 2️⃣ نصب ابزارهای امنیتی و Pre-commit

```bash
# نصب Pre-commit و ابزارهای امنیتی
pip install pre-commit detect-secrets bandit safety pip-audit

# یا استفاده از Makefile
make install
```

### 3️⃣ نصب Pre-commit Hooks

```bash
# نصب hooks
pre-commit install

# نصب hook برای commit messages
pre-commit install --hook-type commit-msg

# ایجاد baseline برای detect-secrets
detect-secrets scan > .secrets.baseline

# یا استفاده از Makefile
make pre-commit-install
```

### 4️⃣ بررسی Pre-commit

```bash
# اجرای manual روی تمام فایل‌ها
pre-commit run --all-files

# یا
make pre-commit-run
```

---

## نصب Pre-commit Hooks

### 🔒 اهمیت Pre-commit

Pre-commit hooks قبل از هر commit اجرا می‌شوند و موارد زیر را چک می‌کنند:

- ✅ **کیفیت کد**: Black, Flake8, isort برای Python
- ✅ **کیفیت کد**: ESLint, Prettier برای JavaScript
- ✅ **امنیت**: Bandit برای Python security issues
- ✅ **Secret Detection**: جلوگیری از commit کردن passwords, API keys
- ✅ **Dockerfile Linting**: Hadolint
- ✅ **YAML/JSON Validation**
- ✅ **جلوگیری از commit به main branch**

### دستورات مفید:

```bash
# اجرا روی فایل‌های تغییر یافته
pre-commit run

# اجرا روی تمام فایل‌ها
pre-commit run --all-files

# اجرا روی فایل خاص
pre-commit run --files path/to/file.py

# بروزرسانی hooks
pre-commit autoupdate

# Skip کردن موقت (فقط در موارد اضطراری)
git commit --no-verify -m "message"
```

---

## محیط های مختلف اجرایی

### 🔧 محیط Development (Local)

```bash
# کپی کردن .env.example
cp .env.example .env.local

# ویرایش .env.local با مقادیر development
nano .env.local

# اجرا با docker-compose
docker-compose up --build

# یا استفاده از Makefile
make dev
```

**توجه**: در محیط development:
- `DEBUG=True`
- Secrets می‌توانند ساده باشند
- ALLOWED_HOSTS شامل localhost

### 🧪 محیط Test

```bash
# اجرای تست‌ها
make test

# یا مستقیم
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
```

**ویژگی‌های محیط تست**:
- استفاده از tmpfs برای database (سرعت بالا)
- Database جداگانه
- Celery در حالت EAGER

### 🚀 محیط Production

```bash
# ⚠️ قبل از production حتما این چک‌لیست را مرور کنید
cat SECURITY.md

# بررسی آمادگی
make prod-check

# Build
make prod-build

# اجرا (فقط بعد از اطمینان کامل)
make prod-up
```

**⚠️ نکات بحرانی Production**:

```bash
# ایجاد .env.production (نباید در git باشد)
cp .env.example .env.production

# ویرایش و تنظیم مقادیر production
nano .env.production
```

**موارد الزامی در `.env.production`**:
```bash
DEBUG=False
SECRET_KEY=<generate-new-50-chars-random-string>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
POSTGRES_PASSWORD=<strong-16-char-password>
REDIS_PASSWORD=<strong-16-char-password>
```

**تولید SECRET_KEY جدید**:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## اجرای تست ها

### Backend Tests

```bash
# اجرای تمام تست‌ها
make test-backend

# با coverage
make test-coverage

# اجرای تست خاص
cd backend
pytest path/to/test_file.py::test_function

# Watch mode برای TDD
make test-watch
```

### Frontend Tests

```bash
# اجرای تست‌های frontend
make test-frontend

# یا مستقیم
cd frontend
npm test

# با coverage
npm run test:coverage
```

### Coverage Report

```bash
# تولید coverage report
make test-coverage

# مشاهده report در مرورگر
open backend/htmlcov/index.html
```

**هدف Coverage**: حداقل ۸۵٪

---

## بررسی های امنیتی

### 🛡️ Security Scanning Tools

#### 1. Bandit (Python Security)

```bash
# اجرای Bandit
make bandit

# یا مستقیم
bandit -r backend/ -ll

# با فرمت JSON
bandit -r backend/ -ll -f json -o bandit-report.json
```

#### 2. Safety (Python Dependencies)

```bash
# بررسی vulnerabilities
make safety

# یا مستقیم
safety check --file backend/requirements.txt
```

#### 3. Pip-audit

```bash
# بررسی با pip-audit
cd backend
pip-audit
```

#### 4. NPM Audit (Frontend)

```bash
# بررسی npm packages
make npm-audit

# تلاش برای fix خودکار
make npm-audit-fix
```

#### 5. Trivy (Docker Images)

```bash
# نصب Trivy
# macOS
brew install trivy

# Ubuntu/Debian
sudo apt-get install trivy

# اجرای scan
make security-scan-docker

# یا مستقیم
trivy image enginner-backend:latest
trivy image enginner-frontend:latest
```

#### 6. Secret Detection

```bash
# اجرای detect-secrets
detect-secrets scan --baseline .secrets.baseline

# بررسی فایل جدید
detect-secrets scan new_file.py

# آپدیت baseline
detect-secrets scan > .secrets.baseline
```

### 📋 Security Checklist روزانه

```bash
# اجرای تمام بررسی‌های امنیتی
make security-check

# شامل:
# - Bandit
# - Safety
# - npm audit
# - Secret detection
```

### 🔍 Security Audit کامل

```bash
# اجرای full security audit
make security-full

# شامل:
# - همه چیزهای security-check
# - Docker image scanning
```

---

## دستورات مفید

### Database Management

```bash
# اجرای migrations
make migrate

# ایجاد migration جدید
make makemigrations

# باز کردن database shell
make db-shell

# ایجاد superuser
make createsuperuser

# Backup گرفتن
make backup-db

# Restore کردن
make restore-db FILE=backups/backup_20240102.sql
```

### Docker Management

```bash
# مشاهده وضعیت containers
make ps

# مشاهده logs
make logs

# باز کردن shell در backend
make shell-backend

# باز کردن Django shell
make django-shell

# پاک کردن همه چیز
make clean
```

### Code Quality

```bash
# فرمت کردن کد Python
make format-backend

# فرمت کردن کد JavaScript
make format-frontend

# Lint کردن
make lint-backend
make lint-frontend
```

---

## عیب یابی

### مشکل 1: Pre-commit hook fail می‌شود

```bash
# بررسی error message دقیق
pre-commit run --all-files --verbose

# اجرای fix خودکار (اگر ممکن باشد)
black backend/
isort backend/
prettier --write frontend/

# Skip موقت (فقط در موارد ضروری)
git commit --no-verify -m "message"
```

### مشکل 2: Docker build fail می‌شود

```bash
# پاک کردن cache
docker system prune -a

# Build بدون cache
docker-compose build --no-cache

# بررسی logs
docker-compose logs
```

### مشکل 3: Database connection error

```bash
# بررسی وضعیت database
docker-compose ps

# Restart کردن database
docker-compose restart db

# بررسی logs
docker-compose logs db

# پاک کردن و شروع مجدد
docker-compose down -v
docker-compose up -d
```

### مشکل 4: Port already in use

```bash
# پیدا کردن process که port را اشغال کرده
lsof -i :8000  # backend
lsof -i :3000  # frontend
lsof -i :5432  # postgres

# Kill کردن process
kill -9 <PID>

# یا تغییر port در docker-compose.yml
```

### مشکل 5: Permission denied

```bash
# اضافه کردن user به docker group
sudo usermod -aG docker $USER

# Logout/Login مجدد
newgrp docker

# یا اجرا با sudo (not recommended)
sudo docker-compose up
```

---

## 📚 منابع بیشتر

- [SECURITY.md](./SECURITY.md) - چک‌لیست کامل امنیتی
- [DOCKER_SETUP.md](./DOCKER_SETUP.md) - راهنمای Docker
- [DEPLOYMENT.md](./DEPLOYMENT.md) - راهنمای Deploy
- [.pre-commit-config.yaml](./.pre-commit-config.yaml) - کانفیگ Pre-commit

---

## 🆘 دریافت کمک

### مشکل در Pre-commit؟

```bash
# بررسی version ها
pre-commit --version
python --version

# نصب مجدد
pip uninstall pre-commit
pip install pre-commit
pre-commit clean
pre-commit install
```

### مشکل در Docker؟

```bash
# بررسی Docker
docker info
docker-compose version

# پاک کردن کامل
docker system prune -a --volumes
```

---

## ⚡ Quick Start Commands

```bash
# راه‌اندازی سریع برای شروع کار
git clone https://github.com/mhmdrz22/enginner.git
cd enginner
make setup                # نصب همه چیز
make dev                  # شروع development

# در terminal دیگر
make test                 # اجرای تست‌ها
make security-check       # بررسی امنیتی
```

---

## 📝 Next Steps

1. ✅ راه‌اندازی محیط development
2. ✅ نصب pre-commit hooks
3. ✅ اجرای تست‌ها
4. ✅ بررسی امنیتی
5. ⏳ نوشتن feature جدید
6. ⏳ Code review
7. ⏳ Merge به main
8. ⏳ Deploy به production (بعد از تکمیل SECURITY.md checklist)

---

**آخرین بروزرسانی**: 2026-01-02
**نسخه**: 1.0.0
