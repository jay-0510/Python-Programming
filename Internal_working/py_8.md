# 🐍 Python Testing — Complete Guide
### Pytest · Unittest · Fixtures · Mocking · Coverage · BDD/TDD and More
---

## 📖 How This File Flows

```
PART 1 — FOUNDATIONS
  1.  Why Testing? What Problem It Solves
  2.  Testing Terminology You Must Know
  3.  TDD and BDD — Approach and Mindset

PART 2 — UNITTEST (Standard Library)
  4.  unittest basics — structure, run, assert methods
  5.  setUp and tearDown — test lifecycle
  6.  Two-file example: main.py + test_main.py

PART 3 — PYTEST (Recommended Framework)
  7.  Why pytest over unittest?
  8.  Writing pytest tests — all conventions
  9.  Assertions in pytest — how they work under the hood
  10. Fixtures — setup, teardown, scope
  11. Parametrize — run one test with many inputs
  12. Two-file example: main.py + test_main.py

PART 4 — MOCKING AND PATCHING
  13. What is mocking and why?
  14. unittest.mock — patch, MagicMock
  15. Mocking in pytest

PART 5 — TEST DISCOVERY AND COVERAGE
  16. How test discovery works
  17. Code coverage — measuring what's tested

PART 6 — TESTING TYPES (Know the Terminology)
  18. Unit Testing vs Integration Testing
  19. Regression Testing
  20. Smoke Testing
  21. Performance and Load Testing — glance
  22. API Testing — glance
  23. Doctest

PART 7 — COMPLETE PROJECT EXAMPLE
  24. Full project: two-file structure, all concepts together
```

---

# PART 1 — FOUNDATIONS

---

## 1. Why Testing? The Problem It Solves

Imagine you have a working payment system. You add a discount feature. Next morning: payments are broken. Without tests, you spend 3 hours debugging. With tests, you know in 5 seconds exactly which function broke.

```
WITHOUT TESTS:
  Write code → deploy → user reports bug → debug → fix → maybe breaks something else
  Loop forever. No confidence. Every deploy is scary.

WITH TESTS:
  Write code → run tests → fail → fix → tests pass → deploy with confidence
  Tests tell you WHAT broke, WHERE, immediately.
```

**What tests give you:**
- **Confidence** — change anything, tests tell you if something broke
- **Documentation** — tests show HOW to use your code
- **Design feedback** — hard-to-test code usually means poor design
- **Regression prevention** — fixed bugs stay fixed

---

## 2. Testing Terminology You Must Know

```
Unit Test:        Tests ONE function/method in isolation
Integration Test: Tests multiple components working together
End-to-End Test:  Tests the entire flow (UI → API → DB → response)
Regression Test:  Re-runs existing tests after changes to catch regressions
Smoke Test:       Quick check: is the basic system alive? (before full test run)
Load Test:        How does the system perform under heavy traffic?

Test Case:    One specific test (one function in your test file)
Test Suite:   A collection of test cases
Test Runner:  The tool that executes tests (pytest, unittest runner)
Fixture:      Setup code that runs before/after tests (DB connection, test data)
Mock/Stub:    A fake object that replaces a real one during testing
Assert:       A check — did the result match what we expected?
Coverage:     What % of your code is actually executed by tests?
```

---

## 3. TDD and BDD — Approach and Mindset

### TDD — Test-Driven Development

```
RED → GREEN → REFACTOR

1. RED:    Write a failing test for a feature that doesn't exist yet
2. GREEN:  Write the minimum code to make the test pass
3. REFACTOR: Clean up the code while keeping tests green

Example flow:
  Task: "Add a discount function"

  Step 1 (RED): Write test
    def test_apply_discount():
        assert apply_discount(1000, 10) == 900   # fails — function doesn't exist

  Step 2 (GREEN): Write function
    def apply_discount(price, percent):
        return price - (price * percent / 100)   # test passes

  Step 3 (REFACTOR): Make it cleaner, validate inputs, etc.
```

**Why TDD?**
- Forces you to think about the API before the implementation
- Guarantees tests exist for every feature
- Catches edge cases early

### BDD — Behaviour-Driven Development

```
BDD = TDD written in plain English terms that non-developers can read

Uses Given / When / Then structure:

  Feature: User Login

  Scenario: Successful login
    Given the user has a valid account
    When they enter correct credentials
    Then they receive a session token

Tools: pytest-bdd, Behave (Python BDD framework)
```

```python
# BDD style naming (no special library needed — just naming convention)
def test_given_valid_credentials_when_login_then_returns_token():
    # Given
    user = {"username": "arjun", "password": "secret123"}

    # When
    result = login(user["username"], user["password"])

    # Then
    assert "token" in result
    assert result["token"] is not None
```

---

# PART 2 — UNITTEST (Standard Library)

---

## 4. unittest Basics

`unittest` is Python's built-in testing framework. No installation needed.

```
Structure:
  - Inherit from unittest.TestCase
  - Each test is a method starting with test_
  - Use self.assertXxx() methods for assertions
  - Run with: python -m unittest test_file.py
              python -m unittest discover
```

### All unittest Assertion Methods

```python
# Equality
self.assertEqual(a, b)        # a == b
self.assertNotEqual(a, b)     # a != b

# Truth
self.assertTrue(x)            # bool(x) is True
self.assertFalse(x)           # bool(x) is False

# Identity
self.assertIs(a, b)           # a is b
self.assertIsNot(a, b)        # a is not b
self.assertIsNone(x)          # x is None
self.assertIsNotNone(x)       # x is not None

# Membership
self.assertIn(a, b)           # a in b
self.assertNotIn(a, b)        # a not in b

# Type
self.assertIsInstance(a, T)   # isinstance(a, T)

# Comparison
self.assertGreater(a, b)      # a > b
self.assertLess(a, b)         # a < b
self.assertGreaterEqual(a, b) # a >= b
self.assertLessEqual(a, b)    # a <= b

# Approximation (for floats!)
self.assertAlmostEqual(a, b, places=7)  # a ≈ b
self.assertAlmostEqual(0.1 + 0.2, 0.3, places=5)  # True

# Containers
self.assertListEqual(a, b)
self.assertDictEqual(a, b)
self.assertSetEqual(a, b)

# Exceptions
self.assertRaises(ValueError, func, arg)
with self.assertRaises(ValueError):
    func(bad_arg)

# Regex
self.assertRaisesRegex(ValueError, "must be positive", func, -1)
```

---

## 5. setUp and tearDown — Test Lifecycle

```
Test lifecycle in unittest:

  setUpClass()    → runs ONCE before ALL tests in this class
  setUp()         → runs BEFORE EACH test method
  test_xxx()      → the actual test
  tearDown()      → runs AFTER EACH test method
  tearDownClass() → runs ONCE after ALL tests in this class

Use setUp/tearDown for: creating test data, DB connections, temp files
Use tearDown for: cleanup — deleting temp files, closing connections
```

```python
import unittest

class TestShoppingCart(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Runs ONCE before all tests. Use for expensive setup (DB connection)."""
        print("\n--- Starting ShoppingCart tests ---")

    @classmethod
    def tearDownClass(cls):
        """Runs ONCE after all tests."""
        print("\n--- ShoppingCart tests complete ---")

    def setUp(self):
        """Runs before EACH test. Fresh cart for every test."""
        self.cart = ShoppingCart()
        self.cart.add("Laptop", 50000, 1)

    def tearDown(self):
        """Runs after EACH test. Cleanup."""
        self.cart = None

    def test_add_item(self):
        self.cart.add("Mouse", 800, 2)
        self.assertEqual(len(self.cart), 2)

    def test_remove_item(self):
        self.cart.remove("Laptop")
        self.assertEqual(len(self.cart), 0)

    def test_total(self):
        self.assertEqual(self.cart.total, 50000)
```

---

## 6. Two-File Example — unittest

### `main.py` — The Code Being Tested

