# Python Concurrency & Ruff — Interview Prep Guide

> **Goal:** Understand the *why* behind each concept, not just the definition.
> Every section follows: **Mental Model → How it works → When to use it → Gotchas**

---

## Table of Contents

1. [The GIL — What it is and why it exists](#1-the-gil)
2. [Multithreading](#2-multithreading)
3. [Multiprocessing](#3-multiprocessing)
4. [Async IO](#4-async-io)
5. [Concurrency vs Parallelism — The Big Picture](#5-concurrency-vs-parallelism)
6. [How GIL Affects Each Model](#6-how-gil-affects-concurrency)
7. [Ruff — Linter and Formatter](#7-ruff)
8. [Quick Decision Table](#8-quick-decision-table)
9. [25 Interview Questions & Answers](#9-interview-questions--answers)

---

## 1. The GIL

### Mental Model

> Imagine a kitchen with one knife. Ten chefs can work in the kitchen (threads exist), but only one chef can hold the knife at a time (only one thread runs Python bytecode at a time).

### What Is It?

The **Global Interpreter Lock (GIL)** is a mutex (mutual exclusion lock) inside CPython — the standard Python interpreter. It ensures that **only one thread executes Python bytecode at any given moment**, even on a multi-core machine.

### Why Does It Exist?

CPython manages memory using **reference counting**. Every object tracks how many names point to it. When that count hits zero, the object is freed.

```python
x = [1, 2, 3]   # ref count = 1
y = x            # ref count = 2
del x            # ref count = 1
del y            # ref count = 0 → memory freed
```

Without the GIL, two threads could decrement the same ref count simultaneously — one could free memory the other is still using. The GIL prevents this race condition by allowing only one thread to touch Python objects at a time.

### Key Facts

- The GIL is a **CPython implementation detail** — not part of the Python language spec
- **Jython** (Java-based) and **PyPy-STM** don't have it
- The GIL is **released** during I/O operations (file reads, network calls, sleep) — threads CAN run concurrently during I/O
- The GIL is **NOT released** during CPU-bound Python code (loops, math, string processing)
- **Python 3.13+** introduced experimental support for a "free-threaded" mode (no GIL), opt-in

### The Practical Impact

```
CPU-bound work:  Thread A runs → GIL held → Thread B waits → no real parallelism
I/O-bound work:  Thread A starts I/O → GIL released → Thread B runs → real concurrency
```

---

## 2. Multithreading

### Mental Model

> Multiple workers sharing one desk. They can take turns at the desk, but only one works at a time. Great when most of their work involves waiting (phone calls, fetching files) — bad when all work is calculation.

### How It Works

Python's `threading` module creates OS-level threads. They share the same memory space (same variables, same objects). The GIL controls who runs Python code at any moment.

```python
import threading
import time

results = []   # Shared memory — all threads can read/write this

def fetch_data(url):
    time.sleep(1)          # GIL is RELEASED during sleep/I/O
    results.append(url)    # GIL re-acquired to modify the list

threads = [threading.Thread(target=fetch_data, args=(f"url_{i}",)) for i in range(5)]

for t in threads: t.start()
for t in threads: t.join()   # Wait for all to finish

print(results)   # All 5 results, took ~1s not ~5s ✓
```

### When Threads ARE Useful (I/O-bound)

- **HTTP requests** — waiting for a server response, GIL released
- **File reads/writes** — disk I/O, GIL released
- **Database queries** — network I/O to the DB, GIL released
- **sleep()** — GIL released, other threads run

### When Threads Are USELESS (CPU-bound)

```python
import threading

def count_up():
    total = 0
    for _ in range(10_000_000):   # Pure Python loop — GIL held the WHOLE time
        total += 1
    return total

# Two threads on two cores still take ~2x time — GIL forces them to take turns
t1 = threading.Thread(target=count_up)
t2 = threading.Thread(target=count_up)
# No speedup. Actually slightly SLOWER due to GIL contention overhead.
```

### Thread Safety

Threads share memory — this creates race conditions:

```python
counter = 0

def increment():
    global counter
    for _ in range(100_000):
        counter += 1   # NOT atomic — read, add, write are three steps
                       # Another thread can interrupt between them

t1 = threading.Thread(target=increment)
t2 = threading.Thread(target=increment)
t1.start(); t2.start()
t1.join();  t2.join()
print(counter)   # Could be 150,000 or 180,000 — not 200,000!
```

**Fix with a Lock:**

```python
import threading

counter = 0
lock = threading.Lock()

def increment():
    global counter
    for _ in range(100_000):
        with lock:     # Only one thread runs this block at a time
            counter += 1

# Now result is always 200,000 ✓
```

### ThreadPoolExecutor (Modern API)

```python
from concurrent.futures import ThreadPoolExecutor
import requests

urls = ["https://api.example.com/data"] * 10

def fetch(url):
    return requests.get(url).json()

with ThreadPoolExecutor(max_workers=5) as pool:
    results = list(pool.map(fetch, urls))
# All 10 requests happen concurrently — 5 at a time ✓
```

---

## 3. Multiprocessing

### Mental Model

> Multiple kitchens, each with their own knife, cutting board, and chef. They don't share anything. Each kitchen is a separate Python interpreter. True parallelism on multiple CPU cores.

### How It Works

`multiprocessing` spawns **separate OS processes**. Each process has:
- Its own Python interpreter
- Its own GIL
- Its own memory space (no shared variables by default)
- Its own copy of the data

Because each process has its own GIL, they truly run in parallel on separate CPU cores.

```python
from multiprocessing import Pool
import os

def cpu_heavy(n):
    """Pure computation — GIL would block threads, but processes are free"""
    total = sum(i * i for i in range(n))
    return total

if __name__ == "__main__":   # REQUIRED on Windows/macOS — prevents recursive spawning
    with Pool(processes=4) as pool:
        results = pool.map(cpu_heavy, [10_000_000] * 4)
    # 4 processes on 4 cores — true parallelism ✓
```

### The Cost of Multiprocessing

```
Threads:    Shared memory → data passing is instant (same RAM)
Processes:  Separate memory → data must be serialised (pickled) to move between processes
```

```python
# This data is PICKLED and sent to each worker process via IPC (inter-process communication)
big_df = pd.DataFrame(...)   # 500MB
pool.map(process_chunk, [big_df] * 4)   # Sends 500MB × 4 = 2GB of pickle data!
# Very expensive — chunk the data FIRST, send small pieces
```

### ProcessPoolExecutor (Modern API)

```python
from concurrent.futures import ProcessPoolExecutor

def compute(n):
    return sum(range(n))

with ProcessPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(compute, [10**7, 10**7, 10**7, 10**7]))
```

### Shared State Between Processes

Since processes don't share memory, you need special objects:

```python
from multiprocessing import Process, Value, Array

shared_counter = Value('i', 0)   # Shared integer, initialized to 0

def increment(counter):
    for _ in range(1000):
        with counter.get_lock():   # Lock still needed!
            counter.value += 1
```

### When to Use Multiprocessing

- **CPU-bound tasks**: video encoding, data transformation, ML training
- **NumPy/Pandas heavy pipelines** — numpy releases GIL for many operations, but for pure Python loops, use multiprocessing
- **Embarrassingly parallel** problems: same operation on N independent chunks

---

## 4. Async IO

### Mental Model

> One chef with a timer. They start a dish, set a timer (I/O wait), then immediately start the next dish. When the timer goes off (I/O complete), they go back to finish the first dish. One person, many dishes "in progress" — no waiting around doing nothing.

### How It Works

`asyncio` uses an **event loop** — a single thread that manages many tasks. When a task hits a waiting point (`await`), control returns to the event loop, which starts or resumes another task.

**No new threads or processes** — one thread, cooperative multitasking.

```python
import asyncio
import httpx

async def fetch(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)    # ← Yields control here during the wait
        return resp.json()              # ← Resumes here when response arrives

async def main():
    urls = [f"https://api.example.com/{i}" for i in range(10)]
    tasks = [fetch(url) for url in urls]
    results = await asyncio.gather(*tasks)   # All 10 fire "simultaneously"
    return results

asyncio.run(main())
```

### Key Keywords

| Keyword | Meaning |
|---|---|
| `async def` | Declares a coroutine — a function that CAN be paused |
| `await` | Pauses this coroutine and yields to the event loop |
| `asyncio.gather()` | Run multiple coroutines concurrently, wait for all |
| `asyncio.run()` | Entry point — starts the event loop |

### The Golden Rule of Async

> **Never block the event loop.** One blocking call freezes everything.

```python
import asyncio
import time
import requests   # Synchronous — BLOCKS

async def bad():
    resp = requests.get("https://slow-api.com")   # ❌ Blocks event loop for 2s
    # Every other coroutine is frozen during this wait

async def good():
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://slow-api.com")   # ✓ Yields during wait
```

### Async vs Threads for I/O

```
Threads:  10,000 threads = 10,000 OS threads = heavy memory, OS scheduling overhead
Async:    10,000 coroutines = lightweight objects in one thread = tiny memory footprint
```

Async scales to **100,000+ concurrent connections**. Threads don't.

### When Async Wins

- **High-concurrency I/O**: web scrapers, API aggregators, chat servers
- **FastAPI endpoints** that call multiple downstream APIs
- **WebSockets**: maintaining thousands of live connections

### When Async Does NOT Help

```python
async def bad_cpu_work():
    await asyncio.sleep(0)          # Won't help
    result = sum(range(10_000_000)) # CPU-bound — still blocks the event loop
    return result
# async doesn't make CPU work concurrent — only I/O operations can yield
```

---

## 5. Concurrency vs Parallelism

### The Distinction

| Concept | Definition | Python Tool |
|---|---|---|
| **Concurrency** | Multiple tasks *in progress* at once (may not run simultaneously) | `threading`, `asyncio` |
| **Parallelism** | Multiple tasks *executing* simultaneously on multiple cores | `multiprocessing` |

```
Concurrency:   Task A ──wait──── Task A   (one lane, tasks interleaved)
               Task B ────── Task B

Parallelism:   Task A ──────────────────  (two lanes, truly simultaneous)
               Task B ──────────────────
```

### Simple Rule

```
I/O-bound + low concurrency  →  threading
I/O-bound + high concurrency →  asyncio
CPU-bound                    →  multiprocessing
```

---

## 6. How GIL Affects Concurrency

### Summary Table

| Workload | Threading | Multiprocessing | AsyncIO |
|---|---|---|---|
| I/O-bound (network, disk) | ✅ Works well | ✅ Works (overkill) | ✅ Best choice |
| CPU-bound (loops, math) | ❌ No speedup (GIL) | ✅ True parallelism | ❌ No help |
| High concurrency (10k+) | ❌ Too many threads | ❌ Too many processes | ✅ Designed for this |
| Shared state | ⚠️ Need locks | ❌ Separate memory | ✅ Single thread, safe |

### Why Threading Fails for CPU Work

```python
import threading, time

def count():
    total = 0
    for _ in range(50_000_000): total += 1

# Sequential
start = time.time()
count(); count()
print(f"Sequential: {time.time()-start:.2f}s")   # ~8s

# Threaded — you'd EXPECT ~4s on 2 cores
t1 = threading.Thread(target=count)
t2 = threading.Thread(target=count)
start = time.time()
t1.start(); t2.start()
t1.join();  t2.join()
print(f"Threaded: {time.time()-start:.2f}s")   # ~9s — SLOWER due to GIL switching overhead!
```

### Why Multiprocessing Wins for CPU Work

```python
from multiprocessing import Pool, cpu_count

def count(_):
    total = 0
    for _ in range(50_000_000): total += 1
    return total

if __name__ == "__main__":
    with Pool(processes=cpu_count()) as pool:
        pool.map(count, range(cpu_count()))
    # Each process has its own GIL — TRUE parallelism ✓
    # Time: ~8s / num_cores
```

### GIL and NumPy — The Exception

NumPy releases the GIL during C-level operations:

```python
import numpy as np
import threading

arr = np.random.rand(10_000_000)

def compute():
    _ = arr * 2 + arr   # NumPy's C layer releases GIL → threads CAN run in parallel!

t1 = threading.Thread(target=compute)
t2 = threading.Thread(target=compute)
# These genuinely run in parallel — NumPy's C extension releases the GIL
```

This is why `ThreadPoolExecutor` with NumPy can actually speed things up.

---

## 7. Ruff

### Mental Model

> Ruff is a single fast tool that replaces flake8 + isort + pyupgrade + black — all in one, written in Rust. 10–100x faster than any of those tools individually.

### What Is Ruff?

Ruff is a **Python linter AND formatter** written in Rust. It:
- Finds style issues and bugs (linting)
- Reformats code to a consistent style (formatting)
- Replaces: `flake8`, `isort`, `black`, `pyupgrade`, `bandit` rules, and more

### Why Ruff?

```
flake8 on large codebase:  ~10 seconds
ruff on same codebase:     ~0.1 seconds  (100x faster)
```

Ruff is now the default linter in many major Python projects (FastAPI, Pydantic, etc.)

### Basic Usage

```bash
# Install
pip install ruff

# Lint — check for issues
ruff check .

# Lint and auto-fix what it can
ruff check --fix .

# Format — like black
ruff format .

# Format check only (no changes, good for CI)
ruff format --check .
```

### Configuration — pyproject.toml

```toml
[tool.ruff]
line-length = 88          # Same as black's default
target-version = "py311"  # Minimum Python version to support

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes (unused imports, undefined names)
    "I",    # isort (import ordering)
    "UP",   # pyupgrade (modernise syntax: f-strings, typing updates)
    "B",    # flake8-bugbear (common bugs)
    "C4",   # flake8-comprehensions (better list/dict comprehensions)
]
ignore = [
    "E501",   # Line too long — let the formatter handle this
]

[tool.ruff.lint.isort]
known-first-party = ["myapp"]   # Treat as local imports for grouping
```

### What Ruff Catches

```python
# F401 — unused import
import os   # ← ruff flags this if os is never used

# E711 — comparison to None
if x == None:   # ← ruff fixes to: if x is None:

# UP006 — use built-in types for type hints (Python 3.9+)
from typing import List
def fn(x: List[int]):   # ← ruff upgrades to: def fn(x: list[int]):

# B006 — mutable default argument
def fn(items=[]):   # ← ruff flags this

# I001 — imports not sorted
import sys
import os     # ← ruff reorders: os before sys

# C416 — unnecessary list comprehension
result = list(x for x in items)   # ← ruff simplifies to: list(items)
```

### Ruff Format vs Black

Ruff format is intentionally **compatible with Black** — same output, faster.

```python
# Before ruff format
x={"key":"value","another":"thing","and":"more"}

# After ruff format (same as black would produce)
x = {
    "key": "value",
    "another": "thing",
    "and": "more",
}
```

### In a CI Pipeline

```yaml
# .github/workflows/lint.yml
- name: Lint and format check
  run: |
    pip install ruff
    ruff check .          # Fail CI if lint errors exist
    ruff format --check . # Fail CI if code isn't formatted
```

### Ruff vs Other Tools

| Tool | What Ruff Replaces |
|---|---|
| `flake8` | Style + error linting |
| `isort` | Import sorting |
| `black` | Code formatting |
| `pyupgrade` | Syntax modernisation |
| `bandit` | Security checks (subset) |
| `pydocstyle` | Docstring style |

---

## 8. Quick Decision Table

```
Problem you have                    →  Tool to reach for
────────────────────────────────────────────────────────
10 API calls, want them concurrent  →  asyncio / httpx
1000+ concurrent connections        →  asyncio
Heavy CPU computation               →  multiprocessing
I/O + low concurrency               →  threading
NumPy math on multiple cores        →  threading (NumPy releases GIL)
Lint + format the codebase          →  ruff check . && ruff format .
```

---

## 9. Interview Questions & Answers

---

### GIL Questions

---

**Q1. What is the GIL and why does CPython have it?**

**A:** The GIL (Global Interpreter Lock) is a mutex that allows only one thread to execute Python bytecode at a time. CPython uses reference counting for memory management — without the GIL, two threads could simultaneously modify an object's reference count, corrupting memory. The GIL makes CPython's object model thread-safe without per-object locks.

---

**Q2. Does the GIL mean Python can't do concurrent I/O with threads?**

**A:** No — the GIL is *released* during I/O operations (network calls, file reads, sleep). While Thread A waits for a network response, the GIL is released and Thread B can run Python code. So threading works well for I/O-bound work. The GIL only blocks concurrent *CPU-bound* Python execution.

---

**Q3. A colleague says "Python can't use multiple CPU cores." Is that accurate?**

**A:** Partially. CPython threads can't use multiple cores for CPU-bound Python code because the GIL serialises execution. But `multiprocessing` spawns separate processes — each with its own interpreter and GIL — achieving true multi-core parallelism. Also, C extensions like NumPy release the GIL, so NumPy operations on threads can run in parallel across cores.

---

**Q4. Will removing the GIL make Python faster?**

**A:** Not automatically. For single-threaded code (the majority of Python programs), removing the GIL would actually make it *slower* — you'd need fine-grained per-object locks instead, adding overhead. The GIL speeds up single-threaded execution at the cost of multi-threaded CPU parallelism. Python 3.13 has experimental free-threaded mode — the performance impact is still being measured.

---

### Multithreading Questions

---

**Q5. When would you use threading over asyncio?**

**A:** Use threading when:
1. You're integrating with a synchronous library that can't be made async (e.g. `requests`, `boto3` standard clients, legacy DB drivers)
2. The concurrency level is moderate (tens, not thousands of connections)
3. You want to parallelise NumPy/C-extension work (which releases the GIL)

Use asyncio when concurrency is high (thousands of connections) or your whole stack is async-native.

---

**Q6. What is a race condition? Give a concrete Python example.**

**A:** A race condition occurs when the result depends on the relative timing of two threads accessing shared data.

```python
counter = 0

def increment():
    global counter
    for _ in range(100_000):
        counter += 1   # Read, add, write — three steps, not atomic
                       # Thread 2 can interrupt between read and write

# Two threads: counter ends up at ~150k, not 200k
```

`counter += 1` compiles to three bytecode instructions. The GIL can switch threads between them. Fix with `threading.Lock()`.

---

**Q7. What does `thread.join()` do and why does it matter?**

**A:** `join()` blocks the calling thread until the target thread finishes. Without it, the main thread may exit before worker threads complete — either killing them mid-work or producing incomplete results. Always `join()` threads you spawn unless you deliberately want daemon threads.

---

**Q8. What is a daemon thread?**

**A:** A daemon thread is automatically killed when the main thread exits, regardless of whether it finished. Non-daemon threads keep the process alive until they complete.

```python
t = threading.Thread(target=background_job, daemon=True)
t.start()
# Main thread exits → t is killed immediately, no join() needed
```

Use for background cleanup jobs that shouldn't delay program shutdown.

---

### Multiprocessing Questions

---

**Q9. Why must the multiprocessing entry point be inside `if __name__ == "__main__"`?**

**A:** On Windows and macOS, Python spawns new processes by importing the main module. Without the guard, each new process would import the module and re-execute the process-spawning code — creating infinite recursive process creation (a fork bomb). The guard ensures spawning code only runs in the original process.

---

**Q10. What gets copied when you spawn a new process? What's the performance implication?**

**A:** On Unix (`fork`): the entire parent process memory is copy-on-write duplicated — fast, but large parent memory = large child. On Windows/macOS (`spawn`): a fresh Python interpreter starts and the target function + its arguments are *pickled* and sent via IPC. The implication: large arguments (big DataFrames, models) are expensive to pass. Always pass small arguments; let workers load large data themselves.

---

**Q11. How do two processes share data?**

**A:** Three options:
1. **`multiprocessing.Queue`** — safe message passing between processes
2. **`multiprocessing.Value` / `Array`** — shared memory for simple types, with explicit locks
3. **`multiprocessing.Manager`** — proxy objects (list, dict) backed by a server process; slowest but most flexible

For most cases, design processes to work on independent chunks and return results — avoiding shared state entirely.

---

**Q12. ProcessPoolExecutor vs Pool — which should you use?**

**A:** `ProcessPoolExecutor` from `concurrent.futures` is the modern API. It has a cleaner interface, integrates with `Future` objects, and handles exceptions better. `multiprocessing.Pool` is older but has `starmap` and `imap_unordered` which are occasionally more convenient. For new code, prefer `ProcessPoolExecutor`.

---

### Async IO Questions

---

**Q13. What is a coroutine? How is it different from a regular function?**

**A:** A coroutine is a function defined with `async def` that can pause its execution at `await` points and yield control back to the event loop. A regular function runs to completion without pausing. Coroutines are lightweight — you can have 100,000 of them; threads would crash the OS at that scale.

---

**Q14. What happens if you call an `async def` function without `await`?**

**A:** You get a coroutine *object* — the function body doesn't execute at all. Python also raises a `RuntimeWarning: coroutine 'fn' was never awaited`. You must `await` it or pass it to `asyncio.gather()` / `asyncio.run()` to actually execute it.

```python
async def greet(): return "hello"

result = greet()       # ← Returns coroutine object, prints warning, body NOT run
result = await greet() # ← Runs the body, returns "hello"
```

---

**Q15. What's the difference between `asyncio.gather()` and `asyncio.wait()`?**

**A:**
- `gather(*tasks)` — runs all coroutines concurrently, returns results in the *same order as input*, raises exceptions immediately (fails fast)
- `wait(tasks)` — returns two sets: `done` and `pending`, lets you handle each result or exception individually as they complete; more control, more verbose

Use `gather` for "run all, get all results". Use `wait` when you need to handle partial completions or mixed success/failure.

---

**Q16. You have an async FastAPI endpoint but it calls `requests.get()` inside. What happens?**

**A:** The entire asyncio event loop freezes for the duration of the HTTP call. No other request can be processed until it returns. Fix options:
1. Replace `requests` with `httpx.AsyncClient` and `await` it
2. Change the endpoint to a regular `def` — FastAPI runs sync endpoints in a thread pool, keeping the event loop free
3. Use `asyncio.run_in_executor()` to offload the blocking call to a thread pool

---

**Q17. Can async IO help with CPU-bound tasks?**

**A:** No. `async/await` only helps when the bottleneck is *waiting* — network, disk, sleep. For CPU-bound work, the event loop is still a single thread. `await asyncio.sleep(0)` yields to the loop but doesn't run anything in parallel. Use `multiprocessing` or `run_in_executor` with a `ProcessPoolExecutor` for CPU-bound async code.

---

### Concurrency & Comparison Questions

---

**Q18. Explain concurrency vs parallelism with a Python-specific example.**

**A:**
- **Concurrency**: tasks are in progress at the same time but may not run simultaneously. `asyncio` with 100 HTTP requests — one thread, 100 coroutines switching at `await` points. Interleaved, not simultaneous.
- **Parallelism**: tasks run at the *exact same instant* on different CPU cores. `multiprocessing.Pool` with 4 workers on 4 cores — 4 Python interpreters running at the same time.

Threading sits in the middle: concurrent (interleaved) for Python code, but can be genuinely parallel for C extension code (NumPy, I/O) that releases the GIL.

---

**Q19. You need to process 1 million rows of data through a heavy Python function. Which concurrency model do you choose?**

**A:** `multiprocessing`. The work is CPU-bound Python — threading won't help (GIL), asyncio won't help (not I/O). Split the data into chunks, one per CPU core, and process in parallel:

```python
from multiprocessing import Pool, cpu_count
import numpy as np

def process_chunk(chunk): return [heavy_fn(row) for row in chunk]

data = list(range(1_000_000))
chunks = np.array_split(data, cpu_count())   # Split evenly

with Pool() as pool:
    results = pool.map(process_chunk, chunks)
```

---

**Q20. What is the `concurrent.futures` module and why is it preferred over `threading`/`multiprocessing` directly?**

**A:** `concurrent.futures` provides `ThreadPoolExecutor` and `ProcessPoolExecutor` — a unified high-level API for both. Benefits:
- Returns `Future` objects — easier result/exception handling
- `pool.map()` and `pool.submit()` are cleaner than manually managing threads/processes
- Automatically manages pool lifecycle with context manager
- Switching from threads to processes is one word change: `ThreadPoolExecutor` → `ProcessPoolExecutor`

---

### Ruff Questions

---

**Q21. What does Ruff do and what tools does it replace?**

**A:** Ruff is a fast Python linter and formatter written in Rust. It replaces `flake8` (linting), `isort` (import sorting), `black` (formatting), and `pyupgrade` (syntax modernisation) — all in one tool, 10–100x faster than any of them individually. It's now the default linter in FastAPI and Pydantic.

---

**Q22. What's the difference between `ruff check` and `ruff format`?**

**A:**
- `ruff check` — **linting**: finds logical errors, style violations, unused imports, buggy patterns. Reports issues, optionally auto-fixes some with `--fix`
- `ruff format` — **formatting**: rewrites code layout (indentation, line breaks, quotes) to a consistent style. Like `black`. Doesn't check logic, just aesthetics

Both should be in CI: `ruff check .` fails if there are lint errors; `ruff format --check .` fails if any file isn't formatted.

---

**Q23. What is the `select` key in Ruff config and name four useful rule sets.**

**A:** `select` specifies which rule categories Ruff enforces. Useful ones:
- `"E"` / `"W"` — pycodestyle errors and warnings (spacing, indentation)
- `"F"` — pyflakes: unused imports, undefined variables
- `"I"` — isort: import ordering
- `"B"` — flake8-bugbear: common subtle bugs (mutable defaults, useless comparisons)
- `"UP"` — pyupgrade: modernise syntax (use `list[int]` instead of `List[int]`)
- `"C4"` — better comprehension patterns

---

**Q24. You're reviewing a PR and the CI shows `ruff format --check` failing but `ruff check` passing. What does that mean?**

**A:** The code has no logical errors or style violations (`ruff check` passes), but the code *layout* doesn't match Ruff's format standard — things like inconsistent indentation, trailing commas, line breaks, or quote style (`ruff format` would change it). The developer just needs to run `ruff format .` locally and push again. It's a cosmetic issue, not a logic issue.

---

**Q25. How would you add Ruff to a new FastAPI project from scratch?**

**A:**

```bash
pip install ruff
```

`pyproject.toml`:
```toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "UP", "C4"]
ignore = ["E501"]

[tool.ruff.lint.isort]
known-first-party = ["app"]
```

`pre-commit` hook (`.pre-commit-config.yaml`):
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

CI step: `ruff check . && ruff format --check .`

---

### Tricky / Critical Thinking Questions

---

**Q26. Threading increases CPU usage when running I/O-bound code. Why?**

**A:** With multiple threads doing I/O concurrently, all their responses can arrive and all their post-I/O processing (parsing, transforming) can happen in an overlapping window. Each thread uses CPU during its processing phase. The total CPU work is the same as sequential — but it's packed into a shorter wall-clock window because threads are not idle waiting for I/O. The apparent CPU increase is utilisation improvement, not extra work.

---

**Q27. Can asyncio and multiprocessing work together? Give a use case.**

**A:** Yes — and this is the production pattern for FastAPI + ML inference.

```python
import asyncio
from concurrent.futures import ProcessPoolExecutor

executor = ProcessPoolExecutor(max_workers=4)

async def run_model(data):
    loop = asyncio.get_event_loop()
    # Offload CPU-heavy model inference to a process pool
    # while the async event loop stays free to handle other requests
    result = await loop.run_in_executor(executor, model.predict, data)
    return result
```

The event loop handles hundreds of concurrent HTTP requests (async I/O). Heavy inference is offloaded to processes (CPU parallelism). Best of both worlds.

---

**Q28. A FastAPI app handles 500 requests/second normally. You add a 2-second `time.sleep(2)` inside an `async def` endpoint. What happens?**

**A:** Total collapse. `time.sleep()` is a blocking call — it holds the event loop frozen for 2 seconds. During those 2 seconds, zero other requests are processed. At 500 req/s, ~1000 requests queue up behind each sleep. The server appears to hang.

Fix:
```python
# ❌ Blocks event loop
async def endpoint():
    time.sleep(2)

# ✅ Yields to event loop
async def endpoint():
    await asyncio.sleep(2)   # Other coroutines run during this wait
```

`asyncio.sleep()` is the async-safe version — it yields control while waiting.

---

*End of guide. Total: 28 questions across GIL, threading, multiprocessing, asyncio, concurrency, and Ruff.*
