# Python Interview Prep — Set 3 (Gap Filler)
### True 0-2 Years Level | Most Likely to Appear in Intern Interviews

> **These are the questions interviewers ask to warm you up or check fundamentals.**
> If you can answer these cleanly — you already look better than 60% of candidates.
> Simple questions answered confidently > complex questions answered shakily.

---

## MODULE 1 — Core Basics & Data Types

---

### Q1. Sets vs Dictionaries vs Lists — When to use which?

**What they're testing:** Data structure decision-making — very common warm-up.

```python
# LIST — ordered, allows duplicates, use when sequence matters
fruits = ["apple", "banana", "apple", "cherry"]
print(fruits[0])       # "apple" — indexing works
print(len(fruits))     # 4 — duplicates counted

# SET — unordered, NO duplicates, use when uniqueness matters
unique_fruits = {"apple", "banana", "cherry"}
unique_fruits.add("apple")     # ignored — already exists
print(unique_fruits)           # {'apple', 'banana', 'cherry'} — still 3
# print(unique_fruits[0])      # TypeError! — sets have no index

# DICTIONARY — key-value pairs, use when you need lookup by name
student = {"name": "Alice", "age": 25, "score": 88}
print(student["name"])         # "Alice" — lookup by key
print(student.get("grade", "N/A"))  # "N/A" — safe get with default


# --- Common Set operations (very useful) ---
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

print(a & b)    # {3, 4}        — intersection (common elements)
print(a | b)    # {1,2,3,4,5,6} — union (all elements)
print(a - b)    # {1, 2}        — difference (in a but not b)
print(a ^ b)    # {1,2,5,6}     — symmetric diff (not in both)


# Real use case — remove duplicates from a list:
data = [1, 2, 2, 3, 3, 3, 4]
unique = list(set(data))   # [1, 2, 3, 4] — fast dedup
```

**Decision table:**
```
Need order + duplicates    → List
Need uniqueness            → Set
Need key-value lookup      → Dictionary
Need fast "is X in it?"   → Set (O(1) vs List O(n))
```

---

### Q2. String Formatting — f-string vs `.format()` vs `%`

**What they're testing:** Pythonic string usage — you'll write this on paper.**

```python
name = "Alice"
score = 95.678
rank = 1

# Old way — % formatting (Python 2 style, avoid in new code)
print("Name: %s, Score: %.2f" % (name, score))
# "Name: Alice, Score: 95.68"

# Better way — .format() (Python 3, still common)
print("Name: {}, Score: {:.2f}".format(name, score))
print("Name: {n}, Rank: {r}".format(n=name, r=rank))  # named args

# Best way — f-strings (Python 3.6+, fastest, most readable)
print(f"Name: {name}, Score: {score:.2f}")
print(f"Rank: {rank}, Is topper: {rank == 1}")   # expressions inside!
print(f"Score rounded: {score:.0f}")              # 96
print(f"Name upper: {name.upper()}")              # ALICE


# Format specifiers (write these on paper):
pi = 3.14159
print(f"{pi:.2f}")      # "3.14"      — 2 decimal places
print(f"{pi:.0f}")      # "3"         — 0 decimal places
print(f"{1000000:,}")   # "1,000,000" — comma separator
print(f"{0.25:.0%}")    # "25%"       — percentage
print(f"{'hi':>10}")    # "        hi"— right align in 10 chars
print(f"{'hi':<10}")    # "hi        "— left align in 10 chars
```

---

### Q3. `enumerate()` and `zip()` — Write the output. (Very common on paper)

**What they're testing:** Looping patterns — almost guaranteed in interviews.**

