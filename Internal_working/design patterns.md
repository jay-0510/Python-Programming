# 🏗️ Python — Design Patterns, SOLID, Tools & Best Practices

## 🧠 Why Do Design Patterns Exist?

As codebases grow, three problems emerge repeatedly:

1. **Tight coupling** — changing one class breaks five others
1. **Duplication** — the same logic scattered across files
1. **Rigid structure** — adding a feature requires rewriting core code

Design patterns are **proven, named solutions** to these recurring problems. They are not libraries — they are *blueprints for structuring code* that experienced engineers arrived at independently and then codified.

-----

-----

# Part 1: Design Patterns

-----

## 1. Singleton Pattern

### Problem it solves

You want **exactly one instance** of a class to exist throughout the entire application — a database connection pool, a config loader, a logger. Creating multiple instances would waste resources or cause conflicting state.

### The naive version (broken)

```python
# Without Singleton — every call creates a NEW object
class Config:
    def __init__(self):
        self.settings = {}   # imagine loading from a file here

c1 = Config()
c2 = Config()

print(c1 is c2)   # False — two separate objects in memory!
# If you update c1.settings, c2 doesn't know about it.
```

### Singleton using `__new__`

```python
class Config:
    _instance = None   # class-level variable — shared across ALL instances

    def __new__(cls):
        # __new__ is called BEFORE __init__
        # It is responsible for actually creating the object
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.settings = {}   # initialise once
        return cls._instance   # always return the SAME object

    def set(self, key, value):
        self.settings[key] = value

    def get(self, key):
        return self.settings.get(key)


# Usage
c1 = Config()
c2 = Config()

c1.set('debug', True)

print(c2.get('debug'))   # True — same object, same data
print(c1 is c2)          # True — identical memory address
print(id(c1), id(c2))    # same id
```

### How it works internally

```
First call:  Config()
  → __new__ runs, _instance is None
  → creates object, stores in _instance
  → __init__ runs

Second call: Config()
  → __new__ runs, _instance is NOT None
  → returns the EXISTING object immediately
  → __init__ runs again on same object (watch out!)
```

### Thread-safe Singleton (real world)

```python
import threading

class DatabasePool:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:           # only one thread enters at a time
                if cls._instance is None:   # double-check after acquiring lock
                    cls._instance = super().__new__(cls)
                    cls._instance.pool = []   # simulate connection pool
        return cls._instance

    def add_connection(self, conn):
        self.pool.append(conn)

    def get_pool_size(self):
        return len(self.pool)


db1 = DatabasePool()
db2 = DatabasePool()

db1.add_connection("conn_1")
print(db2.get_pool_size())   # 1 — same pool
print(db1 is db2)            # True
```

### When to use Singleton

- Logger (one log stream for the whole app)
- Configuration loader (one source of truth for settings)
- Database connection pool
- Cache manager

### When NOT to use Singleton

- When you need testability — Singletons are hard to mock/reset between tests
- When you might need multiple instances later — premature Singleton is a trap

-----

## 2. Factory / Abstract Factory Pattern

### Problem it solves

You want to **create objects without specifying the exact class** in the calling code. The object creation logic is centralised. Adding a new type means adding a new class — not modifying existing code.

### Simple Factory

```python
# Without factory — calling code is tightly coupled to class names
class IndianPayment:
    def pay(self, amount):
        print(f"Paying ₹{amount} via UPI")

class USPayment:
    def pay(self, amount):
        print(f"Paying ${amount} via Credit Card")

# Caller must know ALL concrete classes
country = "IN"
if country == "IN":
    p = IndianPayment()
elif country == "US":
    p = USPayment()
p.pay(500)
# Problem: adding "UK" means modifying THIS block everywhere it appears
```

```python
# With Simple Factory — creation logic in ONE place

class IndianPayment:
    def pay(self, amount):
        print(f"Paying ₹{amount} via UPI")

class USPayment:
    def pay(self, amount):
        print(f"Paying ${amount} via Credit Card")

class UKPayment:
    def pay(self, amount):
        print(f"Paying £{amount} via Bank Transfer")


class PaymentFactory:
    _registry = {
        'IN': IndianPayment,
        'US': USPayment,
        'UK': UKPayment,
    }

    @staticmethod
    def create(country: str):
        cls = PaymentFactory._registry.get(country)
        if cls is None:
            raise ValueError(f"No payment method for country: {country}")
        return cls()


# Caller only knows about the Factory — not concrete classes
p = PaymentFactory.create('IN')
p.pay(1000)

p2 = PaymentFactory.create('UK')
p2.pay(200)

# Adding a new country: just add to _registry dict + write new class
# Zero changes to caller code ✅
```

### Abstract Factory — family of related objects

