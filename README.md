# 📊 Task Manager - سیستم مدیریت تسک

یک سیستم مدیریت تسک مدرن و کامل با Django REST Framework و React + TypeScript

[![License](https://img.shields.io/badge/license-GPL--3.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-4.2+-green.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/react-18+-61dafb.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/typescript-5+-3178c6.svg)](https://www.typescriptlang.org/)

---

## 🌟 ویژگی‌های کلیدی

### 🔐 Authentication & Security
- ✅ JWT Authentication با Access & Refresh Tokens
- ✅ User Registration & Login
- ✅ Password Reset Flow
- ✅ Rate Limiting
- ✅ Token Blacklisting
- ✅ CORS پیکربندی شده

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

### ⚡ Performance
- ✅ Redis Caching
- ✅ Database Query Optimization
- ✅ Lazy Loading & Code Splitting
- ✅ React Query for Data Fetching
- ✅ Optimistic UI Updates

### 🧠 Developer Experience
- ✅ TypeScript برای Type Safety
- ✅ ESLint & Prettier
- ✅ Git Hooks (پیش‌فرض خاموش)
- ✅ Docker & Docker Compose
- ✅ API Documentation (Swagger)
- ✅ Comprehensive Testing

---

## 📦 تکنولوژی‌های استفاده شده

### Backend
- **Framework:** Django 4.2+ & Django REST Framework
- **Database:** PostgreSQL 14+
- **Cache:** Redis 7+
- **Authentication:** JWT (djangorestframework-simplejwt)
- **API Docs:** drf-spectacular (Swagger/OpenAPI)
- **Testing:** pytest, pytest-django, pytest-cov

### Frontend
- **Framework:** React 18+ with TypeScript
- **Build Tool:** Vite
- **UI Library:** shadcn/ui (Radix UI + Tailwind CSS)
- **State Management:** Zustand
- **Data Fetching:** TanStack Query (React Query)
- **Forms:** React Hook Form + Zod
- **Drag & Drop:** dnd-kit
- **Routing:** React Router v6
- **Date Handling:** date-fns
- **Notifications:** react-hot-toast
- **Testing:** Vitest, React Testing Library, Playwright

### DevOps
- **Containerization:** Docker & Docker Compose
- **CI/CD:** GitHub Actions
- **Code Quality:** ESLint, Prettier, Black, isort

---

## 🚀 راه‌اندازی سریع

### پیش‌نیازها

```bash
# Python 3.10+, Node.js 18+, PostgreSQL 14+, Redis 7+
# یا
# Docker & Docker Compose
```

### نصب با Docker (توصیه می‌شود)

```bash
# 1. Clone رپوزیتوری
git clone https://github.com/mhmdrz22/enginner.git
cd enginner

# 2. اجرا با Docker Compose
docker-compose up --build

# 3. اجرای Migrations
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser

# ✅ آماده است!
# Backend: http://localhost:8000
# Frontend: http://localhost:5173
# API Docs: http://localhost:8000/api/schema/swagger/
```

### نصب مستقیم

برای راهنمای کامل [SETUP.md](SETUP.md) را مشاهده کنید.

---

## 📝 ساختار پروژه

```
enginner/
├── backend/
│   ├── accounts/              # مدیریت کاربران
│   │   ├── models.py           # User model
│   │   ├── serializers.py      # User serializers
│   │   ├── views.py            # Auth views
│   │   └── tests/              # تست‌ها
│   ├── tasks/                 # مدیریت تسک‌ها
│   │   ├── models.py           # Task & TaskHistory models
│   │   ├── serializers.py      # Task serializers
│   │   ├── views.py            # Task ViewSets
│   │   ├── filters.py          # Task filters
│   │   └── tests/              # تست‌ها
│   ├── config/                # تنظیمات Django
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   ├── development.py
│   │   │   └── production.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── requirements.txt
│   └── manage.py
│
├── frontend/
│   ├── src/
│   │   ├── components/        # کامپوننت‌ها
│   │   │   ├── ui/             # shadcn/ui components
│   │   │   ├── layout/         # Layout components
│   │   │   └── tasks/          # Task components
│   │   ├── pages/             # صفحات
│   │   │   ├── Login.tsx
│   │   │   ├── Register.tsx
│   │   │   ├── ForgotPassword.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   ├── TasksPage.tsx
│   │   │   ├── TaskDetailPage.tsx
│   │   │   └── ProfilePage.tsx
│   │   ├── services/          # API services
│   │   │   └── api.ts
│   │   ├── store/             # State management
│   │   │   └── authStore.ts
│   │   ├── lib/               # Utilities
│   │   └── App.tsx
│   ├── package.json
│   └── vite.config.ts
│
├── docker-compose.yml
├── .github/
│   └── workflows/
│       ├── backend-tests.yml
│       └── frontend-tests.yml
├── README.md
└── SETUP.md
```

---

## 📚 مستندسازی

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

## 🧠 تست

### Backend Tests
```bash
cd backend

# اجرای تمام تست‌ها
pytest

# با coverage report
pytest --cov=. --cov-report=html

# Coverage: 95%+
```

### Frontend Tests
```bash
cd frontend

# Unit & Integration tests
npm run test

# Coverage report
npm run test:coverage

# E2E tests
npm run test:e2e

# Coverage: 85%+
```

---

## 👥 مشارکت

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

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
- و خیلی دیگر...

---

## 📈 Roadmap

- [ ] Real-time notifications با WebSocket
- [ ] Task comments & collaboration
- [ ] File attachments
- [ ] Email notifications
- [ ] Mobile app (React Native)
- [ ] Advanced analytics & reporting
- [ ] Team workspaces
- [ ] Task templates
- [ ] Recurring tasks
- [ ] Calendar view

---

<div align="center">
  <strong>ساخته شده با ❤️ در ایران</strong>
</div>
