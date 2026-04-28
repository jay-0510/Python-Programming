# 🔢 NumPy — Complete Guide: Under the Hood + Hands-On

> **How to use this file:** Read the theory first, then type every code example manually. Don’t copy-paste. Manual typing builds muscle memory and forces you to read each character.

-----

## 🧠 What is NumPy and WHY Does It Exist?

Python lists are flexible — they can hold integers, strings, functions, anything. But that flexibility has a cost: **each element is a full Python object stored as a pointer**, scattered across memory.

```
Python List [1, 2, 3]:
Memory:  [ptr→obj(1)] [ptr→obj(2)] [ptr→obj(3)]
         ↑                ↑                ↑
     random addr      random addr      random addr
```

This means:

- To add two lists element-by-element, Python loops, dereferences each pointer, boxes/unboxes the value, and loops again.
- The CPU cache gets thrashed because data is scattered.

**NumPy’s fix:** Store all elements as **raw bytes in a single contiguous block of memory**, with a fixed data type.

```
NumPy Array [1, 2, 3] (dtype=int64):
Memory:  [00000001][00000002][00000003]
          8 bytes    8 bytes    8 bytes
         ← contiguous, tightly packed →
```

Now the CPU can:

- Load a whole chunk into cache in one shot
- Use **SIMD instructions** (Single Instruction, Multiple Data) — one CPU instruction operates on 4–8 numbers simultaneously
- Avoid Python’s interpreter loop entirely (operations run in compiled C)

**Result:** NumPy is typically **50x–200x faster** than equivalent pure Python for numerical work.

-----

## 📦 Installation & Import

```bash
pip install numpy
```

```python
import numpy as np   # 'np' is the universal alias — always use this
```

-----

-----

# 1. Arrays & Creation

## What is an ndarray?

`ndarray` = N-Dimensional Array. It is NumPy’s core object. Every array has:

- A **data buffer** — the raw bytes in memory
- A **dtype** — what type each element is (int32, float64, etc.)
- A **shape** — dimensions of the array
- **Strides** — how many bytes to skip to reach the next element along each axis

```
Array metadata (header):
  data pointer → [raw bytes in memory]
  dtype        = float64
  shape        = (3, 4)
  strides      = (32, 8)   ← skip 32 bytes to go to next row, 8 to go to next column
```

## np.array() — Create from Python data

```python
import numpy as np

# 1D array (vector)
a = np.array([10, 20, 30, 40])
print(a)          # [10 20 30 40]
print(type(a))    # <class 'numpy.ndarray'>

# 2D array (matrix)
b = np.array([[1, 2, 3],
              [4, 5, 6]])
print(b)
# [[1 2 3]
#  [4 5 6]]

# NumPy infers dtype automatically
c = np.array([1.0, 2.0, 3.0])
print(c.dtype)   # float64

# Force a specific dtype
d = np.array([1, 2, 3], dtype=np.float32)
print(d.dtype)   # float32
```

> **Under the hood:** `np.array()` allocates a contiguous memory block, then copies your Python values into it, converting them to the target dtype.

## np.zeros() and np.ones()

```python
# All zeros — useful to pre-allocate an array before filling it
z = np.zeros((3, 4))        # shape: 3 rows, 4 columns
print(z)
# [[0. 0. 0. 0.]
#  [0. 0. 0. 0.]
#  [0. 0. 0. 0.]]

# All ones
o = np.ones((2, 3), dtype=int)
print(o)
# [[1 1 1]
#  [1 1 1]]

# Filled with any constant
f = np.full((2, 2), 7)
print(f)
# [[7 7]
#  [7 7]]
```

## np.arange() — Like Python’s range(), but returns an array

```python
# arange(start, stop, step)   — stop is EXCLUDED
r = np.arange(0, 10, 2)
print(r)   # [0 2 4 6 8]

r2 = np.arange(5)        # 0 to 4
print(r2)  # [0 1 2 3 4]

r3 = np.arange(1.0, 2.0, 0.3)   # works with floats too
print(r3)  # [1.  1.3 1.6 1.9]
```

> ⚠️ With float steps, rounding errors can cause unexpected element counts. Prefer `np.linspace` when you need exact count.

## np.linspace() — Evenly spaced between two endpoints