```python
# Abstract Factory: creates FAMILIES of related objects
# Example: UI theme — each theme creates matching Button + TextBox

from abc import ABC, abstractmethod


# --- Abstract Products ---
class Button(ABC):
    @abstractmethod
    def render(self):
        pass

class TextBox(ABC):
    @abstractmethod
    def render(self):
        pass


# --- Concrete Products: Light Theme ---
class LightButton(Button):
    def render(self):
        print("[ Light Button ]")

class LightTextBox(TextBox):
    def render(self):
        print("[ Light TextBox ]")


# --- Concrete Products: Dark Theme ---
class DarkButton(Button):
    def render(self):
        print("[ Dark Button █ ]")

class DarkTextBox(TextBox):
    def render(self):
        print("[ Dark TextBox █ ]")


# --- Abstract Factory ---
class UIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass

    @abstractmethod
    def create_textbox(self) -> TextBox:
        pass


# --- Concrete Factories ---
class LightThemeFactory(UIFactory):
    def create_button(self):
        return LightButton()

    def create_textbox(self):
        return LightTextBox()


class DarkThemeFactory(UIFactory):
    def create_button(self):
        return DarkButton()

    def create_textbox(self):
        return DarkTextBox()


# --- Client code — knows only about UIFactory interface ---
def render_ui(factory: UIFactory):
    btn = factory.create_button()
    txt = factory.create_textbox()
    btn.render()
    txt.render()


render_ui(LightThemeFactory())
# [ Light Button ]
# [ Light TextBox ]

render_ui(DarkThemeFactory())
# [ Dark Button █ ]
# [ Dark TextBox █ ]

# Adding a "High Contrast" theme = new factory + new products
# render_ui() needs ZERO changes ✅
```

### When to use Factory

- Object creation involves logic that shouldn’t be in the caller
- You want to decouple creation from usage
- You anticipate adding new types frequently

-----

## 3. Decorator Pattern

### Problem it solves

You want to **add behaviour to an object dynamically** without modifying its class or using inheritance. Inheritance is static (baked in at class definition time). Decorators are dynamic and composable — you can stack them.

> Python has built-in decorator syntax (`@`) which is a different but related concept. The Design Pattern Decorator is about wrapping objects.

### Function Decorator (Python’s native `@` syntax)

```python
# Python's @ decorator wraps a function with additional behaviour

def log_calls(func):
    """Wrapper that logs before and after every function call."""
    def wrapper(*args, **kwargs):
        print(f"→ Calling {func.__name__} with {args}")
        result = func(*args, **kwargs)
        print(f"← {func.__name__} returned {result}")
        return result
    return wrapper


@log_calls   # equivalent to: add = log_calls(add)
def add(a, b):
    return a + b


add(3, 5)
# → Calling add with (3, 5)
# ← add returned 8
```

### Stacking decorators

```python
import time
import functools

def timer(func):
    @functools.wraps(func)   # preserves original function name/docstring
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"⏱ {func.__name__} took {time.time()-start:.4f}s")
        return result
    return wrapper

def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"📞 {func.__name__} called")
        return func(*args, **kwargs)
    return wrapper


@timer
@log_calls     # decorators apply bottom-up: log_calls first, then timer wraps that
def compute(n):
    return sum(range(n))


compute(1_000_000)
# 📞 compute called
# ⏱ compute took 0.0312s
```

### Class-based Decorator Pattern (OOP style)

```python
# Wrapping objects (the classic Gang of Four pattern)

class Coffee:
    def cost(self):
        return 50

    def description(self):
        return "Plain Coffee"


# Decorator base — wraps the original object
class CoffeeDecorator:
    def __init__(self, coffee):
        self._coffee = coffee   # holds reference to wrapped object

    def cost(self):
        return self._coffee.cost()

    def description(self):
        return self._coffee.description()


# Concrete decorators — each adds something
class Milk(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 15

    def description(self):
        return self._coffee.description() + " + Milk"


class Sugar(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 5

    def description(self):
        return self._coffee.description() + " + Sugar"


class ExtraShot(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 25

    def description(self):
        return self._coffee.description() + " + Extra Shot"


# Build the drink by stacking decorators
order = Coffee()
order = Milk(order)
order = Sugar(order)
order = ExtraShot(order)

print(order.description())   # Plain Coffee + Milk + Sugar + Extra Shot
print(f"₹{order.cost()}")    # ₹95

# Each decorator WRAPS the previous — like nested function calls
# ExtraShot.cost() → Sugar.cost() → Milk.cost() → Coffee.cost()
```

### When to use Decorator

- Adding logging, caching, authentication, timing to functions
- Building configurable pipelines (middleware in web frameworks)
- Adding features to objects without touching the original class

-----

## 4. Strategy Pattern

### Problem it solves

You have **multiple algorithms** for the same task (sorting, discount calculation, payment processing). Instead of one giant `if/elif` block, you encapsulate each algorithm in its own class and swap them at runtime.

### Without Strategy (the problem)

