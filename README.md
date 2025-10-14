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

## Input Formats

**JSON:** `{"points": [{"x": 100, "y": 5, "label": "name"}]}`
([example](examples/model-data-example.json))

**CSV:** `label,x,y` (auto-detects column names)
([example](examples/model-data-example.csv))
