# 🐼 Pandas — Complete Guide: Under the Hood + Hands-On

> **How to use this file:** Read the theory first, then type every code example manually. Don’t copy-paste. Manual typing builds muscle memory and forces you to read each line.

-----

## 🧠 What is Pandas and WHY Does It Exist?

Imagine you have a CSV with 1 million rows of stock prices. You want to:

- Filter rows where price > 500
- Group by company
- Compute average price per group

In **pure Python**, you’d write nested loops, manual dict management, and type-checking for every column. It would be slow, verbose, and fragile.

**Pandas fixes all of this** by wrapping NumPy arrays in labeled, intelligent containers — giving you SQL-like power with Python syntax.

### Why is Pandas faster than Python loops?

```
Python loop approach:
  for row in data:             ← Python interpreter overhead each iteration
      if row['price'] > 500:   ← dictionary lookup, type check, every row
          result.append(row)   ← dynamic memory reallocation

Pandas approach:
  df[df['price'] > 500]
  → builds a boolean NumPy array in C (no Python loop)
  → uses that mask to index contiguous memory blocks
  → returns result in microseconds
```

Python loops have **interpreter overhead per iteration** — the interpreter must decode each bytecode instruction, check types, manage references. For 1 million rows, that’s 1 million cycles of overhead.

Pandas operations drop to C-level code via NumPy, skipping the interpreter entirely for the heavy lifting.

### Memory model

```
DataFrame in memory:

  Column 'age'     → NumPy int64 array    [25, 30, 45, ...]  ← contiguous int64 bytes
  Column 'salary'  → NumPy float64 array  [50k, 80k, 90k, ...]
  Column 'name'    → NumPy object array   [ptr→"Alice", ptr→"Bob", ...]
                                           ↑ strings are Python objects, slower

  Index            → NumPy int64 array    [0, 1, 2, 3, ...]  ← row labels
```

Each column is an independent NumPy array stored contiguously. This is **columnar storage** — when you operate on one column, you read one tight memory block, maximizing CPU cache efficiency.

-----

## 📦 Installation & Import

```bash
pip install pandas
```

```python
import pandas as pd
import numpy as np   # pandas depends on numpy internally
```

-----

-----

# 1. Core Data Structures

## Series — A labeled 1D array

Think of a Series as a NumPy array with an **index** (row labels) attached to it.

```
Series structure:
  Index  │  Values
  ───────┼──────────────────────
    0    │  10        ← index 0 maps to value 10
    1    │  20
    2    │  30
  ───────┴──────────────────────
  dtype: int64
```

```python
import pandas as pd
import numpy as np

# Create from a list — index defaults to 0, 1, 2...
s = pd.Series([10, 20, 30, 40])
print(s)
# 0    10
# 1    20
# 2    30
# 3    40
# dtype: int64

# Create with custom index (labels)
s2 = pd.Series([100, 200, 300], index=['a', 'b', 'c'])
print(s2)
# a    100
# b    200
# c    300

# Access by label
print(s2['b'])     # 200

# Access by position
print(s2.iloc[1])  # 200

# Series from a dict — keys become the index
s3 = pd.Series({'RELIANCE': 2800, 'TCS': 3500, 'INFY': 1500})
print(s3)
# RELIANCE    2800
# TCS         3500
# INFY        1500
```

> **Under the hood:** A Series is a thin Python wrapper around a NumPy ndarray + an Index object. The Index itself is also a NumPy array. When you do `s + 10`, it delegates to NumPy’s vectorized addition — no Python loop.

## DataFrame — A labeled 2D table

Think of a DataFrame as a dict of aligned Series — each column is a Series, all sharing the same index.

```
DataFrame structure:
  Index  │ name     │ age  │ salary
  ───────┼──────────┼──────┼────────
    0    │ "Alice"  │  25  │  50000
    1    │ "Bob"    │  30  │  80000
    2    │ "Carol"  │  45  │  90000
  ───────┴──────────┴──────┴────────
```

### Creating from a dict of lists

```python
data = {
    'name':   ['Alice', 'Bob', 'Carol', 'David'],
    'age':    [25, 30, 45, 28],
    'salary': [50000, 80000, 90000, 60000],
    'dept':   ['HR', 'IT', 'IT', 'Finance']
}

df = pd.DataFrame(data)
print(df)
#     name  age  salary     dept
# 0  Alice   25   50000       HR
# 1    Bob   30   80000       IT
# 2  Carol   45   90000       IT
# 3  David   28   60000  Finance

print(type(df))   # <class 'pandas.core.frame.DataFrame'>
```

### Creating from a list of dicts

```python
records = [
    {'city': 'Mumbai',  'population': 20.7, 'state': 'Maharashtra'},
    {'city': 'Delhi',   'population': 32.9, 'state': 'Delhi'},
    {'city': 'Kolkata', 'population': 14.9, 'state': 'West Bengal'},
]

df2 = pd.DataFrame(records)
print(df2)
```

### Custom index

```python
df3 = pd.DataFrame(
    {'score': [88, 92, 75]},
    index=['Aarav', 'Priya', 'Raj']
)
print(df3)
#        score
# Aarav     88
# Priya     92
# Raj       75
```

### Index basics

```python
df = pd.DataFrame({'val': [10, 20, 30]}, index=['x', 'y', 'z'])

print(df.index)     # Index(['x', 'y', 'z'], dtype='object')
print(df.columns)   # Index(['val'], dtype='object')
print(df.values)    # [[10] [20] [30]]  ← underlying NumPy array

# Reset index to default 0,1,2...
df_reset = df.reset_index()   # old index becomes a column
print(df_reset)
#   index  val
# 0     x   10
# 1     y   20
# 2     z   30

# Set a column as the index
df4 = pd.DataFrame({'name': ['Alice','Bob'], 'score': [88, 92]})
df4 = df4.set_index('name')
print(df4)
#        score
# name
# Alice     88
# Bob       92
```

-----

-----

# 2. Reading & Writing Data

## read_csv() — Load a CSV file

```python
# Basic usage
df = pd.read_csv('sales.csv')

# Common parameters
df = pd.read_csv(
    'sales.csv',
    sep=',',             # delimiter (use sep='\t' for TSV)
    header=0,            # row number to use as column names (0 = first row)
    index_col='id',      # column to use as row index
    usecols=['name','price','qty'],   # load only specific columns (saves memory!)
    nrows=1000,          # load only first 1000 rows
    skiprows=2,          # skip first 2 rows
    na_values=['NA', 'N/A', '-'],     # extra strings to treat as NaN
    dtype={'price': float, 'qty': int},  # force column types (faster than inference)
    encoding='utf-8',    # file encoding
)
```

