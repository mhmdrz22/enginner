# GitHub Actions Workflows

این پوشه حاوی تمام workflowهای CI/CD پروژه است.

## 📦 Workflows موجود

### 1. Backend Tests (`backend-tests.yml`)

**زمان اجرا:**
- Push به `main` یا `develop`
- Pull Request به `main` یا `develop`
- فقط وقتی تغییرات در `backend/` باشد

**عملکرد:**
- راه‌اندازی PostgreSQL و Redis
- تست روی Python 3.10, 3.11, 3.12
- اجرای Linting (flake8, black, isort)
- اجرای Migrations
- اجرای تمام تست‌ها با coverage
- آپلود coverage به Codecov
- چک threshold coverage (85%+)

**Badge:**
```markdown
![Backend Tests](https://github.com/mhmdrz22/enginner/workflows/Backend%20Tests/badge.svg)
```

---

### 2. Frontend Tests (`frontend-tests.yml`)

**زمان اجرا:**
- Push به `main` یا `develop`
- Pull Request به `main` یا `develop`
- فقط وقتی تغییرات در `frontend/` باشد

**عملکرد:**
- تست روی Node.js 18.x, 20.x, 22.x
- اجرای ESLint
- Type checking (TypeScript)
- اجرای Unit Tests با coverage
- Build پروژه
- اجرای E2E Tests (Playwright)
- آپلود artifacts

**Badge:**
```markdown
![Frontend Tests](https://github.com/mhmdrz22/enginner/workflows/Frontend%20Tests/badge.svg)
```

---

### 3. CI/CD Pipeline (`ci-cd.yml`)

**زمان اجرا:**
- Push به `main`
- Pull Request به `main`

**عملکرد:**
- اجرای تست‌های Backend
- اجرای تست‌های Frontend
- Build Frontend
- Build Docker Images
- Security Scan (Trivy)
- آماده‌سازی برای Deployment

**Badge:**
```markdown
![CI/CD](https://github.com/mhmdrz22/enginner/workflows/CI/CD%20Pipeline/badge.svg)
```

---

### 4. Code Quality (`code-quality.yml`)

**زمان اجرا:**
- Push به `main` یا `develop`
- Pull Request به `main` یا `develop`

**عملکرد:**

**Backend:**
- Flake8 (PEP8 compliance)
- Black (code formatting)
- isort (import sorting)
- Bandit (security issues)
- Radon (complexity analysis)

**Frontend:**
- ESLint (code quality)
- Prettier (formatting)
- TypeScript type checking
- npm audit (security)

**Badge:**
```markdown
![Code Quality](https://github.com/mhmdrz22/enginner/workflows/Code%20Quality/badge.svg)
```

---

## 🛠️ پیکربندی

### Secrets مورد نیاز

در حال حاضر نیازی به secret نیست. برای فعال‌سازی Codecov:

1. برو به Settings > Secrets and variables > Actions
2. اضافه کن: `CODECOV_TOKEN`

### فعال‌سازی Workflows

Workflowها به طور خودکار بعد از push/PR اجرا می‌شوند.

برای مشاهده وضعیت:
- برو به تب **Actions** در GitHub

---

## 📄 گزارش‌ها

### Coverage Reports
- Backend: `backend/htmlcov/index.html`
- Frontend: `frontend/coverage/index.html`
- Codecov: https://codecov.io/gh/mhmdrz22/enginner

### Artifacts
تمام گزارش‌ها به عنوان artifacts در هر workflow run موجود هستند:
- Coverage reports
- Test results
- Build artifacts
- Security scan results
- E2E screenshots

---

## 🐛 عیب‌یابی

### خطای Backend Tests

```bash
# لوکال تست کنید
cd backend
pytest --cov=. --cov-report=html
```

### خطای Frontend Tests

```bash
# لوکال تست کنید
cd frontend
npm run test
npm run test:e2e
```

### مشاهده Logs

1. برو به Actions tab
2. روی workflow run کلیک کن
3. روی job مورد نظر کلیک کن
4. logs را بررسی کنید

---

## 🚀 اجرای دستی

برای اجرای دستی workflow:

1. برو به Actions > workflow مورد نظر
2. کلیک روی "Run workflow"
3. branch را انتخاب کنید
4. "Run workflow" را کلیک کنید

---

## 📊 Status Badges

برای اضافه کردن به README:

```markdown
[![Backend Tests](https://github.com/mhmdrz22/enginner/workflows/Backend%20Tests/badge.svg)](https://github.com/mhmdrz22/enginner/actions)
[![Frontend Tests](https://github.com/mhmdrz22/enginner/workflows/Frontend%20Tests/badge.svg)](https://github.com/mhmdrz22/enginner/actions)
[![CI/CD](https://github.com/mhmdrz22/enginner/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/mhmdrz22/enginner/actions)
[![Code Quality](https://github.com/mhmdrz22/enginner/workflows/Code%20Quality/badge.svg)](https://github.com/mhmdrz22/enginner/actions)
```

---

## 📝 یادداشت‌ها

- تمام workflowها `continue-on-error: true` دارند تا از فیل شدن pipeline جلوگیری کنند
- PostgreSQL و Redis به صورت service راه‌اندازی می‌شوند
- Coverage threshold: 85%+
- تست روی چند نسخه Python/Node.js
- Artifacts به مدت 7 روز نگهداری می‌شوند