```python
class OrderProcessor:
    def calculate_discount(self, price, customer_type):
        if customer_type == 'regular':
            return price * 0.05
        elif customer_type == 'premium':
            return price * 0.15
        elif customer_type == 'vip':
            return price * 0.30
        # Adding 'employee' type means MODIFYING this class ← bad
```

### With Strategy Pattern

```python
from abc import ABC, abstractmethod


# --- Strategy Interface ---
class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, price: float) -> float:
        pass


# --- Concrete Strategies ---
class RegularDiscount(DiscountStrategy):
    def calculate(self, price):
        return price * 0.05

class PremiumDiscount(DiscountStrategy):
    def calculate(self, price):
        return price * 0.15

class VIPDiscount(DiscountStrategy):
    def calculate(self, price):
        return price * 0.30

class EmployeeDiscount(DiscountStrategy):
    def calculate(self, price):
        return price * 0.40


# --- Context: uses whichever strategy is injected ---
class OrderProcessor:
    def __init__(self, discount_strategy: DiscountStrategy):
        self._strategy = discount_strategy

    def set_strategy(self, strategy: DiscountStrategy):
        self._strategy = strategy   # swap strategy at runtime

    def process(self, price: float):
        discount = self._strategy.calculate(price)
        final    = price - discount
        print(f"Price: ₹{price}, Discount: ₹{discount:.0f}, Final: ₹{final:.0f}")


# Usage — inject the strategy
processor = OrderProcessor(RegularDiscount())
processor.process(1000)   # Price: ₹1000, Discount: ₹50, Final: ₹950

processor.set_strategy(VIPDiscount())
processor.process(1000)   # Price: ₹1000, Discount: ₹300, Final: ₹700

# Adding EmployeeDiscount needs ZERO changes to OrderProcessor ✅
processor.set_strategy(EmployeeDiscount())
processor.process(1000)
```

### Strategy with Python callables (Pythonic approach)

```python
# In Python, functions are first-class — you can use them as strategies
# without creating a class hierarchy

def regular_discount(price):  return price * 0.05
def premium_discount(price):  return price * 0.15
def vip_discount(price):      return price * 0.30


class Order:
    def __init__(self, price, discount_fn):
        self.price = price
        self.discount_fn = discount_fn

    def total(self):
        return self.price - self.discount_fn(self.price)


o = Order(1000, vip_discount)
print(f"₹{o.total()}")   # ₹700.0

# Swap at runtime
o.discount_fn = regular_discount
print(f"₹{o.total()}")   # ₹950.0
```

### When to use Strategy

- Multiple algorithms for the same operation (sorting, compression, pricing)
- Eliminating large if/elif chains that grow over time
- When you want to switch behaviour at runtime

-----

-----

# Part 2: SOLID Principles

SOLID is five principles of object-oriented design that, when followed, make code easier to extend, test, and maintain.

-----

## S — Single Responsibility Principle

**“A class should have only one reason to change.”**

If a class handles both business logic AND formatting AND database operations, then a change in *any* of those three areas forces you to touch the class. That’s three reasons to change — three sources of bugs.

```python
# ❌ BAD — one class doing three jobs
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def calculate_tax(self):            # business logic
        return self.salary * 0.30

    def save_to_db(self):               # database concern
        print(f"INSERT INTO employees VALUES ({self.name}, {self.salary})")

    def print_report(self):             # formatting concern
        print(f"Employee: {self.name}, Salary: {self.salary}")
```

```python
# ✅ GOOD — each class has exactly one job

class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def calculate_tax(self):
        return self.salary * 0.30


class EmployeeRepository:
    def save(self, employee: Employee):
        print(f"Saving {employee.name} to database")


class EmployeeReporter:
    def print_report(self, employee: Employee):
        print(f"Employee: {employee.name}, Salary: ₹{employee.salary}")


# Usage
emp = Employee("Alice", 80000)

repo = EmployeeRepository()
repo.save(emp)

reporter = EmployeeReporter()
reporter.print_report(emp)

print(f"Tax: ₹{emp.calculate_tax()}")
```

-----

## O — Open/Closed Principle

**“Open for extension, closed for modification.”**

You should be able to add new behaviour without touching existing, working code.

```python
# ❌ BAD — every new shape requires modifying this class

class AreaCalculator:
    def calculate(self, shape):
        if shape['type'] == 'circle':
            return 3.14 * shape['radius'] ** 2
        elif shape['type'] == 'rectangle':
            return shape['width'] * shape['height']
        # Adding 'triangle' means modifying HERE — risky
```

```python
# ✅ GOOD — add new shapes without touching AreaCalculator

from abc import ABC, abstractmethod
import math

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Triangle(Shape):         # ← new shape added, zero changes elsewhere
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height


class AreaCalculator:
    def total_area(self, shapes: list[Shape]) -> float:
        return sum(shape.area() for shape in shapes)


shapes = [Circle(5), Rectangle(4, 6), Triangle(3, 8)]
calc = AreaCalculator()
print(f"Total area: {calc.total_area(shapes):.2f}")
```