```python
# main.py
"""
Simple e-commerce utility functions.
This is the code we are testing.
"""

class InsufficientFundsError(Exception):
    pass

class ItemNotFoundError(Exception):
    pass


class ShoppingCart:
    def __init__(self):
        self._items = {}   # {name: {"price": x, "qty": y}}

    def add(self, name: str, price: float, qty: int = 1):
        if price <= 0:
            raise ValueError("Price must be positive")
        if qty <= 0:
            raise ValueError("Quantity must be positive")
        if name in self._items:
            self._items[name]["qty"] += qty
        else:
            self._items[name] = {"price": price, "qty": qty}

    def remove(self, name: str):
        if name not in self._items:
            raise ItemNotFoundError(f"'{name}' not in cart")
        del self._items[name]

    def __len__(self):
        return len(self._items)

    @property
    def total(self) -> float:
        return sum(v["price"] * v["qty"] for v in self._items.values())

    @property
    def item_count(self) -> int:
        return sum(v["qty"] for v in self._items.values())

    def apply_discount(self, percent: float) -> float:
        if not 0 < percent <= 100:
            raise ValueError("Discount must be between 0 and 100")
        return self.total * (1 - percent / 100)

    def is_empty(self) -> bool:
        return len(self._items) == 0


def calculate_tax(amount: float, rate: float = 0.18) -> float:
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    if not 0 <= rate <= 1:
        raise ValueError("Tax rate must be between 0 and 1")
    return round(amount * rate, 2)


def format_price(amount: float, currency: str = "INR") -> str:
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    symbols = {"INR": "₹", "USD": "$", "EUR": "€"}
    symbol = symbols.get(currency, currency)
    return f"{symbol}{amount:,.2f}"
```

---

### `test_main_unittest.py` — unittest Tests

```python
# test_main_unittest.py
"""
Tests for main.py using Python's built-in unittest framework.

Run with:
  python -m unittest test_main_unittest.py        # run this file
  python -m unittest test_main_unittest.py -v     # verbose output
  python -m unittest discover                     # auto-discover all test files
"""

import unittest
from main import ShoppingCart, calculate_tax, format_price, ItemNotFoundError


class TestShoppingCartAdd(unittest.TestCase):
    """Tests for adding items to cart."""

    def setUp(self):
        """Fresh cart before each test."""
        self.cart = ShoppingCart()

    # ── Happy path ──────────────────────────────────────────────

    def test_add_single_item(self):
        self.cart.add("Laptop", 50000)
        self.assertEqual(len(self.cart), 1)

    def test_add_multiple_items(self):
        self.cart.add("Laptop", 50000)
        self.cart.add("Mouse",  800)
        self.cart.add("Bag",    1500)
        self.assertEqual(len(self.cart), 3)

    def test_add_same_item_increases_quantity(self):
        self.cart.add("Laptop", 50000, 1)
        self.cart.add("Laptop", 50000, 2)
        self.cart._items["Laptop"]["qty"] == 3

    def test_add_item_with_quantity(self):
        self.cart.add("Pen", 10, 5)
        self.assertEqual(self.cart.item_count, 5)

    # ── Validation ──────────────────────────────────────────────

    def test_add_negative_price_raises_error(self):
        with self.assertRaises(ValueError):
            self.cart.add("Laptop", -100)

    def test_add_zero_price_raises_error(self):
        with self.assertRaises(ValueError):
            self.cart.add("Free Item", 0)

    def test_add_zero_quantity_raises_error(self):
        with self.assertRaises(ValueError):
            self.cart.add("Laptop", 50000, 0)

    def test_add_negative_quantity_raises_error(self):
        with self.assertRaises(ValueError):
            self.cart.add("Laptop", 50000, -1)

    # Error message check
    def test_negative_price_error_message(self):
        with self.assertRaisesRegex(ValueError, "Price must be positive"):
            self.cart.add("Laptop", -100)


class TestShoppingCartRemove(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()
        self.cart.add("Laptop", 50000)
        self.cart.add("Mouse",  800)

    def test_remove_existing_item(self):
        self.cart.remove("Laptop")
        self.assertEqual(len(self.cart), 1)

    def test_remove_non_existent_item_raises(self):
        with self.assertRaises(ItemNotFoundError):
            self.cart.remove("Keyboard")

    def test_cart_empty_after_removing_all(self):
        self.cart.remove("Laptop")
        self.cart.remove("Mouse")
        self.assertTrue(self.cart.is_empty())


class TestShoppingCartTotal(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()

    def test_total_single_item(self):
        self.cart.add("Laptop", 50000, 1)
        self.assertEqual(self.cart.total, 50000)

    def test_total_multiple_items(self):
        self.cart.add("Laptop", 50000, 1)
        self.cart.add("Mouse",  800,   2)
        # 50000 + (800 * 2) = 51600
        self.assertEqual(self.cart.total, 51600)

    def test_total_empty_cart(self):
        self.assertEqual(self.cart.total, 0)

    def test_apply_discount(self):
        self.cart.add("Laptop", 10000)
        discounted = self.cart.apply_discount(10)  # 10% off
        self.assertEqual(discounted, 9000)

    def test_apply_invalid_discount_raises(self):
        self.cart.add("Laptop", 10000)
        with self.assertRaises(ValueError):
            self.cart.apply_discount(0)
        with self.assertRaises(ValueError):
            self.cart.apply_discount(110)


class TestCalculateTax(unittest.TestCase):

    def test_standard_tax(self):
        self.assertEqual(calculate_tax(1000), 180.0)   # 18% default

    def test_custom_rate(self):
        self.assertEqual(calculate_tax(1000, 0.05), 50.0)

    def test_zero_amount(self):
        self.assertEqual(calculate_tax(0), 0.0)

    def test_negative_amount_raises(self):
        with self.assertRaises(ValueError):
            calculate_tax(-100)

    def test_invalid_rate_raises(self):
        with self.assertRaises(ValueError):
            calculate_tax(1000, 1.5)   # rate > 1

    def test_float_result_precision(self):
        # Float arithmetic: use assertAlmostEqual for floats
        result = calculate_tax(333)   # 333 * 0.18 = 59.94
        self.assertAlmostEqual(result, 59.94, places=2)


class TestFormatPrice(unittest.TestCase):

    def test_format_inr(self):
        self.assertEqual(format_price(1500), "₹1,500.00")

    def test_format_usd(self):
        self.assertEqual(format_price(1500, "USD"), "$1,500.00")

    def test_format_large_number(self):
        self.assertEqual(format_price(1000000), "₹10,00,000.00")  # or 1,000,000.00

    def test_negative_amount_raises(self):
        with self.assertRaises(ValueError):
            format_price(-100)

    def test_unknown_currency_uses_code(self):
        result = format_price(100, "JPY")
        self.assertIn("JPY", result)


if __name__ == "__main__":
    # Run with: python test_main_unittest.py
    unittest.main(verbosity=2)
```

**Running:**
```bash
# Run all tests
python -m unittest test_main_unittest.py

# Verbose output (shows each test name)
python -m unittest test_main_unittest.py -v

# Output:
# test_add_multiple_items (TestShoppingCartAdd) ... ok
# test_add_negative_price_raises_error (TestShoppingCartAdd) ... ok
# ...
# Ran 24 tests in 0.003s
# OK
```

---

# PART 3 — PYTEST (Recommended Framework)

---

## 7. Why pytest Over unittest?

```
unittest:                           pytest:
  class TestFoo(unittest.TestCase)    def test_foo():
    def test_bar(self):                   result = bar()
        self.assertEqual(...)             assert result == expected
        self.assertRaises(...)            with pytest.raises(...)

Verbose, class-based                  Simple functions
self.assertXxx() everywhere           Just use assert
More boilerplate                      Less boilerplate
Hard-to-read failures                 Beautiful, detailed failure messages
```

```python
# unittest failure message:
# AssertionError: 180.0 != 200.0

# pytest failure message:
# FAILED test_main.py::test_calculate_tax
# E   AssertionError: assert 180.0 == 200.0
# E    +  where 180.0 = calculate_tax(1000)
#
# ↑ pytest shows you EXACTLY what was called and what it returned
```

