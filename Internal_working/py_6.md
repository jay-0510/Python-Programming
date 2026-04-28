# 🐍 Iterators, Generators, Scope & Decorators

---

## 📖 How This File Is Organized

```
PART 1 — ITERATION
  1. Iterable vs Iterator — what's the difference?
  2. Under the hood — what Python actually does
  3. The iterator protocol — __iter__ and __next__
  4. Build your own for loop
  5. Custom iterator class
  6. When to use list vs iterator?

PART 2 — GENERATORS
  7. Why generators exist (problem with iterators)
  8. yield — how it works at memory level
  9. How generator remembers local variables
  10. yield vs return — the core difference
  11. Generator expressions
  12. Real-world use cases: list / iterator / generator — which when?

PART 3 — SCOPE & NAMESPACES
  13. What is a namespace?
  14. LEGB rule — all cases with output
  15. global and nonlocal keywords
  16. Edge cases that trip everyone up

PART 4 — DECORATORS
  17. What problem decorators solve
  18. Without @ sign — the manual way first
  19. With @ sign — syntactic sugar
  20. How decorators work at call stack / memory level
  21. Decorator with arguments (3-layer pattern)
  22. Chaining decorators — order matters
  23. Real-world use cases
```

---

# PART 1 — ITERATION

---

## 1. Iterable vs Iterator — The Difference

These two words sound similar but they are **different things**. This confuses most beginners.

```
ITERABLE:  An object you CAN loop over.
           Has __iter__() method.
           Example: list, string, dict, set, range, file

ITERATOR:  An object that PRODUCES values one at a time.
           Has __iter__() AND __next__() method.
           Remembers WHERE it is in the sequence.
           Example: list_iterator, file object, generator
```

Think of it like this:

```
ITERABLE = a book (you can read it, it holds the content)
ITERATOR = a bookmark (knows which PAGE you're currently on)

Reading a book:
  1. You take the book (iterable)
  2. You place a bookmark (create iterator from iterable)
  3. You read page by page (call __next__ each time)
  4. Bookmark reaches last page → stop (StopIteration)
```

### Checking in Code — Using `dir()`

```python
my_list = [1, 2, 3]

# Check what methods it has
print("__iter__" in dir(my_list))   # True  ← it's iterable
print("__next__" in dir(my_list))   # False ← it's NOT an iterator

# Create an iterator FROM the list
my_iter = iter(my_list)
print("__iter__" in dir(my_iter))   # True
print("__next__" in dir(my_iter))   # True ← NOW it's an iterator

# You can also check with hasattr
print(hasattr(my_list, "__iter__"))  # True  — iterable
print(hasattr(my_list, "__next__"))  # False — not iterator
print(hasattr(my_iter, "__next__"))  # True  — iterator

# Check the types directly
from collections.abc import Iterable, Iterator
print(isinstance(my_list, Iterable))  # True
print(isinstance(my_list, Iterator))  # False
print(isinstance(my_iter, Iterator))  # True
```

---

## 2. Under the Hood — What Python Actually Does in a `for` Loop

```python
for item in [1, 2, 3]:
    print(item)
```

Most people think Python magically loops. Here's what **actually** happens:

```
Step 1:  Python calls iter([1, 2, 3])
         This calls list.__iter__()
         Returns a list_iterator object

Step 2:  Python calls next(iterator) repeatedly
         Each call: list_iterator.__next__()
         Returns: 1, then 2, then 3

Step 3:  After 3 is returned, next call raises StopIteration
         Python catches it → loop ends

That's it. That's the entire mechanism.
```

```
for item in [1, 2, 3]:         BECOMES:
    print(item)
                                _iter = iter([1, 2, 3])
                                while True:
                                    try:
                                        item = next(_iter)
                                        print(item)
                                    except StopIteration:
                                        break
```

---

## 3. The Iterator Protocol — Two Methods

```python
# The FULL contract:
# __iter__(self)   → must return self (so iterator is also iterable)
# __next__(self)   → return next value, OR raise StopIteration

# Proving this manually:
numbers = [10, 20, 30]

it = iter(numbers)       # creates iterator
print(next(it))          # 10
print(next(it))          # 20
print(next(it))          # 30
print(next(it))          # StopIteration raised!

# Once exhausted — iterator is DONE
# You cannot restart it
# You must create a new iterator

it2 = iter(numbers)      # fresh iterator
print(next(it2))         # 10  ← starts from beginning

# Iterator calls iter(self) → returns itself
print(iter(it2) is it2)  # True — iterator IS its own iterable
```

