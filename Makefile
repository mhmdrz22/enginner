.PHONY: help install pre-commit dev test test-coverage security-check build up down clean logs migrate shell

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

help: ## Show this help message
	@echo '$(BLUE)Available commands:$(NC)'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

# ==============================================================================
# INSTALLATION & SETUP
# ==============================================================================

install: ## Install all dependencies and setup pre-commit hooks
	@echo "$(BLUE)Installing dependencies...$(NC)"
	pip install pre-commit detect-secrets bandit safety
	cd backend && pip install -r requirements.txt -r requirements-dev.txt
	cd frontend && npm install
	@echo "$(GREEN)Dependencies installed successfully!$(NC)"
	@make pre-commit-install

pre-commit-install: ## Install pre-commit hooks
	@echo "$(BLUE)Installing pre-commit hooks...$(NC)"
	pre-commit install
	pre-commit install --hook-type commit-msg
	detect-secrets scan > .secrets.baseline || true
	@echo "$(GREEN)Pre-commit hooks installed!$(NC)"

pre-commit-run: ## Run pre-commit on all files
	@echo "$(BLUE)Running pre-commit checks...$(NC)"
	pre-commit run --all-files

pre-commit-update: ## Update pre-commit hooks to latest versions
	pre-commit autoupdate

# ==============================================================================
# DEVELOPMENT ENVIRONMENT
# ==============================================================================

dev: ## Start development environment
	@echo "$(BLUE)Starting development environment...$(NC)"
	docker-compose -f docker-compose.local.yml up --build

dev-detached: ## Start development environment in detached mode
	@echo "$(BLUE)Starting development environment (detached)...$(NC)"
	docker-compose -f docker-compose.local.yml up -d --build

dev-down: ## Stop development environment
	@echo "$(YELLOW)Stopping development environment...$(NC)"
	docker-compose -f docker-compose.local.yml down

dev-logs: ## Show logs from development environment
	docker-compose -f docker-compose.local.yml logs -f

dev-shell-backend: ## Open shell in development backend container
	docker-compose -f docker-compose.local.yml exec backend sh

dev-shell-frontend: ## Open shell in development frontend container
	docker-compose -f docker-compose.local.yml exec frontend sh

# ==============================================================================
# TESTING
# ==============================================================================

test: ## Run all tests
	@echo "$(BLUE)Running tests...$(NC)"
	docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
	docker-compose -f docker-compose.test.yml down

test-backend: ## Run backend tests only
	@echo "$(BLUE)Running backend tests...$(NC)"
	cd backend && pytest -v

test-frontend: ## Run frontend tests only
	@echo "$(BLUE)Running frontend tests...$(NC)"
	cd frontend && npm test

test-coverage: ## Run tests with coverage report
	@echo "$(BLUE)Running tests with coverage...$(NC)"
	cd backend && pytest --cov=. --cov-report=html --cov-report=term --cov-report=xml
	@echo "$(GREEN)Coverage report generated in backend/htmlcov/index.html$(NC)"

test-watch: ## Run tests in watch mode
	cd backend && pytest-watch

# ==============================================================================
# SECURITY & CODE QUALITY
# ==============================================================================

security-check: ## Run all security checks
	@echo "$(BLUE)Running security checks...$(NC)"
	@make bandit
	@make safety
	@make npm-audit
	@echo "$(GREEN)Security checks completed!$(NC)"

bandit: ## Run bandit security scanner on backend
	@echo "$(BLUE)Running Bandit security scanner...$(NC)"
	bandit -r backend/ -ll -x backend/tests,backend/migrations

safety: ## Check for known security vulnerabilities in Python packages
	@echo "$(BLUE)Checking Python dependencies for vulnerabilities...$(NC)"
	safety check --file backend/requirements.txt --full-report

npm-audit: ## Check for vulnerabilities in npm packages
	@echo "$(BLUE)Auditing npm packages...$(NC)"
	cd frontend && npm audit

npm-audit-fix: ## Automatically fix npm vulnerabilities
	@echo "$(YELLOW)Attempting to fix npm vulnerabilities...$(NC)"
	cd frontend && npm audit fix

lint-backend: ## Run linting on backend code
	@echo "$(BLUE)Linting backend code...$(NC)"
	cd backend && flake8 . --exclude=migrations,venv,env
	cd backend && black --check .
	cd backend && isort --check-only .

lint-frontend: ## Run linting on frontend code
	@echo "$(BLUE)Linting frontend code...$(NC)"
	cd frontend && npm run lint

format-backend: ## Format backend code
	@echo "$(BLUE)Formatting backend code...$(NC)"
	cd backend && black .
	cd backend && isort .

format-frontend: ## Format frontend code
	@echo "$(BLUE)Formatting frontend code...$(NC)"
	cd frontend && npm run format

# ==============================================================================
# DATABASE
# ==============================================================================

migrate: ## Run database migrations
	@echo "$(BLUE)Running migrations...$(NC)"
	docker-compose -f docker-compose.local.yml exec backend python manage.py migrate

