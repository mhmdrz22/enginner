# 🚀 TaskBoard - Team Task Management System

> A complete full-stack task management application built with Django REST Framework and React, featuring authentication, real-time updates, and async email notifications.

[![CI/CD](https://github.com/mhmdrz22/enginner/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/mhmdrz22/enginner/actions)
[![codecov](https://codecov.io/gh/mhmdrz22/enginner/branch/main/graph/badge.svg)](https://codecov.io/gh/mhmdrz22/enginner)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

---

## 📚 Documentation

- **[Quick Start Guide](QUICK_START.md)** - راهنمای سریع شروع کار
- **[CI/CD Troubleshooting](CI_CD_TROUBLESHOOTING.md)** - رفع مشکلات Pipeline
- **[Security Checklist](SECURITY.md)** - چک‌لیست امنیتی
- **[Setup Guide](SETUP_GUIDE.md)** - راهنمای نصب کامل

---

## ✨ Features

### Core Features
- ✅ **User Authentication** - Email-based registration and login with token auth
- ✅ **Task Management** - CRUD operations for tasks with status tracking
- ✅ **User Isolation** - Each user can only see and manage their own tasks
- ✅ **Priority & Status** - Organize tasks by priority (HIGH/MEDIUM/LOW) and status (TODO/DOING/DONE)
- ✅ **Responsive UI** - Modern React interface with Tailwind CSS

### Admin Panel
- ✅ **User Overview** - See all users with task statistics
- ✅ **Email Notifications** - Send emails to selected users
- ✅ **Async Processing** - Celery + Redis for background email sending
- ✅ **Markdown Support** - Rich text formatting in email messages

### DevOps & CI/CD
- ✅ **Docker** - Fully containerized with docker-compose
- ✅ **CI/CD** - Automated testing and deployment with GitHub Actions
- ✅ **Pre-commit Hooks** - Code quality checks before commits
- ✅ **Security Scanning** - Trivy, Bandit, Safety checks
- ✅ **API Documentation** - Interactive Swagger/ReDoc docs
- ✅ **90+ Tests** - Comprehensive test coverage

---

## 🛠 Tech Stack

### Backend
- **Django 4.2** - Python web framework
- **Django REST Framework** - RESTful API
- **PostgreSQL** - Primary database
- **Redis** - Message broker for Celery
- **Celery** - Async task queue
- **drf-yasg** - API documentation

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **Tailwind CSS** - Styling

### DevOps
- **Docker & Docker Compose** - Containerization
- **GitHub Actions** - CI/CD pipeline
- **Nginx** - Reverse proxy (production)
- **Gunicorn** - WSGI server

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Git
- Make (optional)

### Installation

```bash
# 1. Clone repository
git clone https://github.com/mhmdrz22/enginner.git
cd enginner

# 2. Copy environment file
cp .env.example .env

# 3. Start with Makefile (recommended)
make setup  # Install pre-commit hooks
make dev    # Start development environment

# OR with Docker Compose
docker-compose up --build

# 4. Create superuser
make superuser
# OR
docker-compose exec backend python manage.py createsuperuser
```

### Access Services

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000/api/
- **Admin Panel:** http://localhost:8000/admin/
- **Swagger Docs:** http://localhost:8000/swagger/
- **ReDoc:** http://localhost:8000/redoc/

**For detailed instructions, see [QUICK_START.md](QUICK_START.md)**

---

## 📁 Project Structure

```
enginner/
├── backend/                # Django backend
│   ├── accounts/          # User authentication
│   ├── tasks/             # Task management
│   ├── config/            # Django settings & config
│   ├── requirements.txt   # Python dependencies
│   └── Dockerfile         # Backend Docker image
├── frontend/               # React frontend
│   ├── src/               # Source code
│   ├── package.json       # Node dependencies
│   └── Dockerfile         # Frontend Docker image
├── .github/
│   └── workflows/
│       └── ci-cd.yml      # CI/CD pipeline
├── docker-compose.yml      # Development setup
├── docker-compose.test.yml # Testing environment
├── docker-compose.prod.yml # Production setup
├── Makefile                # Useful commands
├── .pre-commit-config.yaml # Code quality hooks
└── README.md               # This file
```

---

## 📚 API Documentation

### Access Documentation

- **Swagger UI:** http://localhost:8000/swagger/
- **ReDoc:** http://localhost:8000/redoc/

### Main Endpoints

#### Authentication
```
POST   /api/accounts/register/    - User registration
POST   /api/accounts/login/       - User login
GET    /api/accounts/profile/     - Get user profile
PATCH  /api/accounts/profile/     - Update profile
```

#### Tasks
```
GET    /api/tasks/                - List user's tasks
POST   /api/tasks/                - Create task
GET    /api/tasks/{id}/           - Get task detail
PATCH  /api/tasks/{id}/           - Update task
DELETE /api/tasks/{id}/           - Delete task
```

#### Admin Panel
```
GET    /api/accounts/admin/overview/   - Get users & stats (Admin only)
POST   /api/accounts/admin/notify/     - Send email notifications (Admin only)
```

---

## 🧪 Testing

### Run All Tests

```bash
# With Makefile
make test

# With coverage report
make test-coverage

# Or directly
docker-compose exec backend python manage.py test
```

### Test Coverage

- **Overall:** 85%+
- **Models:** 90%+
- **Views/APIs:** 85%+
- **Total Tests:** 90+

---

## 🐳 Docker Services

| Service | Port | Description |
|---------|------|-------------|
| **frontend** | 3000 | React app (Nginx) |
| **backend** | 8000 | Django API (Gunicorn) |
| **db** | 5432 | PostgreSQL database |
| **redis** | 6379 | Redis (Celery broker) |
| **celery_worker** | - | Background task processor |

### Useful Commands

```bash
# Start services
make up

# View logs
make logs

# Stop services
make down

# Clean everything
make clean
```

---

## 🔧 Development

### Makefile Commands

Run `make help` to see all available commands:

```bash
make help              # Show all commands
make setup             # Install pre-commit hooks
make dev               # Start development
make test              # Run tests
make test-coverage     # Run tests with coverage
make migrations        # Create and apply migrations
make superuser         # Create Django superuser
make shell-backend     # Open Django shell
make shell-db          # Open PostgreSQL shell
make format            # Format code
make lint              # Run linters
make security-check    # Run security scans
make clean             # Clean up
make prod-check        # Pre-production checklist
```

### Pre-commit Hooks

```bash
# Install
make setup

# Run manually
pre-commit run --all-files

# Skip for urgent commit
git commit -m "message" --no-verify
```

---

## 🌐 Deployment

### Environment Variables

Create `.env` file based on `.env.example`:

```env
# Django
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com

# Database
POSTGRES_DB=taskboard
POSTGRES_USER=postgres
POSTGRES_PASSWORD=strong-password

# Redis/Celery
CELERY_BROKER_URL=redis://redis:6379/0

# Email (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Deploy to Production

```bash
# Use production docker-compose
docker-compose -f docker-compose.prod.yml up -d --build

# Run migrations
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate

# Collect static files
docker-compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --noinput

# Create superuser
docker-compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment guide.

---

## 🔒 Security

### Pre-production Checklist

Run the complete security checklist:

```bash
make prod-check
```

See [SECURITY.md](SECURITY.md) for complete security guidelines.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and checks (`make prod-check`)
5. Commit your changes (`git commit -m 'feat: add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

**Pull Request Template** will guide you through the process.

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Mohammad Reza Daghanbari** - [mhmdrz22](https://github.com/mhmdrz22)

---

## 🙏 Acknowledgments

- Malik Ashtar University of Technology
- Software Engineering Course
- Open source community

---

## 📞 Support

- 🐛 **Issues:** [GitHub Issues](https://github.com/mhmdrz22/enginner/issues)
- 📚 **Documentation:** [Wiki](https://github.com/mhmdrz22/enginner/wiki)
- 🚀 **Quick Start:** [QUICK_START.md](QUICK_START.md)

---

## 📈 Project Status

- ✅ Development environment ready
- ✅ CI/CD pipeline configured
- ✅ Pre-commit hooks active
- ✅ Security scanning enabled
- ✅ Tests with 85%+ coverage
- ⏳ Production deployment pending

---

**Made with ❤️ for Software Engineering Course**
