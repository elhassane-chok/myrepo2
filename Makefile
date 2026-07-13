.PHONY: dev dev-backend dev-frontend install install-backend install-frontend build test lint clean docker-up docker-down

install: install-backend install-frontend

install-backend:
	cd backend && pip install -r requirements.txt

install-frontend:
	cd frontend && npm install

dev-backend:
	cd backend && python wsgi.py

dev-frontend:
	cd frontend && npm run dev

dev:
	@echo "Run 'make dev-backend' and 'make dev-frontend' in separate terminals"

build:
	cd frontend && npm run build

test:
	cd backend && python -m pytest tests/ -v

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down

clean:
	cd frontend && rm -rf dist node_modules
	cd backend && rm -rf __pycache__ .pytest_cache
