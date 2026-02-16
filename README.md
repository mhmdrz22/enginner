# 📊 Task Manager - سیستم مدیریت تسک

یک سیستم مدیریت تسک مدرن، حرفه‌ای و production-ready با Django REST Framework و React + TypeScript

[![License](https://img.shields.io/badge/license-GPL--3.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-4.2+-green.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/react-18+-61dafb.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/typescript-5+-3178c6.svg)](https://www.typescriptlang.org/)
[![Coverage](https://img.shields.io/badge/coverage-85%25+-brightgreen.svg)]()
[![Code Quality](https://img.shields.io/badge/code%20quality-A+-success.svg)]()

---

## ⭐ ویژگی‌های برجسته

### 🏗️ معماری حرفه‌ای
- ✅ **Low Coupling & High Cohesion** - طراحی مدولار و قابل نگهداری
- ✅ **SOLID Principles** - تمام اصول SOLID رعایت شده
- ✅ **Layered Architecture** - جداسازی کامل لایه‌ها
- ✅ **Design Patterns** - Repository, Factory, Observer, Strategy
- 📖 **[مستندات معماری کامل](ARCHITECTURE.md)**

### 🎯 Non-Functional Requirements
- ✅ **Performance**: < 200ms API response time
- ✅ **Security**: JWT, Rate Limiting, HTTPS, Security Headers
- ✅ **Scalability**: Stateless backend, Redis caching
- ✅ **Reliability**: 99.9% uptime, automated backups
- ✅ **Maintainability**: 85%+ test coverage, comprehensive docs
- 📖 **[مستندات NFR کامل](NFR.md)**

---

## 🌟 ویژگی‌های کلیدی

### 🔐 Authentication & Security
- ✅ JWT Authentication با Access & Refresh Tokens  
- ✅ User Registration & Login
- ✅ Password Reset Flow
- ✅ Rate Limiting (100/day anonymous, 1000/day authenticated)
- ✅ Token Blacklisting
- ✅ CORS پیکربندی شده
- ✅ Security Headers (XSS, CSRF, Clickjacking protection)

### 📋 Task Management
- ✅ CRUD کامل برای تسک‌ها
- ✅ Kanban Board با Drag & Drop
- ✅ Task Status (TODO, DOING, DONE)
- ✅ Priority Levels (LOW, MEDIUM, HIGH)
- ✅ Due Dates & Overdue Detection
- ✅ Task History & Audit Trail
- ✅ Soft Delete (بازیابی تسک‌ها)
- ✅ Tags & Labels
- ✅ Search & Filter
- ✅ Bulk Operations

### 🎨 UI/UX
- ✅ مدرن و زیبا با shadcn/ui
- ✅ Dark Mode Support
- ✅ Responsive Design (موبایل و دسکتاپ)
- ✅ Persian RTL Support
- ✅ Toast Notifications
- ✅ Loading States
- ✅ Error Boundaries
- ✅ Optimistic UI Updates

### ⚡ Performance & Optimization
- ✅ Redis Caching (5-min TTL)
- ✅ Database Query Optimization (select_related, prefetch_related)
- ✅ Connection Pooling (CONN_MAX_AGE=600)
- ✅ Lazy Loading & Code Splitting
- ✅ React Query for Data Fetching
- ✅ Bundle Size < 250KB (gzipped)

### 🧪 Testing & Quality
- ✅ **Backend Coverage: 85%+**
- ✅ **Frontend Coverage: 80%+**
- ✅ Unit Tests (pytest, Vitest)
- ✅ Integration Tests
- ✅ E2E Tests (Playwright)
- ✅ Code Linting (ESLint, flake8, black)
- ✅ Type Safety (TypeScript, mypy)
- ✅ Automated CI/CD (GitHub Actions)

### 🚀 DevOps & Deployment
- ✅ Docker & Docker Compose
- ✅ Multi-stage Docker builds
- ✅ CI/CD Pipeline
- ✅ Automated testing
- ✅ Security scanning (Trivy)
- ✅ Health checks
- ✅ Logging & Monitoring ready

---

## 📦 تکنولوژی‌های استفاده شده

### Backend
- **Framework:** Django 4.2+ & Django REST Framework 3.14+
- **Database:** PostgreSQL 14+
- **Cache:** Redis 7+
- **Authentication:** JWT (djangorestframework-simplejwt)
- **API Docs:** drf-spectacular (Swagger/OpenAPI)
- **Testing:** pytest, pytest-django, pytest-cov, pytest-faker
- **Task Queue:** Celery (ready for async tasks)
- **Code Quality:** black, isort, flake8, mypy

### Frontend
- **Framework:** React 18+ with TypeScript 5+
- **Build Tool:** Vite 5+
- **UI Library:** shadcn/ui (Radix UI + Tailwind CSS)
- **State Management:** Zustand
- **Data Fetching:** TanStack Query (React Query)
- **Forms:** React Hook Form + Zod
- **Drag & Drop:** @dnd-kit/core
- **Routing:** React Router v6
- **Date Handling:** date-fns
- **Notifications:** sonner
- **Testing:** Vitest, React Testing Library, Playwright
- **Code Quality:** ESLint, Prettier, TypeScript strict mode

### DevOps
- **Containerization:** Docker & Docker Compose
- **CI/CD:** GitHub Actions
- **Security:** Trivy vulnerability scanner
- **Monitoring:** Health check endpoints
- **Logging:** Rotating file logs (10 MB, 5 backups)

---

## 🚀 راه‌اندازی سریع

### پیش‌نیازها

```bash
# روش اول: Docker (توصیه می‌شود)
Docker 20+
Docker Compose 2+

# روش دوم: نصب مستقیم
Python 3.10+
Node.js 20+
PostgreSQL 14+
Redis 7+
```

### نصب با Docker (راحت‌ترین روش)

```bash
# 1. Clone رپوزیتوری
git clone https://github.com/mhmdrz22/enginner.git
cd enginner

# 2. اجرا با Docker Compose
docker-compose up --build

# 3. اجرای Migrations (در terminal دیگر)
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser

# ✅ آماده است!
# Backend API: http://localhost:8000
# Frontend: http://localhost:5173
# API Docs: http://localhost:8000/api/schema/swagger/
# Admin Panel: http://localhost:8000/admin/
```

### نصب مستقیم

برای راهنمای کامل [SETUP.md](SETUP.md) را مشاهده کنید.

---

## 📝 ساختار پروژه

```
enginner/
├── backend/                   # Django backend
│   ├── accounts/              # User management
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── tests/
│   ├── tasks/                 # Task management
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── filters.py
│   │   └── tests/
│   ├── config/                # Django settings
│   │   └── settings/
│   │       ├── base.py
│   │       ├── development.py
│   │       ├── production.py
│   │       └── test.py
│   ├── requirements.txt
│   └── pytest.ini
│
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/            # shadcn/ui components
│   │   │   ├── layout/
│   │   │   └── tasks/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── stores/
│   │   ├── hooks/
│   │   ├── lib/
│   │   └── tests/
│   ├── e2e/                   # Playwright E2E tests
│   ├── package.json
│   ├── vite.config.ts
│   ├── vitest.config.ts
│   └── .prettierrc
│
├── .github/
│   └── workflows/
│       ├── backend-tests.yml
│       ├── frontend-tests.yml
│       └── ci-cd.yml
│
├── docker-compose.yml
├── README.md                  # این فایل
├── ARCHITECTURE.md            # 🏗️ مستندات معماری
├── NFR.md                     # 🎯 Non-Functional Requirements
└── SETUP.md                   # راهنمای نصب کامل
```

---

## 📚 مستندسازی جامع

### 📖 مستندات اصلی
- 🏗️ **[Architecture Documentation](ARCHITECTURE.md)** - معماری، Coupling/Cohesion، SOLID
- 🎯 **[Non-Functional Requirements](NFR.md)** - Performance، Security، Testing
- 📦 **[Setup Guide](SETUP.md)** - راهنمای نصب کامل

### API Documentation
- **Swagger UI:** http://localhost:8000/api/schema/swagger/
- **ReDoc:** http://localhost:8000/api/schema/redoc/
- **OpenAPI Schema:** http://localhost:8000/api/schema/

### Endpoints اصلی

#### Authentication
```
POST   /api/accounts/register/          # ثبت‌نام
POST   /api/accounts/login/             # ورود
POST   /api/accounts/logout/            # خروج
POST   /api/accounts/token/refresh/     # بازیابی token
POST   /api/accounts/password-reset/    # بازیابی رمز عبور
GET    /api/accounts/profile/           # پروفایل کاربر
PATCH  /api/accounts/profile/           # به‌روزرسانی پروفایل
```

#### Tasks
```
GET    /api/tasks/tasks/                # لیست تسک‌ها
POST   /api/tasks/tasks/                # ایجاد تسک
GET    /api/tasks/tasks/{id}/           # جزئیات تسک
PATCH  /api/tasks/tasks/{id}/           # به‌روزرسانی تسک
DELETE /api/tasks/tasks/{id}/           # حذف تسک
GET    /api/tasks/tasks/{id}/history/   # تاریخچه تسک
POST   /api/tasks/tasks/{id}/restore/   # بازیابی تسک
GET    /api/tasks/tasks/statistics/     # آمار تسک‌ها
POST   /api/tasks/tasks/bulk_update/    # به‌روزرسانی دسته‌جمعی
POST   /api/tasks/tasks/bulk_delete/    # حذف دسته‌جمعی
```

---

## 🧪 تست (Test Coverage 85%+)

### Backend Tests
```bash
cd backend

# اجرای تمام تست‌ها
pytest

# با coverage report
pytest --cov=. --cov-report=html --cov-report=term-missing

# فقط یک app
pytest accounts/tests/
pytest tasks/tests/

# Coverage threshold: 85%
```

### Frontend Tests
```bash
cd frontend

# Unit & Integration tests
npm run test

# Watch mode
npm run test:watch

# Coverage report
npm run test:coverage

# E2E tests
npm run test:e2e

# E2E UI mode
npm run test:e2e:ui

# Coverage threshold: 80%
```

### CI/CD Pipeline
```yaml
Backend:
  ✓ Lint (flake8, black, isort)
  ✓ Type check (mypy)
  ✓ Unit tests (pytest)
  ✓ Coverage check (85%+)
  ✓ Security scan (bandit, safety)

Frontend:
  ✓ Lint (ESLint)
  ✓ Type check (TypeScript)
  ✓ Format (Prettier)
  ✓ Unit tests (Vitest)
  ✓ Coverage check (80%+)
  ✓ Build verification
  ✓ E2E tests (Playwright)

Security:
  ✓ Trivy vulnerability scan
  ✓ Dependency audit
```

---

## 🎨 Code Quality Standards

### Backend (Python)
```bash
# Formatting
black --line-length=100 .
isort --profile=black .

# Linting
flake8 --max-line-length=100 --exclude=migrations

# Type checking
mypy . --exclude migrations

# Security
bandit -r . --exclude=tests
safety check
```

### Frontend (TypeScript)
```bash
# Linting
npm run lint
npm run lint:fix

# Type checking
npm run type-check

# Formatting
npm run format
```

---

## 👥 مشارکت

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: Add some amazing feature'`)
4. Run tests (`pytest` and `npm test`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

**Commit Convention:** ما از [Conventional Commits](https://www.conventionalcommits.org/) استفاده می‌کنیم:
- `feat:` - ویژگی جدید
- `fix:` - رفع باگ
- `docs:` - تغییرات مستندات
- `style:` - تغییرات formatting
- `refactor:` - refactoring کد
- `test:` - افزودن تست
- `chore:` - تغییرات build tools

---

## 📝 لایسنس

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.

---

## 👤 سازنده

**Mohammad Reza**
- GitHub: [@mhmdrz22](https://github.com/mhmdrz22)
- Email: mhmdrdaqnbry2025@gmail.com

---

## 🙏 تشکر

این پروژه با استفاده از کتابخانه‌ها و ابزارهای عالی open-source ساخته شده است:
- Django & Django REST Framework
- React & TypeScript
- shadcn/ui & Tailwind CSS
- TanStack Query
- PostgreSQL & Redis
- Docker
- و خیلی دیگر...

---

## 📈 Roadmap

### Phase 1 (Current) ✅
- [x] Core task management
- [x] Authentication & authorization
- [x] Comprehensive testing
- [x] Docker deployment
- [x] CI/CD pipeline

### Phase 2 (Coming Soon)
- [ ] Real-time notifications (WebSocket)
- [ ] Task comments & collaboration
- [ ] File attachments
- [ ] Email notifications
- [ ] Advanced analytics dashboard

### Phase 3 (Future)
- [ ] Team workspaces
- [ ] Mobile app (React Native)
- [ ] Task templates
- [ ] Recurring tasks
- [ ] Calendar view integration
- [ ] Third-party integrations (Slack, Discord)

---

## 🌟 چرا این پروژه؟

این پروژه نشان‌دهنده:
- ✅ **معماری حرفه‌ای**: Low coupling, high cohesion, SOLID principles
- ✅ **کیفیت کد**: 85%+ test coverage، linting، type safety
- ✅ **Best Practices**: Clean code، design patterns، comprehensive docs
- ✅ **Production Ready**: Security، performance، scalability، monitoring
- ✅ **Modern Stack**: جدیدترین تکنولوژی‌ها و best practices

**این فقط یک TODO app نیست - این یک نمونه از software engineering حرفه‌ای است.** 🚀

---

<div align="center">
  <strong>ساخته شده با ❤️ و توجه به جزئیات در ایران</strong>
  <br><br>
  <em>"Code is like humor. When you have to explain it, it's bad." - Cory House</em>
</div>
