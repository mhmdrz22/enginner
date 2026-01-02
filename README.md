# 🚀 TaskBoard - Team Task Management System

> A complete full-stack task management application built with Django REST Framework and React, featuring authentication, real-time updates, and async email notifications.

[![CI/CD](https://github.com/mhmdrz22/enginner/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/mhmdrz22/enginner/actions)
[![codecov](https://codecov.io/gh/mhmdrz22/enginner/branch/main/graph/badge.svg)](https://codecov.io/gh/mhmdrz22/enginner)

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Testing](#-testing)
- [Deployment](#-deployment)

---

## ✨ Features

### Core Features
- ✅ **User Authentication** - Email-based registration and login with token auth
- ✅ **Task Management** - CRUD operations for tasks with status tracking
- ✅ **User Isolation** - Each user can only see and manage their own tasks
- ✅ **Priority & Status** - Organize tasks by priority (HIGH/MEDIUM/LOW) and status (TODO/DOING/DONE)
- ✅ **Responsive UI** - Modern React interface with Tailwind CSS

### Admin Panel (New! 🎉)
- ✅ **User Overview** - See all users with task statistics
- ✅ **Email Notifications** - Send emails to selected users
- ✅ **Async Processing** - Celery + Redis for background email sending
- ✅ **Markdown Support** - Rich text formatting in email messages

### DevOps
- ✅ **Docker** - Fully containerized with docker-compose
- ✅ **CI/CD** - Automated testing and deployment with GitHub Actions
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

- Docker & Docker Compose installed
- Git

### Installation

```bash
# 1. Clone repository
git clone https://github.com/mhmdrz22/enginner.git
cd enginner

# 2. Copy environment file
cp .env.example .env

# 3. Start all services
docker-compose up --build
```

Wait 2-3 minutes for all services to start, then access:

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000/api/
- **Swagger Docs:** http://localhost:8000/swagger/
- **Admin Panel:** http://localhost:8000/admin/

### Create Admin User

```bash
docker-compose exec backend python manage.py createsuperuser
```

---

## 📁 Project Structure

```
enginner/
├── backend/
│   ├── accounts/           # User authentication
│   │   ├── models.py       # User model
│   │   ├── views.py        # Auth & admin endpoints
│   │   ├── tasks.py        # Celery email tasks
│   │   └── tests/          # 25+ tests
│   ├── tasks/              # Task management
│   │   ├── models.py       # Task model
│   │   ├── views.py        # Task CRUD API
│   │   └── tests/          # 30+ tests
│   ├── config/
│   │   ├── settings.py     # Django settings
│   │   ├── celery.py       # Celery config
│   │   └── urls.py         # URL routing + Swagger
│   ├── tests/              # Integration tests
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/            # API calls (axios)
│   │   ├── components/     # Reusable components
│   │   ├── context/        # Auth context
│   │   ├── pages/          # Page components
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   └── AdminPanel.jsx
│   │   ├── App.jsx         # Routing
│   │   └── main.jsx        # Entry point
│   ├── Dockerfile
│   └── package.json
├── nginx/                  # Nginx configs
├── .github/
│   └── workflows/
│       └── ci-cd.yml       # CI/CD pipeline
├── docker-compose.yml      # Development setup
├── docker-compose.prod.yml # Production setup
└── README.md
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
# With Docker
docker-compose exec backend python manage.py test

# Or with pytest
docker-compose exec backend pytest

# With coverage
docker-compose exec backend pytest --cov --cov-report=html
```

### Test Coverage

- **Overall:** 85%+
- **Models:** 90%+
- **Views/APIs:** 85%+
- **Total Tests:** 90+

View coverage report:
```bash
open backend/htmlcov/index.html
```

See [TESTING.md](backend/TESTING.md) for detailed testing guide.

---

## 🐳 Docker Services

### Services Overview

| Service | Port | Description |
|---------|------|-------------|
| **frontend** | 3000 | React app (Nginx) |
| **backend** | 8000 | Django API (Gunicorn) |
| **db** | 5432 | PostgreSQL database |
| **redis** | 6379 | Redis (Celery broker) |
| **celery_worker** | - | Background task processor |

### Docker Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f
docker-compose logs -f backend
docker-compose logs -f celery_worker

# Stop services
docker-compose stop

# Remove everything
docker-compose down -v

# Rebuild
docker-compose up --build
```

See [DOCKER_SETUP.md](DOCKER_SETUP.md) for complete Docker guide.

---

## 🌐 Deployment

### Environment Variables

Create `.env` file:

```env
# Django
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
POSTGRES_DB=taskboard
POSTGRES_USER=postgres
POSTGRES_PASSWORD=strong-password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Redis/Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1

# Email (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@taskboard.com
```

### Deploy to Production

```bash
# Use production docker-compose
docker-compose -f docker-compose.prod.yml up -d --build

# Run migrations
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate

# Create superuser
docker-compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser

# Collect static files
docker-compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --noinput
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment guide.

---

## 📝 Development

### Local Development (without Docker)

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Setup database
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

#### Celery Worker

```bash
cd backend
celery -A config worker --loglevel=info
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Your Name** - [mhmdrz22](https://github.com/mhmdrz22)

---

## 🙏 Acknowledgments

- Malik Ashtar University of Technology
- Software Engineering Course
- Open source community

---

## 📞 Support

- 📧 Email: support@taskboard.com
- 🐛 Issues: [GitHub Issues](https://github.com/mhmdrz22/enginner/issues)
- 📖 Documentation: [Wiki](https://github.com/mhmdrz22/enginner/wiki)

---

**Made with ❤️ for Software Engineering Course**
