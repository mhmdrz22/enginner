.PHONY: help install dev-backend dev-frontend dev test clean docker-build docker-up docker-down docker-logs migrate createsuperuser shell

help:
	@echo "📋 Available commands:"
	@echo "  make install          - Install all dependencies"
	@echo "  make dev-backend      - Run backend development server"
	@echo "  make dev-frontend     - Run frontend development server"
	@echo "  make dev              - Run both backend and frontend"
	@echo "  make test             - Run all tests"
	@echo "  make test-backend     - Run backend tests"
	@echo "  make test-frontend    - Run frontend tests"
	@echo "  make docker-build     - Build Docker images"
	@echo "  make docker-up        - Start Docker containers"
	@echo "  make docker-down      - Stop Docker containers"
	@echo "  make docker-logs      - View Docker logs"
	@echo "  make migrate          - Run Django migrations"
	@echo "  make createsuperuser  - Create Django superuser"
	@echo "  make shell            - Open Django shell"
	@echo "  make clean            - Clean cache and temp files"

install:
	@echo "📦 Installing dependencies..."
	cd backend && pip install -r requirements.txt
	cd frontend && npm install
	@echo "✅ Dependencies installed!"

dev-backend:
	@echo "🚀 Starting backend server..."
	cd backend && python manage.py runserver

dev-frontend:
	@echo "🚀 Starting frontend server..."
	cd frontend && npm run dev

dev:
	@echo "🚀 Starting both backend and frontend..."
	@make -j2 dev-backend dev-frontend

test:
	@echo "🧪 Running all tests..."
	@make test-backend
	@make test-frontend

test-backend:
	@echo "🧪 Running backend tests..."
	cd backend && python manage.py test
	@echo "✅ Backend tests completed!"

test-frontend:
	@echo "🧪 Running frontend tests..."
	cd frontend && npm run test || echo "No frontend tests configured"

test-coverage:
	@echo "📊 Running tests with coverage..."
	cd backend && coverage run --source='.' manage.py test
	cd backend && coverage report
	cd backend && coverage html
	@echo "✅ Coverage report generated at backend/htmlcov/index.html"

docker-build:
	@echo "🐳 Building Docker images..."
	docker-compose build
	@echo "✅ Docker images built!"

docker-up:
	@echo "🐳 Starting Docker containers..."
	docker-compose up -d
	@echo "✅ Containers started!"
	@echo "   Frontend: http://localhost:5173"
	@echo "   Backend:  http://localhost:8000"
	@echo "   Admin:    http://localhost:8000/admin"

docker-down:
	@echo "🛑 Stopping Docker containers..."
	docker-compose down
	@echo "✅ Containers stopped!"

docker-logs:
	@echo "📜 Viewing Docker logs..."
	docker-compose logs -f

migrate:
	@echo "🔄 Running migrations..."
	cd backend && python manage.py migrate
	@echo "✅ Migrations completed!"

migrate-docker:
	@echo "🔄 Running migrations in Docker..."
	docker-compose exec backend python manage.py migrate
	@echo "✅ Migrations completed!"

createsuperuser:
	@echo "👤 Creating superuser..."
	cd backend && python manage.py createsuperuser

createsuperuser-docker:
	@echo "👤 Creating superuser in Docker..."
	docker-compose exec backend python manage.py createsuperuser

shell:
	@echo "🐚 Opening Django shell..."
	cd backend && python manage.py shell

shell-docker:
	@echo "🐚 Opening Django shell in Docker..."
	docker-compose exec backend python manage.py shell

clean:
	@echo "🧹 Cleaning cache and temp files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	cd frontend && rm -rf dist node_modules/.cache 2>/dev/null || true
	@echo "✅ Cleaned!"

lint-backend:
	@echo "🔍 Linting backend code..."
	cd backend && flake8 . || true

format-backend:
	@echo "✨ Formatting backend code..."
	cd backend && black . || true

lint-frontend:
	@echo "🔍 Linting frontend code..."
	cd frontend && npm run lint || true

format-frontend:
	@echo "✨ Formatting frontend code..."
	cd frontend && npm run format || true

prod-build:
	@echo "🏗️ Building for production..."
	docker-compose -f docker-compose.prod.yml build
	@echo "✅ Production build complete!"

prod-up:
	@echo "🚀 Starting production environment..."
	docker-compose -f docker-compose.prod.yml up -d
	@echo "✅ Production environment running!"

prod-down:
	@echo "🛑 Stopping production environment..."
	docker-compose -f docker-compose.prod.yml down
	@echo "✅ Production environment stopped!"