---

## 4. Build Your Own `for` Loop

```python
def my_for_loop(iterable, func):
    """
    Replicate exactly what Python's for loop does.
    No magic — just the iterator protocol.
    """
    iterator = iter(iterable)       # Step 1: get iterator
    while True:
        try:
            item = next(iterator)   # Step 2: get next value
            func(item)              # Step 3: do the work
        except StopIteration:
            break                   # Step 4: stop when done

# Test it
my_for_loop([1, 2, 3], print)
# 1
# 2
# 3

my_for_loop("hello", print)
# h
# e
# l
# l
# o
```

This is EXACTLY what Python does internally. No difference whatsoever.

---

## 5. Custom Iterator — Build Your Own

When you need a sequence that doesn't fit neatly into a list.

**Example: Generate square numbers on demand**

```python
class SquareNumbers:
    """
    Iterates through square numbers: 1, 4, 9, 16, 25...
    Does NOT pre-compute them — produces one at a time.
    """

    def __init__(self, limit):
        self.limit   = limit    # how many squares to produce
        self.current = 1        # current number we're squaring

    def __iter__(self):
        return self             # return self — iterator is its own iterable

    def __next__(self):
        if self.current > self.limit:
            raise StopIteration  # signal: we're done
        
        result       = self.current ** 2
        self.current += 1        # move to next
        return result


# Use it like any iterable
for sq in SquareNumbers(5):
    print(sq)
# 1, 4, 9, 16, 25

# Works with all built-ins
squares = SquareNumbers(5)
print(list(squares))     # [1, 4, 9, 16, 25]
print(sum(SquareNumbers(5)))  # 55
print(max(SquareNumbers(5)))  # 25
```

**Under the hood when Python runs `for sq in SquareNumbers(5)`:**

```
1. Python calls iter(SquareNumbers(5))
   → calls SquareNumbers.__iter__()
   → returns self (same object)

2. Python calls next(obj) repeatedly
   → calls SquareNumbers.__next__()
   → returns 1, 4, 9, 16, 25 in order

3. When current > limit:
   → __next__ raises StopIteration
   → Python catches it, loop ends
```

---

## 6. When to Use List vs Iterator?

```
USE A LIST when:
  ✅ You need random access: items[5], items[-1]
  ✅ You need len()
  ✅ You need to iterate MULTIPLE times
  ✅ The data fits comfortably in memory
  ✅ You need to sort, reverse, or slice

USE AN ITERATOR when:
  ✅ Data is LARGE — you can't load it all into memory
  ✅ You only need to go through it ONCE
  ✅ Values are expensive to compute (compute on demand)
  ✅ Data is INFINITE (like a stream or sensor feed)
  ✅ You're building a pipeline of transformations
```

```python
# LIST — loads everything into RAM
all_users = db.fetch_all_users()   # 1 million users → ~500MB in RAM!
for user in all_users:
    send_email(user)

# ITERATOR — one user at a time, constant memory
for user in db.fetch_users_iter():  # fetches in chunks, ~few KB
    send_email(user)
```

---

*Now here's the problem: writing an iterator class like SquareNumbers above is verbose. You need a class, `__iter__`, `__next__`, manage state manually. That's a lot of code for something simple.*

*This is exactly why generators were invented.*

---

# PART 2 — GENERATORS

---

## 7. Why Generators Exist — The Problem They Solve

```python
# The iterator class for squares:  12 lines of code
class SquareNumbers:
    def __init__(self, limit):
        self.limit   = limit
        self.current = 1
    def __iter__(self):
        return self
    def __next__(self):
        if self.current > self.limit:
            raise StopIteration
        result = self.current ** 2
        self.current += 1
        return result

# The GENERATOR version:  3 lines of code
def square_numbers(limit):
    for i in range(1, limit + 1):
        yield i ** 2

# Same usage:
for sq in square_numbers(5):
    print(sq)
# 1, 4, 9, 16, 25
```

**Generators are iterators that Python writes for you.** You just use `yield`.

A generator function automatically gets `__iter__` and `__next__` — you write none of that boilerplate.

---

## 8. `yield` — How It Works at Memory Level

This is the most important thing to understand:

```python
def my_gen():
    print("START")
    yield 1           # pause here
    print("AFTER 1")
    yield 2           # pause here
    print("AFTER 2")
    yield 3           # pause here
    print("DONE")
```