-----

## L — Liskov Substitution Principle

**“Subclasses must be substitutable for their parent class without breaking the program.”**

If code works with a `Bird`, it must work with any `Bird` subclass — including ones not yet written.

```python
# ❌ BAD — Penguin breaks the Bird contract

class Bird:
    def fly(self):
        print("Flying!")

class Eagle(Bird):
    def fly(self):
        print("Eagle soaring high")

class Penguin(Bird):
    def fly(self):
        raise NotImplementedError("Penguins can't fly!")   # ← breaks LSP

def make_bird_fly(bird: Bird):
    bird.fly()   # crashes for Penguin

make_bird_fly(Eagle())    # OK
make_bird_fly(Penguin())  # ❌ RuntimeError
```

```python
# ✅ GOOD — correct hierarchy reflects reality

from abc import ABC, abstractmethod

class Bird(ABC):
    @abstractmethod
    def move(self):
        pass

class FlyingBird(Bird):
    def fly(self):
        print("Flying!")

    def move(self):
        self.fly()

class SwimmingBird(Bird):
    def swim(self):
        print("Swimming!")

    def move(self):
        self.swim()

class Eagle(FlyingBird):
    def fly(self):
        print("Eagle soaring high")

class Penguin(SwimmingBird):
    def swim(self):
        print("Penguin swimming gracefully")


def make_bird_move(bird: Bird):
    bird.move()   # works for ALL Bird subclasses ✅

make_bird_move(Eagle())    # Eagle soaring high
make_bird_move(Penguin())  # Penguin swimming gracefully
```

-----

## I — Interface Segregation Principle

**“No class should be forced to implement methods it doesn’t use.”**

Fat interfaces force implementors to write dummy/stub methods, which is a code smell.

```python
# ❌ BAD — one fat interface forces irrelevant methods

from abc import ABC, abstractmethod

class Worker(ABC):
    @abstractmethod
    def work(self):  pass

    @abstractmethod
    def eat(self):   pass   # Robots don't eat!

    @abstractmethod
    def sleep(self): pass   # Robots don't sleep!


class Human(Worker):
    def work(self):  print("Human working")
    def eat(self):   print("Human eating")
    def sleep(self): print("Human sleeping")

class Robot(Worker):
    def work(self):  print("Robot working")
    def eat(self):   raise NotImplementedError("Robots don't eat")  # ← forced stub
    def sleep(self): raise NotImplementedError("Robots don't sleep") # ← forced stub
```

```python
# ✅ GOOD — small, focused interfaces

class Workable(ABC):
    @abstractmethod
    def work(self): pass

class Eatable(ABC):
    @abstractmethod
    def eat(self): pass

class Sleepable(ABC):
    @abstractmethod
    def sleep(self): pass


class Human(Workable, Eatable, Sleepable):
    def work(self):  print("Human working")
    def eat(self):   print("Human eating")
    def sleep(self): print("Human sleeping")

class Robot(Workable):           # only implements what it needs
    def work(self):  print("Robot working")


h = Human()
h.work()
h.eat()

r = Robot()
r.work()   # no stubs, no NotImplementedError ✅
```

-----

## D — Dependency Inversion Principle

**“High-level modules should not depend on low-level modules. Both should depend on abstractions.”**

If your `OrderService` directly imports `MySQLDatabase`, switching to PostgreSQL requires changing `OrderService`. Instead, both should depend on a `Database` interface.

```python
# ❌ BAD — high-level class directly depends on low-level class

class MySQLDatabase:
    def save(self, data):
        print(f"Saving '{data}' to MySQL")

class OrderService:
    def __init__(self):
        self.db = MySQLDatabase()   # ← hardcoded dependency

    def place_order(self, item):
        self.db.save(item)

# Switching to PostgreSQL requires modifying OrderService ← bad
```

```python
# ✅ GOOD — both depend on an abstraction

from abc import ABC, abstractmethod

# Abstraction (interface)
class Database(ABC):
    @abstractmethod
    def save(self, data: str): pass


# Low-level modules implement the interface
class MySQLDatabase(Database):
    def save(self, data):
        print(f"MySQL: saving '{data}'")

class PostgreSQLDatabase(Database):
    def save(self, data):
        print(f"PostgreSQL: saving '{data}'")

class MockDatabase(Database):    # for testing!
    def __init__(self):
        self.records = []

    def save(self, data):
        self.records.append(data)
        print(f"Mock DB: saved '{data}'")


# High-level module depends ONLY on the abstraction
class OrderService:
    def __init__(self, db: Database):   # ← injected, not hardcoded
        self.db = db

    def place_order(self, item):
        self.db.save(item)


# Swap implementations without changing OrderService
svc = OrderService(MySQLDatabase())
svc.place_order("Laptop")    # MySQL: saving 'Laptop'

svc2 = OrderService(PostgreSQLDatabase())
svc2.place_order("Phone")    # PostgreSQL: saving 'Phone'

# Testing with a mock
mock_db = MockDatabase()
svc3 = OrderService(mock_db)
svc3.place_order("Tablet")
print(mock_db.records)       # ['Tablet'] ✅
```

