# Python Interview Prep — Core Concepts

---

## 1. List vs Tuple — Memory & BTS

**Key difference:** List is mutable (changeable), Tuple is immutable (fixed).

### Behind the Scenes — Memory

```python
import sys

my_list  = [1, 2, 3]
my_tuple = (1, 2, 3)

print(sys.getsizeof(my_list))   # ~120 bytes
print(sys.getsizeof(my_tuple))  # ~72 bytes
```

**Why does List use more memory?**

- List allocates **extra buffer space** (over-allocation) so appending is fast — no memory reallocation every time.
- Tuple knows it won't change → allocates **exactly** what it needs.

```
List  in memory: [ptr] [ptr] [ptr] [empty] [empty]  ← extra slots pre-reserved
Tuple in memory: [ptr] [ptr] [ptr]                  ← tight, no extra space
```

```python
a = [1, 2, 3]
a.append(4)       # Fast — uses pre-reserved slot, no reallocation needed

b = (1, 2, 3)
# b.append(4)     # TypeError — tuples are immutable
```

**When to use what:**
- **List** → data that changes (cart items, user inputs)
- **Tuple** → fixed data (coordinates, RGB values, DB records)

---

## 2. Pass by Value vs Pass by Reference

Python does **neither** exactly. It's **"Pass by Object Reference"** (also called pass by assignment).

### The Rule:
- **Immutable objects** (int, str, tuple) → behave like pass by value — original unchanged
- **Mutable objects** (list, dict) → behave like pass by reference — original can change

```python
# --- Immutable (int) — acts like pass by value ---
def change_num(x):
    x = 100       # creates a new int object, doesn't touch original
    print("inside:", x)

n = 10
change_num(n)
print("outside:", n)   # still 10 — original untouched


# --- Mutable (list) — acts like pass by reference ---
def add_item(lst):
    lst.append(99)    # modifies the SAME list object in memory

my_list = [1, 2, 3]
add_item(my_list)
print(my_list)        # [1, 2, 3, 99] — original changed!
```

**BTS:** Python passes the **memory address** (reference) of the object. For immutables, any "change" creates a new object at a new address, leaving the original untouched.

---

## 3. Dunder Methods (Magic Methods)

Dunder = **D**ouble **under**score. These are special methods Python calls automatically in certain situations.

```python
class Book:
    def __init__(self, title, price):
        # called when object is created: Book("Python", 500)
        self.title = title
        self.price = price

    def __str__(self):
        # called when you print(book) — human-readable
        return f"Book: {self.title}"

    def __repr__(self):
        # called in console/debug — developer-readable
        return f"Book('{self.title}', {self.price})"

    def __add__(self, other):
        # called when you do book1 + book2
        return self.price + other.price

    def __len__(self):
        # called when you do len(book)
        return len(self.title)

    def __eq__(self, other):
        # called when you do book1 == book2
        return self.price == other.price


b1 = Book("Python", 500)
b2 = Book("Django", 300)

print(b1)           # calls __str__  → "Book: Python"
print(repr(b1))     # calls __repr__ → "Book('Python', 500)"
print(b1 + b2)      # calls __add__  → 800
print(len(b1))      # calls __len__  → 6
print(b1 == b2)     # calls __eq__   → False
```

**BTS:** When Python sees `b1 + b2`, it looks for `b1.__add__(b2)`. Every operator maps to a dunder method.

---

## 4. Context Manager & Context Variable

### Context Manager
Automates **setup and teardown** — guarantees cleanup even if an error occurs.

```python
# Without context manager — risky!
f = open("file.txt", "r")
data = f.read()
f.close()         # if an error happens above, file stays open

# With context manager — safe
with open("file.txt", "r") as f:
    data = f.read()
# file is automatically closed here, even if error occurs
```

### Build Your Own Context Manager

```python
class DBConnection:
    def __enter__(self):
        # runs when `with` block starts
        print("Connecting to DB...")
        return self          # value assigned to `as` variable

    def __exit__(self, exc_type, exc_val, exc_tb):
        # runs when `with` block ends (error or not)
        print("Closing DB connection...")
        return False         # False = don't suppress exceptions


with DBConnection() as db:
    print("Running query...")
# Output:
# Connecting to DB...
# Running query...
# Closing DB connection...
```

### Using `contextlib` (simpler way)

```python
from contextlib import contextmanager

@contextmanager
def managed_resource():
    print("Setup")     # __enter__ part
    yield              # pause here, give control to `with` block
    print("Teardown")  # __exit__ part

with managed_resource():
    print("Doing work")
```

### Context Variable (`contextvars`)
Used for **per-task isolated state** — common in async code / multi-threading.

```python
from contextvars import ContextVar

user_id = ContextVar("user_id", default="anonymous")

def process_request(uid):
    token = user_id.set(uid)          # set value for THIS context
    print(f"Processing for: {user_id.get()}")
    user_id.reset(token)              # restore previous value

process_request("user_42")
print(user_id.get())                  # "anonymous" — not affected
```

