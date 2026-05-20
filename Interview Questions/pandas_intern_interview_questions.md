# Pandas – 20 Intern Interview Questions

---

## 1. What is the difference between a Series and a DataFrame?

**Answer:**
- **Series** — 1D, like a single column with an index.
- **DataFrame** — 2D, like a table with rows and columns.

```python
import pandas as pd

# Series — one column
s = pd.Series([10, 20, 30], index=["a", "b", "c"])
print(s)
# a    10
# b    20
# c    30

# DataFrame — multiple columns
df = pd.DataFrame({"name": ["Alice", "Bob"], "age": [25, 30]})
print(df)
#     name  age
# 0  Alice   25
# 1    Bob   30
```

> **Why it matters:** Every Pandas operation either outputs a Series or a DataFrame. Knowing which one you're working with prevents attribute errors.

---

## 2. What is the difference between `loc[]` and `iloc[]`?

**Answer:**
- `loc[]` — selects by **label** (column name, index name).
- `iloc[]` — selects by **integer position** (0, 1, 2...).

```python
df = pd.DataFrame({"score": [85, 90, 78]}, index=["alice", "bob", "carol"])

df.loc["bob"]       # Select row by label name "bob"
df.iloc[1]          # Select row at position 1 (same row, different method)

# Slicing — loc is INCLUSIVE on both ends, iloc is EXCLUSIVE on the end
df.loc["alice":"bob"]    # Returns alice AND bob
df.iloc[0:2]             # Returns position 0 and 1 — bob NOT included
```

> **Why it matters:** Using `iloc` when you meant `loc` gives wrong rows silently — a classic intern mistake during data extraction.

---

## 3. How do you handle missing values in Pandas?

**Answer:**
Three steps: **detect**, **decide**, then **act** (drop or fill).

```python
df = pd.DataFrame({"age": [25, None, 30], "city": ["Delhi", None, "Mumbai"]})

# Step 1: Detect
df.isnull()          # True where value is missing
df.isnull().sum()    # Count of missing values per column
df.notnull()         # Opposite — True where value exists

# Step 2A: Drop rows with ANY missing value
df.dropna()

# Step 2B: Drop only if ALL values in the row are missing
df.dropna(how="all")

# Step 3: Fill missing values instead of dropping
df.fillna(0)                        # Fill with a fixed value
df["age"].fillna(df["age"].mean())  # Fill with column mean — common in ML
```

> **Why it matters:** Real datasets always have missing values. Dropping blindly loses data; filling badly introduces bias. Knowing both options matters.

---

## 4. What does `describe()` tell you, and when would you use it?

**Answer:**
`describe()` gives a quick statistical summary: count, mean, std, min, max, and quartiles — for all numeric columns at once.

```python
df = pd.DataFrame({"age": [22, 35, 28, 41, 19], "salary": [30000, 80000, 50000, 120000, 25000]})

df.describe()
#         age       salary
# count   5.0          5.0
# mean   29.0      61000.0
# std     8.6      38000.0
# min    19.0      25000.0
# 25%    22.0      30000.0
# 50%    28.0      50000.0   ← median
# 75%    35.0      80000.0
# max    41.0     120000.0
```

> **Why it matters:** First thing you run after loading a dataset. Spots outliers, skewed distributions, and wrong data types immediately.

---

## 5. What is the difference between `drop()` and filtering with a boolean condition?

**Answer:**
- `drop()` removes rows/columns by **label**.
- Boolean filtering keeps rows that **match a condition**.

```python
df = pd.DataFrame({"name": ["Alice", "Bob", "Carol"], "age": [25, 17, 30]})

# drop() — remove by index label or column name
df.drop(index=1)              # Remove row at label 1 (Bob)
df.drop(columns=["age"])      # Remove the age column

# Boolean filter — keep rows where condition is True
df[df["age"] >= 18]           # Keep only adults
```

> **Why it matters:** `drop()` is for removing known labels. Filtering is for removing based on data content. They solve different problems.

---

## 6. How do you filter rows with multiple conditions?

**Answer:**
Use `&` (AND) and `|` (OR) with parentheses around **each condition**. Python's `and`/`or` don't work here.