```python
g = my_gen()          # NO code runs yet. Zero. Nothing.
                      # Just a generator object created.

print(next(g))        # START printed, returns 1, PAUSES at yield 1
print(next(g))        # AFTER 1 printed, returns 2, PAUSES at yield 2
print(next(g))        # AFTER 2 printed, returns 3, PAUSES at yield 3
print(next(g))        # DONE printed, then StopIteration raised
```

Output:
```
START
1
AFTER 1
2
AFTER 2
3
DONE
StopIteration
```

**The key: generator does NOT run until you call `next()`.**

---

## 9. How Generator Remembers Local Variables

This is the magic. Regular functions lose all locals when they return. Generators **preserve** them.

```
REGULAR FUNCTION:
  Call → frame created → runs → return → FRAME DESTROYED
  All locals gone forever.

GENERATOR:
  Call → generator object created (frame NOT running yet)
  next() → frame RESUMES, runs until yield
  yield  → frame SUSPENDED (locals PRESERVED in memory)
  next() → frame RESUMES from exact same line
  return → StopIteration raised, frame finally destroyed
```

```python
def counter(start, end):
    current = start         # local variable

    while current <= end:
        yield current       # PAUSE — but 'current' is preserved!
        current += 1        # resumes HERE after pause

g = counter(1, 5)

# Check the frame's locals (they're preserved!)
next(g)
print(g.gi_frame.f_locals)  # {'start': 1, 'end': 5, 'current': 2}

next(g)
print(g.gi_frame.f_locals)  # {'start': 1, 'end': 5, 'current': 3}
```

```
Memory picture:

AFTER first next(g):
  ┌──────────────────────────────────┐
  │  Generator frame (SUSPENDED)     │
  │  f_locals: {                     │
  │    start:   1,                   │
  │    end:     5,                   │
  │    current: 2  ← updated!        │
  │  }                               │
  │  f_lasti: line number of yield   │ ← knows WHERE it paused
  └──────────────────────────────────┘

This frame stays in memory until the generator is exhausted.
next() resumes it. yield suspends it again.
```

---

## 10. `yield` vs `return` — The Core Difference

```python
# RETURN — ends the function, frame destroyed
def get_numbers_return():
    return [1, 2, 3]     # builds full list, returns it, DONE

result = get_numbers_return()
print(result)   # [1, 2, 3]  — the whole list

# YIELD — pauses function, frame preserved
def get_numbers_yield():
    yield 1              # pause, give 1
    yield 2              # pause, give 2
    yield 3              # pause, give 3
    # implicit return → StopIteration

result = get_numbers_yield()
print(result)   # <generator object>  — NOT the values yet
print(next(result))  # 1
print(next(result))  # 2
print(next(result))  # 3
```

```
┌─────────────────────────────────────────────────────────────┐
│                    yield  vs  return                        │
├────────────────────────┬────────────────────────────────────┤
│  return                │  yield                             │
├────────────────────────┼────────────────────────────────────┤
│  Ends the function     │  Pauses the function               │
│  Frame destroyed       │  Frame preserved in memory         │
│  Returns one value     │  Can produce many values over time │
│  Caller gets value     │  Caller gets generator object      │
│  Can't resume          │  Resumes on next()                 │
│  All values at once    │  One value at a time (lazy)        │
└────────────────────────┴────────────────────────────────────┘
```

### `yield` in a loop — Most Common Pattern

```python
def read_lines(filepath):
    """Read a file one line at a time. Works for ANY size file."""
    with open(filepath) as f:
        for line in f:
            yield line.strip()

# Usage — memory stays constant even for 10GB files
for line in read_lines("huge_log.txt"):
    if "ERROR" in line:
        print(line)

# WHY: only ONE line is in memory at any time
# 'return f.readlines()' would load entire file into RAM
```

---

## 11. Generator Expressions — Compact Generator

Just like list comprehension but with `()` instead of `[]` — and it's LAZY.

```python
# List comprehension — computes ALL NOW, stores in RAM
squares_list = [x**2 for x in range(1_000_000)]
# ~8 MB in memory

# Generator expression — computes ONE AT A TIME
squares_gen = (x**2 for x in range(1_000_000))
# ~120 bytes in memory! (just the generator object)

import sys
print(sys.getsizeof([x**2 for x in range(1_000_000)]))  # ~8MB
print(sys.getsizeof((x**2 for x in range(1_000_000))))  # 120 bytes
```

### When Generator Expression Is Perfect

