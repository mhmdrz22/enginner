# 🚀 راهنمای راه‌اندازی پروژه Task Manager

## 📚 فهرست مطالب

- [1. پیش‌نیازها](#1-پیش‌نیازها)
- [2. نصب Backend](#2-نصب-backend)
- [3. نصب Frontend](#3-نصب-frontend)
- [4. راه‌اندازی با Docker](#4-راه‌اندازی-با-docker)
- [5. تست پروژه](#5-تست-پروژه)
- [6. مشکلات رایج](#6-مشکلات-رایج)

---

## 1. پیش‌نیازها

قبل از شروع، مطمئن شوید که این ابزارها نصب شده‌اند:

### نسخه مستقیم (Without Docker)

```bash
# Python 3.10+
python --version

# Node.js 18+ و npm
node --version
npm --version

# PostgreSQL 14+
psql --version

# Redis 7+
redis-cli --version
```

### نسخه Docker

```bash
# Docker و Docker Compose
docker --version
docker-compose --version
```

---

## 2. نصب Backend

### 2.1. Clone رپوزیتوری

```bash
git clone https://github.com/mhmdrz22/enginner.git
cd enginner
```

### 2.2. ساخت Virtual Environment

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2.3. نصب وابستگی‌ها

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 2.4. پیکربندی متغیرهای محیطی

```bash
# کپی فایل .env.example
cp .env.example .env

# ویرایش .env و تنظیم مقادیر زیر:
```

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_NAME=taskboard
DATABASE_USER=postgres
DATABASE_PASSWORD=your-password
DATABASE_HOST=localhost
DATABASE_PORT=5432

REDIS_URL=redis://localhost:6379/1

CORS_ALLOWED_ORIGINS=http://localhost:5173
```

### 2.5. ایجاد بانک اطلاعاتی

```bash
# ورود به PostgreSQL
psql -U postgres

# ایجاد database
CREATE DATABASE taskboard;

# خروج
\q
```

### 2.6. اجرای Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 2.7. ایجاد Superuser

```bash
python manage.py createsuperuser
```

### 2.8. راه‌اندازی Server

```bash
python manage.py runserver
```

✅ Backend روی http://localhost:8000 فعال است

---

## 3. نصب Frontend

### 3.1. نصب وابستگی‌ها

```bash
cd ../frontend
npm install
```

### 3.2. پیکربندی متغیرهای محیطی

```bash
# کپی فایل .env.example
cp .env.example .env

# محتوای .env:
```

```env
VITE_API_URL=http://localhost:8000/api
```

### 3.3. راه‌اندازی Development Server

```bash
npm run dev
```

✅ Frontend روی http://localhost:5173 فعال است

---

## 4. راه‌اندازی با Docker

### 4.1. بیلد و اجرا

```bash
# برگشت به ریشه پروژه
cd ..

# بیلد و راه‌اندازی
docker-compose up --build
```

### 4.2. راه‌اندازی Migrations

```bash
# در ترمینال جدید
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```

✅ پروژه کامل روی Docker فعال است:
- Backend: http://localhost:8000
- Frontend: http://localhost:5173
- PgAdmin: http://localhost:5050

---

## 5. تست پروژه

### 5.1. تست Backend

```bash
cd backend

# اجرای همه تست‌ها
python manage.py test

# با pytest
pytest

# با coverage
pytest --cov=. --cov-report=html
```

### 5.2. تست Frontend

```bash
cd frontend

# Unit و Integration tests
npm run test

# با coverage
npm run test:coverage

# E2E tests
npm run test:e2e
```

---

## 6. مشکلات رایج

### مشکل 1: خطای CORS

**علت:** Backend به Frontend اجازه دسترسی نمی‌دهد

**حل:**
```python
# در backend/config/settings/base.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
```

### مشکل 2: خطای اتصال به Database

**حل:**
```bash
# مطمئن شوید PostgreSQL فعال است
sudo service postgresql status

# اگر غیرفعال است
sudo service postgresql start
```

### مشکل 3: Module Not Found در Frontend

**حل:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### مشکل 4: Redis Connection Error

**حل:**
```bash
# شروع Redis
sudo service redis-server start

# چک وضعیت
redis-cli ping
# باید PONG برگرداند
```

---

## 📦 ساختار پروژه

```
enginner/
├── backend/              # Django REST API
│   ├── accounts/         # مدیریت کاربران
│   ├── tasks/            # مدیریت تسک‌ها
│   ├── config/           # تنظیمات
│   └── requirements.txt
│
├── frontend/            # React + TypeScript
│   ├── src/
│   │   ├── components/   # کامپوننت‌ها
│   │   ├── pages/        # صفحات
│   │   ├── services/     # API calls
│   │   ├── store/        # State management
│   │   └── App.tsx
│   └── package.json
│
├── docker-compose.yml
└── README.md
```

---

## 🚀 ویژگی‌های پیاده‌سازی شده

### Backend
- ✅ JWT Authentication
- ✅ User Management
- ✅ Task CRUD
- ✅ Soft Delete
- ✅ Task History
- ✅ Redis Caching
- ✅ Rate Limiting
- ✅ 95%+ Test Coverage

### Frontend
- ✅ Login/Register Pages
- ✅ Dashboard with Statistics
- ✅ Kanban Board with Drag & Drop
- ✅ Task Filters & Search
- ✅ Profile Management
- ✅ Dark Mode
- ✅ Responsive Design
- ✅ 85%+ Test Coverage

---

## 👥 مشارکت

برای مشارکت:

1. Fork کنید
2. Feature branch بسازید: `git checkout -b feature/amazing-feature`
3. Commit کنید: `git commit -m 'Add amazing feature'`
4. Push کنید: `git push origin feature/amazing-feature`
5. Pull Request بفرستید

---

## 📝 لایسنس

GPL-3.0 License

---

## 👤 مخاطب

Mohammad Reza - [@mhmdrz22](https://github.com/mhmdrz22)

Project Link: [https://github.com/mhmdrz22/enginner](https://github.com/mhmdrz22/enginner)
