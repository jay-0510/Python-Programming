# NumPy & Pandas – 30 Basic Interview Questions You Must Know

---

## The Question Your Mentor Asked First

### NumPy Array vs Pandas DataFrame — Full Answer

```python
import numpy as np
import pandas as pd

# NumPy Array — homogeneous, mathematical, N-dimensional
arr = np.array([[1, 2, 3],
                [4, 5, 6]])
# - Every element is the SAME dtype (all int, all float)
# - Indexed by position only: arr[0][1] or arr[0, 1]
# - Built for math: matrix ops, linear algebra, broadcasting
# - No column names, no row labels
# - Shape: (2, 3) — 2 rows, 3 columns

# Pandas DataFrame — heterogeneous, labeled, tabular
df = pd.DataFrame({
    "name":   ["Alice", "Bob"],    # string column
    "age":    [25, 30],            # int column
    "salary": [50000.0, 80000.0]   # float column
})
# - Each COLUMN can have a different dtype
# - Indexed by label (loc) or position (iloc)
# - Built for data analysis: filter, group, merge, clean
# - Has column names and row index
```

| | NumPy Array | Pandas DataFrame |
|---|---|---|
| Data types | All same (homogeneous) | Each column can differ |
| Index | Position only (0,1,2) | Labels + position |
| Column names | ❌ No | ✅ Yes |
| Best for | Math, ML inputs | Data cleaning, analysis |
| Missing values | Not built-in | Built-in (NaN handling) |
| Speed | Faster for math | Slower but more features |

> **When to use which:**
> Use NumPy when doing matrix math, ML model inputs, or scientific computing.
> Use Pandas when loading CSVs, cleaning data, filtering rows, grouping — anything "table-like".

---

## NumPy — 15 Basic Questions

---

### 1. What is a NumPy array? How is it different from a Python list?

**Answer:**
A NumPy array is a **fixed-type, fixed-size grid of values**. Python list can hold mixed types and is flexible. NumPy array is strict — same type, faster math.

```python
# Python list — mixed types, flexible
py_list = [1, "hello", 3.14, True]   # totally fine

# NumPy array — one type only
arr = np.array([1, 2, 3, 4])         # all integers

# What happens when you mix:
mixed = np.array([1, 2.5, 3])        # NumPy upgrades all to float
print(mixed)       # [1.  2.5 3. ]   # ← notice the dots — all float now
print(mixed.dtype) # float64

# Math on list — doesn't work intuitively
py_list = [1, 2, 3]
py_list * 2        # [1, 2, 3, 1, 2, 3] ← repeats the list!

# Math on array — works element-wise
arr = np.array([1, 2, 3])
arr * 2            # [2, 4, 6] ← multiplies each element
```

> **Why it matters:** NumPy's fixed type is why it's fast — it uses raw C under the hood, no Python overhead per element.

---

### 2. What does `dtype` mean in a NumPy array?

**Answer:**
`dtype` is the **data type** of every element in the array. Since all elements share one type, NumPy can store them efficiently.

```python
arr_int   = np.array([1, 2, 3])
arr_float = np.array([1.0, 2.0, 3.0])
arr_str   = np.array(["a", "b", "c"])

print(arr_int.dtype)    # int64    ← 64-bit integer
print(arr_float.dtype)  # float64  ← 64-bit float
print(arr_str.dtype)    # <U1      ← Unicode string

# You can set dtype manually:
arr = np.array([1, 2, 3], dtype=np.float32)  # use float32 to save memory
print(arr.dtype)   # float32
print(arr)         # [1. 2. 3.]
```

> **Why it matters:** Choosing the right dtype saves memory. `float32` uses half the memory of `float64` — important when working with large ML datasets.

---

### 3. What is the difference between `shape` and `size`?

**Answer:**
- `shape` — tuple showing dimensions (rows, columns, depth...)
- `size` — total number of elements (multiply all shape values)

