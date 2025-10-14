# scatter-svg

Scatter plot generator with automatic label collision avoidance using
matplotlib + adjustText.

## Usage (Docker)

### Basic Usage

```bash
# JSON/CSV from stdin → SVG to stdout
cat data.json | docker run -i docker.io/hugojosefson/scatter-svg > output.svg
cat data.csv | docker run -i docker.io/hugojosefson/scatter-svg > output.svg
```

### PNG Output

```bash
cat data.json | docker run -i docker.io/hugojosefson/scatter-svg --format png > output.png
```

### Example Data

```bash
cat examples/model-data-example.json | docker run -i docker.io/hugojosefson/scatter-svg > output.svg
cat examples/model-data-example.csv | docker run -i docker.io/hugojosefson/scatter-svg > output.svg
```

## Build

```bash
./docker-build
```

## Development

### Setup

Install the package in editable mode with development dependencies:

```bash
pip install -e ".[dev]"
```

### Development Commands

Use `make` to run common development tasks:

```bash
make install   # Install package in editable mode with dev dependencies
make format    # Format code with black
make lint      # Check code with ruff
make test      # Run tests with pytest and coverage
make all       # Run format, lint, and test (pre-commit check)
make check     # Alias for 'all'
```

### Pre-commit Workflow

Before committing changes, run all checks:

```bash
make all
```

This will:
1. Format code with black
2. Lint code with ruff
3. Run tests with pytest and coverage

The Docker build also runs formatting and linting checks before tests.

## Input Formats

**JSON:** `{"points": [{"x": 100, "y": 5, "label": "name"}]}`
([example](examples/model-data-example.json))

**CSV:** `label,x,y` (auto-detects column names)
([example](examples/model-data-example.csv))