```python
# enumerate() — gives you index + value together
fruits = ["apple", "banana", "cherry"]

for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")
# 0: apple
# 1: banana
# 2: cherry

# Start from 1 instead of 0:
for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")
# 1. apple
# 2. banana
# 3. cherry

# Without enumerate (ugly way — don't do this):
for i in range(len(fruits)):
    print(f"{i}: {fruits[i]}")     # works but not Pythonic


# zip() — combines two lists element by element
names  = ["Alice", "Bob", "Carol"]
scores = [88, 92, 75]

for name, score in zip(names, scores):
    print(f"{name} scored {score}")
# Alice scored 88
# Bob scored 92
# Carol scored 75

# zip stops at shortest list:
a = [1, 2, 3, 4]
b = ["x", "y"]
print(list(zip(a, b)))   # [(1,'x'), (2,'y')] — stops at length 2

# Unzip (reverse of zip):
pairs = [("Alice", 88), ("Bob", 92)]
names, scores = zip(*pairs)    # * unpacks the list
print(names)    # ("Alice", "Bob")
print(scores)   # (88, 92)
```

---

### Q4. Dictionary Comprehension + Set Comprehension (Write on paper)

**What they're testing:** Comprehension family — list comp's cousins.**

```python
# Dictionary Comprehension — {key: value for item in iterable}
names  = ["Alice", "Bob", "Carol"]
scores = [88, 92, 75]

# Pair names with scores
score_dict = {name: score for name, score in zip(names, scores)}
print(score_dict)   # {'Alice': 88, 'Bob': 92, 'Carol': 75}

# Squares dictionary
squares = {n: n**2 for n in range(1, 6)}
print(squares)      # {1:1, 2:4, 3:9, 4:16, 5:25}

# With condition — only even squares
even_squares = {n: n**2 for n in range(1, 11) if n % 2 == 0}
print(even_squares)  # {2:4, 4:16, 6:36, 8:64, 10:100}

# Flip keys and values
original = {"a": 1, "b": 2, "c": 3}
flipped  = {v: k for k, v in original.items()}
print(flipped)       # {1:'a', 2:'b', 3:'c'}


# Set Comprehension — {expr for item in iterable}
data = [1, 2, 2, 3, 3, 3, 4]
unique_squares = {x**2 for x in data}
print(unique_squares)   # {1, 4, 9, 16} — no duplicates, unordered


# Generator Expression — (expr for item) — lazy, no brackets stored
gen = (x**2 for x in range(1000000))   # creates NO list — memory efficient
print(next(gen))   # 0 — compute one at a time
print(next(gen))   # 1
```

---

### Q5. `sorted()` with `key` parameter — Write these outputs.

**What they're testing:** Sorting custom objects — common in data tasks.**

```python
# Basic sort
nums = [3, 1, 4, 1, 5, 9, 2, 6]
print(sorted(nums))              # [1, 1, 2, 3, 4, 5, 6, 9] — ascending
print(sorted(nums, reverse=True)) # [9, 6, 5, 4, 3, 2, 1, 1] — descending


# Sort strings by length
words = ["banana", "fig", "apple", "kiwi", "watermelon"]
print(sorted(words, key=len))
# ['fig', 'kiwi', 'apple', 'banana', 'watermelon']


# Sort list of dicts by a field
students = [
    {"name": "Alice", "score": 88},
    {"name": "Bob",   "score": 95},
    {"name": "Carol", "score": 72}
]

by_score = sorted(students, key=lambda s: s["score"], reverse=True)
for s in by_score:
    print(s["name"], s["score"])
# Bob   95
# Alice 88
# Carol 72


# Sort by multiple keys — primary: dept, secondary: score descending
employees = [
    {"name": "Alice", "dept": "ML",   "score": 88},
    {"name": "Bob",   "dept": "Data", "score": 95},
    {"name": "Carol", "dept": "ML",   "score": 92},
    {"name": "Dave",  "dept": "Data", "score": 80},
]

sorted_emp = sorted(employees, key=lambda e: (e["dept"], -e["score"]))
for e in sorted_emp:
    print(e["dept"], e["name"], e["score"])
# Data  Bob   95
# Data  Dave  80
# ML    Carol 92
# ML    Alice 88
```

---

### Q6. Python Keywords — What do these do? (1 Question, Multiple Keywords)

**What they're testing:** Language awareness — common quick-fire round.**