```python
# linspace(start, stop, num)  — stop IS INCLUDED by default
L = np.linspace(0, 1, 5)
print(L)   # [0.   0.25 0.5  0.75 1.  ]

L2 = np.linspace(0, 10, 11)
print(L2)  # [ 0.  1.  2.  3.  4.  5.  6.  7.  8.  9. 10.]
```

**`arange` vs `linspace`:**

- Use `arange` when you know the **step size**
- Use `linspace` when you know the **number of points**

## np.random.rand() — Random values

```python
# rand() gives values from uniform distribution between [0, 1)
r = np.random.rand(3, 4)    # 3x4 matrix of random floats
print(r)

# Random integers
ri = np.random.randint(0, 100, size=(3, 3))   # values 0–99
print(ri)
```

-----

-----

# 2. Array Properties

Every ndarray has attributes that describe its structure. These are just reading metadata — they don’t copy data.

```python
import numpy as np

a = np.array([[1, 2, 3],
              [4, 5, 6]])

print(a.shape)   # (2, 3)   → 2 rows, 3 columns
print(a.ndim)    # 2        → number of dimensions (axes)
print(a.size)    # 6        → total number of elements
print(a.dtype)   # int64    → type of each element
print(a.itemsize)# 8        → bytes per element (int64 = 8 bytes)
print(a.nbytes)  # 48       → total bytes = size × itemsize
```

> **Under the hood:** `shape`, `ndim`, `size` are all just reading from the array’s header struct — no computation happens.

## reshape() — Change shape without changing data

```python
a = np.arange(12)          # [0 1 2 3 4 5 6 7 8 9 10 11]
print(a.shape)             # (12,)

b = a.reshape(3, 4)        # 3 rows, 4 columns
print(b)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]

c = a.reshape(2, 2, 3)     # 3D array: 2 "blocks" of 2x3
print(c.shape)             # (2, 2, 3)

# Use -1 to let NumPy infer one dimension automatically
d = a.reshape(4, -1)       # 4 rows, NumPy figures out columns = 3
print(d.shape)             # (4, 3)
```

> **Under the hood:** `reshape` returns a **view** (same memory block), just changes the strides/shape metadata. No data is copied. This is why reshape is O(1) — instant, regardless of array size.

```python
# Verify it's the same memory
a = np.arange(12)
b = a.reshape(3, 4)
b[0, 0] = 999
print(a[0])    # 999 — same memory!
```

-----

-----

# 3. Indexing & Slicing

## 1D Indexing

```python
a = np.array([10, 20, 30, 40, 50])

print(a[0])    # 10    (first element)
print(a[-1])   # 50    (last element)
print(a[-2])   # 40    (second from end)
```

## 1D Slicing — a[start:stop:step]

```python
a = np.array([10, 20, 30, 40, 50, 60])

print(a[1:4])    # [20 30 40]    (index 1 to 3, stop excluded)
print(a[:3])     # [10 20 30]    (from start to index 2)
print(a[3:])     # [40 50 60]    (from index 3 to end)
print(a[::2])    # [10 30 50]    (every 2nd element)
print(a[::-1])   # [60 50 40 30 20 10]   (reversed)
```

## 2D Indexing — a[row, col]

```python
a = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])

print(a[0, 0])   # 1   (top-left)
print(a[1, 2])   # 6   (row 1, col 2)
print(a[-1, -1]) # 9   (bottom-right)

# Entire row
print(a[1, :])   # [4 5 6]

# Entire column
print(a[:, 1])   # [2 5 8]

# Sub-matrix (2D slice)
print(a[0:2, 1:3])
# [[2 3]
#  [5 6]]
```

## ⚠️ CRITICAL: Slices are VIEWS, not copies

```python
a = np.array([1, 2, 3, 4, 5])
b = a[1:4]       # b is a VIEW of a's memory
b[0] = 99
print(a)         # [ 1 99  3  4  5] — a is modified!

# To get an independent copy:
c = a[1:4].copy()
c[0] = 0
print(a)         # unchanged
```

## Boolean Masking — Filter by condition

```python
a = np.array([10, 25, 3, 47, 8, 60])

mask = a > 20
print(mask)    # [False  True False  True False  True]

# Apply mask — returns only True elements
print(a[mask]) # [25 47 60]

# One-liner
print(a[a > 20])   # [25 47 60]

# Compound conditions
print(a[(a > 10) & (a < 50)])   # [25 47]
print(a[(a < 10) | (a > 50)])   # [3 8 60]
```