**Install:**
```bash
pip install pytest
pip install pytest-cov          # coverage
pip install pytest-mock         # better mocking
```

---

## 8. Writing pytest Tests — All Conventions

```python
# File must be named:  test_something.py  OR  something_test.py
# Function must start with: test_
# Class must start with: Test (no inheritance needed)

# Simplest possible test:
def test_addition():
    assert 1 + 1 == 2

# Class grouping (optional but useful for organization):
class TestCalculator:
    def test_add(self):
        assert add(2, 3) == 5

    def test_divide(self):
        assert divide(10, 2) == 5.0
```

---

## 9. Assertions in pytest — How They Work

pytest rewrites your `assert` statements at collection time (AST transformation) to produce detailed failure messages.

```python
# You write:
assert calculate_tax(1000) == 200

# pytest rewrites it internally to capture both sides:
# → assert 180.0 == 200  (shows the actual value returned)

# ── All assertion patterns ──────────────────────────────────────

# Equality
assert result == 42
assert result != 42

# Truth
assert is_active
assert not is_banned

# None
assert result is None
assert result is not None

# Membership
assert "error" in response
assert key in my_dict
assert item not in blacklist

# Type
assert isinstance(result, dict)

# Approximate floats — NEVER assert 0.1 + 0.2 == 0.3!
import pytest
result = 0.1 + 0.2
assert result == pytest.approx(0.3)            # ✅ handles float imprecision
assert result == pytest.approx(0.3, rel=1e-3)  # relative tolerance
assert result == pytest.approx(0.3, abs=1e-6)  # absolute tolerance

# Exceptions
with pytest.raises(ValueError):
    calculate_tax(-100)

with pytest.raises(ValueError, match="cannot be negative"):
    calculate_tax(-100)   # also checks error message contains this string

# Check exception info
with pytest.raises(ValueError) as exc_info:
    calculate_tax(-100)
assert "negative" in str(exc_info.value)
```

---

## 10. Fixtures — The pytest Superpower

Fixtures are functions that set up (and tear down) test resources. They're the pytest equivalent of `setUp`/`tearDown` but far more powerful.

```python
import pytest

@pytest.fixture
def empty_cart():
    """Provides a fresh empty cart."""
    return ShoppingCart()

@pytest.fixture
def cart_with_items():
    """Provides a cart with pre-loaded items."""
    cart = ShoppingCart()
    cart.add("Laptop", 50000, 1)
    cart.add("Mouse",  800,   2)
    return cart

# Use fixtures by adding them as function parameters
def test_empty_cart_total(empty_cart):
    assert empty_cart.total == 0

def test_cart_item_count(cart_with_items):
    assert cart_with_items.item_count == 3   # 1 laptop + 2 mice
```

### Fixture with Teardown

```python
@pytest.fixture
def temp_file(tmp_path):
    """Creates a temp file and cleans up after test."""
    file = tmp_path / "test_data.csv"
    file.write_text("name,price\nLaptop,50000\nMouse,800")

    yield file          # ← test runs here with 'file' available

    # Everything after yield runs AFTER the test (teardown)
    # tmp_path is automatically cleaned up by pytest, but
    # for databases, connections, etc. you'd do cleanup here
    print(f"Cleaned up {file}")


def test_read_csv(temp_file):
    content = temp_file.read_text()
    assert "Laptop" in content
```

### Fixture Scope — How Long It Lives

```python
# scope="function" (default) — new instance per test function
# scope="class"              — one instance per test class
# scope="module"             — one instance per test file
# scope="session"            — one instance for the entire test run

@pytest.fixture(scope="session")
def db_connection():
    """Real DB connection — created once for entire test run."""
    conn = create_db_connection()
    yield conn
    conn.close()   # cleanup once at end

@pytest.fixture(scope="module")
def api_client():
    """API client — created once per test file."""
    return TestClient()

@pytest.fixture(scope="function")  # default
def cart():
    """Fresh cart for each test."""
    return ShoppingCart()
```

### `conftest.py` — Shared Fixtures

Put fixtures used across multiple test files in `conftest.py` at the project root. pytest discovers it automatically.

```python
# conftest.py  (no import needed — pytest loads it automatically)
import pytest
from main import ShoppingCart

@pytest.fixture
def empty_cart():
    return ShoppingCart()

@pytest.fixture
def sample_products():
    return [
        {"name": "Laptop", "price": 50000},
        {"name": "Mouse",  "price": 800},
        {"name": "Bag",    "price": 1500},
    ]
```

### Built-in pytest Fixtures

```python
# tmp_path: temporary directory (unique per test, auto-cleaned)
def test_file_writing(tmp_path):
    f = tmp_path / "output.txt"
    f.write_text("hello")
    assert f.read_text() == "hello"

# capsys: capture stdout/stderr
def test_print_output(capsys):
    print("Hello World")
    captured = capsys.readouterr()
    assert captured.out == "Hello World\n"

# monkeypatch: safely modify objects, environment variables, etc.
def test_env_variable(monkeypatch):
    monkeypatch.setenv("DB_HOST", "test-server")
    import os
    assert os.environ["DB_HOST"] == "test-server"
    # automatically reverted after the test
```

---

## 11. Parametrize — One Test, Many Inputs

Instead of writing the same test structure 10 times with different values, use `@pytest.mark.parametrize`.

```python
import pytest
from main import calculate_tax

# ── Without parametrize — repetitive ────────────────────────────
def test_tax_1000():
    assert calculate_tax(1000) == 180.0

def test_tax_500():
    assert calculate_tax(500) == 90.0

def test_tax_0():
    assert calculate_tax(0) == 0.0

# ── With parametrize — clean ─────────────────────────────────────
@pytest.mark.parametrize("amount, expected", [
    (1000, 180.0),
    (500,   90.0),
    (0,      0.0),
    (333,   59.94),
    (10000, 1800.0),
])
def test_calculate_tax(amount, expected):
    assert calculate_tax(amount) == pytest.approx(expected, abs=0.01)


# Multiple parameters
@pytest.mark.parametrize("amount, rate, expected", [
    (1000, 0.18,  180.0),
    (1000, 0.05,   50.0),
    (1000, 0.28,  280.0),
    (500,  0.12,   60.0),
])
def test_calculate_tax_with_rate(amount, rate, expected):
    assert calculate_tax(amount, rate) == pytest.approx(expected, abs=0.01)


# Parametrize with IDs (makes test output readable)
@pytest.mark.parametrize("price, expected", [
    pytest.param(1500,    "₹1,500.00",    id="normal"),
    pytest.param(0,       "₹0.00",        id="zero"),
    pytest.param(1000000, "₹10,00,000.00",id="large"),
], ids=lambda x: str(x))
def test_format_price_parametrized(price, expected):
    assert format_price(price) == expected
```

**Output:**
```
test_calculate_tax[1000-180.0]  PASSED
test_calculate_tax[500-90.0]    PASSED
test_calculate_tax[0-0.0]       PASSED
test_calculate_tax[333-59.94]   PASSED
test_calculate_tax[10000-1800.0] PASSED
```

---

## 12. Two-File Example — pytest

### `main.py` — Same as before (or new version)