```python
# THESE ARE PYTHON KEYWORDS — reserved words, can't use as variable names

# --- pass ---
# Does absolutely nothing — placeholder when syntax needs a body
class EmptyClass:
    pass          # valid! without pass, IndentationError

def todo_function():
    pass          # "I'll implement this later"


# --- break and continue ---
for i in range(10):
    if i == 3:
        continue    # skip rest of THIS iteration, go to next
    if i == 6:
        break       # EXIT the loop entirely
    print(i)
# prints: 0, 1, 2, 4, 5  (3 skipped, stops before 6)


# --- yield ---
def counter(n):
    for i in range(n):
        yield i       # pause here, send i, resume on next()

gen = counter(3)
print(next(gen))  # 0
print(next(gen))  # 1


# --- assert ---
def divide(a, b):
    assert b != 0, "b cannot be zero!"   # crash with message if False
    return a / b

divide(10, 2)   # works
divide(10, 0)   # AssertionError: b cannot be zero!


# --- del ---
my_list = [1, 2, 3, 4]
del my_list[1]       # removes index 1
print(my_list)       # [1, 3, 4]

my_dict = {"a": 1, "b": 2}
del my_dict["a"]     # removes key "a"
print(my_dict)       # {"b": 2}


# --- in and not in ---
fruits = ["apple", "banana", "cherry"]
print("apple" in fruits)       # True
print("grape" not in fruits)   # True


# --- global and nonlocal ---
count = 0

def increment():
    global count        # access + modify outer global variable
    count += 1

def outer():
    x = 10
    def inner():
        nonlocal x      # access + modify enclosing function's variable
        x += 1
    inner()
    print(x)            # 11
```

---

### Q7. Lambda — Why does it exist when we already have `def`?

**This is your special question — most candidates can't explain this clearly.**

**What they're testing:** Conceptual depth — not just "lambda is anonymous function."

```python
# def — named, reusable, multi-line, lives in memory with a name
def square(x):
    return x ** 2

result = square(5)    # call it by name anytime
print(square)         # <function square at 0x...> — has a name


# lambda — anonymous, single expression, throwaway, no name stored
sq = lambda x: x ** 2
print(sq(5))          # 25 — works same way
print(sq)             # <function <lambda> at 0x...> — name is <lambda>
```

**The real reason lambda exists — it's designed for ONE specific job:**

```python
# When you need a function FOR JUST ONE MOMENT and don't want to def it

# Without lambda — you have to def a whole function just to use once
def get_score(student):
    return student["score"]

students = [{"name": "Alice", "score": 88}, {"name": "Bob", "score": 95}]
sorted_students = sorted(students, key=get_score)  # used once, never again


# With lambda — inline, no name needed, no pollution of namespace
sorted_students = sorted(students, key=lambda s: s["score"])  # clean!


# Other common places lambda shines:
nums = [1, 2, 3, 4, 5, 6]

# filter() — keep only evens
evens = list(filter(lambda x: x % 2 == 0, nums))
print(evens)   # [2, 4, 6]

# map() — apply to every element
doubled = list(map(lambda x: x * 2, nums))
print(doubled) # [2, 4, 6, 8, 10, 12]


# Why CAN'T lambda replace def?
# 1. lambda = only ONE expression — no if/elif/else blocks, no loops
# 2. lambda = no docstring — can't document it
# 3. lambda = hard to debug — traceback shows <lambda>, not a name
# 4. lambda = not reusable by name in other parts of code

# This is IMPOSSIBLE in lambda:
def process(x):
    if x > 0:
        result = x * 2
        return result
    else:
        return 0
# Can't write multi-step logic in lambda — that's by design


# BUILT-IN vs USER-DEFINED — the key distinction:
# Built-in functions: print(), len(), sorted(), map(), filter(), zip()
#   → written in C, optimized, always available, no import needed
#   → Python provides these as part of the language itself

# User-defined: def square(x) or lambda x: x**2
#   → written by YOU in Python
#   → exists only when your code runs

# lambda is USER-DEFINED — it's not a built-in
# It's a built-in KEYWORD (reserved word), but functions made with it are user-defined

# Proof:
import builtins
print(dir(builtins))    # you'll see: print, len, sorted... but NOT lambda
                        # lambda is syntax, not a built-in function
```

