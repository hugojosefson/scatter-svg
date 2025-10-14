# Visualization Tools Comparison: Label Collision Avoidance

## Overview

Comprehensive research comparing visualization tools for creating scatter plots
with **automatic label collision avoidance** - the primary requirement for
plotting model data (X=speed, Y=quality tiers).

**Research Date**: October 14, 2025\
**Use Case**: Scatter plot with ~30-40 labeled points requiring collision-free
text labels\
**Critical Requirement**: Automatic label positioning to avoid overlaps

---

## Executive Summary

### ✅ Tools with TRUE Automatic Collision Avoidance

Only **2 tools** provide production-ready automatic label collision avoidance:

1. **Python matplotlib + adjustText** - Dedicated iterative adjustment algorithm
2. **R ggplot2 + ggrepel** - Industry-standard repelling labels

### ❌ Tools WITHOUT Automatic Collision Avoidance

All JavaScript-based visualization libraries lack this feature:

- **Vega-Lite**: No collision avoidance (only truncation via `limit`)
- **Observable Plot**: No collision avoidance (manual filtering required)
- **Plotly.js**: No collision avoidance (`textposition: "auto"` only for single
  points)

---

## Detailed Tool Comparison

### 1. Python matplotlib + adjustText ✅

**Status**: **FULL COLLISION AVOIDANCE**\
**Runtime**: Python 3.x\
**License**: MIT (adjustText), BSD-compatible (matplotlib)

#### Key Features

- Dedicated `adjustText` library specifically for label collision avoidance
- Iterative force-directed algorithm to minimize overlaps
- Repels labels from:
  - Each other
  - Data points
  - Plot edges
- Inspired by R's ggrepel
- Configurable repulsion forces and arrow connectors

#### Installation

```bash
# Via pip
pip install matplotlib adjustText

# Via conda
conda install matplotlib
conda install -c conda-forge adjusttext
```

#### Input Format

```python
# CSV input example
import pandas as pd
import matplotlib.pyplot as plt
from adjustText import adjust_text

# Read data
df = pd.read_csv('models.csv')  # columns: name, speed, quality

# Create scatter plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(df['speed'], df['quality'])

# Add labels with collision avoidance
texts = [ax.text(row['speed'], row['quality'], row['name'], fontsize=8) 
         for _, row in df.iterrows()]
adjust_text(texts, arrowprops=dict(arrowstyle='->', color='gray', lw=0.5))

# Save output
plt.savefig('output.svg', format='svg')
plt.savefig('output.png', dpi=300)
```

#### Stdin/Stdout Support

Python scripts don't natively support stdin→stdout for image generation, but can
be wrapped:

```python
#!/usr/bin/env python3
import sys
import json
import matplotlib.pyplot as plt
from adjustText import adjust_text
import io

# Read JSON from stdin
data = json.load(sys.stdin)

# Create plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter([p['x'] for p in data['points']], 
           [p['y'] for p in data['points']])

texts = [ax.text(p['x'], p['y'], p['label'], fontsize=8) 
         for p in data['points']]
adjust_text(texts)

# Write SVG to stdout
output = io.StringIO()
plt.savefig(output, format='svg')
sys.stdout.write(output.getvalue())
```

#### Pros

- ✅ TRUE collision avoidance (primary requirement)
- ✅ Highly configurable (force parameters, arrow styles)
- ✅ Actively maintained library
- ✅ Export to SVG, PNG, PDF
- ✅ Well-documented with extensive examples

#### Cons

- ❌ Requires Python runtime
- ❌ No native stdin→stdout pipeline (requires wrapper)
- ❌ Iterative algorithm can be slow for 500+ labels
- ❌ May require parameter tuning for optimal results

#### Effort Level

**Medium** - Requires Python setup, but straightforward API

---

### 2. R ggplot2 + ggrepel ✅

**Status**: **FULL COLLISION AVOIDANCE**\
**Runtime**: R 4.x\
**License**: GPL-3 (ggplot2, ggrepel)

#### Key Features

- Industry-standard solution for label repelling
- `geom_text_repel()` and `geom_label_repel()` functions
- Advanced algorithm repels labels from:
  - Each other
  - Data points
  - Plot edges
  - User-defined areas
- Extensive configuration options
- Production-proven in scientific publications

#### Installation

```r
# Install from CRAN
install.packages("ggplot2")
install.packages("ggrepel")
```

#### Input Format

