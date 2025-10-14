#!/usr/bin/env python3
"""
Comprehensive unit tests for scatter_svg plot module.

Tests cover:
- File format detection (CSV vs JSON)
- CSV data loading
- JSON data loading
- Stdin autodetection (CSV vs JSON)
- Content-based format detection fallback
- Edge cases (empty files, malformed data, etc.)

Run with:
    python -m pytest tests/
    python -m unittest discover tests/
    python -m unittest tests.test_plot -v  # verbose
"""

import unittest
from unittest.mock import mock_open, patch, MagicMock, call
import json
import io
import sys
from pathlib import Path
import tempfile
import os

# Import from scatter_svg package
from scatter_svg.plot import (
    detect_file_format,
    load_csv_file,
    load_json_file,
    load_json_stdin,
    load_stdin,
    load_data_file,
    create_scatter_plot,
    save_figure
)

# For mocking purposes
import scatter_svg.plot as plot_module


class TestFileFormatDetection(unittest.TestCase):
    """Test file format detection based on extension and content."""
    
    def test_detect_csv_by_extension(self):
        """Should detect CSV format from .csv extension."""
        with patch('pathlib.Path.exists', return_value=True):
            format_type = detect_file_format('data.csv')
            self.assertEqual(format_type, 'csv')
    
    def test_detect_json_by_extension(self):
        """Should detect JSON format from .json extension."""
        with patch('pathlib.Path.exists', return_value=True):
            format_type = detect_file_format('data.json')
            self.assertEqual(format_type, 'json')
    
    def test_detect_csv_case_insensitive(self):
        """Should detect CSV format case-insensitively."""
        with patch('pathlib.Path.exists', return_value=True):
            format_type = detect_file_format('data.CSV')
            self.assertEqual(format_type, 'csv')
    
    def test_detect_json_case_insensitive(self):
        """Should detect JSON format case-insensitively."""
        with patch('pathlib.Path.exists', return_value=True):
            format_type = detect_file_format('data.JSON')
            self.assertEqual(format_type, 'json')
    
    def test_detect_json_by_content(self):
        """Should detect JSON format by parsing content when no extension."""
        json_content = '{"points": [{"x": 1, "y": 2, "label": "test"}]}'
        m = mock_open(read_data=json_content)
        
        with patch('builtins.open', m):
            format_type = detect_file_format('data.txt')
            self.assertEqual(format_type, 'json')
    
    def test_detect_csv_by_content_fallback(self):
        """Should default to CSV when JSON parsing fails."""
        csv_content = 'label,x,y\ntest,1,2'
        m = mock_open(read_data=csv_content)
        
        with patch('builtins.open', m):
            format_type = detect_file_format('data.txt')
            self.assertEqual(format_type, 'csv')
    
    def test_detect_csv_on_read_error(self):
        """Should default to CSV on file read errors."""
        with patch('builtins.open', side_effect=IOError("Cannot read file")):
            format_type = detect_file_format('nonexistent.txt')
            self.assertEqual(format_type, 'csv')


class TestJSONLoading(unittest.TestCase):
    """Test JSON data loading from files and stdin."""
    
    def test_load_json_file_valid(self):
        """Should load valid JSON file correctly."""
        json_data = {
            "title": "Test Plot",
            "xlabel": "X Axis",
            "ylabel": "Y Axis",
            "points": [
                {"x": 100, "y": 5, "label": "model-a"},
                {"x": 200, "y": 4, "label": "model-b"}
            ]
        }
        json_content = json.dumps(json_data)
        m = mock_open(read_data=json_content)
        
        with patch('builtins.open', m):
            result = load_json_file('test.json')
            self.assertEqual(result, json_data)
    
    def test_load_json_file_minimal(self):
        """Should load JSON with only points (no metadata)."""
        json_data = {
            "points": [
                {"x": 100, "y": 5, "label": "model-a"}
            ]
        }
        json_content = json.dumps(json_data)
        m = mock_open(read_data=json_content)
        
        with patch('builtins.open', m):
            result = load_json_file('test.json')
            self.assertEqual(result['points'][0]['label'], 'model-a')
    
    def test_load_json_stdin(self):
        """Should load JSON from stdin."""
        json_data = {
            "points": [{"x": 100, "y": 5, "label": "test"}]
        }
        
        with patch('sys.stdin', io.StringIO(json.dumps(json_data))):
            result = load_json_stdin()
            self.assertEqual(result, json_data)
    
    def test_load_json_file_invalid(self):
        """Should raise error on invalid JSON."""
        invalid_json = '{"points": [invalid json'
        m = mock_open(read_data=invalid_json)
        
        with patch('builtins.open', m):
            with self.assertRaises(json.JSONDecodeError):
                load_json_file('invalid.json')