```python
arr = np.array([[1, 2, 3],
                [4, 5, 6]])

print(arr.shape)   # (2, 3)  ← 2 rows, 3 columns
print(arr.size)    # 6       ← 2 × 3 = 6 total elements

# 3D array example:
arr3d = np.zeros((4, 3, 2))
print(arr3d.shape) # (4, 3, 2)
print(arr3d.size)  # 24       ← 4 × 3 × 2 = 24
```

> **Why it matters:** Shape mismatch is the most common error in ML. Checking shape before operations saves debugging time.

---

### 4. What does `ndim` return?

**Answer:**
`ndim` returns the **number of dimensions** (axes) of the array.

```python
arr_1d = np.array([1, 2, 3])            # like a list
arr_2d = np.array([[1, 2], [3, 4]])     # like a table
arr_3d = np.zeros((2, 3, 4))            # like a cube

print(arr_1d.ndim)   # 1
print(arr_2d.ndim)   # 2
print(arr_3d.ndim)   # 3

# Quick memory trick:
# ndim = number of brackets to open before reaching a number
# [1, 2, 3]         → 1 bracket → ndim = 1
# [[1, 2], [3, 4]]  → 2 brackets → ndim = 2
```

> **Why it matters:** ML models expect specific dimensions. Images are 3D (height, width, channels). Batches are 4D. Wrong ndim = model error.

---

### 5. What is the difference between `np.zeros()` and `np.empty()`?

**Answer:**
- `np.zeros()` — fills array with **actual zeros**. Safe, predictable.
- `np.empty()` — fills with **whatever was in memory**. Fast but unpredictable.

```python
z = np.zeros((2, 3))
print(z)
# [[0. 0. 0.]
#  [0. 0. 0.]]   ← guaranteed zeros

e = np.empty((2, 3))
print(e)
# [[1.23e-30  4.56e-12  0.0]
#  [8.9e+20   0.0       3.2e-45]]   ← garbage values from memory!

# np.ones() — fills with 1s
o = np.ones((2, 3))
# [[1. 1. 1.]
#  [1. 1. 1.]]
```

> **Why it matters:** Use `empty()` only when you'll fill every element yourself (faster). Use `zeros()` when you need a safe starting point.

---

### 6. What does `reshape()` do — and what error does it throw?

**Answer:**
`reshape()` changes the **shape** of an array without changing its data. Total elements must stay the same — otherwise it throws a `ValueError`.

```python
arr = np.arange(12)        # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
print(arr.shape)           # (12,)

# Valid reshapes — total stays 12
arr.reshape(3, 4)          # shape (3, 4)  → 3×4 = 12 ✅
arr.reshape(2, 6)          # shape (2, 6)  → 2×6 = 12 ✅
arr.reshape(2, 2, 3)       # shape (2,2,3) → 2×2×3 = 12 ✅

# -1 means "figure it out automatically"
arr.reshape(3, -1)         # NumPy calculates: 12/3 = 4 → shape (3, 4)
arr.reshape(-1, 1)         # shape (12, 1) ← makes column vector

# Invalid — total doesn't match
arr.reshape(3, 5)          # 3×5 = 15 ≠ 12 → ValueError!
# ValueError: cannot reshape array of size 12 into shape (3,5)
```

> **Why it matters:** `reshape(-1, 1)` and `reshape(1, -1)` are used constantly when preparing data for ML models.

---

### 7. What is the difference between `np.arange()` and `np.linspace()`?

**Answer:**
- `np.arange(start, stop, step)` — you control the **step size**.
- `np.linspace(start, stop, num)` — you control the **number of points**.

```python
# arange — step is 2, NumPy figures out how many points
np.arange(0, 10, 2)       # [0, 2, 4, 6, 8]  → stop is EXCLUSIVE

# linspace — 5 points, NumPy figures out the step
np.linspace(0, 10, 5)     # [0, 2.5, 5, 7.5, 10]  → stop is INCLUSIVE

# The float trap with arange:
np.arange(0, 1, 0.3)
# [0.  0.3  0.6  0.9]  ← floating point rounding, unpredictable count

# linspace avoids this:
np.linspace(0, 1, 4)
# [0.    0.333 0.667 1.   ]  ← always exactly 4 points
```

