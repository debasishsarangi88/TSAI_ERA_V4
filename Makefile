.PHONY: help install install-dev run test clean lint format check

help: ## Show this help message
	@echo "YouTube Audio Waveform Visualizer - Development Commands"
	@echo "======================================================"
	@echo ""
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install production dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -r requirements.txt
	pip install pytest pytest-cov black flake8 mypy

run: ## Run the Flask development server
	python app.py

test: ## Run tests
	pytest tests/ -v --cov=app --cov-report=html

test-simple: ## Run tests without coverage
	pytest tests/ -v

lint: ## Run linting checks
	flake8 app.py templates/
	mypy app.py

format: ## Format code with black
	black app.py templates/

check: lint test-simple ## Run all checks (lint + test)

clean: ## Clean up temporary files
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf temp_audio/*
	rm -rf .mypy_cache/
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

setup: ## Initial setup for development
	python -m venv venv
	@echo "Virtual environment created. Activate it with:"
	@echo "source venv/bin/activate  # On Unix/macOS"
	@echo "venv\\Scripts\\activate     # On Windows"

docker-build: ## Build Docker image
	docker build -t youtube-waveform-visualizer .

docker-run: ## Run with Docker
	docker run -p 8000:8000 youtube-waveform-visualizer

docker-clean: ## Clean Docker images
	docker rmi youtube-waveform-visualizer

deploy: ## Deploy to production (placeholder)
	@echo "Deployment not configured yet"
	@echo "Add your deployment commands here"

docs: ## Generate documentation
	@echo "Documentation generation not configured yet"
	@echo "Add your documentation generation commands here"

release: ## Create a new release
	@echo "Creating release..."
	@echo "1. Update version in setup.py and pyproject.toml"
	@echo "2. Update CHANGELOG.md"
	@echo "3. Create git tag"
	@echo "4. Push to GitHub"
