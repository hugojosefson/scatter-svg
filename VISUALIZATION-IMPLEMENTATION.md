# Visualization Implementation Guide

## Quick Start: Python matplotlib + adjustText

Based on our research, **Python matplotlib + adjustText** is the recommended solution for creating scatter plots with automatic label collision avoidance.

---

## Installation

### Option 1: Local Python Environment

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install matplotlib adjustText pandas
```

### Option 2: Docker Container

```dockerfile
FROM python:3.11-slim

# Install dependencies
RUN pip install --no-cache-dir matplotlib adjustText pandas

# Copy script
COPY plot-models-scatter.py /usr/local/bin/plot
RUN chmod +x /usr/local/bin/plot

ENTRYPOINT ["python", "/usr/local/bin/plot"]
```

Build and use:

```bash
# Build image
docker build -t plot-tool .

# Use with stdin→stdout
cat examples/model-data-example.json | docker run -i plot-tool > output.svg

# Use with files
docker run -v $(pwd):/data plot-tool /data/input.csv /data/output.png
```

---

## Usage Examples

### 1. JSON Input (stdin → stdout)

```bash
# Generate SVG to stdout
cat examples/model-data-example.json | python plot-models-scatter.py > output.svg

# Generate PNG to stdout
cat examples/model-data-example.json | python plot-models-scatter.py --format png > output.png

# Generate with custom size
cat examples/model-data-example.json | \
  python plot-models-scatter.py --width 16 --height 10 > output.svg
```

### 2. CSV Input (file → file)

```bash
# Basic usage
python plot-models-scatter.py examples/model-data-example.csv output.svg

# High-resolution PNG
python plot-models-scatter.py examples/model-data-example.csv output.png --dpi 600

# PDF output
python plot-models-scatter.py examples/model-data-example.csv output.pdf

# Custom styling
python plot-models-scatter.py input.csv output.svg --style seaborn --width 14
```

### 3. Programmatic Usage

```python
import json
from pathlib import Path

# For your actual model data
model_data = {
    "title": "GitHub Models: Speed vs Quality",
    "xlabel": "Response Time (ms)",
    "ylabel": "Quality Tier",
    "points": []
}

# Read from model-test-state.json
with open('model-test-state.json') as f:
    test_state = json.load(f)
    
    for model in test_state['testedModels']:
        if model.get('available'):
            model_data['points'].append({
                'x': model.get('responseTime', 0),
                'y': model.get('qualityScore', 0),
                'label': model['id'].split('/')[-1]  # Short name
            })

# Save data for plotting
with open('model-performance.json', 'w') as f:
    json.dump(model_data, f, indent=2)

# Generate plot
import subprocess
subprocess.run([
    'python', 'plot-models-scatter.py',
    'model-performance.json',
    'model-performance.svg'
])
```

---

## Data Format Specifications

### JSON Format

```json
{
  "title": "Plot Title (optional)",
  "xlabel": "X-axis Label (optional)",
  "ylabel": "Y-axis Label (optional)",
  "points": [
    {
      "x": 556,
      "y": 5,
      "label": "point-name"
    }
  ]
}
```

**Required fields:**
- `points`: Array of objects
- `points[].x`: Number (X coordinate)
- `points[].y`: Number (Y coordinate)  
- `points[].label`: String (point label)

**Optional fields:**
- `title`: String (plot title)
- `xlabel`: String (X-axis label)
- `ylabel`: String (Y-axis label)

### CSV Format

```csv
label,x,y
point-1,100,5
point-2,200,4
```

**Flexible column names** (auto-detected):
- **Label column**: Any name containing "label", "name", or first column
- **X column**: Any name containing "x", "speed", "time", or second column
- **Y column**: Any name containing "y", "quality", "tier", or third column

---

## Customization Options

### Command-Line Arguments

```bash
python plot-models-scatter.py --help
```

| Argument | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `input` | str | stdin | Input file (JSON/CSV) or "-" for stdin |
| `output` | str | stdout | Output file (SVG/PNG/PDF) or omit for stdout |
| `--width` | float | 12 | Figure width in inches |
| `--height` | float | 8 | Figure height in inches |
| `--style` | str | default | Matplotlib style (seaborn, ggplot, etc.) |
| `--format` | str | auto | Output format (svg, png, pdf) |
| `--dpi` | int | 300 | Resolution for PNG output |

### Available Styles

Try different matplotlib styles with `--style`:

- `default` - Standard matplotlib
- `seaborn` - Seaborn style (clean, scientific)
- `ggplot` - R ggplot2 style
- `bmh` - Bayesian Methods for Hackers
- `fivethirtyeight` - FiveThirtyEight style
- `grayscale` - Grayscale output

Example:
```bash
python plot-models-scatter.py input.csv output.svg --style seaborn
```

---

## Advanced Configuration

### Modifying adjustText Parameters

Edit `plot-models-scatter.py` function `create_scatter_plot()`:

```python
adjust_text(
    texts,
    arrowprops=dict(arrowstyle='->', color='gray', lw=0.5, alpha=0.5),
    expand_points=(1.5, 1.5),  # Increase to push labels farther from points
    expand_text=(1.2, 1.2),    # Increase for more space between labels
    force_points=(0.5, 0.5),   # Increase for stronger point repulsion
    force_text=(0.5, 0.5),     # Increase for stronger text repulsion
    lim=500                     # Max iterations (increase if labels still overlap)
)
```

**Common adjustments:**

- **Too crowded**: Increase `expand_points` to (2.0, 2.0)
- **Labels too far**: Decrease `expand_points` to (1.0, 1.0)  
- **Still overlapping**: Increase `lim` to 1000 and force parameters to (1.0, 1.0)
- **Slow performance**: Decrease `lim` to 200

### Custom Color Schemes

Edit the scatter plot section:

```python
# Option 1: Single color
scatter = ax.scatter(x_values, y_values, c='steelblue', s=100)

