IMAGE := docker.io/hugojosefson/scatter-svg

.PHONY: format lint test all check install docker-build docker-push docker-test help

help:
	@echo "Available commands:"
	@echo "  make install       - Install package in editable mode with dev dependencies"
	@echo "  make format        - Format code with black"
	@echo "  make lint          - Check code with ruff"
	@echo "  make test          - Run tests with pytest and coverage"
	@echo "  make all           - Run format, lint, and test (pre-commit check)"
	@echo "  make check         - Alias for 'all'"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-push   - Build and push Docker image"
	@echo "  make docker-test   - Build and run Docker test stage"

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

docker-build:
	docker build -t $(IMAGE) .

docker-push: docker-build
	docker push $(IMAGE)

docker-test:
	docker build --target test .
