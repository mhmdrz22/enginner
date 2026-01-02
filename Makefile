.PHONY: help setup dev test test-coverage clean build up down logs

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m # No Color

help: ## Show this help message
	@echo '$(GREEN)Available commands:$(NC)'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'

setup: ## Initial setup - install pre-commit hooks
	@echo "$(GREEN)Installing pre-commit hooks...$(NC)"
	pip install pre-commit
	pre-commit install
	pre-commit install --hook-type commit-msg
	@echo "$(GREEN)Creating secrets baseline...$(NC)"
	detect-secrets scan > .secrets.baseline || true
	@echo "$(GREEN)Setup complete!$(NC)"

dev: ## Start development environment
	@echo "$(GREEN)Starting development environment...$(NC)"
	docker-compose up --build

up: ## Start all services in detached mode
	@echo "$(GREEN)Starting services...$(NC)"
	docker-compose up -d

down: ## Stop all services
	@echo "$(YELLOW)Stopping services...$(NC)"
	docker-compose down

logs: ## Show logs from all services
	docker-compose logs -f

build: ## Build all Docker images
	@echo "$(GREEN)Building Docker images...$(NC)"
	docker-compose build

test: ## Run all tests
	@echo "$(GREEN)Running backend tests...$(NC)"
	docker-compose exec backend python manage.py test
	@echo "$(GREEN)Running frontend tests...$(NC)"
	docker-compose exec frontend npm test || true

test-coverage: ## Run tests with coverage report
	@echo "$(GREEN)Running backend tests with coverage...$(NC)"
	docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
	docker-compose -f docker-compose.test.yml down

pre-commit-run: ## Run pre-commit on all files
	@echo "$(GREEN)Running pre-commit checks...$(NC)"
	pre-commit run --all-files

security-check: ## Run security checks
	@echo "$(GREEN)Running security scans...$(NC)"
	@echo "$(YELLOW)Bandit (Python security)...$(NC)"
	cd backend && bandit -r . -ll || true
	@echo "$(YELLOW)Safety (dependency check)...$(NC)"
	cd backend && safety check --file requirements.txt || true
	@echo "$(YELLOW)Trivy (Docker scan)...$(NC)"
	trivy fs . || true

migrations: ## Create and apply database migrations
	@echo "$(GREEN)Creating migrations...$(NC)"
	docker-compose exec backend python manage.py makemigrations
	@echo "$(GREEN)Applying migrations...$(NC)"
	docker-compose exec backend python manage.py migrate

superuser: ## Create Django superuser
	@echo "$(GREEN)Creating superuser...$(NC)"
	docker-compose exec backend python manage.py createsuperuser

shell-backend: ## Open Django shell
	docker-compose exec backend python manage.py shell

shell-db: ## Open PostgreSQL shell
	docker-compose exec db psql -U postgres -d taskboard

clean: ## Clean up containers, volumes, and temp files
	@echo "$(RED)Cleaning up...$(NC)"
	docker-compose down -v
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
	find . -type d -name htmlcov -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '.coverage' -delete
	@echo "$(GREEN)Cleanup complete!$(NC)"

format: ## Format code with black and prettier
	@echo "$(GREEN)Formatting Python code...$(NC)"
	cd backend && black .
	cd backend && isort .
	@echo "$(GREEN)Formatting frontend code...$(NC)"
	cd frontend && npm run format || true

lint: ## Run linters
	@echo "$(GREEN)Linting Python code...$(NC)"
	cd backend && flake8 .
	@echo "$(GREEN)Linting frontend code...$(NC)"
	cd frontend && npm run lint || true

prod-check: ## Pre-production checklist
	@echo "$(YELLOW)Running pre-production checks...$(NC)"
	@echo "$(YELLOW)1. Checking for secrets...$(NC)"
	detect-secrets scan || true
	@echo "$(YELLOW)2. Running security scans...$(NC)"
	make security-check
	@echo "$(YELLOW)3. Running tests...$(NC)"
	make test
	@echo "$(YELLOW)4. Checking Docker images...$(NC)"
	docker-compose build
	@echo "$(GREEN)Pre-production checks complete!$(NC)"
