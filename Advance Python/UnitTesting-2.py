" UNIT TESTING WITH PY-TEST " # Third-party module
# pytest is a third-party testing framework that’s simpler and more powerful than unittest.
# It provides a more concise syntax for writing tests and supports fixtures, parameterization, and more.
# To use pytest, install it using pip: pip install pytest

# Code to test
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

# Test functions
def test_add():
    assert add(2, 3) == 5  # Assert that 2 + 3 = 5
    assert add(2, 3) != 6  # Assert that 2 + 3 ≠ 6

def test_subtract():
    assert subtract(10, 5) == 5  # Assert that 10 - 5 = 5
    assert subtract(10, 5) != 4  # Assert that 10 - 5 ≠ 4
    
    
" Running pytest "
# To run tests using pytest, create a test file with test functions and run pytest in the terminal.
# pytest will automatically discover and run the test functions.
# To run tests in a specific file, use the command pytest filename.py.

# Features of pytest
# Auto-discovery: Detects test files and functions automatically.
# Fixtures: Replace setUp and tearDown with reusable fixtures.
# Parameterization: Easily test multiple inputs and outputs.

# Fixtures
import pytest # type: ignore

@pytest.fixture
def data():
    return [1, 2, 3]  # Provide reusable data

def test_length(data):
    assert len(data) == 3

def test_first_element(data):
    assert data[0] == 1