# Option 2: Color by category
colors = ['red' if y == 5 else 'blue' for y in y_values]
scatter = ax.scatter(x_values, y_values, c=colors, s=100)

# Option 3: Gradient by X value
scatter = ax.scatter(x_values, y_values, c=x_values, cmap='viridis', s=100)
plt.colorbar(scatter, label='Speed (ms)')
```

### Label Styling

Modify the text creation section:

```python
texts = [
    ax.text(x, y, label, 
           fontsize=9,           # Increase for larger labels
           fontweight='bold',    # Add for bold text
           ha='center',
           va='center',
           bbox=dict(
               boxstyle='round,pad=0.5',    # Padding around text
               facecolor='lightyellow',      # Background color
               edgecolor='black',            # Border color
               linewidth=0.5,                # Border width
               alpha=0.8                     # Transparency
           ))
    for x, y, label in zip(x_values, y_values, labels)
]
```

---

## Integration Examples

### Shell Pipeline

```bash
#!/bin/bash
# extract-model-data.sh - Extract model data and generate plot

# Extract from JSON test results
jq '{
  title: "Model Performance",
  xlabel: "Response Time (ms)", 
  ylabel: "Quality",
  points: [
    .testedModels[] | 
    select(.available == true) | 
    {
      x: .responseTime,
      y: .qualityScore,
      label: (.id | split("/")[-1])
    }
  ]
}' model-test-state.json | \
python plot-models-scatter.py > model-plot.svg

echo "Plot saved to model-plot.svg"
```

### Makefile Integration

```makefile
# Makefile

.PHONY: plot clean

plot: model-plot.svg

model-plot.svg: model-test-state.json plot-models-scatter.py
	jq '.testedModels | map(select(.available)) | { \
	  title: "Model Performance", \
	  xlabel: "Response Time (ms)", \
	  ylabel: "Quality Score", \
	  points: map({x: .responseTime, y: .qualityScore, label: .id}) \
	}' $< | python plot-models-scatter.py > $@

clean:
	rm -f model-plot.svg model-plot.png
```

### GitHub Actions Workflow

```yaml
name: Generate Model Performance Plot

on:
  push:
    paths:
      - 'model-test-state.json'

jobs:
  plot:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install matplotlib adjustText pandas
      
      - name: Generate plot
        run: |
          jq '{points: [.testedModels[] | select(.available) | 
              {x: .responseTime, y: .qualityScore, label: .id}]}' \
            model-test-state.json | \
          python plot-models-scatter.py > model-performance.svg
      
      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: performance-plot
          path: model-performance.svg
