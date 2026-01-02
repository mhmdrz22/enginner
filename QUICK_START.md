# 🚀 Quick Start Guide

## پیش‌نیازها

قبل از شروع، اطمینان حاصل کنید که موارد زیر نصب هستند:

- ✅ **Docker** & **Docker Compose**
- ✅ **Git**
- ✅ **Make** (اختیاری اما پیشنهادی)

---

## 📦 نصب سریع

### مرحله 1: Clone کردن Repository

```bash
git clone https://github.com/mhmdrz22/enginner.git
cd enginner
```

### مرحله 2: آماده‌سازی Environment Variables

```bash
# کپی فایل نمونه
cp .env.example .env

# ویرایش فایل .env (برای development می‌توان پیش‌فرض بماند)
# nano .env
```

### مرحله 3: اجرای پروژه

#### روش 1: با Makefile (آسان‌تر)

```bash
# نمایش تمام دستورات
make help

# نصب pre-commit hooks
make setup

# اجرای development environment
make dev
```

#### روش 2: با Docker Compose

```bash
# اجرا و build
docker-compose up --build

# اجرا در پس‌زمینه
docker-compose up -d
```

### مرحله 4: ایجاد Superuser

```bash
# با Makefile
make superuser

# یا مستقیم
docker-compose exec backend python manage.py createsuperuser
```

---

## 🎯 دسترسی به سرویس‌ها

بعد از اجرای موفق، می‌توانید به موارد زیر دسترسی داشته باشید:

| سرویس | URL | توضیحات |
|---------|-----|------------|
| **Frontend** | http://localhost:3000 | رابط کاربری React |
| **Backend API** | http://localhost:8000/api/ | Django REST API |
| **Admin Panel** | http://localhost:8000/admin/ | Django Admin |
| **Swagger Docs** | http://localhost:8000/swagger/ | مستندات API |
| **ReDoc** | http://localhost:8000/redoc/ | مستندات API (نسخه 2) |

---

## 🔧 دستورات مفید

### Makefile Commands

```bash
make help              # نمایش تمام دستورات
make setup             # نصب pre-commit hooks
make dev               # اجرای development
make up                # اجرا در پس‌زمینه
make down              # خاموش کردن سرویس‌ها
make logs              # مشاهده logs
make test              # اجرای تست‌ها
make test-coverage     # تست با coverage report
make migrations        # ایجاد و اعمال migrations
make superuser         # ایجاد superuser
make shell-backend     # Django shell
make shell-db          # PostgreSQL shell
make format            # Format کردن کد
make lint              # چک کردن code quality
make security-check    # بررسی امنیتی
make clean             # پاک کردن کامل
make prod-check        # چک‌لیست قبل از production
```

### Docker Commands

```bash
# مشاهده وضعیت containers
docker-compose ps

# Logs تک سرویس
docker-compose logs -f backend
docker-compose logs -f frontend

# وارد شدن به container
docker-compose exec backend bash
docker-compose exec frontend sh

# Restart کردن سرویس
docker-compose restart backend

# Rebuild کردن
docker-compose build --no-cache

# پاک کردن همه چیز
docker-compose down -v --remove-orphans
```

---

## 🧪 اجرای تست‌ها

### Backend Tests

```bash
# با Makefile
make test

# با coverage
make test-coverage

# یا مستقیم
docker-compose exec backend python manage.py test
docker-compose exec backend pytest --cov
```

### Frontend Tests

```bash
docker-compose exec frontend npm test
docker-compose exec frontend npm run test:coverage
```

---

## 🔒 Pre-commit Hooks

```bash
# نصب
make setup

# اجرا روی تمام فایل‌ها
pre-commit run --all-files

# اجرا روی فایل‌های staged
pre-commit run

# Skip کردن برای commit فوری
git commit -m "message" --no-verify
```

---

## 📂 Database Management

### Migrations

```bash
# ایجاد migration جدید
make migrations
# یا
docker-compose exec backend python manage.py makemigrations

# اعمال migrations
docker-compose exec backend python manage.py migrate

# برگشت migration
docker-compose exec backend python manage.py migrate app_name migration_name

# مشاهده وضعیت migrations
docker-compose exec backend python manage.py showmigrations
```

### Database Shell

```bash
# PostgreSQL shell
make shell-db
# یا
docker-compose exec db psql -U postgres -d taskboard

# دستورات SQL مفید:
\dt                 # لیست tables
\d table_name       # ساختار table
\q                  # خروج
```

---

## 🐞 رفع مشکلات رایج

### Port قبلاً در حال استفاده است

```bash
# پیدا کردن و kill کردن process
sudo lsof -i :8000
sudo kill -9 <PID>

# یا تغییر port در docker-compose.yml
```

### Container ها start نمی‌شوند

```bash
# بررسی logs
docker-compose logs -f

# Rebuild بدون cache
docker-compose build --no-cache
docker-compose up --force-recreate

# پاک کردن کامل
make clean
docker system prune -a
```

### Database Connection Error

```bash
# چک کردن که PostgreSQL آماده است
docker-compose exec db pg_isready

# Restart database
docker-compose restart db

# چک کردن فایل .env
cat .env | grep POSTGRES
```

### Tests Fail می‌شوند

```bash
# اطمینان از بودن migrations
make migrations

# اجرای تک تست
docker-compose exec backend python manage.py test app.tests.test_file

# مشاهده logs دقیق‌تر
docker-compose exec backend python manage.py test --verbosity=2
```

---

## 🚀 Development Workflow

### 1. شروع کار روزانه

```bash
# Pull کردن آخرین تغییرات
git pull origin main

# اجرای پروژه
make up

# مشاهده logs
make logs
```

### 2. کار روی Feature جدید

```bash
# ایجاد branch جدید
git checkout -b feature/new-feature

# کدنویسی...

# Format و Lint
make format
make lint

# تست
make test

# Commit (خودکار pre-commit اجرا می‌شه)
git add .
git commit -m "feat: add new feature"

# Push
git push origin feature/new-feature
```

### 3. قبل از PR

```bash
# چک‌لیست کامل
make prod-check

# Rebase با main
git fetch origin
git rebase origin/main

# Push
git push origin feature/new-feature --force-with-lease

# ایجاد Pull Request در GitHub
```

---

## 📚 منابع بیشتر

- [README.md](README.md) - مستندات کامل پروژه
- [CI_CD_TROUBLESHOOTING.md](CI_CD_TROUBLESHOOTING.md) - رفع مشکلات CI/CD
- [SECURITY.md](SECURITY.md) - چک‌لیست امنیتی
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - راهنمای نصب جزئیات

---

## ❓ دریافت کمک

اگر مشکلی داشتید:

1. در [CI_CD_TROUBLESHOOTING.md](CI_CD_TROUBLESHOOTING.md) جستجو کنید
2. Logs را بررسی کنید: `make logs`
3. در [GitHub Issues](https://github.com/mhmdrz22/enginner/issues) جستجو کنید
4. Issue جدید باز کنید

---

**موفق باشید!** 🚀