**How to say this in interview:**
> *"Lambda exists for throwaway, single-use functions — mainly when passing a function as an argument to another function like sorted(), map(), or filter(). def is for anything reusable or complex. Lambda can't replace def because it's limited to one expression — that's intentional, not a limitation."*

---

### Q8. `map()` and `filter()` — Write with and without lambda

**What they're testing:** Functional programming basics — often paired with lambda.**

```python
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


# --- map() — apply a function to EVERY element ---
# Returns a map object (lazy) — wrap in list() to see results

# With lambda:
squares = list(map(lambda x: x**2, nums))
print(squares)   # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

# With def:
def square(x): return x**2
squares = list(map(square, nums))   # same result

# Modern Pythonic way — list comprehension (often preferred):
squares = [x**2 for x in nums]     # most readable


# --- filter() — keep elements where function returns True ---

# With lambda:
evens = list(filter(lambda x: x % 2 == 0, nums))
print(evens)   # [2, 4, 6, 8, 10]

# With list comprehension (preferred):
evens = [x for x in nums if x % 2 == 0]


# --- Combining map + filter ---
# Square of even numbers only:
result = list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, nums)))
print(result)   # [4, 16, 36, 64, 100]

# Cleaner with comprehension:
result = [x**2 for x in nums if x % 2 == 0]   # same, more readable


# --- map() on strings ---
names = ["alice", "BOB", "  carol  "]
cleaned = list(map(str.strip, names))          # strip spaces
print(cleaned)   # ["alice", "BOB", "carol"]

titled = list(map(str.title, cleaned))
print(titled)    # ["Alice", "Bob", "Carol"]
```

---

## MODULE 4 — NumPy Gaps

---

### Q9. NumPy `where()`, `argmax()`, `argmin()` — Write code on paper

**What they're testing:** Conditional selection + finding extremes — core ML ops.**

```python
import numpy as np

arr = np.array([10, 25, 3, 47, 8, 30, 15])


# --- argmax() / argmin() — INDEX of max/min value ---
print(np.argmax(arr))    # 3  — index 3 has value 47 (max)
print(np.argmin(arr))    # 2  — index 2 has value 3 (min)

print(arr[np.argmax(arr)])   # 47 — the actual max value
# same as: np.max(arr)


# In 2D — specify axis
matrix = np.array([[1, 9, 2],
                   [8, 3, 7]])

print(np.argmax(matrix, axis=0))   # [1, 0, 1] — which ROW has max per column
print(np.argmax(matrix, axis=1))   # [1, 0]    — which COL has max per row


# --- where() — conditional element selection ---
# np.where(condition, value_if_true, value_if_false)

arr = np.array([10, 25, 3, 47, 8, 30])

# Replace values — if >20 keep value, else replace with 0
result = np.where(arr > 20, arr, 0)
print(result)   # [ 0 25  0 47  0 30]

# Binary label — like ML target encoding
labels = np.where(arr > 20, "High", "Low")
print(labels)   # ['Low' 'High' 'Low' 'High' 'Low' 'High']

# Just get indices where condition is True (1 argument version):
indices = np.where(arr > 20)
print(indices)       # (array([1, 3, 5]),) — tuple of arrays
print(arr[indices])  # [25, 47, 30] — values at those indices
# Same as: arr[arr > 20]
```

---

### Q10. NumPy — `stack()`, `concatenate()`, `split()` (Array joining and splitting)

**What they're testing:** Combining arrays — you'll need this in ML data prep.**

```python
import numpy as np

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])


# --- concatenate() — join along EXISTING axis ---
print(np.concatenate([a, b]))          # [1 2 3 4 5 6] — flat join

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

print(np.concatenate([A, B], axis=0))  # stack rows (add rows)
# [[1,2],[3,4],[5,6],[7,8]]

print(np.concatenate([A, B], axis=1))  # stack columns (add columns)
# [[1,2,5,6],[3,4,7,8]]


# --- stack() — join along NEW axis ---
print(np.stack([a, b]))          # [[1,2,3],[4,5,6]] — new row axis
print(np.stack([a, b], axis=1))  # [[1,4],[2,5],[3,6]] — new col axis


# --- split() — divide array into parts ---
arr = np.array([1, 2, 3, 4, 5, 6])

parts = np.split(arr, 3)              # split into 3 equal parts
print(parts)   # [array([1,2]), array([3,4]), array([5,6])]

# ML use case: split dataset into train/val/test
data = np.arange(100)
train, val, test = np.split(data, [70, 85])  # 70%, 15%, 15%
print(len(train), len(val), len(test))  # 70, 15, 15
```