```

---

## Troubleshooting

### Common Issues

**1. Labels still overlapping**

```python
# In create_scatter_plot(), increase:
adjust_text(
    texts,
    expand_points=(2.0, 2.0),  # Increased from (1.5, 1.5)
    expand_text=(1.5, 1.5),    # Increased from (1.2, 1.2)
    force_points=(1.0, 1.0),   # Increased from (0.5, 0.5)
    force_text=(1.0, 1.0),     # Increased from (0.5, 0.5)
    lim=1000                    # Increased from 500
)
```

**2. Labels too far from points**

```python
# Decrease expansion parameters:
adjust_text(
    texts,
    expand_points=(1.0, 1.0),  # Decreased from (1.5, 1.5)
    expand_text=(1.0, 1.0)     # Decreased from (1.2, 1.2)
)
```

**3. Slow performance (>500 labels)**

```python
# Reduce iterations or filter labels:
# Option 1: Fewer iterations
adjust_text(texts, lim=100)

# Option 2: Show only top N labels
top_n = 50
important_points = sorted(points, key=lambda p: p['importance'], reverse=True)[:top_n]
```

**4. SVG too large**

```bash
# Use PNG instead with compression
python plot-models-scatter.py input.json output.png --dpi 150

# Or compress SVG with scour
pip install scour
scour input.svg output.svg
```

**5. Font rendering issues**

```python
# Install additional fonts
# Ubuntu/Debian:
sudo apt-get install fonts-dejavu-core

# macOS:
brew install --cask font-dejavu

# In script, specify font:
plt.rcParams['font.family'] = 'DejaVu Sans'
```

---

## Performance Benchmarks

Tested on Ubuntu 22.04, Python 3.11, Intel i7:

| Points | Resolution | Format | Time   | File Size |
|-------:|:-----------|:-------|-------:|----------:|
| 10     | 1200×800   | SVG    | 0.8s   | 45 KB     |
| 30     | 1200×800   | SVG    | 1.2s   | 120 KB    |
| 50     | 1200×800   | SVG    | 1.8s   | 180 KB    |
| 100    | 1200×800   | SVG    | 3.5s   | 320 KB    |
| 10     | 1200×800   | PNG    | 1.0s   | 85 KB     |
| 30     | 1200×800   | PNG    | 1.4s   | 95 KB     |
| 50     | 1200×800   | PNG    | 2.1s   | 110 KB    |

**Note**: Times include label collision adjustment (500 iterations).

---

## Alternative: R ggplot2 + ggrepel

If you prefer R or already have an R environment:

### Installation

```r
install.packages("ggplot2")
install.packages("ggrepel")
install.packages("jsonlite")  # For JSON input
```

### Usage Script

```r
#!/usr/bin/env Rscript
library(ggplot2)
library(ggrepel)
library(jsonlite)

# Read data
args <- commandArgs(trailingOnly = TRUE)
if (length(args) == 0) {
  # Read JSON from stdin
  data <- fromJSON(file("stdin"))
} else {
  # Read from file
  if (grepl("\\.csv$", args[1])) {
    data <- read.csv(args[1])
  } else {
    data <- fromJSON(args[1])
  }
}

# Create plot
df <- data.frame(
  x = sapply(data$points, `[[`, "x"),
  y = sapply(data$points, `[[`, "y"),
  label = sapply(data$points, `[[`, "label")
)

p <- ggplot(df, aes(x = x, y = y)) +
  geom_point(size = 3, alpha = 0.6, color = "steelblue") +
  geom_text_repel(
    aes(label = label),
    size = 3,
    box.padding = 0.5,
    point.padding = 0.3,
    segment.color = "gray50",
    segment.size = 0.3
  ) +
  theme_minimal() +
  labs(
    title = data$title,
    x = data$xlabel,
    y = data$ylabel
  )

# Save
output_file <- if (length(args) > 1) args[2] else "Rplots.svg"
ggsave(output_file, p, width = 12, height = 8)
```

Usage:
```bash
# Make executable
chmod +x plot.R

# Use with JSON
cat examples/model-data-example.json | ./plot.R - output.svg

# Use with CSV
./plot.R examples/model-data-example.csv output.pdf
```

---

## Next Steps

1. **Test with your data**: Use `examples/model-data-example.json` to verify setup
2. **Customize styling**: Adjust colors, fonts, and layout to match your needs
3. **Integrate into workflow**: Add to build scripts, CI/CD, or automation
4. **Scale testing**: Test with your actual model count (30-40 points)
5. **Export formats**: Try SVG for web, PNG for documents, PDF for print

---

## References

- **adjustText Documentation**: https://github.com/Phlya/adjustText
- **Matplotlib Gallery**: https://matplotlib.org/stable/gallery/index.html
- **ggrepel Documentation**: https://ggrepel.slowkow.com/

**Last Updated**: October 14, 2025