> **Why it matters:** Use `linspace` for plotting and evenly spaced intervals. Use `arange` for integer sequences.

---

### 8. What is broadcasting? Give a simple example.

**Answer:**
Broadcasting lets NumPy do math on arrays of **different shapes** by stretching the smaller one — without copying data.

```python
# Adding a 1D array to a 2D array:
matrix = np.array([[1, 2, 3],
                   [4, 5, 6]])    # shape (2, 3)

row = np.array([10, 20, 30])      # shape (3,) → treated as (1, 3)

result = matrix + row
# NumPy "broadcasts" row across both rows of matrix:
# [[1+10, 2+20, 3+30],   [[11, 22, 33],
#  [4+10, 5+20, 6+30]] =  [14, 25, 36]]

# Adding a scalar — simplest broadcast:
arr = np.array([1, 2, 3])
arr + 100    # [101, 102, 103] ← 100 broadcast to every element

# Shape rule — dimensions must match OR one of them must be 1:
# (2, 3) + (3,)   → works  (3 matches 3)
# (2, 3) + (2, 1) → works  (1 stretches to 3)
# (2, 3) + (2, 2) → FAILS  (3 ≠ 2, neither is 1)
```

> **Why it matters:** Subtracting the mean from every row, normalising data — all use broadcasting. Understanding rules prevents cryptic shape errors.

---

### 9. What is the difference between a view and a copy?

**Answer:**
- **View** — points to same memory. Changing it **changes the original**.
- **Copy** — independent memory. Changing it **does not affect the original**.

```python
arr = np.array([1, 2, 3, 4, 5])

# View — slicing creates a view
view = arr[1:4]
view[0] = 99          # modifying view...
print(arr)            # [1, 99, 3, 4, 5] ← original changed!

# Reset
arr = np.array([1, 2, 3, 4, 5])

# Copy — .copy() creates independent data
copy = arr[1:4].copy()
copy[0] = 99          # modifying copy...
print(arr)            # [1, 2, 3, 4, 5] ← original unchanged

# Check if something is a view:
print(view.base is arr)   # True  ← view shares memory with arr
print(copy.base is arr)   # False ← copy is independent
```

> **Why it matters:** Accidentally modifying source data through a view is a silent bug. Always `.copy()` when you intend to modify without affecting the original.

---

### 10. When does slicing return a view vs a copy?

**Answer:**
- **Basic slicing** (using `:`) → returns a **view**
- **Fancy indexing** (using list/array of indices) → returns a **copy**
- **Boolean masking** → returns a **copy**

```python
arr = np.array([10, 20, 30, 40, 50])

# Basic slice → VIEW
s = arr[1:4]           # [20, 30, 40]
s[0] = 99
print(arr)             # [10, 99, 30, 40, 50] ← original changed

# Fancy indexing → COPY
f = arr[[0, 2, 4]]     # [10, 30, 50]
f[0] = 999
print(arr)             # [10, 99, 30, 40, 50] ← original unchanged

# Boolean mask → COPY
mask = arr > 20
b = arr[mask]          # [99, 30, 40, 50]
b[0] = 0
print(arr)             # [10, 99, 30, 40, 50] ← original unchanged
```

> **Why it matters:** A common interview trick question. Knowing this prevents data corruption bugs in preprocessing pipelines.

---

### 11. What does `axis=0` vs `axis=1` mean in `np.sum()`?

**Answer:**
`axis` tells NumPy which direction to **collapse**.
- `axis=0` → collapse **rows** → result has one value per column
- `axis=1` → collapse **columns** → result has one value per row

```python
arr = np.array([[1, 2, 3],
                [4, 5, 6]])

np.sum(arr)          # 21        ← sums everything
np.sum(arr, axis=0)  # [5, 7, 9] ← sum DOWN columns (collapse rows)
np.sum(arr, axis=1)  # [6, 15]   ← sum ACROSS rows (collapse columns)

# Memory trick:
# axis=0 → result shape loses the first dimension
# (2,3) with axis=0 → (3,)   ← 2 rows collapsed into one value per column
# (2,3) with axis=1 → (2,)   ← 3 cols collapsed into one value per row

# Same logic for mean, max, min, std:
np.mean(arr, axis=0)  # [2.5, 3.5, 4.5] ← average of each column
np.max(arr, axis=1)   # [3, 6]           ← max of each row
```