> **Memory tip:** `usecols` is critical for large files. Loading 5 of 50 columns reads 10% of the data. `dtype` specification skips Pandas’ type inference pass — faster and uses less RAM.

## read_excel()

```python
df = pd.read_excel('report.xlsx', sheet_name='Sheet1')

# Load multiple sheets
sheets = pd.read_excel('report.xlsx', sheet_name=None)  # dict of DataFrames
```

## Writing data

```python
# Write to CSV (index=False avoids writing the row numbers as a column)
df.to_csv('output.csv', index=False)

# Write to Excel
df.to_excel('output.xlsx', sheet_name='Results', index=False)

# Write to JSON
df.to_json('output.json', orient='records')
```

## Quick inspection — always do these first

```python
# For demo, build a sample DataFrame
import pandas as pd
import numpy as np

np.random.seed(42)
df = pd.DataFrame({
    'product': ['A','B','C','D','E'] * 20,
    'price':   np.random.uniform(10, 500, 100).round(2),
    'qty':     np.random.randint(1, 50, 100),
    'region':  np.random.choice(['North','South','East','West'], 100)
})

print(df.head())        # first 5 rows
print(df.tail(3))       # last 3 rows
print(df.shape)         # (100, 4) — rows, columns
print(df.columns)       # column names
print(df.dtypes)        # dtype of each column
print(df.info())        # non-null counts + dtypes + memory usage
print(df.describe())    # count, mean, std, min, quartiles, max for numeric columns
```

`info()` output explained:

```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 100 entries, 0 to 99
Data columns (total 4 columns):
 #   Column   Non-Null Count  Dtype
---  ------   --------------  -----
 0   product  100 non-null    object    ← 'object' means Python strings, not efficient
 1   price    100 non-null    float64
 2   qty      100 non-null    int64
 3   region   100 non-null    object
memory usage: 3.2+ KB
```

-----

-----

# 3. Selecting Data

## Select a single column → returns a Series

```python
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Carol'],
    'age':  [25, 30, 45],
    'salary': [50000, 80000, 90000]
})

col = df['age']
print(type(col))   # <class 'pandas.core.series.Series'>
print(col)
# 0    25
# 1    30
# 2    45

# Dot notation also works (but only for simple column names, no spaces)
print(df.age)      # same result
```

## Select multiple columns → returns a DataFrame

```python
subset = df[['name', 'salary']]   # double brackets — pass a list
print(type(subset))   # <class 'pandas.core.frame.DataFrame'>
print(subset)
#     name  salary
# 0  Alice   50000
# 1    Bob   80000
# 2  Carol   90000
```

## loc[] — Label-based selection

`loc` uses the **index label** for rows and **column name** for columns.
Syntax: `df.loc[row_label, column_label]`
Both start and stop are **inclusive**.

```python
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Carol', 'David'],
    'age':  [25, 30, 45, 28],
    'salary': [50000, 80000, 90000, 60000]
}, index=['r0','r1','r2','r3'])

# Single row
print(df.loc['r1'])
# name        Bob
# age          30
# salary    80000

# Row range (inclusive on both ends!)
print(df.loc['r0':'r2'])

# Single cell
print(df.loc['r1', 'salary'])   # 80000

# Row range + specific columns
print(df.loc['r0':'r1', ['name', 'age']])

# Boolean array with loc (most common usage)
print(df.loc[df['age'] > 28])
```

## iloc[] — Position-based selection

`iloc` uses **integer positions** (like NumPy indexing). Stop is **exclusive**.

```python
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Carol', 'David'],
    'age':  [25, 30, 45, 28],
    'salary': [50000, 80000, 90000, 60000]
})

# Row by position
print(df.iloc[0])      # first row
print(df.iloc[-1])     # last row

# Row range (stop excluded)
print(df.iloc[1:3])    # rows 1 and 2

# Single cell
print(df.iloc[0, 2])   # row 0, column 2 → 50000

# Row + column ranges
print(df.iloc[0:2, 0:2])   # first 2 rows, first 2 columns

# Every other row
print(df.iloc[::2])
```

**loc vs iloc — when to use which:**

```
loc  → when you know the label:  df.loc['2024-01-15', 'price']
iloc → when you know the position: df.iloc[0, -1]
loc  → for boolean filtering:    df.loc[df['price'] > 100]
iloc → for numeric slicing:      df.iloc[:100]  (first 100 rows)
```

-----

-----

# 4. Filtering Rows

## Single condition

```python
df = pd.DataFrame({
    'name':   ['Alice', 'Bob', 'Carol', 'David', 'Eve'],
    'age':    [25, 30, 45, 28, 35],
    'salary': [50000, 80000, 90000, 60000, 75000],
    'dept':   ['HR', 'IT', 'IT', 'Finance', 'HR']
})

# Returns a boolean Series
mask = df['salary'] > 65000
print(mask)
# 0    False
# 1     True
# 2     True
# 3    False
# 4     True

# Apply mask to filter rows
print(df[mask])
# or in one line:
print(df[df['salary'] > 65000])
```

## Multiple conditions — use & and | (not ‘and’/‘or’)

```python
# AND condition — parentheses are REQUIRED around each condition
it_high_salary = df[(df['dept'] == 'IT') & (df['salary'] > 70000)]
print(it_high_salary)

# OR condition
hr_or_finance = df[(df['dept'] == 'HR') | (df['dept'] == 'Finance')]
print(hr_or_finance)

# NOT condition
not_it = df[~(df['dept'] == 'IT')]
print(not_it)

# Chained conditions
senior_hr = df[(df['dept'] == 'HR') & (df['age'] > 28)]
print(senior_hr)
```

> ⚠️ Why `&` not `and`? Python’s `and` operates on single truth values. `&` is NumPy’s element-wise bitwise AND on boolean arrays — which is what Pandas needs.

## isin() — Filter against a list of values

```python
# Instead of: df[(df['dept'] == 'IT') | (df['dept'] == 'HR')]
target_depts = ['IT', 'HR']
print(df[df['dept'].isin(target_depts)])

# Negation with ~
print(df[~df['dept'].isin(['Finance'])])
```

## str.contains() — Filter by substring

```python
products = pd.DataFrame({
    'product': ['iPhone 14', 'Samsung Galaxy', 'iPhone 15 Pro', 'OnePlus 11', 'iPad Pro'],
    'price':   [79000, 55000, 129000, 60000, 85000]
})

# Find all iPhones
print(products[products['product'].str.contains('iPhone')])

# Case-insensitive
print(products[products['product'].str.contains('iphone', case=False)])

# Using regex — starts with 'i'
print(products[products['product'].str.contains('^i', regex=True)])

# Combine with numeric filter
print(products[products['product'].str.contains('Pro') & (products['price'] > 80000)])
```

