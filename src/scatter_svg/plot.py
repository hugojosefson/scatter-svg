#!/usr/bin/env python3
"""
Model Performance Scatter Plot with Collision-Free Labels

Usage:
    # From JSON stdin
    cat models.json | ./plot-models-scatter.py > output.svg

    # From CSV stdin
    cat models.csv | ./plot-models-scatter.py > output.svg

    # From CSV file
    ./plot-models-scatter.py models.csv output.svg

    # From JSON file
    ./plot-models-scatter.py models.json output.svg

Note: stdin input automatically detects JSON vs CSV format

Input Format (JSON):
    {
      "title": "Model Speed vs Quality",
      "xlabel": "Response Time (ms)",
      "ylabel": "Quality Tier",
      "points": [
        {"x": 556, "y": 4, "label": "llama-4-scout"},
        {"x": 666, "y": 5, "label": "gpt-4o-mini"},
        ...
      ]
    }

Input Format (CSV):
    label,x,y
    llama-4-scout,556,4
    gpt-4o-mini,666,5
    ...

Dependencies:
    pip install matplotlib adjustText pandas

Author: OpenCode Visualization Research
Date: October 14, 2025
"""

import sys
import json
import io
import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from adjustText import adjust_text
import pandas as pd


def load_stdin():
    """
    Load data from stdin with automatic format detection.

    Tries to parse as JSON first, falls back to CSV if JSON parsing fails.

    Returns:
        Dict with 'points', 'title', 'xlabel', 'ylabel'
    """
    # Read all stdin content once
    stdin_content = sys.stdin.read()

    # Try parsing as JSON first
    try:
        data = json.loads(stdin_content)
        return data
    except json.JSONDecodeError:
        # Fall back to CSV parsing
        csv_buffer = io.StringIO(stdin_content)
        df = pd.read_csv(csv_buffer)

        # Detect column names (same logic as load_csv_file)
        label_col = next(
            (c for c in df.columns if "label" in c.lower() or "name" in c.lower()), df.columns[0]
        )
        x_col = next(
            (
                c
                for c in df.columns
                if "x" in c.lower() or "speed" in c.lower() or "time" in c.lower()
            ),
            df.columns[1],
        )
        y_col = next(
            (
                c
                for c in df.columns
                if "y" in c.lower() or "quality" in c.lower() or "tier" in c.lower()
            ),
            df.columns[2],
        )

        return {
            "points": [
                {"label": row[label_col], "x": row[x_col], "y": row[y_col]}
                for _, row in df.iterrows()
            ],
            "xlabel": x_col,
            "ylabel": y_col,
            "title": "Scatter Plot",
        }


def load_json_stdin():
    """Load JSON data from stdin (deprecated - use load_stdin instead)."""
    return json.load(sys.stdin)


def load_json_file(filepath):
    """Load JSON data from file."""
    with open(filepath) as f:
        return json.load(f)


def load_csv_file(filepath):
    """Load CSV data and convert to expected format."""
    df = pd.read_csv(filepath)

    # Detect column names (flexible)
    label_col = next(
        (c for c in df.columns if "label" in c.lower() or "name" in c.lower()), df.columns[0]
    )
    x_col = next(
        (c for c in df.columns if "x" in c.lower() or "speed" in c.lower() or "time" in c.lower()),
        df.columns[1],
    )
    y_col = next(
        (
            c
            for c in df.columns
            if "y" in c.lower() or "quality" in c.lower() or "tier" in c.lower()
        ),
        df.columns[2],
    )

    return {
        "points": [
            {"label": row[label_col], "x": row[x_col], "y": row[y_col]} for _, row in df.iterrows()
        ],
        "xlabel": x_col,
        "ylabel": y_col,
        "title": "Scatter Plot",
    }


def detect_file_format(filepath):
    """
    Automatically detect if file is CSV or JSON based on extension and content.

    Args:
        filepath: Path to the input file

    Returns:
        'csv' or 'json'
    """
    path = Path(filepath)

    # First, check file extension
    if path.suffix.lower() == ".csv":
        return "csv"
    elif path.suffix.lower() == ".json":
        return "json"

    # No recognized extension - detect from content
    try:
        with open(filepath, "r") as f:
            content = f.read().strip()

        # Try to parse as JSON first
        try:
            json.loads(content)
            return "json"
        except json.JSONDecodeError:
            # If JSON fails, assume CSV
            return "csv"
    except Exception:
        # Default to CSV if we can't read the file
        return "csv"


def load_data_file(filepath):
    """
    Load data from file, automatically detecting CSV or JSON format.

    Args:
        filepath: Path to input file (CSV or JSON)

    Returns:
        Dict with 'points', 'title', 'xlabel', 'ylabel'
    """
    file_format = detect_file_format(filepath)

    if file_format == "csv":
        return load_csv_file(filepath)
    else:
        return load_json_file(filepath)


