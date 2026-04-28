# 🐍 Python Mastery Notes

---

## 📖 Table of Contents

| # | Topic | Every Case Covered |
|---|---|---|
| [01](#-topic-01--compiled-vs-interpreted--what-is-python) | What is Python | Compiled vs interpreted, hybrid, bytecode, PVM, CPython, JIT |
| [02](#-topic-02--basic-syntax) | Basic Syntax | 4 stages, INDENT/DEDENT, colons, comments vs docstrings, `__name__`, f-strings, imports |
| [03](#-topic-03--variables--datatypes) | Variables & Datatypes | PyObject, label vs box, int/float/str/bool/None/bytes, interning, mutability, copy vs deepcopy |
| [04](#-topic-04--operators) | Operators | Dunder methods, resolution flow, arithmetic, comparison, logical, bitwise, walrus, precedence, overloading |
| [05](#-topic-05--type-casting) | Type Casting | Numeric tower, int/float/str/bool/Decimal, all edge cases, error types |
| [06](#-topic-06--conditional-statements) | Conditionals | Bytecode jumps, guard clauses, truthiness, ternary, match/case, sequences, dicts, classes, guards |
| [07](#-topic-07--loops) | Loops | Iterator protocol, while, for, range, enumerate, zip, break/continue/else, all comprehensions, generators, yield, reduce |
| [08](#-topic-08--exception-handling) | Exception Handling | Stack unwinding, full hierarchy, try/except/else/finally, raise/chain, custom exceptions, context managers |
| [09](#-topic-09--functions--built-in-functions) | Functions | First-class, stack frames, all arg types, /, *, mutable default, LEGB, global/nonlocal, closures, lambda, decorators, builtins |

---

## 🧠 The Unifying Mental Model

```
Everything in Python is an OBJECT on the HEAP:
  42, "hello", [1,2,3], def f(): ..., class C:  — all objects

A VARIABLE is a NAME in a namespace dict pointing to an object:
  x = 42  means  globals["x"] = <address of int object 42>

Every object has:
  ob_refcnt  → how many names/containers point here
  ob_type    → what class/type it is
  ob_val     → the actual value(s)

When ob_refcnt hits 0 → object freed immediately (reference counting GC)
```

---

# 🐍 Topic 01 — Compiled vs Interpreted & What is Python?

> *"Python is called interpreted — but that's a simplification. Understanding the real execution model changes how you think about performance, errors, and what Python actually does with your code."*

---

## 1. Compiled Languages

You write code → compiler reads **entire file at once** → produces binary (machine code) → you run that binary.

```
Source (.c / .go)
      │
  [COMPILER] ← reads whole file
      │
  Binary (.exe / .out)
      │
  CPU runs directly ⚡ (no translation at runtime)
```

```c
// C example
#include <stdio.h>
int main() { printf("Hello\n"); }

// Two separate steps:
// gcc hello.c -o hello    ← compile
// ./hello                 ← run binary
```

**Key traits:**
- All errors caught before running (compile-time errors)
- Binary is platform-specific (Windows binary won't run on Linux)
- Very fast — CPU executes native instructions directly
- Examples: C, C++, Go, Rust

What the compiler actually does in multiple passes:
```
Source → Lexer (tokens) → Parser (AST) → Semantic Analysis
       → Optimizer → Code Generator → Binary
```

---

## 2. Interpreted Languages

No separate compile step. Interpreter reads source and executes **line by line** at runtime.

```
Source → [INTERPRETER] → reads line 1 → executes line 1
                       → reads line 2 → executes line 2
                       → ...
```

**Key traits:**
- Errors only appear when that specific line runs
- Same code runs anywhere the interpreter exists
- Slower (translation happens during execution)
- Examples: early PHP, older Ruby, shell scripts

---

## 3. Python Is a Hybrid

Python's documentation says "interpreted." That's incomplete. Here's what **actually happens**:

```
python app.py
      │
      ▼
┌──────────────────────────────────────────┐
│  STAGE 1: COMPILATION (hidden, automatic)│
│  .py source → bytecode (.pyc)            │
│  Stored in __pycache__/                  │
│  Platform-neutral intermediate code      │
│                                          │
│  STAGE 2: INTERPRETATION                 │
│  PVM (Python Virtual Machine)            │
│  reads bytecode instruction by           │
│  instruction and executes                │
└──────────────────────────────────────────┘
```

**Python = Compiled to bytecode + Interpreted by PVM = Hybrid**

The `.pyc` file is proof:
```python
import py_compile, os

py_compile.compile("yourfile.py")
print(os.listdir("__pycache__"))
# ['yourfile.cpython-311.pyc']  ← bytecode file
```

On second run, Python checks: has `.py` changed? No → skip recompilation, run `.pyc` directly → faster startup.

---

## 4. The Bytecode — What It Looks Like

```python
import dis

def add(a, b):
    return a + b

dis.dis(add)
```

```
Output:
  RESUME          0
  LOAD_FAST       0 (a)
  LOAD_FAST       1 (b)
  BINARY_OP       0 (+)
  RETURN_VALUE
```

Not machine code. Not your source. An intermediate language only the PVM understands. Platform-neutral — same `.pyc` runs on any OS with CPython installed.

---

## 5. CPython — The Default Python

When you download Python from python.org, you get **CPython** — the reference implementation.

```
CPython = the PVM is written in C
        = your Python code runs inside a C program
```

When you call `sum([1,2,3])`, Python's PVM (written in C) executes C code under the hood. That's why Python libraries like NumPy are fast — they're C code with a Python API on top.

### Other Implementations

| Name | Written In | Why It Exists |
|---|---|---|
| **CPython** | C | Default, most compatible |
| **PyPy** | Python+RPython | JIT compilation → much faster |
| **Jython** | Java | Runs on JVM, Java interop |
| **MicroPython** | C | Microcontrollers, embedded |

---

## 6. JIT Compilation — Why PyPy Is Faster

CPython interprets bytecode one instruction at a time.

PyPy uses **Just-In-Time (JIT)** compilation:
```
Start interpreting → detect "hot paths" (code running many times)
                  → compile those paths to native machine code on the fly
                  → next time that code runs → native speed ⚡
```

This is also how Java (JVM) and JavaScript (V8) achieve high performance despite being "interpreted."

---

## 7. Full Execution Pipeline

```
your_code.py
    │
    │  Lexing (tokenizer)
    ▼
Tokens (NAME, OP, STRING, INDENT, NEWLINE...)
    │
    │  Parsing
    ▼
Abstract Syntax Tree (AST)   ← SyntaxErrors caught here
    │
    │  Compilation
    ▼
Bytecode (.pyc)
    │
    │  Execution
    ▼
CPython PVM
    │
    │  System calls
    ▼
Operating System / Hardware
```

Every `print("hello")` travels this entire chain.

---

## 8. Why Python Is Slow But Dominates Industry

```
Time breakdown in a real production web request:
  Database query:   ~50ms   ← actual bottleneck
  Network I/O:      ~20ms
  File I/O:         ~10ms
  Python code:      ~0.1ms  ← negligible

Optimizing Python execution speed is almost always the wrong problem.
```

Python dominates because:
- **Developer velocity** — write features 3–5× faster than Java/C++
- **Ecosystem** — 500,000+ packages on PyPI
- **AI/ML dominance** — TensorFlow, PyTorch, NumPy are C/C++ under the hood
- **Glue language** — wraps fast C/Fortran libraries with clean Python API
- **Readability** — onboarding new engineers is faster

Instagram runs Django (Python). They don't rewrite in C++ because developer time costs more than servers.

---

## Summary

```
.py file
  → Python compiler  → bytecode (.pyc) in __pycache__/
  → PVM interprets bytecode
  = HYBRID (not purely interpreted, not purely compiled)

SyntaxErrors: caught at parse stage, before any code runs
RuntimeErrors: caught during PVM execution

CPython = default Python, PVM written in C
PyPy    = JIT compiled Python, much faster for CPU-heavy code

Performance: I/O (DB, network) is the real bottleneck, not Python speed
```

---

## 🎯 5 Questions

1. What file does Python create in `__pycache__` and why?
2. At which stage are SyntaxErrors caught?
3. What does PVM stand for and what does it consume?
4. Why is PyPy faster than CPython?
5. Why doesn't Python's execution speed usually matter in production?

---

<!-- ══════════════════════════════════════════════════════ -->

# 🐍 Topic 02 — Basic Syntax

> *"Python's syntax is minimal but precise. Whitespace has meaning, colons are mandatory, and a single indentation mistake is a grammar error — not a style issue."*

---

## 1. How Python Reads Your File — 4 Stages

```
your_file.py (raw text on disk)
      │
      ▼  Stage 1: TOKENIZER (Lexer)
  Reads characters, groups into tokens:
  NAME("x"), OP("="), NUMBER(10), NEWLINE
  INDENT, DEDENT, COLON, STRING, ...

      │
      ▼  Stage 2: PARSER
  Tokens → Abstract Syntax Tree
  Checks grammar rules
  ⚠ SyntaxErrors caught HERE — before any code runs

      │
      ▼  Stage 3: COMPILER
  AST → Bytecode (.pyc in __pycache__/)

      │
      ▼  Stage 4: PVM
  Executes bytecode instruction by instruction
  RuntimeErrors happen here
```

**Critical insight:** A SyntaxError fires even if the broken line is inside an `if False:` block that would never execute — the parser checks everything before running anything.

---

## 2. Indentation — The Grammar Rule

In C/Java, `{}` defines blocks. In Python, indentation defines blocks. This is **not style** — it's grammar enforced by the tokenizer.

The tokenizer generates special `INDENT` and `DEDENT` tokens:

```
if x > 0:           → COLON NEWLINE
    print("yes")    → INDENT  NAME("print") ... NEWLINE
    print("ok")     → NAME("print") ... NEWLINE
print("done")       → DEDENT NAME("print") ... NEWLINE
```

The parser uses `INDENT`/`DEDENT` to build block structure — no `{}` needed.

### All Indentation Rules

```python
# ✅ Standard — 4 spaces (PEP 8, used by everyone in industry)
if True:
    print("hello")
    print("world")

# ✅ Legal but non-standard — 2 spaces (consistent = OK)
if True:
  print("hello")
  print("world")

# ✅ Legal — 1 space (consistent = OK, but ugly)
if True:
 print("hello")

# ❌ IndentationError — inconsistent inside same block
if True:
    print("hello")
       print("world")   # 7 spaces — different from 4

# ❌ IndentationError — block under block must be deeper
if True:
    print("a")
  print("b")   # less indented than block — error

# ❌ TabError — mixing tabs and spaces (Python 3 forbids this)
if True:
    print("spaces")
	print("tab")   # tab character — crashes

# ❌ IndentationError — empty block not allowed
if True:
# comment
# nothing here — SyntaxError: expected an indented block
```

### Nested Blocks — Each Level + 4 Spaces

```python
def process(order):               # level 0
    if order.valid:               # level 1
        for item in order.items: # level 2
            if item.in_stock:    # level 3
                ship(item)       # level 4
            else:
                notify(item)     # level 4
    else:
        cancel(order)            # level 1
```

---

## 3. The Colon — Required After Every Block Header

```python
if condition:       # colon required
    pass

elif condition:     # colon required
    pass

else:               # colon required
    pass

for x in items:     # colon required
    pass

while condition:    # colon required
    pass

def func():         # colon required
    pass

class MyClass:      # colon required
    pass

try:                # colon required
    pass
except Error:       # colon required
    pass
```

Missing colon = `SyntaxError: expected ':'`

---

## 4. Statements — One Per Line

```python
# Normal — one statement per line, no terminator needed
name = "Arjun"
age  = 22
print(name, age)

# Semicolons — allowed but avoid (not Pythonic)
name = "Arjun"; age = 22; print(name)

# One-liner if (acceptable for simple guard clauses)
if not user: return None
if error: raise ValueError(error)
```

### Line Continuation

```python
# ❌ Backslash — fragile (breaks if trailing space after \)
result = value_one + value_two + \
         value_three

# ✅ Implicit continuation inside brackets — safe and preferred
result = (
    value_one
    + value_two
    + value_three
)

# Works inside any brackets: (), [], {}
config = {
    "host": "localhost",
    "port": 8000,
    "debug": True,
}

result = some_function(
    argument_one,
    argument_two,
    argument_three,
)
```

---

## 5. Comments — Two Types

### Single-Line `#`

```python
# This is a comment — discarded completely at tokenizer stage
# It never reaches the parser or compiler — doesn't exist as code
x = 10  # inline comment — ignored from # onward

# Write WHY, not WHAT:
# ❌ x = x + 1  # add 1 to x    (obvious, useless)
# ✅ x = x + 1  # offset: API uses 0-based indexing internally
```

### Docstrings `"""..."""` — NOT Comments

```python
def get_user(user_id: int) -> dict:
    """
    Fetch user from database by ID.

    Args:
        user_id (int): Unique user identifier.

    Returns:
        dict: User data {'id', 'name', 'email'}

    Raises:
        ValueError: If user_id is not a positive integer.
        NotFoundError: If user does not exist.

    Example:
        >>> get_user(42)
        {'id': 42, 'name': 'Arjun', 'email': 'a@b.com'}
    """
    pass
```

Docstrings are **string objects** stored as `func.__doc__`:
```python
print(get_user.__doc__)    # prints the docstring
help(get_user)             # formatted display in terminal
```

IDEs use `__doc__` for tooltips. Sphinx/pdoc use it to generate HTML documentation. `#` comments are completely invisible to everything except the human reader.

### Multi-line "Comments" — Common Pattern

```python
# For actual multi-line comments, use multiple # lines:
# This block validates the JWT token.
# It checks expiry, signature, and audience claims.
# Returns True if valid, raises AuthError if not.
def validate_token(token):
    pass

# Triple-quoted strings used as block comments (technically a string literal)
# Python evaluates it but discards it immediately — no variable holds it
"""
This is sometimes used as a block comment.
But it IS evaluated (creates a str object, then discards it).
Use # for true comments. Use """ only for docstrings.
"""
```

---

## 6. Identifiers — Naming Rules

```
✅ Must start with letter (a–z, A–Z) or underscore (_)
✅ Can contain letters, digits (0–9), underscores
✅ Case-sensitive: name ≠ Name ≠ NAME
❌ Cannot start with a digit
❌ Cannot be a Python keyword
❌ No spaces, hyphens, @, $, etc.
```

```python
# ✅ Valid
user_name = "Arjun"
_private  = "hidden"
UserID    = 101
value2    = 99
__dunder__= "special"

# ❌ Invalid
2fast     = "no"   # starts with digit
user-name = "no"   # hyphen not allowed
class     = "no"   # reserved keyword
my var    = "no"   # space not allowed
```

### PEP 8 Naming Conventions

| What | Convention | Example |
|---|---|---|
| Variables & functions | `snake_case` | `user_name`, `get_data()` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_RETRIES = 3` |
| Classes | `PascalCase` | `UserProfile`, `OrderItem` |
| Internal/private | `_single_underscore` | `_validate()`, `_cache` |
| Name mangling in class | `__double_underscore` | `__password` |
| Special dunder methods | `__name__` | `__init__`, `__str__` |
| Module names | `lowercase` | `utils`, `db_client` |
| Package names | `lowercase` | `mypackage` |

---

## 7. Python Keywords — All 35

These are reserved. You cannot use them as variable names.

```python
import keyword
print(keyword.kwlist)
```

```
False    None     True     and      as       assert
async    await    break    class    continue def
del      elif     else     except   finally  for
from     global   if       import   in       is
lambda   nonlocal not      or       pass     raise
return   try      while    with     yield
```

---

## 8. `import` — Loading Modules

```python
# Import whole module
import os
import sys
import json

# Import specific names
from os import path, getcwd
from datetime import datetime, timedelta

# Import with alias (very common)
import numpy as np
import pandas as pd
from datetime import datetime as dt

# Relative import (inside a package)
from . import utils          # sibling module
from .models import User     # from sibling module
from ..config import DB_URL  # from parent package

# ❌ Avoid — pollutes namespace, unclear where names come from
from os import *
```

### What Happens When You Import — Under the Hood

```
import os
    │
    ▼
Check sys.modules: is "os" already imported?
    │
    ├── YES → return cached module object (no re-execution)
    │
    └── NO  → find os.py in sys.path
               execute os.py top to bottom (once only)
               store module object in sys.modules["os"]
               bind name "os" in current namespace
```

```python
import sys

import os              # first time: executes os.py
import os              # second time: returns from sys.modules cache

print("os" in sys.modules)  # True
print(sys.modules["os"])    # <module 'os' from '...'>
```

**This is why import order matters:** side effects in a module (printing, connecting to DB) only run on the **first** import. Subsequent imports return the cached object instantly.

---

## 9. The `__name__` Variable

Every Python file has `__name__`. Its value depends on how the file is used:

```
python myfile.py    →  __name__ == "__main__"    (run directly)
import myfile       →  __name__ == "myfile"      (imported)
```

```python
# utils.py

def calculate_tax(amount, rate):
    return amount * rate

def format_currency(amount):
    return f"₹{amount:,.2f}"

# This block ONLY runs when: python utils.py
# It does NOT run when: import utils
if __name__ == "__main__":
    print(format_currency(calculate_tax(1000, 0.18)))
```

Without this guard, every `import utils` would execute your test/demo code.

---

## 10. `print()` — All Parameters

```python
# print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)

print("a", "b", "c")              # a b c          (sep=' ' default)
print("a", "b", "c", sep="-")     # a-b-c
print("a", "b", "c", sep="")      # abc

print("Loading", end="")           # no newline
print("...", end=" ")
print("Done")
# Output: Loading... Done

# Print to stderr (for errors/logs)
import sys
print("Error!", file=sys.stderr)

# Force flush (real-time logging)
print("Processing...", flush=True)
```

---

## 11. f-Strings — All Forms (Python 3.6+)

```python
name   = "Arjun"
age    = 22
salary = 75000.50
pi     = 3.14159

# Basic embedding
f"Hello {name}"              # Hello Arjun

# Expressions
f"Next year: {age + 1}"     # Next year: 23
f"Upper: {name.upper()}"    # Upper: ARJUN

# Number formatting
f"{salary:,.2f}"             # 75,000.50
f"{pi:.2f}"                  # 3.14
f"{1000000:,}"               # 1,000,000
f"{42:08b}"                  # 00101010  (8-bit binary)
f"{0.75:.1%}"                # 75.0%

# Padding and alignment
f"{'left':<10}|"             # left      |
f"{'right':>10}|"            #      right|
f"{'center':^10}|"           #   center  |

# Debug format (Python 3.8+)
value = 42
f"{value=}"                  # value=42   (shows name + value)

# Multi-line
message = (
    f"User: {name}\n"
    f"Age: {age}\n"
    f"Salary: ₹{salary:,.2f}"
)

# Nested quotes
f"He said {'hello'!r}"       # He said 'hello'

# !r, !s, !a conversion flags
f"{name!r}"    # 'Arjun'  (repr)
f"{name!s}"    # Arjun    (str)
f"{name!a}"    # 'Arjun'  (ascii)
```

---

## 12. `pass` Statement

`pass` is a no-op. Required when Python syntactically needs a block but you have nothing to put there.

```python
# Placeholder during development
def send_email(to, subject, body):
    pass   # TODO: implement SMTP logic

# Empty class
class Config:
    pass

# Intentional no-op in conditional
if event.type == "heartbeat":
    pass   # expected, nothing to do
else:
    handle_event(event)

# Silencing a specific exception (use with care — always at least log)
try:
    cleanup()
except Exception:
    pass   # ⚠ dangerous — adds: import logging; logging.warning("cleanup failed", exc_info=True)
```

---

## 13. Complete Syntax Quick Reference

```python
# Block headers always end with colon + indented body
if condition:        body
elif condition:      body
else:                body

for var in iterable: body
while condition:     body

def function():      body
class MyClass:       body

try:                 body
except Error:        body
else:                body
finally:             body

with context as var: body
```

---

## Simple Production Example

```python
# config.py — demonstrates __name__, docstrings, f-strings, naming conventions

import os

# Constants use UPPER_SNAKE_CASE
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = int(os.environ.get("DB_PORT", "5432"))
DEBUG   = os.environ.get("DEBUG", "false").lower() == "true"


def get_db_url(host: str = DB_HOST, port: int = DB_PORT) -> str:
    """
    Build a PostgreSQL connection URL.

    Args:
        host (str): Database hostname.
        port (int): Database port.

    Returns:
        str: Full connection URL.
    """
    return f"postgresql://{host}:{port}/appdb"


def print_config() -> None:
    """Print current configuration to stdout."""
    print(f"{'DB Host':<12} {DB_HOST}")
    print(f"{'DB Port':<12} {DB_PORT}")
    print(f"{'Debug':<12} {DEBUG}")
    print(f"{'DB URL':<12} {get_db_url()}")


# Entry point guard — only runs when: python config.py
# Does NOT run when: import config
if __name__ == "__main__":
    print_config()
```

---

## Summary

```
4 stages: Tokenizer → Parser (SyntaxErrors here) → Compiler → PVM
Indentation: 4 spaces. INDENT/DEDENT tokens. Not style — grammar.
Colon: required after every block header
Comments: # discarded at tokenizer | """ stored as __doc__
__name__: "__main__" when run directly, module name when imported
f-strings: f"Hello {name}" — expressions, formatting, !r/!s/!a flags
Imports: cached in sys.modules — execute once, return cached after
pass: syntactic no-op for empty blocks
PEP 8: snake_case vars/funcs, PascalCase classes, UPPER_SNAKE constants
```

---

## 🎯 5 Questions

1. At which stage are SyntaxErrors caught, and why does this mean they fire even in unreachable code?
2. What are `INDENT` and `DEDENT` tokens?
3. What is the difference between `#` comments and `"""` docstrings?
4. What value does `__name__` have when a file is imported vs run directly?
5. Why does importing the same module 10 times not execute it 10 times?

---

<!-- ══════════════════════════════════════════════════════ -->

# 🐍 Topic 03 — Variables & Datatypes

> *"In Python, everything is an object. A variable is a name tag pointing to one — not a box containing a value. This single mental model explains mutability, copying, identity checks, and why `a = b` for lists behaves so differently from integers."*

---

## 1. How Python Stores Objects — PyObject

Every Python object, regardless of type, is a C struct with at minimum:

```c
typedef struct {
    Py_ssize_t  ob_refcnt;    // reference count (how many names point here)
    PyTypeObject *ob_type;    // pointer to the type/class
} PyObject;
// Plus the actual value fields depending on type
```

Memory layout for `x = 42`:
```
Heap memory:
┌──────────────────────────────┐
│  ob_refcnt  =  1             │  ← one name points here
│  ob_type    →  <int class>   │
│  ob_val     =  42            │
└──────────────────────────────┘
         ▲
         │ pointer
    namespace["x"]
```

```python
x = 42
print(id(x))           # memory address, e.g. 140234567890
print(type(x))         # <class 'int'>
print(sys.getsizeof(x))# 28 bytes — int(42) costs 28 bytes in Python
                       # vs 4 bytes in C — the overhead is ob_refcnt + ob_type
```

---

## 2. Variables Are Labels, Not Boxes

```python
# C: x IS a box with 10 inside
int x = 10;

# Python: x is a label pointing to an int object containing 10
x = 10
```

### What Assignment Really Does

```python
x = 10      # namespace["x"] = <address of int object 10>
y = x       # namespace["y"] = same address (NOT a copy!)

print(id(x) == id(y))   # True — same object in memory
print(x is y)           # True

x = 20      # namespace["x"] = <address of NEW int object 20>
            # int object 10 is still there, y still points to it

print(y)         # 10 — unchanged
print(id(x) == id(y))  # False — x moved to new object
```

```
BEFORE x = 20:      AFTER x = 20:
  x ──┐               x ──────→ [int: 20]  (new object)
      ▼
  [int: 10]                      [int: 10]  (still exists)
      ▲               y ─────────────────┘
  y ──┘
```

---

## 3. Integer — `int`

### Unlimited Precision

```python
# No integer overflow in Python
print(2 ** 100)          # 1267650600228229401496703205376  (exact!)
print(factorial(50))     # exact 65-digit number

# All literal forms
decimal   = 100
binary    = 0b1010       # 10
octal     = 0o17         # 15
hex_val   = 0xFF         # 255
readable  = 1_000_000    # underscores for readability, value = 1000000
neg       = -42
```

### Integer Interning — The Cache [-5 to 256]

CPython pre-creates integer objects for -5 to 256 at startup and **reuses them forever**:

```python
a = 100
b = 100
print(a is b)    # True  ← same cached object!
print(id(a) == id(b))  # True — same memory address

a = 257
b = 257
print(a is b)    # False ← outside cache, new object each time
print(a == b)    # True  ← same VALUE though

# The cache in memory (conceptually):
# {-5: PyObject(int,-5), -4: PyObject(int,-4), ..., 256: PyObject(int,256)}
# int(42) returns the cached object — no allocation
# int(1000) allocates a new PyObject — new address
```

**Rule:** Always use `==` to compare values. `is` only for `None`, `True`, `False`.

### Useful int Methods

```python
n = 255
n.bit_length()             # 8  ← bits needed to represent 255
n.to_bytes(2, 'big')       # b'\x00\xff'
int.from_bytes(b'\xff', 'big')  # 255
bin(10)                    # '0b1010'
oct(8)                     # '0o10'
hex(255)                   # '0xff'
divmod(17, 5)              # (3, 2) — quotient and remainder at once
pow(2, 10, 1000)           # 24 — (2**10) % 1000, fast modular exponentiation
```

---

## 4. Float — `float`

### IEEE 754 Double — NOT Exact

```python
print(0.1 + 0.2)   # 0.30000000000000004  ← NOT 0.3!
```

Why: `0.1` in binary = `0.0001100110011...` (infinitely repeating). 64 bits truncates it → tiny error compounds.

```python
# All forms
f1 = 3.14
f2 = 2.5e3        # 2500.0 (scientific notation)
f3 = 1.5e-4       # 0.00015
f4 = .5           # 0.5
f5 = float('inf') # infinity
f6 = float('nan') # not a number

import math
math.isnan(float('nan'))   # True
math.isinf(float('inf'))   # True

# Rounding
round(3.7)         # 4
round(3.14159, 2)  # 3.14
math.floor(3.9)    # 3
math.ceil(3.1)     # 4
math.trunc(3.9)    # 3  (toward zero)

# Banker's rounding — Python rounds to even on .5
round(0.5)   # 0 ← rounds to even (0)
round(1.5)   # 2 ← rounds to even (2)
round(2.5)   # 2 ← rounds to even (2)
```

### Use `Decimal` for Money

```python
from decimal import Decimal, ROUND_HALF_UP

# ❌ Never float for money
print(19.99 * 1.18)   # 23.588200000000002

# ✅ Always Decimal for money
price = Decimal("19.99")  # string! not float!
tax   = Decimal("0.18")
total = price * (1 + tax)
print(total)          # 23.5882
print(total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))  # 23.59
```

---

## 5. Boolean — `bool`

### `bool` Is a Subclass of `int`

```python
isinstance(True, int)   # True — bool IS-A int!
True  == 1              # True
False == 0              # True
True  + True            # 2
True  * 5               # 5
int(True)               # 1
int(False)              # 0
```

### Truthiness — Every Object Has a Bool Value

Python calls `bool(x)` which calls `x.__bool__()` — or `x.__len__()` if `__bool__` not defined.

```python
# Falsy — evaluate to False in boolean context
bool(False)   # False
bool(None)    # False
bool(0)       # False
bool(0.0)     # False
bool("")      # False
bool([])      # False  ← empty list
bool({})      # False  ← empty dict
bool(set())   # False  ← empty set
bool(())      # False  ← empty tuple

# Truthy — everything else
bool(1)       # True
bool(-1)      # True  ← any non-zero
bool("0")     # True  ← non-empty string, even if content is "0"!
bool("False") # True  ← non-empty string!
bool([0])     # True  ← list with one element (even if that element is falsy)
bool(" ")     # True  ← space is non-empty
```

```python
# Idiomatic Python uses truthiness directly
if users:           # instead of len(users) > 0
if not errors:      # instead of len(errors) == 0
if response:        # instead of response is not None

# BUT be careful — 0 and "" are falsy
count = 0
if count:           # won't enter — 0 is falsy!
    print("has items")

# When 0 is a valid value, be explicit:
if count is not None:   # 0 is not None → enters correctly
    print("count exists")
```

---

## 6. String — `str`

### Immutable Sequence of Unicode Code Points

```python
# All literal forms
s1 = 'single'
s2 = "double"
s3 = """multi
line"""
s4 = '''also
multi'''
s5 = r"raw\nstring"      # backslash not processed: r prefix
s6 = b"bytes"            # bytes, not str
s7 = f"hello {name}"     # f-string (formatted)
s8 = rb"raw bytes"       # raw bytes

# String is IMMUTABLE
s = "hello"
s[0] = "H"   # TypeError: 'str' object does not support item assignment
```

### Indexing and Slicing

```python
s = "Python"
#    0 1 2 3 4 5
#   -6-5-4-3-2-1

s[0]      # 'P'
s[-1]     # 'n'
s[1:4]    # 'yth'  (start inclusive, end exclusive)
s[:3]     # 'Pyt'
s[3:]     # 'hon'
s[::2]    # 'Pto'  (every 2nd)
s[::-1]   # 'nohtyP'  (reversed)
s[1:5:2]  # 'yh'  (start=1, stop=5, step=2)
```

### String Interning

```python
# Identifier-like strings (letters, digits, underscores only) → auto-interned
a = "hello"
b = "hello"
print(a is b)        # True — same object

# With spaces/special chars → NOT automatically interned
a = "hello world"
b = "hello world"
print(a is b)        # False — different objects

# Force interning
import sys
a = sys.intern("hello world")
b = sys.intern("hello world")
print(a is b)        # True — now same object

# Why intern? When you have 1M rows from DB with same status values,
# interning means 1 object not 1M. Comparison becomes identity check (O(1)).
```

### Important String Methods

```python
s = "  Hello, World!  "

# Case
s.upper()          # "  HELLO, WORLD!  "
s.lower()          # "  hello, world!  "
s.title()          # "  Hello, World!  "
s.swapcase()       # "  hELLO, wORLD!  "

# Whitespace
s.strip()          # "Hello, World!"
s.lstrip()         # "Hello, World!  "
s.rstrip()         # "  Hello, World!"

# Search
s.find("World")    # 9  (-1 if not found)
s.index("World")   # 9  (raises ValueError if not found)
s.count("l")       # 3
s.startswith("  H")# True
s.endswith("!  ")  # True
"World" in s       # True  (calls __contains__)

# Modify (returns NEW string — immutable!)
s.replace("World", "Python")     # "  Hello, Python!  "
"a,b,c".split(",")               # ['a', 'b', 'c']
"a,b,c".split(",", maxsplit=1)   # ['a', 'b,c']
" ".join(["Hello", "World"])     # "Hello World"

# Validate
"hello123".isalnum()  # True
"hello".isalpha()     # True
"12345".isdigit()     # True
"  ".isspace()        # True
"Hello".istitle()     # True

# Format
"42".zfill(5)         # "00042"
"hello".center(11, "-")  # "---hello---"
f"{3.14:.2f}"            # "3.14"
```

### String Concatenation Performance

```python
# ❌ O(n²) — creates new string object every iteration
result = ""
for word in words:
    result += word   # NEW object each time; old object may be GC'd

# ✅ O(n) — join() pre-calculates length, allocates ONCE, fills in
result = "".join(words)

# Why: str is immutable. "ab" + "c" → new "abc" object allocated,
# "ab" contents copied over, "c" appended. At 10,000 words:
# += creates 10,000 intermediate strings (10,000 mallocs)
# join() does 1 malloc for the final string
```

---

## 7. NoneType — `None`

```python
# Exactly ONE None object exists in Python's entire runtime — singleton
x = None
y = None
print(x is y)        # True — ALWAYS (same singleton object)
print(id(None))      # same address every time

# Always check with 'is', never '=='
if x is None:        # ✅ correct — identity check
    pass
if x == None:        # ❌ wrong — __eq__ can be overridden by custom classes
    pass

# Common uses
def get_user(user_id) -> dict | None:
    user = db.find(user_id)
    return user if user else None    # signal "not found"

result = cache.get("key")   # returns None if missing
if result is None:
    result = compute()
    cache["key"] = result
```

---

## 8. Complex — `complex`

```python
z = 3 + 4j        # j is imaginary unit in Python (not i)
z.real             # 3.0
z.imag             # 4.0
abs(z)             # 5.0  (magnitude: sqrt(3²+4²))
z.conjugate()      # (3-4j)
complex(3, 4)      # (3+4j)
```

Used in signal processing, scientific computing, electrical engineering calculations.

---

## 9. Bytes and Bytearray — Raw Binary

```python
# bytes — immutable sequence of integers 0–255
b = b"hello"
print(b[0])            # 104  (ASCII code of 'h')
print(type(b))         # <class 'bytes'>

# Encode string to bytes
s = "Hello नमस्ते"
b = s.encode("utf-8")  # b'Hello \xe0\xa4\xa8\xe0\xa4\xae...'

# Decode bytes to string
s2 = b.decode("utf-8")
print(s2)              # Hello नमस्ते

# bytearray — mutable version of bytes
ba = bytearray(b"hello")
ba[0] = 72             # change 'h' (104) to 'H' (72)
print(ba)              # bytearray(b'Hello')
```

Used for: binary file I/O, network sockets, image data, cryptography.

---

## 10. Type Checking

```python
# type() — exact type (no inheritance)
type(42) is int          # True
type(True) is int        # False — True is bool, not int (exactly)

# isinstance() — includes inheritance (preferred in production)
isinstance(42, int)      # True
isinstance(True, int)    # True — bool IS-A int
isinstance(True, bool)   # True

# Check multiple types
isinstance("hello", (str, bytes))   # True — is it str OR bytes?

# In production — always isinstance, not type():
def process(value):
    if not isinstance(value, (int, float)):
        raise TypeError(f"Expected number, got {type(value).__name__}")
```

---

## 11. Mutable vs Immutable — Complete Rules

```python
# IMMUTABLE: int, float, bool, str, tuple, frozenset, bytes, NoneType
# Any "change" creates a NEW object

s = "hello"
id_before = id(s)
s += " world"
id_after  = id(s)
print(id_before == id_after)  # False — new object

# MUTABLE: list, dict, set, bytearray
# Change modifies the SAME object, all references see it

a = [1, 2, 3]
b = a               # b points to SAME list
b.append(4)
print(a)            # [1, 2, 3, 4]  ← a sees it too!

# Copying
b = a.copy()        # shallow copy — new list, same element objects
import copy
b = copy.deepcopy(a)  # deep copy — fully independent at all levels

# += on mutable vs immutable
a = [1, 2, 3]
id_before = id(a)
a += [4]            # calls list.__iadd__ — MODIFIES IN PLACE
print(id(a) == id_before)  # True — same object!

t = (1, 2, 3)
id_before = id(t)
t += (4,)           # tuple immutable → creates NEW tuple
print(id(t) == id_before)  # False — new object
```

---

## 12. Complete Datatype Summary Table

| Type | Mutable | Ordered | Indexed | Literal |
|---|---|---|---|---|
| `int` | ❌ | — | — | `42`, `0xFF` |
| `float` | ❌ | — | — | `3.14`, `2.5e3` |
| `bool` | ❌ | — | — | `True`, `False` |
| `str` | ❌ | ✅ | ✅ | `"hello"`, `f"hi"` |
| `NoneType` | ❌ | — | — | `None` |
| `bytes` | ❌ | ✅ | ✅ | `b"data"` |
| `tuple` | ❌ | ✅ | ✅ | `(1, 2, 3)` |
| `frozenset` | ❌ | ❌ | — | `frozenset({1,2})` |
| `list` | ✅ | ✅ | ✅ | `[1, 2, 3]` |
| `dict` | ✅ | ✅* | — | `{"a": 1}` |
| `set` | ✅ | ❌ | — | `{1, 2, 3}` |
| `bytearray` | ✅ | ✅ | ✅ | `bytearray(b"x")` |

*dict preserves insertion order since Python 3.7

---

## Simple Production Example

```python
# user_profile.py — type validation using isinstance and truthiness

from decimal import Decimal

def create_profile(data: dict) -> dict:
    """Validate and normalise user profile data."""

    name = data.get("name")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("'name' must be a non-empty string")

    age = data.get("age")
    if not isinstance(age, int) or isinstance(age, bool):
        raise TypeError("'age' must be an integer")
    if not 13 <= age <= 120:
        raise ValueError(f"'age' must be 13–120, got {age}")

    balance = data.get("balance", "0")
    try:
        balance = Decimal(str(balance))
    except Exception:
        raise ValueError(f"'balance' must be a valid number, got {balance!r}")

    is_active = data.get("is_active", True)
    if not isinstance(is_active, bool):
        raise TypeError("'is_active' must be a boolean")

    return {
        "name":      name.strip(),
        "age":       age,
        "balance":   balance,
        "is_active": is_active,
    }


try:
    profile = create_profile({"name": "Arjun", "age": 22, "balance": "1500.50"})
    print(f"Profile: {profile}")

    create_profile({"name": "", "age": 22})  # empty name → error

except (ValueError, TypeError) as e:
    print(f"Validation error: {e}")
```

---

## Summary

```
Variable = name tag in namespace dict pointing to an object on the heap
Every object = ob_refcnt + ob_type + value field(s)
id(x) = memory address | type(x) = class | x is y = same object?

Immutable: int, float, bool, str, tuple, bytes, None
  "change" → new object created, old refcnt decremented

Mutable: list, dict, set, bytearray
  change modifies in place → all references see it
  a = b → both share SAME object → use a.copy() to get independent copy

Integer cache: -5 to 256 → always same object (interned)
Float: IEEE 754, not exact → use Decimal for money
bool: subclass of int (True=1, False=0)
None: singleton → always check with 'is None'
str: immutable, use join() not += in loops

isinstance() preferred over type() — handles inheritance correctly
```

---

## 🎯 5 Questions

1. What are the three C-level fields every Python object has?
2. Why does `a = b` for a list mean both see mutations, but for an int they don't?
3. What is the integer cache and why does `1000 is 1000` sometimes return `False`?
4. Why use `Decimal` for money and why pass it as a string (`Decimal("19.99")`)?
5. Why use `isinstance(x, int)` instead of `type(x) is int`?

---

<!-- ══════════════════════════════════════════════════════ -->

# 🐍 Topic 04 — Operators

> *"Every operator is a dunder method call in disguise. `a + b` is `a.__add__(b)`. Once you see that, you understand why operators work on custom objects, why some fail on certain types, and how to build types that support any operator."*

---

## 1. Operators Are Dunder Method Calls

```python
a + b      →   a.__add__(b)
a - b      →   a.__sub__(b)
a * b      →   a.__mul__(b)
a / b      →   a.__truediv__(b)
a // b     →   a.__floordiv__(b)
a % b      →   a.__mod__(b)
a ** b     →   a.__pow__(b)
a == b     →   a.__eq__(b)
a < b      →   a.__lt__(b)
a > b      →   a.__gt__(b)
a <= b     →   a.__le__(b)
a >= b     →   a.__ge__(b)
a & b      →   a.__and__(b)
a | b      →   a.__or__(b)
a ^ b      →   a.__xor__(b)
~a         →   a.__invert__()
a << b     →   a.__lshift__(b)
a >> b     →   a.__rshift__(b)
-a         →   a.__neg__()
+a         →   a.__pos__()
abs(a)     →   a.__abs__()
len(a)     →   a.__len__()
a[i]       →   a.__getitem__(i)
b in a     →   a.__contains__(b)
```

### Operator Resolution — Full Flow

```
a + b:
  1. Call a.__add__(b)
     ├── Returns a value → use it, done
     └── Returns NotImplemented?
           │
           ▼
  2. Call b.__radd__(a)   ← reflected (right-hand) version
     ├── Returns a value → use it, done
     └── Returns NotImplemented?
           │
           ▼
  3. Raise TypeError: unsupported operand type(s) for +

# Proof:
(5).__add__(3)         # 8
(5).__add__("hello")   # NotImplemented — int can't add str
```

---

## 2. Arithmetic Operators

```python
a, b = 17, 5

a + b    # 22  → a.__add__(b)
a - b    # 12  → a.__sub__(b)
a * b    # 85  → a.__mul__(b)
a / b    # 3.4 → a.__truediv__(b)  — ALWAYS returns float
a // b   # 3   → a.__floordiv__(b) — floor division
a % b    # 2   → a.__mod__(b)      — modulo
a ** b   # 1419857 → a.__pow__(b)  — exponentiation
-a       # -17 → a.__neg__()
abs(-a)  # 17  → a.__abs__()
```

### `/` vs `//` — Critical Difference

```python
7   / 2    #  3.5  ← always float
10  / 2    #  5.0  ← float even when even
7  // 2    #  3    ← floor (truncates toward -∞)
-7 // 2    # -4    ← floor of -3.5 = -4 (goes DOWN, not toward zero!)
7  // -2   # -4    ← floor of -3.5 = -4
-7 // -2   #  3    ← floor of 3.5 = 3
```

```
Floor division = floor(a / b) = largest integer ≤ result
  7  / 2  =  3.5  → floor( 3.5) =  3
  -7 / 2  = -3.5  → floor(-3.5) = -4  ← surprise!

int(-7 / 2) = int(-3.5) = -3  ← truncation toward zero (different!)
-7 // 2     = -4               ← floor (toward -∞)
```

### `%` Modulo — Follows Divisor Sign

```python
7  % 3    #  1   (7 = 2×3 + 1)
-7 % 3    #  2   (-7 = -3×3 + 2)  ← positive! follows divisor
7  % -3   # -2   (7 = -3×(-3) + (-2))
-7 % -3   # -1

# Real uses:
n % 2 == 0          # even check
i % len(lst)        # cycling/round-robin index
total_sec % 60      # seconds remainder
(hour + shift) % 24 # wrap-around clock arithmetic
```

### `**` Exponentiation

```python
2 ** 10      # 1024
2 ** 0.5     # 1.414...  (square root)
8 ** (1/3)   # 2.0       (cube root)
2 ** 100     # exact large integer (no overflow in Python)
pow(2, 10)   # 1024      (same as **)
pow(2, 10, 1000)  # 24   (2**10 % 1000 — fast modular exponentiation)
```

---

## 3. Comparison Operators

```python
a == b    # equal value        → a.__eq__(b)
a != b    # not equal          → a.__ne__(b)
a <  b    # less than          → a.__lt__(b)
a >  b    # greater than       → a.__gt__(b)
a <= b    # less or equal      → a.__le__(b)
a >= b    # greater or equal   → a.__ge__(b)
```

### Chained Comparisons

```python
# Python allows chaining — evaluates as (a < b) and (b < c)
x = 15
10 < x < 20       # True  — reads like math!
0 <= age <= 120   # valid age range
"a" <= grade <= "d"  # grade range

# How it works internally:
1 < 2 < 3   →  (1 < 2) and (2 < 3)  →  True and True  →  True
3 > 2 > 5   →  (3 > 2) and (2 > 5)  →  True and False →  False

# Note: middle value evaluated only once
1 < get_val() < 10   # get_val() called exactly once
```

### `==` vs `is` — Value vs Identity

```python
# == calls __eq__ → compares VALUES
# is checks id() → compares IDENTITY (same object?)

a = [1, 2, 3]
b = [1, 2, 3]   # same values, different objects
c = a

a == b    # True   ← same values
a is b    # False  ← different objects in memory
a is c    # True   ← c is literally the same object as a

# Rules:
# Use ==  for comparing values (almost always)
# Use is  ONLY for: None, True, False
x = None
if x is None:    # ✅ correct
if x == None:    # ❌ wrong — custom class could override __eq__
```

---

## 4. Logical Operators — `and`, `or`, `not`

These don't have dunder methods — handled directly by the interpreter's bytecode (`JUMP_IF_TRUE_OR_POP`, `JUMP_IF_FALSE_OR_POP`).

### They Return Operands, Not Booleans!

```python
# 'and' returns the FIRST FALSY value, or LAST value if all truthy
0     and "hello"    # 0       ← 0 is falsy, returned immediately
""    and "hello"    # ""      ← empty string falsy
"hi"  and "hello"   # "hello" ← all truthy, returns last
True  and 42         # 42      ← all truthy, returns last

# 'or' returns the FIRST TRUTHY value, or LAST if all falsy
0    or "hello"      # "hello" ← 0 falsy, skip; "hello" truthy
"hi" or "hello"      # "hi"    ← "hi" truthy, stop immediately
0    or ""           # ""      ← all falsy, returns last
None or 0 or False   # False   ← all falsy, returns last

# 'not' always returns True or False (actual bool)
not True     # False
not 0        # True
not "hello"  # False
not []       # True
```

### Short-Circuit Evaluation

The **right side may never be evaluated**:

```python
# 'and' — if left is falsy, right is NEVER evaluated
user = None
user and user.email    # None  ← 'user' is falsy, stops
                       # user.email NEVER called → no AttributeError!

def risky():
    print("risky called!")
    return True

False and risky()    # "risky called!" is NOT printed
True  or  risky()   # "risky called!" is NOT printed

# Why this matters — avoid expensive computation:
is_flag_on() and expensive_db_query()  # DB only hit if flag is on
```

### Production Patterns with `or` / `and`

```python
# Default value
name = user_input or "Anonymous"
port = os.environ.get("PORT") or 8000
timeout = config.get("timeout") or 30

# Safe attribute access
email = user and user.profile and user.profile.email

# Conditional execution
DEBUG and print("debug:", data)   # print only in debug mode

# But prefer explicit ternary for clarity:
name = user_input if user_input else "Anonymous"
```

---

## 5. Bitwise Operators

Operate on the binary representation of integers.

```python
a = 0b1010   # 10
b = 0b1100   # 12

a & b    # 0b1000 = 8   AND: both bits must be 1
a | b    # 0b1110 = 14  OR:  at least one bit is 1
a ^ b    # 0b0110 = 6   XOR: exactly one bit is 1
~a       # -11          NOT: flips all bits (two's complement: ~n = -(n+1))
a << 1   # 20           left shift: multiply by 2
a >> 1   # 5            right shift: integer divide by 2
```

```
Binary:
  a = 1010
  b = 1100
  
  a & b = 1000 = 8    (AND)
  a | b = 1110 = 14   (OR)
  a ^ b = 0110 = 6    (XOR)
  ~a    = ...0101 = -11 (invert all bits)
  a<<1  = 10100 = 20  (shift left)
  a>>1  = 0101  = 5   (shift right)
```

### Real Use: Permission Flags (Bitmask Pattern)

```python
# Each permission = one bit = power of 2
READ    = 0b0001   # 1
WRITE   = 0b0010   # 2
DELETE  = 0b0100   # 4
ADMIN   = 0b1000   # 8

# Assign permissions using OR (combine bits)
user_perms  = READ | WRITE          # 0b0011 = 3
admin_perms = READ | WRITE | DELETE | ADMIN  # 0b1111 = 15

# Check a permission using AND (isolate a bit)
def has(perms, perm):
    return bool(perms & perm)

has(user_perms, READ)    # True  — bit 1 set
has(user_perms, DELETE)  # False — bit 3 not set

# Add a permission
user_perms |= DELETE         # set the DELETE bit

# Remove a permission using AND + NOT
user_perms &= ~WRITE         # clear the WRITE bit

# Toggle a permission using XOR
user_perms ^= READ           # flip the READ bit

# Check multiple permissions at once
can_write_and_delete = (user_perms & (WRITE | DELETE)) == (WRITE | DELETE)
```

### Other Bitwise Use Cases

```python
# Fast even/odd check
def is_odd(n):  return bool(n & 1)   # last bit is 1 for odd
def is_even(n): return not (n & 1)

# Fast power-of-2 check
def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0
    # Powers of 2: 8=1000, 8-1=0111, AND=0000

# Left/right shift as fast multiply/divide by powers of 2
x = 5
x << 3   # 5 * 8  = 40  (faster than * for powers of 2)
x >> 2   # 5 // 4 = 1
```

---

## 6. Identity and Membership

```python
# Identity
x is y          # True if same object (same id())
x is not y      # True if different objects

# Membership — calls __contains__
3 in [1, 2, 3]         # True
"ell" in "hello"       # True
"b" in {"a":1,"b":2}   # True (checks KEYS in dict)
3 in {1, 2, 3}         # True

5 not in [1, 2, 3]     # True
```

### `in` Performance Depends on Container

```python
# list: O(n) — scans element by element
3 in [1, 2, 3, ..., 1_000_000]   # ~1M comparisons worst case

# set: O(1) — hash lookup
3 in {1, 2, 3, ..., 1_000_000}   # ~1 lookup

# dict: O(1) — hash lookup on keys
"key" in {"key": "val", ...}      # ~1 lookup

# Production rule: if you do repeated 'in' checks → convert to set
blacklist = set(get_blacklisted_ids())   # convert once O(n)
for req in requests:
    if req.user_id in blacklist:         # O(1) each time!
        block(req)
```

---

## 7. Assignment Operators

```python
x = 10          # basic assignment

# Augmented — shorthand for x = x op y
x += 5          # x = x + 5  → calls x.__iadd__(5)  (in-place if mutable)
x -= 3          # x = x - 3
x *= 2          # x = x * 2
x /= 4          # x = x / 4   (always float)
x //= 3         # x = x // 3
x %= 7          # x = x % 7
x **= 2         # x = x ** 2
x &= 0b101      # x = x & 0b101
x |= 0b010      # x = x | 0b010
x ^= 0b111      # x = x ^ 0b111
x <<= 1         # x = x << 1
x >>= 1         # x = x >> 1
```

### `+=` on Mutable vs Immutable

```python
# MUTABLE: += calls __iadd__ — modifies in place, same object
a = [1, 2, 3]
b = a
a += [4]          # list.__iadd__ extends in place
print(id(a) == id(b))  # True — SAME object
print(b)               # [1, 2, 3, 4] — b sees the change!

# IMMUTABLE: += creates a new object
t = (1, 2, 3)
u = t
t += (4,)         # tuple immutable → new tuple created
print(id(t) == id(u))  # False — different objects
print(u)               # (1, 2, 3) — u unchanged
```

### Walrus Operator `:=` — Assign Inside Expression (Python 3.8+)

```python
# Regular = is a statement — can't use inside if/while/comprehension
# := is an expression — assigns AND returns the value

# Without walrus — call function twice
data = fetch()
if data:
    process(data)

# With walrus — assign and check in one line
if data := fetch():
    process(data)

# While loop: read until empty
while chunk := file.read(4096):
    process(chunk)

# In comprehension: capture transformed value for filtering
results = [
    processed
    for raw in data
    if (processed := transform(raw)) is not None
]
```

### Multiple Assignment

```python
# Multiple targets
a = b = c = 0       # all point to SAME object (fine for immutables)

# Tuple unpacking
x, y    = 10, 20
x, y    = y, x      # swap! Python builds tuple (y,x) then unpacks

# Extended unpacking
first, *rest = [1, 2, 3, 4, 5]
# first = 1, rest = [2, 3, 4, 5]

*start, last = [1, 2, 3, 4, 5]
# start = [1, 2, 3, 4], last = 5

first, *middle, last = [1, 2, 3, 4, 5]
# first = 1, middle = [2, 3, 4], last = 5

# Nested unpacking
(a, b), c = (1, 2), 3
print(a, b, c)    # 1 2 3

# In for loops — very common
pairs = [(1, "a"), (2, "b")]
for num, letter in pairs:
    print(num, letter)
```

---

## 8. Operator Precedence — Full Table (High to Low)

```
Priority  Operator(s)                   Notes
────────────────────────────────────────────────────────
  1       ()                            Parentheses
  2       **                            Exponentiation (RIGHT-to-left!)
  3       +x  -x  ~x                   Unary
  4       *   /   //   %               Multiplication, division, modulo
  5       +   -                        Addition, subtraction
  6       <<  >>                       Bitwise shift
  7       &                            Bitwise AND
  8       ^                            Bitwise XOR
  9       |                            Bitwise OR
  10      ==  !=  <  >  <=  >=         Comparisons
          is  is not  in  not in       Identity, membership
  11      not                          Logical NOT
  12      and                          Logical AND
  13      or                           Logical OR (LOWEST)
```

```python
# Common surprises:
2 + 3 * 4              # 14  — * before +
2 ** 3 ** 2            # 512 — ** is RIGHT-to-left: 2**(3**2) = 2**9
not 5 > 3              # False — (5>3)=True, not True = False
True or False and False # True — and before or: True or (False and False)

# When in doubt: parentheses
result = (2 + 3) * 4   # explicit is always safer
```

---

## 9. Operator Overloading — Custom Types

Since operators call dunder methods, you define them for your own classes:

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):        # v1 + v2
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):        # v1 - v2
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):       # v * 3
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):      # 3 * v  (reversed)
        return self.__mul__(scalar)

    def __eq__(self, other):         # v1 == v2
        return self.x == other.x and self.y == other.y

    def __abs__(self):               # abs(v)
        return (self.x**2 + self.y**2) ** 0.5

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)   # Vector(4, 6)
print(3 * v1)    # Vector(3, 6)  — uses __rmul__
print(abs(v2))   # 5.0
```

---

## Simple Production Example

```python
# access_control.py — bitwise permission system

READ    = 0b0001
WRITE   = 0b0010
DELETE  = 0b0100
PUBLISH = 0b1000

EDITOR    = READ | WRITE
MODERATOR = READ | WRITE | DELETE
ADMIN     = READ | WRITE | DELETE | PUBLISH

def check_access(user_role: int, required: int) -> bool:
    """Check if user_role includes all required permissions."""
    return (user_role & required) == required

def grant(role: int, perm: int) -> int:
    """Add a permission to a role."""
    return role | perm

def revoke(role: int, perm: int) -> int:
    """Remove a permission from a role."""
    return role & ~perm


# Test
role = EDITOR
print(f"Can read:    {check_access(role, READ)}")     # True
print(f"Can delete:  {check_access(role, DELETE)}")   # False

role = grant(role, DELETE)
print(f"After grant delete: {check_access(role, DELETE)}")  # True

role = revoke(role, WRITE)
print(f"After revoke write: {check_access(role, WRITE)}")   # False

try:
    if not check_access(role, PUBLISH):
        raise PermissionError("Publish requires ADMIN role")
except PermissionError as e:
    print(f"Access denied: {e}")
```

---

## Summary

```
Operators = dunder method calls
  a + b  →  a.__add__(b)  →  b.__radd__(a) if NotImplemented

/ always float | // floors toward -∞ (not zero!) | % follows divisor sign

and/or return OPERANDS:
  and → first falsy or last value (short-circuits on falsy)
  or  → first truthy or last value (short-circuits on truthy)
  not → always returns True or False

Bitwise: & AND  | OR  ^ XOR  ~ NOT  << left  >> right
  Use & to CHECK flag | | to SET | & ~flag to CLEAR | ^ to TOGGLE

is = same object? (identity) | == = same value? (equality)
in list = O(n) | in set/dict = O(1) → prefer set for repeated membership checks

:= walrus = assign + return in single expression

Precedence: () ** unary */% +- shifts & ^ | comparisons not and or
  When unsure → use parentheses
```

---

## 🎯 5 Questions

1. What does Python do when `a.__add__(b)` returns `NotImplemented`?
2. What does `and` actually return — why is `"hi" and "hello"` equal to `"hello"`?
3. Why is checking `user_id in blacklist_list` slow but `user_id in blacklist_set` fast?
4. What is the difference between `-7 // 2` and `int(-7 / 2)`?
5. Why does `a += [4]` on a list keep the same `id()` but `t += (4,)` on a tuple changes `id()`?

---

<!-- ══════════════════════════════════════════════════════ -->

# 🐍 Topic 05 — Type Casting (Type Conversion)

> *"Every form submission, API payload, CSV file, and environment variable gives you a string. Converting them correctly — and handling every way they can fail — is a daily production skill."*

---

## 1. Two Kinds of Conversion

### Implicit Conversion — Python Automatically Widens Types

Python widens to the "broader" type when combining compatible types in an operation. The rule: never lose precision.

```python
5 + 2.0      # 7.0   — int + float → float (float is wider)
True + 5     # 6     — bool + int  → int   (bool is narrower)
True + 2.5   # 3.5   — bool + float → float

# Python's numeric tower (each level is wider):
# bool → int → float → complex
```

### How It Works Under the Hood

```
5 + 2.0:
  Call (5).__add__(2.0)
    → int.__add__ sees float operand
    → returns NotImplemented
  Call (2.0).__radd__(5)
    → float.__radd__ converts 5 to 5.0
    → returns 7.0
```

### What Python Will NEVER Implicitly Convert

```python
"hello" + 5    # TypeError — string + int is ambiguous
               # should it be "hello5" or arithmetic?
               # Python refuses to guess

5 + None       # TypeError — no meaning
"3" + True     # TypeError — also ambiguous
```

---

## 2. `int()` — Every Form

```python
# From numeric types — truncates (does NOT round)
int(3.9)       # 3   ← truncates toward zero
int(3.1)       # 3
int(-3.9)      # -3  ← toward zero, not -4!
int(True)      # 1
int(False)     # 0

# From strings — strict parsing
int("42")      # 42
int("  42  ")  # 42   ← whitespace stripped automatically
int("-17")     # -17
int("+5")      # 5

# From strings with base (base must be 2–36)
int("FF", 16)     # 255  ← hex, no prefix needed when base given
int("0xFF", 16)   # 255  ← also works with prefix
int("0b1010", 2)  # 10   ← binary
int("0o17", 8)    # 15   ← octal
int("1010", 2)    # 10   ← binary without prefix
int("z", 36)      # 35   ← base 36 (0-9, a-z)

# FAILS:
int("3.14")    # ValueError — float-format string not allowed!
               # Reason: "." is not a valid digit in base 10
int("hello")   # ValueError
int("")        # ValueError — empty string
int(None)      # TypeError — None is not a string or number
int([1, 2])    # TypeError — list has no numeric meaning
int(float("inf"))  # OverflowError — infinity can't be int
```

### The Float-String Trap

```python
# Common mistake: price comes as "19.99" → want integer 19
price_str = "19.99"

int(price_str)                # ValueError! "." not valid for int()
int(float(price_str))         # 19  ← correct: float first, then truncate
round(float(price_str))       # 20  ← if you want rounding
```

---

## 3. `float()` — Every Form

```python
float(5)          # 5.0
float(True)       # 1.0
float(False)      # 0.0

float("3.14")     # 3.14
float("3")        # 3.0
float(".5")       # 0.5
float("-.7")      # -0.7
float("1e3")      # 1000.0  ← scientific notation
float("1.5e-2")   # 0.015
float("inf")      # inf
float("-inf")     # -inf
float("nan")      # nan
float("  3.14  ") # 3.14    ← whitespace stripped

# FAILS:
float("3,14")     # ValueError — comma not decimal separator!
float("hello")    # ValueError
float(None)       # TypeError
```

### The Locale Comma Trap

```python
# Input from Indian/European locale uses comma as thousand separator
user_input = "1,23,456.78"    # Indian number format

float(user_input)              # ValueError! comma breaks it

# Fix: strip commas before converting
value = float(user_input.replace(",", ""))   # 123456.78
```

---

## 4. `str()` — Every Form

```python
str(42)           # "42"
str(3.14)         # "3.14"
str(True)         # "True"
str(False)        # "False"
str(None)         # "None"   ← the STRING "None", not the None object!
str([1, 2, 3])    # "[1, 2, 3]"
str({"a": 1})     # "{'a': 1}"
str(b"bytes")     # "b'bytes'"
```

### `str()` vs `repr()` vs f-string

```python
x = "hi\nbye"

str(x)     # hi        ← interprets escape sequences, newline is actual newline
repr(x)    # 'hi\nbye' ← raw representation, shows \n literally, includes quotes
f"{x}"     # hi        ← same as str()
f"{x!r}"   # 'hi\nbye' ← same as repr()
f"{x!s}"   # hi        ← same as str() (explicit)
f"{x!a}"   # 'hi\nbye' ← ascii representation

# Rule: use repr() in logs and debugging — shows EXACTLY what the value is
# including quotes, escape chars, type hints
import logging
logging.error(f"Unexpected value: {x!r}")   # shows quotes + escapes
```

---

## 5. `bool()` — Every Form and the Traps

```python
# Falsy → False
bool(False)    # False
bool(None)     # False
bool(0)        # False
bool(0.0)      # False
bool(0j)       # False (complex zero)
bool("")       # False
bool(b"")      # False (empty bytes)
bool([])       # False
bool(())       # False
bool({})       # False
bool(set())    # False

# Truthy → True (everything else)
bool(1)        # True
bool(-1)       # True — any non-zero number
bool(0.001)    # True
bool("0")      # True ← "0" is non-empty string!
bool("False")  # True ← "False" is non-empty string!
bool([0])      # True ← list with one element
bool(" ")      # True ← space is non-empty
```

### The String Boolean Trap — Burns Everyone Once

```python
# Config value from environment variable or .env file:
debug = "False"          # came as string

if bool(debug):
    print("Debug is ON")   # THIS PRINTS! "False" is truthy!

# ❌ Wrong ways people try to fix this:
bool(int("False"))       # ValueError — "False" isn't "0" or "1"
"False" == True          # False (different types, never equal)

# ✅ Correct: compare string explicitly
debug = "False"
is_debug = debug.strip().lower() in ("true", "1", "yes", "on")
print(is_debug)   # False  ✅

# ✅ Reusable helper:
def parse_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return bool(value)
    if isinstance(value, str):
        return value.strip().lower() in ("true", "1", "yes", "on")
    return bool(value)

parse_bool("False")   # False ✅
parse_bool("true")    # True  ✅
parse_bool("1")       # True  ✅
parse_bool(True)      # True  ✅
parse_bool(0)         # False ✅
```

---

## 6. Collection Type Conversions

```python
# list() — from any iterable
list("abc")               # ['a', 'b', 'c']
list((1, 2, 3))           # [1, 2, 3]
list({1, 2, 3})           # [1, 2, 3]  (order not guaranteed from set)
list({"a": 1, "b": 2})   # ['a', 'b']  ← KEYS only!
list(range(5))            # [0, 1, 2, 3, 4]

# tuple() — from any iterable
tuple([1, 2, 3])          # (1, 2, 3)
tuple("abc")              # ('a', 'b', 'c')
tuple(range(3))           # (0, 1, 2)

# set() — removes duplicates!
set([1, 2, 2, 3, 3])      # {1, 2, 3}
set("hello")              # {'h', 'e', 'l', 'o'}  ← unique chars

# dict() — multiple forms
dict([("a", 1), ("b", 2)])    # {'a': 1, 'b': 2}
dict(zip(["a","b"], [1,2]))   # {'a': 1, 'b': 2}
dict(a=1, b=2)                # {'a': 1, 'b': 2}
dict({"a":1}, b=2)            # {'a': 1, 'b': 2}
```

---

## 7. `Decimal` — The Right Type for Money

```python
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

# ❌ float — imprecise (IEEE 754)
print(0.1 + 0.2)          # 0.30000000000000004
print(19.99 * 1.18)       # 23.588200000000002

# ✅ Decimal — exact
a = Decimal("0.1")
b = Decimal("0.2")
print(a + b)              # 0.3  ← exact!

price = Decimal("19.99")
tax   = Decimal("0.18")
total = price * (1 + tax)
print(total)              # 23.5882  exact

# Round properly (banking rules)
rounded = total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
print(rounded)            # 23.59

# ALWAYS pass as string — never as float
Decimal("19.99")    # ✅ exact
Decimal(19.99)      # ❌ Decimal('19.990000000000001136...')  inherits float error!

# Error handling
try:
    amount = Decimal(str(user_input))
except InvalidOperation:
    raise ValueError(f"Invalid amount: {user_input!r}")
```

---

## 8. Error Types — What to Catch

```python
# ValueError: right type, wrong value or format
int("hello")        # ValueError
float("not-a-num")  # ValueError
int("")             # ValueError — empty string

# TypeError: wrong type entirely
int(None)           # TypeError
int([1, 2])         # TypeError
float({"a": 1})     # TypeError

# OverflowError: value too large for target type
int(float("inf"))   # OverflowError

# AttributeError: object doesn't support conversion
class Foo: pass
int(Foo())          # TypeError (no __int__ method)
```

---

## 9. Conversion Chain Patterns

```python
# Pattern: string → float → int (for currency strings)
def parse_price_to_cents(price_str: str) -> int:
    """Convert "19.99" to 1999 (cents, avoids float entirely)."""
    return int(Decimal(price_str) * 100)

parse_price_to_cents("19.99")   # 1999

# Pattern: safe cast with fallback
def safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

safe_int("42")       # 42
safe_int("abc")      # 0
safe_int(None)       # 0
safe_int("3.14")     # 0  ← fails, returns default

# Pattern: safe cast for float-format strings
def safe_int_from_any(value, default=0):
    try:
        return int(float(str(value).replace(",", "")))
    except (ValueError, TypeError, OverflowError):
        return default

safe_int_from_any("3.14")       # 3
safe_int_from_any("1,000")      # 1000
safe_int_from_any("not-a-num")  # 0
```

---

## Simple Production Example

```python
# order_parser.py — safely parse an incoming order API payload

from decimal import Decimal, InvalidOperation

class OrderParseError(ValueError):
    def __init__(self, field, message):
        super().__init__(f"Field '{field}': {message}")
        self.field = field


def parse_order(raw: dict) -> dict:
    """
    Convert raw API payload to typed order data.
    All values from JSON may be strings or wrong types.
    """

    # quantity — must be positive integer
    try:
        quantity = int(raw.get("quantity", 0))
    except (ValueError, TypeError):
        raise OrderParseError("quantity", f"must be integer, got {raw.get('quantity')!r}")

    if quantity <= 0:
        raise OrderParseError("quantity", f"must be > 0, got {quantity}")

    # unit_price — must be positive Decimal (money!)
    try:
        unit_price = Decimal(str(raw.get("unit_price", "")))
    except InvalidOperation:
        raise OrderParseError("unit_price", f"must be valid number, got {raw.get('unit_price')!r}")

    if unit_price <= 0:
        raise OrderParseError("unit_price", f"must be > 0, got {unit_price}")

    # apply_gst — boolean from form/JSON
    raw_gst  = raw.get("apply_gst", "false")
    apply_gst = str(raw_gst).strip().lower() in ("true", "1", "yes")

    # compute total
    gst_rate = Decimal("0.18") if apply_gst else Decimal("0")
    subtotal = unit_price * quantity
    total    = subtotal * (1 + gst_rate)

    return {
        "quantity":   quantity,
        "unit_price": unit_price,
        "apply_gst":  apply_gst,
        "subtotal":   subtotal,
        "total":      total.quantize(Decimal("0.01")),
    }


# Test
try:
    order = parse_order({"quantity": "3", "unit_price": "499.99", "apply_gst": "true"})
    print(f"Total: ₹{order['total']}  (GST included)")

    parse_order({"quantity": "zero", "unit_price": "499.99"})

except OrderParseError as e:
    print(f"Parse error — {e}")
```

---

## Summary

```
IMPLICIT:
  int + float → float (numeric tower: bool→int→float→complex)
  str + int   → TypeError (Python refuses ambiguous conversions)

EXPLICIT:
  int(3.9)      → 3       (truncates toward zero, NOT rounds!)
  int("3.14")   → ValueError! use int(float("3.14"))
  float("1,234")→ ValueError! strip commas first
  str(None)     → "None"  (string, not None object)
  bool("False") → True    (non-empty string is truthy!)
  bool("0")     → True    (still non-empty!)

DECIMAL for money:
  Always Decimal("19.99") not Decimal(19.99)
  (float imprecision baked in before Decimal sees it)

ERRORS:
  ValueError   → right type, wrong format
  TypeError    → wrong type entirely
  OverflowError→ too large (int(float("inf")))
  InvalidOperation → Decimal parse failure
```

---

## 🎯 5 Questions

1. Why does Python implicitly convert `int + float` to float but refuse `str + int`?
2. Why does `int("3.14")` fail but `int(3.14)` gives `3`?
3. Why is `bool("False")` equal to `True` and how do you correctly parse boolean strings?
4. Why must you pass `Decimal("19.99")` as a string, not `Decimal(19.99)`?
5. What are the three exception types to catch when casting user input?

---

<!-- ══════════════════════════════════════════════════════ -->

# 🐍 Topic 06 — Conditional Statements

> *"`if` compiles to a jump instruction. The CPU doesn't understand 'conditions' — it understands 'jump to address X if this value is zero.' Every branching decision your program makes becomes a jump instruction at the bytecode level."*

---

## 1. How `if` Works — Bytecode Level

```python
import dis
def example(x):
    if x > 5:
        print("big")

dis.dis(example)
```

```
LOAD_FAST        x
LOAD_CONST       5
COMPARE_OP       >           ← evaluates to True or False object
POP_JUMP_IF_FALSE  → end     ← if False: jump past the block
LOAD_GLOBAL      print
LOAD_CONST       'big'
CALL_FUNCTION    1
end:  (resumes here)
```

The `if` keyword itself doesn't exist in bytecode. It becomes `COMPARE_OP` + `POP_JUMP_IF_FALSE`. The CPU executes a conditional branch instruction. Same mechanism in every language under the hood.

**SyntaxErrors** (missing colon, bad indentation) are caught at the Parser stage — before any bytecode is even generated, before any line of your code runs.

---

## 2. `if` / `elif` / `else` — All Forms

### Basic Structure

```python
if condition:
    body          # runs if condition is truthy
elif condition2:
    body          # runs if condition1 falsy AND condition2 truthy
elif condition3:
    body          # further elif — unlimited
else:
    body          # runs if ALL conditions were falsy
```

### Execution Order — Python Stops at First Truthy

```python
def http_status(code):
    if code < 200:        # checked first
        return "informational"
    elif code < 300:      # only checked if < 200 was False
        return "success"
    elif code < 400:      # only checked if < 300 was False
        return "redirection"
    elif code < 500:
        return "client error"
    else:                 # no condition evaluated — runs if all above False
        return "server error"
```

**Performance tip:** Put the most common case first. Once a truthy branch is found, remaining conditions are not evaluated at all.

### `if` Without `else`

```python
# Perfectly valid — else is optional
if DEBUG:
    log("debug message")
# if DEBUG is False, nothing happens and execution continues
```

### Nested `if`

```python
# Legal but creates "arrow code" — hard to read
def process(user, order):
    if user:
        if user.is_active:
            if order:
                if order.items:
                    return ship(order)
```

---

## 3. Guard Clauses — Flat Over Nested

The professional pattern: handle failure cases first, then the happy path is flat and unindented.

```python
# ❌ Nested — reader must track 4 levels to find the actual logic
def process(user, order):
    if user:
        if user.is_active:
            if order:
                if order.items:
                    return ship(order)
    return None

# ✅ Guard clauses — fail fast, happy path at left edge
def process(user, order):
    if not user:            return None
    if not user.is_active:  return None
    if not order:           return None
    if not order.items:     return None
    return ship(order)       # happy path — no nesting
```

Each guard handles exactly one failure condition and exits. The success logic lives at the lowest indentation level — easy to see and reason about.

---

## 4. Truthiness in Conditions

Python calls `bool(x)` on any condition, which calls `x.__bool__()`.

```python
# Everything evaluates as truthy or falsy
# FALSY: False, None, 0, 0.0, "", b"", [], {}, set(), ()
# TRUTHY: everything else

# Idiomatic — use truthiness directly
if users:           # same as: if len(users) > 0
if not errors:      # same as: if len(errors) == 0
if response:        # same as: if response is not None
if data:            # same as: if data is not None and data != ""

# CAREFUL — 0 and "" are falsy
count = 0
if count:           # WRONG — won't enter! 0 is falsy
    process(count)

# When 0 / "" / [] are valid values, check explicitly
if count is not None:       # only checks for None — 0 passes through
    process(count)

if name != "":              # only rejects empty string — 0 and None pass
    process(name)
```

---

## 5. Short-Circuit Evaluation in Conditions

```python
# 'and' stops at FIRST FALSY value — right side not evaluated
user = None
if user and user.is_active:   # user is None (falsy) → stops
    grant_access()            # user.is_active NEVER evaluated → no AttributeError

# 'or' stops at FIRST TRUTHY value — right side not evaluated
cache_result = cache.get(key)
value = cache_result or expensive_db_query(key)  # DB only hit if cache miss

# Conditional execution using short-circuit
DEBUG and log(request_data)   # log only if DEBUG truthy
```

---

## 6. Ternary Operator — Conditional Expression

```python
# Syntax: value_if_true  if  condition  else  value_if_false
label  = "admin"  if user.is_admin  else "user"
result = x        if x > y          else y         # same as max(x, y)
status = "active" if user.active    else "inactive"
value  = data     if data is not None else {}
```

### All Contexts Where Ternary Is Useful

```python
# In assignment
discount = 0.20 if is_member else 0.05

# In f-strings
print(f"Role: {'admin' if user.is_admin else 'user'}")

# In function arguments
log(message, level="ERROR" if critical else "WARNING")

# In return
def absolute(x):
    return x if x >= 0 else -x

# In list comprehensions
result = ["even" if x % 2 == 0 else "odd" for x in range(5)]

# In dict comprehension
d = {k: v * 2 if v > 10 else v for k, v in data.items()}
```

### Nested Ternary — Use Sparingly

```python
# Two levels — acceptable
grade = "pass" if score >= 50 else "fail"

# Three levels — getting hard to read
grade = "A" if score >= 90 else ("B" if score >= 80 else "C")

# Four+ levels — use if/elif instead
grade = "A" if s>=90 else "B" if s>=80 else "C" if s>=70 else "F"
# Hard to follow — replace with if/elif chain
```

---

## 7. One-Liner `if` (Inline)

```python
# Legal: single statement on same line as if
if not user: return None
if error: raise ValueError(error)
if cache_hit: return cache_result

# Legal: multiple statements on one line (avoid — hard to debug)
if x > 0: y = x; print(y)   # works but don't do this

# One-liner if/else requires ternary (not possible with inline syntax)
```

---

## 8. `pass` in Conditionals

```python
# Placeholder while developing
if user.is_admin:
    pass   # TODO: admin logic

# Explicit do-nothing
if event.type == "ping":
    pass   # heartbeat — no action needed
else:
    handle_event(event)

# Silencing errors (use only when intentional, always comment why)
try:
    cleanup_temp_files()
except PermissionError:
    pass   # temp files may be locked — ok to leave them
```

---

## 9. `match` / `case` — Structural Pattern Matching (Python 3.10+)

Not just a switch statement. Matches structure, type, value, and binds variables simultaneously.

### How `match` Works Internally

```
match subject:
  case pattern:
    1. Does subject's STRUCTURE match pattern?
    2. Bind any named variables in pattern
    3. If guard (if ...) → evaluate it too
    4. All match → run block, exit match
    5. No → try next case

case _ → wildcard, matches anything, binds nothing
No match found → nothing happens (no error, unlike C switch)
```

### Matching Literals and OR Patterns

```python
def day_type(day: str) -> str:
    match day.lower():
        case "monday" | "tuesday" | "wednesday" | "thursday" | "friday":
            return "weekday"
        case "saturday" | "sunday":
            return "weekend"
        case _:
            return "unknown"
```

### Matching Sequences

```python
def parse_command(tokens: list) -> str:
    match tokens:
        case []:
            return "empty command"

        case ["quit"]:
            return "quitting"

        case ["go", direction]:        # captures 'direction' variable
            return f"going {direction}"

        case ["go", direction, speed]:
            return f"going {direction} at {speed}"

        case ["move", *steps]:         # *steps captures remaining items
            return f"moving via {len(steps)} steps"

        case [cmd, *args]:             # catch-all with args
            return f"unknown command {cmd} with {len(args)} args"
```

### Matching Mappings (Dicts) — Partial Match

```python
# Dict matching is PARTIAL — extra keys are ignored
def handle_api_event(event: dict):
    match event:
        case {"type": "user_signup", "email": email}:
            send_welcome_email(email)

        case {"type": "purchase", "amount": amount, "user_id": uid}:
            record_sale(uid, amount)

        case {"type": "error", "code": code} if code >= 500:
            alert_oncall(code)

        case {"type": "error", "code": code}:
            log_client_error(code)

        case {"type": str(unknown)}:
            print(f"Unknown event type: {unknown}")
```

### Matching Classes (Dataclasses)

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

def describe(shape):
    match shape:
        case Point(x=0, y=0):
            return "origin"

        case Point(x=x, y=0):
            return f"on x-axis at {x}"

        case Point(x=0, y=y):
            return f"on y-axis at {y}"

        case Point(x=x, y=y):
            return f"point at ({x}, {y})"
```

### Guards — `if` Inside `case`

```python
def classify_score(result: dict):
    match result:
        case {"score": score, "subject": subject} if score >= 90:
            return f"Distinction in {subject}"

        case {"score": score, "subject": subject} if score >= 60:
            return f"Pass in {subject}"

        case {"score": score, "subject": subject}:
            return f"Fail in {subject} (score: {score})"

        case _:
            return "Invalid result format"
```

### Capturing with `as`

```python
match value:
    case ({"status": 400} | {"status": 422}) as err:
        # matches either status, captures entire dict as 'err'
        log_client_error(err)

    case {"status": code} as response if code >= 500:
        # matches dict with status, captures whole dict as 'response'
        alert_team(response)
```

---

## Simple Production Example

```python
# auth_handler.py — all conditional patterns in one realistic example

def authenticate(request: dict, db) -> dict:
    """
    Authenticate a request. Returns user data or raises appropriate error.
    Demonstrates: guard clauses, truthiness, match/case, ternary.
    """

    # Guard clauses — fail fast
    if not isinstance(request, dict):
        raise TypeError("request must be a dict")

    username = request.get("username", "").strip()
    password = request.get("password", "")
    auth_type = request.get("auth_type", "password")

    if not username:
        raise ValueError("username is required")

    if not password:
        raise ValueError("password is required")

    # Match on auth_type — structural pattern matching
    match auth_type:
        case "password":
            user = db.find_by_username(username)
            if user is None:
                raise LookupError(f"User '{username}' not found")
            if not user.check_password(password):
                raise PermissionError("Invalid credentials")

        case "token":
            user = db.find_by_token(password)   # 'password' field holds token
            if user is None:
                raise PermissionError("Invalid or expired token")

        case "api_key":
            user = db.find_by_api_key(password)
            if user is None:
                raise PermissionError("Invalid API key")

        case _:
            raise ValueError(f"Unknown auth_type: {auth_type!r}")

    # Ternary for role label
    role = "admin" if user.is_admin else "member"

    return {
        "user_id":   user.id,
        "username":  user.username,
        "role":      role,
        "is_active": user.is_active,
    }


# In the API layer:
try:
    user_data = authenticate(request, db)
    print(f"Authenticated: {user_data['username']} ({user_data['role']})")

except (ValueError, TypeError) as e:
    print(f"400 Bad Request: {e}")
except LookupError as e:
    print(f"404 Not Found: {e}")
except PermissionError as e:
    print(f"403 Forbidden: {e}")
```

---

## Summary

```
if/elif/else → compiles to COMPARE_OP + POP_JUMP_IF_FALSE bytecode
  Python stops at first truthy branch — remaining conditions not evaluated
  Put most likely case first for performance

Guard clauses > deep nesting — handle failures early, keep happy path flat

Truthiness: if x: catches None, 0, "", [], {} all at once
  if x is not None: catches ONLY None (use when 0/"" are valid values)

Short-circuit: user and user.email — safe attribute access without AttributeError

Ternary: value_if_true if condition else value_if_false
  Good for 2-way, use if/elif for 3+ branches

One-liner if: only for simple guard clauses (return/raise)

match/case (Python 3.10+):
  Matches structure (dicts, lists, classes) not just values
  | for OR patterns
  case pattern if guard: — structure match AND guard condition
  case *rest: — capture remaining sequence items
  case _ — wildcard default
  Dict matching is PARTIAL — extra keys ignored
```

---

## 🎯 5 Questions

1. What bytecode instruction does `if` compile to?
2. Why does `if count:` fail when `count = 0`, and how do you fix it?
3. What is the difference between `if user and user.email` and `if user.email`?
4. What makes `match/case` more powerful than a regular `if/elif` chain?
5. When should ternary NOT be used, and what should replace it?

---

<!-- ══════════════════════════════════════════════════════ -->

# 🐍 Topic 07 — Loops

> *"Every `for` loop in Python is a conversation between an iterator and a consumer. The loop calls `__next__()` repeatedly until `StopIteration` is raised. Once you understand the iterator protocol, generators, comprehensions, and lazy evaluation all follow naturally."*

---

## 1. The Iterator Protocol — Engine of All Loops

Two dunder methods power every `for` loop:

```python
__iter__()   → called once; returns an iterator object
__next__()   → called each iteration; returns next value OR raises StopIteration
```

```python
# What Python does when you write:
for item in [1, 2, 3]:
    print(item)

# Is EXACTLY this:
_iter = iter([1, 2, 3])       # calls list.__iter__() → returns list_iterator
while True:
    try:
        item = next(_iter)    # calls list_iterator.__next__()
        print(item)
    except StopIteration:
        break                 # loop ends
```

This protocol is why `for` works on lists, strings, dicts, files, generators, range objects, database cursors — anything implementing these two methods.

```python
# Prove it — manually iterate
lst  = [10, 20, 30]
it   = iter(lst)         # list_iterator object
print(next(it))          # 10
print(next(it))          # 20
print(next(it))          # 30
print(next(it))          # raises StopIteration
```

---

## 2. `while` Loop — All Forms

```python
# Basic: condition checked before each iteration
n = 5
while n > 0:
    print(n)
    n -= 1          # without this: infinite loop!

# While True — run until explicit break
while True:
    data = fetch()
    if data is None:
        break
    process(data)

# While with else
# else block runs ONLY if loop exited normally (no break)
attempts = 0
while attempts < 3:
    if try_connect():
        break
    attempts += 1
else:
    raise RuntimeError("Failed to connect after 3 attempts")

# Walrus operator in while (Python 3.8+)
while chunk := file.read(4096):   # assigns chunk AND checks truthiness
    process(chunk)
# reads until file.read() returns b'' (falsy)
```

### Simulated `do-while` — Always Run at Least Once

```python
# Python has no do-while keyword — simulate with while True + break at end
while True:
    user_input = input("Enter a positive number: ").strip()
    if user_input.isdigit() and int(user_input) > 0:
        break
    print("Invalid input. Try again.")

# Alternative: init variable to trigger first iteration
value = None
while value is None or not is_valid(value):
    value = get_input()
```

---

## 3. `for` Loop — All Forms

### Basic Iteration

```python
# Over list
for item in [1, 2, 3]:
    print(item)

# Over string — each character
for char in "Python":
    print(char)    # P, y, t, h, o, n

# Over tuple
for x, y in [(1, 2), (3, 4), (5, 6)]:   # unpacking in loop
    print(x + y)

# Over set (order not guaranteed)
for item in {1, 2, 3}:
    print(item)
```

### Over Dictionaries — All Ways

```python
config = {"host": "localhost", "port": 8000, "debug": True}

# Iterate KEYS (default)
for key in config:
    print(key)

# Iterate VALUES
for value in config.values():
    print(value)

# Iterate KEY-VALUE PAIRS (most common)
for key, value in config.items():
    print(f"{key}: {value}")

# Iterate KEYS explicitly
for key in config.keys():
    print(key)

# With index
for i, (key, value) in enumerate(config.items()):
    print(f"{i}: {key} = {value}")

# Modify dict while iterating — DON'T
# for key in config:
#     config[key] = str(config[key])  # RuntimeError: dict changed size

# Safe: iterate a copy
for key in list(config.keys()):
    config[key] = str(config[key])   # ok — iterating over a list copy
```

### Over File Lines

```python
# File object implements __iter__ / __next__ — yields one line at a time
with open("data.txt") as f:
    for line in f:             # reads one line at a time — O(1) memory!
        process(line.strip())

# vs readlines() — loads ALL lines into memory at once
with open("data.txt") as f:
    for line in f.readlines():  # full file in RAM — bad for large files
        process(line.strip())
```

---

## 4. `range()` — Lazy Numeric Iterator

```python
range(stop)              # 0 to stop-1
range(start, stop)       # start to stop-1
range(start, stop, step) # with step

range(5)          # 0, 1, 2, 3, 4
range(2, 8)       # 2, 3, 4, 5, 6, 7
range(0, 20, 5)   # 0, 5, 10, 15
range(10, 0, -1)  # 10, 9, 8, ..., 1
range(0, 10, 2)   # 0, 2, 4, 6, 8  (even numbers)
range(9, -1, -1)  # 9, 8, 7, ..., 0
```

### Why `range()` Is Memory Efficient

```python
import sys
print(sys.getsizeof(range(1_000_000)))         # 48 bytes!
print(sys.getsizeof(list(range(1_000_000))))   # ~8 MB

# range stores only: start, stop, step (3 integers = 48 bytes)
# Generates each value on demand when next() is called
# list(range(...)) creates all values at once in memory

# range supports random access (unlike generators)
r = range(0, 100, 2)
print(r[10])      # 20  — O(1) calculation: start + 10 * step
print(50 in r)    # True — O(1) math: no scanning needed!
print(len(r))     # 50
```

---

## 5. `enumerate()` — Index + Value

```python
fruits = ["apple", "banana", "cherry"]

# ❌ Anti-pattern — never do this
for i in range(len(fruits)):
    print(i, fruits[i])

# ✅ Correct — use enumerate
for i, fruit in enumerate(fruits):
    print(i, fruit)

# Start from a different index
for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")
# 1. apple
# 2. banana
# 3. cherry

# Under the hood — enumerate creates (index, value) tuples lazily
e = enumerate(["a", "b", "c"])
print(next(e))   # (0, 'a')
print(next(e))   # (1, 'b')
```

Why not `range(len(...))`?
- `range(len(x))` requires `len()` — doesn't work on generators or iterators without length
- `enumerate()` works on any iterable, lazy, doesn't need to know the length upfront

---

## 6. `zip()` — Parallel Iteration

```python
names  = ["Alice", "Bob", "Charlie"]
scores = [95, 87, 92]
grades = ["A", "B", "A"]

# Iterate all in parallel
for name, score, grade in zip(names, scores, grades):
    print(f"{name}: {score} ({grade})")

# zip stops at the SHORTEST iterable
a = [1, 2, 3, 4, 5]
b = ["a", "b", "c"]
list(zip(a, b))   # [(1,'a'), (2,'b'), (3,'c')]  — stops at 3

# zip_longest — pad shorter iterables
from itertools import zip_longest
list(zip_longest(a, b, fillvalue="?"))
# [(1,'a'), (2,'b'), (3,'c'), (4,'?'), (5,'?')]

# Build dict from two lists — very common
keys   = ["name", "age", "city"]
values = ["Arjun", 22, "Ahmedabad"]
data   = dict(zip(keys, values))
# {"name": "Arjun", "age": 22, "city": "Ahmedabad"}

# Unzip — transpose a list of tuples
pairs   = [(1, "a"), (2, "b"), (3, "c")]
numbers, letters = zip(*pairs)   # * unpacks the list into arguments
print(numbers)   # (1, 2, 3)
print(letters)   # ('a', 'b', 'c')

# zip with enumerate — both at once
for i, (name, score) in enumerate(zip(names, scores), start=1):
    print(f"#{i}: {name} scored {score}")
```

---

## 7. Loop Control — `break`, `continue`, `else`

```python
# break — exit the entire loop immediately
for i in range(10):
    if i == 5:
        break       # exits for loop at i=5
    print(i)        # prints 0,1,2,3,4

# continue — skip rest of current iteration, go to next
for i in range(10):
    if i % 2 == 0:
        continue    # skip even numbers
    print(i)        # prints 1,3,5,7,9

# break and continue in while
i = 0
while True:
    i += 1
    if i % 3 == 0:
        continue
    if i > 10:
        break
    print(i)
```

### `else` on Loops — The Misunderstood Feature

```python
# else on for: runs ONLY if loop completed WITHOUT hitting break
# else on while: runs ONLY if condition became False (didn't break)

# Perfect for "search and not found" pattern:
users = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
target_id = 3

for user in users:
    if user["id"] == target_id:
        print(f"Found: {user['name']}")
        break
else:
    print(f"User {target_id} not found")   # runs because no break hit
# Output: User 3 not found

# Retry with else:
import time
for attempt in range(3):
    try:
        result = connect()
        break              # success — skip else
    except ConnectionError:
        time.sleep(2 ** attempt)
else:
    raise RuntimeError("All 3 attempts failed")
```

---

## 8. Nested Loops and Breaking Out

```python
# break only exits the INNERMOST loop
for i in range(3):
    for j in range(3):
        if i == j == 1:
            break       # only breaks inner loop!
    print(i, "outer continues")

# ✅ Option 1: use a function (cleanest)
def find_cell(matrix, target):
    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            if val == target:
                return (i, j)   # return exits entire function
    return None

# ✅ Option 2: flag variable
found = False
for i in range(5):
    for j in range(5):
        if condition(i, j):
            found = True
            break
    if found:
        break

# ✅ Option 3: itertools.product (flattens nested loop)
from itertools import product
for i, j in product(range(5), range(5)):
    if condition(i, j):
        break
```

---

## 9. Comprehensions — Compact, Optimized Loop Expressions

### List Comprehension

```python
# [expression  for  item  in  iterable  if  condition]
squares = [x**2 for x in range(10)]
evens   = [x for x in range(20) if x % 2 == 0]
words   = [w.strip().title() for w in raw_input.split(",")]

# With transformation + filter
valid_emails = [
    email.lower()
    for email in raw_emails
    if "@" in email and "." in email.split("@")[1]
]

# Nested loops in comprehension
matrix = [[1,2,3],[4,5,6],[7,8,9]]
flat   = [val for row in matrix for val in row]
# [1, 2, 3, 4, 5, 6, 7, 8, 9]
# Note: outer loop first, inner loop second (same order as nested for)

# Ternary inside comprehension
results = ["even" if x % 2 == 0 else "odd" for x in range(5)]
```

### Why Comprehensions Are Faster Than Loops

```python
# Loop approach
result = []
for x in range(1000):
    result.append(x**2)

# Comprehension approach
result = [x**2 for x in range(1000)]

# Why faster:
# Loop: each iteration runs LOAD_ATTR to look up 'append' on the list object
# Comprehension: uses LIST_APPEND bytecode — dedicated instruction, no lookup
# Comprehension is ~20-30% faster for the same work
```

### Dict Comprehension

```python
# {key_expr: val_expr for item in iterable if condition}
original = {"a": 1, "b": 2, "c": 3}

# Invert a dict
inverted = {v: k for k, v in original.items()}
# {1: 'a', 2: 'b', 3: 'c'}

# Filter a dict — keep only certain keys
config   = {"host": "localhost", "port": 8000, "secret": "abc123"}
safe     = {k: v for k, v in config.items() if k != "secret"}

# Transform values
squared  = {k: v**2 for k, v in original.items()}

# Build lookup table from list
users = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
by_id = {u["id"]: u for u in users}   # {1: {...}, 2: {...}}
print(by_id[1])   # {"id": 1, "name": "Alice"}

# Normalize keys
raw  = {"Name": "Arjun", "AGE": 22}
norm = {k.lower(): v for k, v in raw.items()}
# {"name": "Arjun", "age": 22}
```

### Set Comprehension

```python
# Unique values automatically
unique_squares = {x**2 for x in [-3, -2, -1, 0, 1, 2, 3]}
# {0, 1, 4, 9}  — duplicates removed

# Extract unique domains from emails
emails  = ["a@gmail.com", "b@yahoo.com", "c@gmail.com"]
domains = {e.split("@")[1] for e in emails}
# {'gmail.com', 'yahoo.com'}
```

### Generator Expression — Lazy Comprehension

```python
# List comprehension — computes ALL values immediately, stores in memory
squares_list = [x**2 for x in range(1_000_000)]   # ~8 MB in RAM

# Generator expression — computes ONE value at a time, O(1) memory
squares_gen  = (x**2 for x in range(1_000_000))   # ~120 bytes!

# Use when:
# - You only need to iterate once (no random access)
# - The result is consumed by another function (sum, max, any, all, etc.)
total = sum(x**2 for x in range(1_000_000))    # pass generator to sum()
found = any(x > 999 for x in data)             # stops at first match
valid = all(x > 0 for x in numbers)            # stops at first False

# Generator is exhausted after one iteration!
gen = (x**2 for x in range(5))
list(gen)   # [0, 1, 4, 9, 16]
list(gen)   # []  ← exhausted! can't iterate again
```

---

## 10. Generators — Custom Lazy Iterators with `yield`

### How `yield` Works — Frame Suspension

```python
def count_up(n):
    i = 0
    while i < n:
        yield i      # PAUSE here, return i, remember ALL local state
        i += 1       # resumes HERE on next next() call

g = count_up(3)
print(next(g))   # 0  — ran until yield, returned 0
print(next(g))   # 1  — resumed from yield, i became 1, yielded 1
print(next(g))   # 2
print(next(g))   # StopIteration — while condition False, function returned
```

```
Normal function:    return → frame POPPED, locals gone
Generator function: yield  → frame SUSPENDED (locals preserved in memory)
                    next() → frame RESUMED from exact yield line
                    StopIteration → when function returns naturally
```

```python
# See the suspended frame:
g = count_up(5)
next(g)
print(g.gi_frame.f_locals)   # {'i': 1, 'n': 5}  — locals preserved!
```

### Generator vs List — Memory

```python
import sys

def read_file_lines(path):
    with open(path) as f:
        for line in f:
            yield line.strip()   # one line at a time

# vs:
def read_all_lines(path):
    with open(path) as f:
        return f.readlines()     # ALL lines in RAM at once

# For a 1GB log file:
# read_file_lines: ~120 bytes memory usage (one line at a time)
# read_all_lines:  ~1 GB memory usage
```

### Generator Patterns

```python
# Infinite generator
def integers_from(start=0):
    n = start
    while True:
        yield n
        n += 1

from itertools import islice
first_10 = list(islice(integers_from(5), 10))
# [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

# Pipeline of generators — each stage is lazy
def read_records(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.strip()

def parse_json(lines):
    import json
    for line in lines:
        try:
            yield json.loads(line)
        except json.JSONDecodeError:
            pass   # skip invalid lines

def filter_active(records):
    for r in records:
        if r.get("active"):
            yield r

# Connect the pipeline — nothing runs yet
pipeline = filter_active(parse_json(read_records("data.jsonl")))

# Consume — now it runs lazily
for record in pipeline:
    process(record)
# File is read one line at a time, parsed, filtered — all in O(1) memory
```

### `yield from` — Delegating to Sub-Generator

```python
def chain(*iterables):
    for it in iterables:
        yield from it    # delegates to each iterable

list(chain([1,2], [3,4], [5]))   # [1, 2, 3, 4, 5]

# yield from also forwards values and exceptions to sub-generator
def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)   # recurse into nested list
        else:
            yield item

list(flatten([1, [2, [3, 4]], 5]))   # [1, 2, 3, 4, 5]
```

---

## 11. `itertools` — Essential Loop Tools

```python
from itertools import (
    chain, product, combinations, permutations,
    groupby, islice, takewhile, dropwhile,
    cycle, repeat, count, accumulate
)

# chain — iterate multiple iterables as one
list(chain([1,2], [3,4], [5]))          # [1, 2, 3, 4, 5]

# product — cartesian product (nested loops flattened)
list(product([1,2], ["a","b"]))         # [(1,'a'),(1,'b'),(2,'a'),(2,'b')]

# combinations — nCr, no repetition
list(combinations([1,2,3], 2))          # [(1,2),(1,3),(2,3)]

# permutations — nPr
list(permutations([1,2,3], 2))          # [(1,2),(1,3),(2,1),(2,3),(3,1),(3,2)]

# islice — slice any iterator
list(islice(range(100), 5))             # [0, 1, 2, 3, 4]
list(islice(range(100), 10, 20))        # [10, 11, ..., 19]

# takewhile — take items while condition is true
list(takewhile(lambda x: x < 5, [1,3,6,2,8]))   # [1, 3]  stops at 6

# dropwhile — drop items while condition is true, then yield rest
list(dropwhile(lambda x: x < 5, [1,3,6,2,8]))   # [6, 2, 8]

# cycle — infinite cycle through iterable
import itertools
gen = itertools.cycle(["A","B","C"])
[next(gen) for _ in range(7)]           # ['A','B','C','A','B','C','A']

# accumulate — running totals
list(accumulate([1,2,3,4,5]))           # [1, 3, 6, 10, 15]
list(accumulate([1,2,3,4,5], max))      # [1, 2, 3, 4, 5]  running max

# groupby — group CONSECUTIVE elements by key (sort first!)
data = sorted([("MH", 100), ("GJ", 200), ("MH", 300)], key=lambda x: x[0])
for state, group in groupby(data, key=lambda x: x[0]):
    total = sum(amt for _, amt in group)
    print(f"{state}: {total}")
# GJ: 200
# MH: 400
```

---

## 12. `reduce()` — Fold a Sequence to One Value

```python
from functools import reduce

# reduce(function, iterable, initial_value)
# function takes (accumulator, current_item) → returns new accumulator

nums = [1, 2, 3, 4, 5]
total   = reduce(lambda acc, x: acc + x, nums, 0)      # 15
product = reduce(lambda acc, x: acc * x, nums, 1)       # 120
maximum = reduce(lambda a, b: a if a > b else b, nums)  # 5

# Real example: sum account balances by state (one pass)
records = [
    {"state": "MH", "balance": 50000},
    {"state": "GJ", "balance": 30000},
    {"state": "MH", "balance": 20000},
]

# reduce does one pass, building state_totals dict as accumulator
def accumulate_state(acc, r):
    state = r["state"]
    acc[state] = acc.get(state, 0) + r["balance"]
    return acc

state_totals = reduce(accumulate_state, records, {})
print(state_totals)   # {"MH": 70000, "GJ": 30000}
```

### Why `reduce` vs `sum()` + filter

```python
# sum() + filter — two passes
mh_records = [r for r in records if r["state"] == "MH"]  # pass 1: list created
total = sum(r["balance"] for r in mh_records)              # pass 2: sum

# sum() + generator — one pass, same efficiency for simple sums
total = sum(r["balance"] for r in records if r["state"] == "MH")

# reduce — shines when building complex result in ONE pass
# (filter + group + aggregate simultaneously):
state_totals = reduce(accumulate_state, records, {})
# One pass, no intermediate list, handles any accumulation logic
```

---

## Simple Production Example

```python
# transaction_report.py — lazy pipeline for large transaction files

import json
from functools import reduce
from itertools import groupby

def read_transactions(filepath: str):
    """Generator: one transaction dict at a time."""
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue   # skip malformed lines

def filter_by_date(records, date: str):
    """Generator: filter by date prefix."""
    for r in records:
        if r.get("date", "").startswith(date):
            yield r

def build_state_report(records) -> dict:
    """Reduce: build state totals in one pass."""
    def accumulate(acc, r):
        state = r.get("state", "UNKNOWN")
        acc[state] = acc.get(state, 0) + r.get("amount", 0)
        return acc
    return reduce(accumulate, records, {})


try:
    # Lazy pipeline — O(1) memory regardless of file size
    all_txns    = read_transactions("transactions.jsonl")
    march_txns  = filter_by_date(all_txns, "2024-03")
    report      = build_state_report(march_txns)

    # Sort and display
    for state, total in sorted(report.items(), key=lambda x: -x[1]):
        print(f"  {state}: ₹{total:>10,.2f}")

except FileNotFoundError as e:
    print(f"Data file not found: {e}")
```

---

## Summary

```
for = iter(obj).__iter__() + repeated __next__() + StopIteration to stop

while: condition before each iteration | while True + break = do-while
for: over any iterable
range(): lazy 48 bytes, supports indexing + 'in' check in O(1)
enumerate(): index + value — never use range(len(x))
zip(): parallel, stops at shortest, zip_longest for equal length

break:    exit loop immediately
continue: skip to next iteration
else:     runs ONLY if no break occurred (great for "not found" logic)

Comprehensions:
  [x for x in y if z]     → list (eager)
  {k:v for ...}            → dict
  {x for x in y}           → set
  (x for x in y)           → generator (lazy, O(1) memory)
  Faster than loops: LIST_APPEND bytecode vs LOAD_ATTR + append call

Generators:
  yield: suspends frame, preserves locals, resumes on next()
  yield from: delegates to sub-generator
  One-time use — exhausted after iteration

reduce:
  sum(gen) for simple totals
  reduce() for complex one-pass accumulation (group + sum, build dict, etc.)
```

---

## 🎯 5 Questions

1. What two dunder methods does every `for` loop call?
2. Why is `range(1_000_000)` only 48 bytes but `list(range(1_000_000))` is ~8MB?
3. When does the `else` block on a loop run?
4. What happens to generator local variables when `yield` is hit?
5. When is `reduce()` better than `sum()` with a generator?

---

<!-- ══════════════════════════════════════════════════════ -->

# 🐍 Topic 08 — Exception Handling

> *"An exception is an object. Raising one starts stack unwinding — Python walks up call frames looking for a matching handler. If none found, the program crashes with a traceback. Once you see exception as object + unwinding, everything about try/except/raise clicks."*

---

## 1. What Happens When an Exception Is Raised

```python
def c(): raise ValueError("bad value")
def b(): c()
def a(): b()
a()
```

```
Execution reaches c() → ValueError object created → raise begins stack unwinding:

  Frame c():  raise → no except here → unwind up
  Frame b():  no except here → unwind up
  Frame a():  no except here → unwind up
  Module:     no except here → CRASH + print traceback

Traceback (most recent call last):  ← reads bottom-up (deepest first)
  File "...", line X, in a
    b()
  File "...", line X, in b
    c()
  File "...", line X, in c
    raise ValueError("bad value")
ValueError: bad value
```

**Key points:**
- Exception is an **object** — instance of a class inheriting from `BaseException`
- Python **unwinds** the call stack frame by frame looking for a matching `except`
- First matching `except` (using `isinstance()`) wins
- If none found → program crashes
- Traceback reads bottom-up: most recent call is last

---

## 2. Exception Hierarchy

```
BaseException
├── SystemExit              ← sys.exit() — DO NOT catch without re-raising
├── KeyboardInterrupt       ← Ctrl+C — same
├── GeneratorExit           ← when generator.close() called
└── Exception               ← base for all "normal" exceptions to catch
    ├── ArithmeticError
    │   ├── ZeroDivisionError
    │   ├── OverflowError
    │   └── FloatingPointError
    ├── AttributeError       ← obj.missing
    ├── ImportError
    │   └── ModuleNotFoundError
    ├── LookupError
    │   ├── IndexError       ← list[999]
    │   └── KeyError         ← dict["missing"]
    ├── NameError
    │   └── UnboundLocalError
    ├── OSError (IOError)
    │   ├── FileNotFoundError
    │   ├── PermissionError
    │   ├── FileExistsError
    │   └── TimeoutError
    ├── RuntimeError
    │   └── RecursionError
    ├── StopIteration
    ├── TypeError
    ├── ValueError
    │   └── UnicodeError
    │       └── UnicodeDecodeError
    └── Warning
```

**Inheritance matters for catching:**
```python
# isinstance() is used — parent catches all children
except Exception:         # catches ALL exceptions (too broad)
except LookupError:       # catches IndexError AND KeyError
except OSError:           # catches FileNotFoundError, PermissionError, etc.
except ValueError:        # only ValueError (and subclasses)
```

**Rules:**
- Never catch `BaseException`, `SystemExit`, `KeyboardInterrupt` without re-raising
- Catch the **most specific** type possible
- Order `except` clauses specific → general

---

## 3. `try` / `except` — All Forms

### Single Exception

```python
try:
    result = int(user_input)
except ValueError:
    print("Not a valid number")
```

### Capture the Exception Object with `as`

```python
try:
    result = int(user_input)
except ValueError as e:
    print(f"Error: {e}")           # invalid literal for int()...
    print(f"Type: {type(e)}")      # <class 'ValueError'>
    print(f"Args: {e.args}")       # ('invalid literal...',)

    import traceback
    traceback.print_exc()          # full stack trace to stderr
    tb = traceback.format_exc()    # full trace as string (for logging)
```

### Multiple Exception Types — One Handler

```python
try:
    data = load_and_parse(source)
except (ValueError, TypeError) as e:
    print(f"Data format error: {e}")
```

### Multiple `except` Clauses — Most Specific First

```python
try:
    result = process(data)
except ZeroDivisionError:           # most specific first
    print("Division by zero")
except ArithmeticError:             # catches remaining ArithmeticErrors
    print("Math error")
except ValueError as e:
    print(f"Bad value: {e}")
except OSError as e:
    print(f"IO error: {e}")
except Exception as e:              # catch-all — last resort
    import traceback
    traceback.print_exc()
    raise                           # re-raise unexpected errors!
```

**Order matters:** Python checks top to bottom. If `Exception` is first, it catches everything and specific handlers never run.

### What NOT to Catch — The Broad Catches to Avoid

```python
# ❌ Too broad — hides bugs, catches Ctrl+C, SystemExit, etc.
except BaseException:
    pass

# ❌ Still too broad — hides ALL exceptions silently
except Exception:
    pass

# ❌ Bare except — catches EVERYTHING including SystemExit, KeyboardInterrupt
except:
    pass

# ✅ Catch-all that re-raises unexpected ones:
except Exception as e:
    log_error(e)   # log it
    raise          # re-raise — don't swallow!
```

---

## 4. `else` — Runs Only If No Exception

```python
try:
    result = parse(data)       # ONLY the risky operation
except ValueError:
    print("parse failed")
else:
    save(result)               # ONLY runs if try had NO exception
    notify(result)
```

### Why `else` Matters

```python
# ❌ Wrong: success code inside try
try:
    result = parse(data)
    save(result)         # if save() raises ValueError — we catch it!
except ValueError:
    print("WHICH one failed? parse or save?")

# ✅ Correct: only the "risky" code in try
try:
    result = parse(data)   # parse() raises ValueError — we catch it
except ValueError:
    print("parse failed")
else:
    save(result)           # save()'s ValueError propagates normally (NOT caught)
```

`else` gives you precision: the `except` only handles the specific operation you put in `try`, not every operation that happens after.

---

## 5. `finally` — Always Runs

```python
file = None
try:
    file = open("data.txt")
    data = file.read()
except FileNotFoundError as e:
    print(f"File not found: {e}")
except PermissionError as e:
    print(f"Permission denied: {e}")
else:
    process(data)         # only on success
finally:
    if file:
        file.close()      # ALWAYS — whether success, error, return, or break
```

**`finally` runs in ALL cases:**
- Normal completion ✅
- Exception handled ✅
- Exception not handled (program crashing) ✅
- `return` inside try ✅
- `break` or `continue` inside try ✅

### `finally` + `return` Gotcha

```python
def tricky():
    try:
        return "from try"
    finally:
        return "from finally"   # OVERRIDES the try return!

print(tricky())   # "from finally"  ← surprising!

# Rule: NEVER return from finally — it silently swallows exceptions and
# overrides other returns. finally is ONLY for cleanup.
```

### The Variable-Not-Assigned Trap

```python
# ❌ If open() fails, 'file' is never assigned → NameError in finally
try:
    file = open("data.txt")
    process(file)
finally:
    file.close()   # NameError if open() raised!

# ✅ Initialize to None first
file = None
try:
    file = open("data.txt")
    process(file)
finally:
    if file:
        file.close()   # safe check

# ✅✅ Better: use context manager — handles this automatically
try:
    with open("data.txt") as file:   # __exit__ calls close() always
        process(file)
except FileNotFoundError:
    handle_missing()
```

---

## 6. `raise` — All Forms

### Raise a New Exception

```python
def set_age(age):
    if not isinstance(age, int):
        raise TypeError(f"age must be int, got {type(age).__name__}")
    if not 0 <= age <= 120:
        raise ValueError(f"age must be 0–120, got {age}")
```

### Re-raise the Current Exception

```python
try:
    connect_db()
except ConnectionError as e:
    log_error(e)       # log it
    raise              # ← bare 'raise': re-raises SAME exception, PRESERVES traceback

# vs:
except ConnectionError as e:
    log_error(e)
    raise e            # ← 'raise e': also re-raises but RESETS traceback to THIS line
                       #   loses original location info — worse for debugging
```

**Always use bare `raise`** when you want to re-raise inside an `except` block.

### Exception Chaining — `raise ... from ...`

```python
try:
    config = load("app.json")
except FileNotFoundError as e:
    raise RuntimeError("Cannot start: config file missing") from e
    # Traceback shows BOTH:
    # FileNotFoundError: [Errno 2] No such file: 'app.json'
    # The above exception was the direct cause of the following:
    # RuntimeError: Cannot start: config file missing

# Suppress the chain with 'from None'
try:
    value = config["missing_key"]
except KeyError:
    raise ValueError("Required setting 'missing_key' not found") from None
    # Hides the KeyError — only shows ValueError
```

### Raise in Different Contexts

```python
# Raise without an active exception — must provide exception
raise ValueError("something went wrong")

# Re-raise inside except — no argument needed
try:
    risky()
except ValueError:
    log_it()
    raise   # re-raises the caught ValueError

# Conditional raise
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError(f"Cannot divide {a} by zero")
    return a / b

# Raise from a function that returns exception info
def validate(data):
    errors = []
    if not data.get("name"):
        errors.append("name is required")
    if errors:
        raise ValueError("; ".join(errors))
```

---

## 7. Custom Exceptions

```python
# Base exception for your application domain
class AppError(Exception):
    """Base for all application errors."""
    pass

# Specific domain exceptions
class ValidationError(AppError):
    """Input validation failed."""
    def __init__(self, field: str, message: str):
        super().__init__(f"'{field}': {message}")
        self.field   = field
        self.message = message

class NotFoundError(AppError):
    """Resource not found."""
    def __init__(self, resource: str, identifier=None):
        msg = f"{resource} not found"
        if identifier is not None:
            msg += f" (id={identifier!r})"
        super().__init__(msg)
        self.resource   = resource
        self.identifier = identifier

class AuthError(AppError):
    """Authentication or authorization failure."""
    pass

class RateLimitError(AppError):
    """Rate limit exceeded."""
    def __init__(self, retry_after: int = 60):
        super().__init__(f"Rate limit exceeded. Retry after {retry_after}s")
        self.retry_after = retry_after
```

### Why Custom Exceptions?

```python
# With custom exceptions, callers can catch at any level:
try:
    result = api_call()
except ValidationError as e:
    return 400, {"error": str(e), "field": e.field}
except NotFoundError as e:
    return 404, {"error": str(e)}
except AuthError:
    return 403, {"error": "Forbidden"}
except AppError as e:
    return 500, {"error": str(e)}      # catches any AppError we missed
# (unknown exceptions propagate up — don't catch what you can't handle)
```

---

## 8. Context Managers — `with` Statement

`with` = automatic `try/finally`. Calls `__enter__` on entry, `__exit__` on exit (always, even on exception).

```python
# File is always closed, even if exception occurs during processing
with open("data.txt") as f:
    data = f.read()

# Equivalent:
f = open("data.txt")
try:
    data = f.read()
finally:
    f.close()
```

### What `__enter__` and `__exit__` Do

```python
class DatabaseConnection:
    def __enter__(self):
        self.conn = connect_to_db()
        return self.conn         # value bound to 'as' variable

    def __exit__(self, exc_type, exc_val, exc_tb):
        # exc_type/val/tb are None if no exception occurred
        if exc_type is not None:
            self.conn.rollback()   # exception: rollback
        else:
            self.conn.commit()     # no exception: commit
        self.conn.close()
        return False   # don't suppress the exception (True would suppress it)

with DatabaseConnection() as conn:
    conn.execute("INSERT ...")
    conn.execute("UPDATE ...")
# commits on success, rolls back on exception, always closes
```

### `@contextmanager` — Simpler Way

```python
from contextlib import contextmanager

@contextmanager
def timer(label: str):
    import time
    start = time.perf_counter()
    try:
        yield                          # code inside 'with' runs here
    finally:
        elapsed = time.perf_counter() - start
        print(f"{label}: {elapsed:.3f}s")

with timer("database query"):
    result = db.execute("SELECT ...")
# prints: database query: 0.043s

# More useful context managers
from contextlib import suppress

# suppress — silently swallow specific exceptions
with suppress(FileNotFoundError):
    os.remove("maybe_exists.tmp")   # no error if file missing

# Multiple context managers
with open("in.txt") as src, open("out.txt", "w") as dst:
    dst.write(src.read().upper())
```

### `__exit__` Return Value

```python
class SuppressValueError:
    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is ValueError:
            return True    # True → suppress the exception, execution continues after 'with'
        return False       # False → propagate the exception

with SuppressValueError():
    raise ValueError("this is suppressed")
print("execution continues here")   # this runs!
```

---

## 9. Exception Inspection

```python
import traceback, sys

try:
    1 / 0
except ZeroDivisionError as e:
    # Exception attributes
    print(e.args)            # ('division by zero',)
    print(e.__class__)       # <class 'ZeroDivisionError'>
    print(e.__cause__)       # None (or chained exception)
    print(e.__traceback__)   # traceback object

    # Get traceback info
    exc_type, exc_value, exc_tb = sys.exc_info()
    for frame in traceback.extract_tb(exc_tb):
        print(f"  {frame.filename}:{frame.lineno} in {frame.name}")
        print(f"    {frame.line}")

    # Full traceback as string (for logging)
    tb_string = traceback.format_exc()

    # Log with full context
    import logging
    logging.error("Error in calculation", exc_info=True)
    # exc_info=True tells logging to include the full traceback
```

---

## Simple Production Example

```python
# user_service.py — complete exception handling for a user API

class UserNotFoundError(Exception):
    def __init__(self, user_id):
        super().__init__(f"User {user_id} not found")
        self.user_id = user_id

class UserInactiveError(Exception):
    def __init__(self, username):
        super().__init__(f"Account '{username}' is deactivated")

class InvalidCredentialsError(Exception):
    pass

class AccountLockedError(Exception):
    def __init__(self, username, locked_until):
        super().__init__(f"Account '{username}' locked until {locked_until}")
        self.locked_until = locked_until


def login(username: str, password: str, db) -> dict:
    """
    Authenticate user. Returns session data on success.
    Raises specific exception for each failure mode.
    """

    # Input validation
    if not username or not isinstance(username, str):
        raise ValueError("username must be a non-empty string")
    if not password:
        raise ValueError("password is required")

    # Fetch user
    user = db.get_by_username(username.strip().lower())
    if user is None:
        raise UserNotFoundError(username)

    # Status checks
    if user.locked_until and user.locked_until > now():
        raise AccountLockedError(username, user.locked_until)

    if not user.is_active:
        raise UserInactiveError(username)

    # Credential check
    if not user.verify_password(password):
        raise InvalidCredentialsError("Incorrect password")

    return {"token": generate_token(user.id), "user_id": user.id}


# API layer — map each exception to HTTP response
def handle_login_request(request: dict, db) -> dict:
    try:
        result = login(request.get("username"), request.get("password"), db)
        return {"status": 200, "data": result}

    except ValueError as e:
        return {"status": 400, "error": str(e)}

    except UserNotFoundError as e:
        return {"status": 404, "error": str(e)}

    except (InvalidCredentialsError, AccountLockedError, UserInactiveError) as e:
        return {"status": 401, "error": str(e)}   # don't reveal which

    except Exception as e:
        import traceback
        traceback.print_exc()    # log full trace internally
        return {"status": 500, "error": "Internal server error"}
```

---

## Summary

```
Exception = Python object (instance of exception class)
raise     → creates object, begins stack unwinding
except    → checked with isinstance() → parent catches children

try:     → risky code ONLY (minimal scope!)
except:  → handler (specific first, general last)
else:    → success path (runs ONLY if no exception in try)
finally: → cleanup (ALWAYS runs — even on return/break/crash)

raise           → re-raise current (preserves traceback) ✅
raise e         → re-raise (resets traceback to here) ❌
raise New() from original → explicit chain (shows both)
raise New() from None     → suppress original chain

Custom exceptions:
  class MyError(Exception): pass  — at minimum
  Add fields (field, code, retry_after) for rich error info
  Build hierarchy: AppError → ValidationError, NotFoundError, AuthError

with statement = __enter__ + __exit__ = guaranteed cleanup
  __exit__(exc_type, exc_val, exc_tb) — None if no exception
  return True to suppress exception, False/None to propagate

Never: except Exception: pass  — swallows everything silently
Always: log it, then raise if you can't fully handle it
```

---

## 🎯 5 Questions

1. What does Python do when an exception is raised with no matching `except`?
2. Why should success code go in `else` rather than at the end of `try`?
3. What is the difference between `raise` and `raise e`?
4. When does `finally` NOT run?
5. What does returning `True` from `__exit__` do?

---

<!-- ══════════════════════════════════════════════════════ -->

# 🐍 Topic 09 — Functions & Built-in Functions

> *"A function is a first-class object. It has a type, an address, attributes, a code object. You can assign it, pass it, return it, store it in a list. Why? Because Python's design treats code as data — and that single decision enables closures, decorators, callbacks, and every higher-order pattern."*

---

## 1. Functions Are First-Class Objects

"First-class" means: functions can be used anywhere any other value can be used.

```python
def greet(name):
    """Greet someone by name."""
    return f"Hello, {name}!"

# Functions have type, identity, attributes — like any object
print(type(greet))         # <class 'function'>
print(id(greet))           # memory address
print(greet.__name__)      # 'greet'
print(greet.__doc__)       # 'Greet someone by name.'
print(greet.__code__)      # <code object greet ...>

# Assign to a variable — function IS a value
say_hi = greet
print(say_hi("Arjun"))     # Hello, Arjun!
print(say_hi is greet)     # True — same object

# Store in a data structure
handlers = {
    "greet":   greet,
    "upper":   str.upper,
    "reverse": lambda s: s[::-1],
}
print(handlers["greet"]("World"))   # Hello, World!
print(handlers["upper"]("hello"))   # HELLO

# Pass as argument to another function (higher-order function)
def apply(func, value):
    return func(value)

print(apply(greet, "Python"))   # Hello, Python!
print(apply(len, "Python"))     # 6

# Return from a function
def make_greeter(greeting):
    def greeter(name):
        return f"{greeting}, {name}!"
    return greeter             # return a function object

say_hello = make_greeter("Hello")
say_hi    = make_greeter("Hi")
print(say_hello("Arjun"))     # Hello, Arjun!
print(say_hi("World"))        # Hi, World!
```

### Why "First-Class" — Why It Matters

Functions being first-class is what enables:
- **Callbacks** — pass a function to be called later
- **Decorators** — wrap a function with another function
- **Closures** — inner function captures outer variables
- **Strategy pattern** — pass different behavior as a parameter
- **Event handlers** — `button.on_click(my_function)`

```python
# Without first-class functions — you'd need verbose patterns
# With first-class functions — clean and direct

# Sorting with custom key — passing a function as argument
users = [{"name": "Bob", "age": 30}, {"name": "Alice", "age": 25}]
sorted(users, key=lambda u: u["age"])   # sort by age — lambda IS a function object
sorted(users, key=lambda u: u["name"]) # sort by name
```

---

## 2. Function Object Under the Hood

```python
def add(a, b):
    return a + b
```

When Python executes `def`:
```
1. Compile function body → code object (bytecode)
2. Create PyFunctionObject on the heap:
   ┌───────────────────────────────────┐
   │  func_name     = "add"           │
   │  func_code     → code object     │  ← compiled bytecode
   │  func_globals  → module globals  │  ← what global names this sees
   │  func_defaults → None            │  ← default args (if any)
   │  func_closure  → None            │  ← closure cells (if any)
   │  func_doc      → docstring       │
   └───────────────────────────────────┘
3. Bind name "add" in namespace → points to this object
```

### Stack Frame on Call

```python
add(3, 5)
```

```
Creates a new STACK FRAME:
  ┌────────────────────────────┐
  │  Frame: add()              │
  │  locals: {a: 3, b: 5}     │
  │  back: → caller's frame   │
  └────────────────────────────┘
Executes bytecode:
  LOAD_FAST a  → 3
  LOAD_FAST b  → 5
  BINARY_OP +  → 8
  RETURN_VALUE → pops frame, returns 8 to caller

Frame is destroyed on return → locals freed immediately
```

---

## 3. Defining Functions — All Syntax Forms

### Basic `def`

```python
def function_name(parameters):
    """Docstring."""
    body
    return value

# No return → implicitly returns None
def greet(name):
    print(f"Hello, {name}")

result = greet("Arjun")
print(result)   # None
```

### Multiple Return Values

```python
def minmax(lst):
    return min(lst), max(lst)   # returns TUPLE

low, high = minmax([3, 1, 4, 1, 5])   # tuple unpacking
result    = minmax([3, 1, 4, 1, 5])
print(type(result))    # <class 'tuple'>
print(result)          # (1, 5)
```

### Nested Functions

```python
def outer(x):
    print(f"outer: x={x}")

    def inner(y):             # inner defined INSIDE outer
        print(f"inner: x={x}, y={y}")   # can access outer's x
        return x + y

    return inner(10)          # call inner from within outer

result = outer(5)
# outer: x=5
# inner: x=5, y=10
print(result)   # 15

# inner is NOT accessible from outside:
# inner(10)   → NameError: name 'inner' is not defined
```

---

## 4. Arguments — All Types, All Cases

### The Complete Argument Order

```python
def complete(
    pos_only,           # positional-only (before /)
    also_pos_only,      # positional-only
    /,                  # ← positional-only marker
    normal,             # regular: can be positional OR keyword
    normal2 = "default",# regular with default
    *args,              # variable positional: extra positional args → tuple
    keyword_only,       # keyword-only (after *): MUST be named
    kw_only2 = 10,      # keyword-only with default
    **kwargs            # variable keyword: extra keyword args → dict
):
    pass
```

### 1. Positional Arguments

```python
def describe(name, age, city):
    return f"{name}, {age}, {city}"

describe("Arjun", 22, "Ahmedabad")   # all positional — order matters
describe(city="Ahmedabad", name="Arjun", age=22)  # all keyword — any order
describe("Arjun", city="Ahmedabad", age=22)       # mixed — positional first
```

### 2. Default Arguments

```python
def connect(host, port=5432, timeout=30, ssl=False):
    return f"Connecting to {host}:{port} (timeout={timeout}, ssl={ssl})"

connect("localhost")                       # all defaults
connect("localhost", 3306)                 # override port
connect("localhost", timeout=10)           # keyword override
connect("localhost", 3306, 10, True)       # all positional
```

### 3. The Mutable Default Trap — Critical!

```python
# ❌ BUG — [] created ONCE when 'def' executes
# stored in function.__defaults__ = ([],)
# same list object reused on every call!
def add_to_list(item, lst=[]):
    lst.append(item)
    return lst

add_to_list(1)    # [1]
add_to_list(2)    # [1, 2]  ← list persisted between calls!
add_to_list(3)    # [1, 2, 3]

# Proof:
print(add_to_list.__defaults__)   # ([1, 2, 3],)  ← the mutated list

# ✅ CORRECT — use None as sentinel
def add_to_list(item, lst=None):
    if lst is None:
        lst = []    # new list created EACH call
    lst.append(item)
    return lst

add_to_list(1)   # [1]
add_to_list(2)   # [2]  ← fresh each time

# Same applies to dict, set — any mutable default
def create(name, meta=None):
    if meta is None:
        meta = {}   # new dict each call
    meta["name"] = name
    return meta
```

### 4. `*args` — Variable Positional Arguments

```python
def total(*args):
    print(type(args))    # <class 'tuple'>  ← always a tuple
    print(args)          # (1, 2, 3, 4)
    return sum(args)

total(1, 2, 3, 4)        # 10
total()                  # 0 — empty tuple
total(5)                 # 5

# *args after required positional args
def log(level, *messages):
    for msg in messages:
        print(f"[{level}] {msg}")

log("INFO", "Server started", "Port 8000", "Ready")

# Unpacking into *args call
nums = [1, 2, 3]
total(*nums)   # same as total(1, 2, 3)
```

### 5. `**kwargs` — Variable Keyword Arguments

```python
def display(**kwargs):
    print(type(kwargs))   # <class 'dict'>  ← always a dict
    for k, v in kwargs.items():
        print(f"  {k}: {v}")

display(name="Arjun", age=22, city="Ahmedabad")

# **kwargs after required args
def create_user(username, **profile):
    return {"username": username, **profile}

create_user("arjun", age=22, role="dev", active=True)
# {'username': 'arjun', 'age': 22, 'role': 'dev', 'active': True}

# Unpacking dict into **kwargs call
opts = {"sep": "-", "end": "\n\n"}
print("a", "b", "c", **opts)   # a-b-c  (with double newline)
```

### 6. Positional-Only Parameters — `/` (Python 3.8+)

```python
def circle_area(radius, /, precision=2):
    """radius is positional-only — cannot be passed as keyword."""
    import math
    return round(math.pi * radius ** 2, precision)

circle_area(5)               # ✅ positional
circle_area(5, precision=4)  # ✅ precision is keyword-capable
circle_area(radius=5)        # ❌ TypeError: positional-only argument passed as keyword

# Why use /?
# 1. Implementation freedom: rename 'radius' internally without breaking callers
# 2. Avoid ambiguity when parameter name conflicts with **kwargs
```

### 7. Keyword-Only Parameters — `*` (Python 3.0+)

```python
def send_email(to, subject, *, cc=None, bcc=None, priority="normal"):
    """cc, bcc, priority must be passed by name."""
    pass

send_email("a@b.com", "Hi")                           # ✅
send_email("a@b.com", "Hi", cc="c@d.com")             # ✅
send_email("a@b.com", "Hi", "c@d.com")                # ❌ TypeError: 3rd positional unexpected
send_email("a@b.com", "Hi", cc="c@d.com", bcc=None)   # ✅

# Why keyword-only?
# Forces callers to be explicit — easier to read at call site
# send_email("to", "subject", True, False) is confusing
# send_email("to", "subject", cc="c@d.com", bcc=None) is clear
```

### 8. Combined — All Argument Types Together

```python
def fully_typed(
    required,          # positional-only
    /,
    normal,            # positional or keyword
    optional="default",# positional or keyword with default
    *args,             # extra positionals → tuple
    kw_required,       # keyword-only, no default (required!)
    kw_optional=None,  # keyword-only with default
    **kwargs           # extra keywords → dict
):
    print(f"required={required}")
    print(f"normal={normal}")
    print(f"optional={optional}")
    print(f"args={args}")
    print(f"kw_required={kw_required}")
    print(f"kw_optional={kw_optional}")
    print(f"kwargs={kwargs}")

fully_typed(
    1,                    # required (positional-only)
    2,                    # normal
    "x",                  # optional
    "a", "b", "c",        # goes into *args
    kw_required="MUST",   # keyword-only required
    kw_optional="nice",   # keyword-only optional
    extra1="e1",          # goes into **kwargs
    extra2="e2",
)
```

---

## 5. Scope — LEGB Rule

Python resolves names in four scopes, searched in order:

```
L — Local:     names inside the current function
E — Enclosing: names in enclosing functions (closures)
G — Global:    names at module level
B — Built-in:  names in builtins module (print, len, range, etc.)
```

```python
x = "global"   # G scope

def outer():
    x = "enclosing"   # E scope (for inner)

    def inner():
        x = "local"   # L scope
        print(x)      # L: 'local'

    inner()
    print(x)          # E: 'enclosing'

outer()
print(x)              # G: 'global'

# Name lookup for 'print' inside inner():
# L: not there
# E: not there
# G: not there
# B: found! print is a built-in
```

### `global` — Modify Module-Level Variable

```python
count = 0   # global variable

def increment():
    global count       # declare: use the GLOBAL 'count', not create a local
    count += 1

def reset():
    global count
    count = 0

increment()
increment()
print(count)   # 2

# Without 'global':
def bad_increment():
    count += 1   # UnboundLocalError! Python sees the assignment and thinks
                 # 'count' is a local variable, but it hasn't been assigned yet
```

### `nonlocal` — Modify Enclosing Function's Variable

```python
def make_counter(start=0):
    count = start        # enclosing scope variable

    def increment(by=1):
        nonlocal count   # declare: use ENCLOSING 'count'
        count += by
        return count

    def reset():
        nonlocal count
        count = start

    def get():
        return count     # just reading — no nonlocal needed

    return increment, reset, get

inc, rst, get = make_counter(10)
print(inc())    # 11
print(inc(5))   # 16
print(get())    # 16
rst()
print(get())    # 10
```

### Variable Scope — All Edge Cases

```python
# Case 1: read global without 'global' keyword — OK
x = 10
def f():
    print(x)   # reads global x — OK, no 'global' needed for reading

# Case 2: assign without 'global' — creates LOCAL variable
x = 10
def f():
    x = 20      # creates new LOCAL x — doesn't modify global x
    print(x)    # 20

f()
print(x)   # still 10

# Case 3: BOTH read AND assign → UnboundLocalError
x = 10
def f():
    print(x)    # Python sees x is assigned below → treats as local
    x = 20      # local assignment
# f()  → UnboundLocalError: local variable 'x' referenced before assignment

# Case 4: class body is its own scope (NOT LEGB-searchable from methods)
class Counter:
    count = 0   # class scope

    def increment(self):
        # count += 1  ← NameError: 'count' not found in L/E/G/B
        Counter.count += 1   # must qualify with class name
        # or: type(self).count += 1
```

---

## 6. Closures — Functions That Remember

A closure is a function that **captures variables from its enclosing scope** even after that scope has finished.

```python
def make_multiplier(factor):
    # 'factor' lives in make_multiplier's frame
    def multiply(x):
        return x * factor   # 'factor' captured
    return multiply          # return inner function

double = make_multiplier(2)
triple = make_multiplier(3)

# make_multiplier's frame is gone — but factor is preserved!
print(double(5))   # 10
print(triple(5))   # 15
```

### How Closure Cells Work

```
make_multiplier(2) executes:
  Creates frame with local: factor = 2
  Creates 'multiply' function object
  Python detects 'multiply' uses 'factor' from outer scope
  Creates a CELL OBJECT: cell(factor=2)
  multiply.__closure__ = (cell(2),)

make_multiplier's frame pops — but cell(2) stays alive
  because multiply holds a reference to it

double(5):
  Looks up 'factor' → not in local → check closure cells → cell(2)
  Returns 5 * 2 = 10
```

```python
# Inspect the closure
print(double.__closure__)                       # (<cell at 0x...>,)
print(double.__closure__[0].cell_contents)      # 2
print(triple.__closure__[0].cell_contents)      # 3
```

### Closure — Multiple Functions Sharing a Cell

```python
def make_account(balance=0):
    """All three inner functions share the SAME 'balance' cell."""

    def deposit(amount):
        nonlocal balance
        balance += amount
        return balance

    def withdraw(amount):
        nonlocal balance
        if amount > balance:
            raise ValueError("Insufficient funds")
        balance -= amount
        return balance

    def get_balance():
        return balance   # read-only — no nonlocal needed

    return deposit, withdraw, get_balance

deposit, withdraw, balance = make_account(1000)
print(deposit(500))    # 1500
print(withdraw(200))   # 1300
print(balance())       # 1300
```

### The Classic Closure Loop Bug

```python
# ❌ Bug — all functions capture the SAME 'i' variable by reference
funcs = []
for i in range(3):
    def f():
        return i        # captures 'i' by REFERENCE, not by value
    funcs.append(f)

print([f() for f in funcs])   # [2, 2, 2]  ← all see final i=2!

# ✅ Fix 1 — default argument captures current value
funcs = []
for i in range(3):
    def f(i=i):         # i=i: default arg copies current value
        return i
    funcs.append(f)

print([f() for f in funcs])   # [0, 1, 2]  ✅

# ✅ Fix 2 — factory function
funcs = []
for i in range(3):
    def make_f(val):
        def f():
            return val
        return f
    funcs.append(make_f(i))

print([f() for f in funcs])   # [0, 1, 2]  ✅
```

---

## 7. Lambda — Anonymous Functions

```python
# Syntax: lambda parameters: expression (one expression only)
square = lambda x: x ** 2
add    = lambda a, b: a + b

print(square(5))   # 25
print(add(3, 4))   # 7

# Lambda IS a function object
print(type(square))   # <class 'function'>
print(square.__name__)# '<lambda>'
```

### When to Use Lambda

```python
# ✅ Good use: short key functions for sorting/filtering
users = [{"name": "Bob", "age": 30}, {"name": "Alice", "age": 25}]

sorted(users, key=lambda u: u["age"])
sorted(users, key=lambda u: (u["age"], u["name"]))   # multi-key
sorted(users, key=lambda u: -u["age"])               # descending

min(users, key=lambda u: u["age"])
max(users, key=lambda u: u["age"])

# ✅ Good: simple callbacks and one-off functions
numbers = [1, -2, 3, -4, 5]
positives = list(filter(lambda x: x > 0, numbers))
doubled   = list(map(lambda x: x * 2, numbers))

# Sort by stock descending, then price ascending
sorted(products, key=lambda p: (-p["stock"], p["price"]))
```

### When NOT to Use Lambda

```python
# ❌ Complex logic — use def
process = lambda x: x if x > 0 else (x * -1 if x < -10 else 0)

# ✅ Use def for anything complex
def process(x):
    if x > 0:    return x
    if x < -10:  return x * -1
    return 0

# ❌ Lambda assigned to a name (pointless — just use def)
double = lambda x: x * 2   # no benefit over def

# ✅
def double(x): return x * 2

# Lambda cannot contain statements — only expressions
# No assignment, no return, no if/else blocks, no loops
# lambda x: x = 1  ← SyntaxError
```

---

## 8. Decorators — Functions That Transform Functions

A decorator takes a function, wraps it, and returns the wrapped version.

```python
# The @ syntax is PURE syntactic sugar:
@decorator
def my_func():
    pass

# Is EXACTLY:
def my_func():
    pass
my_func = decorator(my_func)
```

### Building a Decorator

```python
import functools

def log_calls(func):
    @functools.wraps(func)    # copies __name__, __doc__, etc. to wrapper
    def wrapper(*args, **kwargs):
        print(f"→ Calling {func.__name__}({args}, {kwargs})")
        result = func(*args, **kwargs)
        print(f"← {func.__name__} returned {result!r}")
        return result
    return wrapper

@log_calls
def add(a, b):
    return a + b

add(2, 3)
# → Calling add((2, 3), {})
# ← add returned 5
```

### `@functools.wraps` — Why It Matters

```python
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def good_decorator(func):
    @functools.wraps(func)    # preserves original metadata
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@bad_decorator
def my_func():
    """My docstring."""
    pass

@good_decorator
def my_func2():
    """My docstring."""
    pass

print(my_func.__name__)    # 'wrapper'    ← lost original name
print(my_func.__doc__)     # None         ← lost docstring
print(my_func2.__name__)   # 'my_func2'   ← preserved
print(my_func2.__doc__)    # 'My docstring.' ← preserved
```

Without `@functools.wraps`, all decorated functions look like `wrapper` in stack traces and `help()`.

### Decorator with Arguments — Three Layers

```python
def retry(max_attempts=3, delay=1.0):
    """Decorator factory — returns a decorator."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import time
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise
                    print(f"Attempt {attempt} failed: {e}. Retrying...")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5)
def fetch_data(url):
    return http_get(url)
```

```
@retry(max_attempts=3, delay=0.5)
  Step 1: retry(max_attempts=3, delay=0.5) called → returns decorator
  Step 2: decorator(fetch_data) called → returns wrapper
  Step 3: fetch_data = wrapper
```

### Stacking Decorators

```python
@decorator_a
@decorator_b
@decorator_c
def func():
    pass

# Applied BOTTOM-UP at definition:
# func = decorator_a(decorator_b(decorator_c(func)))

# Executed TOP-DOWN at call:
# decorator_a's wrapper → decorator_b's wrapper → decorator_c's wrapper → func
```

### Common Decorator Patterns

```python
import functools, time

# 1. Timing
def timed(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start  = time.perf_counter()
        result = func(*args, **kwargs)
        ms     = (time.perf_counter() - start) * 1000
        print(f"{func.__name__}: {ms:.2f}ms")
        return result
    return wrapper

# 2. Caching (memoization)
def memoize(func):
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    wrapper.cache = cache        # expose cache for inspection
    return wrapper

# Or use stdlib (preferred):
@functools.lru_cache(maxsize=128)
def fibonacci(n):
    if n <= 1: return n
    return fibonacci(n-1) + fibonacci(n-2)

# 3. Access control
def requires_auth(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.get("user"):
            raise PermissionError("Authentication required")
        return func(request, *args, **kwargs)
    return wrapper
```

---

## 9. Higher-Order Built-in Functions

### `map()` — Apply Function to Each Item (Lazy)

```python
# map(func, iterable) → iterator (lazy — nothing computed until consumed)
numbers = [1, 2, 3, 4, 5]
squared = map(lambda x: x**2, numbers)

# Nothing computed yet — squared is an iterator
list(squared)   # [1, 4, 9, 16, 25]  ← computed on demand

# map with multiple iterables
sums = list(map(lambda a, b: a + b, [1,2,3], [10,20,30]))
# [11, 22, 33]

# When is lazy map better than list comprehension?
# When you only need partial results:
from itertools import islice
first_3 = list(islice(map(expensive_fn, big_list), 3))
# Only computes 3 results — list comprehension would compute ALL

# Equivalent list comprehension (eager):
squared_list = [x**2 for x in numbers]   # all computed now
```

### `filter()` — Keep Matching Items (Lazy)

```python
# filter(func, iterable) → iterator
numbers  = [-3, -1, 0, 2, 5, -2, 8]
positive = list(filter(lambda x: x > 0, numbers))   # [2, 5, 8]

# filter(None, iterable) — removes all falsy values
data    = [0, 1, None, 2, "", 3, False, 4]
cleaned = list(filter(None, data))   # [1, 2, 3, 4]
```

### `reduce()` — Fold Sequence to Single Value

```python
from functools import reduce

nums = [1, 2, 3, 4, 5]

# Basic accumulation
total   = reduce(lambda acc, x: acc + x, nums, 0)   # 15
product = reduce(lambda acc, x: acc * x, nums, 1)   # 120

# Each step: function(accumulator, current_item) → new accumulator
# reduce(+, [1,2,3,4,5], 0):
#   Step 1: acc=0,  x=1  → 1
#   Step 2: acc=1,  x=2  → 3
#   Step 3: acc=3,  x=3  → 6
#   Step 4: acc=6,  x=4  → 10
#   Step 5: acc=10, x=5  → 15

# Complex accumulation — group and sum in ONE pass
records = [
    {"state": "MH", "amount": 5000},
    {"state": "GJ", "amount": 3000},
    {"state": "MH", "amount": 2000},
]

state_totals = reduce(
    lambda acc, r: {**acc, r["state"]: acc.get(r["state"], 0) + r["amount"]},
    records,
    {}
)
print(state_totals)   # {"MH": 7000, "GJ": 3000}
# ONE pass, no intermediate list, build dict as accumulator
```

### `sorted()`, `min()`, `max()` with `key`

```python
products = [{"name": "B", "price": 500}, {"name": "A", "price": 200}]

# All accept a 'key' function
sorted(products, key=lambda p: p["price"])           # ascending
sorted(products, key=lambda p: p["price"], reverse=True) # descending
sorted(products, key=lambda p: (-p["price"], p["name"])) # multi-key

min(products, key=lambda p: p["price"])   # cheapest item
max(products, key=lambda p: p["price"])   # most expensive

# itemgetter — faster than lambda for attribute/key access
from operator import itemgetter, attrgetter
sorted(products, key=itemgetter("price"))   # same result, faster
```

### `any()` and `all()` — Short-Circuit Boolean Checks

```python
# any(): returns True at FIRST truthy — stops early
any(x > 10 for x in [1, 2, 15, 3])   # True — stops at 15, never checks 3
any(x > 10 for x in [1, 2, 3])       # False — checks all

# all(): returns False at FIRST falsy — stops early
all(x > 0 for x in [1, 2, -1, 3])   # False — stops at -1
all(x > 0 for x in [1, 2, 3])       # True — checks all

# Use generators so they're lazy (short-circuit works)
# Using list would compute all values first:
all([x > 0 for x in [1, 2, -1]])    # list computed fully then passed to all
all(x > 0 for x in [1, 2, -1])     # generator — short-circuits at -1
```

### `functools.partial` — Pre-fill Arguments

```python
from functools import partial

def send(user_id: int, message: str, channel: str = "email", priority: int = 1):
    print(f"Send to {user_id} via {channel}: {message} [priority={priority}]")

# Create specialised versions with some args pre-filled
send_email = partial(send, channel="email", priority=1)
send_urgent = partial(send, channel="sms", priority=10)

send_email(42, "Your order shipped")
send_urgent(42, "Account compromised!")

# Real use: configure a function for a specific context
from functools import partial
int_from_hex = partial(int, base=16)
int_from_bin = partial(int, base=2)

int_from_hex("FF")    # 255
int_from_bin("1010")  # 10
```

### `functools.lru_cache` — Memoization

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_user_permissions(user_id: int) -> tuple:
    """Cached DB lookup — expensive query run once per user_id."""
    return tuple(db.query_permissions(user_id))   # tuple is hashable

get_user_permissions(42)   # DB hit
get_user_permissions(42)   # cache hit — no DB
get_user_permissions(42)   # cache hit — no DB

print(get_user_permissions.cache_info())
# CacheInfo(hits=2, misses=1, maxsize=128, currsize=1)

get_user_permissions.cache_clear()   # invalidate when permissions change
```

### Essential Built-ins — Complete Reference

```python
# Type & identity
type(x)                  # <class 'int'>
isinstance(x, int)       # True/False, respects inheritance
issubclass(bool, int)    # True
id(x)                    # memory address
callable(x)              # True if x() would work (has __call__)
hash(x)                  # hash value (for hashable objects)

# Numeric
abs(-5)                  # 5
round(3.7)               # 4
round(3.14159, 2)        # 3.14
pow(2, 10)               # 1024
pow(2, 10, 1000)         # 24 (modular exponentiation)
divmod(17, 5)            # (3, 2) — quotient and remainder at once
sum([1,2,3])             # 6
sum([1,2,3], 100)        # 106 — with starting value
min(3,1,4,1)             # 1
max(3,1,4,1)             # 4
min([3,1,4])             # 1 — also works on iterable

# Sequence creation
range(5)                 # 0,1,2,3,4
range(2, 10, 2)          # 2,4,6,8
list(range(5))           # [0,1,2,3,4]
tuple([1,2,3])           # (1,2,3)
set([1,1,2,3])           # {1,2,3}
frozenset([1,2,3])       # frozenset({1,2,3})
dict(a=1, b=2)           # {'a':1,'b':2}

# Iteration
len([1,2,3])             # 3 — calls __len__
reversed([1,2,3])        # iterator: 3,2,1
sorted([3,1,2])          # [1,2,3]
enumerate(["a","b"])     # (0,'a'), (1,'b')
zip([1,2],[3,4])         # (1,3),(2,4)
map(str, [1,2,3])        # '1','2','3' (lazy)
filter(None, [0,1,2])    # 1,2 (lazy)
any([0,0,1])             # True
all([1,1,1])             # True

# String / conversion
str(42)                  # '42'
repr(42)                 # '42' (same for int, different for str)
int("42")                # 42
float("3.14")            # 3.14
bool(0)                  # False
chr(65)                  # 'A'
ord('A')                 # 65
bin(10)                  # '0b1010'
oct(8)                   # '0o10'
hex(255)                 # '0xff'
format(3.14159, ".2f")   # '3.14'

# Object inspection
dir(x)                   # list all attributes and methods
vars(obj)                # obj.__dict__ — instance attributes as dict
getattr(obj, "name")     # obj.name
getattr(obj, "name", default)  # obj.name or default if missing
setattr(obj, "name", val)      # obj.name = val
hasattr(obj, "name")           # True if attribute exists
delattr(obj, "name")           # del obj.name

# I/O
print(*args, sep=" ", end="\n", file=sys.stdout, flush=False)
input("prompt: ")        # always returns str
open(file, mode="r", encoding=None)  # modes: r w a b x +

# Memory
__import__("os")         # dynamic import
globals()                # current global namespace dict
locals()                 # current local namespace dict
```

---

## Simple Production Example

```python
# product_service.py — first-class functions, closures, decorators, builtins

import functools
import time
import logging

logger = logging.getLogger(__name__)


# Decorator: log function calls with timing
def log_and_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            ms = (time.perf_counter() - start) * 1000
            logger.info(f"{func.__name__} completed in {ms:.1f}ms")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} failed: {e}")
            raise
    return wrapper


# Closure: creates a filter function bound to a category
def make_category_filter(category: str):
    """Returns a function that tests if a product matches category."""
    def matches(product: dict) -> bool:
        return product.get("category") == category
    matches.__name__ = f"is_{category}"
    return matches


# Cached lookup
@functools.lru_cache(maxsize=64)
def get_tax_rate(category: str) -> float:
    """Cached tax rate lookup by category."""
    rates = {"electronics": 0.18, "food": 0.05, "clothing": 0.12}
    return rates.get(category, 0.18)   # default 18%


@log_and_time
def compute_invoice(products: list, filter_fn=None, discount_pct: float = 0) -> dict:
    """
    Compute invoice total.
    filter_fn: optional function(product) -> bool for filtering
    discount_pct: percentage discount 0–100
    """
    if not isinstance(discount_pct, (int, float)):
        raise TypeError(f"discount_pct must be numeric, got {type(discount_pct).__name__}")
    if not 0 <= discount_pct <= 100:
        raise ValueError(f"discount_pct must be 0–100, got {discount_pct}")

    # Filter using passed function (or include all)
    items = list(filter(filter_fn, products)) if filter_fn else products

    if not items:
        return {"items": 0, "subtotal": 0, "tax": 0, "total": 0}

    # Compute line totals using map
    line_totals = list(map(lambda p: p["price"] * p["qty"], items))
    subtotal = sum(line_totals)

    # Compute tax using reduce — one pass through items
    tax = functools.reduce(
        lambda acc, p: acc + p["price"] * p["qty"] * get_tax_rate(p["category"]),
        items,
        0.0
    )

    discount = subtotal * (discount_pct / 100)
    total    = subtotal + tax - discount

    return {
        "items":    len(items),
        "subtotal": round(subtotal, 2),
        "tax":      round(tax, 2),
        "discount": round(discount, 2),
        "total":    round(total, 2),
    }


# Test
products = [
    {"name": "Laptop",    "price": 50000, "qty": 1, "category": "electronics"},
    {"name": "Rice 5kg",  "price": 300,   "qty": 2, "category": "food"},
    {"name": "T-Shirt",   "price": 599,   "qty": 3, "category": "clothing"},
    {"name": "Headphones","price": 2999,  "qty": 1, "category": "electronics"},
]

# Full invoice
invoice = compute_invoice(products, discount_pct=10)
print(f"Full invoice: ₹{invoice['total']:.2f} ({invoice['items']} items)")

# Electronics only — pass a closure-based filter
electronics_filter = make_category_filter("electronics")
elec_invoice = compute_invoice(products, filter_fn=electronics_filter)
print(f"Electronics only: ₹{elec_invoice['total']:.2f}")

# Using partial to create a pre-configured invoicing function
compute_with_gst = functools.partial(compute_invoice, discount_pct=0)
gst_invoice = compute_with_gst(products)
print(f"GST invoice: ₹{gst_invoice['total']:.2f}")
```

---

## Summary

```
Functions are FIRST-CLASS OBJECTS:
  type(), id(), __name__, __doc__, __code__ — like any object
  Assignable, passable, returnable, storable in collections

def:       creates function object + code object, binds name in namespace
Call:      creates stack frame, executes bytecode, pops frame on return

ARGUMENT TYPES (in order):
  pos_only, / , normal, default=val, *args, kw_only, kw_only=val, **kwargs
  /: before → positional-only (can't be keyword)
  *: after  → keyword-only (must be keyword)
  *args:    extra positionals → tuple
  **kwargs: extra keywords → dict
  
MUTABLE DEFAULT TRAP:
  def f(lst=[])  ← [] created ONCE, shared — always use None

SCOPE — LEGB: Local → Enclosing → Global → Built-in
  global:   declare to modify module-level variable
  nonlocal: declare to modify enclosing function's variable
  Reading is fine without declaration; assignment creates local

CLOSURES:
  Inner function captures outer variable via CELL OBJECT
  Cell stays alive even after outer function returns
  Loop bug: capture by reference → use default arg or factory

LAMBDA:  lambda x: expr  — function object, one expression only
  Use for short key functions; use def for anything complex

DECORATORS: @decorator = func = decorator(func)
  @functools.wraps always — preserves __name__, __doc__
  With args: factory → decorator → wrapper (3 layers)
  Stack: bottom-up definition, top-down execution

KEY BUILT-INS:
  map(f, it)    → lazy iterator
  filter(f, it) → lazy iterator
  reduce(f, it, init) → single accumulated value
  sorted(it, key=f, reverse=False)
  any(gen) / all(gen) → short-circuit boolean
  partial(f, **kwargs) → pre-filled function
  lru_cache(maxsize) → automatic memoization
```

---

## 🎯 5 Questions

1. Why are functions called "first-class citizens" and what does that enable?
2. What is stored in `func.__closure__` and why does a cell object keep variables alive?
3. Why is `def f(data=[])` dangerous and what's the correct pattern?
4. What does `@functools.wraps(func)` actually do and why is it important?
5. What is the difference between `map()` and a list comprehension in terms of when computation happens?