class TestStdinAutodetection(unittest.TestCase):
    """Test stdin autodetection of JSON vs CSV format."""
    
    def test_load_stdin_json(self):
        """Should load JSON from stdin."""
        json_data = {
            "title": "Test Plot",
            "points": [{"x": 100, "y": 5, "label": "model-a"}]
        }
        
        with patch('sys.stdin', io.StringIO(json.dumps(json_data))):
            result = load_stdin()
            self.assertEqual(result, json_data)
            self.assertEqual(result['title'], 'Test Plot')
    
    def test_load_stdin_csv(self):
        """Should load CSV from stdin when JSON parsing fails."""
        csv_content = 'label,x,y\nmodel-a,100,5\nmodel-b,200,4'
        
        with patch('sys.stdin', io.StringIO(csv_content)):
            result = load_stdin()
            self.assertEqual(len(result['points']), 2)
            self.assertEqual(result['points'][0]['label'], 'model-a')
            self.assertEqual(result['points'][0]['x'], 100)
            self.assertEqual(result['points'][0]['y'], 5)
            self.assertEqual(result['xlabel'], 'x')
            self.assertEqual(result['ylabel'], 'y')
    
    def test_load_stdin_csv_custom_columns(self):
        """Should detect custom CSV column names from stdin."""
        csv_content = 'name,speed_ms,quality_tier\nfast-model,556,5\nslow-model,1200,3'
        
        with patch('sys.stdin', io.StringIO(csv_content)):
            result = load_stdin()
            self.assertEqual(len(result['points']), 2)
            self.assertEqual(result['points'][0]['label'], 'fast-model')
            self.assertEqual(result['points'][0]['x'], 556)
            self.assertEqual(result['xlabel'], 'speed_ms')
            self.assertEqual(result['ylabel'], 'quality_tier')
    
    def test_load_stdin_json_minimal(self):
        """Should load minimal JSON (points only) from stdin."""
        json_data = {
            "points": [
                {"x": 100, "y": 5, "label": "test-model"}
            ]
        }
        
        with patch('sys.stdin', io.StringIO(json.dumps(json_data))):
            result = load_stdin()
            self.assertEqual(len(result['points']), 1)
            self.assertEqual(result['points'][0]['label'], 'test-model')
    
    def test_load_stdin_csv_single_row(self):
        """Should load CSV with single data row from stdin."""
        csv_content = 'label,x,y\nsingle-model,150,4'
        
        with patch('sys.stdin', io.StringIO(csv_content)):
            result = load_stdin()
            self.assertEqual(len(result['points']), 1)
            self.assertEqual(result['points'][0]['label'], 'single-model')
    
    def test_load_stdin_csv_with_floats(self):
        """Should handle CSV with float values from stdin."""
        csv_content = 'label,x,y\nmodel-a,123.45,4.8\nmodel-b,234.56,3.2'
        
        with patch('sys.stdin', io.StringIO(csv_content)):
            result = load_stdin()
            self.assertAlmostEqual(result['points'][0]['x'], 123.45)
            self.assertAlmostEqual(result['points'][0]['y'], 4.8)