```python
df = pd.DataFrame({
    "age":    [22, 35, 17, 41],
    "salary": [30000, 80000, 15000, 120000],
    "city":   ["Delhi", "Mumbai", "Delhi", "Bangalore"]
})

# Both conditions must be True
df[(df["age"] >= 18) & (df["salary"] > 50000)]

# Either condition can be True
df[(df["city"] == "Delhi") | (df["salary"] > 100000)]

# NOT condition
df[~(df["city"] == "Delhi")]   # Everyone NOT in Delhi
```

> **Why it matters:** Forgetting parentheses around each condition causes a cryptic operator precedence error — very common beginner mistake.

---

## 7. What does `groupby()` do, and how do you use it with `agg()`?

**Answer:**
`groupby()` splits the data into groups and lets you apply a function to each group. `agg()` lets you apply **multiple functions at once**.

```python
df = pd.DataFrame({
    "department": ["HR", "Tech", "HR", "Tech", "Tech"],
    "salary":     [40000, 80000, 45000, 90000, 95000],
    "age":        [30, 25, 35, 28, 32]
})

# Simple groupby — average salary per department
df.groupby("department")["salary"].mean()

# agg() — multiple stats in one shot
df.groupby("department").agg(
    avg_salary=("salary", "mean"),   # mean salary
    max_age=("age", "max"),          # oldest person
    headcount=("salary", "count")    # number of people
)
```

> **Why it matters:** Summarising data by category is one of the most frequent real-world tasks — sales by region, performance by team, etc.

---

## 8. What is `value_counts()` and when do you use it?

**Answer:**
`value_counts()` counts how many times each unique value appears in a column. Sorted by frequency by default.

```python
df = pd.DataFrame({"city": ["Delhi", "Mumbai", "Delhi", "Bangalore", "Mumbai", "Delhi"]})

df["city"].value_counts()
# Delhi        3
# Mumbai       2
# Bangalore    1

# As percentages instead
df["city"].value_counts(normalize=True)
# Delhi        0.50
# Mumbai       0.33
# Bangalore    0.17
```

> **Why it matters:** First thing to run on a categorical column — spots class imbalance, typos, and unexpected categories instantly.

---

## 9. What is the difference between `apply()` and `map()`?

**Answer:**
- `map()` — works on a **Series**, element by element. For simple value substitution.
- `apply()` — works on a **Series or DataFrame**, can handle complex logic.

```python
df = pd.DataFrame({"score": [45, 72, 88, 55, 91]})

# map() — simple value transformation on a Series
df["score"].map(lambda x: "pass" if x >= 50 else "fail")

# apply() — same on Series, but also works row/column-wise on DataFrame
df["score"].apply(lambda x: "pass" if x >= 50 else "fail")

# apply() on full DataFrame — axis=1 means row by row
df["grade"] = df.apply(
    lambda row: "A" if row["score"] >= 80 else "B",
    axis=1   # process each row, not each column
)
```

> **Why it matters:** `applymap()` (now `df.map()` in newer Pandas) is for element-wise on entire DataFrames. Knowing which to use avoids errors.

---

## 10. What does `pivot_table()` do?

**Answer:**
`pivot_table()` reshapes data — rows become one category, columns become another, and values are aggregated (sum, mean, etc.).

```python
df = pd.DataFrame({
    "month":      ["Jan", "Jan", "Feb", "Feb"],
    "product":    ["A",   "B",   "A",   "B"],
    "revenue":    [1000,  1500,  1200,  1800]
})

# rows = month, columns = product, values = revenue, aggregated by sum
pivot = df.pivot_table(
    index="month",
    columns="product",
    values="revenue",
    aggfunc="sum"       # how to combine if multiple entries exist
)

# product     A     B
# month
# Feb      1200  1800
# Jan      1000  1500
```

> **Why it matters:** It's the Pandas equivalent of Excel pivot tables — used in every BI and reporting task.

---

## 11. What is the difference between `pd.merge()` and `df.join()`?

**Answer:**
- `pd.merge()` — joins on **column values** (like SQL JOIN). More flexible.
- `df.join()` — joins on **index** by default. Simpler but less flexible.