```r
library(ggplot2)
library(ggrepel)

# Read CSV data
df <- read.csv('models.csv')  # columns: name, speed, quality

# Create scatter plot with repelled labels
p <- ggplot(df, aes(x = speed, y = quality)) +
  geom_point() +
  geom_text_repel(aes(label = name), size = 3, box.padding = 0.5) +
  theme_minimal()

# Save output
ggsave('output.svg', p, width = 10, height = 6)
ggsave('output.png', p, width = 10, height = 6, dpi = 300)
```

#### Stdin/Stdout Support

R can be used in pipeline mode with Rscript:

```r
#!/usr/bin/env Rscript
library(ggplot2)
library(ggrepel)
library(jsonlite)

# Read JSON from stdin
input <- paste(readLines(file("stdin")), collapse = "\n")
data <- fromJSON(input)

# Create plot
df <- data.frame(
  x = sapply(data$points, `[[`, "x"),
  y = sapply(data$points, `[[`, "y"),
  label = sapply(data$points, `[[`, "label")
)

p <- ggplot(df, aes(x = x, y = y)) +
  geom_point() +
  geom_text_repel(aes(label = label)) +
  theme_minimal()

# Write SVG to stdout
ggsave(stdout(), p, device = "svg", width = 10, height = 6)
```

#### Pros

- ✅ TRUE collision avoidance (primary requirement)
- ✅ Industry-standard solution (widely trusted)
- ✅ Excellent default behavior (minimal tuning needed)
- ✅ Rich ecosystem (ggplot2 grammar)
- ✅ Publication-quality output

#### Cons

- ❌ Requires R runtime
- ❌ Steeper learning curve (ggplot2 syntax)
- ❌ Less familiar to non-R developers
- ❌ Stdin→stdout requires jsonlite library

#### Effort Level

**Medium-High** - Requires R setup and ggplot2 knowledge

---

### 3. Vega-Lite ❌

**Status**: **NO COLLISION AVOIDANCE**\
**Runtime**: Browser / Node.js (vega-cli)\
**License**: BSD-3-Clause

#### Research Findings

- **Text mark properties**: Only `limit` (character truncation) available
- **No `labelOverlap` parameter**: This exists only for axis/legend labels, NOT
  for text marks
- **No automatic positioning**: Text marks require manual `dx`/`dy` offsets
- **Workaround**: Manual coordinate calculation in data preprocessing

#### Documentation Review

Examined:

- Text mark documentation
- Label configuration options
- Mark properties reference
- Encoding channels

**Conclusion**: Vega-Lite does NOT support automatic label collision avoidance
for scatter plot point labels.

#### Example (Manual Positioning Required)

```json
{
  "data": { "url": "models.csv" },
  "mark": { "type": "text", "dx": 5, "dy": -5 },
  "encoding": {
    "x": { "field": "speed", "type": "quantitative" },
    "y": { "field": "quality", "type": "quantitative" },
    "text": { "field": "name", "type": "nominal" }
  }
}
```

#### Stdin/Stdout Support

✅ Excellent - vega-cli designed for pipelines:

```bash
cat spec.json | vl2svg > output.svg
cat spec.json | vl2png > output.png
```

#### Pros

- ✅ Excellent stdin→stdout support
- ✅ JSON declarative syntax
- ✅ Lightweight Node.js runtime
- ✅ SVG/PNG/PDF export via vega-cli

#### Cons

- ❌ **NO collision avoidance** (fails primary requirement)
- ❌ Requires manual label positioning
- ❌ Not suitable for dense scatter plots

#### Effort Level

**Low** (for basic plots) / **Very High** (for collision-free labels via
preprocessing)

---

### 4. Observable Plot ❌

**Status**: **NO COLLISION AVOIDANCE**\
**Runtime**: Browser / Node.js\
**License**: ISC

#### Research Findings

- **Issue #27**: "Automatic labeling" feature request still open
- **Documentation quote**: "If you'd like automatic labeling, please upvote #27"
- **Current approach**: Manual filtering via transform to show subset of labels
- **No built-in collision detection**: Must handle manually

#### Documentation Review

Examined:

- Text mark documentation
- Label strategies discussion
- Community feature requests
- Official examples

**Conclusion**: Observable Plot explicitly lacks automatic label collision
avoidance and recommends manual filtering.

#### Example (Manual Filtering Required)

```javascript
import * as Plot from "@observablehq/plot";

Plot.plot({
  marks: [
    Plot.dot(data, { x: "speed", y: "quality" }),
    Plot.text(
      data.filter((d, i) => i % 3 === 0), // Manual: show every 3rd label
      { x: "speed", y: "quality", text: "name", dx: 5 },
    ),
  ],
});
```

#### Stdin/Stdout Support

Not designed for stdin→stdout pipelines. Requires browser or JSDOM environment.

#### Pros

- ✅ Elegant JavaScript API
- ✅ Part of Observable ecosystem
- ✅ Good for interactive notebooks

#### Cons

- ❌ **NO collision avoidance** (fails primary requirement)
- ❌ Manual label filtering needed
- ❌ Poor stdin→stdout support
- ❌ Requires JSDOM for server-side rendering

#### Effort Level

**Low** (for basic plots) / **Very High** (for collision-free labels via
filtering)

---

### 5. Plotly.js ❌

**Status**: **NO TRUE COLLISION AVOIDANCE**\
**Runtime**: Browser / Node.js (plotly-orca / kaleido)\
**License**: MIT

#### Research Findings

- **`textposition: "auto"`**: Only positions text relative to SINGLE point
  (top/bottom/left/right)
- **No inter-label collision detection**: Labels can overlap each other
- **Use case**: Designed for small number of labels or interactive tooltips
- **Not suitable**: Dense scatter plots with many labels

#### Documentation Review

Examined:

- Scatter plot text annotations
- `textposition` parameter behavior
- Layout annotation options
- Kaleido export capabilities

**Conclusion**: Plotly's "auto" positioning only handles single-point
positioning, not multi-label collision avoidance.

#### Example

```javascript
const data = [{
  x: [1, 2, 3],
  y: [1, 2, 3],
  text: ["A", "B", "C"],
  mode: "markers+text",
  textposition: "auto", // Only positions relative to each point
}];

// Export via Kaleido (Python required)
```

#### Stdin/Stdout Support

Limited - Kaleido (export tool) requires Python runtime and file I/O.

#### Pros

- ✅ Interactive hover tooltips (alternative to static labels)
- ✅ Rich charting capabilities
- ✅ Export to PNG/SVG via Kaleido

#### Cons

- ❌ **NO collision avoidance** (fails primary requirement)
- ❌ `textposition: "auto"` only for single points
- ❌ Kaleido requires Python runtime
- ❌ Complex setup for static exports

#### Effort Level

**Medium** (for basic plots) / **High** (for static exports with Kaleido)

---

## Tools Not Yet Researched

### gnuplot (Low Priority)

**Status**: Not researched\
**Expected**: Likely no automatic collision avoidance\
**Reason for low priority**: Old tool, unlikely to have modern label algorithms

### Graphviz (Medium Priority)

**Status**: Not researched\
**Expected**: Might work as creative hack\
**Notes**:

- Designed for graph layouts, not scatter plots
- Force-directed layout engine could repel labels
- Would require translating scatter plot to graph structure
- Worth investigating if Python/R not viable

### Mermaid CLI (Low Priority)

**Status**: Not researched\
**Expected**: Not designed for scatter plots\
**Reason for low priority**: Focused on diagrams (flowcharts, sequence, etc.)

### D3.js Force Simulation (Medium Priority)

**Status**: Not researched\
**Expected**: Custom implementation required\
**Notes**:

- Force simulation can repel labels
- Requires significant custom code
- Example: Mike Bostock's force-directed labels
- High effort but full control

---

## Comparison Matrix

| Tool                        | Collision Avoid | Runtime    | Stdin→Stdout | Effort | Export      | Recommendation  |
| :-------------------------- | :-------------- | :--------- | :----------- | :----- | :---------- | :-------------- |
| **matplotlib + adjustText** | ✅ YES          | Python 3.x | Via wrapper  | Medium | SVG/PNG/PDF | **Top choice**  |
| **ggplot2 + ggrepel**       | ✅ YES          | R 4.x      | Via Rscript  | Medium | SVG/PNG/PDF | **Top choice**  |
| Vega-Lite                   | ❌ NO           | Node.js    | ✅ Native    | Low    | SVG/PNG     | Not suitable    |
| Observable Plot             | ❌ NO           | Node.js    | ❌ Poor      | Low    | SVG         | Not suitable    |
| Plotly.js                   | ❌ NO           | Node.js/Py | Limited      | High   | PNG/SVG     | Not suitable    |
| gnuplot                     | ❓ Unknown      | Native     | ✅ Native    | ?      | Many        | Not researched  |
| Graphviz                    | ❓ Maybe        | Native     | ✅ Native    | High   | SVG/PNG     | Worth exploring |
| D3.js force                 | ⚠️ Custom       | Node.js    | ❌ Poor      | V.High | SVG         | Only if custom  |

---

## Recommendations

### For Your Use Case (Model Speed vs Quality Plot)

**Recommended Solution**: **Python matplotlib + adjustText**

#### Reasons:

1. ✅ **Meets primary requirement**: True automatic collision avoidance
2. ✅ **Reasonable effort**: Straightforward API, good docs
3. ✅ **Production-ready**: Actively maintained, widely used
4. ✅ **Export flexibility**: SVG for web, PNG for documents
5. ✅ **Docker-friendly**: Easy to containerize Python environment

#### Alternative Solution: **R ggplot2 + ggrepel**

Use if:

- Already have R environment
- Prefer declarative grammar of graphics
- Need publication-quality defaults

### Implementation Path

#### Option 1: Direct Python Script

```bash
# Install dependencies
pip install matplotlib adjustText pandas

# Run script
python create_plot.py models.csv output.svg
```

#### Option 2: Docker Container

```dockerfile
FROM python:3.11-slim
RUN pip install matplotlib adjustText pandas
COPY plot_script.py /app/
WORKDIR /app
ENTRYPOINT ["python", "plot_script.py"]
```

```bash
# Usage
cat models.csv | docker run -i plot-tool > output.svg
```

#### Option 3: stdin→stdout Wrapper

```python
#!/usr/bin/env python3
"""
Usage: cat models.json | ./plot.py > output.svg
Input: JSON with {"points": [{"x": 1, "y": 2, "label": "Name"}, ...]}
Output: SVG to stdout
"""
import sys, json, io
import matplotlib.pyplot as plt
from adjustText import adjust_text

data = json.load(sys.stdin)
fig, ax = plt.subplots(figsize=(12, 8))

# Plot points
x = [p['x'] for p in data['points']]
y = [p['y'] for p in data['points']]
ax.scatter(x, y, s=50, alpha=0.6)

# Add labels with collision avoidance
texts = [ax.text(p['x'], p['y'], p['label'], fontsize=9) 
         for p in data['points']]
adjust_text(texts, 
           arrowprops=dict(arrowstyle='->', color='gray', lw=0.5),
           expand_points=(1.5, 1.5))

# Styling
ax.set_xlabel(data.get('xlabel', 'X'))
ax.set_ylabel(data.get('ylabel', 'Y'))
ax.set_title(data.get('title', 'Scatter Plot'))
ax.grid(True, alpha=0.3)

# Output SVG to stdout
output = io.StringIO()
plt.savefig(output, format='svg', bbox_inches='tight')
sys.stdout.write(output.getvalue())
```

---

## Next Steps

### Immediate Actions

1. ✅ Research complete for primary tools
2. 📝 Create working code examples (in progress)
3. 🔄 Test with actual model data
4. 📦 Decide on deployment approach (direct/Docker/wrapper)

### Optional Follow-up Research

If Python/R not viable:

1. Research Graphviz as creative alternative
2. Explore D3.js force simulation custom implementation
3. Investigate gnuplot capabilities

### Questions for User

1. **Runtime preference**: Python vs R vs Docker?
2. **Pipeline integration**: Need stdin→stdout or file-based OK?
3. **Data format**: CSV, JSON, or other?
4. **Output requirements**: SVG only, or PNG/PDF too?
5. **Deployment context**: Local script, web service, CI/CD pipeline?

---

## References

### Documentation Links

- **adjustText**: https://github.com/Phlya/adjustText
- **ggrepel**: https://ggrepel.slowkow.com/
- **Vega-Lite**: https://vega.github.io/vega-lite/docs/text.html
- **Observable Plot**: https://github.com/observablehq/plot/issues/27
- **Plotly**: https://plotly.com/javascript/text-and-annotations/

### Academic References

- Overlap removal algorithms: "A Fast and Simple Graph Drawing Algorithm for
  Network Visualization" (Dwyer et al.)
- Label placement: "Point Feature Label Placement" (Christensen et al.)

---

**Last Updated**: October 14, 2025\
**Status**: Research complete for primary tools; ready for implementation phase
