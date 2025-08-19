# Makefile for CRM backend

# Variables
PYTHON = python3
PIP = pip3

# Install dependencies
install:
	$(PIP) install -r requirements.txt

# Install development dependencies
install-dev:
	$(PIP) install -r requirements.txt
	$(PIP) install black flake8 mypy

# Run the application
run:
	$(PYTHON) -m uvicorn app.main:app --reload

# Run tests
test:
	$(PYTHON) -m pytest

# Run specific test
test-comprehensive:
	$(PYTHON) -m pytest tests/test_comprehensive.py -v

# Test the Gemini AI integration
test-gemini:
	$(PYTHON) scripts/test_gemini.py

# Run fine-tuning script
fine-tune:
	$(PYTHON) scripts/fine_tune_rag.py

# Format code with black
format:
	black .

# Check code with flake8
lint:
	flake8 .

# Type check with mypy
type-check:
	mypy .

# Install all dependencies including dev
setup-dev: install-dev format lint

# Help
help:
	@echo "Available commands:"
	@echo "  install         - Install dependencies"
	@echo "  install-dev     - Install dependencies including development tools"
	@echo "  run             - Run the application"
	@echo "  test            - Run all tests"
	@echo "  test-comprehensive - Run comprehensive tests"
	@echo "  test-gemini     - Test Gemini AI integration"
	@echo "  fine-tune       - Run fine-tuning script"
	@echo "  format          - Format code with black"
	@echo "  lint            - Check code with flake8"
	@echo "  type-check      - Type check with mypy"
	@echo "  setup-dev       - Install all dependencies and format code"
	@echo "  help            - Show this help message"

.PHONY: install install-dev run test test-comprehensive test-gemini fine-tune format lint type-check setup-dev help
