.PHONY: add-migration start-infra finish-infra run-dev test-dev build test run

MIGRATION_NAME ?= auto_migration

add-migration:
	@beanie new-migration -n $(MIGRATION_NAME) -p src/infrastructure/mongodb/migrations

migrate:
	@PYTHONPATH=src uv run python -m scripts/run_migrations.py

init-infra:
	@docker-compose up --build -d mongodb redis rabbitmq

shutdown-infra:
	@docker-compose down -v

dev:
	@PYTHONPATH=src uv run python -m uvicorn src.main:app --reload --reload-dir src --reload-include '*.json'

worker:
	@PYTHONPATH=src uv run python -m celery -A src.infrastructure.celery worker --loglevel=info -P solo --without-mingle --without-gossip

test-dev:
	@uv run pytest

build:
	@docker build -t py-cd-sn:latest -f Dockerfile.multistage .

test: build
	@docker run --rm py-cd-sn:latest uv run pytest

prod: build
	@docker run -it --rm py-cd-sn:latest

remove-pycache:
	@export PYTHONDONTWRITEBYTECODE=1
	@find . -type d -name "__pycache__" -exec rm -rf {} +

help:
	@echo "Available commands:"
	@echo "make X: to be defined..."
