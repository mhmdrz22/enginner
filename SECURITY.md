# Security Guidelines & Checklist

## 🔴 Critical Security Issues - MUST FIX BEFORE PRODUCTION

### Authentication & Secrets
- [ ] **SECRET_KEY**: تولید SECRET_KEY جدید با حداقل 50 کاراکتر
  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
- [ ] **Database Passwords**: استفاده از رمز عبور قوی (حداقل 16 کاراکتر، شامل حروف بزرگ/کوچک، اعداد و کاراکترهای خاص)
- [ ] **Redis Password**: تنظیم رمز عبور برای Redis در production
- [ ] **Environment Variables**: همه مقادیر حساس از فایل `.env` خوانده شوند نه hardcode

### Django Security Settings
- [ ] `DEBUG=False` در production
- [ ] `ALLOWED_HOSTS` محدود به دامنه‌های واقعی (نه `*`)
- [ ] `CORS_ALLOWED_ORIGINS` محدود به دامنه‌های مجاز
- [ ] `SECURE_SSL_REDIRECT=True` برای redirect اجباری به HTTPS
- [ ] `SESSION_COOKIE_SECURE=True`
- [ ] `CSRF_COOKIE_SECURE=True`
- [ ] `SECURE_BROWSER_XSS_FILTER=True`
- [ ] `SECURE_CONTENT_TYPE_NOSNIFF=True`
- [ ] `X_FRAME_OPTIONS=DENY` یا `SAMEORIGIN`
- [ ] `SECURE_HSTS_SECONDS=31536000` (1 سال)
- [ ] `SECURE_HSTS_INCLUDE_SUBDOMAINS=True`
- [ ] `SECURE_HSTS_PRELOAD=True`

### File & Git Security
- [ ] فایل `.env` در `.gitignore` قرار دارد
- [ ] فایل `.env` از git history حذف شده است
- [ ] Pre-commit hooks نصب و فعال است
- [ ] Secret scanning با detect-secrets فعال است
- [ ] هیچ کلید خصوصی یا certificate در repository نیست

---

## 🟡 Pre-Production Checklist

### Code Quality & Testing
- [ ] تمام تست‌ها pass می‌شوند
- [ ] Code coverage حداقل 80% است
- [ ] Security scan با bandit انجام شده
- [ ] Dependency vulnerability check با safety انجام شده
- [ ] Static code analysis با flake8/pylint انجام شده

### Docker & Infrastructure
- [ ] Dockerfile از multi-stage build استفاده می‌کند
- [ ] Images از non-root user استفاده می‌کنند
- [ ] Health checks برای همه سرویس‌ها تعریف شده
- [ ] Resource limits (CPU/Memory) تنظیم شده
- [ ] Logging به درستی پیکربندی شده

### Database
- [ ] Database migrations اعمال شده
- [ ] Database backup strategy مشخص شده
- [ ] Database indexes بهینه شده
- [ ] Database connection pooling پیکربندی شده

### API & Backend
- [ ] Rate limiting فعال است
- [ ] API authentication برای همه endpoints
- [ ] Input validation در همه جا اعمال شده
- [ ] SQL injection prevention (استفاده از ORM)
- [ ] XSS prevention در output ها
- [ ] CSRF protection فعال است

---

## 🟢 Production Checklist

### SSL/TLS
- [ ] SSL Certificate نصب شده (Let's Encrypt یا خریداری شده)
- [ ] Certificate renewal خودکار پیکربندی شده
- [ ] TLS 1.2+ فعال است
- [ ] Weak ciphers غیرفعال شده‌اند

### Monitoring & Logging
- [ ] Application monitoring راه‌اندازی شده (Sentry, New Relic, etc.)
- [ ] Log aggregation پیکربندی شده
- [ ] Error alerting فعال است
- [ ] Performance monitoring فعال است
- [ ] Uptime monitoring فعال است

### Backup & Recovery
- [ ] Database backup روزانه/هفتگی
- [ ] Backup verification منظم
- [ ] Disaster recovery plan مستند شده
- [ ] Media files backup شده

### Performance
- [ ] Static files از CDN serve می‌شوند
- [ ] Database query optimization انجام شده
- [ ] Caching strategy پیاده شده (Redis)
- [ ] GZIP compression فعال است
- [ ] Image optimization انجام شده

### Network Security
- [ ] Firewall rules تنظیم شده
- [ ] DDoS protection فعال است (Cloudflare, etc.)
- [ ] Port scanning prevention
- [ ] VPN/Private network برای دسترسی به database

---

## 🔧 Security Tools & Commands

### Pre-commit Setup
```bash
# نصب pre-commit
pip install pre-commit

# نصب hooks
pre-commit install

# اجرا روی تمام فایل‌ها
pre-commit run --all-files

# ایجاد baseline برای secrets
detect-secrets scan > .secrets.baseline
```

### Security Scanning
```bash
# Bandit - Python security scanner
bandit -r backend/ -ll

# Safety - Dependency vulnerability checker
safety check --file backend/requirements.txt

# Trivy - Container vulnerability scanner
trivy image taskboard_backend:latest

# npm audit - Node.js dependencies
cd frontend && npm audit
```

### Package Updates
```bash
# بررسی نسخه‌های outdated در Python
pip list --outdated

# بررسی نسخه‌های outdated در Node.js
npm outdated

# بروزرسانی packages (با احتیاط)
pip install --upgrade <package-name>
npm update <package-name>
```

---

## 📚 Security Best Practices

### Password Policies
- حداقل 16 کاراکتر
- ترکیب حروف بزرگ/کوچک، اعداد و کاراکترهای خاص
- استفاده از password manager
- تغییر منظم passwords (هر 90 روز)
- عدم استفاده مجدد از passwords

### API Security
- استفاده از JWT یا Token-based authentication
- Rate limiting برای جلوگیری از abuse
- Input validation در سمت server
- Output encoding برای جلوگیری از XSS
- استفاده از HTTPS برای همه API calls

### Container Security
- استفاده از official images
- Scan images برای vulnerabilities
- استفاده از non-root users
- حداقل packages ضروری را نصب کنید
- بروزرسانی منظم base images

### Code Review Guidelines
- بررسی hardcoded secrets
- بررسی SQL injection vulnerabilities
- بررسی XSS vulnerabilities
- بررسی authentication/authorization logic
- بررسی error handling و information disclosure

---

## 🚨 Incident Response

در صورت کشف vulnerability:

1. **فوری**: سرویس را از دسترس خارج کنید (در صورت critical)
2. **ارزیابی**: میزان آسیب را ارزیابی کنید
3. **اصلاح**: vulnerability را اصلاح کنید
4. **تست**: اصلاح را به طور کامل تست کنید
5. **Deploy**: با احتیاط به production deploy کنید
6. **مستند‌سازی**: incident را مستند کنید
7. **یادگیری**: از incident درس بگیرید

---

## 📞 Security Contacts

- **تیم توسعه**: [ایمیل یا Slack]
- **مدیر پروژه**: [ایمیل]
- **مسئول امنیت**: [ایمیل]

---

## 📅 Security Audit Schedule

- **روزانه**: Automated security scans (pre-commit, CI/CD)
- **هفتگی**: Dependency updates check
- **ماهانه**: Manual security review
- **فصلی**: Comprehensive security audit
- **سالانه**: Penetration testing

---

**آخرین بروزرسانی**: 2026-01-02
**نسخه**: 1.0.0
