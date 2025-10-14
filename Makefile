.PHONY: format lint test all check install help

help:
	@echo "Available commands:"
	@echo "  make install  - Install package in editable mode with dev dependencies"
	@echo "  make format   - Format code with black"
	@echo "  make lint     - Check code with ruff"
	@echo "  make test     - Run tests with pytest and coverage"
	@echo "  make all      - Run format, lint, and test (pre-commit check)"
	@echo "  make check    - Alias for 'all'"

install:
	pip install -e ".[dev]"

format:
	black src/ tests/

lint:
	ruff check src/ tests/

test:
	pytest tests/ --cov=scatter_svg --cov-report=term-missing

all: format lint test

check: all
