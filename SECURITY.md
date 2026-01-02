# Security Policy and Checklist

## 🔒 Security Guidelines

این فایل شامل تمام موارد امنیتی است که باید قبل از production بررسی شوند.

## Pre-Production Checklist (فعلا)

### ✅ کانفیگ‌های اولیه
- [x] Pre-commit hooks نصب و فعال شده
- [x] فایل `.pre-commit-config.yaml` ایجاد شده
- [x] Git hooks برای جلوگیری از commit به main
- [ ] تمام تیم اعضا pre-commit را نصب کرده‌اند
- [ ] `.secrets.baseline` ایجاد شده

### ✅ مدیریت Secret ها
- [ ] فایل `.env` از git history حذف شده (استفاده از git filter-repo)
- [ ] تمام `.env` فایل‌ها در `.gitignore` هستند
- [ ] `.env.example` بدون هیچ اطلاعات حساس
- [ ] تمام SECRET_KEY ها و password ها تغییر کرده‌اند
- [ ] استفاده از environment variables به جای hardcode

### ✅ Docker و محیط‌های مختلف
- [x] `docker-compose.yml` برای development
- [x] `docker-compose.prod.yml` برای production
- [ ] `docker-compose.test.yml` برای تست‌ها
- [ ] `.env.example` کامل با توضیحات
- [ ] `.env.local` برای development محلی
- [ ] `.env.test` برای محیط تست
- [ ] `.env.production` برای production (نباید در git باشد)

### ✅ تست و کیفیت کد
- [ ] Coverage حداقل 85٪
- [ ] تست‌های Unit برای بخش‌های حیاتی
- [ ] تست‌های Integration برای API ها
- [ ] Security tests (مثلا SQL injection, XSS)
- [ ] تست‌های load و performance

---

## 🚨 Production Critical Checklist

### Django Settings - CRITICAL
```python
# ⚠️ این موارد حتما باید در production تنظیم شوند
DEBUG = False  # حتما False
SECRET_KEY = os.environ.get('SECRET_KEY')  # از environment
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']  # محدود به domain واقعی
```

### Security Headers - REQUIRED
```python
# Django Security Settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### Database Security
- [ ] Password قوی (حداقل 16 کاراکتر، ترکیبی)
- [ ] Database user با حداقل دسترسی لازم
- [ ] Backup روزانه فعال
- [ ] Backup در مکان جداگانه و امن
- [ ] Test restore کردن backup

### SSL/TLS Configuration
- [ ] SSL Certificate نصب شده
- [ ] Certificate از CA معتبر (مثلا Let's Encrypt)
- [ ] HTTPS اجباری (HTTP redirect to HTTPS)
- [ ] TLS 1.2+ فعال (TLS 1.0 و 1.1 غیرفعال)
- [ ] SSL Labs test: حداقل نمره A

### Application Security
- [ ] CORS به درستی کانفیگ شده
- [ ] Rate limiting فعال (مثلا django-ratelimit)
- [ ] SQL Injection prevention (استفاده از ORM)
- [ ] XSS protection فعال
- [ ] CSRF protection فعال
- [ ] File upload validation
- [ ] Input sanitization

### Infrastructure Security
- [ ] Firewall کانفیگ شده (فقط port های لازم)
- [ ] SSH key-based authentication
- [ ] Fail2ban یا مشابه نصب شده
- [ ] Automated security updates
- [ ] Log rotation کانفیگ شده

### Monitoring و Logging
- [ ] Error logging فعال (مثلا Sentry)
- [ ] Access logs فعال
- [ ] Alert برای suspicious activities
- [ ] Health check endpoints
- [ ] Monitoring dashboard (مثلا Grafana)
- [ ] Uptime monitoring

### Docker Production
- [ ] استفاده از non-root user در containers
- [ ] Multi-stage builds برای کاهش حجم
- [ ] Security scan با Trivy یا Snyk
- [ ] Resource limits تعریف شده
- [ ] Health checks برای تمام services
- [ ] Restart policies تنظیم شده

### CI/CD Security
- [ ] Secrets در GitHub Secrets ذخیره شده
- [ ] Security scanning در pipeline
- [ ] Dependency vulnerability scanning
- [ ] Code quality gates
- [ ] Automated testing قبل از merge

---

## 🔍 Security Scanning Commands

### Pre-commit Checks
```bash
# نصب pre-commit
pip install pre-commit
pre-commit install

# اجرای manual
pre-commit run --all-files

# بروزرسانی hooks
pre-commit autoupdate
```

### Python Security Scanning
```bash
# Bandit - Security linter
bandit -r backend/ -ll

# Safety - Dependency vulnerability check
safety check --file backend/requirements.txt

# Pip-audit - Alternative to safety
pip-audit
```

### Docker Security Scanning
```bash
# Trivy - Container vulnerability scanner
trivy image your-image:tag

# Docker scan
docker scan your-image:tag

# Hadolint - Dockerfile linter
hadolint backend/Dockerfile
hadolint frontend/Dockerfile
```

### Full Project Scan
```bash
# Trivy filesystem scan
trivy fs --security-checks vuln,config .

# Secret scanning
detect-secrets scan > .secrets.baseline
detect-secrets audit .secrets.baseline
```

---

## 📋 Regular Security Tasks

### هفتگی
- [ ] بررسی logs برای suspicious activities
- [ ] بررسی uptime و performance metrics
- [ ] بررسی disk space و resources

### ماهانه
- [ ] بروزرسانی dependencies
- [ ] Security scanning کل پروژه
- [ ] Review access logs
- [ ] Test backup restoration

### فصلی (هر 3 ماه)
- [ ] Security audit کامل
- [ ] Penetration testing
- [ ] Review و بروزرسانی security policies
- [ ] SSL certificate renewal check

---

## 🆘 Incident Response Plan

در صورت مشکل امنیتی:

1. **فوری**: سرویس را offline کنید اگر breach فعال است
2. **شناسایی**: scope و nature مشکل را تعیین کنید
3. **Log**: تمام اطلاعات مربوط را ذخیره کنید
4. **Patch**: مشکل را برطرف کنید
5. **Test**: تست کنید که مشکل حل شده
6. **Monitor**: مانیتورینگ فعال برای تشخیص تکرار
7. **Document**: همه چیز را مستند کنید
8. **Review**: Post-mortem و بهبود process ها

---

## 📞 Reporting Security Issues

اگر مشکل امنیتی پیدا کردید:
- ❌ Public issue باز نکنید
- ✅ به صورت خصوصی گزارش دهید
- ✅ شامل جزئیات کافی برای reproduce

---

## 🔗 Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django Security](https://docs.djangoproject.com/en/stable/topics/security/)
- [Docker Security Best Practices](https://docs.docker.com/develop/security-best-practices/)
- [Mozilla Observatory](https://observatory.mozilla.org/)
- [SSL Labs](https://www.ssllabs.com/ssltest/)

---

**آخرین بروزرسانی**: {{ date }}
**بررسی بعدی**: قبل از production deployment