> **Why it matters:** Getting axis wrong gives a wrong answer with no error. This is the single most common NumPy mistake in practice.

---

### 12. What is fancy indexing?

**Answer:**
Fancy indexing means selecting elements using a **list or array of indices** instead of a slice. It always returns a copy.

```python
arr = np.array([10, 20, 30, 40, 50])

# Basic indexing — one element
arr[2]             # 30

# Fancy indexing — multiple elements, any order
arr[[0, 2, 4]]     # [10, 30, 50]   ← pick positions 0, 2, 4
arr[[4, 1, 3]]     # [50, 20, 40]   ← any order you want

# 2D fancy indexing:
matrix = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])

# Select rows 0 and 2:
matrix[[0, 2]]
# [[1, 2, 3],
#  [7, 8, 9]]

# Select specific (row, col) pairs:
matrix[[0, 1, 2], [0, 1, 2]]   # [1, 5, 9] ← diagonal elements
```

> **Why it matters:** Used constantly when you have a list of indices to extract (e.g., top-k predictions, shuffling datasets).

---

### 13. What does `np.where()` return?

**Answer:**
Two uses:
- `np.where(condition)` → returns **indices** where condition is True
- `np.where(condition, x, y)` → returns `x` where True, `y` where False (vectorized if-else)

```python
arr = np.array([5, -3, 8, -1, 0, 7])

# Use 1: Find indices where condition is True
indices = np.where(arr > 0)
print(indices)       # (array([0, 2, 5]),)   ← positions 0, 2, 5 are positive

# Access those values:
arr[np.where(arr > 0)]    # [5, 8, 7]

# Use 2: Vectorized if-else
result = np.where(arr > 0, arr, 0)
# Replace negatives with 0: [5, 0, 8, 0, 0, 7]

result = np.where(arr > 0, "positive", "non-positive")
# ['positive', 'non-positive', 'positive', 'non-positive', 'non-positive', 'positive']
```

> **Why it matters:** Replaces conditional loops. Used in data cleaning, label encoding, and masking operations.

---

### 14. What is the difference between `np.dot()` and `*`?

**Answer:**
- `*` — **element-wise** multiplication (same shape required)
- `np.dot()` — **matrix multiplication** (dot product)

```python
A = np.array([[1, 2],
              [3, 4]])

B = np.array([[5, 6],
              [7, 8]])

# Element-wise — multiply each matching position
A * B
# [[1×5, 2×6],   [[5,  12],
#  [3×7, 4×8]] =  [21, 32]]

# Matrix multiplication — row × column
np.dot(A, B)
# [[1×5+2×7, 1×6+2×8],   [[19, 22],
#  [3×5+4×7, 3×6+4×8]] =  [43, 50]]

# In Python 3.5+ you can also use @:
A @ B      # same as np.dot(A, B)
```

> **Why it matters:** Neural networks use matrix multiplication (dot product) in every layer. Using `*` when you mean `@` gives wrong results silently.

---

### 15. What does `flatten()` return vs `ravel()`?

**Answer:**
Both convert multi-dimensional arrays to 1D, but:
- `flatten()` → always returns a **copy**
- `ravel()` → returns a **view** when possible (faster, less memory)

```python
arr = np.array([[1, 2, 3],
                [4, 5, 6]])

# flatten — always a copy
flat = arr.flatten()
flat[0] = 99
print(arr)      # [[1, 2, 3], [4, 5, 6]] ← original unchanged

# ravel — view when possible
rav = arr.ravel()
rav[0] = 99
print(arr)      # [[99, 2, 3], [4, 5, 6]] ← original changed!

# Both give same output:
# [1, 2, 3, 4, 5, 6]

# When to use which:
# Need to modify result without affecting original → flatten()
# Need speed/memory efficiency and won't modify → ravel()
```