```python
# main.py
"""
Order processing system.
"""
from decimal import Decimal


class OrderError(Exception):
    pass

class ItemNotFoundError(OrderError):
    pass

class PaymentError(OrderError):
    pass


class Product:
    def __init__(self, name: str, price: float, stock: int = 100):
        if price <= 0:
            raise ValueError("Price must be positive")
        self.name  = name
        self.price = round(float(price), 2)
        self.stock = stock

    def __repr__(self):
        return f"Product({self.name!r}, {self.price})"


class Order:
    def __init__(self, customer: str):
        if not customer or not customer.strip():
            raise ValueError("Customer name is required")
        self.customer = customer.strip()
        self._items   = {}    # {product_name: {"product": Product, "qty": int}}
        self.status   = "pending"

    def add_item(self, product: Product, qty: int = 1):
        if qty <= 0:
            raise ValueError("Quantity must be positive")
        if product.stock < qty:
            raise OrderError(f"Only {product.stock} '{product.name}' in stock")
        if product.name in self._items:
            self._items[product.name]["qty"] += qty
        else:
            self._items[product.name] = {"product": product, "qty": qty}

    def remove_item(self, product_name: str):
        if product_name not in self._items:
            raise ItemNotFoundError(f"'{product_name}' not in order")
        del self._items[product_name]

    @property
    def subtotal(self) -> float:
        return round(sum(
            v["product"].price * v["qty"]
            for v in self._items.values()
        ), 2)

    @property
    def tax(self) -> float:
        return round(self.subtotal * 0.18, 2)

    @property
    def total(self) -> float:
        return round(self.subtotal + self.tax, 2)

    def apply_coupon(self, code: str) -> float:
        coupons = {"SAVE10": 10, "HALF50": 50, "FLAT100": 5}
        if code not in coupons:
            raise ValueError(f"Invalid coupon: {code!r}")
        discount_pct = coupons[code]
        return round(self.total * (1 - discount_pct / 100), 2)

    def confirm(self):
        if not self._items:
            raise OrderError("Cannot confirm empty order")
        self.status = "confirmed"

    def cancel(self):
        if self.status == "delivered":
            raise OrderError("Cannot cancel delivered order")
        self.status = "cancelled"

    def __len__(self):
        return len(self._items)

    def is_empty(self) -> bool:
        return len(self._items) == 0


def process_payment(amount: float, method: str) -> dict:
    """
    Simulate payment processing.
    In production this would call a payment gateway API.
    """
    valid_methods = ["card", "upi", "netbanking", "wallet"]
    if method not in valid_methods:
        raise PaymentError(f"Invalid payment method: {method!r}")
    if amount <= 0:
        raise PaymentError("Amount must be positive")
    return {
        "status":         "success",
        "transaction_id": f"TXN{int(amount * 100):010d}",
        "amount":         amount,
        "method":         method,
    }
```

---

### `test_main_pytest.py` — pytest Tests

```python
# test_main_pytest.py
"""
Tests for main.py using pytest.

Run with:
  pytest test_main_pytest.py           # run this file
  pytest test_main_pytest.py -v        # verbose
  pytest test_main_pytest.py -v -s     # show print output too
  pytest test_main_pytest.py -k "tax"  # only tests with 'tax' in name
  pytest                               # auto-discover all test files
"""

import pytest
from main import Product, Order, process_payment, ItemNotFoundError, OrderError, PaymentError


# ══════════════════════════════════════════════════════════════════
# FIXTURES
# ══════════════════════════════════════════════════════════════════

@pytest.fixture
def laptop():
    return Product("Laptop", 50000, stock=10)

@pytest.fixture
def mouse():
    return Product("Mouse", 800, stock=50)

@pytest.fixture
def empty_order():
    return Order("Arjun")

@pytest.fixture
def order_with_items(empty_order, laptop, mouse):
    """Order pre-loaded with items."""
    empty_order.add_item(laptop, 1)
    empty_order.add_item(mouse, 2)
    return empty_order


# ══════════════════════════════════════════════════════════════════
# PRODUCT TESTS
# ══════════════════════════════════════════════════════════════════

class TestProduct:

    def test_create_product(self):
        p = Product("Keyboard", 1500)
        assert p.name  == "Keyboard"
        assert p.price == 1500.0

    def test_price_rounded_to_2_decimals(self):
        p = Product("Item", 99.999)
        assert p.price == 100.0

    def test_negative_price_raises(self):
        with pytest.raises(ValueError, match="Price must be positive"):
            Product("Item", -100)

    def test_zero_price_raises(self):
        with pytest.raises(ValueError):
            Product("Item", 0)

    def test_repr(self, laptop):
        assert "Laptop" in repr(laptop)


# ══════════════════════════════════════════════════════════════════
# ORDER ADD ITEM TESTS
# ══════════════════════════════════════════════════════════════════

class TestOrderAddItem:

    def test_add_single_item(self, empty_order, laptop):
        empty_order.add_item(laptop)
        assert len(empty_order) == 1

    def test_add_multiple_items(self, order_with_items):
        assert len(order_with_items) == 2

    def test_add_same_item_increases_qty(self, empty_order, laptop):
        empty_order.add_item(laptop, 1)
        empty_order.add_item(laptop, 2)
        assert empty_order._items["Laptop"]["qty"] == 3

    def test_add_zero_qty_raises(self, empty_order, laptop):
        with pytest.raises(ValueError, match="Quantity must be positive"):
            empty_order.add_item(laptop, 0)

    def test_add_more_than_stock_raises(self, empty_order, laptop):
        # laptop has stock=10
        with pytest.raises(OrderError, match="Only 10"):
            empty_order.add_item(laptop, 15)

    def test_add_item_empty_order_check(self, empty_order):
        assert empty_order.is_empty()


# ══════════════════════════════════════════════════════════════════
# ORDER TOTALS — PARAMETRIZED
# ══════════════════════════════════════════════════════════════════

class TestOrderTotals:

    def test_subtotal(self, order_with_items):
        # laptop(50000*1) + mouse(800*2) = 51600
        assert order_with_items.subtotal == 51600.0

    def test_tax_is_18_percent(self, order_with_items):
        expected_tax = round(51600 * 0.18, 2)
        assert order_with_items.tax == pytest.approx(expected_tax, abs=0.01)

    def test_total_is_subtotal_plus_tax(self, order_with_items):
        assert order_with_items.total == pytest.approx(
            order_with_items.subtotal + order_with_items.tax, abs=0.01
        )

    def test_empty_order_subtotal(self, empty_order):
        assert empty_order.subtotal == 0

    @pytest.mark.parametrize("coupon, expected_total", [
        ("SAVE10",  round(51600 * 1.18 * 0.90, 2)),   # 10% off
        ("HALF50",  round(51600 * 1.18 * 0.50, 2)),   # 50% off
    ])
    def test_apply_coupon(self, order_with_items, coupon, expected_total):
        result = order_with_items.apply_coupon(coupon)
        assert result == pytest.approx(expected_total, abs=0.01)

    def test_invalid_coupon_raises(self, order_with_items):
        with pytest.raises(ValueError, match="Invalid coupon"):
            order_with_items.apply_coupon("FAKE99")


# ══════════════════════════════════════════════════════════════════
# ORDER STATUS TESTS
# ══════════════════════════════════════════════════════════════════

class TestOrderStatus:

    def test_initial_status_is_pending(self, empty_order):
        assert empty_order.status == "pending"

    def test_confirm_order(self, order_with_items):
        order_with_items.confirm()
        assert order_with_items.status == "confirmed"

    def test_confirm_empty_order_raises(self, empty_order):
        with pytest.raises(OrderError, match="Cannot confirm empty order"):
            empty_order.confirm()

    def test_cancel_order(self, order_with_items):
        order_with_items.cancel()
        assert order_with_items.status == "cancelled"

    def test_cancel_delivered_raises(self, order_with_items):
        order_with_items.status = "delivered"
        with pytest.raises(OrderError, match="Cannot cancel delivered"):
            order_with_items.cancel()


# ══════════════════════════════════════════════════════════════════
# PAYMENT TESTS — PARAMETRIZED
# ══════════════════════════════════════════════════════════════════

class TestPayment:

    @pytest.mark.parametrize("method", ["card", "upi", "netbanking", "wallet"])
    def test_valid_payment_methods(self, method):
        result = process_payment(1000, method)
        assert result["status"] == "success"
        assert result["amount"] == 1000
        assert result["method"] == method

    def test_payment_returns_transaction_id(self):
        result = process_payment(500, "upi")
        assert "transaction_id" in result
        assert result["transaction_id"].startswith("TXN")

    def test_invalid_method_raises(self):
        with pytest.raises(PaymentError, match="Invalid payment method"):
            process_payment(1000, "bitcoin")

    def test_zero_amount_raises(self):
        with pytest.raises(PaymentError, match="Amount must be positive"):
            process_payment(0, "card")

    @pytest.mark.parametrize("amount", [-100, -1, -0.01])
    def test_negative_amounts_raise(self, amount):
        with pytest.raises(PaymentError):
            process_payment(amount, "card")


# ══════════════════════════════════════════════════════════════════
# ORDER CREATION EDGE CASES
# ══════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("bad_customer", ["", "   ", None])
def test_empty_customer_raises(bad_customer):
    if bad_customer is None:
        with pytest.raises((ValueError, TypeError)):
            Order(bad_customer)
    else:
        with pytest.raises(ValueError):
            Order(bad_customer)
```