-----

-----

# Part 3: Dependency Injection

### What is it?

Dependency Injection (DI) means **providing a class its dependencies from outside** rather than letting it create them internally.

```
Without DI:  Class creates its own dependencies internally
With DI:     Dependencies are "injected" by the caller

Benefit: Loose coupling, easy testing, easy swapping
```

```python
# ❌ Without DI — hard to test, hard to swap

class EmailService:
    def send(self, to, message):
        print(f"Sending email to {to}: {message}")

class UserService:
    def __init__(self):
        self.email = EmailService()   # hardcoded — can't swap for SMS

    def register(self, user):
        # ...save user...
        self.email.send(user, "Welcome!")
```

```python
# ✅ With DI — constructor injection

from abc import ABC, abstractmethod

class NotificationService(ABC):
    @abstractmethod
    def notify(self, user: str, message: str): pass

class EmailService(NotificationService):
    def notify(self, user, message):
        print(f"📧 Email to {user}: {message}")

class SMSService(NotificationService):
    def notify(self, user, message):
        print(f"📱 SMS to {user}: {message}")

class MockNotifier(NotificationService):
    def __init__(self):
        self.sent = []

    def notify(self, user, message):
        self.sent.append((user, message))


class UserService:
    def __init__(self, notifier: NotificationService):   # injected
        self.notifier = notifier

    def register(self, user):
        print(f"Registered {user}")
        self.notifier.notify(user, "Welcome!")


# Production
svc = UserService(EmailService())
svc.register("Alice")

# Swap to SMS with zero changes to UserService
svc2 = UserService(SMSService())
svc2.register("Bob")

# Testing — no real emails sent
mock = MockNotifier()
svc3 = UserService(mock)
svc3.register("Carol")
print(mock.sent)   # [('Carol', 'Welcome!')]
```

### Types of DI

```python
# 1. Constructor Injection (most common — prefer this)
class Service:
    def __init__(self, dep):
        self.dep = dep

# 2. Setter Injection
class Service:
    def set_dependency(self, dep):
        self.dep = dep

# 3. Method/Parameter Injection
class Service:
    def do_work(self, dep):
        dep.something()
```

-----

-----

# Part 4: Pylint & Formatter

## Pylint — Static Code Analyser

Pylint reads your code WITHOUT running it and reports:

- Syntax errors
- Undefined variables
- Unused imports
- Naming convention violations
- Code complexity issues

```bash
pip install pylint

# Run on a file
pylint my_file.py

# Run on a whole package
pylint my_package/
```

### Example Pylint output

```
my_file.py:5:0: W0611: Unused import os (unused-import)
my_file.py:8:4: C0103: Variable name "x" doesn't conform to snake_case (invalid-name)
my_file.py:12:0: R0914: Too many local variables (16/15) (too-many-locals)
my_file.py:20:0: E1101: Module 'json' has no 'loads_fast' member (no-member)

--------------------------------------------------------------------
Your code has been rated at 6.50/10
```

### Pylint message codes

```
C = Convention (style guide violation)
W = Warning    (potential issue)
E = Error      (probable bug)
R = Refactor   (structural improvement needed)
F = Fatal      (prevents pylint running)
```

### Disabling specific warnings (with comment)

```python
import os   # noqa: F401      ← suppress in flake8
import os   # pylint: disable=unused-import   ← suppress in pylint

# Disable for a block
# pylint: disable=too-many-arguments
def complex_function(a, b, c, d, e, f):
    pass
# pylint: enable=too-many-arguments
```

### .pylintrc config file

```ini
# .pylintrc — project-level config
[MESSAGES CONTROL]
disable = C0114,  # missing-module-docstring
          C0115,  # missing-class-docstring
          C0116   # missing-function-docstring

[FORMAT]
max-line-length = 100

[DESIGN]
max-args = 7
max-locals = 20
```

-----

## Black — Code Formatter

Black is an **opinionated, zero-config** formatter. It reformats your code automatically. You don’t argue about style — Black decides.

```bash
pip install black

# Format a file (modifies it in place)
black my_file.py

# Preview what would change (dry run)
black --diff my_file.py

# Format entire project
black .

# Set line length (default 88)
black --line-length 100 my_file.py
```

### What Black does

