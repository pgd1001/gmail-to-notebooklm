# Makefile for Gmail to NotebookLM Converter
# Provides convenient commands for common development tasks

.PHONY: help install install-dev test coverage lint format clean build docs run

# Default target
help:
	@echo "Gmail to NotebookLM Converter - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install       Install production dependencies"
	@echo "  make install-dev   Install with development dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make test          Run tests"
	@echo "  make coverage      Run tests with coverage report"
	@echo "  make lint          Run linting (flake8, mypy)"
	@echo "  make format        Format code (black, isort)"
	@echo "  make check         Run all checks (format, lint, test)"
	@echo ""
	@echo "Build:"
	@echo "  make build         Build distribution packages"
	@echo "  make clean         Clean build artifacts"
	@echo ""
	@echo "Run:"
	@echo "  make run           Run the CLI (requires LABEL argument)"
	@echo "  make example       Run with example label"
	@echo ""
	@echo "Examples:"
	@echo "  make run LABEL='Client A' OUTPUT=./output"
	@echo "  make test"
	@echo "  make format"

# Installation targets
install:
	pip install -r requirements.txt
	pip install -e .

install-dev:
	pip install -r requirements.txt
	pip install -e ".[dev]"
	pre-commit install

# Testing targets
test:
	pytest

coverage:
	pytest --cov=gmail_to_notebooklm --cov-report=term-missing --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

# Code quality targets
lint:
	@echo "Running flake8..."
	flake8 gmail_to_notebooklm tests
	@echo "Running mypy..."
	mypy gmail_to_notebooklm

format:
	@echo "Running black..."
	black gmail_to_notebooklm tests
	@echo "Running isort..."
	isort gmail_to_notebooklm tests
	@echo "Code formatted successfully!"

# Comprehensive check
check: format lint test
	@echo "All checks passed!"

# Build targets
build: clean
	python -m build
	@echo "Build complete! Packages in dist/"

clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	@echo "Clean complete!"

# Documentation
docs:
	@echo "Opening documentation..."
	@if [ -f "README.md" ]; then \
		if command -v open > /dev/null; then \
			open README.md; \
		elif command -v xdg-open > /dev/null; then \
			xdg-open README.md; \
		else \
			echo "Please open README.md manually"; \
		fi \
	fi

# Run targets
run:
	@if [ -z "$(LABEL)" ]; then \
		echo "Error: LABEL argument required"; \
		echo "Usage: make run LABEL='Your Label' [OUTPUT=./output]"; \
		exit 1; \
	fi
	gmail-to-notebooklm --label "$(LABEL)" --output-dir $(or $(OUTPUT),./output)

example:
	@echo "Running example export..."
	gmail-to-notebooklm --label "Test" --output-dir "./test_output" --verbose

# Development utilities
shell:
	python

watch-test:
	@echo "Watching for changes and running tests..."
	@while true; do \
		clear; \
		make test; \
		inotifywait -qre modify .; \
	done

pre-commit:
	pre-commit run --all-files

# Version management
version:
	@python -c "import gmail_to_notebooklm; print(gmail_to_notebooklm.__version__)"

# Security
security-check:
	@echo "Checking for security vulnerabilities..."
	pip-audit

# Requirements
requirements:
	pip freeze > requirements-freeze.txt
	@echo "Current requirements frozen to requirements-freeze.txt"

# Virtual environment setup
venv:
	python -m venv .venv
	@echo "Virtual environment created in .venv"
	@echo "Activate with: source .venv/bin/activate (Unix) or .venv\\Scripts\\activate (Windows)"