**Running:**
```bash
pytest test_main_pytest.py -v

# Output:
# PASSED test_main_pytest.py::TestProduct::test_create_product
# PASSED test_main_pytest.py::TestProduct::test_price_rounded_to_2_decimals
# ...
# PASSED test_main_pytest.py::TestPayment::test_valid_payment_methods[card]
# PASSED test_main_pytest.py::TestPayment::test_valid_payment_methods[upi]
# ...
# 35 passed in 0.12s
```

---

# PART 4 — MOCKING AND PATCHING

---

## 13. What Is Mocking and Why?

```
Problem: Your code calls external things — payment APIs, databases, email services.
         You don't want to actually hit these in tests.
         - They're slow
         - They cost money (real API calls)
         - They might not be available
         - You can't control what they return

Solution: Replace the real thing with a MOCK — a fake that behaves how you tell it to.
```

```
MOCK:    A fake object. You control what it returns, what it raises.
PATCH:   Temporarily replace an object/function with a mock for the duration of a test.
STUB:    A simple fake that returns hardcoded values.
SPY:     A mock that also records calls (so you can assert it was called).
```

---

## 14. unittest.mock

```python
from unittest.mock import Mock, MagicMock, patch, call

# ── Basic Mock ───────────────────────────────────────────────────
mock = Mock()
mock.return_value = 42         # set what it returns when called
print(mock())                  # 42

mock.some_method.return_value = "hello"
print(mock.some_method())      # hello

# Mock can be called any way — it won't raise AttributeError
mock.anything.at.all.returns_a_mock()   # works fine

# ── Check how it was called ──────────────────────────────────────
mock = Mock(return_value=100)
mock(1, 2, key="value")

mock.assert_called_once()
mock.assert_called_with(1, 2, key="value")
print(mock.call_count)         # 1
print(mock.call_args)          # call(1, 2, key='value')
```

---

## 15. Mocking in pytest — Real Examples

### `main.py` with External Dependencies

```python
# main.py  (extended with external calls)

import smtplib
import requests   # pip install requests

def send_welcome_email(to_email: str, username: str) -> bool:
    """
    Send welcome email via SMTP.
    In tests: we don't want to actually send emails.
    """
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.sendmail("noreply@app.com", to_email, f"Welcome {username}!")
        server.quit()
        return True
    except Exception:
        return False


def fetch_product_from_api(product_id: int) -> dict:
    """
    Fetch product from external API.
    In tests: we don't want to actually call the API.
    """
    response = requests.get(f"https://api.example.com/products/{product_id}")
    response.raise_for_status()
    return response.json()


def register_user(username: str, email: str, db) -> dict:
    """
    Register a user. Uses a database object.
    In tests: we mock the db.
    """
    if db.user_exists(email):
        raise ValueError(f"User with email {email!r} already exists")
    user_id = db.create_user(username, email)
    send_welcome_email(email, username)
    return {"id": user_id, "username": username, "email": email}
```

### `test_mocking.py` — All Mocking Patterns

```python
# test_mocking.py
"""
Shows mocking patterns for pytest.

Install: pip install pytest-mock
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, call


# ══════════════════════════════════════════════════════════════════
# PATTERN 1: Mock a database object passed as argument
# ══════════════════════════════════════════════════════════════════

from main import register_user

def test_register_new_user():
    """Mock the database — we don't need a real DB for this test."""
    mock_db = Mock()
    mock_db.user_exists.return_value = False   # user doesn't exist yet
    mock_db.create_user.return_value = 42      # returns new user_id

    with patch("main.send_welcome_email", return_value=True):
        result = register_user("arjun", "a@b.com", mock_db)

    assert result["id"] == 42
    assert result["username"] == "arjun"

    # Verify DB was called correctly
    mock_db.user_exists.assert_called_once_with("a@b.com")
    mock_db.create_user.assert_called_once_with("arjun", "a@b.com")


def test_register_duplicate_email_raises():
    """If email exists, should raise ValueError."""
    mock_db = Mock()
    mock_db.user_exists.return_value = True    # email already taken

    with pytest.raises(ValueError, match="already exists"):
        register_user("arjun", "taken@b.com", mock_db)

    # create_user should NEVER be called if email already exists
    mock_db.create_user.assert_not_called()


# ══════════════════════════════════════════════════════════════════
# PATTERN 2: Patch with @patch decorator
# ══════════════════════════════════════════════════════════════════

from unittest.mock import patch
from main import send_welcome_email

@patch("main.smtplib.SMTP")   # replace smtplib.SMTP with a mock
def test_send_welcome_email_success(mock_smtp):
    """Email sends successfully — no real SMTP connection."""
    # mock_smtp is the Mock replacing smtplib.SMTP
    mock_server = Mock()
    mock_smtp.return_value = mock_server   # SMTP("...") returns mock_server

    result = send_welcome_email("user@example.com", "Arjun")

    assert result is True
    mock_smtp.assert_called_once_with("smtp.gmail.com", 587)
    mock_server.sendmail.assert_called_once()


@patch("main.smtplib.SMTP")
def test_send_email_fails_on_smtp_error(mock_smtp):
    """If SMTP raises, email returns False."""
    mock_smtp.side_effect = ConnectionError("SMTP server unavailable")

    result = send_welcome_email("user@example.com", "Arjun")

    assert result is False


# ══════════════════════════════════════════════════════════════════
# PATTERN 3: Patch requests (HTTP call)
# ══════════════════════════════════════════════════════════════════

from main import fetch_product_from_api

@patch("main.requests.get")
def test_fetch_product_success(mock_get):
    """Mock HTTP response — no real API call."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "id": 1, "name": "Laptop", "price": 50000
    }
    mock_response.raise_for_status.return_value = None   # no error
    mock_get.return_value = mock_response

    result = fetch_product_from_api(1)

    assert result["name"] == "Laptop"
    assert result["price"] == 50000
    mock_get.assert_called_once_with("https://api.example.com/products/1")


@patch("main.requests.get")
def test_fetch_product_api_error(mock_get):
    """If API returns 404, raise_for_status raises HTTPError."""
    import requests
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
    mock_get.return_value = mock_response

    with pytest.raises(requests.HTTPError):
        fetch_product_from_api(999)


# ══════════════════════════════════════════════════════════════════
# PATTERN 4: pytest-mock's mocker fixture (cleaner syntax)
# ══════════════════════════════════════════════════════════════════

def test_with_mocker(mocker):
    """mocker fixture from pytest-mock — no decorators needed."""
    mock_get = mocker.patch("main.requests.get")

    mock_response = Mock()
    mock_response.json.return_value = {"id": 2, "name": "Mouse", "price": 800}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = fetch_product_from_api(2)
    assert result["name"] == "Mouse"


# ══════════════════════════════════════════════════════════════════
# PATTERN 5: Mock side_effect — different return per call
# ══════════════════════════════════════════════════════════════════

def test_mock_multiple_calls():
    mock_fn = Mock()
    mock_fn.side_effect = [10, 20, 30]   # returns 10 first, 20 second, 30 third

    assert mock_fn() == 10
    assert mock_fn() == 20
    assert mock_fn() == 30

def test_mock_raises_on_call():
    mock_fn = Mock(side_effect=ValueError("bad input"))
    with pytest.raises(ValueError, match="bad input"):
        mock_fn()
```

