"""
scatter-svg: Scatter Plot Generator with Automatic Label Collision Avoidance

A Python tool using matplotlib + adjustText for creating collision-free scatter plots
with professional-quality output.
"""

__version__ = "1.0.0"

from scatter_svg.plot import (
    load_stdin,
    load_json_stdin,
    load_json_file,
    load_csv_file,
    load_data_file,
    detect_file_format,
    create_scatter_plot,
    save_figure,
)

__all__ = [
    "load_stdin",
    "load_json_stdin",
    "load_json_file",
    "load_csv_file",
    "load_data_file",
    "detect_file_format",
    "create_scatter_plot",
    "save_figure",
]