def create_scatter_plot(data, figsize=(12, 8), style="default"):
    """
    Create scatter plot with collision-free labels.

    Args:
        data: Dict with 'points', optional 'title', 'xlabel', 'ylabel'
        figsize: Tuple of (width, height) in inches
        style: Matplotlib style ('default', 'seaborn', 'ggplot', etc.)

    Returns:
        matplotlib Figure object
    """
    # Apply style
    if style != "default":
        plt.style.use(style)

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Extract data
    points = data["points"]
    x_values = [p["x"] for p in points]
    y_values = [p["y"] for p in points]
    labels = [p["label"] for p in points]

    # Color by quality tier if y-values are discrete
    unique_y = sorted(set(y_values))
    if len(unique_y) <= 10:  # Assume discrete tiers
        colors = plt.cm.viridis([y_values.index(y) / len(unique_y) for y in y_values])
    else:
        colors = "steelblue"

    # Plot scatter points
    scatter = ax.scatter(
        x_values, y_values, s=100, c=colors, alpha=0.6, edgecolors="white", linewidth=1.5, zorder=2
    )

    # Add labels with collision avoidance
    texts = [
        ax.text(
            x,
            y,
            label,
            fontsize=8,
            ha="center",
            va="center",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="none", alpha=0.7),
        )
        for x, y, label in zip(x_values, y_values, labels)
    ]

    # Adjust text positions to avoid overlaps
    adjust_text(
        texts,
        arrowprops=dict(arrowstyle="->", color="gray", lw=0.5, alpha=0.5),
        expand_points=(1.5, 1.5),  # How much to repel from points
        expand_text=(1.2, 1.2),  # How much to repel from other text
        force_points=(0.5, 0.5),  # Force multiplier for point repulsion
        force_text=(0.5, 0.5),  # Force multiplier for text repulsion
        lim=500,  # Max iterations
    )

    # Styling
    ax.set_xlabel(data.get("xlabel", "X"), fontsize=12, fontweight="bold")
    ax.set_ylabel(data.get("ylabel", "Y"), fontsize=12, fontweight="bold")
    ax.set_title(data.get("title", "Scatter Plot"), fontsize=14, fontweight="bold", pad=20)

    # Grid
    ax.grid(True, alpha=0.3, linestyle="--", linewidth=0.5, zorder=1)
    ax.set_axisbelow(True)

    # Format y-axis if discrete tiers
    if len(unique_y) <= 10:
        ax.set_yticks(unique_y)
        ax.set_yticklabels([f"Tier {int(y)}" if y == int(y) else str(y) for y in unique_y])

    # Tight layout
    plt.tight_layout()

    return fig


def save_figure(fig, output_path=None, format="svg", dpi=300):
    """
    Save figure to file or stdout.

    Args:
        fig: matplotlib Figure object
        output_path: Path to save (None = stdout)
        format: 'svg', 'png', or 'pdf'
        dpi: Resolution for raster formats (PNG)
    """
    if output_path:
        # Save to file
        fig.savefig(output_path, format=format, dpi=dpi, bbox_inches="tight")
    else:
        # Save to stdout
        if format == "png":
            output = io.BytesIO()
            fig.savefig(output, format=format, dpi=dpi, bbox_inches="tight")
            sys.stdout.buffer.write(output.getvalue())
        else:
            output = io.StringIO()
            fig.savefig(output, format=format, dpi=dpi, bbox_inches="tight")
            sys.stdout.write(output.getvalue())


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Create scatter plot with collision-free labels",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("input", nargs="?", help="Input file (JSON or CSV), or read from stdin")
    parser.add_argument("output", nargs="?", help="Output file (SVG, PNG, PDF), or write to stdout")
    parser.add_argument(
        "--width", type=float, default=12, help="Figure width in inches (default: 12)"
    )
    parser.add_argument(
        "--height", type=float, default=8, help="Figure height in inches (default: 8)"
    )
    parser.add_argument(
        "--style", default="default", help="Matplotlib style (default, seaborn, ggplot, etc.)"
    )
    parser.add_argument(
        "--format", choices=["svg", "png", "pdf"], help="Output format (auto-detect from filename)"
    )
    parser.add_argument("--dpi", type=int, default=300, help="DPI for PNG output (default: 300)")

    args = parser.parse_args()

    # Load data
    if not args.input or args.input == "-":
        # Read from stdin (autodetect JSON or CSV)
        data = load_stdin()
    else:
        # Read from file (automatically detect format)
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: File not found: {args.input}", file=sys.stderr)
            sys.exit(1)

        # Automatically detect and load CSV or JSON
        data = load_data_file(input_path)

    # Determine output format
    if args.output:
        output_format = args.format or Path(args.output).suffix.lstrip(".") or "svg"
    else:
        output_format = args.format or "svg"

    # Create plot
    fig = create_scatter_plot(data, figsize=(args.width, args.height), style=args.style)

    # Save plot
    save_figure(fig, args.output, format=output_format, dpi=args.dpi)

    # Close figure to free memory
    plt.close(fig)


if __name__ == "__main__":
    main()