---

# PART 5 — TEST DISCOVERY AND COVERAGE

---

## 16. Test Discovery — How pytest Finds Your Tests

```
pytest searches for tests automatically:

1. Starting from current directory (or path you give it)
2. Recurses into subdirectories
3. Looks for files matching:   test_*.py  OR  *_test.py
4. Inside those files, finds:
   - Functions starting with:  test_
   - Classes starting with:    Test
   - Methods starting with:    test_

Standard project structure:
  project/
  ├── src/
  │   ├── main.py
  │   └── utils.py
  ├── tests/
  │   ├── conftest.py          ← shared fixtures
  │   ├── test_main.py
  │   └── test_utils.py
  ├── pytest.ini               ← pytest configuration
  └── requirements.txt
```

### `pytest.ini` — Configuration File

```ini
# pytest.ini
[pytest]
testpaths = tests          # where to look for tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short    # always run verbose with short tracebacks
```

### Running Specific Tests

```bash
pytest                                     # all tests
pytest tests/                             # tests in specific folder
pytest tests/test_main.py                 # specific file
pytest tests/test_main.py::TestProduct    # specific class
pytest tests/test_main.py::TestProduct::test_create_product  # specific test
pytest -k "payment"                       # tests with 'payment' in name
pytest -k "not slow"                      # exclude tests marked 'slow'
pytest -m "integration"                   # only tests marked 'integration'
pytest --lf                               # only last failed tests
pytest -x                                 # stop on first failure
pytest -v                                 # verbose output
```

### Marking Tests

```python
import pytest

@pytest.mark.slow
def test_heavy_computation():
    # Takes 10 seconds
    pass

@pytest.mark.integration
def test_real_database():
    pass

@pytest.mark.skip(reason="API not available in CI")
def test_external_api():
    pass

@pytest.mark.skipif(condition, reason="Only runs on Linux")
def test_linux_only():
    pass
```

---

## 17. Code Coverage

Coverage tells you: **what percentage of your code is actually executed by tests?**

```bash
pip install pytest-cov

# Run tests with coverage
pytest --cov=main tests/                       # measure coverage of main.py
pytest --cov=main --cov-report=term-missing    # show which lines are missed
pytest --cov=main --cov-report=html            # generate HTML report
```

### Coverage Report Example

```
---------- coverage: platform linux, python 3.11 -----------
Name      Stmts   Miss  Cover   Missing
-----------------------------------------
main.py      87      4    95%   45, 89-91
-----------------------------------------
TOTAL        87      4    95%

Lines 45, 89-91 in main.py are NOT covered by any test.
```

### `.coveragerc` — Coverage Configuration

```ini
# .coveragerc
[run]
source = src
omit =
    tests/*
    */__init__.py

[report]
exclude_lines =
    if __name__ == "__main__"
    raise NotImplementedError
    pass
```

---

# PART 6 — TESTING TYPES

---

## 18. Unit vs Integration Testing

```python
# UNIT TEST — tests ONE function in isolation
# All dependencies are mocked

def test_calculate_tax_unit():
    # Only tests calculate_tax. No DB, no API, no file system.
    assert calculate_tax(1000) == 180.0


# INTEGRATION TEST — tests multiple components together
# Uses real dependencies (or test versions of them)

def test_order_and_payment_integration(tmp_path):
    """
    Tests Order + Payment working together.
    Uses real objects, no mocking.
    """
    laptop = Product("Laptop", 50000)
    order  = Order("Arjun")
    order.add_item(laptop)
    order.confirm()

    result = process_payment(order.total, "upi")   # real function, no mock

    assert result["status"] == "success"
    assert result["amount"] == order.total
    assert order.status == "confirmed"
```

---

## 19. Regression Testing

```
Regression = a bug that was fixed but came back after a code change.

Regression tests = tests you write specifically to prevent known bugs
                   from coming back.

Every time you fix a bug → write a test that would have caught it.
```

```python
# Bug report: "Discount of exactly 100% should be invalid but it was allowed"
# Fix: change condition from `percent > 100` to `percent >= 100`
# Regression test: write a test that would have caught this bug

def test_regression_100_percent_discount_should_raise():
    """
    Regression test: Bug #42 — 100% discount was incorrectly allowed.
    Fixed in commit abc123. This test ensures it stays fixed.
    """
    cart = ShoppingCart()
    cart.add("Laptop", 50000)
    with pytest.raises(ValueError):
        cart.apply_discount(100)   # 100% discount = free = not allowed


# Naming convention: mention the bug it covers
def test_regression_empty_customer_name_bug_101():
    """Bug #101: empty string was accepted as customer name."""
    with pytest.raises(ValueError):
        Order("")
```

---

## 20. Smoke Testing

```
Smoke test = quick sanity check: "Is the system alive?"
Run before full test suite or after deployment.

Named after hardware testing: turn on the device,
if it doesn't smoke, proceed to detailed tests.
```

```python
# smoke_tests.py — quick basic checks
import pytest

class TestSmoke:
    """Quick smoke tests — runs in under 1 second."""

    def test_product_can_be_created(self):
        p = Product("Test", 100)
        assert p is not None

    def test_order_can_be_created(self):
        o = Order("Test User")
        assert o is not None

    def test_payment_function_exists_and_callable(self):
        assert callable(process_payment)

    def test_basic_order_flow(self):
        """The most basic happy path. If this fails, stop everything."""
        p = Product("Item", 100)
        o = Order("Customer")
        o.add_item(p)
        o.confirm()
        assert o.status == "confirmed"
```

```bash
# Run only smoke tests (fast feedback)
pytest -m smoke tests/smoke_tests.py
```

---

## 21. Performance and Load Testing — Glance

```
Performance Test: Does the function complete within acceptable time?
Load Test:        What happens under heavy concurrent traffic?

Tools:
  pytest-benchmark  — measure function execution time
  locust            — simulate many concurrent users
  k6                — load testing tool
```

```python
# Performance test with pytest-benchmark
# pip install pytest-benchmark

def test_order_total_performance(benchmark, order_with_items):
    """Total calculation should complete in under 1ms."""
    result = benchmark(order_with_items.total)
    # benchmark runs the function many times and reports stats
    # Mean, median, min, max, stddev

# Load test concept (with locust):
# from locust import HttpUser, task
# class ShopUser(HttpUser):
#     @task
#     def view_product(self):
#         self.client.get("/products/1")
```

---

## 22. API Testing — Glance

```
Test your REST API endpoints directly.
Check: correct status codes, correct response body, correct headers.

Tools:
  httpx         — sync/async HTTP client for testing
  requests      — simple HTTP client
  FastAPI TestClient — built-in test client for FastAPI apps
```

```python
# Minimal FastAPI app (app.py)
from fastapi import FastAPI
app = FastAPI()

@app.get("/products/{pid}")
def get_product(pid: int):
    return {"id": pid, "name": "Laptop", "price": 50000}

@app.post("/orders")
def create_order(data: dict):
    return {"order_id": 1, **data, "status": "pending"}


# test_api.py
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_get_product():
    response = client.get("/products/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Laptop"

def test_create_order():
    payload = {"customer": "Arjun", "product_id": 1}
    response = client.post("/orders", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "pending"

def test_product_not_found():
    response = client.get("/products/9999")
    assert response.status_code == 404
```

---

## 23. Doctest — Tests Inside Docstrings

```python
def calculate_tax(amount: float, rate: float = 0.18) -> float:
    """
    Calculate tax on an amount.

    Args:
        amount: The base amount.
        rate:   Tax rate as decimal. Default 0.18 (18%).

    Returns:
        Tax amount.

    Examples:
        >>> calculate_tax(1000)
        180.0
        >>> calculate_tax(500, 0.05)
        25.0
        >>> calculate_tax(0)
        0.0
        >>> calculate_tax(-100)
        Traceback (most recent call last):
            ...
        ValueError: Amount cannot be negative
    """
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    return round(amount * rate, 2)
```