```python
# sum, max, min, any, all — consume one value at a time
# Pass generator directly — no list needed

total   = sum(x**2 for x in range(1_000_000))       # never makes a list
maximum = max(x**2 for x in range(1_000_000))
found   = any(x > 999 for x in data)                # stops at first match!
valid   = all(x > 0   for x in numbers)             # stops at first False!
```

---

## 12. Choosing: `for` Loop / Iterator / Generator — Which When?

```
SCENARIO                              BEST CHOICE
─────────────────────────────────────────────────────────────────
Simple list of 100 items              for loop with list
Need to transform a list              list comprehension
Need result for further processing    list comprehension
Large file (millions of rows)         generator function
Infinite sequence (stream/sensor)     generator function
One-time computation of sequence      generator expression
Need sum/max/any of large data        generator expression
Need random access (items[5])         list
Need to iterate multiple times        list
Custom complex iteration logic        iterator class (rare)
Lazy pipeline of transformations      generator pipeline
```

```python
# CASE 1: Simple processing → list comprehension
emails = ["  A@B.COM  ", "c@d.com ", " E@F.org"]
clean  = [e.strip().lower() for e in emails]   # fine, small data

# CASE 2: Large CSV file → generator
def read_csv(path):
    with open(path) as f:
        next(f)  # skip header
        for line in f:
            yield line.strip().split(",")

for row in read_csv("million_rows.csv"):
    process(row)  # constant memory, any file size

# CASE 3: Sum of filtered data → generator expression
# Don't make a list just to sum it
total = sum(float(row[2]) for row in read_csv("sales.csv") if row[1] == "MH")

# CASE 4: Infinite sequence → generator
def live_prices(symbol):
    """Continuously yield stock prices from API."""
    while True:
        yield fetch_price(symbol)   # never ends!

for price in live_prices("RELIANCE"):
    if price > 2500:
        place_sell_order()
        break
```

---

*Now that you understand iteration and generators, let's look at scope — because closures (used in generators AND decorators) depend on it.*

---

# PART 3 — SCOPE & NAMESPACES

---

## 13. What Is a Namespace?

A namespace is simply a **dictionary** that maps names to objects.

```python
x = 10
y = "hello"

# Python stores these like:
# globals() = {"x": <int object 10>, "y": <str object "hello">, ...}

print(globals()["x"])   # 10 — same as print(x)
print(globals()["y"])   # hello
```

**Three main namespaces:**

```
Built-in namespace:   print, len, range, int, str, ...  (always available)
Global namespace:     names at module (file) level
Local namespace:      names inside a function call
```

```
Namespace as dict:
  built-in:  {"print": <func>, "len": <func>, "range": <func>, ...}
  global:    {"x": 10, "greet": <func>, "DB_URL": "..."}
  local:     {"name": "Arjun", "result": 42}  (exists only during function call)
```

---

## 14. LEGB Rule — The Name Lookup Order

When Python sees a name, it searches in this exact order and **stops at the first match**:

```
L  →  Local:     Inside the current function
E  →  Enclosing: Inside any enclosing functions (closures)
G  →  Global:    Module level (the file)
B  →  Built-in:  Python's built-in names (print, len, etc.)
```

```
                ┌──────────────────────────────┐
                │         BUILT-IN             │  print, len, range...
                │  ┌───────────────────────┐   │
                │  │       GLOBAL          │   │  module-level names
                │  │  ┌────────────────┐   │   │
                │  │  │   ENCLOSING    │   │   │  outer function
                │  │  │  ┌──────────┐  │   │   │
                │  │  │  │  LOCAL   │  │   │   │  current function
                │  │  │  │  x = ?   │  │   │   │
                │  │  │  └──────────┘  │   │   │
                │  │  └────────────────┘   │   │
                │  └───────────────────────┘   │
                └──────────────────────────────┘

Name search: LOCAL first → ENCLOSING → GLOBAL → BUILT-IN
             Stops at FIRST match. Error if not found in any.
```

### All LEGB Cases With Output

```python
# ── CASE 1: LOCAL found first ────────────────────────────────────
x = "global"

def func():
    x = "local"     # creates LOCAL x
    print(x)        # finds LOCAL x first → "local"

func()
print(x)            # back to module level → "global"
```
```
Output:
local
global
```

---

```python
# ── CASE 2: ENCLOSING found ──────────────────────────────────────
x = "global"

def outer():
    x = "enclosing"     # outer's local (enclosing for inner)

    def inner():
        print(x)        # L: not there, E: found "enclosing"
    
    inner()

outer()
print(x)                # G: "global"
```
```
Output:
enclosing
global
```

