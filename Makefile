.PHONY: help setup start stop clean test lint

help:
	@echo "Available commands:"
	@echo "  make setup      - Set up the development environment"
	@echo "  make start     - Start all services"
	@echo "  make stop      - Stop all services"
	@echo "  make clean     - Clean up the project"
	@echo "  make test      - Run tests"
	@echo "  make lint      - Run linting"

setup:
	@echo "Setting up development environment..."
	cd backend && python -m venv .venv
	cd backend && source .venv/bin/activate && pip install -r requirements.txt
	cd frontend && npm install
	cp .env.example .env

start:
	@echo "Starting services..."
	docker-compose up -d

stop:
	@echo "Stopping services..."
	docker-compose down

clean:
	@echo "Cleaning up..."
	docker-compose down -v
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	rm -rf backend/.venv
	rm -rf frontend/node_modules
	rm -rf frontend/build

test:
	@echo "Running tests..."
	cd backend && source .venv/bin/activate && pytest
	cd frontend && npm test

lint:
	@echo "Running linting..."
	cd backend && source .venv/bin/activate && ruff check . && ruff format .
	cd frontend && npm run lint 