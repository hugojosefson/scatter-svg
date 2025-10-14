# Test stage - install all deps and run tests
FROM python:3.13 AS test

COPY pyproject.toml /tmp/pyproject.toml
WORKDIR /tmp
RUN pip install --no-cache-dir ".[dev]"

COPY src/ /tmp/src/
COPY tests/ /tmp/tests/
RUN pytest tests/ -v

# Production stage - minimal with only prod deps
FROM python:3.13-slim AS production

COPY pyproject.toml /tmp/pyproject.toml
WORKDIR /tmp
RUN pip install --no-cache-dir .

COPY src/ /tmp/src/
RUN pip install --no-cache-dir .

ENTRYPOINT ["python", "-m", "scatter_svg"]