---

```python
# ── CASE 3: GLOBAL found ─────────────────────────────────────────
x = "global"

def func():
    print(x)    # L: not there, E: no enclosing, G: found "global"

func()
```
```
Output:
global
```

---

```python
# ── CASE 4: BUILT-IN found ───────────────────────────────────────
def func():
    print(len("hello"))  
    # L: 'len' not there
    # E: no enclosing
    # G: not at module level
    # B: found! len is a built-in

func()
```
```
Output:
5
```

---

```python
# ── CASE 5: All four levels together ────────────────────────────
x = "G"   # global

def outer():
    x = "E"    # enclosing

    def middle():
        x = "L"   # local

        def inner():
            print(x)     # L: not in inner → E: found "L" from middle
        inner()
        print(x)         # L: "L" from middle
    
    middle()
    print(x)     # L: "E" from outer (middle returned, its frame gone)

outer()
print(x)         # G: "G"
```
```
Output:
L
L
E
G
```

---

```python
# ── CASE 6: NameError — not found anywhere ───────────────────────
def func():
    print(undefined_name)   # L: no, E: no, G: no, B: no → NameError

# func()  # NameError: name 'undefined_name' is not defined
```

---

```python
# ── CASE 7: Read global vs Create local ─────────────────────────
count = 0

def show():
    print(count)   # ✅ READS global — no assignment, no issue

def increment():
    count = count + 1   # ❌ UnboundLocalError!
    # Python sees assignment to 'count' → treats as local
    # But before assignment, it tries to READ local 'count' → doesn't exist yet!

# Why? Python scans the WHOLE function body at compile time.
# If any assignment to 'count' exists → treated as local everywhere in function.
# Reading before assignment → UnboundLocalError.
```

---

## 15. `global` and `nonlocal`

### `global` — Reach Into Module Level

```python
login_count = 0   # module-level

def record_login():
    global login_count      # "I mean the GLOBAL login_count"
    login_count += 1        # modifies global

record_login()
record_login()
record_login()
print(login_count)   # 3
```

```
Without 'global':
  Python sees 'login_count += 1'
  Tries to create a LOCAL 'login_count'
  += needs to READ it first → doesn't exist yet → UnboundLocalError

With 'global login_count':
  Python knows: this name refers to the GLOBAL scope
  Goes to global dict, modifies it directly
```

### `nonlocal` — Reach Into Enclosing Function

```python
def make_counter():
    count = 0        # enclosing variable

    def increment():
        nonlocal count   # "I mean the ENCLOSING count"
        count += 1
        return count

    def reset():
        nonlocal count
        count = 0

    return increment, reset

inc, rst = make_counter()
print(inc())    # 1
print(inc())    # 2
print(inc())    # 3
rst()
print(inc())    # 1  (reset worked)
```

```
Without 'nonlocal':
  Python sees 'count += 1' → treats as local
  Reading local count before assignment → UnboundLocalError

With 'nonlocal count':
  Python looks in ENCLOSING scope → finds count in make_counter's frame
  Modifies it directly
```

---

## 16. Scope Edge Cases

```python
# ── Edge Case 1: Shadowing a built-in ──────────────────────────
# You can accidentally hide built-in names
list = [1, 2, 3]      # BAD: 'list' now points to your list, not the built-in!
print(list([4, 5]))   # TypeError: 'list' object is not callable
del list              # recover the built-in
print(list([4, 5]))   # [4, 5]  ✅

# ── Edge Case 2: Class scope is NOT in LEGB ─────────────────────
class Counter:
    count = 0          # class-level variable

    def increment(self):
        # count += 1   ← NameError: 'count' not found
        # Class scope is NOT searched in LEGB!
        Counter.count += 1    # must qualify with class name

# ── Edge Case 3: Comprehension has its own scope ────────────────
x = 10
result = [x for x in range(5)]  # this 'x' is LOCAL to comprehension
print(x)    # 10 — outer 'x' unchanged (Python 3)
            # Python 2 would print 4 (comprehension leaked) — fixed in Python 3

# ── Edge Case 4: Lambda captures by reference ───────────────────
funcs = [lambda: i for i in range(3)]
print([f() for f in funcs])   # [2, 2, 2] ← all see final i=2
# Fix: default arg
funcs = [lambda i=i: i for i in range(3)]
print([f() for f in funcs])   # [0, 1, 2] ✅
```

---

