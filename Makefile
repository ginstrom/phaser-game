.PHONY: help backend-shell backend

# Default target
.DEFAULT_GOAL := help

help: ## Display this help message
	@echo "Space Conquest Game Development Environment"
	@echo ""
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

backend-shell: ## Open an interactive shell in the backend container
	docker compose -f docker/docker-compose.yml run --rm backend-shell

backend: ## Run the Django development server
	docker compose -f docker/docker-compose.yml up backend 