> **Why it matters:** Flattening images before passing to a dense layer is standard. Unexpected mutation via `ravel()` is a real bug to watch for.

---

## Pandas — 15 Basic Questions

---

### 16. What is the difference between a Series and a DataFrame?

**Answer:**
- **Series** — 1D, one column with an index. Like a single column.
- **DataFrame** — 2D, multiple columns. Like a full table.

```python
# Series — one column
s = pd.Series([10, 20, 30], index=["a", "b", "c"])
print(s)
# a    10
# b    20
# c    30
print(type(s))   # <class 'pandas.core.series.Series'>

# DataFrame — multiple columns
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Carol"],
    "age":  [25, 30, 22]
})
print(type(df))  # <class 'pandas.core.frame.DataFrame'>

# Selecting one column from DataFrame returns a Series:
print(type(df["name"]))      # Series
# Selecting with double brackets returns a DataFrame:
print(type(df[["name"]]))    # DataFrame  ← shape (3,1) not (3,)
```

> **Why it matters:** Many errors come from expecting a DataFrame but getting a Series (or vice versa). Knowing `df["col"]` vs `df[["col"]]` saves debugging time.

---

### 17. How do you create a DataFrame from a dictionary?

**Answer:**
Dictionary keys become **column names**, values become **column data**.

```python
# Method 1: From dict — most common
data = {
    "name":   ["Alice", "Bob", "Carol"],
    "age":    [25, 30, 22],
    "salary": [50000, 80000, 45000]
}
df = pd.DataFrame(data)

# Method 2: From list of dicts — each dict is one row
rows = [
    {"name": "Alice", "age": 25},
    {"name": "Bob",   "age": 30},
]
df = pd.DataFrame(rows)

# Method 3: From NumPy array — add column names manually
arr = np.array([[1, 2], [3, 4], [5, 6]])
df = pd.DataFrame(arr, columns=["col_A", "col_B"])

# Method 4: From CSV
df = pd.read_csv("data.csv")
```

> **Why it matters:** Every data task starts with creating or loading a DataFrame. Knowing multiple ways shows practical experience.

---

### 18. What is the index in a DataFrame — and can you change it?

**Answer:**
The index is the **row label** — like a row ID. By default it's 0, 1, 2... but it can be anything.

```python
df = pd.DataFrame({"name": ["Alice", "Bob"], "age": [25, 30]})

print(df.index)    # RangeIndex(start=0, stop=2, step=1)

# Set a column as index:
df = df.set_index("name")
print(df)
#        age
# name
# Alice   25
# Bob     30

# Now access by name instead of position:
df.loc["Alice"]    # age = 25

# Reset back to default 0,1,2:
df = df.reset_index()

# Set index when loading CSV:
df = pd.read_csv("data.csv", index_col="employee_id")
```

> **Why it matters:** Index controls how `loc` works and how DataFrames join/merge. Wrong index causes misalignment in merge operations.

---

### 19. What is the difference between `loc` and `iloc`?

**Answer:**
- `loc` — select by **label** (index name, column name). End is **inclusive**.
- `iloc` — select by **integer position** (0,1,2...). End is **exclusive**.

```python
df = pd.DataFrame(
    {"score": [85, 90, 78, 92]},
    index=["alice", "bob", "carol", "dave"]
)

# loc — by label
df.loc["bob"]              # row labeled "bob"
df.loc["alice":"carol"]    # alice, bob, carol ← ALL THREE included

# iloc — by position
df.iloc[1]                 # row at position 1 (bob)
df.iloc[0:3]               # positions 0,1,2 ← dave NOT included

# Selecting rows AND columns:
df.loc["alice":"bob", "score"]     # rows alice-bob, score column
df.iloc[0:2, 0]                    # rows 0-1, first column

# THE TRAP — when index is 0,1,2 (default):
df2 = pd.DataFrame({"val": [10, 20, 30, 40]})
df2.loc[0:2]     # rows 0,1,2 ← 3 rows (inclusive)
df2.iloc[0:2]    # rows 0,1   ← 2 rows (exclusive)
# Same-looking code, different results!
```