*Understanding scope is critical because decorators use closures, and closures depend on the enclosing (E) scope. Now let's build decorators from the ground up.*

---

# PART 4 — DECORATORS

---

## 17. What Problem Decorators Solve

Imagine you have several API functions and you need to log every call:

```python
def get_user(user_id):
    print(f"→ Calling get_user({user_id})")   # logging
    result = db.find_user(user_id)
    print(f"← get_user returned {result}")    # logging
    return result

def create_order(data):
    print(f"→ Calling create_order({data})")  # same logging
    result = db.create(data)
    print(f"← create_order returned {result}")
    return result

def delete_item(item_id):
    print(f"→ Calling delete_item({item_id})")  # same logging again
    result = db.delete(item_id)
    print(f"← delete_item returned {result}")
    return result
```

The logging code is **repeated** in every function. If the format changes, you update 50 places.

**Decorators let you add this behaviour ONCE, apply everywhere.**

---

## 18. Without @ Sign — Building It Manually First

Understanding this step is crucial before the `@` syntax.

### Step 1: A function that wraps another function

```python
def log_calls(func):           # takes a function as argument
    def wrapper(*args, **kwargs):
        print(f"→ Calling {func.__name__}")
        result = func(*args, **kwargs)   # calls the original
        print(f"← Done")
        return result
    return wrapper             # returns the NEW function


# The original function
def get_user(user_id):
    return f"User #{user_id}"


# MANUALLY wrapping — without @ syntax
get_user = log_calls(get_user)    # replace get_user with wrapped version

# Now calling get_user actually calls wrapper
get_user(42)
# → Calling get_user
# ← Done
```

```
What happened in memory:

BEFORE wrapping:
  "get_user" → <function get_user at 0x001>

AFTER: get_user = log_calls(get_user)
  log_calls creates 'wrapper' function
  wrapper closes over 'func' (which is the original get_user)
  "get_user" → <function wrapper at 0x002>   ← name now points to wrapper
  wrapper.__closure__[0] = cell(<function get_user at 0x001>)
```

### Step 2: Apply to multiple functions

```python
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

# Manual decoration:
add      = log_calls(add)
multiply = log_calls(multiply)

add(2, 3)
# → Calling add
# ← Done

multiply(4, 5)
# → Calling multiply
# ← Done
```

---

## 19. With `@` Sign — Syntactic Sugar

`@decorator` is **identical** to `func = decorator(func)`. That's all it is.

```python
@log_calls
def get_user(user_id):
    return f"User #{user_id}"

# IS EXACTLY THE SAME AS:
def get_user(user_id):
    return f"User #{user_id}"
get_user = log_calls(get_user)
```

The `@` just makes it cleaner to read — you see the decoration right at the function definition.

```python
# Clean version with @ syntax:
import functools

def log_calls(func):
    @functools.wraps(func)        # preserves __name__, __doc__
    def wrapper(*args, **kwargs):
        print(f"→ {func.__name__}({args}, {kwargs})")
        result = func(*args, **kwargs)
        print(f"← returned {result!r}")
        return result
    return wrapper


@log_calls
def get_user(user_id):
    return f"User #{user_id}"

@log_calls
def create_order(data):
    return {"id": 1, **data}


get_user(42)
# → get_user((42,), {})
# ← returned 'User #42'

create_order({"item": "laptop"})
# → create_order(({'item': 'laptop'},), {})
# ← returned {'id': 1, 'item': 'laptop'}
```

---

## 20. How Decorators Work — Call Stack and Memory

```python
import functools

def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("before")
        result = func(*args, **kwargs)
        print("after")
        return result
    return wrapper

@log_calls
def add(a, b):
    return a + b

add(2, 3)
```

**Step by step at definition time:**

```
1. Python compiles 'add' → creates function object at 0x001
2. Python calls log_calls(add):
   a. 'func' in log_calls refers to original add (0x001)
   b. 'wrapper' function created at 0x002
   c. wrapper has closure: __closure__ = [cell(func=0x001)]
   d. log_calls returns wrapper (0x002)
3. Name "add" now points to wrapper (0x002)
   Original add object still exists — wrapper holds it via closure
```

**Step by step at call time `add(2, 3)`:**

