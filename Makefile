.PHONY: help build up down logs restart clean db-migrate db-upgrade

help:
	@echo "Comandos disponibles:"
	@echo "  make build       - Construir contenedores"
	@echo "  make up          - Levantar servicios"
	@echo "  make down        - Detener servicios"
	@echo "  make logs        - Ver logs"
	@echo "  make restart     - Reiniciar servicios"
	@echo "  make clean       - Limpiar todo"
	@echo "  make db-migrate  - Crear migración"
	@echo "  make db-upgrade  - Aplicar migraciones"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

restart:
	docker-compose restart

clean:
	docker-compose down -v
	rm -rf backend/uploads/*
	rm -rf backend/__pycache__
	rm -rf frontend/dist

db-migrate:
	docker-compose exec backend alembic revision --autogenerate -m "$(message)"

db-upgrade:
	docker-compose exec backend alembic upgrade head

db-downgrade:
	docker-compose exec backend alembic downgrade -1

backend-shell:
	docker-compose exec backend bash

frontend-shell:
	docker-compose exec frontend sh

test:
	docker-compose exec backend pytest

dev-backend:
	cd backend && uvicorn app.main:app --reload

dev-frontend:
	cd frontend && npm run dev
