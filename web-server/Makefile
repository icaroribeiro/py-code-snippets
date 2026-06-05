# Ensures targets always execute regardless of local directory states
.PHONY: add-migration start-infra finish-infra run-dev test-dev build test run

MIGRATION_NAME ?= auto_migration

add-migration:
	@beanie new-migration -n $(MIGRATION_NAME) -p src/infrastructure/mongodb/migrations

migrate:
	@echo "Running database migrations..."
	@uv run scripts/run_migrations.py

init-infra:
	@docker-compose up --build -d mongodb redis rabbitmq

shutdown-infra:
	@docker-compose down -v

run-dev:
	@uv run src/main.py

test-dev:
	@uv run pytest

build:
	@docker build -t py-cd-sn:latest -f Dockerfile.multistage .

test: build
	@docker run --rm py-cd-sn:latest uv run pytest

run: build
	@docker run -it --rm py-cd-sn:latest