```bash
# Run doctests
python -m doctest main.py -v
pytest --doctest-modules main.py
```

---

# PART 7 — COMPLETE PROJECT EXAMPLE

---

## 24. Full Project: Two Files, All Concepts

### Project Structure

```
ecommerce/
├── main.py          ← production code
├── test_main.py     ← all tests
├── conftest.py      ← shared fixtures
└── pytest.ini       ← configuration
```

### `conftest.py`

```python
# conftest.py
import pytest
from main import Product, Order

@pytest.fixture
def laptop():
    return Product("Laptop", 50000, stock=10)

@pytest.fixture
def mouse():
    return Product("Mouse", 800, stock=50)

@pytest.fixture
def headphones():
    return Product("Headphones", 2999, stock=5)

@pytest.fixture
def empty_order():
    return Order("Test Customer")

@pytest.fixture
def loaded_order(empty_order, laptop, mouse):
    empty_order.add_item(laptop, 1)
    empty_order.add_item(mouse, 2)
    return empty_order
```

### `main.py` — Complete Final Version

```python
# main.py
"""
E-commerce order system.
All functions and classes used across tests.
"""

class OrderError(Exception): pass
class ItemNotFoundError(OrderError): pass
class PaymentError(OrderError): pass


class Product:
    def __init__(self, name: str, price: float, stock: int = 100):
        if not name or not name.strip():
            raise ValueError("Product name is required")
        if price <= 0:
            raise ValueError("Price must be positive")
        if stock < 0:
            raise ValueError("Stock cannot be negative")
        self.name  = name.strip()
        self.price = round(float(price), 2)
        self.stock = stock

    def reduce_stock(self, qty: int):
        if qty > self.stock:
            raise OrderError(f"Not enough stock for {self.name}")
        self.stock -= qty

    def __repr__(self):
        return f"Product({self.name!r}, ₹{self.price}, stock={self.stock})"


class Order:
    def __init__(self, customer: str):
        if not customer or not customer.strip():
            raise ValueError("Customer name is required")
        self.customer = customer.strip()
        self._items   = {}
        self.status   = "pending"

    def add_item(self, product: Product, qty: int = 1):
        if qty <= 0:
            raise ValueError("Quantity must be positive")
        if product.stock < qty:
            raise OrderError(f"Only {product.stock} '{product.name}' in stock")
        if product.name in self._items:
            self._items[product.name]["qty"] += qty
        else:
            self._items[product.name] = {"product": product, "qty": qty}

    def remove_item(self, name: str):
        if name not in self._items:
            raise ItemNotFoundError(f"'{name}' not in order")
        del self._items[name]

    def get_item(self, name: str) -> dict:
        if name not in self._items:
            raise ItemNotFoundError(f"'{name}' not in order")
        return self._items[name]

    @property
    def subtotal(self) -> float:
        return round(sum(v["product"].price * v["qty"] for v in self._items.values()), 2)

    @property
    def tax(self) -> float:
        return round(self.subtotal * 0.18, 2)

    @property
    def total(self) -> float:
        return round(self.subtotal + self.tax, 2)

    def apply_coupon(self, code: str) -> float:
        coupons = {"SAVE10": 10, "SAVE20": 20, "HALF50": 50}
        if code not in coupons:
            raise ValueError(f"Invalid coupon: {code!r}")
        return round(self.total * (1 - coupons[code] / 100), 2)

    def confirm(self):
        if not self._items:
            raise OrderError("Cannot confirm empty order")
        self.status = "confirmed"

    def cancel(self):
        if self.status == "delivered":
            raise OrderError("Cannot cancel a delivered order")
        self.status = "cancelled"

    def __len__(self):
        return len(self._items)

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __repr__(self):
        return f"Order({self.customer!r}, {len(self)} items, ₹{self.total})"


def process_payment(amount: float, method: str) -> dict:
    valid_methods = ["card", "upi", "netbanking", "wallet"]
    if method not in valid_methods:
        raise PaymentError(f"Invalid payment method: {method!r}")
    if amount <= 0:
        raise PaymentError("Amount must be positive")
    return {
        "status":         "success",
        "transaction_id": f"TXN{int(amount * 100):010d}",
        "amount":         amount,
        "method":         method,
    }


def send_order_confirmation(email: str, order) -> bool:
    """Sends confirmation email. In production: calls SMTP/SendGrid."""
    import smtplib
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.sendmail("noreply@shop.com", email, f"Order confirmed: {order}")
        server.quit()
        return True
    except Exception:
        return False
```

### `test_main.py` — Complete Final Tests

