# NumPy – 15 Intern Interview Questions

---

## 1. What is `np.arange()` and when would you use it over `np.linspace()`?

**Answer:**
`np.arange()` generates values with a fixed **step size**. `np.linspace()` generates a fixed **number of evenly spaced values** between two endpoints.

Use `np.arange()` when you know the step. Use `np.linspace()` when you know how many points you need.

```python
import numpy as np

np.arange(0, 10, 2)      # [0, 2, 4, 6, 8] — step of 2
np.linspace(0, 10, 5)    # [0, 2.5, 5, 7.5, 10] — exactly 5 points
```

> **Why it matters:** In ML/data tasks, you often need exact point counts (e.g., plotting), so `linspace` avoids off-by-one errors that `arange` can cause with floats.

---

## 2. What does `reshape()` do, and why does the total number of elements matter?

**Answer:**
`reshape()` changes the shape of an array **without changing its data**. The total number of elements must stay the same — you're just rearranging the "view", not the data itself.

```python
arr = np.arange(12)        # 12 elements, shape (12,)
arr_2d = arr.reshape(3, 4) # Now shape (3, 4) — still 12 elements

# This would FAIL — 12 elements can't fit into shape (3, 5) = 15 slots
# arr.reshape(3, 5)  → ValueError
```

> **Why it matters:** Reshaping is used constantly when feeding data into ML models (e.g., flattening images, adding batch dimensions).

---

## 3. What is the difference between `ndim`, `shape`, and `size`?

**Answer:**

| Property | What it tells you |
|----------|------------------|
| `ndim`   | Number of dimensions (axes) |
| `shape`  | Tuple of size along each axis |
| `size`   | Total number of elements |

```python
arr = np.zeros((3, 4, 2))

print(arr.ndim)   # 3 — it's a 3D array
print(arr.shape)  # (3, 4, 2)
print(arr.size)   # 24 — total elements (3 × 4 × 2)
```

> **Why it matters:** Debugging shape mismatches is one of the most common tasks in NumPy/ML code. Knowing these three saves time.

---

## 4. What is boolean masking and why is it useful?

**Answer:**
Boolean masking filters an array using a condition that returns `True/False` for each element. It avoids writing explicit loops.

```python
arr = np.array([10, 25, 3, 47, 8, 60])

mask = arr > 20          # [False, True, False, True, False, True]
result = arr[mask]       # [25, 47, 60] — only values where condition is True

# Shortcut — write it inline
result = arr[arr > 20]
```

> **Why it matters:** Filtering datasets without loops is faster and cleaner — this is bread-and-butter data cleaning work.

---

## 5. What is the `axis` parameter in functions like `np.sum()` or `np.mean()`?

**Answer:**
`axis` tells NumPy **which direction** to collapse when computing. Without it, the operation runs over the entire array.

```python
arr = np.array([[1, 2, 3],
                [4, 5, 6]])

np.sum(arr)          # 21 — sums everything
np.sum(arr, axis=0)  # [5, 7, 9] — sums DOWN each column (collapses rows)
np.sum(arr, axis=1)  # [6, 15]   — sums ACROSS each row (collapses columns)
```

> **Why it matters:** Averaging over samples vs. features in a dataset requires controlling axis — getting it wrong silently produces wrong results.

---

## 6. What is broadcasting, and what are its shape rules?

**Answer:**
Broadcasting lets NumPy do arithmetic on arrays with **different shapes** by virtually expanding the smaller one — without actually copying data.

Rules:
1. If shapes differ in number of dims, pad the shorter shape on the **left** with 1s.
2. Dimensions must either match or one of them must be 1.

```python
arr = np.array([[1, 2, 3],
                [4, 5, 6]])   # shape (2, 3)

scalar = np.array([10, 20, 30])  # shape (3,) → treated as (1, 3)

result = arr + scalar
# [[11, 22, 33],
#  [14, 25, 36]]
```

> **Why it matters:** Normalizing data row-by-row, adding bias terms, subtracting means — all rely on broadcasting.

---

## 7. What is the difference between a view and a copy in NumPy?

**Answer:**
- **View:** Points to the same memory. Changing it changes the original.
- **Copy:** Independent data. Changes don't affect the original.

Slicing creates a **view**. `np.copy()` creates a **copy**.

```python
arr = np.array([1, 2, 3, 4, 5])

view = arr[1:4]    # This is a VIEW
view[0] = 99       # Also changes arr!
print(arr)         # [1, 99, 3, 4, 5]

safe = arr[1:4].copy()  # Independent copy
safe[0] = 0             # arr is NOT affected
```

> **Why it matters:** Accidentally modifying source data through a view is a common silent bug, especially when preprocessing datasets.

---

## 8. What does `np.where()` do?

