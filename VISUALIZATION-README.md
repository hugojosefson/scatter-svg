# Visualization Research: Label Collision Avoidance

Quick navigation for scatter plot visualization with automatic label collision avoidance.

## 📁 Documentation Files

### Main Documents

1. **[visualization-tools-comparison.md](./visualization-tools-comparison.md)**
   - Comprehensive research on 5+ visualization tools
   - Detailed pros/cons, stdin/stdout support analysis
   - Only 2 tools have TRUE collision avoidance: Python matplotlib + adjustText, R ggplot2 + ggrepel
   - Full comparison matrix and recommendations

2. **[VISUALIZATION-IMPLEMENTATION.md](./VISUALIZATION-IMPLEMENTATION.md)**
   - Complete implementation guide for recommended solution
   - Installation instructions (local + Docker)
   - Usage examples (stdin, files, programmatic)
   - Customization options and troubleshooting
   - Integration examples (shell, Makefile, GitHub Actions)

### Code + Examples

3. **[plot-models-scatter.py](./plot-models-scatter.py)** ⭐ **READY TO USE**
   - Production-ready Python script
   - Automatic label collision avoidance via adjustText
   - Supports JSON/CSV input, SVG/PNG/PDF output
   - stdin→stdout pipeline support
   - Flexible column name detection

4. **[examples/model-data-example.json](./examples/model-data-example.json)**
   - Sample JSON input with 33 model data points
   - Based on actual GitHub Models performance data
   - Use to test the visualization script

5. **[examples/model-data-example.csv](./examples/model-data-example.csv)**
   - Same data in CSV format
   - Shows flexible column naming

## 🚀 Quick Start (5 minutes)

```bash
# 1. Install dependencies
pip install matplotlib adjustText pandas

# 2. Test with example data
./plot-models-scatter.py examples/model-data-example.json model-plot.svg

# 3. View output
# Open model-plot.svg in browser or editor
```

## 📊 Research Summary

### ✅ Tools with Collision Avoidance

| Tool | Runtime | Effort | Status |
|:-----|:--------|:-------|:-------|
| **Python matplotlib + adjustText** | Python 3.x | Medium | ⭐ **RECOMMENDED** |
| **R ggplot2 + ggrepel** | R 4.x | Medium-High | ⭐ Alternative |

### ❌ Tools WITHOUT Collision Avoidance

- **Vega-Lite**: JSON-based, great stdin/stdout, but NO collision avoidance
- **Observable Plot**: Modern JS API, but explicitly lacks feature (issue #27)
- **Plotly.js**: `textposition: "auto"` only for single points, not multi-label

### ❓ Not Researched Yet

- **gnuplot**: Likely no collision avoidance
- **Graphviz**: Might work as creative hack (force-directed layout)
- **D3.js force**: Requires custom implementation

## 📖 Use Case

**Problem**: Create scatter plot with ~30-40 labeled points (AI model performance: speed vs quality)

**Critical Requirement**: Labels must NOT overlap each other or data points

**Solution**: Python matplotlib + adjustText
- Iterative force-directed algorithm
- Repels labels from points, edges, and each other
- Configurable repulsion forces
- Production-proven library

## 🔧 Key Features of plot-models-scatter.py

- ✅ **Automatic collision avoidance** (primary requirement)
- ✅ **Flexible input**: JSON or CSV via stdin or file
- ✅ **Multiple output formats**: SVG, PNG, PDF
- ✅ **Auto-detection**: Column names, file types
- ✅ **Customizable**: Size, style, DPI, colors
- ✅ **Pipeline-friendly**: stdin→stdout support
- ✅ **Docker-ready**: Easy containerization

## 📝 Next Steps

1. **Test the script** with example data
2. **Prepare your data** in JSON or CSV format
3. **Generate plot** with your model performance data
4. **Customize** colors, styling, labels as needed
5. **Integrate** into your workflow (scripts, CI/CD, etc.)

## 🔗 Related Files

- [model-research.md](./model-research.md) - GitHub Models API research
- [model-test-state.json](./model-test-state.json) - Test results data source
- [github-copilot-model-test-results.md](./github-copilot-model-test-results.md) - OpenCode model testing

## 💡 Usage Examples

```bash
# Example 1: JSON stdin → SVG stdout
cat examples/model-data-example.json | ./plot-models-scatter.py > output.svg

# Example 2: CSV file → PNG file (high DPI)
./plot-models-scatter.py examples/model-data-example.csv output.png --dpi 600

# Example 3: Custom size and style
./plot-models-scatter.py input.json output.svg --width 16 --height 10 --style seaborn

# Example 4: Docker pipeline
cat data.json | docker run -i plot-tool > chart.svg
```

## ⚙️ Customization

Edit `plot-models-scatter.py` to adjust:

- **Label spacing**: `expand_points=(1.5, 1.5)` in `adjust_text()`
- **Arrow style**: `arrowprops=dict(...)` parameters
- **Colors**: Modify scatter plot `c=` parameter
- **Fonts**: Change `fontsize`, `fontweight` in text creation
- **Grid**: Adjust `ax.grid()` alpha, linestyle
- **Background**: Modify bbox facecolor, edgecolor

See [VISUALIZATION-IMPLEMENTATION.md](./VISUALIZATION-IMPLEMENTATION.md) for detailed customization guide.

---

**Research Status**: ✅ Complete  
**Implementation Status**: ✅ Production-ready script available  
**Last Updated**: October 14, 2025
