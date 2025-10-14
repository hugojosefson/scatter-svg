# Testing Guide

Comprehensive test suite using `pytest` for the scatter-svg package.

## Test Coverage

The test suite (`tests/test_plot.py`) covers:

### 1. File Format Detection

- ✅ CSV detection by `.csv` extension
- ✅ JSON detection by `.json` extension
- ✅ Case-insensitive extension detection
- ✅ Content-based detection (parsing JSON)
- ✅ Fallback to CSV when JSON parsing fails
- ✅ Error handling for unreadable files

### 2. JSON Data Loading

- ✅ Valid JSON file loading
- ✅ JSON from stdin
- ✅ Minimal JSON (points only)
- ✅ JSON with full metadata (title, xlabel, ylabel)
- ✅ Invalid JSON error handling
- ✅ JSON with extra fields

### 3. CSV Data Loading

- ✅ Standard columns (`label`, `x`, `y`)
- ✅ Custom columns (`speed_ms`, `quality_tier`)
- ✅ Alternative label column (`name`)
- ✅ Positional column fallback
- ✅ Multiple rows
- ✅ Float values
- ✅ Labels with spaces

### 4. Integrated File Loading

- ✅ Automatic format detection + loading
- ✅ CSV and JSON routing

### 5. Edge Cases

- ✅ Empty JSON points array
- ✅ Empty CSV file
- ✅ Single data point
- ✅ Missing optional metadata fields
- ✅ Malformed data handling

### 6. Plot Creation

- ✅ Basic scatter plot creation
- ✅ Default labels
- ✅ Custom figure size
- ✅ Custom matplotlib styles

### 7. Figure Saving

- ✅ Save to file
- ✅ Save SVG to stdout
- ✅ Save PNG to stdout
- ✅ Custom DPI settings

### 8. Real File Operations

- ✅ Integration tests with temporary files
- ✅ Real CSV/JSON detection and loading

## Running the Tests

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=scatter_svg --cov-report=html

# Run specific test file
pytest tests/test_plot.py -v
```

The `unittest` module is built into Python, so no additional test dependencies
are needed.

### Run All Tests

```bash
# Basic run (shows dots for each test)
python -m unittest test_plot_models_scatter.py

# Verbose output (shows test names)
python -m unittest test_plot_models_scatter.py -v

# Auto-discover all tests in directory
python -m unittest discover

# Run as script directly
python test_plot_models_scatter.py
```

### Run Specific Test Classes

```bash
# Run only file format detection tests
python -m unittest test_plot_models_scatter.TestFileFormatDetection -v

# Run only JSON loading tests
python -m unittest test_plot_models_scatter.TestJSONLoading -v

# Run only CSV loading tests
python -m unittest test_plot_models_scatter.TestCSVLoading -v

# Run only edge case tests
python -m unittest test_plot_models_scatter.TestEdgeCases -v
```

### Run Specific Individual Tests

```bash
# Run a single test method
python -m unittest test_plot_models_scatter.TestFileFormatDetection.test_detect_csv_by_extension -v
```

## Expected Output

```
============================= test session starts ==============================
platform linux -- Python 3.14.0
collected 40 tests

tests/test_plot.py::TestStdinAutodetection::test_detect_json PASSED
tests/test_plot.py::TestStdinAutodetection::test_detect_csv PASSED
...

============================== 40 passed in 0.50s ==============================
```
test_create_scatter_plot_basic ... ok
test_create_scatter_plot_custom_figsize ... ok
test_create_scatter_plot_custom_style ... ok
test_create_scatter_plot_default_labels ... ok
test_detect_csv_by_content_fallback ... ok
test_detect_csv_by_extension ... ok
test_detect_csv_case_insensitive ... ok
test_detect_csv_on_read_error ... ok
test_detect_json_by_content ... ok
test_detect_json_by_extension ... ok
test_detect_json_case_insensitive ... ok
...

----------------------------------------------------------------------
Ran 40 tests in 0.XXXs

OK
```

### With Failures

```
FAIL: test_something ...
----------------------------------------------------------------------
Traceback (most recent call last):
  ...
AssertionError: Expected X but got Y

----------------------------------------------------------------------
Ran 40 tests in 0.XXXs

FAILED (failures=1)
```

## Test Structure

```
tests/test_plot.py
├── TestStdinAutodetection - Automatic JSON/CSV detection
├── TestFileFormatDetection - Extension-based detection
├── TestJSONLoading - JSON parsing (file + stdin)
├── TestCSVLoading - CSV parsing with flexible columns
├── TestDataFileLoading - Integrated file loading
├── TestEdgeCases - Empty data, malformed input
├── TestScatterPlotCreation - Matplotlib integration
├── TestFigureSaving - Output to file/stdout
└── TestRealFileOperations - Integration with temp files
```

## Mocking Strategy

Tests use `unittest.mock` to avoid external dependencies:

- **File I/O**: Mocked with `mock_open()` and `patch('builtins.open')`
- **Pandas**: Mocked DataFrames returned from `read_csv()`
- **Matplotlib**: Mocked figure/axes objects
- **stdin**: Mocked with `io.StringIO()`

This approach ensures tests run fast, have no side effects, are deterministic, and test logic rather than dependencies.

## Continuous Integration

For CI/CD pipelines:

```bash
# Run tests with proper exit code
pytest tests/
```

See `.github/workflows/ci.yml` for the GitHub Actions setup.

## Coverage Analysis

To measure code coverage:

```bash
# Run tests with coverage
pytest tests/ --cov=scatter_svg --cov-report=html

# View report
open htmlcov/index.html
```

## Troubleshooting

### Import Errors

If you see `ModuleNotFoundError`:

```bash
# Ensure dependencies are installed
pip install -e ".[dev]"
```

## Adding New Tests

To add tests for new functionality:

1. Add test methods to appropriate test class in `tests/test_plot.py`
2. Use descriptive names: `test_<action>_<expected_result>`
3. Add docstrings explaining what the test validates
4. Follow AAA pattern: Arrange, Act, Assert

## Test Philosophy

Tests follow best practices:

- **Unit Tests**: Test individual functions in isolation
- **Mocking**: Avoid external dependencies (files, network)
- **Fast**: All tests run in < 1 second
- **Deterministic**: Same input → same output, always
- **Comprehensive**: Edge cases + happy paths
- **Readable**: Clear names + docstrings

## Dependencies

Development dependencies (defined in `pyproject.toml`):

```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "black>=23.0",
    "ruff>=0.1.0"
]
```

Install with: `pip install -e ".[dev]"`