```
Call stack grows:

  ┌─────────────────────────────────────┐
  │  wrapper(a=2, b=3)                  │  ← Python calls wrapper (add = wrapper)
  │  → print("before")                  │
  │  → calls func(2, 3)                 │  ← func is original add via closure
  │    ┌───────────────────────────────┐│
  │    │  add(a=2, b=3)               ││  ← original add runs
  │    │  → return 2 + 3 = 5          ││
  │    └───────────────────────────────┘│
  │  → result = 5                       │
  │  → print("after")                   │
  │  → return 5                         │
  └─────────────────────────────────────┘
```

```
Memory after decoration:

  "add" ──────────────→ [wrapper function]
                              │
                        __closure__
                              │
                              ▼
                        cell: func ──→ [original add function]
```

### `@functools.wraps` — Why It's Important

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@decorator
def my_function():
    """This is my function's docstring."""
    pass

# WITHOUT @functools.wraps:
print(my_function.__name__)  # 'wrapper'   ← wrong!
print(my_function.__doc__)   # None        ← lost!

# Now with @functools.wraps:
def decorator(func):
    @functools.wraps(func)    # copies metadata from func to wrapper
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@decorator
def my_function():
    """This is my function's docstring."""
    pass

print(my_function.__name__)  # 'my_function'  ✅
print(my_function.__doc__)   # 'This is my function's docstring.'  ✅
```

Without `@functools.wraps`, stack traces show `wrapper` everywhere instead of the real function name, and `help()` shows nothing useful.

---

## 21. Decorator With Arguments — Three-Layer Pattern

Sometimes you want to configure the decorator:

```python
@retry(times=3)          # this is a decorator WITH an argument
def fetch_data(url):
    ...
```

This requires THREE layers:

```python
import functools, time