**Answer:**
`np.where(condition, x, y)` returns elements from `x` where condition is `True`, and from `y` where it's `False`. Think of it as a vectorized `if-else`.

```python
arr = np.array([5, -3, 8, -1, 0])

result = np.where(arr > 0, arr, 0)
# Replace negatives with 0: [5, 0, 8, 0, 0]

# Also works as: np.where(condition) → returns indices where True
indices = np.where(arr > 0)
# (array([0, 2]),) → positions 0 and 2 are positive
```

> **Why it matters:** Replaces conditional loops cleanly — used often in data cleaning and feature engineering.

---

## 9. What is `np.dot()` and how is it different from `*` multiplication?

**Answer:**
- `*` does **element-wise** multiplication (same shape required).
- `np.dot()` does **matrix multiplication** (dot product).

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

A * B        # Element-wise: [[5,12],[21,32]]
np.dot(A, B) # Matrix multiply: [[19,22],[43,50]]
```

> **Why it matters:** Neural network forward passes, linear regression predictions — all use dot products. Confusing the two gives wrong results with no error.

---

## 10. What does `flatten()` do, and how is it different from `ravel()`?

**Answer:**
Both convert multi-dimensional arrays to 1D, but:
- `flatten()` always returns a **copy**.
- `ravel()` returns a **view** when possible (faster, less memory).

```python
arr = np.array([[1, 2], [3, 4]])

flat = arr.flatten()   # Copy — safe to modify
rav  = arr.ravel()     # View — modifying it may affect arr
```

> **Why it matters:** Before feeding image data into a dense layer, you flatten it. Using `flatten()` is safer; `ravel()` is faster.

---

## 11. How do `np.stack()` and `np.concatenate()` differ?

**Answer:**
- `np.concatenate()` joins arrays **along an existing axis** (no new axis added).
- `np.stack()` joins arrays **along a new axis** (adds a dimension).

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

np.concatenate([a, b])      # [1, 2, 3, 4, 5, 6] — shape (6,)
np.stack([a, b])            # [[1,2,3],[4,5,6]]   — shape (2, 3)
np.stack([a, b], axis=1)    # [[1,4],[2,5],[3,6]] — shape (3, 2)
```

> **Why it matters:** Combining batches of data or building feature matrices requires knowing which one adds a dimension.

---

## 12. What is `np.random.seed()` and why is it used?

**Answer:**
Setting a seed makes random number generation **reproducible** — you get the same "random" numbers every run.

```python
np.random.seed(42)          # Fix the seed
print(np.random.rand(3))    # Always: [0.374, 0.951, 0.732]

np.random.seed(42)          # Reset to same seed
print(np.random.rand(3))    # Same output again
```

> **Why it matters:** ML experiments need reproducibility. Without a seed, results change every run, making debugging and comparison impossible.

---

## 13. What does `np.argmax()` return, and how is it different from `np.max()`?

**Answer:**
- `np.max()` returns the **highest value**.
- `np.argmax()` returns the **index** of the highest value.

```python
scores = np.array([0.1, 0.7, 0.05, 0.15])

np.max(scores)     # 0.7  — the value
np.argmax(scores)  # 1    — the position

# Works on 2D arrays too
matrix = np.array([[3, 9, 2], [8, 1, 5]])
np.argmax(matrix, axis=1)  # [1, 0] — index of max in each row
```

> **Why it matters:** In classification, a model outputs probability scores — `argmax` picks the predicted class index.

---

## 14. What are `np.std()` and `np.var()`, and what's the relationship between them?

**Answer:**
- `np.var()` is the **average of squared differences** from the mean.
- `np.std()` is the **square root of variance** — same unit as the data.

```python
data = np.array([2, 4, 4, 4, 5, 5, 7, 9])

mean = np.mean(data)    # 5.0
var  = np.var(data)     # 4.0
std  = np.std(data)     # 2.0 — because sqrt(4) = 2

# Verify the relationship
import numpy as np
assert np.isclose(np.sqrt(var), std)  # True
```

> **Why it matters:** Feature scaling (standardization) uses mean and std. Low std = values clustered together. High std = spread out.

---

## 15. What does `np.percentile()` do, and when would you use it over mean?

**Answer:**
`np.percentile(arr, q)` finds the value below which `q%` of the data falls.

Use percentiles when data has **outliers** — mean gets pulled by extremes, but median (50th percentile) stays stable.

```python
salaries = np.array([30000, 32000, 31000, 35000, 500000])  # One outlier

np.mean(salaries)              # 125600 — misleading
np.percentile(salaries, 50)    # 32000  — median, more realistic
np.percentile(salaries, 90)    # 500000 — top 10% earners
np.percentile(salaries, 25)    # 30500  — lower quartile (Q1)
```

> **Why it matters:** Used in EDA (exploratory data analysis) to understand data distribution without being misled by outliers.

---

*Good luck with the interview!*