> **Under the hood:** Boolean indexing always creates a **copy** (unlike slice views), because selected elements may not be contiguous in memory.

-----

-----

# 4. Array Operations

## Arithmetic — Element-wise by default

```python
a = np.array([1, 2, 3, 4])
b = np.array([10, 20, 30, 40])

print(a + b)    # [11 22 33 44]
print(b - a)    # [ 9 18 27 36]
print(a * b)    # [ 10  40  90 160]
print(b / a)    # [10. 10. 10. 10.]
print(a ** 2)   # [ 1  4  9 16]

# Scalar operations (broadcasting automatically applies)
print(a + 100)  # [101 102 103 104]
print(a * 2)    # [2 4 6 8]
```

> **Under the hood:** These call optimized C/Fortran routines (BLAS/LAPACK). No Python loop exists — the CPU processes multiple elements per clock cycle using vectorized instructions.

## Aggregate Functions

```python
a = np.array([[1, 2, 3],
              [4, 5, 6]])

print(np.sum(a))      # 21   (sum of ALL elements)
print(np.mean(a))     # 3.5
print(np.min(a))      # 1
print(np.max(a))      # 6
```

## The axis Parameter — Direction of operation

`axis=0` → collapse **rows** (operate column-by-column, result has shape of one row)
`axis=1` → collapse **columns** (operate row-by-row, result has shape of one column)

```python
a = np.array([[1, 2, 3],
              [4, 5, 6]])

# axis=0: sum DOWN each column
print(np.sum(a, axis=0))    # [5 7 9]

# axis=1: sum ACROSS each row
print(np.sum(a, axis=1))    # [ 6 15]

print(np.mean(a, axis=0))   # [2.5 3.5 4.5]
print(np.max(a, axis=1))    # [3 6]
```

**Visual aid for axis:**

```
          col0 col1 col2
  row0  [  1    2    3  ]   axis=1 → sum across → 6
  row1  [  4    5    6  ]   axis=1 → sum across → 15
           ↓    ↓    ↓
         axis=0 (sum down)
          5    7    9
```

-----

-----

# 5. Array Manipulation

## flatten() vs ravel() — Convert to 1D

```python
a = np.array([[1, 2, 3],
              [4, 5, 6]])

flat = a.flatten()    # Always returns a COPY
print(flat)           # [1 2 3 4 5 6]

rav = a.ravel()       # Returns a VIEW when possible (faster)
print(rav)            # [1 2 3 4 5 6]
```

## transpose() — Swap axes

```python
a = np.array([[1, 2, 3],
              [4, 5, 6]])
print(a.shape)       # (2, 3)

t = a.T              # shorthand for transpose
print(t)
# [[1 4]
#  [2 5]
#  [3 6]]
print(t.shape)       # (3, 2)
```

> **Under the hood:** `.T` doesn’t move any data. It just swaps the stride values in the header. Instant operation.

## np.concatenate() — Join arrays along existing axis

```python
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])

# axis=0: stack vertically (add rows)
c = np.concatenate([a, b], axis=0)
print(c)
# [[1 2]
#  [3 4]
#  [5 6]
#  [7 8]]

# axis=1: stack horizontally (add columns)
d = np.concatenate([a, b], axis=1)
print(d)
# [[1 2 5 6]
#  [3 4 7 8]]
```

## np.stack() — Join along a NEW axis

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# axis=0: creates a new first axis
s0 = np.stack([a, b], axis=0)
print(s0)
# [[1 2 3]
#  [4 5 6]]
print(s0.shape)   # (2, 3)

# axis=1: creates a new second axis
s1 = np.stack([a, b], axis=1)
print(s1)
# [[1 4]
#  [2 5]
#  [3 6]]
print(s1.shape)   # (3, 2)
```

**`concatenate` vs `stack`:**

- `concatenate`: arrays must have the same shape along the chosen axis; joins along an **existing** axis
- `stack`: arrays must have the **exact same shape**; creates a **new** axis

## np.split() — Divide array into parts

```python
a = np.arange(12)

# Split into 3 equal parts
parts = np.split(a, 3)
print(parts)   # [array([0,1,2,3]), array([4,5,6,7]), array([8,9,10,11])]