def retry(times=3, delay=1.0):        # Layer 1: FACTORY — takes config args
    def decorator(func):              # Layer 2: DECORATOR — takes the function
        @functools.wraps(func)
        def wrapper(*args, **kwargs): # Layer 3: WRAPPER — runs each call
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == times:
                        raise         # all attempts failed
                    print(f"Attempt {attempt} failed: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
        return wrapper
    return decorator


@retry(times=3, delay=0.5)
def call_payment_api(amount):
    # Might fail due to network
    import random
    if random.random() < 0.5:
        raise ConnectionError("Network timeout")
    return {"status": "success", "amount": amount}
```

**How `@retry(times=3)` is processed:**

```
Step 1: retry(times=3, delay=0.5) is called
        → returns 'decorator' function

Step 2: decorator(call_payment_api) is called
        → creates wrapper with closure over func AND times AND delay
        → returns wrapper

Step 3: call_payment_api = wrapper

So:  @retry(times=3)
     def call_payment_api(...):

Is:  call_payment_api = retry(times=3)(call_payment_api)
```

---

## 22. Chaining Decorators — Order Matters

```python
@decorator_a
@decorator_b
@decorator_c
def my_func():
    pass
```

**Applied BOTTOM-UP at definition time:**
```
my_func = decorator_a(decorator_b(decorator_c(my_func)))
```

**Executed TOP-DOWN at call time:**
```
my_func() calls:
  decorator_a's wrapper
    → calls decorator_b's wrapper
        → calls decorator_c's wrapper
            → calls original my_func
```

**Example showing the order:**

```python
import functools

def bold(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"<b>{func(*args, **kwargs)}</b>"
    return wrapper

def italic(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"<i>{func(*args, **kwargs)}</i>"
    return wrapper

def underline(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"<u>{func(*args, **kwargs)}</u>"
    return wrapper


@bold
@italic
@underline
def greet(name):
    return f"Hello, {name}"


print(greet("Arjun"))
# Applied bottom-up: underline first, then italic, then bold
# <b><i><u>Hello, Arjun</u></i></b>
```

```
Definition:
  greet = bold(italic(underline(greet)))
          ↑ outermost           ↑ innermost

Call:
  bold's wrapper runs first
    italic's wrapper runs second
      underline's wrapper runs third
        original greet runs last
```

---

## 23. Real-World Use Cases — Simple Code

### Use Case 1: Timing Functions

```python
import functools
import time

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start  = time.perf_counter()
        result = func(*args, **kwargs)
        end    = time.perf_counter()
        print(f"{func.__name__} took {(end-start)*1000:.2f}ms")
        return result
    return wrapper


@timer
def process_orders(orders):
    return [o["amount"] * 1.18 for o in orders]


orders = [{"amount": 500} for _ in range(100_000)]
result = process_orders(orders)
# process_orders took 12.34ms
```

---

### Use Case 2: Authentication Check

```python
import functools

def require_login(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.get("user"):
            raise PermissionError("You must be logged in")
        return func(request, *args, **kwargs)
    return wrapper


@require_login
def get_my_orders(request):
    return f"Orders for {request['user']}"

@require_login
def update_profile(request, data):
    return f"Updated {request['user']} with {data}"


# Test
try:
    req = {"user": "arjun"}
    print(get_my_orders(req))           # Orders for arjun

    req_no_user = {}
    print(get_my_orders(req_no_user))   # PermissionError

except PermissionError as e:
    print(f"Error: {e}")
```

---

### Use Case 3: Caching / Memoization

```python
import functools

def simple_cache(func):
    """Cache function results by arguments."""
    cache = {}

    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            print(f"  Computing {func.__name__}{args}...")
            cache[args] = func(*args)
        else:
            print(f"  Cache hit for {func.__name__}{args}")
        return cache[args]

    wrapper.clear_cache = lambda: cache.clear()
    return wrapper


@simple_cache
def get_tax_rate(state: str, year: int) -> float:
    # Imagine this queries a database
    rates = {("MH", 2024): 0.18, ("GJ", 2024): 0.12}
    return rates.get((state, year), 0.18)


print(get_tax_rate("MH", 2024))   # Computing...  → 0.18
print(get_tax_rate("MH", 2024))   # Cache hit!    → 0.18
print(get_tax_rate("GJ", 2024))   # Computing...  → 0.12

# Or use stdlib's built-in:
@functools.lru_cache(maxsize=128)
def get_tax_rate_v2(state: str, year: int) -> float:
    rates = {("MH", 2024): 0.18, ("GJ", 2024): 0.12}
    return rates.get((state, year), 0.18)
```

---

### Use Case 4: Combining Decorators

```python
import functools

# Apply multiple behaviours cleanly
@timer            # outer: times everything including auth check
@require_login    # inner: auth check before actual function
def get_dashboard(request):
    return f"Dashboard for {request['user']}"


req = {"user": "arjun"}
result = get_dashboard(req)
# get_dashboard took 0.05ms
```

---

## Summary Flowchart — Everything Connected

```
ITERABLE                    ITERATOR                   GENERATOR
   │                            │                          │
   │ has __iter__()             │ has __iter__()           │ is an iterator
   │ does NOT have __next__()   │ AND __next__()           │ created by yield
   │                            │                          │
   │  iter(iterable)            │  next(iterator)          │  yield pauses,
   │  ──────────────→           │  ──────────────→         │  preserves frame
   │  creates iterator          │  returns next value      │
   │                            │  or StopIteration        │
   └────────────────────────────┴──────────────────────────┘
                                        │
                              for loop uses this protocol
                                        │
                                        ▼
SCOPE (LEGB)
  Names in closures (E scope) keep variables alive
                │
                ▼
DECORATORS
  function that wraps another function
  uses closures to hold reference to original function
  @syntax = func = decorator(func)
  chains: bottom-up wrap, top-down execute
```

---

## Quick Reference

```
ITERABLE  = has __iter__  (list, str, dict, range, generator)
ITERATOR  = has __iter__ + __next__  (iterator objects, generators)
GENERATOR = iterator made with yield  (simpler than iterator class)

for x in obj:
  = _it = iter(obj) → while True: x = next(_it) except StopIteration: break

yield    = pause function, preserve frame, return value
return   = end function, destroy frame, return value

LEGB: Local → Enclosing → Global → Built-in  (stops at first found)
global:    modify module-level variable inside function
nonlocal:  modify enclosing function's variable inside nested function

DECORATOR:
  @dec def f(): ...   =   f = dec(f)
  with args: f = dec(arg)(f)   [3 layers: factory → decorator → wrapper]
  chain: @a @b = a(b(f))  applied bottom-up, executed top-down
  always use @functools.wraps to preserve __name__ and __doc__
```

---

## 🎯 10 Questions Across All Topics

1. What is the difference between an iterable and an iterator? Give one example of each.
2. What two dunder methods must an iterator have?
3. How do you check if an object is an iterator using `dir()`?
4. What does `yield` do differently from `return` at the memory level?
5. Why does a generator use less memory than a list for large data?
6. What is the LEGB rule and in what order does Python search?
7. What is the difference between `global` and `nonlocal`?
8. Why does `def f(): x = x + 1` (where x is a global) raise `UnboundLocalError`?
9. What does `@functools.wraps(func)` preserve and why does it matter?
10. When decorators are stacked `@a @b @c`, in what order are they applied at definition? In what order do they execute at call time?
