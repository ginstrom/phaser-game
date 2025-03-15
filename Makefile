.PHONY: help backend-shell backend test

# Default target
.DEFAULT_GOAL := help

help: ## Display this help message
	@echo "Space Conquest Game Development Environment"
	@echo ""
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

backend-shell: ## Open an interactive shell in the backend container or run a command if arguments provided
	docker compose -f docker/docker-compose.yml run --rm backend-shell $(filter-out $@,$(MAKECMDGOALS))

%:
	@:

backend: ## Run the Django development server
	docker compose -f docker/docker-compose.yml up backend

test: ## Run all tests (backend and frontend)
	@echo "Running all tests..."
	@make test-backend
	@echo "Frontend tests not implemented yet"

test-backend: ## Run backend tests
	docker compose -f docker/docker-compose.dev.yml run --rm backend-test

test-frontend: ## Run frontend tests (not implemented)
	@echo "Frontend tests not implemented yet" 