-----

-----

# 5. Handling Missing Data

## What is NaN?

`NaN` (Not a Number) is a special float64 value from IEEE 754. It is the standard way to represent “missing” in Pandas numeric columns.

```
NaN in memory: a specific bit pattern in float64 (0x7FF8000000000000)
Operations with NaN propagate NaN: NaN + 5 = NaN, NaN > 3 = False
Exception: np.nansum(), pd.Series.sum() skip NaN by default
```

For non-numeric columns (strings), Pandas uses `None` (Python object) or `pd.NA`.

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'name':   ['Alice', 'Bob', None,    'David'],
    'age':    [25,      np.nan, 45,     28],
    'salary': [50000,   80000,  np.nan, 60000]
})

print(df)
#     name   age   salary
# 0  Alice  25.0  50000.0
# 1    Bob   NaN  80000.0
# 2   None  45.0      NaN
# 3  David  28.0  60000.0
```

> Notice: when NaN is introduced into an int column, Pandas upgrades it to float64 — because NaN is a float concept. This is the old behavior; newer Pandas has `Int64` (nullable integer).

## Detecting missing values

```python
print(df.isnull())       # True where value is NaN/None
#     name    age  salary
# 0  False  False   False
# 1  False   True   False
# 2   True  False    True
# 3  False  False   False

print(df.notnull())      # opposite of isnull()

# Count missing per column
print(df.isnull().sum())
# name      1
# age       1
# salary    1

# Percentage missing
print((df.isnull().sum() / len(df) * 100).round(1))

# Any row with at least one NaN
print(df[df.isnull().any(axis=1)])
```

## dropna() — Remove missing values

```python
# Drop rows with ANY missing value
clean = df.dropna()
print(clean)

# Drop rows only if ALL values in that row are missing
df.dropna(how='all')

# Drop rows with NaN in specific columns only
df.dropna(subset=['age', 'salary'])

# Drop columns with any NaN
df.dropna(axis=1)
```

## fillna() — Fill missing values

```python
# Fill all NaN with a constant
df_filled = df.fillna(0)

# Fill each column differently
df_filled2 = df.fillna({
    'age':    df['age'].mean(),        # fill with column mean
    'salary': df['salary'].median(),   # fill with median
    'name':   'Unknown'                # fill with string
})
print(df_filled2)

# Forward fill — use the previous valid value
df_ffill = df.fillna(method='ffill')

# Backward fill — use the next valid value
df_bfill = df.fillna(method='bfill')
```

-----

-----

# 6. Adding & Modifying Data

## Adding new columns

```python
df = pd.DataFrame({
    'name':   ['Alice', 'Bob', 'Carol'],
    'salary': [50000, 80000, 90000],
    'bonus':  [5000, 10000, 15000]
})

# New column from arithmetic (vectorized — no loop)
df['total_comp'] = df['salary'] + df['bonus']

# New column from condition
df['is_senior'] = df['salary'] > 70000

# New column from function
df['salary_lakh'] = df['salary'] / 100000

print(df)
#     name  salary  bonus  total_comp  is_senior  salary_lakh
# 0  Alice   50000   5000       55000      False          0.5
# 1    Bob   80000  10000       90000       True          0.8
# 2  Carol   90000  15000      105000       True          0.9
```

## drop() — Remove columns or rows

```python
# Drop a column (axis=1 means column)
df2 = df.drop('bonus', axis=1)          # returns new DataFrame
df2 = df.drop(columns=['bonus'])        # cleaner syntax

# Drop multiple columns
df2 = df.drop(columns=['bonus', 'salary_lakh'])

# Drop rows by index label
df2 = df.drop(index=0)        # drop row with label 0
df2 = df.drop(index=[0, 2])   # drop rows 0 and 2

# inplace=True modifies the original (use with caution)
df.drop(columns=['bonus'], inplace=True)
```

## rename() — Rename columns or index

```python
df = pd.DataFrame({'nm': ['Alice','Bob'], 'sal': [50000, 80000]})

# Rename columns using a dict (old_name → new_name)
df = df.rename(columns={'nm': 'name', 'sal': 'salary'})
print(df)

# Rename index labels
df = df.rename(index={0: 'first', 1: 'second'})
print(df)
```

## astype() — Change column data type

```python
df = pd.DataFrame({
    'age':    ['25', '30', '45'],     # stored as strings (common after CSV read)
    'salary': [50000.0, 80000.0, 90000.0],
    'active': [1, 0, 1]
})

# Convert age from string to int
df['age'] = df['age'].astype(int)

# Convert salary from float to int
df['salary'] = df['salary'].astype(int)

# Convert to category (memory optimization — covered in topic 14)
df['active'] = df['active'].astype(bool)

print(df.dtypes)
# age       int64
# salary    int64
# active     bool
```

-----

-----

# 7. Sorting & Ranking

## sort_values() — Sort by column values

```python
df = pd.DataFrame({
    'name':   ['Carol', 'Alice', 'David', 'Bob', 'Eve'],
    'dept':   ['IT', 'HR', 'IT', 'Finance', 'HR'],
    'salary': [90000, 50000, 60000, 80000, 75000],
    'age':    [45, 25, 28, 30, 35]
})

# Sort by salary (ascending by default)
print(df.sort_values('salary'))

# Sort descending
print(df.sort_values('salary', ascending=False))

# Sort by multiple columns
# First by dept (A-Z), then within same dept by salary (high to low)
print(df.sort_values(
    by=['dept', 'salary'],
    ascending=[True, False]
))

# Sort and reset index
df_sorted = df.sort_values('salary', ascending=False).reset_index(drop=True)
print(df_sorted)
```

## sort_index() — Sort by index labels

```python
df2 = pd.DataFrame({'val': [30, 10, 20]}, index=['c', 'a', 'b'])
print(df2.sort_index())       # sorts index A-Z
print(df2.sort_index(ascending=False))  # Z-A
```

## nlargest() and nsmallest()

```python
# Top 3 by salary (faster than sort + head for large DataFrames)
print(df.nlargest(3, 'salary'))

# Bottom 2 by age
print(df.nsmallest(2, 'age'))

# nlargest on a Series
print(df['salary'].nlargest(3))
```

-----

-----

# 8. Grouping & Aggregation

## groupby() — The SQL GROUP BY of Pandas

`groupby` is a three-phase operation:

1. **Split** — divide DataFrame into groups based on key column(s)
1. **Apply** — run an aggregation function on each group independently
1. **Combine** — collect results into a new DataFrame

```
Original:
  dept     salary
  IT       80000
  HR       50000
  IT       90000
  HR       75000

