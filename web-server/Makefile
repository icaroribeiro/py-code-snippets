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
	@PYTHONPATH=src uv run uvicorn src.main:app \
		--reload \
		--reload-dir src

run:
	@PYTHONPATH=src uv run uvicorn src.main:app \
		--workers 4

test-dev:
	@uv run pytest

build:
	@docker build -t py-cd-sn:latest -f Dockerfile.multistage .

test: build
	@docker run --rm py-cd-sn:latest uv run pytest

run: build
	@docker run -it --rm py-cd-sn:latest

remove-pycache:
	@export PYTHONDONTWRITEBYTECODE=1
	@find . -type d -name "__pycache__" -exec rm -rf {} +