```python
# Before Black (your messy code)
x={'a':1,'b':2,'c':3}
def foo(a,b,c,d,e):
    return a+b+c+d+e
result=foo(1,2,3,4,5)
my_list=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

# After Black (clean, consistent)
x = {"a": 1, "b": 2, "c": 3}

def foo(a, b, c, d, e):
    return a + b + c + d + e

result = foo(1, 2, 3, 4, 5)
my_list = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
    11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
]
```

-----

## isort — Import Sorter

```bash
pip install isort

isort my_file.py
```

```python
# Before isort (random order)
import sys
import os
import pandas as pd
from datetime import datetime
import numpy as np
from collections import defaultdict

# After isort (stdlib → third-party → local, alphabetical within each)
import os
import sys
from collections import defaultdict
from datetime import datetime

import numpy as np
import pandas as pd
```

-----

## flake8 — Lightweight Linter

```bash
pip install flake8

flake8 my_file.py
```

```
my_file.py:1:1: F401 'os' imported but unused
my_file.py:5:80: E501 line too long (95 > 79 characters)
my_file.py:10:1: E302 expected 2 blank lines, found 1
```

-----

## Recommended Tool Stack

```
black    → formats code automatically (style)
isort    → organises imports
pylint   → deep analysis (bugs, complexity, conventions)
flake8   → fast, lightweight lint

Run order: isort → black → flake8 → pylint
```

### Pre-commit hook (auto-run on every git commit)

```bash
pip install pre-commit
```

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.0
    hooks:
      - id: black

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
```

```bash
pre-commit install   # installs hooks into .git/hooks
# Now black+isort+flake8 run automatically before every commit
```

-----

-----

# Part 5: Package Manager

## pip — The Standard Package Manager

```bash
# Install
pip install requests
pip install requests==2.31.0        # specific version
pip install "requests>=2.28,<3.0"   # version range

# Install from requirements file
pip install -r requirements.txt

# Uninstall
pip uninstall requests

# List installed packages
pip list
pip show requests                   # details about one package

# Upgrade
pip install --upgrade requests

# Freeze current env to requirements.txt
pip freeze > requirements.txt
```

### requirements.txt

```
# requirements.txt
pandas==2.1.4
numpy==1.26.2
requests>=2.28.0
sqlalchemy==2.0.23
python-dotenv==1.0.0
```

-----

## Virtual Environments — Isolating Projects

Without virtual environments, every project shares the same global Python packages. Project A needs `pandas==1.5`, Project B needs `pandas==2.1` — conflict.

```bash
# Create a virtual environment
python -m venv venv

# Activate (Mac/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# You're now isolated — installs go into venv/
pip install pandas
pip install numpy

# Deactivate when done
deactivate

# Typical project structure
myproject/
├── venv/              ← never commit this (add to .gitignore)
├── requirements.txt   ← commit this
├── src/
└── tests/
```

-----

## pip-tools — Pinning Dependencies Cleanly

```bash
pip install pip-tools

# requirements.in — your direct dependencies (human-maintained)
# pandas>=2.0
# requests

pip-compile requirements.in
# → generates requirements.txt with ALL transitive deps pinned exactly
# → reproducible environments across all machines
```

-----

## Poetry — Modern All-in-One Tool

Poetry combines package management + virtual environments + publishing.

```bash
pip install poetry

# Start a new project
poetry new my_project

# Add a dependency
poetry add pandas
poetry add numpy@^1.26

# Add dev dependency (not installed in production)
poetry add --group dev pytest black pylint

# Install all dependencies
poetry install

# Run inside the virtual env
poetry run python main.py
poetry run pytest

# Export to requirements.txt format (for compatibility)
poetry export -f requirements.txt --output requirements.txt
```

### pyproject.toml (Poetry’s config file)

```toml
[tool.poetry]
name = "my-project"
version = "0.1.0"
description = "A sample project"
authors = ["Kathan <kathan@example.com>"]

[tool.poetry.dependencies]
python = "^3.11"
pandas = "^2.1.0"
numpy = "^1.26.0"
requests = "^2.31.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
black = "^23.12.0"
pylint = "^3.0.0"

[tool.black]
line-length = 100

[tool.isort]
profile = "black"
```

-----

-----

# Part 6: Best Practices in Python

## 1. Naming Conventions

```python
# Variables and functions: snake_case
user_name = "Alice"
total_price = 100.0

def calculate_tax(salary):
    pass

# Classes: PascalCase
class OrderProcessor:
    pass

class MySQLDatabase:
    pass

# Constants: UPPER_SNAKE_CASE
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30
BASE_URL = "https://api.example.com"

# Private (convention, not enforced): leading underscore
class MyClass:
    def __init__(self):
        self._internal_state = 0   # "please don't touch from outside"
        self.__private = 0          # name-mangled → _MyClass__private

# "Throwaway" variable: underscore
for _ in range(5):
    print("hello")

_, important_value = (1, 42)
```

-----

## 2. Type Hints — Make Intent Explicit

```python
# Without type hints — what does this function accept/return?
def process(data, limit, flag):
    pass