---

## 5. Decorators

A decorator **wraps a function** to add behavior before/after it — without modifying the original function.

### BTS — What's Actually Happening

```python
# A decorator is just a function that takes a function and returns a new function

def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before the function")
        result = func(*args, **kwargs)   # call original function
        print("After the function")
        return result
    return wrapper                       # return the wrapped version


# Using @ syntax (syntactic sugar)
@my_decorator
def say_hello():
    print("Hello!")

say_hello()
# Output:
# Before the function
# Hello!
# After the function

# What @my_decorator actually does behind the scenes:
# say_hello = my_decorator(say_hello)
```

### Real-World Use Case — Timer

```python
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)

slow_function()   # slow_function took 1.0012s
```

---

## 6. *args and **kwargs

- `*args` → collects **extra positional** arguments as a **tuple**
- `**kwargs` → collects **extra keyword** arguments as a **dict**

```python
def greet(*args, **kwargs):
    # args is a tuple of positional args
    # kwargs is a dict of keyword args

    for name in args:
        print(f"Hello, {name}!")          # positional

    for key, val in kwargs.items():
        print(f"{key} = {val}")           # keyword


greet("Alice", "Bob", age=25, city="Mumbai")
# Hello, Alice!
# Hello, Bob!
# age = 25
# city = Mumbai
```

```python
# Unpacking when calling a function
def add(a, b, c):
    return a + b + c

nums = [1, 2, 3]
info = {"a": 1, "b": 2, "c": 3}

print(add(*nums))    # unpacks list  → add(1, 2, 3)
print(add(**info))   # unpacks dict  → add(a=1, b=2, c=3)
```

---

## 7. Decorator Chaining

Multiple decorators stack on top of each other. **Applied bottom-up, executed top-down.**

```python
def bold(func):
    def wrapper():
        return "<b>" + func() + "</b>"
    return wrapper

def italic(func):
    def wrapper():
        return "<i>" + func() + "</i>"
    return wrapper

@bold          # applied second (outer)
@italic        # applied first (inner)
def greet():
    return "Hello"

print(greet())   # <b><i>Hello</i></b>

# BTS — what Python does:
# greet = bold(italic(greet))
# So execution: bold wraps italic which wraps original
```

```
Execution order:
bold.wrapper START
  italic.wrapper START
    original greet()
  italic.wrapper END
bold.wrapper END
```

---

## 8. Generator vs Iterator

### Iterator
Any object with `__iter__()` and `__next__()`. Loads everything in memory first.

### Generator
A **lazy iterator** — produces values **one at a time**, only when asked. Uses `yield` instead of `return`.

```python
# Regular function — all values created at once, stored in memory
def get_numbers_list(n):
    result = []
    for i in range(n):
        result.append(i * i)
    return result                # returns full list


# Generator — creates ONE value at a time, pauses at yield
def get_numbers_gen(n):
    for i in range(n):
        yield i * i              # pause here, send value, resume on next()


# Memory comparison
import sys
lst = get_numbers_list(1000)
gen = get_numbers_gen(1000)

print(sys.getsizeof(lst))        # ~8856 bytes — full list in memory
print(sys.getsizeof(gen))        # ~112 bytes  — just the generator object


# Using a generator
gen = get_numbers_gen(5)
print(next(gen))   # 0
print(next(gen))   # 1
print(next(gen))   # 4
# or just loop it:
for val in get_numbers_gen(5):
    print(val)
```

### BTS — Generator State Machine

```
yield creates a "pause point":
  call next() → run until yield → send value → FREEZE state
  call next() → resume from freeze → run until next yield → FREEZE
  no more yields → raises StopIteration
```

**When to use Generator:**
- Large datasets (reading big files line by line)
- Infinite sequences
- When you don't need all values at once

---

## 9. Method Overloading

**Python doesn't support true method overloading** (same name, different params) like Java/C++.

If you define the same method twice, the **second one overwrites the first**.

```python
class Calculator:
    def add(self, a, b):
        return a + b

    def add(self, a, b, c):    # this REPLACES the above add()
        return a + b + c

c = Calculator()
# c.add(1, 2)      # TypeError! Only the 3-param version exists
print(c.add(1, 2, 3))   # works → 6
```

### Python's Way — Default Args / *args

```python
class Calculator:
    # Handle variable number of args with defaults or *args
    def add(self, *args):
        return sum(args)        # works for any number of arguments

c = Calculator()
print(c.add(1, 2))        # 3
print(c.add(1, 2, 3))     # 6
print(c.add(1, 2, 3, 4))  # 10
```

```python
# Using functools.singledispatch for type-based overloading
from functools import singledispatch

@singledispatch
def process(data):
    print(f"Unknown type: {type(data)}")

@process.register(int)
def _(data):
    print(f"Processing int: {data * 2}")

@process.register(str)
def _(data):
    print(f"Processing string: {data.upper()}")

process(10)       # Processing int: 20
process("hello")  # Processing string: HELLO
```

