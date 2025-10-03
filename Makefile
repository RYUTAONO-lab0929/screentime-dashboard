SHELL := /bin/bash

export COMPOSE_PROJECT_NAME := screentime

.PHONY: up down logs build seed test fmt migrate openapi backend-test frontend-build

up:
	docker compose --env-file .env.sample up -d --build

stop:
	docker compose down

logs:
	docker compose logs -f --tail 200

migrate:
	docker compose exec api alembic upgrade head || true

seed:
	docker compose exec api python tools/seed_synthetic.py

backend-test:
	docker compose exec api pytest -q

frontend-build:
	docker compose exec web npm run build

fmt:
	docker compose exec api ruff check --fix || true

test: backend-test

openapi:
	docker compose exec api python tools/export_openapi.py