# With type hints — self-documenting code
from typing import Optional, Union

def process(
    data: list[dict],
    limit: int = 100,
    flag: bool = False
) -> list[str]:
    pass

def find_user(user_id: int) -> Optional[dict]:
    """Returns user dict or None if not found."""
    pass

def parse_value(val: Union[int, str]) -> float:
    pass

# Dataclass — structured data with types
from dataclasses import dataclass, field

@dataclass
class Employee:
    name: str
    salary: float
    dept: str
    skills: list[str] = field(default_factory=list)

    def tax(self) -> float:
        return self.salary * 0.30

emp = Employee(name="Alice", salary=80000, dept="IT")
print(emp)
print(emp.tax())
```

-----

## 3. Context Managers — Always Clean Up

```python
# ❌ BAD — file not closed if an exception occurs
f = open('data.txt', 'r')
data = f.read()
f.close()

# ✅ GOOD — file always closed, even on exception
with open('data.txt', 'r') as f:
    data = f.read()

# Custom context manager using contextlib
from contextlib import contextmanager
import time

@contextmanager
def timer(label: str):
    start = time.time()
    try:
        yield              # code inside 'with' block runs here
    finally:
        elapsed = time.time() - start
        print(f"{label} took {elapsed:.3f}s")


with timer("Data processing"):
    total = sum(range(10_000_000))

# Custom context manager using a class
class ManagedResource:
    def __enter__(self):
        print("Resource acquired")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Resource released")
        return False   # False = don't suppress exceptions

with ManagedResource() as r:
    print("Using resource")
```

-----

## 4. List/Dict Comprehensions — Readable and Fast

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# ❌ Loop style
evens = []
for n in numbers:
    if n % 2 == 0:
        evens.append(n)

# ✅ Comprehension style
evens = [n for n in numbers if n % 2 == 0]

# Transformation
squares = [n**2 for n in numbers]

# Dict comprehension
names = ['alice', 'bob', 'carol']
name_lengths = {name: len(name) for name in names}
# {'alice': 5, 'bob': 3, 'carol': 5}

# Set comprehension
unique_lengths = {len(name) for name in names}
# {3, 5}

# Generator expression (lazy — doesn't build full list in memory)
total = sum(n**2 for n in range(1_000_000))   # uses O(1) memory
```

-----

## 5. Exception Handling — Be Specific

```python
# ❌ BAD — catches everything, hides bugs
try:
    result = int(user_input) / divisor
except:
    print("Something went wrong")   # which error? we don't know

# ❌ ALSO BAD — too broad
try:
    result = int(user_input) / divisor
except Exception as e:
    print(f"Error: {e}")

# ✅ GOOD — specific exceptions, meaningful messages
try:
    value = int(user_input)
except ValueError:
    print(f"Invalid input: '{user_input}' is not a number")
    raise   # re-raise after logging

try:
    result = value / divisor
except ZeroDivisionError:
    print("Divisor cannot be zero")
    result = 0

# Custom exception
class InsufficientFundsError(Exception):
    def __init__(self, balance, amount):
        super().__init__(f"Balance ₹{balance} < Required ₹{amount}")
        self.balance = balance
        self.amount = amount


class BankAccount:
    def __init__(self, balance):
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFundsError(self.balance, amount)
        self.balance -= amount


account = BankAccount(1000)
try:
    account.withdraw(2000)
except InsufficientFundsError as e:
    print(e)   # Balance ₹1000 < Required ₹2000
```

-----

## 6. Logging — Never Use print() in Production

```python
import logging

# Configure once at application startup
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
    handlers=[
        logging.StreamHandler(),                    # console
        logging.FileHandler('app.log'),             # file
    ]
)

logger = logging.getLogger(__name__)   # each module gets its own logger

# Use appropriate levels
logger.debug("Processing item %s", item_id)      # dev only
logger.info("Order %s placed successfully", order_id)
logger.warning("Retry attempt %d of %d", attempt, max_retries)
logger.error("Failed to connect to DB: %s", error)
logger.critical("System out of memory!")

# Never use string formatting IN the log call (performance)
# ❌ logger.debug(f"Value: {expensive_computation()}")  # always runs
# ✅ logger.debug("Value: %s", value)  # only formats if DEBUG is enabled
```

-----

## 7. Avoid Mutable Default Arguments

```python
# ❌ CLASSIC BUG — list is created ONCE at function definition time
def add_item(item, items=[]):
    items.append(item)
    return items

print(add_item("apple"))   # ['apple']
print(add_item("banana"))  # ['apple', 'banana']  ← not a fresh list!

# ✅ CORRECT — use None as sentinel
def add_item(item, items=None):
    if items is None:
        items = []      # new list created each call
    items.append(item)
    return items

print(add_item("apple"))   # ['apple']
print(add_item("banana"))  # ['banana']  ✅
```

