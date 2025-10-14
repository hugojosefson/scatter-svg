# Unit Tests for plot-models-scatter.py

Comprehensive test suite using Python's built-in `unittest` framework.

## Test Coverage

The test suite (`test_plot_models_scatter.py`) covers:

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

### Prerequisites

Install dependencies (if not already installed):

```bash
pip install -r requirements.txt
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

### Successful Run (Verbose)

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
test_plot_models_scatter.py
├── TestFileFormatDetection (7 tests)
│   ├── Extension-based detection
│   └── Content-based fallback
├── TestJSONLoading (4 tests)
│   ├── File loading
│   └── Stdin loading
├── TestCSVLoading (6 tests)
│   ├── Column detection
│   └── Data parsing
├── TestDataFileLoading (2 tests)
│   └── Integrated loading
├── TestEdgeCases (7 tests)
│   ├── Empty data
│   ├── Single points
│   └── Malformed input
├── TestScatterPlotCreation (4 tests)
│   └── Matplotlib integration
├── TestFigureSaving (4 tests)
│   └── Output handling
└── TestRealFileOperations (4 tests)
    └── Integration tests
```

## Mocking Strategy

The tests use `unittest.mock` to avoid external dependencies:

- **File I/O**: Mocked with `mock_open()` and `patch('builtins.open')`
- **Pandas**: Mocked DataFrames returned from `read_csv()`
- **Matplotlib**: Mocked figure/axes objects
- **stdin**: Mocked with `io.StringIO()`

This approach:

- ✅ Tests run fast (no actual file I/O)
- ✅ No side effects (no files created)
- ✅ Deterministic (no external state)
- ✅ Tests logic, not dependencies

## Continuous Integration

To integrate with CI/CD pipelines:

```bash
# Run tests and exit with proper code
python -m unittest test_plot_models_scatter.py

# Check exit code
if [ $? -eq 0 ]; then
    echo "All tests passed!"
else
    echo "Tests failed!"
    exit 1
fi
```

## Coverage Analysis (Optional)

To measure code coverage:

```bash
# Install coverage tool
pip install coverage

# Run tests with coverage
coverage run -m unittest test_plot_models_scatter.py

# Generate report
coverage report -m

# Generate HTML report
coverage html
# Open htmlcov/index.html in browser
```

## Troubleshooting

### Import Errors

If you see `ModuleNotFoundError`:

```bash
# Ensure dependencies are installed
pip install matplotlib adjustText pandas

# Ensure you're in the correct directory
cd /path/to/scatter-svg
```

### IDE Warnings

Static analysis tools may show import warnings for:

- `plot_models_scatter`
- `matplotlib`
- `pandas`
- `adjustText`

These are expected and will not affect test execution.

## Adding New Tests

To add tests for new functionality:

1. **Create a new test class**:

```python
class TestNewFeature(unittest.TestCase):
    """Test description."""
    
    def test_something(self):
        """Should do something."""
        result = some_function()
        self.assertEqual(result, expected)
```

2. **Use descriptive names**: `test_<action>_<expected_result>`

3. **Add docstrings**: Brief description of what the test validates

4. **Follow AAA pattern**:
   - **Arrange**: Set up test data
   - **Act**: Call function under test
   - **Assert**: Verify results

## Test Philosophy

These tests follow best practices:

- **Unit Tests**: Test individual functions in isolation
- **Mocking**: Avoid external dependencies (files, network)
- **Fast**: All tests run in < 1 second
- **Deterministic**: Same input → same output, always
- **Comprehensive**: Edge cases + happy paths
- **Readable**: Clear names + docstrings

## Dependencies

```txt
# Production dependencies (required to run tests)
matplotlib>=3.5.0
adjustText>=0.8
pandas>=1.3.0

# Test dependencies (built-in)
unittest (Python standard library)
```

No additional test framework dependencies required!
