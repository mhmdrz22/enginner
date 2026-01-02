# Team Task Board – Django + React Starter

یک سیستم مدیریت وظایف تیمی با Django REST Framework در بک‌اند و React در فرانت‌اند. این پروژه شامل قابلیت‌های احراز هویت، مدیریت کاربران، تسک‌ها و پنل ادمین با ارسال ایمیل غیرهمزمان است.

## 📋 فهرست مطالب

- [نیازمندی‌ها](#نیازمندی‌ها)
- [راه‌اندازی محلی](#راه‌اندازی-محلی)
- [راه‌اندازی با Docker](#راه‌اندازی-با-docker)
- [متغیرهای محیطی](#متغیرهای-محیطی)
- [تست‌ها](#تست‌ها)
- [دیپلوی روی Liara](#دیپلوی-روی-liara)
- [ساختار پروژه](#ساختار-پروژه)

## 🔧 نیازمندی‌ها

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (اختیاری)

## 🚀 راه‌اندازی محلی

### Backend (Django)

```bash
cd backend
python -m venv venv

# فعال‌سازی محیط مجازی
venv\Scripts\activate    # Windows
source venv/bin/activate # Linux/macOS

# نصب وابستگی‌ها
pip install -r requirements.txt

# ایجاد فایل .env
cp ../.env.example ../.env
# سپس مقادیر را در فایل .env تنظیم کنید

# اجرای Migration
python manage.py migrate

# ایجاد Superuser
python manage.py createsuperuser

# اجرای سرور
python manage.py runserver 8000
```

### Redis (برای Celery)

```bash
# نصب Redis
# Ubuntu/Debian:
sudo apt-get install redis-server
sudo systemctl start redis

# macOS:
brew install redis
brew services start redis

# Windows:
# دانلود از: https://github.com/microsoftarchive/redis/releases
```

### Celery Worker

در یک ترمینال جدید:

```bash
cd backend
source venv/bin/activate  # یا venv\Scripts\activate در Windows
celery -A config worker --loglevel=info
```

### Frontend (React + Vite)

در یک ترمینال جدید:

```bash
cd frontend
npm install
npm run dev
```

پروژه روی آدرس‌های زیر در دسترس است:
- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000/api`
- Admin Panel: `http://localhost:8000/admin`

## 🐳 راه‌اندازی با Docker

### پیش‌نیاز

مطمئن شوید Docker و Docker Compose نصب شده‌اند.

### اجرای پروژه

```bash
# ایجاد فایل .env
cp .env.example .env
# مقادیر را در .env تنظیم کنید

# Build و اجرای تمام سرویس‌ها
docker-compose up --build

# اجرا در Background
docker-compose up -d

# مشاهده لاگ‌ها
docker-compose logs -f

# مشاهده لاگ یک سرویس خاص
docker-compose logs -f backend
docker-compose logs -f celery_worker

# متوقف کردن سرویس‌ها
docker-compose down

# پاک کردن Volume‌ها (دیتابیس)
docker-compose down -v
```

### ایجاد Superuser در Docker

```bash
docker-compose exec backend python manage.py createsuperuser
```

### اجرای Migration در Docker

```bash
docker-compose exec backend python manage.py migrate
```

## ⚙️ متغیرهای محیطی

فایل `.env.example` را کپی کرده و به `.env` تغییر نام دهید:

```bash
cp .env.example .env
```

### متغیرهای ضروری:

| متغیر | توضیحات | مثال |
|-------|---------|------|
| `POSTGRES_DB` | نام دیتابیس | `software_project_test` |
| `POSTGRES_USER` | نام کاربری PostgreSQL | `postgres` |
| `POSTGRES_PASSWORD` | رمز عبور دیتابیس | `your_password` |
| `DATABASE_URL` | URL اتصال به دیتابیس | `postgresql://user:pass@db:5432/dbname` |
| `SECRET_KEY` | کلید مخفی Django | Generate با `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` |
| `DEBUG` | حالت Debug | `True` برای Development، `False` برای Production |
| `ALLOWED_HOSTS` | هاست‌های مجاز | `localhost,127.0.0.1,yourdomain.com` |
| `CELERY_BROKER_URL` | آدرس Redis برای Celery | `redis://redis:6379/0` |
| `EMAIL_HOST` | سرور SMTP | `smtp.gmail.com` |
| `EMAIL_HOST_USER` | ایمیل فرستنده | `your_email@gmail.com` |
| `EMAIL_HOST_PASSWORD` | رمز عبور ایمیل | App Password برای Gmail |

## 🧪 تست‌ها

### اجرای تست‌ها

```bash
cd backend
python manage.py test

# اجرای تست‌های یک اپلیکیشن خاص
python manage.py test tasks
python manage.py test accounts

# اجرای تست با نمایش Coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # تولید گزارش HTML
```

### اجرای تست در Docker

```bash
docker-compose exec backend python manage.py test
```

### هدف تست‌ها

- اطمینان از صحت عملکرد API endpoints
- تست احراز هویت و دسترسی‌ها
- تست منطق کسب‌وکار (Business Logic)
- تست ارسال ایمیل غیرهمزمان با Celery
- حداقل 85% Coverage برای بخش‌های کلیدی

## ☁️ دیپلوی روی Liara

### پیش‌نیازها

```bash
# نصب Liara CLI
npm install -g @liara/cli

# لاگین به Liara
liara login
```

### ایجاد برنامه و سرویس‌ها

```bash
# ایجاد برنامه Django
liara create --app enginner-taskboard --platform docker --region germany

# ایجاد دیتابیس PostgreSQL
liara db create --name taskboard-db --type postgres --plan starter

# ایجاد Redis
liara db create --name taskboard-redis --type redis --plan starter
```

### تنظیم متغیرهای محیطی در Liara

در پنل Liara، بخش Settings > Environment Variables:

```bash
DATABASE_URL=postgresql://username:password@host:port/database
SECRET_KEY=<your-strong-secret-key>
DEBUG=False
ALLOWED_HOSTS=enginner-taskboard.liara.run,yourdomain.ir
CELERY_BROKER_URL=redis://redis-host:6379/0
CELERY_RESULT_BACKEND=redis://redis-host:6379/1
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

### دیپلوی

```bash
# اولین دیپلوی
liara deploy --app enginner-taskboard --port 8000

# دیپلوی‌های بعدی
liara deploy
```

### اجرای Migration در Production

```bash
liara shell --app enginner-taskboard
python manage.py migrate
python manage.py createsuperuser
```

### لینک دیپلوی شده

🌐 **Production URL**: [https://enginner-taskboard.liara.run](https://enginner-taskboard.liara.run)

## 📁 ساختار پروژه

```
enginner/
├── backend/
│   ├── accounts/          # اپلیکیشن کاربران
│   ├── tasks/             # اپلیکیشن مدیریت تسک‌ها
│   ├── config/            # تنظیمات Django
│   │   ├── settings.py
│   │   ├── celery.py      # پیکربندی Celery
│   │   └── urls.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── manage.py
├── frontend/
│   ├── src/
│   ├── Dockerfile
│   ├── package.json
│   └── vite.config.js
├── .env                   # متغیرهای محیطی (Git Ignore)
├── .env.example           # نمونه متغیرها
├── docker-compose.yml     # تنظیمات Docker Compose
├── liara.json            # تنظیمات Liara
└── README.md
```

## 🔄 CI/CD با GitHub Actions

پایپ‌لاین CI/CD به صورت خودکار:
- تست‌ها را اجرا می‌کند
- Coverage را چک می‌کند
- در صورت موفقیت، به Liara دیپلوی می‌کند

فایل‌های Workflow در `.github/workflows/` قرار دارند.

## 📝 توضیحات فیچرها

### پنل ادمین
- مشاهده لیست کاربران و تسک‌ها
- ارسال ایمیل اطلاع‌رسانی به کاربران
- ارسال غیرهمزمان با Celery Worker

### احراز هویت
- JWT Token Authentication
- Registration & Login
- Password Reset

### مدیریت تسک‌ها
- CRUD operations
- تخصیص تسک به کاربران
- فیلتر و جستجو

## 🤝 مشارکت

برای مشارکت در پروژه:
1. Fork کنید
2. Branch جدید بسازید (`git checkout -b feature/AmazingFeature`)
3. تغییرات را Commit کنید (`git commit -m 'Add some AmazingFeature'`)
4. Push کنید (`git push origin feature/AmazingFeature`)
5. Pull Request باز کنید

## 📄 License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.

## 👥 نویسندگان

- **مهندسی نرم‌افزار** - پروژه پایانی
- دانشگاه: دانشگاه مالک اشتر

## 🙏 تشکر

- Django REST Framework
- React & Vite
- Celery & Redis
- Docker
- Liara Cloud Platform
