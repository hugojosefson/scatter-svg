# Test stage - install all deps and run tests
FROM python:3.14.0 AS test

# Copy minimal files for dependency installation (better caching)
COPY pyproject.toml /tmp/pyproject.toml
# Create stub __init__.py with just version for setuptools
RUN mkdir -p /tmp/src/scatter_svg && \
    echo '__version__ = "1.0.0"' > /tmp/src/scatter_svg/__init__.py
WORKDIR /tmp
RUN pip install --no-cache-dir ".[dev]"

# Copy full source code later (won't invalidate cache if dependencies unchanged)
COPY src/ /tmp/src/
# Reinstall in editable mode to use the full source
RUN pip install --no-cache-dir -e .
COPY tests/ /tmp/tests/
RUN pytest tests/ -v

# Production stage - minimal with only prod deps
FROM python:3.14.0-slim AS production

# Copy minimal files for dependency installation (better caching)
COPY pyproject.toml /tmp/pyproject.toml
# Create stub __init__.py with just version for setuptools
RUN mkdir -p /tmp/src/scatter_svg && \
    echo '__version__ = "1.0.0"' > /tmp/src/scatter_svg/__init__.py
WORKDIR /tmp
RUN pip install --no-cache-dir .

# Copy full source code later (won't invalidate cache if dependencies unchanged)
COPY src/ /tmp/src/
# Reinstall to use the full source
RUN pip install --no-cache-dir --force-reinstall --no-deps .

ENTRYPOINT ["python", "-m", "scatter_svg"]
