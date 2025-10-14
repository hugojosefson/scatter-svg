# scatter-svg

Scatter plot generator with automatic label collision avoidance using matplotlib + adjustText.

## Usage (Docker)

```bash
# JSON/CSV from stdin → SVG to stdout
cat data.json | docker run -i scatter-svg > output.svg
cat data.csv | docker run -i scatter-svg > output.svg

# PNG output
cat data.json | docker run -i scatter-svg --format png > output.png
```

## Build

```bash
docker build -t scatter-svg .
```

## Input Formats

**JSON:** `{"points": [{"x": 100, "y": 5, "label": "name"}]}`

**CSV:** `label,x,y` (auto-detects column names)
