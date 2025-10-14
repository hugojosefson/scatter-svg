# scatter-svg

**Scatter Plot Generator with Automatic Label Collision Avoidance**

Python tool using matplotlib + adjustText for collision-free scatter plots with professional-quality output.

## Quick Start

Using Docker (recommended):

```bash
# Pull the image
docker pull docker.io/hugojosefson/scatter-svg

# Generate SVG from JSON data
cat data.json | docker run -i docker.io/hugojosefson/scatter-svg > output.svg

# Generate PNG with custom size
cat data.json | docker run -i docker.io/hugojosefson/scatter-svg --format png --width 12 --height 8 > output.png
```

## Usage

### Stdin to Stdout (Pipeline Workflow)

```bash
# JSON input
cat model-data-example.json | ./plot-models-scatter.py > output.svg

# CSV input
cat model-data-example.csv | ./plot-models-scatter.py --format png > output.png
```

### File Input/Output

```bash
# Specify input and output files
./plot-models-scatter.py --input data.json --output chart.svg

# Different format
./plot-models-scatter.py --input data.csv --output chart.pdf --format pdf
```

### Command Line Options

```bash
./plot-models-scatter.py [options]

Options:
  --input FILE       Input file (JSON or CSV). Default: stdin
  --output FILE      Output file. Default: stdout
  --format FORMAT    Output format: svg, png, pdf. Default: svg
  --width INCHES     Figure width in inches. Default: 10
  --height INCHES    Figure height in inches. Default: 6
  --title TEXT       Chart title
  --xlabel TEXT      X-axis label
  --ylabel TEXT      Y-axis label
```

## Input Format

### JSON Format

```json
[
  {
    "name": "Point A",
    "x": 1.5,
    "y": 2.3
  },
  {
    "name": "Point B",
    "x": 2.7,
    "y": 1.8
  }
]
```

### CSV Format

```csv
name,x,y
Point A,1.5,2.3
Point B,2.7,1.8
```

See `model-data-example.json` and `model-data-example.csv` for complete examples.

## Installation

### Using pip

```bash
pip install matplotlib adjustText pandas
```

### Using Docker

```bash
docker pull docker.io/hugojosefson/scatter-svg
```

### Building from Source

```bash
# Build Docker image
./build.sh

# Build and push to registry
./build.sh --push
```

## Features

- 📊 **Automatic Label Collision Avoidance**: Uses adjustText library for intelligent label positioning
- 🎨 **Multiple Output Formats**: SVG (vector), PNG, and PDF support
- 📥 **Flexible Input**: JSON or CSV via stdin or file
- 📤 **Pipeline Friendly**: Stdin → stdout workflow for Unix pipelines
- 🐳 **Docker Support**: Pre-built image for zero-install usage
- ⚙️ **Customizable**: Configure dimensions, labels, titles, and formats

## Docker Image

**Repository**: `docker.io/hugojosefson/scatter-svg`

The Docker image includes all dependencies pre-installed and exposes the scatter plot generator as the entrypoint.

## Examples

See the included example files:
- `model-data-example.json` - Example JSON input
- `model-data-example.csv` - Example CSV input
- `VISUALIZATION-IMPLEMENTATION.md` - Implementation details
- `visualization-tools-comparison.md` - Tool comparison and decision rationale

## License

MIT