---

## MODULE 4 — Pandas Gaps

---

### Q11. `value_counts()`, `nunique()`, `unique()` — Exploratory Data Analysis

**What they're testing:** EDA basics — first things you do on a real dataset.**

```python
import pandas as pd

df = pd.DataFrame({
    "dept":   ["ML", "Data", "ML", "ML", "Data", "ML", "DevOps"],
    "grade":  ["A", "B", "A", "C", "B", "A", "B"],
    "salary": [90000, 70000, 85000, 60000, 75000, 92000, 80000]
})


# --- value_counts() — frequency of each unique value ---
print(df["dept"].value_counts())
# ML       4
# Data     2
# DevOps   1

# As percentage:
print(df["dept"].value_counts(normalize=True).round(2))
# ML       0.57
# Data     0.29
# DevOps   0.14


# --- unique() — what are the unique values ---
print(df["dept"].unique())      # ['ML' 'Data' 'DevOps'] — array of unique values
print(df["grade"].unique())     # ['A' 'B' 'C']


# --- nunique() — HOW MANY unique values ---
print(df["dept"].nunique())     # 3 — number of unique depts
print(df.nunique())             # nunique for every column at once
# dept      3
# grade     3
# salary    7


# Together in EDA workflow:
for col in df.columns:
    print(f"{col}: {df[col].nunique()} unique | {df[col].dtype}")
```

---

### Q12. `pd.crosstab()` — What it is and when to use it

**What they're testing:** Cross-tabulation — shows data relationship awareness.**

```python
import pandas as pd

df = pd.DataFrame({
    "dept":    ["ML","ML","Data","Data","ML","Data","ML"],
    "grade":   ["A","B","A","B","A","C","B"],
    "passed":  [True,True,True,False,True,False,True]
})


# crosstab — count frequency of two categorical columns together
ct = pd.crosstab(df["dept"], df["grade"])
print(ct)
# grade   A  B  C
# dept
# Data    1  1  1
# ML      2  2  0

# With percentages (normalize):
ct_pct = pd.crosstab(df["dept"], df["grade"], normalize="index").round(2)
print(ct_pct)
# grade      A     B     C
# dept
# Data    0.33  0.33  0.33
# ML      0.50  0.50  0.00


# crosstab with values + aggfunc (like pivot_table):
ct_val = pd.crosstab(
    index=df["dept"],
    columns=df["grade"],
    values=df["passed"],
    aggfunc="sum"
)
print(ct_val)


# When to use:
# crosstab    → quick frequency table of 2 categorical columns, minimal code
# pivot_table → more flexible, custom aggregation, multiple values
```

---

### Q13. Pandas — `merge()` types written on paper (SQL JOIN equivalent)

**What they're testing:** Joining DataFrames — essential for real data work.**

```python
import pandas as pd

employees = pd.DataFrame({
    "emp_id": [1, 2, 3, 4],
    "name":   ["Alice", "Bob", "Carol", "Dave"]
})

salaries = pd.DataFrame({
    "emp_id": [1, 2, 5],      # note: 3,4 missing; 5 is extra
    "salary": [90000, 80000, 70000]
})

# Visual:
# employees: 1,2,3,4    salaries: 1,2,5

# INNER JOIN — only rows that match in BOTH
inner = pd.merge(employees, salaries, on="emp_id", how="inner")
print(inner)
#   emp_id   name  salary
# 0      1  Alice   90000
# 1      2    Bob   80000
# Result: only 1 and 2 (matched in both)

# LEFT JOIN — all from LEFT, matched from right (NaN if no match)
left = pd.merge(employees, salaries, on="emp_id", how="left")
print(left)
#   emp_id   name    salary
# 0      1  Alice   90000.0
# 1      2    Bob   80000.0
# 2      3  Carol       NaN   ← Carol has no salary entry
# 3      4   Dave       NaN   ← Dave has no salary entry

# RIGHT JOIN — all from RIGHT, matched from left
right = pd.merge(employees, salaries, on="emp_id", how="right")
print(right)
#   emp_id   name  salary
# 0      1  Alice   90000
# 1      2    Bob   80000
# 2      5    NaN   70000  ← emp_id 5 not in employees

# OUTER JOIN — ALL rows from both, NaN where no match
outer = pd.merge(employees, salaries, on="emp_id", how="outer")
```