makemigrations: ## Create new migrations
	@echo "$(BLUE)Creating migrations...$(NC)"
	docker-compose -f docker-compose.local.yml exec backend python manage.py makemigrations

db-shell: ## Open database shell
	docker-compose -f docker-compose.local.yml exec backend python manage.py dbshell

db-reset: ## Reset database (WARNING: Destroys all data)
	@echo "$(RED)WARNING: This will destroy all database data!$(NC)"
	@read -p "Are you sure? (yes/no): " confirm && [ "$$confirm" = "yes" ] || (echo "Aborted" && exit 1)
	docker-compose -f docker-compose.local.yml down -v
	docker-compose -f docker-compose.local.yml up -d db
	sleep 5
	docker-compose -f docker-compose.local.yml up -d backend
	@make migrate

# ==============================================================================
# PRODUCTION
# ==============================================================================

prod-check: ## Check production readiness
	@echo "$(BLUE)Checking production readiness...$(NC)"
	@echo "$(YELLOW)Verifying security settings...$(NC)"
	@if [ -f .env ]; then \
		echo "$(RED)ERROR: .env file exists! Remove it before production deployment$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)✓ No .env file found$(NC)"
	@echo "$(YELLOW)Checking for secrets in code...$(NC)"
	detect-secrets scan --baseline .secrets.baseline
	@echo "$(GREEN)✓ No secrets detected$(NC)"
	@make security-check
	@echo "$(GREEN)Production readiness check completed!$(NC)"

prod-build: prod-check ## Build production images
	@echo "$(BLUE)Building production images...$(NC)"
	docker-compose -f docker-compose.prod.yml build

prod-up: ## Start production environment (WARNING: USE ONLY WHEN READY)
	@echo "$(RED)⚠️  PRODUCTION MODE$(NC)"
	@echo "$(YELLOW)Please verify:$(NC)"
	@echo "1. .env.production file exists with correct values"
	@echo "2. SSL certificates are in place"
	@echo "3. Backup strategy is active"
	@echo "4. All security checks passed"
	@read -p "Continue? (yes/no): " confirm && [ "$$confirm" = "yes" ] || (echo "Aborted" && exit 1)
	docker-compose -f docker-compose.prod.yml up -d

prod-down: ## Stop production environment
	@echo "$(YELLOW)Stopping production environment...$(NC)"
	docker-compose -f docker-compose.prod.yml down

prod-logs: ## Show production logs
	docker-compose -f docker-compose.prod.yml logs -f

# ==============================================================================
# DOCKER MANAGEMENT
# ==============================================================================

build: ## Build all Docker images
	docker-compose build

up: ## Start all services
	docker-compose up

down: ## Stop all services
	docker-compose down

clean: ## Remove all containers, volumes, and images
	@echo "$(RED)WARNING: This will remove all containers, volumes, and images!$(NC)"
	@read -p "Are you sure? (yes/no): " confirm && [ "$$confirm" = "yes" ] || (echo "Aborted" && exit 1)
	docker-compose down -v --rmi all
	logs: ## Show logs from all services
	docker-compose logs -f

ps: ## Show running containers
	docker-compose ps

# ==============================================================================
# UTILITIES
# ==============================================================================

createsuperuser: ## Create Django superuser
	docker-compose -f docker-compose.local.yml exec backend python manage.py createsuperuser

collectstatic: ## Collect static files
	docker-compose exec backend python manage.py collectstatic --noinput

shell: ## Open Django shell
	docker-compose -f docker-compose.local.yml exec backend python manage.py shell

update-deps: ## Update all dependencies (check first, don't auto-update)
	@echo "$(BLUE)Checking for outdated Python packages...$(NC)"
	cd backend && pip list --outdated
	@echo "$(BLUE)Checking for outdated npm packages...$(NC)"
	cd frontend && npm outdated
	@echo "$(YELLOW)Review the list above and update manually if needed$(NC)"

backup-db: ## Backup database
	@echo "$(BLUE)Backing up database...$(NC)"
	mkdir -p backups
	docker-compose exec -T db pg_dump -U $${POSTGRES_USER:-taskboard_user} $${POSTGRES_DB:-taskboard_db} > backups/db_backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "$(GREEN)Database backup created in backups/$(NC)"

restore-db: ## Restore database from backup (specify file with FILE=path/to/backup.sql)
	@if [ -z "$(FILE)" ]; then \
		echo "$(RED)ERROR: Please specify backup file with FILE=path/to/backup.sql$(NC)"; \
		exit 1; \
	fi
	@echo "$(YELLOW)Restoring database from $(FILE)...$(NC)"
	docker-compose exec -T db psql -U $${POSTGRES_USER:-taskboard_user} $${POSTGRES_DB:-taskboard_db} < $(FILE)
	@echo "$(GREEN)Database restored!$(NC)"

# ==============================================================================
# DEFAULT
# ==============================================================================

.DEFAULT_GOAL := help