After groupby('dept'):
  Group 'HR':   [50000, 75000]  → mean → 62500
  Group 'IT':   [80000, 90000]  → mean → 85000

Result:
  dept   salary
  HR     62500
  IT     85000
```

```python
df = pd.DataFrame({
    'dept':   ['IT', 'HR', 'IT', 'Finance', 'HR', 'IT', 'Finance'],
    'salary': [80000, 50000, 90000, 60000, 75000, 70000, 65000],
    'age':    [30, 25, 45, 28, 35, 32, 40],
    'name':   ['Bob','Alice','Carol','David','Eve','Frank','Grace']
})

# Mean salary per department
print(df.groupby('dept')['salary'].mean())
# dept
# Finance    62500.0
# HR         62500.0
# IT         80000.0

# Count employees per department
print(df.groupby('dept')['name'].count())

# Multiple aggregations at once
print(df.groupby('dept')['salary'].agg(['mean', 'min', 'max', 'count']))

# Group by multiple columns
print(df.groupby(['dept'])['salary', 'age'].mean())
```

## agg() — Custom aggregations

```python
# Different aggregations per column
result = df.groupby('dept').agg({
    'salary': ['mean', 'max'],
    'age':    'min',
    'name':   'count'
})
print(result)

# Named aggregations (cleaner output)
result2 = df.groupby('dept').agg(
    avg_salary=('salary', 'mean'),
    max_salary=('salary', 'max'),
    headcount=('name',   'count')
)
print(result2)
```

## value_counts() — Count occurrences

```python
# Count how many employees in each dept
print(df['dept'].value_counts())
# IT         3
# HR         2
# Finance    2

# As percentages
print(df['dept'].value_counts(normalize=True).round(3))
# IT         0.429
# HR         0.286
# Finance    0.286

# Include NaN in counts
print(df['dept'].value_counts(dropna=False))
```

## pivot_table() — Excel-style pivot

```python
df2 = pd.DataFrame({
    'region': ['North','North','South','South','East','East'],
    'product':['A','B','A','B','A','B'],
    'sales':  [100, 200, 150, 120, 90, 300],
    'units':  [10,   20,  15,  12,   9,  30]
})

# Mean sales by region (rows) and product (columns)
pivot = pd.pivot_table(
    df2,
    values='sales',
    index='region',
    columns='product',
    aggfunc='mean',
    fill_value=0,        # fill NaN with 0
    margins=True         # add row/column totals
)
print(pivot)
# product      A      B    All
# region
# East        90    300    195
# North      100    200    150
# South      150    120    135
# All        113    207    160
```

-----

-----

# 9. String Operations

String operations via `.str` accessor avoid Python loops — they iterate in optimized C code over the object array.

```python
df = pd.DataFrame({
    'name':    ['  alice SMITH ', 'BOB jones  ', 'Carol White'],
    'email':   ['alice@gmail.com', 'bob@yahoo.com', 'carol@gmail.com'],
    'product': ['iPhone 14 Pro', 'Samsung Galaxy S23', 'iPad mini']
})

# Cleaning
df['name_clean'] = df['name'].str.strip()         # remove leading/trailing spaces
df['name_lower'] = df['name'].str.strip().str.lower()
df['name_upper'] = df['name'].str.strip().str.upper()
df['name_title'] = df['name'].str.strip().str.title()   # Title Case

print(df[['name', 'name_clean', 'name_lower', 'name_title']])

# Splitting
# str.split returns a Series of lists
parts = df['email'].str.split('@')
print(parts)
# 0    [alice, gmail.com]
# 1    [bob, yahoo.com]
# 2    [carol, gmail.com]

# Extract specific part
df['domain'] = df['email'].str.split('@').str[1]
print(df['domain'])
# 0    gmail.com
# 1    yahoo.com
# 2    gmail.com

# Replacement
df['product_clean'] = df['product'].str.replace('Pro', 'PRO', regex=False)

# Check patterns
print(df['email'].str.endswith('.com'))
print(df['email'].str.startswith('alice'))
print(df['product'].str.contains('iPhone|iPad', regex=True))

# String length
print(df['product'].str.len())

# Slice characters
print(df['name'].str.strip().str[:3])   # first 3 characters
```

-----

-----

# 10. Applying Functions

## apply() — Apply a function to rows or columns

`apply` is more flexible than built-in aggregations but slower — it uses a Python-level loop internally. Use vectorized operations first; reach for `apply` only when no vectorized alternative exists.

```python
df = pd.DataFrame({
    'salary': [50000, 80000, 90000, 60000, 75000],
    'bonus':  [5000, 10000, 15000, 8000, 9000],
    'name':   ['Alice', 'Bob', 'Carol', 'David', 'Eve']
})

# Apply to a single column (Series)
def tax_bracket(salary):
    if salary > 80000:
        return 'High'
    elif salary > 60000:
        return 'Medium'
    else:
        return 'Low'

df['tax_bracket'] = df['salary'].apply(tax_bracket)

# Lambda (anonymous function) — for simple operations
df['salary_k'] = df['salary'].apply(lambda x: x / 1000)

# Apply across rows (axis=1) — receives each row as a Series
df['total'] = df.apply(lambda row: row['salary'] + row['bonus'], axis=1)
# Better version (vectorized):
df['total_fast'] = df['salary'] + df['bonus']   # prefer this!

# Apply to each column (axis=0 — default)
print(df[['salary','bonus']].apply(np.sum))    # sum of each column
```

## map() — Element-wise mapping on a Series

`map` is for replacing/transforming values using a dict or function.

```python
# Map values using a dict
df['dept'] = pd.Series(['IT', 'HR', 'IT', 'Finance', 'HR'])
dept_code = {'IT': 1, 'HR': 2, 'Finance': 3}
df['dept_code'] = df['dept'].map(dept_code)
print(df[['dept', 'dept_code']])

# Map using a function (applies to each element)
df['name_upper'] = df['name'].map(str.upper)
```

## df.map() (formerly applymap) — Element-wise on whole DataFrame

```python
# Apply a function to every single cell in the DataFrame
numeric_df = pd.DataFrame({'a': [1.234, 2.567], 'b': [3.891, 4.123]})

