# scatter-svg

**Scatter Plot Generator with Automatic Label Collision Avoidance**

Python tool using matplotlib + adjustText for collision-free scatter plots with
professional-quality output.

## Installation

### Development Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/hugojosefson/scatter-svg
cd scatter-svg

# Install in editable mode with development dependencies
pip install -e ".[dev]"
```

### Production Installation

```bash
pip install scatter-svg
```

### Using Docker

```bash
docker pull docker.io/hugojosefson/scatter-svg
```

## Quick Start

After installation, use the `scatter-svg` command:

```bash
# From JSON stdin
cat examples/model-data-example.json | scatter-svg > output.svg

# From CSV stdin (auto-detected)
cat examples/model-data-example.csv | scatter-svg > output.svg

# From file with custom options
scatter-svg examples/model-data-example.json output.svg --width 12 --height 8

# Generate PNG instead of SVG
scatter-svg examples/model-data-example.csv output.png --format png
```

## Usage

### Command Line Interface

```bash
scatter-svg [INPUT] [OUTPUT] [OPTIONS]

Arguments:
  INPUT                Input file (JSON or CSV), or use stdin if omitted
  OUTPUT               Output file (SVG, PNG, PDF), or use stdout if omitted

Options:
  --format FORMAT      Output format: svg, png, pdf (default: svg)
  --width INCHES       Figure width in inches (default: 12)
  --height INCHES      Figure height in inches (default: 8)
  --style STYLE        Matplotlib style (default, seaborn, ggplot, etc.)
  --dpi DPI            DPI for PNG output (default: 300)
```

### As a Python Library

```python
from scatter_svg import create_scatter_plot, save_figure, load_data_file

# Load data from file (auto-detects CSV or JSON)
data = load_data_file('examples/model-data-example.csv')

# Create plot
fig = create_scatter_plot(data, figsize=(12, 8))

# Save to file
save_figure(fig, 'output.svg', format='svg')
```

### Stdin/Stdout Pipeline (Unix-style)

```bash
# JSON input automatically detected
cat data.json | scatter-svg > output.svg

# CSV input automatically detected
cat data.csv | scatter-svg --format png > output.png

# Docker usage
cat data.json | docker run -i docker.io/hugojosefson/scatter-svg > output.svg
```

## Input Format

### JSON Format

```json
{
  "title": "Model Speed vs Quality",
  "xlabel": "Response Time (ms)",
  "ylabel": "Quality Tier",
  "points": [
    { "x": 556, "y": 4, "label": "llama-4-scout" },
    { "x": 666, "y": 5, "label": "gpt-4o-mini" }
  ]
}
```

### CSV Format

```csv
label,x,y
llama-4-scout,556,4
gpt-4o-mini,666,5
```

**Note**: Stdin input automatically detects JSON vs CSV format. The tool tries
to parse as JSON first, then falls back to CSV if JSON parsing fails.

See `examples/model-data-example.json` and `examples/model-data-example.csv` for
complete examples.

## Project Structure

```
scatter-svg/
├── src/
│   └── scatter_svg/
│       ├── __init__.py       # Package exports
│       ├── __main__.py       # CLI entry point
│       └── plot.py           # Core plotting logic
├── tests/
│   ├── __init__.py
│   └── test_plot.py          # Comprehensive unit tests
├── examples/
│   ├── model-data-example.json
│   └── model-data-example.csv
├── pyproject.toml            # Package configuration
├── README.md
├── Dockerfile
└── build.sh
```

## Development

### Running Tests

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Run tests
python -m pytest tests/

# Run tests with coverage
python -m pytest tests/ --cov=scatter_svg --cov-report=html

# Run specific test
python -m unittest tests.test_plot.TestStdinAutodetection -v
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/
```

### Building from Source

```bash
# Build Python package
pip install build
python -m build

# Build Docker image
./build.sh

# Build and push to registry
./build.sh --push
```

## Features

- 📊 **Automatic Label Collision Avoidance**: Uses adjustText library for
  intelligent label positioning
- 🎨 **Multiple Output Formats**: SVG (vector), PNG, and PDF support
- 📥 **Flexible Input**: JSON or CSV via stdin or file
- 🔍 **Auto-detection**: Automatically detects JSON vs CSV from stdin
- 📤 **Pipeline Friendly**: Stdin → stdout workflow for Unix pipelines
- 🐳 **Docker Support**: Pre-built image for zero-install usage
- 📦 **Pip Installable**: Standard Python package with CLI entry point
- ⚙️ **Customizable**: Configure dimensions, labels, titles, and formats
- 🧪 **Well Tested**: Comprehensive test suite with high coverage

## Docker Image

**Repository**: `docker.io/hugojosefson/scatter-svg`

The Docker image includes all dependencies pre-installed and exposes the scatter
plot generator as the entrypoint.

## Additional Documentation

- `examples/` - Example JSON and CSV input files
- `TEST-README.md` - Testing documentation
- `VISUALIZATION-IMPLEMENTATION.md` - Implementation details and advanced usage

## License

MIT
