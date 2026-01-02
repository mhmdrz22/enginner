# 🐳 راهنمای کامل اجرای پروژه با Docker

## 📋 پیش‌نیازها

### نصب Docker و Docker Compose

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install docker.io docker-compose -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

**macOS:**
```bash
# با Homebrew
brew install --cask docker
```

**Windows:**
- دانلود [Docker Desktop](https://www.docker.com/products/docker-desktop/)

---

## 🚀 اجرای پروژه (خیلی ساده!)

### مرحله 1: کلون کردن پروژه

```bash
git clone https://github.com/mhmdrz22/enginner.git
cd enginner
```

### مرحله 2: تنظیم Environment Variables

```bash
# کپی کردن فایل .env.example
cp .env.example .env

# ویرایش .env (اختیاری برای development)
nano .env
```

**محتوای `.env` (پیش‌فرض برای Development):**
```env
# Django
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
POSTGRES_DB=taskboard
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Frontend
VITE_API_URL=http://localhost:8000
```

### مرحله 3: ساخت و اجرای Containers

```bash
# ساخت و اجرا (اولین بار)
docker-compose up --build

# یا در background
docker-compose up -d --build
```

**منتظر بمانید تا:**
- ✅ PostgreSQL بالا بیاد
- ✅ Backend migrate شه
- ✅ Frontend build شه
- ✅ Nginx start شه

### مرحله 4: دسترسی به پروژه

**Frontend:** http://localhost:3000

**Backend API:** http://localhost:8000/api/

**Swagger Docs:** http://localhost:8000/swagger/

**ReDoc:** http://localhost:8000/redoc/

**Django Admin:** http://localhost:8000/admin/

---

## 📦 دستورات مفید Docker

### مشاهده Logs

```bash
# همه containers
docker-compose logs -f

# فقط backend
docker-compose logs -f backend

# فقط frontend
docker-compose logs -f frontend

# فقط database
docker-compose logs -f db
```

### Stop کردن Containers

```bash
# توقف
docker-compose stop

# توقف و حذف containers
docker-compose down

# توقف و حذف همه چیز (volumes هم پاک میشه)
docker-compose down -v
```

### Restart کردن

```bash
# restart همه
docker-compose restart

# restart فقط backend
docker-compose restart backend
```

### اجرا بدون Build مجدد

```bash
# اگر قبلاً build کردید
docker-compose up

# در background
docker-compose up -d
```

### Status چک کردن

```bash
# وضعیت containers
docker-compose ps

# استفاده از منابع
docker stats
```

---

## 🔧 Django Management Commands

### اجرای Migrations

```bash
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
```

### ساخت Superuser

```bash
docker-compose exec backend python manage.py createsuperuser
```

### اجرای Tests

```bash
# همه تست‌ها
docker-compose exec backend python manage.py test

# با pytest
docker-compose exec backend pytest

# با coverage
docker-compose exec backend pytest --cov
```

### Collect Static Files

```bash
docker-compose exec backend python manage.py collectstatic --no-input
```

### Django Shell

```bash
docker-compose exec backend python manage.py shell
```

### Database Shell

```bash
# PostgreSQL shell
docker-compose exec db psql -U postgres -d taskboard

# Django dbshell
docker-compose exec backend python manage.py dbshell
```

---

## 🐛 عیب‌یابی (Troubleshooting)

### مشکل 1: Port در حال استفاده است

**خطا:** `Port 8000 is already allocated`

**راه‌حل:**
```bash
# پیدا کردن process
sudo lsof -i :8000

# kill کردن
sudo kill -9 <PID>

# یا تغییر port در docker-compose.yml
```

### مشکل 2: Database Connection Error

**خطا:** `could not connect to server`

**راه‌حل:**
```bash
# بررسی وضعیت db container
docker-compose ps

# restart database
docker-compose restart db

# بررسی logs
docker-compose logs db
```

### مشکل 3: Permission Denied

**خطا:** `Permission denied`

**راه‌حل:**
```bash
# اضافه کردن user به docker group
sudo usermod -aG docker $USER

# logout و login مجدد
```

### مشکل 4: Frontend نمایش داده نمیشه

**راه‌حل:**
```bash
# rebuild frontend
docker-compose up -d --build frontend

# بررسی logs
docker-compose logs frontend

# clear browser cache
```

### مشکل 5: Migrations Error

**راه‌حل:**
```bash
# حذف migrations
docker-compose exec backend find . -path "*/migrations/*.py" -not -name "__init__.py" -delete

# ساخت migrations جدید
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
```

---

## 🧹 پاک‌سازی کامل

```bash
# حذف containers
docker-compose down

# حذف volumes (دیتابیس پاک میشه!)
docker-compose down -v

# حذف images
docker-compose down --rmi all

# پاک‌سازی کامل Docker
docker system prune -a --volumes
```

---

## 📊 مانیتورینگ

### مشاهده Resource Usage

```bash
# realtime stats
docker stats

# استفاده از disk
docker system df
```

### بررسی Health

```bash
# health check
docker-compose ps

# detailed inspect
docker inspect <container_name>
```

---

## 🔐 Production Setup

برای production از `docker-compose.prod.yml` استفاده کن:

```bash
# اجرا
docker-compose -f docker-compose.prod.yml up -d --build

# logs
docker-compose -f docker-compose.prod.yml logs -f
```

**تغییرات ضروری برای Production:**

1. تغییر `SECRET_KEY` در `.env`
2. تنظیم `DEBUG=False`
3. تنظیم `ALLOWED_HOSTS`
4. استفاده از HTTPS
5. تنظیم backup برای database

---

## 📝 Workflow معمولی

```bash
# روز اول
git clone ...
cp .env.example .env
docker-compose up --build

# روزهای بعد
docker-compose up -d

# بعد از تغییر کد
docker-compose restart backend  # یا frontend

# بعد از تغییر models
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate

# پایان کار
docker-compose stop
```

---

## ⚡ Quick Commands

```bash
# همه چیز رو از صفر شروع کن
make clean && make dev

# فقط rebuild backend
make rebuild-backend

# فقط rebuild frontend
make rebuild-frontend

# logs
make logs

# shell backend
make shell-backend

# test
make test
```

---

## 🎯 چک‌لیست اولین اجرا

- [ ] Docker نصب شده؟
- [ ] Docker Compose نصب شده؟
- [ ] فایل `.env` ساخته شده؟
- [ ] `docker-compose up --build` اجرا شد؟
- [ ] Frontend روی port 3000 در دسترسه؟
- [ ] Backend روی port 8000 در دسترسه؟
- [ ] Swagger docs در دسترسه؟
- [ ] میتونی register/login کنی؟

---

**موفق باشی! 🚀**

مشکلی داری؟ [Issue بزن](https://github.com/mhmdrz22/enginner/issues)
