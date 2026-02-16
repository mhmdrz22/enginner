# 🚀 TaskBoard - Team Task Management System

> A complete full-stack task management application built with Django REST Framework and modern React, featuring authentication, real-time updates, Kanban boards, and comprehensive permission system.

[![CI/CD](https://github.com/mhmdrz22/enginner/actions/workflows/production-pipeline.yml/badge.svg)](https://github.com/mhmdrz22/enginner/actions)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-blue.svg)](https://www.typescriptlang.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

---

## 📚 Documentation

- **[Quick Start Guide](QUICK_START.md)** - راهنمای سریع شروع کار
- **[Frontend README](frontend/README.md)** - مستندات کامل Frontend
- **[CI/CD Troubleshooting](CI_CD_TROUBLESHOOTING.md)** - رفع مشکلات Pipeline
- **[Security Checklist](SECURITY.md)** - چک‌لیست امنیتی
- **[API Endpoints](backend/API_ENDPOINTS.md)** - مستندات کامل API

---

## ✨ Features

### 🎨 Modern UI/UX
- ✅ **Professional Design** - shadcn/ui component library with Tailwind CSS
- ✅ **Dark Mode** - Full dark/light/system theme support
- ✅ **Responsive Design** - Mobile-first with desktop optimizations
- ✅ **Smooth Animations** - Polished transitions and interactions
- ✅ **Toast Notifications** - User-friendly feedback system

### 📋 Task Management
- ✅ **Kanban Board** - Visual drag-and-drop task organization
- ✅ **Task Cards** - Display priority, due date, tags, status
- ✅ **Advanced Filters** - Filter by status, priority with 8 sort options
- ✅ **Real-time Search** - Instant task search with debouncing
- ✅ **Task History** - Complete audit trail of changes
- ✅ **Bulk Operations** - Update or delete multiple tasks at once
- ✅ **Soft Delete** - Recoverable task deletion

### 🔐 Authentication & Authorization
- ✅ **Email-based Auth** - JWT authentication with auto token refresh
- ✅ **Protected Routes** - Route guards for secure pages
- ✅ **Permission System** - Role-based access control (RBAC)
- ✅ **Resource Ownership** - Users can only access their own data
- ✅ **Admin Privileges** - Special access for staff and superusers

### 🎯 User Interface
- ✅ **Desktop Sidebar** - Fixed navigation for easy access
- ✅ **Mobile Menu** - Responsive hamburger menu with overlay
- ✅ **User Avatar** - Dropdown menu with profile and settings
- ✅ **Notification Bell** - Ready for real-time notifications
- ✅ **Loading States** - Skeleton screens and spinners
- ✅ **Error Boundaries** - Graceful error handling

### ⚡ Performance
- ✅ **React Query** - Smart data fetching with caching
- ✅ **Code Splitting** - Configured for lazy loading
- ✅ **Optimistic Updates** - Instant UI feedback
- ✅ **Request Deduplication** - Efficient API calls

### 🔧 Admin Panel
- ✅ **User Overview** - See all users with task statistics
- ✅ **Email Notifications** - Send emails to selected users
- ✅ **Async Processing** - Celery + Redis for background jobs
- ✅ **Markdown Support** - Rich text formatting

### 🛠 DevOps & CI/CD
- ✅ **Docker** - Fully containerized with docker-compose
- ✅ **CI/CD** - Automated testing with GitHub Actions
- ✅ **Pre-commit Hooks** - Code quality checks
- ✅ **Security Scanning** - Trivy, Bandit, Safety
- ✅ **API Documentation** - Interactive Swagger/ReDoc
- ✅ **90+ Tests** - Comprehensive test coverage (85%+)

---

## 🛠 Tech Stack

### Backend
- **Django 4.2** - Python web framework
- **Django REST Framework** - RESTful API
- **PostgreSQL** - Primary database
- **Redis** - Caching & message broker
- **Celery** - Async task queue
- **drf-yasg** - API documentation

### Frontend
- **React 18** - UI library with TypeScript
- **Vite** - Lightning-fast build tool
- **React Query** - Data fetching & caching
- **Zustand** - State management
- **React Router** - Client-side routing
- **shadcn/ui** - Component library (Radix UI)
- **Tailwind CSS** - Utility-first styling
- **React Hook Form + Zod** - Form validation
- **Axios** - HTTP client
- **Lucide React** - Beautiful icons
- **Sonner** - Toast notifications

### Testing
- **Pytest** - Backend testing
- **Vitest** - Frontend unit testing
- **Testing Library** - Component testing
- **Coverage.py** - Code coverage

### DevOps
- **Docker & Docker Compose** - Containerization
- **GitHub Actions** - CI/CD pipeline
- **Nginx** - Reverse proxy
- **Gunicorn** - WSGI server

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for local frontend dev)
- Python 3.11+ (for local backend dev)
- Git

### Installation

```bash
# 1. Clone repository
git clone https://github.com/mhmdrz22/enginner.git
cd enginner

# 2. Copy environment file
cp .env.example .env
cp frontend/.env.example frontend/.env

# 3. Start with Docker Compose
docker-compose up --build

# 4. Create superuser
docker-compose exec backend python manage.py createsuperuser
```

### Local Development (Without Docker)

#### Backend
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Access Services

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000/api/
- **Admin Panel:** http://localhost:8000/admin/
- **Swagger Docs:** http://localhost:8000/swagger/
- **ReDoc:** http://localhost:8000/redoc/

---

## 📁 Project Structure

```
enginner/
├── backend/                    # Django backend
│   ├── accounts/              # User authentication
│   ├── tasks/                 # Task management
│   ├── config/                # Django settings
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── auth/         # Auth components
│   │   │   ├── layout/       # Layout components
│   │   │   ├── tasks/        # Task components
│   │   │   └── ui/           # UI primitives
│   │   ├── hooks/            # Custom hooks
│   │   ├── services/         # API services
│   │   ├── stores/           # Zustand stores
│   │   ├── types/            # TypeScript types
│   │   └── lib/              # Utilities
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── Dockerfile
├── nginx/                      # Nginx config
├── .github/workflows/          # CI/CD
├── docker-compose.yml
├── Makefile
└── README.md
```

---

## 🎯 Permission System

### Defined Permissions

```typescript
VIEW_TASKS      // View task list
CREATE_TASKS    // Create new tasks
UPDATE_TASKS    // Update existing tasks
DELETE_TASKS    // Delete tasks
VIEW_USERS      // View user list (admin)
MANAGE_USERS    // Manage users (superuser)
ACCESS_ADMIN    // Access admin panel
MANAGE_SETTINGS // Manage system settings
```

### Role Hierarchy

| Role | Permissions |
|------|-------------|
| **Guest** | None |
| **User** | VIEW_TASKS, CREATE_TASKS, UPDATE_TASKS, DELETE_TASKS (own tasks only) |
| **Staff** | User permissions + VIEW_USERS, ACCESS_ADMIN |
| **Superuser** | All permissions |

### Usage Examples

#### Protected Routes
```tsx
<Route path="/dashboard" element={
  <PrivateRoute><Dashboard /></PrivateRoute>
} />

<Route path="/admin" element={
  <AdminRoute><AdminPanel /></AdminRoute>
} />
```

#### Component Guards
```tsx
<PermissionGuard permission={Permission.DELETE_TASKS}>
  <DeleteButton />
</PermissionGuard>

<AdminGuard>
  <AdminFeature />
</AdminGuard>
```

---

## 📚 API Documentation

### Access Documentation

- **Swagger UI:** http://localhost:8000/swagger/
- **ReDoc:** http://localhost:8000/redoc/
- **Complete Docs:** [backend/API_ENDPOINTS.md](backend/API_ENDPOINTS.md)

### Main Endpoints

#### Authentication
```
POST   /api/accounts/register/    - User registration
POST   /api/accounts/login/       - User login (returns JWT)
GET    /api/accounts/profile/     - Get user profile
PATCH  /api/accounts/profile/     - Update profile
POST   /api/accounts/logout/      - User logout
POST   /api/accounts/token/refresh/ - Refresh JWT token
```

#### Tasks
```
GET    /api/tasks/                - List user's tasks (with filters)
POST   /api/tasks/                - Create task
GET    /api/tasks/{id}/           - Get task detail
PATCH  /api/tasks/{id}/           - Update task
DELETE /api/tasks/{id}/           - Soft delete task
POST   /api/tasks/{id}/restore/   - Restore deleted task
GET    /api/tasks/{id}/history/   - Get task change history
```

#### Admin
```
GET    /api/admin/overview/       - Get users & stats (Admin only)
POST   /api/admin/notify/         - Send email notifications (Admin only)
```

---

## 🧪 Testing

### Backend Tests

```bash
# Run all tests
docker-compose exec backend python manage.py test

# With coverage
make test-coverage
```

### Frontend Tests

```bash
cd frontend

# Run tests
npm test

# With UI
npm run test:ui

# Coverage
npm run test:coverage
```

### Test Coverage
- **Backend:** 85%+ coverage
- **Frontend:** Testing infrastructure ready
- **Total Tests:** 90+ (backend)

---

## 🎨 UI Components

### Available Components

- **Button** - Multiple variants and sizes
- **Input** - Form input with validation
- **Card** - Content containers
- **Dialog** - Modal dialogs
- **Select** - Dropdown selections
- **Badge** - Status indicators
- **Avatar** - User avatars with fallback
- **Dropdown Menu** - Context menus
- **Toast** - Notifications
- **Kanban Board** - Drag-and-drop board
- **Task Card** - Task display
- **Task Filters** - Filter controls
- **Task Search** - Search input
- **Protected Route** - Auth guards
- **Permission Guard** - Permission checks

See [frontend/README.md](frontend/README.md) for complete component documentation.

---

## 🐳 Docker Services

| Service | Port | Description |
|---------|------|-------------|
| **frontend** | 3000 | React app (development) |
| **backend** | 8000 | Django API |
| **db** | 5432 | PostgreSQL |
| **redis** | 6379 | Redis |
| **celery_worker** | - | Background tasks |

---

## 🔧 Development

### Makefile Commands

```bash
make help              # Show all commands
make dev               # Start development
make test              # Run tests
make test-coverage     # Tests with coverage
make migrations        # Create migrations
make superuser         # Create superuser
make shell-backend     # Django shell
make format            # Format code
make lint              # Run linters
make security-check    # Security scans
make clean             # Clean up
```

---

## 🌐 Deployment

See deployment guides:
- [DEPLOYMENT.md](DEPLOYMENT.md) - General deployment
- [DOCKER_SETUP.md](DOCKER_SETUP.md) - Docker production setup

---

## 🔒 Security

- JWT authentication with refresh tokens
- Password hashing with Django's PBKDF2
- CORS configuration
- Rate limiting
- SQL injection protection (Django ORM)
- XSS protection
- CSRF protection
- Security headers in production

See [SECURITY.md](SECURITY.md) for complete security guidelines.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests (`make test`)
5. Commit with conventional commits
6. Open a Pull Request

---

## 📝 License

GPL-3.0 License - see [LICENSE](LICENSE)

---

## 👥 Authors

**Mohammad Reza Daghanbari** - [mhmdrz22](https://github.com/mhmdrz22)

---

## 📈 Project Status

- ✅ Backend API complete
- ✅ Frontend infrastructure complete
- ✅ Authentication & authorization
- ✅ Task management UI
- ✅ Permission system
- ✅ CI/CD pipeline
- ✅ Docker setup
- 🚧 Page implementations (in progress)
- 🚧 Admin dashboard (in progress)
- 🚧 Testing coverage expansion
- 🚀 **60% complete** - Ready for MVP

---

## 📞 Support

- 🐛 **Issues:** [GitHub Issues](https://github.com/mhmdrz22/enginner/issues)
- 📚 **Documentation:** [Wiki](https://github.com/mhmdrz22/enginner/wiki)
- 🚀 **Quick Start:** [QUICK_START.md](QUICK_START.md)

---

**Made with ❤️ for Software Engineering Course**