class TestCSVLoading(unittest.TestCase):
    """Test CSV data loading and column detection."""
    
    def test_load_csv_standard_columns(self):
        """Should load CSV with standard column names (label,x,y)."""
        csv_content = 'label,x,y\nmodel-a,100,5\nmodel-b,200,4'
        
        with patch('pandas.read_csv') as mock_read_csv:
            import pandas as pd
            mock_df = pd.DataFrame({
                'label': ['model-a', 'model-b'],
                'x': [100, 200],
                'y': [5, 4]
            })
            mock_read_csv.return_value = mock_df
            
            result = load_csv_file('test.csv')
            
            self.assertEqual(len(result['points']), 2)
            self.assertEqual(result['points'][0]['label'], 'model-a')
            self.assertEqual(result['points'][0]['x'], 100)
            self.assertEqual(result['points'][0]['y'], 5)
            self.assertEqual(result['xlabel'], 'x')
            self.assertEqual(result['ylabel'], 'y')
    
    def test_load_csv_custom_columns(self):
        """Should detect custom column names (speed_ms, quality_tier)."""
        csv_content = 'label,speed_ms,quality_tier\nmodel-a,556,5'
        
        with patch('pandas.read_csv') as mock_read_csv:
            import pandas as pd
            mock_df = pd.DataFrame({
                'label': ['model-a'],
                'speed_ms': [556],
                'quality_tier': [5]
            })
            mock_read_csv.return_value = mock_df
            
            result = load_csv_file('test.csv')
            
            self.assertEqual(result['points'][0]['x'], 556)
            self.assertEqual(result['points'][0]['y'], 5)
            self.assertEqual(result['xlabel'], 'speed_ms')
            self.assertEqual(result['ylabel'], 'quality_tier')
    
    def test_load_csv_name_column(self):
        """Should detect 'name' as label column."""
        with patch('pandas.read_csv') as mock_read_csv:
            import pandas as pd
            mock_df = pd.DataFrame({
                'name': ['model-a'],
                'time': [100],
                'quality': [5]
            })
            mock_read_csv.return_value = mock_df
            
            result = load_csv_file('test.csv')
            
            self.assertEqual(result['points'][0]['label'], 'model-a')
            self.assertEqual(result['xlabel'], 'time')
            self.assertEqual(result['ylabel'], 'quality')
    
    def test_load_csv_positional_columns(self):
        """Should fall back to positional columns when no match found."""
        with patch('pandas.read_csv') as mock_read_csv:
            import pandas as pd
            mock_df = pd.DataFrame({
                'col1': ['model-a'],
                'col2': [100],
                'col3': [5]
            })
            mock_read_csv.return_value = mock_df
            
            result = load_csv_file('test.csv')
            
            self.assertEqual(result['points'][0]['label'], 'model-a')
            self.assertEqual(result['points'][0]['x'], 100)
            self.assertEqual(result['points'][0]['y'], 5)
    
    def test_load_csv_multiple_rows(self):
        """Should load multiple CSV rows correctly."""
        with patch('pandas.read_csv') as mock_read_csv:
            import pandas as pd
            mock_df = pd.DataFrame({
                'label': ['model-a', 'model-b', 'model-c'],
                'x': [100, 200, 300],
                'y': [5, 4, 5]
            })
            mock_read_csv.return_value = mock_df
            
            result = load_csv_file('test.csv')
            
            self.assertEqual(len(result['points']), 3)
            self.assertEqual(result['points'][2]['label'], 'model-c')
            self.assertEqual(result['points'][2]['x'], 300)