# Round every cell to 1 decimal place
rounded = numeric_df.map(lambda x: round(x, 1))
print(rounded)
#      a    b
# 0  1.2  3.9
# 1  2.6  4.1
```

**Performance hierarchy (fastest → slowest):**

```
1. Vectorized operations:  df['col'] * 2            ← C-speed, always prefer
2. NumPy ufuncs:           np.sqrt(df['col'])        ← nearly as fast
3. .str / .dt accessors:   df['col'].str.upper()     ← optimized loops
4. .map() on Series:       df['col'].map(func)       ← Python loop per element
5. .apply(axis=0):         df.apply(func)            ← Python loop per column
6. .apply(axis=1):         df.apply(func, axis=1)   ← Python loop per row — SLOWEST
```

-----

-----

# 11. Merging & Combining

## pd.merge() — SQL-style join

```python
employees = pd.DataFrame({
    'emp_id': [1, 2, 3, 4],
    'name':   ['Alice', 'Bob', 'Carol', 'David'],
    'dept_id': [10, 20, 10, 30]
})

departments = pd.DataFrame({
    'dept_id':   [10, 20, 40],
    'dept_name': ['IT', 'HR', 'Finance']
})

# INNER JOIN — only rows with matching dept_id in BOTH tables
inner = pd.merge(employees, departments, on='dept_id', how='inner')
print(inner)
#    emp_id   name  dept_id dept_name
# 0       1  Alice       10        IT
# 1       3  Carol       10        IT
# 2       2    Bob       20        HR
# David (dept_id=30) dropped — no match in departments

# LEFT JOIN — all employees, NaN for unmatched departments
left = pd.merge(employees, departments, on='dept_id', how='left')
print(left)
# David gets NaN for dept_name

# OUTER JOIN — all rows from both tables, NaN for non-matches
outer = pd.merge(employees, departments, on='dept_id', how='outer')

# Join on columns with different names
# employees has 'dept_id', departments has 'id'
# pd.merge(employees, departments, left_on='dept_id', right_on='id')

# Suffix for overlapping column names
sales = pd.DataFrame({'emp_id':[1,2], 'amount':[1000,2000], 'date':['2024-01','2024-01']})
targets = pd.DataFrame({'emp_id':[1,2], 'amount':[900,2500]})
merged = pd.merge(sales, targets, on='emp_id', suffixes=('_actual','_target'))
print(merged)
```

**Join types visual:**

```
employees:  [1-Alice-IT] [2-Bob-HR] [3-Carol-IT] [4-David-???]
departments: [IT] [HR] [Finance]