**Memory trick:**
```
inner  → intersection   — only what BOTH have
left   → all left       + matching right
right  → all right      + matching left
outer  → union          — everything from both
```

---

### Q14. Pandas — `concat()` vs `merge()` — What's the difference?

**What they're testing:** Two ways to combine DataFrames — candidates confuse these.**

```python
import pandas as pd

df1 = pd.DataFrame({"name": ["Alice", "Bob"], "score": [88, 92]})
df2 = pd.DataFrame({"name": ["Carol", "Dave"], "score": [75, 95]})
df3 = pd.DataFrame({"grade": ["A", "B"], "rank": [1, 2]})


# --- concat() — STACK DataFrames (add rows or columns) ---
# Use when: same columns, want to combine row-wise (like vstack)

# Stack rows (axis=0, default):
stacked = pd.concat([df1, df2], ignore_index=True)
print(stacked)
#     name  score
# 0  Alice     88
# 1    Bob     92
# 2  Carol     75
# 3   Dave     95

# Stack columns (axis=1):
side_by_side = pd.concat([df1, df3], axis=1)
print(side_by_side)
#     name  score grade  rank
# 0  Alice     88     A     1
# 1    Bob     92     B     2


# --- merge() — JOIN DataFrames on a KEY column ---
# Use when: different info about the SAME entities, join by ID/key

scores = pd.DataFrame({"name": ["Alice","Bob"], "score": [88, 92]})
details = pd.DataFrame({"name": ["Alice","Bob"], "dept": ["ML","Data"]})

merged = pd.merge(scores, details, on="name")
print(merged)
#     name  score  dept
# 0  Alice     88    ML
# 1    Bob     92  Data


# Decision rule:
# concat → combining SAME structure (more rows or more columns)
# merge  → combining DIFFERENT info about SAME entities (join on key)
```

---

### Q15. Pandas — Write `iloc` operations on paper (Practice set)

**What they're testing:** iloc under pressure — write output without running code.**

```python
import pandas as pd

df = pd.DataFrame({
    "name":   ["Alice", "Bob", "Carol", "Dave", "Eve"],
    "age":    [25, 30, 22, 35, 28],
    "score":  [88, 92, 75, 95, 80],
    "dept":   ["ML", "Data", "ML", "Data", "ML"]
})

#      name  age  score  dept
# 0   Alice   25     88    ML
# 1     Bob   30     92  Data
# 2   Carol   22     75    ML
# 3    Dave   35     95  Data
# 4     Eve   28     80    ML


# Write the output for each (cover paper and try first!):

print(df.iloc[0])
# name     Alice
# age         25
# score       88
# dept        ML

print(df.iloc[2, 2])
# 75  — row at position 2 (Carol), column at position 2 (score)

print(df.iloc[1:4])
# rows at position 1,2,3 (Bob, Carol, Dave) — position 4 excluded

print(df.iloc[:, 1])
# all rows, column at position 1 (age): [25, 30, 22, 35, 28]

print(df.iloc[0:3, 0:2])
# rows 0-2, cols 0-1 (name + age for Alice, Bob, Carol)
#     name  age
# 0  Alice   25
# 1    Bob   30
# 2  Carol   22

print(df.iloc[-1])
# Last row — Eve's data

print(df.iloc[[0, 2, 4]])
# rows at positions 0,2,4 — Alice, Carol, Eve

print(df.iloc[::2])
# every 2nd row — Alice(0), Carol(2), Eve(4)
```