> **Why it matters:** The inclusive vs exclusive difference with default integer index is a classic trap — even experienced developers get caught by it.

---

### 20. What does `df.info()` show vs `df.describe()`?

**Answer:**
- `info()` — shows **structure**: column names, non-null counts, dtypes, memory usage.
- `describe()` — shows **statistics**: mean, std, min, max, quartiles.

```python
df = pd.DataFrame({
    "name":   ["Alice", "Bob", None],
    "age":    [25, 30, 22],
    "salary": [50000.0, 80000.0, None]
})

df.info()
# RangeIndex: 3 entries, 0 to 2
# Column  Non-Null Count  Dtype
# name    2 non-null      object   ← spotted the None!
# age     3 non-null      int64
# salary  2 non-null      float64  ← spotted the None!
# memory usage: ...

df.describe()
#         age       salary
# count   3.0          2.0   ← only 2 non-null salary values
# mean   25.67     65000.0
# std     4.04     21213.2
# min    22.0      50000.0
# 25%    23.5      57500.0
# 50%    25.0      65000.0
# max    30.0      80000.0
```

> **Why it matters:** Run these two first on any new dataset. `info()` spots missing values and wrong dtypes. `describe()` spots outliers and skewed distributions.

---

### 21. What is the difference between `dropna()` and `fillna()`?

**Answer:**
Both handle missing values but differently:
- `dropna()` — **removes** rows/columns with missing values.
- `fillna()` — **replaces** missing values with something.

```python
df = pd.DataFrame({
    "name":   ["Alice", "Bob", "Carol"],
    "age":    [25, None, 30],
    "city":   [None, "Mumbai", "Delhi"]
})

# dropna — removes any row that has at least one NaN
df.dropna()
#     name   age   city
# 2  Carol  30.0  Delhi  ← only row with no missing values

# dropna with threshold — keep rows with at least N non-null values
df.dropna(thresh=2)   # keep rows where at least 2 columns are non-null

# fillna — replace NaN with a value
df.fillna("Unknown")          # fill ALL NaNs with "Unknown"
df["age"].fillna(df["age"].mean())  # fill age NaNs with mean age
df.fillna({"age": 0, "city": "Unknown"})  # different fill per column
```

> **Why it matters:** Dropping loses data; filling introduces assumptions. Choosing wrong damages your analysis. This choice is made constantly in real projects.

---

### 22. What does `inplace=True` do?

**Answer:**
`inplace=True` modifies the DataFrame **directly** instead of returning a new one. Without it, the original is unchanged.

```python
df = pd.DataFrame({"A": [3, 1, 2], "B": [6, 4, 5]})

# Without inplace — original unchanged, must reassign:
df_sorted = df.sort_values("A")    # returns new sorted DataFrame
print(df)         # still original order [3,1,2]

# With inplace — modifies df directly:
df.sort_values("A", inplace=True)
print(df)         # now sorted [1,2,3] — no reassignment needed

# Same for other operations:
df.drop(columns=["B"], inplace=True)
df.rename(columns={"A": "values"}, inplace=True)
df.reset_index(inplace=True, drop=True)
```

> **Why it matters:** Forgetting to reassign when `inplace=False` (default) is a common bug — you think the DataFrame changed but it didn't.

---

### 23. What is the difference between `df["col"]` and `df[["col"]]`?

**Answer:**
- `df["col"]` — single brackets → returns a **Series** (1D)
- `df[["col"]]` — double brackets → returns a **DataFrame** (2D)

```python
df = pd.DataFrame({"name": ["Alice", "Bob"], "age": [25, 30]})

# Single bracket — Series
col_series = df["name"]
print(type(col_series))    # Series
print(col_series.shape)    # (2,)        ← 1D

# Double bracket — DataFrame
col_df = df[["name"]]
print(type(col_df))        # DataFrame
print(col_df.shape)        # (2, 1)      ← 2D, one column

# Why it matters practically:
# Some functions require DataFrame input, not Series
# ML libraries like sklearn expect 2D input (DataFrame/array)

# Multiple columns — must use double brackets:
df[["name", "age"]]        # DataFrame with 2 columns ✅
df["name", "age"]          # KeyError ❌ — wrong syntax
```