---

## 10. OOPs — 5 Interview Questions

---

### Q1. What are the 4 pillars of OOP? Explain with examples.

```python
# 1. ENCAPSULATION — bundling data + methods, hiding internals
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance     # __ makes it private

    def deposit(self, amount):
        self.__balance += amount

    def get_balance(self):           # controlled access via method
        return self.__balance

acc = BankAccount(1000)
# print(acc.__balance)    # AttributeError — can't access directly
print(acc.get_balance())  # 1000 — access through method only


# 2. ABSTRACTION — hide complex logic, show only what's needed
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass                         # force subclasses to implement

class Circle(Shape):
    def __init__(self, r): self.r = r
    def area(self): return 3.14 * self.r ** 2

# Shape()        # TypeError — can't instantiate abstract class
Circle(5).area() # 78.5 — use the concrete class


# 3. INHERITANCE — child class reuses parent's code
class Animal:
    def speak(self):
        return "Some sound"

class Dog(Animal):
    def speak(self):                 # override parent method
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

Dog().speak()    # "Woof!"
Cat().speak()    # "Meow!"


# 4. POLYMORPHISM — same interface, different behavior
animals = [Dog(), Cat(), Animal()]
for a in animals:
    print(a.speak())   # each calls its own speak() — polymorphism
```

---

### Q2. What is the difference between `__str__` and `__repr__`?

```python
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        # For end users — readable
        return f"{self.name}: ₹{self.price}"

    def __repr__(self):
        # For developers — should be unambiguous, ideally recreatable
        return f"Product(name='{self.name}', price={self.price})"


p = Product("Laptop", 50000)
print(p)          # calls __str__  → "Laptop: ₹50000"
print(repr(p))    # calls __repr__ → "Product(name='Laptop', price=50000)"

# In a list, __repr__ is used
print([p])        # [Product(name='Laptop', price=50000)]
```

**Rule of thumb:** `__str__` = for users, `__repr__` = for developers/debugging.

---

### Q3. What is `super()` and when do you use it?

```python
class Vehicle:
    def __init__(self, brand, speed):
        self.brand = brand
        self.speed = speed

    def info(self):
        return f"{self.brand} goes {self.speed}km/h"


class Car(Vehicle):
    def __init__(self, brand, speed, num_doors):
        super().__init__(brand, speed)   # calls Vehicle.__init__
        self.num_doors = num_doors       # adds extra attribute

    def info(self):
        base = super().info()            # reuse parent's info()
        return f"{base}, {self.num_doors} doors"


c = Car("Toyota", 180, 4)
print(c.info())   # Toyota goes 180km/h, 4 doors
```

**super() avoids hardcoding the parent class name and handles MRO (Method Resolution Order) correctly in multiple inheritance.**

---

### Q4. What is MRO (Method Resolution Order) in Python?

Python uses **C3 Linearization** to decide which method to call in multiple inheritance.

```python
class A:
    def hello(self): return "A"

class B(A):
    def hello(self): return "B"

class C(A):
    def hello(self): return "C"

class D(B, C):   # inherits from both B and C
    pass


d = D()
print(d.hello())       # "B" — follows MRO

# Check the MRO
print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)
# Python searches LEFT to RIGHT, then up
```

**Order:** D → B → C → A → object. First match wins.

---

### Q5. What is the difference between class method, static method, and instance method?

```python
class Employee:
    company = "TechCorp"         # class variable (shared)

    def __init__(self, name, salary):
        self.name = name         # instance variable (per object)
        self.salary = salary

    # INSTANCE METHOD — works with instance data, takes self
    def get_details(self):
        return f"{self.name} earns {self.salary}"

    # CLASS METHOD — works with class data, takes cls
    @classmethod
    def change_company(cls, new_name):
        cls.company = new_name   # changes for ALL instances

    # STATIC METHOD — no access to instance or class, just utility
    @staticmethod
    def is_valid_salary(salary):
        return salary > 0        # pure logic, no self or cls needed


e1 = Employee("Alice", 50000)
e2 = Employee("Bob", 60000)

# Instance method — needs an object
print(e1.get_details())           # Alice earns 50000

# Class method — can call on class itself
Employee.change_company("NewCorp")
print(e1.company)                 # NewCorp (changed for all)
print(e2.company)                 # NewCorp

# Static method — no instance needed
print(Employee.is_valid_salary(50000))   # True
print(Employee.is_valid_salary(-100))    # False
```

**Summary table:**

| | Access `self` | Access `cls` | Use when |
|---|---|---|---|
| Instance method | ✅ | ✅ (via self) | Working with object data |
| Class method | ❌ | ✅ | Working with class-level data |
| Static method | ❌ | ❌ | Utility logic related to the class |

---

*Happy revising! 🚀*