-----

## 8. Use f-strings (Python 3.6+)

```python
name = "Alice"
salary = 80000.5

# ❌ Old ways
print("Hello, " + name)
print("Hello, %s" % name)
print("Hello, {}".format(name))

# ✅ f-strings — readable, fast
print(f"Hello, {name}")
print(f"Salary: ₹{salary:,.0f}")       # ₹80,001 (comma formatted)
print(f"Salary: ₹{salary:.2f}")        # ₹80000.50
print(f"Doubled: {salary * 2}")        # expressions allowed
print(f"{name!r}")                     # repr: 'Alice'
print(f"{name!u}")                     # upper: ALICE
print(f"{salary = }")                  # debug: salary = 80000.5
```

-----

## 9. Use Pathlib Instead of os.path

```python
# ❌ Old style with os.path (fragile on Windows vs Unix)
import os
base = os.path.join(os.getcwd(), 'data', 'files')
full = os.path.join(base, 'report.csv')

# ✅ Pathlib — clean, cross-platform, OOP
from pathlib import Path

base = Path.cwd() / 'data' / 'files'
full = base / 'report.csv'

print(full.exists())          # True/False
print(full.suffix)            # '.csv'
print(full.stem)              # 'report'
print(full.parent)            # data/files

full.parent.mkdir(parents=True, exist_ok=True)   # create dirs

# Read/write
content = full.read_text(encoding='utf-8')
full.write_text("new content")

# Glob
csv_files = list(Path('data').glob('**/*.csv'))
```

-----

## 10. Keep Functions Small and Focused

```python
# ❌ BAD — one function doing too much
def process_order(order_data):
    # validate
    if not order_data.get('user_id'):
        raise ValueError("Missing user_id")
    if not order_data.get('items'):
        raise ValueError("Empty order")

    # calculate
    total = sum(item['price'] * item['qty'] for item in order_data['items'])
    tax = total * 0.18
    final = total + tax

    # save
    print(f"INSERT INTO orders VALUES ({order_data['user_id']}, {final})")

    # notify
    print(f"Sending confirmation email to user {order_data['user_id']}")

    return final


# ✅ GOOD — each function does ONE thing, reads like prose
def validate_order(order_data: dict) -> None:
    if not order_data.get('user_id'):
        raise ValueError("Missing user_id")
    if not order_data.get('items'):
        raise ValueError("Empty order")


def calculate_total(items: list[dict]) -> float:
    subtotal = sum(item['price'] * item['qty'] for item in items)
    tax = subtotal * 0.18
    return subtotal + tax


def save_order(user_id: int, total: float) -> None:
    print(f"INSERT INTO orders VALUES ({user_id}, {total})")


def notify_user(user_id: int) -> None:
    print(f"Sending confirmation email to user {user_id}")


def process_order(order_data: dict) -> float:
    validate_order(order_data)
    total = calculate_total(order_data['items'])
    save_order(order_data['user_id'], total)
    notify_user(order_data['user_id'])
    return total
```

-----

## 11. Environment Variables — Never Hardcode Secrets

```bash
pip install python-dotenv
```

```python
# .env file (never commit to git)
# DB_PASSWORD=secret123
# API_KEY=abc-xyz-789
# DEBUG=True

# main.py
import os
from dotenv import load_dotenv

load_dotenv()   # loads .env into os.environ

db_password = os.getenv('DB_PASSWORD')
api_key     = os.getenv('API_KEY')
debug       = os.getenv('DEBUG', 'False') == 'True'

# ❌ Never do this
api_key = "abc-xyz-789"   # hardcoded in source code
```

```
# .gitignore
.env
venv/
__pycache__/
*.pyc
.pytest_cache/
```

-----

## Quick Summary Table

|Principle / Tool|One-line Summary                                                   |
|----------------|-------------------------------------------------------------------|
|Singleton       |One instance ever. Use `_instance` class var in `__new__`          |
|Factory         |Centralise object creation. Caller never `import`s concrete classes|
|Decorator       |Add behaviour dynamically by wrapping objects or functions         |
|Strategy        |Swap algorithms at runtime. Replace if/elif chains with classes    |
|SRP             |One class = one reason to change                                   |
|OCP             |Extend with new classes, don’t modify existing ones                |
|LSP             |Subclasses must honour parent’s contract                           |
|ISP             |Small interfaces over one fat interface                            |
|DIP             |Depend on abstractions, inject concretes                           |
|DI              |Pass dependencies in; don’t create them inside                     |
|Pylint          |Analyses code without running it. Score out of 10                  |
|Black           |Auto-formats code. No style debates                                |
|pip             |Install packages. `requirements.txt` pins versions                 |
|venv            |Isolate project deps from global Python                            |
|Poetry          |Modern: manages deps + venv + publishing in one tool               |

-----

*Type every example manually. Patterns only click after you’ve written them yourself.*