# Split at specific indices
parts2 = np.split(a, [3, 7])
print(parts2)  # [array([0,1,2]), array([3,4,5,6]), array([7,8,9,10,11])]
```

-----

-----

# 6. Math Functions

```python
import numpy as np

a = np.array([1, 4, 9, 16])

print(np.sqrt(a))     # [1. 2. 3. 4.]
print(np.exp(a))      # [  2.718  54.598  8103.08  ...]  (e^x for each element)
print(np.log(a))      # [0.    1.386 2.197 2.773]   (natural log)
print(np.log10(a))    # [0.    0.602 0.954 1.204]
print(np.abs(np.array([-3, -1, 2, -5])))   # [3 1 2 5]
```

## np.dot() — Dot product / Matrix multiplication

```python
# For 1D: dot product (sum of element-wise products)
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print(np.dot(a, b))    # 1*4 + 2*5 + 3*6 = 32

# For 2D: matrix multiplication
A = np.array([[1, 2],
              [3, 4]])
B = np.array([[5, 6],
              [7, 8]])
print(np.dot(A, B))
# [[19 22]
#  [43 50]]

# Modern alternative (Python 3.5+)
print(A @ B)    # same result
```

> **Under the hood:** `np.dot` calls BLAS (Basic Linear Algebra Subprograms) — highly optimized C/Fortran routines that use CPU-specific vectorization and multi-threading. This is the same code used by MATLAB and R.

## np.unique() and np.sort()

```python
a = np.array([3, 1, 4, 1, 5, 9, 2, 6, 5, 3])

print(np.unique(a))             # [1 2 3 4 5 6 9]

# Get unique values AND their counts
vals, counts = np.unique(a, return_counts=True)
print(vals)     # [1 2 3 4 5 6 9]
print(counts)   # [2 1 2 1 2 1 1]

# Sort (returns sorted copy)
print(np.sort(a))               # [1 1 2 3 3 4 5 5 6 9]

# Sort descending
print(np.sort(a)[::-1])         # [9 6 5 5 4 3 3 2 1 1]
```

-----

-----

# 7. Broadcasting

Broadcasting is NumPy’s mechanism for doing arithmetic between arrays of **different shapes** — without copying data.

## The Rules

When operating on two arrays, NumPy compares their shapes from the **rightmost** dimension:

1. If dimensions are equal → OK
1. If one dimension is 1 → it is “stretched” to match the other
1. If neither is 1 and they’re not equal → **Error**

## Examples

```python
# Scalar broadcast (trivial case)
a = np.array([1, 2, 3])
print(a + 10)    # [11 12 13]   — 10 is broadcast to [10, 10, 10]

# 1D to 2D broadcast
a = np.array([[1, 2, 3],    # shape (2, 3)
              [4, 5, 6]])
b = np.array([10, 20, 30])  # shape (3,)  → treated as (1, 3) → stretched to (2, 3)
print(a + b)
# [[11 22 33]
#  [14 25 36]]

# Column vector × row vector → 2D matrix
col = np.array([[1],    # shape (3, 1)
                [2],
                [3]])
row = np.array([10, 20, 30])   # shape (3,) → treated as (1, 3)
print(col * row)
# [[10 20 30]
#  [20 40 60]
#  [30 60 90]]
print((col * row).shape)   # (3, 3)
```

**Shape compatibility table:**

```
Shape A    Shape B    Result?
(3,)       (3,)       (3,)    ✅
(3,)       (1,)       (3,)    ✅  (B stretched)
(2,3)      (3,)       (2,3)   ✅  (B treated as (1,3) stretched)
(2,3)      (2,1)      (2,3)   ✅  (B stretched columns)
(2,3)      (2,4)      ERROR   ❌  (3 ≠ 4, neither is 1)
```

> **Under the hood:** No data is actually copied! NumPy uses stride tricks — stride of 0 on the broadcast dimension means the same memory row is “read” multiple times.

-----

-----

# 8. Advanced Indexing

## Fancy Indexing — Index with an array

```python
a = np.array([10, 20, 30, 40, 50])

idx = np.array([0, 2, 4])
print(a[idx])    # [10 30 50]

# Non-sequential, repeated, reordered
print(a[[4, 4, 1, 0]])   # [50 50 20 10]
```

> **Under the hood:** Fancy indexing always creates a **copy** (unlike slice views), because selected elements are typically non-contiguous.

## 2D Fancy Indexing

```python
a = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])