```python
df1 = pd.DataFrame({"emp_id": [1, 2, 3], "name": ["Alice", "Bob", "Carol"]})
df2 = pd.DataFrame({"emp_id": [1, 2, 4], "salary": [50000, 60000, 70000]})

# merge — like SQL inner join on emp_id column
pd.merge(df1, df2, on="emp_id", how="inner")  # Only matching emp_ids (1, 2)
pd.merge(df1, df2, on="emp_id", how="left")   # All from df1, NaN for missing

# concat — stack DataFrames vertically or horizontally
pd.concat([df1, df2], axis=0)   # Stack rows (vertical)
pd.concat([df1, df2], axis=1)   # Stack columns (horizontal)
```

> **Why it matters:** Combining data from multiple sources (tables, files) is a daily task. Wrong join type silently drops or duplicates rows.

---

## 12. How do you rename columns and change data types?

**Answer:**

```python
df = pd.DataFrame({"emp id": [1, 2], "age": ["25", "30"]})

# rename() — pass a dict: old name → new name
df.rename(columns={"emp id": "emp_id"}, inplace=True)
# inplace=True modifies df directly instead of returning a new one

# astype() — convert column data type
df["age"] = df["age"].astype(int)     # String "25" → integer 25
df["emp_id"] = df["emp_id"].astype(str)  # Integer → string

# Check types
df.dtypes
```

> **Why it matters:** Columns loaded from CSVs often have wrong types (numbers as strings). Math on string columns fails silently or throws errors.

---

## 13. How do you sort a DataFrame, and what does `nlargest()` do?

**Answer:**

```python
df = pd.DataFrame({
    "name":   ["Alice", "Bob", "Carol", "Dave"],
    "salary": [80000, 50000, 90000, 70000],
    "age":    [30, 25, 35, 28]
})

# Sort by one column
df.sort_values("salary")                        # Ascending (default)
df.sort_values("salary", ascending=False)       # Descending

# Sort by multiple columns — salary desc, then age asc as tiebreaker
df.sort_values(["salary", "age"], ascending=[False, True])

# nlargest / nsmallest — faster shortcut for top-N rows
df.nlargest(2, "salary")    # Top 2 highest salaries
df.nsmallest(2, "age")      # 2 youngest people
```

> **Why it matters:** Leaderboards, ranking, top-N reports — all use sorting. `nlargest()` is faster than sort + head for large data.

---

## 14. How do you handle duplicates in a DataFrame?

**Answer:**

```python
df = pd.DataFrame({
    "name":  ["Alice", "Bob", "Alice", "Carol"],
    "email": ["a@x.com", "b@x.com", "a@x.com", "c@x.com"]
})

# Check which rows are duplicates
df.duplicated()           # True for rows that are repeated
df.duplicated().sum()     # Count of duplicate rows

# Check duplicates based on specific column only
df.duplicated(subset=["email"])

# Remove duplicates — keeps first occurrence by default
df.drop_duplicates()

# Keep last occurrence instead
df.drop_duplicates(keep="last")

# Remove all occurrences (keep neither)
df.drop_duplicates(keep=False)
```

> **Why it matters:** Duplicate rows in a dataset silently skew counts, means, and model training. Always check early in EDA.

---

## 15. What does `str.contains()` do, and how do you use string operations in Pandas?

**Answer:**
Pandas has a `.str` accessor for running string operations on entire columns without loops.

```python
df = pd.DataFrame({"email": ["alice@gmail.com", "bob@yahoo.com", "carol@gmail.com"]})

# Filter rows where email contains a pattern
df[df["email"].str.contains("gmail")]      # Only gmail users

# Other useful string operations
df["email"].str.lower()                    # Lowercase all
df["email"].str.upper()                    # Uppercase all
df["email"].str.strip()                    # Remove leading/trailing spaces
df["email"].str.replace("@gmail.com", "") # Replace substring
df["email"].str.split("@")                # Split into list ["alice", "gmail.com"]
df["email"].str.startswith("alice")       # True/False per row
```

> **Why it matters:** Cleaning messy text columns (names, emails, addresses) is a constant real-world task. `.str` methods do it without any loop.

---

## 16. What is `pd.to_datetime()` and how do you extract date parts?

**Answer:**
`pd.to_datetime()` converts strings or numbers into proper datetime objects that Pandas understands. Then `.dt` accessor extracts parts.