```python
# test_main.py
"""
Complete test suite for main.py.
Covers: unit tests, fixtures, parametrize, mocking, regression, smoke.

Run:  pytest test_main.py -v
Run with coverage: pytest test_main.py -v --cov=main --cov-report=term-missing
"""

import pytest
from unittest.mock import Mock, patch
from main import (
    Product, Order, process_payment, send_order_confirmation,
    ItemNotFoundError, OrderError, PaymentError
)


# ══════════════════════════════════════════════════════════════════
# SMOKE TESTS — "Is the system alive?" — run these first
# ══════════════════════════════════════════════════════════════════

@pytest.mark.smoke
class TestSmoke:
    def test_product_creation(self):
        assert Product("Item", 100) is not None

    def test_order_creation(self):
        assert Order("Customer") is not None

    def test_basic_flow(self, laptop, empty_order):
        empty_order.add_item(laptop)
        empty_order.confirm()
        assert empty_order.status == "confirmed"


# ══════════════════════════════════════════════════════════════════
# PRODUCT TESTS
# ══════════════════════════════════════════════════════════════════

class TestProduct:

    @pytest.mark.parametrize("name, price, stock", [
        ("Laptop",  50000, 10),
        ("Mouse",   800,   50),
        ("Charger", 499.99, 0),  # zero stock is valid
    ])
    def test_valid_product_creation(self, name, price, stock):
        p = Product(name, price, stock)
        assert p.name  == name
        assert p.price == round(float(price), 2)
        assert p.stock == stock

    @pytest.mark.parametrize("bad_name", ["", "   ", None])
    def test_empty_name_raises(self, bad_name):
        with pytest.raises((ValueError, TypeError)):
            Product(bad_name, 100)

    @pytest.mark.parametrize("bad_price", [0, -1, -999.99])
    def test_invalid_price_raises(self, bad_price):
        with pytest.raises(ValueError, match="Price must be positive"):
            Product("Item", bad_price)

    def test_reduce_stock(self, laptop):
        initial = laptop.stock
        laptop.reduce_stock(3)
        assert laptop.stock == initial - 3

    def test_reduce_stock_below_zero_raises(self, laptop):
        with pytest.raises(OrderError):
            laptop.reduce_stock(laptop.stock + 1)


# ══════════════════════════════════════════════════════════════════
# ORDER TESTS
# ══════════════════════════════════════════════════════════════════

class TestOrderItems:

    def test_add_item(self, empty_order, laptop):
        empty_order.add_item(laptop)
        assert len(empty_order) == 1
        assert not empty_order.is_empty()

    def test_add_multiple_unique_items(self, loaded_order):
        assert len(loaded_order) == 2

    def test_add_same_item_accumulates_qty(self, empty_order, laptop):
        empty_order.add_item(laptop, 1)
        empty_order.add_item(laptop, 3)
        assert empty_order._items["Laptop"]["qty"] == 4

    def test_add_exceeds_stock_raises(self, empty_order, headphones):
        # headphones has stock=5
        with pytest.raises(OrderError, match="Only 5"):
            empty_order.add_item(headphones, 10)

    def test_remove_item(self, loaded_order):
        loaded_order.remove_item("Laptop")
        assert len(loaded_order) == 1

    def test_remove_nonexistent_item_raises(self, empty_order):
        with pytest.raises(ItemNotFoundError, match="not in order"):
            empty_order.remove_item("Ghost Item")

    def test_get_item(self, loaded_order):
        item = loaded_order.get_item("Laptop")
        assert item["product"].name == "Laptop"
        assert item["qty"] == 1

    def test_get_nonexistent_item_raises(self, loaded_order):
        with pytest.raises(ItemNotFoundError):
            loaded_order.get_item("Nonexistent")


class TestOrderFinancials:

    def test_subtotal(self, loaded_order):
        # Laptop(50000*1) + Mouse(800*2) = 51600
        assert loaded_order.subtotal == 51600.0

    def test_tax_18_percent(self, loaded_order):
        assert loaded_order.tax == pytest.approx(51600 * 0.18, abs=0.01)

    def test_total_is_subtotal_plus_tax(self, loaded_order):
        assert loaded_order.total == pytest.approx(
            loaded_order.subtotal + loaded_order.tax, abs=0.01
        )

    def test_empty_order_all_zeros(self, empty_order):
        assert empty_order.subtotal == 0
        assert empty_order.tax      == 0
        assert empty_order.total    == 0

    @pytest.mark.parametrize("coupon, discount_pct", [
        ("SAVE10", 10),
        ("SAVE20", 20),
        ("HALF50", 50),
    ])
    def test_apply_coupon(self, loaded_order, coupon, discount_pct):
        expected = round(loaded_order.total * (1 - discount_pct / 100), 2)
        assert loaded_order.apply_coupon(coupon) == pytest.approx(expected, abs=0.01)

    def test_invalid_coupon_raises(self, loaded_order):
        with pytest.raises(ValueError, match="Invalid coupon"):
            loaded_order.apply_coupon("FAKE99")


class TestOrderStatus:

    def test_default_status(self, empty_order):
        assert empty_order.status == "pending"

    def test_confirm(self, loaded_order):
        loaded_order.confirm()
        assert loaded_order.status == "confirmed"

    def test_confirm_empty_raises(self, empty_order):
        with pytest.raises(OrderError, match="empty order"):
            empty_order.confirm()

    def test_cancel_pending_order(self, loaded_order):
        loaded_order.cancel()
        assert loaded_order.status == "cancelled"

    def test_cancel_confirmed_order(self, loaded_order):
        loaded_order.confirm()
        loaded_order.cancel()
        assert loaded_order.status == "cancelled"

    def test_cannot_cancel_delivered(self, loaded_order):
        loaded_order.status = "delivered"
        with pytest.raises(OrderError, match="Cannot cancel"):
            loaded_order.cancel()


# ══════════════════════════════════════════════════════════════════
# PAYMENT TESTS
# ══════════════════════════════════════════════════════════════════

class TestPayment:

    @pytest.mark.parametrize("method", ["card", "upi", "netbanking", "wallet"])
    def test_all_valid_methods_succeed(self, method):
        result = process_payment(1000, method)
        assert result["status"]  == "success"
        assert result["method"]  == method
        assert result["amount"]  == 1000

    def test_transaction_id_format(self):
        result = process_payment(500, "upi")
        assert result["transaction_id"].startswith("TXN")
        assert len(result["transaction_id"]) == 13   # TXN + 10 digits

    @pytest.mark.parametrize("bad_method", ["bitcoin", "cash", "", "CARD"])
    def test_invalid_methods_raise(self, bad_method):
        with pytest.raises(PaymentError, match="Invalid payment method"):
            process_payment(1000, bad_method)

    @pytest.mark.parametrize("bad_amount", [0, -1, -1000])
    def test_non_positive_amounts_raise(self, bad_amount):
        with pytest.raises(PaymentError, match="Amount must be positive"):
            process_payment(bad_amount, "card")


# ══════════════════════════════════════════════════════════════════
# MOCKING TESTS — email and external dependencies
# ══════════════════════════════════════════════════════════════════

class TestEmailMocking:

    @patch("main.smtplib.SMTP")
    def test_send_confirmation_success(self, mock_smtp, loaded_order):
        mock_server = Mock()
        mock_smtp.return_value = mock_server

        result = send_order_confirmation("arjun@example.com", loaded_order)

        assert result is True
        mock_smtp.assert_called_once_with("smtp.gmail.com", 587)
        mock_server.sendmail.assert_called_once()
        mock_server.quit.assert_called_once()

    @patch("main.smtplib.SMTP")
    def test_send_confirmation_fails_gracefully(self, mock_smtp, loaded_order):
        mock_smtp.side_effect = ConnectionError("SMTP down")

        result = send_order_confirmation("arjun@example.com", loaded_order)

        assert result is False   # graceful failure, no exception raised


# ══════════════════════════════════════════════════════════════════
# REGRESSION TESTS — known bugs that must stay fixed
# ══════════════════════════════════════════════════════════════════

class TestRegression:

    def test_regression_empty_customer_name_bug_001(self):
        """Bug #001: Empty string was accepted as customer. Fixed: added strip() check."""
        with pytest.raises(ValueError):
            Order("")
        with pytest.raises(ValueError):
            Order("   ")

    def test_regression_duplicate_item_overwrites_qty_bug_002(self, empty_order, laptop):
        """Bug #002: Adding same item twice was resetting qty instead of accumulating."""
        empty_order.add_item(laptop, 2)
        empty_order.add_item(laptop, 3)
        assert empty_order._items["Laptop"]["qty"] == 5  # should be 5, not 3

    def test_regression_negative_stock_bug_003(self):
        """Bug #003: Negative stock was allowed in Product constructor."""
        with pytest.raises(ValueError):
            Product("Item", 100, stock=-1)
```

**Final Run:**
```bash
# Run everything
pytest test_main.py -v --cov=main --cov-report=term-missing

# Run only smoke tests
pytest test_main.py -m smoke -v

# Run only regression tests
pytest test_main.py::TestRegression -v

# Run only payment tests
pytest test_main.py::TestPayment -v
```

---

## Summary — Everything in One View

```
UNITTEST (built-in):
  class Test(unittest.TestCase) → def test_xxx(self) → self.assertXxx()
  setUp/tearDown per test | setUpClass/tearDownClass per class
  Run: python -m unittest test_file.py -v

PYTEST (recommended):
  def test_xxx() → assert ... | pytest.raises() | pytest.approx()
  Fixtures: @pytest.fixture → inject as parameter
  Parametrize: @pytest.mark.parametrize("a,b", [(1,2), (3,4)])
  Run: pytest test_file.py -v

FIXTURE SCOPES: function (default) | class | module | session
SHARED FIXTURES: conftest.py (auto-loaded, no import needed)

MOCKING:
  Mock()       → fake object you control
  patch("module.name") → temporarily replace something
  mock.return_value = x  → what it returns when called
  mock.side_effect = Exception  → make it raise
  mock.assert_called_once_with(args)  → verify call happened

COVERAGE: pytest --cov=module --cov-report=term-missing

TESTING TYPES:
  Unit:        one function, mocked dependencies
  Integration: multiple components together
  Regression:  re-tests known fixed bugs
  Smoke:       quick alive-check (runs before everything)
  Performance: timing benchmarks
  API:         test HTTP endpoints

TDD: Write failing test → write minimum code → refactor
BDD: Given/When/Then structure describing behaviour
```

---

## 🎯 10 Questions

1. What is the difference between a unit test and an integration test?
2. What does `setUp()` do in unittest, and what is the equivalent in pytest?
3. Why do you need `pytest.approx()` when asserting float results?
4. What is the difference between `scope="function"` and `scope="session"` in a pytest fixture?
5. What does `patch("main.requests.get")` do, and why does the path matter?
6. What is `mock.side_effect` used for?
7. What is the purpose of `conftest.py`?
8. How does `@pytest.mark.parametrize` reduce test code duplication?
9. What is a regression test and when should you write one?
10. What does `--cov-report=term-missing` show?