# Select elements at (0,0), (1,1), (2,2) — the diagonal
rows = [0, 1, 2]
cols = [0, 1, 2]
print(a[rows, cols])   # [1 5 9]

# Select specific rows
print(a[[0, 2]])       # rows 0 and 2
# [[1 2 3]
#  [7 8 9]]
```

## np.where() — Conditional element selection

```python
a = np.array([1, -2, 3, -4, 5])

# np.where(condition, value_if_true, value_if_false)
result = np.where(a > 0, a, 0)    # keep positives, set negatives to 0
print(result)   # [1 0 3 0 5]

# Replace negatives with their absolute value
result2 = np.where(a > 0, a, -a)
print(result2)  # [1 2 3 4 5]

# With no value args — returns INDICES where condition is True
idx = np.where(a > 0)
print(idx)      # (array([0, 2, 4]),)
print(a[idx])   # [1 3 5]
```

## np.argmax() and np.argsort()

```python
a = np.array([30, 10, 50, 20, 40])

print(np.argmax(a))    # 2   (index of maximum value, 50 is at index 2)
print(np.argmin(a))    # 1   (index of minimum value)

# argmax along axis in 2D
b = np.array([[1, 5, 3],
              [7, 2, 4]])
print(np.argmax(b, axis=0))   # [1 0 1]  → index of max in each column
print(np.argmax(b, axis=1))   # [1 0]    → index of max in each row

# argsort — returns indices that WOULD sort the array
a = np.array([30, 10, 50, 20])
idx = np.argsort(a)
print(idx)       # [1 3 0 2]  → a[1]=10, a[3]=20, a[0]=30, a[2]=50
print(a[idx])    # [10 20 30 50]  (sorted)
```

-----

-----

# 9. Views vs Copies — CRITICAL CONCEPT

This is one of the most important and tricky aspects of NumPy. Getting this wrong causes bugs that are very hard to trace.

## The Rules

|Operation                  |View or Copy?           |
|---------------------------|------------------------|
|Basic slicing `a[1:3]`     |**View**                |
|Reshaping `a.reshape(...)` |**View** (usually)      |
|Transpose `a.T`            |**View**                |
|Boolean indexing `a[a > 0]`|**Copy**                |
|Fancy indexing `a[[0,2,4]]`|**Copy**                |
|`a.copy()`                 |**Copy** (explicit)     |
|`a.flatten()`              |**Copy**                |
|`a.ravel()`                |**View** (when possible)|

## Demonstrating Views

```python
a = np.array([1, 2, 3, 4, 5])

# Slice = view
b = a[1:4]
print(b)          # [2 3 4]
b[0] = 99
print(a)          # [ 1 99  3  4  5]   ← a changed!

# Reshape = view
c = a.reshape(5)
c[0] = 0
print(a)          # [0 99  3  4  5]    ← a changed again!
```

## Demonstrating Copies

```python
a = np.array([1, 2, 3, 4, 5])

# Boolean indexing = copy
mask = a > 2
b = a[mask]
b[0] = 999
print(a)    # [1 2 3 4 5]   ← a unchanged

# Fancy indexing = copy
c = a[[0, 2]]
c[0] = 999
print(a)    # [1 2 3 4 5]   ← a unchanged
```

## Checking if it’s a view with .base

```python
a = np.arange(10)
b = a[2:5]

print(b.base is a)   # True  → b is a view of a
print(b.flags['OWNDATA'])   # False → doesn't own its data

c = a.copy()
print(c.base is None)  # True → c owns its own data
```

## np.copy() — Explicit copy

```python
a = np.array([1, 2, 3, 4, 5])
b = np.copy(a)     # or: b = a.copy()
b[0] = 999
print(a)    # [1 2 3 4 5]   ← safe, a is unchanged
```

-----

-----

# 10. Statistical Functions

```python
import numpy as np

data = np.array([4, 7, 2, 9, 1, 5, 8, 3, 6, 10])

print(np.mean(data))       # 5.5
print(np.median(data))     # 5.5   (middle value when sorted)
print(np.std(data))        # 2.872  (standard deviation)
print(np.var(data))        # 8.25   (variance = std²)