class TestDataFileLoading(unittest.TestCase):
    """Test integrated file loading with automatic format detection."""
    
    def test_load_csv_file_integrated(self):
        """Should load CSV file through load_data_file()."""
        with patch.object(plot_module, 'detect_file_format', return_value='csv'):
            with patch.object(plot_module, 'load_csv_file') as mock_load:
                mock_load.return_value = {'points': []}
                
                result = load_data_file('test.csv')
                
                mock_load.assert_called_once_with('test.csv')
                self.assertEqual(result, {'points': []})
    
    def test_load_json_file_integrated(self):
        """Should load JSON file through load_data_file()."""
        with patch.object(plot_module, 'detect_file_format', return_value='json'):
            with patch.object(plot_module, 'load_json_file') as mock_load:
                mock_load.return_value = {'points': []}
                
                result = load_data_file('test.json')
                
                mock_load.assert_called_once_with('test.json')
                self.assertEqual(result, {'points': []})


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions."""
    
    def test_empty_json_points(self):
        """Should handle JSON with empty points array."""
        json_data = {"points": []}
        json_content = json.dumps(json_data)
        m = mock_open(read_data=json_content)
        
        with patch('builtins.open', m):
            result = load_json_file('empty.json')
            self.assertEqual(result['points'], [])
    
    def test_empty_csv_file(self):
        """Should handle empty CSV file."""
        with patch('pandas.read_csv') as mock_read_csv:
            import pandas as pd
            mock_df = pd.DataFrame(columns=['label', 'x', 'y'])
            mock_read_csv.return_value = mock_df
            
            result = load_csv_file('empty.csv')
            
            self.assertEqual(len(result['points']), 0)
    
    def test_single_point_json(self):
        """Should handle JSON with single point."""
        json_data = {
            "points": [{"x": 100, "y": 5, "label": "only-one"}]
        }
        json_content = json.dumps(json_data)
        m = mock_open(read_data=json_content)
        
        with patch('builtins.open', m):
            result = load_json_file('single.json')
            self.assertEqual(len(result['points']), 1)
    
    def test_json_missing_optional_fields(self):
        """Should handle JSON without title/xlabel/ylabel."""
        json_data = {"points": [{"x": 1, "y": 2, "label": "test"}]}
        json_content = json.dumps(json_data)
        m = mock_open(read_data=json_content)
        
        with patch('builtins.open', m):
            result = load_json_file('minimal.json')
            self.assertNotIn('title', result)
    
    def test_csv_with_spaces_in_names(self):
        """Should handle CSV with spaces in label names."""
        with patch('pandas.read_csv') as mock_read_csv:
            import pandas as pd
            mock_df = pd.DataFrame({
                'label': ['model with spaces', 'another model'],
                'x': [100, 200],
                'y': [5, 4]
            })
            mock_read_csv.return_value = mock_df
            
            result = load_csv_file('test.csv')
            
            self.assertEqual(result['points'][0]['label'], 'model with spaces')
    
    def test_csv_with_float_values(self):
        """Should handle CSV with float x,y values."""
        with patch('pandas.read_csv') as mock_read_csv:
            import pandas as pd
            mock_df = pd.DataFrame({
                'label': ['model-a'],
                'x': [123.45],
                'y': [4.8]
            })
            mock_read_csv.return_value = mock_df
            
            result = load_csv_file('test.csv')
            
            self.assertAlmostEqual(result['points'][0]['x'], 123.45)
            self.assertAlmostEqual(result['points'][0]['y'], 4.8)
    
    def test_json_with_extra_fields(self):
        """Should handle JSON points with extra fields."""
        json_data = {
            "points": [
                {"x": 100, "y": 5, "label": "test", "extra": "ignored"}
            ]
        }
        json_content = json.dumps(json_data)
        m = mock_open(read_data=json_content)
        
        with patch('builtins.open', m):
            result = load_json_file('extra.json')
            # Should still load the essential fields
            self.assertEqual(result['points'][0]['x'], 100)


class TestScatterPlotCreation(unittest.TestCase):
    """Test scatter plot creation logic."""
    
    @patch('scatter_svg.plot.adjust_text')
    @patch('scatter_svg.plot.plt.tight_layout')
    @patch('scatter_svg.plot.plt.subplots')
    def test_create_scatter_plot_basic(self, mock_subplots, mock_tight_layout, mock_adjust_text):
        """Should create scatter plot with basic data."""
        # Mock matplotlib components
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        mock_subplots.return_value = (mock_fig, mock_ax)
        
        data = {
            'points': [
                {'x': 100, 'y': 5, 'label': 'model-a'},
                {'x': 200, 'y': 4, 'label': 'model-b'}
            ],
            'title': 'Test Plot',
            'xlabel': 'X Axis',
            'ylabel': 'Y Axis'
        }
        
        fig = create_scatter_plot(data)
        
        # Verify scatter plot was called
        mock_ax.scatter.assert_called_once()
        
        # Verify labels were set
        mock_ax.set_xlabel.assert_called_once()
        mock_ax.set_ylabel.assert_called_once()
        mock_ax.set_title.assert_called_once()
        
        # Verify adjust_text was called
        mock_adjust_text.assert_called_once()
    
    @patch('scatter_svg.plot.adjust_text')
    @patch('scatter_svg.plot.plt.tight_layout')
    @patch('scatter_svg.plot.plt.subplots')
    def test_create_scatter_plot_default_labels(self, mock_subplots, mock_tight_layout, mock_adjust_text):
        """Should use default labels when not provided."""
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        mock_subplots.return_value = (mock_fig, mock_ax)
        
        data = {
            'points': [{'x': 100, 'y': 5, 'label': 'test'}]
        }
        
        fig = create_scatter_plot(data)
        
        # Check default values were used
        calls = mock_ax.set_xlabel.call_args[0]
        self.assertEqual(calls[0], 'X')
    
    @patch('scatter_svg.plot.adjust_text')
    @patch('scatter_svg.plot.plt.tight_layout')
    @patch('scatter_svg.plot.plt.subplots')
    def test_create_scatter_plot_custom_figsize(self, mock_subplots, mock_tight_layout, mock_adjust_text):
        """Should respect custom figure size."""
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        mock_subplots.return_value = (mock_fig, mock_ax)
        
        data = {'points': [{'x': 100, 'y': 5, 'label': 'test'}]}
        
        fig = create_scatter_plot(data, figsize=(10, 6))
        
        mock_subplots.assert_called_with(figsize=(10, 6))
    
    @patch('scatter_svg.plot.adjust_text')
    @patch('scatter_svg.plot.plt.tight_layout')
    @patch('scatter_svg.plot.plt.style')
    @patch('scatter_svg.plot.plt.subplots')
    def test_create_scatter_plot_custom_style(self, mock_subplots, mock_style, mock_tight_layout, mock_adjust_text):
        """Should apply custom matplotlib style."""
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        mock_subplots.return_value = (mock_fig, mock_ax)
        
        data = {'points': [{'x': 100, 'y': 5, 'label': 'test'}]}
        
        fig = create_scatter_plot(data, style='seaborn')
        
        mock_style.use.assert_called_with('seaborn')


class TestFigureSaving(unittest.TestCase):
    """Test figure saving to file and stdout."""
    
    def test_save_figure_to_file(self):
        """Should save figure to file."""
        mock_fig = MagicMock()
        
        save_figure(mock_fig, 'output.svg', format='svg')
        
        mock_fig.savefig.assert_called_once()
        args = mock_fig.savefig.call_args
        self.assertEqual(args[0][0], 'output.svg')
        self.assertEqual(args[1]['format'], 'svg')
    
    def test_save_figure_svg_to_stdout(self):
        """Should save SVG to stdout."""
        mock_fig = MagicMock()
        output_buffer = io.StringIO()
        
        with patch('sys.stdout', output_buffer):
            with patch('io.StringIO') as mock_stringio:
                mock_io = MagicMock()
                mock_stringio.return_value = mock_io
                mock_io.getvalue.return_value = '<svg>test</svg>'
                
                save_figure(mock_fig, None, format='svg')
    
    def test_save_figure_png_to_stdout(self):
        """Should save PNG to stdout buffer."""
        mock_fig = MagicMock()
        
        with patch('sys.stdout') as mock_stdout:
            mock_stdout.buffer = MagicMock()
            with patch('io.BytesIO') as mock_bytesio:
                mock_io = MagicMock()
                mock_bytesio.return_value = mock_io
                mock_io.getvalue.return_value = b'PNG_DATA'
                
                save_figure(mock_fig, None, format='png')
                
                mock_stdout.buffer.write.assert_called_once()
    
    def test_save_figure_custom_dpi(self):
        """Should respect custom DPI setting."""
        mock_fig = MagicMock()
        
        save_figure(mock_fig, 'output.png', format='png', dpi=150)
        
        args = mock_fig.savefig.call_args
        self.assertEqual(args[1]['dpi'], 150)


class TestRealFileOperations(unittest.TestCase):
    """Test with real temporary files (integration tests)."""
    
    def setUp(self):
        """Create temporary directory for test files."""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_detect_real_csv_file(self):
        """Should detect real CSV file format."""
        csv_path = os.path.join(self.test_dir, 'test.csv')
        with open(csv_path, 'w') as f:
            f.write('label,x,y\ntest,1,2\n')
        
        format_type = detect_file_format(csv_path)
        self.assertEqual(format_type, 'csv')
    
    def test_detect_real_json_file(self):
        """Should detect real JSON file format."""
        json_path = os.path.join(self.test_dir, 'test.json')
        with open(json_path, 'w') as f:
            json.dump({"points": []}, f)
        
        format_type = detect_file_format(json_path)
        self.assertEqual(format_type, 'json')
    
    def test_detect_json_content_no_extension(self):
        """Should detect JSON by content when no extension."""
        file_path = os.path.join(self.test_dir, 'data')
        with open(file_path, 'w') as f:
            json.dump({"points": [{"x": 1, "y": 2, "label": "test"}]}, f)
        
        format_type = detect_file_format(file_path)
        self.assertEqual(format_type, 'json')
    
    def test_load_real_json_file(self):
        """Should load real JSON file."""
        json_path = os.path.join(self.test_dir, 'test.json')
        test_data = {
            "title": "Test",
            "points": [{"x": 100, "y": 5, "label": "model-a"}]
        }
        with open(json_path, 'w') as f:
            json.dump(test_data, f)
        
        result = load_json_file(json_path)
        self.assertEqual(result['title'], 'Test')
        self.assertEqual(len(result['points']), 1)


if __name__ == '__main__':
    # Run tests with verbosity
    unittest.main(verbosity=2)
