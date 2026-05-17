# Phiton Tests

This directory contains tests for the Phiton package.

## Test Structure

- `conftest.py`: pytest fixtures and configuration
- `test_*.py`: Test files for different modules
- `data/`: Test data files
  - `simple.py`: Basic functionality test file
  - `complex.py`: Advanced features test file
  - `patterns.py`: Pattern recognition test file
  - `expected/`: Expected output files for comparison

## Running Tests

Install test dependencies:

```bash
pip install -r tests/requirements.txt
```

Run all tests from the project root:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=phiton
```

Run a specific test file:

```bash
pytest tests/test_converter.py
```

Run a specific test function:

```bash
pytest tests/test_converter.py::test_compress_simple_level1
```

## Adding New Tests

1. Add test data to `data/`
2. Add expected outputs to `data/expected/`
3. Write test functions in the appropriate test file
4. Use existing fixtures from `conftest.py` when possible

## Test Coverage

Tests cover:

- Configuration options
- Compression functionality
- Utility functions
- CLI commands
- Error handling