# Percentiles
print(np.percentile(data, 25))    # 3.25   (Q1)
print(np.percentile(data, 50))    # 5.5    (Q2 = median)
print(np.percentile(data, 75))    # 7.75   (Q3)
print(np.percentile(data, 90))    # 9.1    (90th percentile)
```

## np.corrcoef() — Correlation coefficient

Measures linear relationship between two variables. Output ranges from -1 (perfect inverse) to +1 (perfect direct), 0 = no linear relationship.

```python
study_hours = np.array([1, 2, 3, 4, 5, 6, 7, 8])
exam_scores  = np.array([45, 55, 60, 65, 70, 80, 85, 95])

corr = np.corrcoef(study_hours, exam_scores)
print(corr)
# [[1.         0.995...]
#  [0.995...   1.       ]]
# The off-diagonal value (0.995) is the correlation between the two arrays
# Close to 1.0 → strong positive correlation ✅
```

## 2D Statistics

```python
scores = np.array([[85, 90, 78],
                   [72, 88, 95],
                   [90, 76, 82]])

# Per-student average (mean across columns = axis=1)
print(np.mean(scores, axis=1))   # [84.33 85.   82.67]

# Per-subject average (mean across rows = axis=0)
print(np.mean(scores, axis=0))   # [82.33 84.67 85.  ]

# Spread within each subject
print(np.std(scores, axis=0))    # [7.55 6.03 7.09]
```

-----

-----

# 11. Random Module

## Reproducibility with seed

```python
np.random.seed(42)    # Set seed for reproducibility
a = np.random.rand(5)
print(a)   # Always the same: [0.374 0.951 0.732 0.599 0.156]

np.random.seed(42)
b = np.random.rand(5)
print(b)   # Same as a — same seed = same sequence
```

> **Under the hood:** NumPy uses the Mersenne Twister PRNG. The seed initializes the internal state. Same seed → identical sequence of numbers every time. Essential for reproducible experiments.

## Key Random Functions

```python
np.random.seed(0)

# Uniform [0, 1)
print(np.random.rand(3))          # [0.549 0.715 0.603]

# Uniform [low, high)
print(np.random.uniform(5, 10, size=4))   # random floats between 5 and 10

# Random integers [low, high)
print(np.random.randint(1, 7, size=10))   # simulate 10 dice rolls

# Normal distribution (Gaussian) — mean=0, std=1 by default
print(np.random.normal(loc=0, scale=1, size=5))

# Normal with custom mean and std
heights = np.random.normal(loc=170, scale=10, size=100)   # heights in cm

# Random choice from an array
colors = np.array(['red', 'green', 'blue'])
print(np.random.choice(colors, size=5))
print(np.random.choice(colors, size=5, replace=False))   # no repeats

# Shuffle in-place (modifies original)
a = np.array([1, 2, 3, 4, 5])
np.random.shuffle(a)
print(a)   # [3 1 4 5 2]  (random order, in-place)
```

-----

-----

# 🌍 Real-World Use Cases — Topics Combined

## Use Case 1: Cricket Match Score Analysis

Combining: Array creation, Properties, Statistics, Boolean Masking

```python
import numpy as np

np.random.seed(7)

# 50 overs, runs scored per over (simulate)
runs_per_over = np.random.randint(0, 20, size=50)
print("Total Score:", np.sum(runs_per_over))
print("Average per over:", np.mean(runs_per_over).round(2))
print("Best over:", np.max(runs_per_over))
print("Worst over:", np.min(runs_per_over))

# Powerplay (first 6 overs)
powerplay = runs_per_over[:6]
print("Powerplay runs:", np.sum(powerplay))

# Death overs (last 5)
death = runs_per_over[-5:]
print("Death over runs:", np.sum(death))

# How many overs scored 15+?
big_overs = runs_per_over[runs_per_over >= 15]
print("Overs with 15+ runs:", len(big_overs))

# Which over numbers were those?
over_nums = np.where(runs_per_over >= 15)[0] + 1   # +1 since overs are 1-indexed
print("Big over numbers:", over_nums)
```

-----

## Use Case 2: Student Grade Processing

Combining: 2D Arrays, Axis operations, Broadcasting, Boolean Masking, Statistical Functions

```python
import numpy as np

# 5 students × 4 subjects: Math, Science, English, History
np.random.seed(42)
grades = np.random.randint(40, 100, size=(5, 4))
subjects = ['Math', 'Science', 'English', 'History']
students = ['Aarav', 'Priya', 'Raj', 'Sneha', 'Vikram']