> **Why it matters:** Passing a Series to a function that expects a DataFrame causes errors. This trips up beginners constantly.

---

### 24. What does `groupby()` return before you apply a function?

**Answer:**
`groupby()` alone returns a **GroupBy object** — it hasn't computed anything yet. It only runs when you call an aggregation on it.

```python
df = pd.DataFrame({
    "dept":   ["HR", "Tech", "HR", "Tech"],
    "salary": [40000, 80000, 45000, 90000]
})

# groupby alone — lazy, nothing computed yet
grouped = df.groupby("dept")
print(grouped)    # <DataFrameGroupBy object at 0x...> ← just a blueprint

# Now apply aggregation — computation happens here
grouped["salary"].mean()
# dept
# HR      42500.0
# Tech    85000.0

# Common pattern — chain it directly:
df.groupby("dept")["salary"].mean()    # same result
df.groupby("dept")["salary"].sum()
df.groupby("dept")["salary"].count()
df.groupby("dept").agg({"salary": ["mean", "max"]})  # multiple stats at once
```

> **Why it matters:** Understanding lazy evaluation is key — GroupBy delays computation until needed, which is why it's efficient on large datasets.

---

### 25. What is the difference between `apply()` and `map()`?

**Answer:**
- `map()` — works on a **Series only**, element by element. Simple substitution.
- `apply()` — works on **Series or DataFrame**, handles complex logic.

```python
df = pd.DataFrame({"score": [45, 72, 88, 55, 91], "age": [22, 25, 30, 28, 24]})

# map() — Series only, simple transformation
df["score"].map(lambda x: "pass" if x >= 50 else "fail")
# 0    fail
# 1    pass
# 2    pass ...

# map() also works for value substitution:
df["score"].map({45: "low", 72: "mid", 88: "high"})  # dict mapping

# apply() — same on Series:
df["score"].apply(lambda x: "pass" if x >= 50 else "fail")

# apply() on DataFrame — row by row with axis=1:
df["category"] = df.apply(
    lambda row: "senior" if row["age"] > 25 and row["score"] > 70 else "junior",
    axis=1   # process each ROW (axis=0 would process each column)
)
```

> **Why it matters:** `apply()` with `axis=1` lets you combine multiple columns in logic — something `map()` can't do.

---

### 26. What does `value_counts()` return?

**Answer:**
`value_counts()` counts how many times each **unique value** appears. Returns a Series sorted by frequency (highest first).

```python
df = pd.DataFrame({
    "city": ["Delhi", "Mumbai", "Delhi", "Bangalore", "Mumbai", "Delhi"]
})

df["city"].value_counts()
# Delhi        3
# Mumbai       2
# Bangalore    1

# As percentages:
df["city"].value_counts(normalize=True)
# Delhi        0.500
# Mumbai       0.333
# Bangalore    0.167

# Include NaN in count:
df["city"].value_counts(dropna=False)

# Sort by value instead of frequency:
df["city"].value_counts().sort_index()   # alphabetical order
```

> **Why it matters:** First thing to run on any categorical column. Instantly shows class imbalance, typos ("delhi" vs "Delhi"), unexpected categories.

---

### 27. What is the difference between `merge()` and `concat()`?

**Answer:**
- `merge()` — joins on **matching column values** (like SQL JOIN). Horizontal combination based on a key.
- `concat()` — stacks DataFrames **vertically or horizontally**. No matching required.

