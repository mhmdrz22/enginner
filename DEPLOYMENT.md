# 📦 راهنمای کامل دیپلوی

## فهرست مطالب

- [راه‌های مختلف دیپلوی](#راه‌های-مختلف-دیپلوی)
- [دیپلوی روی Railway](#دیپلوی-روی-railway)
- [دیپلوی روی Liara](#دیپلوی-روی-liara)
- [دیپلوی روی AWS EC2](#دیپلوی-روی-aws-ec2)
- [دیپلوی روی DigitalOcean](#دیپلوی-روی-digitalocean)
- [تنظیمات Production](#تنظیمات-production)
- [مانیتورینگ و Logging](#مانیتورینگ-و-logging)

---

## 🚀 راه‌های مختلف دیپلوی

### مقایسه پلتفرم‌ها

| پلتفرم | سهولت | قیمت | کنترل | مناسب برای |
|--------|-------|------|-------|------------|
| **Railway** | ⭐⭐⭐⭐⭐ | رایگان تا 500 ساعت | متوسط | MVP، شروع |
| **Liara** | ⭐⭐⭐⭐ | از 20 هزار تومان | خوب | پروژه‌های ایرانی |
| **Render** | ⭐⭐⭐⭐ | رایگان محدود | خوب | استارتاپ‌ها |
| **AWS EC2** | ⭐⭐⭐ | Pay as you go | عالی | Enterprise |
| **DigitalOcean** | ⭐⭐⭐ | از $5/ماه | عالی | متوسط تا بزرگ |

---

## 🚂 دیپلوی روی Railway

### مزایا:
- ✅ راحت‌ترین راه
- ✅ رایگان 500 ساعت ماهانه
- ✅ Git push = خودکار deploy
- ✅ Database و Redis داخلی

### مراحل:

#### 1. آماده‌سازی پروژه

```bash
# Procfile (root)
web: cd backend && gunicorn config.wsgi:application
worker: cd backend && celery -A config worker --loglevel=info
```

```bash
# railway.json (root)
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "cd backend && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

#### 2. ایجاد پروژه در Railway

```bash
# نصب Railway CLI
npm i -g @railway/cli

# لاگین
railway login

# ایجاد پروژه
railway init

# لینک به GitHub
railway link
```

#### 3. اضافه کردن Database و Redis

```bash
# PostgreSQL
railway add postgres

# Redis
railway add redis
```

#### 4. تنظیم Environment Variables

```bash
DATABASE_URL=${{Postgres.DATABASE_URL}}
REDIS_URL=${{Redis.REDIS_URL}}
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=*.railway.app
CELERY_BROKER_URL=${{Redis.REDIS_URL}}
```

#### 5. Deploy!

```bash
railway up
```

---

## 🇮🇷 دیپلوی روی Liara

### مزایا:
- ✅ سرورهای ایران
- ✅ پشتیبانی فارسی
- ✅ قیمت مناسب
- ✅ پرداخت ریالی

### مراحل:

#### 1. نصب Liara CLI

```bash
npm install -g @liara/cli
liara login
```

#### 2. ایجاد App

```bash
liara create --app taskboard --platform django
```

#### 3. تنظیم liara.json

```json
{
  "platform": "django",
  "app": "taskboard",
  "port": 8000,
  "django": {
    "collectstatic": true,
    "compressstatic": true
  },
  "build": {
    "location": "backend"
  }
}
```

#### 4. ایجاد Database

```bash
# PostgreSQL
liara db create --name taskboard-db --type postgres --plan starter

# Redis
liara db create --name taskboard-redis --type redis --plan starter
```

#### 5. تنظیم متغیرها

```bash
liara env:set DATABASE_URL=postgresql://...
liara env:set SECRET_KEY=your-secret
liara env:set DEBUG=False
liara env:set ALLOWED_HOSTS=*.liara.run
```

#### 6. Deploy

```bash
liara deploy
```

---

## ☁️ دیپلوی روی AWS EC2

### مزایا:
- ✅ کنترل کامل
- ✅ مقیاس‌پذیری بالا
- ✅ قابلیت‌های Enterprise

### مراحل:

#### 1. راه‌اندازی EC2 Instance

```bash
# AWS Console:
# 1. EC2 → Launch Instance
# 2. Ubuntu 22.04 LTS
# 3. t2.micro (Free tier) یا بزرگتر
# 4. Security Group: 22, 80, 443
# 5. Key pair ساخت و دانلود
```

#### 2. اتصال به سرور

```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

#### 3. نصب Docker

```bash
sudo apt update
sudo apt install docker.io docker-compose -y
sudo usermod -aG docker $USER
newgrp docker
```

#### 4. Clone و Setup

```bash
git clone https://github.com/mhmdrz22/enginner.git
cd enginner

# تنظیم .env
cp .env.example .env
nano .env  # ویرایش مقادیر

# Build و Start
docker-compose -f docker-compose.prod.yml up -d
```

#### 5. Nginx و SSL

```bash
sudo apt install nginx certbot python3-certbot-nginx -y

# تنظیم Nginx
sudo cp nginx/default.conf /etc/nginx/sites-available/taskboard
sudo ln -s /etc/nginx/sites-available/taskboard /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# SSL Certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## 🌊 دیپلوی روی DigitalOcean

### مزایا:
- ✅ قیمت مناسب ($5/ماه)
- ✅ رابط کاربری ساده
- ✅ Marketplace apps

### مراحل:

#### 1. ایجاد Droplet

```
- Ubuntu 22.04
- Basic Plan: $5/mo
- Region: نزدیک‌ترین
- SSH Key یا Password
```

#### 2. اتصال

```bash
ssh root@your-droplet-ip
```

#### 3. نصب Docker (یا استفاده از Docker Marketplace)

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

#### 4. Deploy (مشابه AWS)

```bash
git clone https://github.com/mhmdrz22/enginner.git
cd enginner
cp .env.example .env
# ویرایش .env
docker-compose -f docker-compose.prod.yml up -d
```

---

## ⚙️ تنظیمات Production

### چک‌لیست ضروری:

#### Security:

```bash
# .env
DEBUG=False
SECRET_KEY=<generate-strong-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECURE_SSL_REDIRECT=True
```

#### Database:

```python
# Production DB with connection pooling
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'connect_timeout': 10,
            'options': '-c statement_timeout=30000'
        }
    }
}
```

#### Static Files:

```bash
# Collect static files
python manage.py collectstatic --noinput

# یا با WhiteNoise
pip install whitenoise
# در settings.py:
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    ...
]
```

#### Celery:

```bash
# Supervisor config
[program:celery_worker]
command=/app/venv/bin/celery -A config worker -l info
autostart=true
autorestart=true

[program:celery_beat]
command=/app/venv/bin/celery -A config beat -l info
autostart=true
autorestart=true
```

---

## 📊 مانیتورینگ و Logging

### Sentry (Error Tracking)

```bash
pip install sentry-sdk
```

```python
# settings.py
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0,
)
```

### Logs

```python
# settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/django/error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
        },
    },
}
```

### Health Checks

```python
# urls.py
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({'status': 'healthy'})

urlpatterns = [
    path('health/', health_check),
]
```

---

## 🔄 CI/CD

GitHub Actions خودکار:

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Railway
        run: railway up
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

---

## 📞 پشتیبانی

مشکلی پیش اومد؟
- 📧 ایمیل: support@taskboard.com
- 💬 Issue در GitHub
- 📚 مستندات: [docs.taskboard.com](https://docs.taskboard.com)

---

**موفق باشید! 🚀**