INNER:  Alice, Bob, Carol     (matched only)
LEFT:   Alice, Bob, Carol, David  (all employees, NaN for David's dept)
RIGHT:  Alice, Bob, Carol, Finance-???  (all depts, NaN for Finance's employee)
OUTER:  all of both, NaN where no match
```

## pd.concat() — Stack DataFrames

```python
q1 = pd.DataFrame({'month':['Jan','Feb','Mar'], 'sales':[100,120,90]})
q2 = pd.DataFrame({'month':['Apr','May','Jun'], 'sales':[110,130,95]})

# Stack vertically (add rows) — axis=0
full = pd.concat([q1, q2], axis=0, ignore_index=True)
print(full)

# Stack horizontally (add columns) — axis=1
df_a = pd.DataFrame({'name': ['Alice','Bob']})
df_b = pd.DataFrame({'score': [88, 92]})
combined = pd.concat([df_a, df_b], axis=1)
print(combined)
```

## df.join() — Join on index

```python
df_left  = pd.DataFrame({'salary': [50000, 80000]}, index=['Alice','Bob'])
df_right = pd.DataFrame({'dept':   ['HR', 'IT']},   index=['Alice','Bob'])

joined = df_left.join(df_right)
print(joined)
#        salary dept
# Alice   50000   HR
# Bob     80000   IT
```

-----

-----

# 12. DateTime Handling

DateTime is crucial for financial data, logs, sales analysis — any time-series work.

## pd.to_datetime() — Parse dates

```python
df = pd.DataFrame({
    'date': ['2024-01-15', '2024-03-22', '2024-07-04', '2024-11-11'],
    'sales': [1000, 1500, 800, 2000]
})

# Convert string column to datetime dtype
df['date'] = pd.to_datetime(df['date'])
print(df.dtypes)
# date     datetime64[ns]
# sales             int64

# With different format
df2 = pd.DataFrame({'date': ['15/01/2024', '22/03/2024']})
df2['date'] = pd.to_datetime(df2['date'], format='%d/%m/%Y')
```

## .dt accessor — Extract components

```python
df['year']       = df['date'].dt.year
df['month']      = df['date'].dt.month
df['day']        = df['date'].dt.day
df['dayofweek']  = df['date'].dt.dayofweek   # 0=Monday, 6=Sunday
df['day_name']   = df['date'].dt.day_name()  # 'Monday', 'Tuesday'...
df['quarter']    = df['date'].dt.quarter
df['week']       = df['date'].dt.isocalendar().week

print(df[['date','year','month','dayofweek','day_name','quarter']])
```

## DateTime filtering and operations

```python
# Filter by date range
jan = df[df['date'].dt.month == 1]
q1  = df[df['date'].dt.quarter == 1]

# Filter using string comparison (Pandas parses it)
after_june = df[df['date'] > '2024-06-01']

# Time delta — days between dates
df['days_since'] = (pd.Timestamp('2025-01-01') - df['date']).dt.days
print(df[['date', 'days_since']])

# Set date as index for time-series operations
df = df.set_index('date')
print(df['2024-01':'2024-06'])   # select Jan–Jun using string slicing!

# Resample — aggregate by time frequency
df_monthly = df.resample('ME').sum()   # sum sales per month end
print(df_monthly)
```

-----

-----

# 13. Duplicate Handling

## duplicated() — Find duplicate rows

```python
df = pd.DataFrame({
    'name':   ['Alice', 'Bob', 'Alice', 'Carol', 'Bob', 'Alice'],
    'dept':   ['IT', 'HR', 'IT', 'Finance', 'HR', 'Finance'],
    'salary': [50000, 80000, 50000, 90000, 80000, 70000]
})

# Returns boolean Series — True where row is a duplicate
print(df.duplicated())
# 0    False   ← first occurrence → NOT duplicate
# 1    False
# 2     True   ← exact duplicate of row 0
# 3    False
# 4     True   ← exact duplicate of row 1
# 5    False   ← same name but different dept/salary → NOT duplicate

# Which rows are duplicates?
print(df[df.duplicated()])

# Count duplicates
print(df.duplicated().sum())   # 2

# Duplicates based on specific columns only
print(df.duplicated(subset=['name', 'dept']))

# keep='last' — mark the FIRST occurrence as duplicate instead
print(df.duplicated(keep='last'))

# keep=False — mark ALL occurrences of a duplicate as True
print(df.duplicated(keep=False))
```

## drop_duplicates() — Remove duplicates

```python
# Remove exact duplicate rows (keep first occurrence)
df_clean = df.drop_duplicates()
print(df_clean)

# Keep last occurrence
df_clean2 = df.drop_duplicates(keep='last')

# Drop duplicates based on specific columns
# Keep first entry per (name, dept) combination
df_clean3 = df.drop_duplicates(subset=['name', 'dept'], keep='first')
print(df_clean3)
```

-----

-----

# 14. Performance Basics

## The problem with default dtypes

When Pandas reads a CSV, it infers dtypes. This is convenient but often wasteful:

```
Pandas default inference:
  integers → int64    (8 bytes per value)
  floats   → float64  (8 bytes per value)
  strings  → object   (Python str object + pointer overhead ≈ 50+ bytes!)
  booleans → object   (if mixed with other types)
```

## dtype optimization with integers and floats

```python
import pandas as pd
import numpy as np

# Simulate a large dataset
np.random.seed(42)
df = pd.DataFrame({
    'id':     np.random.randint(1, 10000, 100000),       # max 10000 → fits in int16
    'score':  np.random.randint(0, 100, 100000),         # 0–100 → fits in int8
    'price':  np.random.uniform(0, 500, 100000),         # float32 is enough
    'region': np.random.choice(['N','S','E','W'], 100000)
})

print("Before optimization:")
print(df.dtypes)
print(f"Memory: {df.memory_usage(deep=True).sum() / 1024:.1f} KB")

# Downcast integers
df['id']    = df['id'].astype(np.int16)      # int64→int16: 8→2 bytes
df['score'] = df['score'].astype(np.int8)    # int64→int8:  8→1 byte
df['price'] = df['price'].astype(np.float32) # float64→float32: 8→4 bytes

# Convert string column to category
df['region'] = df['region'].astype('category')

print("\nAfter optimization:")
print(df.dtypes)
print(f"Memory: {df.memory_usage(deep=True).sum() / 1024:.1f} KB")
```

**Integer type ranges:**

```
Type      Bytes   Range
int8         1    -128 to 127
int16        2    -32768 to 32767
int32        4    -2 billion to +2 billion
int64        8    very large numbers
uint8        1    0 to 255   (unsigned — no negatives)
uint16       2    0 to 65535
```

## category dtype — The big win for string columns

When a string column has few unique values relative to its size (e.g., 4 regions in 1 million rows), storing it as `object` means 1 million Python string objects. As `category`, Pandas stores:

- A mapping table: `{'N':0, 'S':1, 'E':2, 'W':3}` (4 strings)
- An array of integers (0,1,2,3…) instead of strings

```
object:   ['North','South','North','East',...] × 1,000,000
           ↑ 1 million Python string objects in heap memory

category: codes=[0,1,0,2,...] (int8) + categories=['East','North','South','West']
          ↑ 1 million int8 values (1 byte each) + just 4 strings
```

```python
# When to use category:
# Rule of thumb: if unique values < 50% of total rows → use category
s = pd.Series(['North','South','East','West'] * 250000)   # 1M rows

print(f"object size:   {s.memory_usage(deep=True):,} bytes")
s_cat = s.astype('category')
print(f"category size: {s_cat.memory_usage(deep=True):,} bytes")

# Category also speeds up groupby operations
```

## query() — Readable and sometimes faster filtering

```python
df = pd.DataFrame({
    'age':    np.random.randint(20, 60, 10000),
    'salary': np.random.randint(30000, 150000, 10000),
    'dept':   np.random.choice(['IT','HR','Finance'], 10000)
})

# Standard boolean indexing
result1 = df[(df['age'] > 30) & (df['salary'] > 80000) & (df['dept'] == 'IT')]

# query() — string expression, cleaner syntax
result2 = df.query('age > 30 and salary > 80000 and dept == "IT"')

# Use Python variable inside query with @
min_salary = 80000
result3 = df.query('salary > @min_salary and dept == "IT"')

# Both give same result
print(result1.shape == result2.shape)   # True
```

> **When query() is faster:** For large DataFrames (millions of rows), `query()` can use `numexpr` under the hood — a library that compiles the expression to optimized bytecode and evaluates it in chunks, making better use of CPU cache. Install with `pip install numexpr`.

## pd.read_csv() with dtype and usecols for large files

```python
# Slowest: load everything, infer dtypes
df = pd.read_csv('big_file.csv')

# Fastest: only load what you need with known dtypes
df = pd.read_csv(
    'big_file.csv',
    usecols=['date', 'product', 'sales'],   # load 3 of 20 columns
    dtype={
        'product': 'category',              # skip object allocation
        'sales':   'float32',               # skip float64 inference
    },
    parse_dates=['date']                    # parse dates during read
)
```

-----

-----

# 🌍 Real-World Use Cases — Topics Combined

## Use Case 1: IPL 2024 Match Analysis

Combining: Reading data, Filtering, GroupBy, Aggregation, Sorting

```python
import pandas as pd
import numpy as np

np.random.seed(10)

# Simulate ball-by-ball IPL data
teams = ['MI', 'CSK', 'RCB', 'KKR', 'DC', 'SRH', 'PBKS', 'RR']
players = [f'Player_{i}' for i in range(1, 30)]

n = 5000
balls = pd.DataFrame({
    'match_id':   np.random.randint(1, 70, n),
    'batting_team': np.random.choice(teams, n),
    'batsman':    np.random.choice(players, n),
    'bowler':     np.random.choice(players, n),
    'runs_scored': np.random.choice([0,0,0,1,1,2,4,6], n, p=[0.3,0.15,0.1,0.15,0.1,0.1,0.07,0.03]),
    'is_wicket':  np.random.choice([0,1], n, p=[0.93, 0.07]),
    'over':       np.random.randint(0, 20, n),
    'ball':       np.random.randint(1, 7, n)
})

print("=== IPL DATA OVERVIEW ===")
print(balls.info())
print(balls.describe())

# Top run-scorers
print("\n=== TOP 10 BATSMEN ===")
top_batsmen = (balls.groupby('batsman')['runs_scored']
               .sum()
               .sort_values(ascending=False)
               .head(10))
print(top_batsmen)

# Team totals
print("\n=== RUNS PER TEAM ===")
team_runs = balls.groupby('batting_team').agg(
    total_runs=('runs_scored', 'sum'),
    total_balls=('runs_scored', 'count'),
    wickets_lost=('is_wicket', 'sum')
).round(2)
team_runs['run_rate'] = (team_runs['total_runs'] / team_runs['total_balls'] * 6).round(2)
print(team_runs.sort_values('total_runs', ascending=False))

# Powerplay vs Death over analysis
balls['phase'] = pd.cut(balls['over'],
                         bins=[-1, 5, 14, 19],
                         labels=['Powerplay (0-5)', 'Middle (6-14)', 'Death (15-19)'])

phase_stats = balls.groupby('phase')['runs_scored'].agg(['mean','sum']).round(2)
print("\n=== PHASE-WISE ANALYSIS ===")
print(phase_stats)

# Top wicket-takers
print("\n=== TOP WICKET-TAKERS ===")
wickets = (balls[balls['is_wicket'] == 1]
           .groupby('bowler')['is_wicket']
           .count()
           .sort_values(ascending=False)
           .head(5))
print(wickets)
```

-----

## Use Case 2: Employee HR Analytics

Combining: Missing data, String ops, DateTime, Boolean filtering, Groupby, Merge

```python
import pandas as pd
import numpy as np
from datetime import date

np.random.seed(7)
n = 200

depts = ['Engineering', 'HR', 'Finance', 'Marketing', 'Operations']
cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Hyderabad']
genders = ['Male', 'Female']

employees = pd.DataFrame({
    'emp_id':     range(1001, 1001 + n),
    'name':       [f'Employee_{i}' for i in range(n)],
    'dept':       np.random.choice(depts, n),
    'city':       np.random.choice(cities, n),
    'gender':     np.random.choice(genders, n),
    'salary':     np.random.randint(300000, 1500000, n),
    'join_date':  pd.to_datetime(
                      np.random.choice(pd.date_range('2015-01-01','2024-01-01'), n)
                  ),
    'rating':     np.random.choice([1,2,3,4,5], n, p=[0.05,0.1,0.4,0.35,0.1])
})

# Introduce some missing values
employees.loc[np.random.choice(n, 15, replace=False), 'salary'] = np.nan
employees.loc[np.random.choice(n, 10, replace=False), 'rating'] = np.nan

print("=== DATA QUALITY CHECK ===")
print(employees.isnull().sum())
print(f"\nDuplicate rows: {employees.duplicated().sum()}")

# Fill missing salary with dept median
employees['salary'] = employees.groupby('dept')['salary'].transform(
    lambda x: x.fillna(x.median())
)

# Fill missing rating with overall median
employees['rating'] = employees['rating'].fillna(employees['rating'].median())

print("\n=== AFTER CLEANING ===")
print(employees.isnull().sum())

# Tenure calculation
employees['tenure_years'] = ((pd.Timestamp('2025-01-01') - employees['join_date'])
                              .dt.days / 365).round(1)

# Experience band
employees['exp_band'] = pd.cut(
    employees['tenure_years'],
    bins=[0, 2, 5, 10, 100],
    labels=['Junior (<2yr)', 'Mid (2-5yr)', 'Senior (5-10yr)', 'Lead (10+yr)']
)

# Salary analysis by dept and gender
print("\n=== SALARY BY DEPT ===")
salary_analysis = employees.groupby('dept').agg(
    headcount=('emp_id',  'count'),
    avg_salary=('salary', 'mean'),
    median_salary=('salary', 'median'),
    min_salary=('salary', 'min'),
    max_salary=('salary', 'max')
).round(0)
print(salary_analysis)

# Gender pay analysis
print("\n=== GENDER PAY COMPARISON ===")
gender_pay = employees.groupby(['dept', 'gender'])['salary'].mean().round(0).unstack()
print(gender_pay)

# High performers in Engineering
print("\n=== TOP ENGINEERS ===")
top_eng = employees[
    (employees['dept'] == 'Engineering') & (employees['rating'] >= 4)
].sort_values('salary', ascending=False).head(5)[['name','salary','tenure_years','rating']]
print(top_eng)
```

-----

## Use Case 3: E-Commerce Sales Dashboard

Combining: DateTime, Pivot table, Merging, GroupBy, String ops, Query

```python
import pandas as pd
import numpy as np

np.random.seed(2024)

# Orders table
n_orders = 1000
categories = ['Electronics', 'Clothing', 'Books', 'Food', 'Sports']
states = ['Maharashtra', 'Karnataka', 'Delhi', 'Tamil Nadu', 'Gujarat']

orders = pd.DataFrame({
    'order_id':   range(10001, 10001 + n_orders),
    'customer_id': np.random.randint(1, 201, n_orders),
    'product':    [f'Product_{np.random.randint(1,50)}' for _ in range(n_orders)],
    'category':   np.random.choice(categories, n_orders),
    'state':      np.random.choice(states, n_orders),
    'quantity':   np.random.randint(1, 10, n_orders),
    'unit_price': np.random.uniform(50, 5000, n_orders).round(2),
    'order_date': pd.to_datetime(
                      np.random.choice(pd.date_range('2024-01-01','2024-12-31'), n_orders)
                  ),
    'status':     np.random.choice(['Delivered','Pending','Cancelled'],
                                   n_orders, p=[0.7, 0.2, 0.1])
})

# Feature engineering
orders['revenue'] = (orders['quantity'] * orders['unit_price']).round(2)
orders['month']   = orders['order_date'].dt.month
orders['quarter'] = orders['order_date'].dt.quarter
orders['weekday'] = orders['order_date'].dt.day_name()

# Only delivered orders for revenue analysis
delivered = orders.query('status == "Delivered"')

print("=== MONTHLY REVENUE TREND ===")
monthly = delivered.groupby('month')['revenue'].sum().round(0)
print(monthly)

print("\n=== CATEGORY PERFORMANCE ===")
cat_perf = delivered.groupby('category').agg(
    total_revenue=('revenue', 'sum'),
    total_orders=('order_id', 'count'),
    avg_order_value=('revenue', 'mean'),
    total_units=('quantity', 'sum')
).round(2).sort_values('total_revenue', ascending=False)
print(cat_perf)

print("\n=== QUARTERLY × CATEGORY PIVOT ===")
qtr_cat = pd.pivot_table(
    delivered,
    values='revenue',
    index='quarter',
    columns='category',
    aggfunc='sum',
    fill_value=0,
    margins=True
).round(0)
print(qtr_cat)

print("\n=== TOP 5 STATES BY REVENUE ===")
print(delivered.groupby('state')['revenue'].sum().nlargest(5).round(0))

print("\n=== CANCELLATION RATE BY CATEGORY ===")
total_by_cat = orders.groupby('category')['order_id'].count()
cancelled_by_cat = orders[orders['status']=='Cancelled'].groupby('category')['order_id'].count()
cancel_rate = (cancelled_by_cat / total_by_cat * 100).round(1)
print(cancel_rate)

print("\n=== HIGH VALUE ORDERS (>₹10,000) ===")
high_value = orders.query('revenue > 10000 and status == "Delivered"')
print(f"Count: {len(high_value)}")
print(f"Revenue contribution: ₹{high_value['revenue'].sum():,.0f}")
```

-----

## Use Case 4: Financial Portfolio Analysis

Combining: DateTime, Merge, GroupBy, apply(), Performance optimizations

```python
import pandas as pd
import numpy as np

np.random.seed(42)

# Stock prices for 5 stocks over 252 trading days
stocks = ['RELIANCE', 'TCS', 'INFY', 'HDFC', 'WIPRO']
dates  = pd.bdate_range('2024-01-01', periods=252)   # business days only

# Build price DataFrame
start_prices = {'RELIANCE': 2800, 'TCS': 3500, 'INFY': 1500, 'HDFC': 1600, 'WIPRO': 500}
prices_dict = {}
for stock, start in start_prices.items():
    daily_ret = np.random.normal(0.0004, 0.015, 252)
    prices_dict[stock] = (start * np.cumprod(1 + daily_ret)).round(2)

prices = pd.DataFrame(prices_dict, index=dates)
prices.index.name = 'date'

print("=== PRICE DATA SAMPLE ===")
print(prices.head())
print(f"\nShape: {prices.shape}")

# Daily returns
returns = prices.pct_change().dropna()

print("\n=== ANNUAL RETURN PER STOCK ===")
annual_return = ((prices.iloc[-1] / prices.iloc[0]) - 1) * 100
print(annual_return.round(2))

print("\n=== RISK (ANNUALIZED VOLATILITY) ===")
volatility = returns.std() * np.sqrt(252) * 100
print(volatility.round(2))

print("\n=== CORRELATION MATRIX ===")
print(returns.corr().round(3))

# Monthly performance
prices_monthly = prices.resample('ME').last()   # last price of each month
monthly_returns = prices_monthly.pct_change() * 100

print("\n=== MONTHLY RETURN HEATMAP DATA ===")
monthly_returns.index = monthly_returns.index.strftime('%b-%Y')
print(monthly_returns.round(2))

# Sharpe Ratio (simplified, risk-free rate = 6%)
risk_free_daily = 0.06 / 252
excess_returns = returns - risk_free_daily
sharpe = (excess_returns.mean() / returns.std() * np.sqrt(252)).round(3)
print("\n=== SHARPE RATIO ===")
print(sharpe.sort_values(ascending=False))

# Worst drawdown per stock
rolling_max = prices.cummax()
drawdown = (prices - rolling_max) / rolling_max * 100
max_drawdown = drawdown.min().round(2)
print("\n=== MAX DRAWDOWN ===")
print(max_drawdown)
```

-----

-----

# 📝 Quick Reference: Common Patterns

```python
# Conditional column assignment (vectorized)
df['grade'] = np.where(df['score'] >= 90, 'A',
              np.where(df['score'] >= 75, 'B',
              np.where(df['score'] >= 60, 'C', 'F')))

# Binning continuous data into categories
df['age_group'] = pd.cut(df['age'],
                          bins=[0, 25, 35, 50, 100],
                          labels=['Young', 'Adult', 'Senior', 'Elder'])

# Cumulative sum (running total)
df['cumulative_sales'] = df['sales'].cumsum()

# Percentage of group total
df['pct_of_dept'] = df.groupby('dept')['salary'].transform(
    lambda x: x / x.sum() * 100
)

# Rank within group
df['rank_in_dept'] = df.groupby('dept')['salary'].rank(ascending=False)

# Rolling window average (7-day moving average)
df['7d_avg'] = df['sales'].rolling(window=7).mean()

# Lag feature — previous row value
df['prev_day_sales'] = df['sales'].shift(1)

# Check if any value in a column matches pattern
df['is_gmail'] = df['email'].str.endswith('@gmail.com')

# Flatten MultiIndex columns after groupby
result = df.groupby('dept').agg({'salary': ['mean','max']})
result.columns = ['_'.join(col) for col in result.columns]

# Chain operations (readable pipeline)
result = (df
    .dropna(subset=['salary'])
    .query('dept != "Finance"')
    .assign(salary_k=lambda x: x['salary'] / 1000)
    .groupby('dept')['salary_k']
    .mean()
    .sort_values(ascending=False)
    .round(1)
)
```

-----

# 📊 Pandas vs Python Loop — Side by Side

```python
import pandas as pd
import numpy as np
import time

df = pd.DataFrame({'salary': np.random.randint(30000, 150000, 1_000_000)})

# Python loop approach
start = time.time()
result_loop = []
for sal in df['salary']:
    if sal > 80000:
        result_loop.append(sal * 1.1)
    else:
        result_loop.append(sal)
print(f"Python loop: {time.time()-start:.3f} seconds")

# Pandas vectorized approach
start = time.time()
result_vec = np.where(df['salary'] > 80000, df['salary'] * 1.1, df['salary'])
print(f"Pandas vectorized: {time.time()-start:.3f} seconds")

# Typical result:
# Python loop:        ~0.4 seconds
# Pandas vectorized:  ~0.005 seconds  ← ~80x faster
```

-----

# 🧠 Summary: Key Mental Models

|Concept      |Mental Model                                                                       |
|-------------|-----------------------------------------------------------------------------------|
|Series       |NumPy array + Index (labels). Operations → delegate to NumPy C code                |
|DataFrame    |Dict of aligned Series (columnar). Each column = separate memory block             |
|Vectorization|Operations run in C, no Python loop, CPU processes many elements per clock         |
|loc          |Row/column by **label**. Slice stop is **inclusive**                               |
|iloc         |Row/column by **integer position**. Slice stop is **exclusive**                    |
|Boolean mask |A NumPy bool array; applying it filters rows in C, returns copy                    |
|groupby      |Split → Apply → Combine. Split stores pointers to row groups, doesn’t copy data    |
|merge        |SQL join on column values. ‘inner’ = intersection, ‘left’ = all left rows          |
|category     |Maps repeated strings to integers; huge memory win for low-cardinality columns     |
|apply(axis=1)|Python loop per row — last resort. Prefer vectorized ops                           |
|NaN          |float64 bit pattern for “missing”. Propagates through operations by design         |
|query()      |Compiles filter to bytecode via numexpr; readable and cache-friendly for large data|

-----

*Made for learning Pandas from the ground up — type every example manually.*