print("Raw grades:\n", grades)

# Per-student average
student_avg = np.mean(grades, axis=1)
for name, avg in zip(students, student_avg):
    print(f"{name}: {avg:.1f}")

# Class average per subject
subject_avg = np.mean(grades, axis=0)
for sub, avg in zip(subjects, subject_avg):
    print(f"{sub}: {avg:.1f}")

# Who passed all subjects? (passing = 50+)
passed_all = np.all(grades >= 50, axis=1)
print("\nPassed all subjects:", np.array(students)[passed_all])

# Normalize grades to [0, 100] based on subject max
# Broadcasting: subtract min, divide by range
grade_min = grades.min(axis=0)     # shape (4,)
grade_max = grades.max(axis=0)     # shape (4,)
normalized = (grades - grade_min) / (grade_max - grade_min) * 100
print("\nNormalized grades:\n", normalized.round(1))

# Top scorer per subject
top_idx = np.argmax(grades, axis=0)
print("\nTop scorer per subject:")
for sub, idx in zip(subjects, top_idx):
    print(f"  {sub}: {students[idx]}")
```

-----

## Use Case 3: Stock Price Simulation & Analysis

Combining: Random Module, Math Functions, Statistical Functions, Views/Copies, Broadcasting

```python
import numpy as np

np.random.seed(2024)

# Simulate 252 trading days (1 year) for 3 stocks
# Daily returns follow normal distribution
# Mean daily return ~0.04%, std ~1.5% (realistic)
n_days = 252
n_stocks = 3
stock_names = ['RELIANCE', 'TCS', 'INFOSYS']

daily_returns = np.random.normal(loc=0.0004, scale=0.015, size=(n_days, n_stocks))

# Convert returns to prices (starting at 1000, 3500, 1500)
start_prices = np.array([1000, 3500, 1500])
# Cumulative product to get price paths
prices = start_prices * np.cumprod(1 + daily_returns, axis=0)

print("=== STOCK ANALYSIS (1 Year) ===")

# Final vs start prices
final_prices = prices[-1]
returns_pct = (final_prices - start_prices) / start_prices * 100

for name, start, end, ret in zip(stock_names, start_prices, final_prices, returns_pct):
    print(f"{name}: ₹{start:.0f} → ₹{end:.0f}  ({ret:+.1f}%)")

# Volatility (annualized std of daily returns × √252)
volatility = np.std(daily_returns, axis=0) * np.sqrt(252) * 100
print("\nAnnualized Volatility:")
for name, vol in zip(stock_names, volatility):
    print(f"  {name}: {vol:.1f}%")

# Correlation between stocks
corr_matrix = np.corrcoef(daily_returns.T)   # .T because corrcoef expects (n_vars, n_obs)
print("\nCorrelation Matrix:")
print(np.round(corr_matrix, 3))

# Days where all stocks fell together (bad market day)
all_down = np.all(daily_returns < 0, axis=1)
print(f"\nDays all 3 stocks fell: {np.sum(all_down)} out of {n_days}")

# Best and worst days per stock
best_day_idx = np.argmax(daily_returns, axis=0)
worst_day_idx = np.argmin(daily_returns, axis=0)
print("\nBest day (day number) per stock:", best_day_idx + 1)
print("Worst day (day number) per stock:", worst_day_idx + 1)
```

-----

## Use Case 4: Image as a NumPy Array (Grayscale Manipulation)

Combining: Array creation, Broadcasting, Slicing, Math Functions

```python
import numpy as np

# In real use: image = np.array(PIL.Image.open('photo.jpg'))
# Here we simulate a 6×6 grayscale image (pixel values 0–255)
np.random.seed(5)
image = np.random.randint(0, 256, size=(6, 6), dtype=np.uint8)
print("Original image (pixel values):\n", image)

# Crop a region (view — no copy!)
crop = image[1:4, 1:4]
print("\nCropped region:\n", crop)

# Flip horizontally (view — no copy!)
flipped = image[:, ::-1]
print("\nHorizontally flipped:\n", flipped)

# Brightness adjustment (Broadcasting)
brightened = np.clip(image.astype(np.int32) + 50, 0, 255).astype(np.uint8)
print("\nBrightened (capped at 255):\n", brightened)