```python
df = pd.DataFrame({"date": ["2024-01-15", "2024-03-22", "2023-11-08"]})

# Convert string column to datetime
df["date"] = pd.to_datetime(df["date"])

# Extract parts using .dt accessor
df["year"]        = df["date"].dt.year
df["month"]       = df["date"].dt.month
df["day"]         = df["date"].dt.day
df["day_of_week"] = df["date"].dt.dayofweek   # 0=Monday, 6=Sunday
df["month_name"]  = df["date"].dt.month_name() # "January", "March"...

# Filter rows for a specific year
df[df["date"].dt.year == 2024]
```

> **Why it matters:** Date columns loaded from CSV come in as strings. Without converting, you can't sort by date, calculate durations, or filter by time range.

---

## 17. What is `isin()` and when is it better than multiple OR conditions?

**Answer:**
`isin()` checks if each value belongs to a given list. Cleaner than chaining multiple `|` conditions.

```python
df = pd.DataFrame({
    "city":   ["Delhi", "Mumbai", "Chennai", "Kolkata", "Pune"],
    "sales":  [100, 200, 150, 80, 120]
})

# Multiple OR — gets messy fast
df[(df["city"] == "Delhi") | (df["city"] == "Mumbai") | (df["city"] == "Chennai")]

# isin() — same result, much cleaner
target_cities = ["Delhi", "Mumbai", "Chennai"]
df[df["city"].isin(target_cities)]

# NOT isin — exclude these cities
df[~df["city"].isin(target_cities)]
```

> **Why it matters:** When filtering on a list of allowed values (states, product codes, user IDs), `isin()` is the right tool.

---

## 18. What is `fillna()` vs `ffill()` vs `bfill()`?

**Answer:**
All three fill missing values, but differently:

- `fillna(value)` — fills with a **fixed value**.
- `ffill()` — fills with the **previous valid value** (forward fill).
- `bfill()` — fills with the **next valid value** (backward fill).

```python
df = pd.DataFrame({"temp": [30, None, None, 28, None, 25]})

df["temp"].fillna(0)      # [30, 0, 0, 28, 0, 25]  — not realistic for temperature

df["temp"].ffill()        # [30, 30, 30, 28, 28, 25] — carries last known value forward

df["temp"].bfill()        # [30, 28, 28, 28, 25, 25] — pulls next known value back
```

> **Why it matters:** For time-series data (stock prices, sensor readings), forward fill is more realistic than replacing with mean.

---

## 19. What does `dtype` optimization mean, and why does it matter?

**Answer:**
By default, Pandas uses `int64` and `float64` — these use more memory than needed. Downcasting and using `category` dtype reduces memory significantly.

```python
df = pd.DataFrame({
    "age":    [25, 30, 22, 41],
    "gender": ["M", "F", "M", "F"],
    "score":  [85.5, 90.2, 78.1, 91.4]
})

# Before optimization
print(df.dtypes)
# age      int64    ← uses 8 bytes per value
# gender   object   ← stored as Python strings (slow)
# score    float64  ← uses 8 bytes per value

# Optimize integer column — values fit in int8 (-128 to 127)
df["age"] = df["age"].astype("int8")

# Convert low-cardinality string column to category (few unique values)
df["gender"] = df["gender"].astype("category")
# Pandas stores "M"/"F" as integers internally — much faster and smaller

# Check memory usage
df.memory_usage(deep=True)
```

> **Why it matters:** On datasets with millions of rows, wrong dtypes cause out-of-memory crashes. `category` dtype makes `groupby` on string columns significantly faster.

---

## 20. What does `query()` do, and when is it preferred over boolean filtering?

**Answer:**
`query()` lets you filter rows using a **string expression** — cleaner syntax for complex conditions, especially in exploratory work.

```python
df = pd.DataFrame({
    "name":   ["Alice", "Bob", "Carol", "Dave"],
    "age":    [25, 17, 30, 42],
    "salary": [50000, 20000, 80000, 120000]
})

# Normal boolean filter — works but verbose
df[(df["age"] >= 18) & (df["salary"] > 50000)]

# query() — same result, reads like English
df.query("age >= 18 and salary > 50000")

# Use a Python variable inside query with @
min_age = 18
df.query("age >= @min_age and salary > 50000")
```

> **Why it matters:** `query()` is faster on large DataFrames (uses numexpr under the hood) and is much more readable when conditions pile up.

---

*Good luck with the interview!*