---

### Q16. Basic `pytest` — Write a test for a given function

**What they're testing:** Can you write tests? Shows engineering awareness.**

```python
# The function you need to test:
def calculate_bmi(weight_kg, height_m):
    """
    Calculate BMI given weight in kg and height in meters.
    BMI = weight / height^2
    Raises ValueError if inputs are non-positive.
    """
    if weight_kg <= 0 or height_m <= 0:
        raise ValueError("Weight and height must be positive")
    return round(weight_kg / (height_m ** 2), 2)


# Test file: test_bmi.py
import pytest

# Test 1: Happy path — normal input
def test_bmi_normal():
    result = calculate_bmi(70, 1.75)
    assert result == 22.86         # 70 / 1.75^2 = 22.857... rounded to 22.86

# Test 2: Boundary — very low valid weight
def test_bmi_low_weight():
    result = calculate_bmi(30, 1.60)
    assert isinstance(result, float)   # just check it returns a number

# Test 3: Edge — zero weight should raise error
def test_zero_weight_raises():
    with pytest.raises(ValueError):
        calculate_bmi(0, 1.75)

# Test 4: Edge — negative height should raise error
def test_negative_height_raises():
    with pytest.raises(ValueError):
        calculate_bmi(70, -1.75)

# Test 5: Return type check
def test_returns_float():
    assert isinstance(calculate_bmi(70, 1.75), float)


# Run all tests:  pytest test_bmi.py -v
# Output:
# test_bmi_normal         PASSED
# test_bmi_low_weight     PASSED
# test_zero_weight_raises PASSED
# test_negative_height_raises PASSED
# test_returns_float      PASSED
```

**Interview phrase:** *"I write tests for happy path, error cases, and boundary values — those three together catch most real bugs."*

---

## Quick Rescue Phrases — Set 3

| If asked about... | Anchor phrase |
|---|---|
| Set vs List | *"Set when I need uniqueness or fast lookup, List when order matters"* |
| f-string format | *"f'{value:.2f}' for 2 decimal places — I use f-strings in all new code"* |
| enumerate vs range(len) | *"enumerate is the Pythonic way — gives index and value together"* |
| lambda vs def | *"Lambda for throwaway single-expression functions — like inside sorted() or map()"* |
| map vs list comp | *"Both work — list comprehension is usually more readable in Python"* |
| iloc vs loc | *"iloc by integer position, loc by label — iloc end excluded, loc end included"* |
| concat vs merge | *"concat stacks same-structure DataFrames, merge joins on a key like SQL"* |
| value_counts | *"First thing I run on a categorical column to see distribution"* |
| pytest | *"Happy path, error case, boundary — three types of tests cover most scenarios"* |

---

## Full Cheat Sheet — Set 3

| Topic | One-liner |
|---|---|
| Set operations | `&` intersect, `\|` union, `-` difference, `^` symmetric diff |
| f-string decimal | `f"{val:.2f}"` → 2 decimal places |
| enumerate | `for i, val in enumerate(lst, start=1)` |
| zip | stops at shortest; `zip(*pairs)` to unzip |
| Dict comprehension | `{k: v for k, v in items if condition}` |
| sorted key | `sorted(lst, key=lambda x: x["field"])` |
| pass | placeholder — do nothing, no error |
| assert | `assert condition, "message"` — crash if False |
| lambda exists because | throwaway inline function for map/filter/sorted |
| lambda can't replace def | one expression only — no loops, no multi-step logic |
| map() | apply function to every element → wrap in list() |
| filter() | keep elements where function → True → wrap in list() |
| np.argmax | index of max value |
| np.where | `np.where(cond, true_val, false_val)` |
| np.concatenate | join along existing axis |
| np.stack | join along NEW axis |
| value_counts() | frequency table of unique values |
| nunique() | count of unique values |
| crosstab | frequency table of 2 categorical columns |
| merge how | inner/left/right/outer |
| concat vs merge | stack same structure vs join on key |
| iloc pen-paper | position-based, end EXCLUDED, works like array |

---

*Set 3 = the questions most likely to actually appear. Nail these first. 🎯*