# Thresholding — make pixels black or white
binary = np.where(image > 128, 255, 0).astype(np.uint8)
print("\nBinary (threshold=128):\n", binary)

# Histogram: count pixels in each intensity range
hist, edges = np.histogram(image.flatten(), bins=4, range=(0, 256))
labels = ['dark', 'mid-dark', 'mid-bright', 'bright']
for label, count in zip(labels, hist):
    print(f"  {label}: {count} pixels")
```

-----

## Use Case 5: Machine Learning — Feature Normalization

Combining: Broadcasting, Statistical Functions, Array Operations, Math Functions

```python
import numpy as np

# Dataset: 6 samples × 3 features (Age, Income_thousands, Years_experience)
data = np.array([
    [25, 30,  2],
    [35, 60,  8],
    [45, 90, 15],
    [28, 40,  4],
    [52, 110, 20],
    [38, 75, 12],
], dtype=float)

print("Raw features:\n", data)

# Min-Max Normalization: scale each feature to [0, 1]
# Formula: (x - min) / (max - min)
col_min = data.min(axis=0)   # shape (3,) — minimum of each feature
col_max = data.max(axis=0)   # shape (3,)
normalized = (data - col_min) / (col_max - col_min)   # Broadcasting!
print("\nMin-Max Normalized:\n", normalized.round(3))

# Z-Score Standardization: mean=0, std=1 for each feature
col_mean = data.mean(axis=0)
col_std  = data.std(axis=0)
standardized = (data - col_mean) / col_std   # Broadcasting!
print("\nZ-Score Standardized:\n", standardized.round(3))

# Verify: each column should now have mean≈0, std≈1
print("\nMeans after standardization:", standardized.mean(axis=0).round(10))
print("Stds after standardization: ", standardized.std(axis=0).round(10))

# Euclidean distance between sample 0 and all others
s0 = standardized[0]                    # shape (3,)
diffs = standardized - s0               # Broadcasting: (6,3) - (3,) → (6,3)
distances = np.sqrt(np.sum(diffs**2, axis=1))
print("\nDistance from sample 0 to all samples:", distances.round(3))
print("Nearest neighbor index:", np.argsort(distances)[1])   # [0] is itself
```

-----

-----

# 🔬 Quick Reference: Common Patterns

```python
# Create evenly spaced values for plotting
x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)

# Stack features as columns
feature1 = np.array([1, 2, 3])
feature2 = np.array([4, 5, 6])
matrix = np.column_stack([feature1, feature2])   # shape (3, 2)

# Get indices of top N values
a = np.array([3, 1, 4, 1, 5, 9, 2, 6])
top3_idx = np.argsort(a)[-3:][::-1]   # indices of 3 largest
print(a[top3_idx])   # [9 6 5]

# Clip values to a range
a = np.array([-10, 5, 200, 75, -3])
print(np.clip(a, 0, 100))   # [  0   5 100  75   0]

# Replace NaN-like values (here: values below 0 treated as "missing")
a = np.array([1.0, -999, 3.0, -999, 5.0])
clean = np.where(a == -999, np.mean(a[a != -999]), a)
print(clean)   # [1. 3. 3. 3. 5.]  (replaced with mean)

# Outer product
a = np.array([1, 2, 3])
b = np.array([10, 20])
print(np.outer(a, b))
# [[10 20]
#  [20 40]
#  [30 60]]
```

-----

# 📝 Summary: Key Mental Models

|Concept      |Mental Model                                                                    |
|-------------|--------------------------------------------------------------------------------|
|ndarray      |Contiguous bytes in RAM with a header describing shape/type                     |
|reshape      |Change the “reading pattern” for the same bytes (free!)                         |
|slice        |A window into existing memory (free, but modifying changes original)            |
|copy         |A completely independent memory block                                           |
|axis         |Direction to collapse: axis=0 collapses rows, axis=1 collapses columns          |
|broadcast    |NumPy “pretends” to repeat data along size-1 dimensions without actually copying|
|fancy index  |Uses an array of indices; always returns a copy                                 |
|dtype        |Fixed type per element is what makes NumPy fast vs Python lists                 |
|vectorization|Operations run in C with no Python loop; uses CPU SIMD instructions             |

-----

*Made for learning NumPy from the ground up — type every example manually.*