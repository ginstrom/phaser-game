.PHONY: help backend-shell backend test frontend frontend-shell test-frontend run purge-db

# Default target
.DEFAULT_GOAL := help

help: ## Display this help message
	@echo "Space Conquest Game Development Environment"
	@echo ""
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

backend-shell: ## Open an interactive shell in the backend container or run a command if arguments provided
	docker compose -f docker/docker-compose.yml run --rm backend-shell $(filter-out $@,$(MAKECMDGOALS))

frontend-shell: ## Open an interactive shell in the frontend container or run a command if arguments provided
	docker compose -f docker/docker-compose.yml run --rm frontend-shell $(filter-out $@,$(MAKECMDGOALS))

%:
	@:

backend: ## Run the Django development server
	docker compose -f docker/docker-compose.yml up backend

frontend: ## Run the frontend development server
	docker compose -f docker/docker-compose.yml up frontend

run: ## Run both frontend and backend servers
	docker compose -f docker/docker-compose.yml up frontend backend

test: ## Run all tests (backend and frontend)
	@echo "Running all tests..."
	@make test-backend
	@make test-frontend

test-backend: ## Run backend tests
	docker compose -f docker/docker-compose.dev.yml run --rm backend-test

test-frontend: ## Run frontend tests
	docker compose -f docker/docker-compose.dev.yml run --rm frontend-test

purge-db: ## Purge all data from the development database
	@echo "WARNING: This will delete all data from the development database."
	@echo "Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]
	docker compose -f docker/docker-compose.yml run --rm backend-shell python manage.py flush --no-input 