```python
df1 = pd.DataFrame({"id": [1, 2, 3], "name": ["Alice", "Bob", "Carol"]})
df2 = pd.DataFrame({"id": [1, 2, 4], "salary": [50000, 60000, 70000]})

# merge — like SQL JOIN, matches on 'id' column
pd.merge(df1, df2, on="id", how="inner")
#    id   name  salary
# 0   1  Alice   50000    ← id 3 dropped (no match), id 4 dropped (no match)
# 1   2    Bob   60000

pd.merge(df1, df2, on="id", how="left")
#    id   name   salary
# 0   1  Alice  50000.0
# 1   2    Bob  60000.0
# 2   3  Carol      NaN  ← id 3 kept, salary is NaN (no match in df2)

# concat — stack, no key matching
pd.concat([df1, df2], axis=0)   # vertical stack (add more rows)
pd.concat([df1, df2], axis=1)   # horizontal stack (add more columns side by side)
```

> **Why it matters:** Wrong join type silently drops rows or creates duplicates. This is the most common data bug when combining tables.

---

### 28. What does `astype()` do and when do you use it?

**Answer:**
`astype()` converts a column's **data type**. Used when data is loaded with the wrong type (numbers as strings, etc.).

```python
df = pd.read_csv("data.csv")
df.dtypes
# age       object   ← should be int, loaded as string!
# salary    object   ← should be float
# active    int64    ← should be bool

# Fix dtypes:
df["age"]    = df["age"].astype(int)
df["salary"] = df["salary"].astype(float)
df["active"] = df["active"].astype(bool)

# Convert to category — for low-cardinality string columns:
df["city"] = df["city"].astype("category")
# Saves memory + speeds up groupby on that column

# Convert int to smaller int to save memory:
df["age"] = df["age"].astype("int8")   # values fit in -128 to 127

# Check result:
df.dtypes   # verify the conversions worked
```

> **Why it matters:** Math on a column stored as string silently fails or gives wrong results. `astype()` is the fix.

---

### 29. What is a categorical dtype and why use it?

**Answer:**
`category` dtype is for columns with **few unique values** that repeat a lot (gender, city, status). Pandas stores them as integers internally — faster and smaller.

```python
df = pd.DataFrame({
    "city":   ["Delhi", "Mumbai", "Delhi", "Mumbai", "Delhi"] * 100000,  # 500k rows
    "gender": ["M", "F", "M", "F", "M"] * 100000
})

# Before category:
print(df["city"].dtype)           # object — stores full string every row
print(df.memory_usage(deep=True)) # high memory

# After category:
df["city"]   = df["city"].astype("category")
df["gender"] = df["gender"].astype("category")

# Internally Pandas does:
# "Delhi" → 0, "Mumbai" → 1  (stores integers, not strings)
# Then keeps a small lookup: {0: "Delhi", 1: "Mumbai"}

print(df.memory_usage(deep=True)) # much lower memory!

# Bonus — groupby on category columns is faster:
df.groupby("city")["gender"].value_counts()   # noticeably faster on large data
```

> **Why it matters:** On 1M+ row datasets, wrong dtypes cause out-of-memory crashes. `category` is the first optimization to apply.

---

### 30. What is the difference between `ffill()` and `bfill()`?

**Answer:**
Both fill missing values but from different directions:
- `ffill()` (forward fill) — fills with the **previous valid value**
- `bfill()` (backward fill) — fills with the **next valid value**

```python
df = pd.DataFrame({
    "date":  ["Mon", "Tue", "Wed", "Thu", "Fri"],
    "temp":  [30, None, None, 28, None]
})

# Original:  [30, NaN, NaN, 28, NaN]

# ffill — carry last known value forward:
df["temp"].ffill()
# [30, 30, 30, 28, 28]   ← NaN filled with previous value

# bfill — pull next known value backward:
df["temp"].bfill()
# [30, 28, 28, 28, NaN]  ← NaN filled with next value
#                           last NaN stays — no future value exists

# fillna with fixed value — fill everything with one value:
df["temp"].fillna(0)
# [30, 0, 0, 28, 0]

# Which to use when:
# Time-series sensor data    → ffill (last known reading makes sense)
# Survey data with gaps      → fillna(mean) (no directional logic)
# Future-known data (rare)   → bfill
```

> **Why it matters:** For time-series (stock prices, IoT sensor data, weather), `ffill` is the most realistic fill strategy. Using `fillna(mean)` on time-series introduces artificial patterns.

---

*Good luck with the interview — nail the basics first.*
