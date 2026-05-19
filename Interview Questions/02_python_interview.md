# Python Interview Prep — Set 2 (20 Fresh Questions)
### AI/ML Intern | Round 2 | No repeats from Set 1

> **Mindset for the interview:**
> - If a word doesn't click → say *"Let me think through this with an example"* and start writing/talking
> - If you forget syntax → explain the logic in plain English first, code second
> - Interviewers at intern level test **thinking**, not memorization
> - Silence is worse than a wrong attempt — always attempt

---

## MODULE 1 — Python Fundamentals

---

### Q1. What is the difference between `is` and `==` in Python?

**What they're testing:** Object identity vs value equality — a classic trap question.

```python
# == checks VALUE equality
# is checks if both point to the SAME object in memory

a = [1, 2, 3]
b = [1, 2, 3]

print(a == b)   # True  — same values
print(a is b)   # False — different objects in memory


# The trap — small integers are cached by Python (-5 to 256)
x = 256
y = 256
print(x is y)   # True  — Python reuses same object for small ints

x = 257
y = 257
print(x is y)   # False — outside cache range, new objects created
```

```
Rule of thumb:
  Use ==  → to compare VALUES (almost always what you want)
  Use is  → only to check if something is None: if x is None
```

**If blank in interview:** *"== compares what's inside the box, is checks if it's literally the same box in memory."*

---

### Q2. What are Python's mutable vs immutable data types? Why does it matter?

**What they're testing:** Memory model understanding — foundational for debugging bugs.

```python
# IMMUTABLE — cannot be changed after creation
# int, float, str, tuple, bool, frozenset

name = "Alice"
name[0] = "B"     # TypeError! strings are immutable

# What actually happens when you "change" a string:
name = "Alice"
id_before = id(name)
name = "Bob"          # creates a NEW object, rebinds the variable
id_after = id(name)
print(id_before == id_after)   # False — different objects


# MUTABLE — can be changed in place
# list, dict, set

my_list = [1, 2, 3]
id_before = id(my_list)
my_list.append(4)         # modifies the SAME object
id_after = id(my_list)
print(id_before == id_after)   # True — same object, just changed


# Why it matters — the mutable default argument trap (very common bug):
def add_item(item, cart=[]):      # ← DANGEROUS: default list is created ONCE
    cart.append(item)
    return cart

print(add_item("apple"))          # ['apple']
print(add_item("banana"))         # ['apple', 'banana'] ← BUG! persists across calls

# Fix:
def add_item_fixed(item, cart=None):
    if cart is None:
        cart = []                 # fresh list every call
    cart.append(item)
    return cart
```

---

### Q3. How does String Slicing work? Write the output for these.

**What they're testing:** String operations — pen and paper style.

```python
s = "PythonInterviewPrep"
#    0123456789...

# Basic slice: s[start:stop:step]  — stop is EXCLUDED

print(s[0:6])       # "Python"       — index 0 to 5
print(s[6:])        # "InterviewPrep"— from index 6 to end
print(s[:6])        # "Python"       — from start to index 5
print(s[-4:])       # "Prep"         — last 4 characters
print(s[::2])       # every 2nd char — "PtоItrePe"
print(s[::-1])      # "perPweivretInohtyP" — reversed string!


# Common interview questions:
word = "interview"

# Reverse a string
print(word[::-1])              # "weivretnI"

# Check if palindrome
def is_palindrome(s):
    return s == s[::-1]

print(is_palindrome("racecar"))  # True
print(is_palindrome("python"))   # False
```

---

### Q4. What is the difference between `deepcopy` and `copy`? When does it matter?

**What they're testing:** Memory + nested data awareness — real ML data bug scenario.

```python
import copy

original = [[1, 2, 3], [4, 5, 6]]

# Shallow copy — copies the outer list, but INNER lists are still shared
shallow = copy.copy(original)
shallow[0][0] = 999

print(original)   # [[999, 2, 3], [4, 5, 6]] ← CHANGED! inner list shared


original = [[1, 2, 3], [4, 5, 6]]

# Deep copy — copies everything, completely independent
deep = copy.deepcopy(original)
deep[0][0] = 999

print(original)   # [[1, 2, 3], [4, 5, 6]] ← unchanged! fully independent
print(deep)       # [[999, 2, 3], [4, 5, 6]]


# Visual:
# original ──► [list_A, list_B]
#                  │        │
# shallow  ──► [list_A, list_B]   ← same inner lists!
#
# deep     ──► [copy_A, copy_B]   ← completely new inner lists
```

**ML context:** When duplicating a dataset config dict — always deepcopy, else nested params bleed between experiments.

---

### Q5. What is `logging` in Python and why use it over `print`?

**What they're testing:** Professional code awareness — shows engineering maturity.

```python
import logging

# print() → for quick debugging only, no context, no control

# logging → structured, has levels, can write to file, timestamps, module name
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger(__name__)   # best practice: use module name

logger.debug("Model loading started")      # level 10 — very detailed
logger.info("Dataset loaded: 5000 rows")   # level 20 — normal flow
logger.warning("Missing values found: 5%") # level 30 — something to note
logger.error("File not found: data.csv")   # level 40 — something broke
logger.critical("GPU out of memory!")      # level 50 — system-level failure


# Levels filter — set to WARNING means debug/info are silently ignored
logging.basicConfig(level=logging.WARNING)
logger.debug("This won't show")     # suppressed
logger.warning("This will show")    # shown
```

**Why over print in 1 line:** *"print has no level, no timestamp, no filtering — you can't turn it off in production without deleting it."*

---

## MODULE 2 — Object-Oriented Programming

---

### Q6. What is the `__init__` vs `__new__` method? When would you override `__new__`?

**What they're testing:** Object creation lifecycle — deeper OOP.**

```python
class MyClass:
    def __new__(cls, *args, **kwargs):
        # called FIRST — creates and returns the object
        print("1. __new__ called — object being created")
        instance = super().__new__(cls)
        return instance

    def __init__(self, name):
        # called SECOND — initializes the object that __new__ created
        print("2. __init__ called — object being initialized")
        self.name = name


obj = MyClass("Alice")
# Output:
# 1. __new__ called — object being created
# 2. __init__ called — object being initialized


# When to override __new__ — Singleton pattern (ensure only 1 instance)
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)   # create only once
        return cls._instance                        # always return same object

s1 = Singleton()
s2 = Singleton()
print(s1 is s2)   # True — same object
```

---

### Q7. What are Getters and Setters? Show the old way vs the Pythonic `@property` way.

**What they're testing:** Encapsulation evolution — shows you know Python idioms.**

```python
# ---- OLD WAY (Java-style) ---- not Pythonic
class Person:
    def __init__(self, age):
        self._age = age

    def get_age(self):          # getter method
        return self._age

    def set_age(self, value):   # setter method
        if value < 0:
            raise ValueError("Age can't be negative")
        self._age = value

p = Person(25)
p.set_age(30)          # ugly — method call syntax
print(p.get_age())     # ugly — method call syntax


# ---- PYTHONIC WAY (@property) ---- clean attribute-style
class Person:
    def __init__(self, age):
        self._age = age

    @property
    def age(self):              # getter — access like p.age
        return self._age

    @age.setter
    def age(self, value):       # setter — assign like p.age = 30
        if value < 0:
            raise ValueError("Age can't be negative")
        self._age = value

    @age.deleter
    def age(self):              # deleter — del p.age
        print("Deleting age")
        del self._age


p = Person(25)
print(p.age)      # 25   — looks like attribute, runs getter
p.age = 30        # runs setter with validation
p.age = -1        # ValueError!
del p.age         # runs deleter
```

---

### Q8. Explain Inheritance with `super()`. What happens without `super()` in `__init__`?

**What they're testing:** Inheritance correctness — a real interview trap.**

```python
class Animal:
    def __init__(self, name, sound):
        self.name = name      # parent attributes
        self.sound = sound

    def speak(self):
        return f"{self.name} says {self.sound}"


# WITHOUT super() — parent __init__ never runs, attributes missing
class Dog(Animal):
    def __init__(self, name, breed):
        # forgot super().__init__()!
        self.breed = breed

d = Dog("Rex", "Labrador")
print(d.breed)    # "Labrador" — works
print(d.name)     # AttributeError! — name never set, Animal.__init__ never ran


# WITH super() — correct way
class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name, "Woof")   # parent runs first, sets name + sound
        self.breed = breed               # then child adds its own

d = Dog("Rex", "Labrador")
print(d.name)     # "Rex"       — from Animal.__init__
print(d.breed)    # "Labrador"  — from Dog.__init__
print(d.speak())  # "Rex says Woof"


# Method override with super()
class GuideDog(Dog):
    def speak(self):
        base = super().speak()                   # get parent's output
        return f"{base} [Guide Dog — trained]"  # extend it

g = GuideDog("Buddy", "Golden")
print(g.speak())  # "Buddy says Woof [Guide Dog — trained]"
```

---

### Q9. What is the difference between `_single_underscore`, `__double_underscore`, and `__dunder__`?

**What they're testing:** Python naming conventions — shows professionalism.**

```python
class BankAccount:

    def __init__(self, owner, balance):
        self.owner = owner          # public — anyone can access
        self._balance = balance     # protected — "please don't touch" (convention only)
        self.__pin = 1234           # private — name mangling applied by Python

    def __str__(self):              # dunder — Python calls this automatically
        return f"{self.owner}'s account"


acc = BankAccount("Alice", 50000)

# Public — fully accessible
print(acc.owner)       # "Alice"

# Protected — accessible but bad practice
print(acc._balance)    # 50000 — works, but you're breaking the convention

# Private — name-mangled by Python, can't access directly
# print(acc.__pin)     # AttributeError!
print(acc._BankAccount__pin)   # 1234 — works via mangled name (don't do this in practice)


# Summary:
# owner        → public    — use freely
# _balance     → protected → internal use, subclass OK, outside callers shouldn't
# __pin        → private   → only this class; Python mangles to _ClassName__attr
# __str__      → dunder    → Python's special methods, don't invent your own
```

---

## MODULE 3 — Design Patterns (Pseudo-code + Use Case)

---

### Q10. What is the Builder Pattern? When would you use it over a constructor?

**Problem it solves:** When an object has too many optional parameters — constructor becomes unreadable.

**ML use case:** Building a model training config with optional params (learning rate, dropout, scheduler, etc.)

```python
# WITHOUT Builder — constructor hell
model = NeuralNetwork("relu", 0.001, 0.2, True, 128, 3, "adam", True, 0.9)
# What does each arg mean?? Impossible to read.


# WITH Builder — readable, step-by-step construction

class ModelConfigBuilder:
    def __init__(self):
        # set all defaults
        self.activation = "relu"
        self.learning_rate = 0.001
        self.dropout = 0.0
        self.batch_size = 32
        self.optimizer = "adam"

    def with_learning_rate(self, lr):
        self.learning_rate = lr
        return self            # returns self so you can chain calls

    def with_dropout(self, rate):
        self.dropout = rate
        return self

    def with_batch_size(self, size):
        self.batch_size = size
        return self

    def build(self):
        return ModelConfig(self)   # create final object from builder state


# Clean, readable, self-documenting
config = (ModelConfigBuilder()
          .with_learning_rate(0.0001)
          .with_dropout(0.3)
          .with_batch_size(64)
          .build())
```

**Key signal to use Builder:** More than 4-5 params, many optional, order shouldn't matter.

---

### Q11. What is the Prototype Pattern? How is it different from just using `copy()`?

**Problem it solves:** Creating a new object by cloning an existing one — when creation is expensive.

**ML use case:** Clone a pre-trained model config to create multiple experiment variants.

```python
# Pseudo-code

import copy

class ExperimentConfig:
    def __init__(self, model, lr, epochs, augmentation):
        self.model = model
        self.lr = lr
        self.epochs = epochs
        self.augmentation = augmentation

    def clone(self):
        return copy.deepcopy(self)    # full clone — independent copy


# Expensive to create from scratch each time
base_config = ExperimentConfig("ResNet50", 0.001, 100, True)

# Clone and tweak — don't rebuild from scratch
experiment_1 = base_config.clone()
experiment_1.lr = 0.0001              # only change what differs

experiment_2 = base_config.clone()
experiment_2.epochs = 200

# base_config is untouched — it's the "prototype"
```

**Difference from plain copy():**
```
copy()      → just a method call — no standard interface
Prototype   → design pattern — defines a clone() contract on the class itself,
              makes it explicit that THIS class is meant to be cloned
```

---

### Q12. What is the State Pattern? Give a real example.

**Problem it solves:** An object's behavior changes based on its internal state — without messy if-else chains.

**Real use case:** ML model lifecycle — Draft → Training → Trained → Deployed → Deprecated

```python
# Pseudo-code

class ModelState:
    def train(self, model): raise NotImplementedError
    def deploy(self, model): raise NotImplementedError
    def predict(self, model): raise NotImplementedError


class DraftState(ModelState):
    def train(self, model):
        print("Starting training...")
        model.state = TrainingState()   # transition to next state

    def deploy(self, model):
        print("Can't deploy — model not trained yet!")

    def predict(self, model):
        print("Can't predict — model not trained yet!")


class TrainingState(ModelState):
    def train(self, model):
        print("Already training!")

    def deploy(self, model):
        print("Training complete. Deploying...")
        model.state = DeployedState()

    def predict(self, model):
        print("Can't predict while training!")


class DeployedState(ModelState):
    def train(self, model):
        print("Already deployed. Retrain? Create new version.")

    def deploy(self, model):
        print("Already deployed!")

    def predict(self, model):
        print("Prediction: [0.92, 0.05, 0.03]")   # actual prediction


class MLModel:
    def __init__(self):
        self.state = DraftState()    # starts in Draft

    def train(self): self.state.train(self)
    def deploy(self): self.state.deploy(self)
    def predict(self): self.state.predict(self)


model = MLModel()
model.predict()   # Can't predict — model not trained yet!
model.train()     # Starting training...
model.deploy()    # Training complete. Deploying...
model.predict()   # Prediction: [0.92, 0.05, 0.03]
```

**Why not if-else:** Adding a new state = add a new class. With if-else, you modify the existing method — risky.

---

### Q13. What is the Flyweight Pattern? When does it save memory?

**Problem it solves:** You have thousands of similar objects that share common data — store shared data once.

**ML use case:** Vocabulary tokens in NLP — millions of words but only ~50,000 unique tokens.

```python
# Pseudo-code

class Token:
    # Shared (intrinsic) state — same for all tokens with same word
    _token_cache = {}

    def __new__(cls, word):
        if word not in cls._token_cache:
            instance = super().__new__(cls)
            instance.word = word              # stored once
            instance.embedding = load_embedding(word)  # expensive — done once
            cls._token_cache[word] = instance
        return cls._token_cache[word]         # reuse existing


# Process 1 million tokens
tokens = [Token(word) for word in massive_text]

# "the" appears 50,000 times in text
# But Token("the") is created ONCE — all 50,000 point to same object
print(Token("the") is Token("the"))   # True — same object


# Memory:
# Without Flyweight: 1,000,000 objects × 300bytes = 300MB
# With Flyweight:    50,000 unique objects × 300bytes = 15MB
```

---

### Q14. What is the Proxy Pattern? Name 3 real use cases.

**Problem it solves:** Control access to an object — add logic before/after the real object is used.

```python
# Pseudo-code

class RealModelAPI:
    def predict(self, data):
        return expensive_model_call(data)     # actual heavy prediction


class ModelProxy:
    def __init__(self):
        self._real_api = None                  # lazy — don't create until needed
        self._cache = {}

    def predict(self, data):
        key = str(data)

        # Use Case 1: CACHING — return cached result if seen before
        if key in self._cache:
            return self._cache[key]

        # Use Case 2: LAZY INITIALIZATION — create real object only when first needed
        if self._real_api is None:
            self._real_api = RealModelAPI()   # heavy init delayed until first use

        # Use Case 3: LOGGING / MONITORING
        print(f"Calling model with: {data}")
        result = self._real_api.predict(data)
        print(f"Model returned: {result}")

        self._cache[key] = result
        return result


proxy = ModelProxy()
proxy.predict([1, 2, 3])    # real call — logs, initializes, caches
proxy.predict([1, 2, 3])    # cache hit — no real call, instant
```

**3 real use cases in 1 line each:**
```
1. Caching Proxy      → save repeated expensive computations
2. Protection Proxy   → check auth before allowing access
3. Virtual Proxy      → delay heavy object creation until actually needed
```

---

## MODULE 4 — NumPy & Pandas (Pen & Paper Style)

> **Write these as if on paper — method names matter more than perfect syntax**

---

### Q15. NumPy `iloc` equivalent — Array indexing on paper. What is the output?

**What they're testing:** Core indexing — you WILL get this on paper.

```python
import numpy as np

# Write the output for each line — practice this on paper

arr = np.array([[ 10,  20,  30,  40],
                [ 50,  60,  70,  80],
                [ 90, 100, 110, 120],
                [130, 140, 150, 160]])

# Shape: (4, 4) — 4 rows, 4 columns
# Index: rows 0-3, columns 0-3

print(arr[0])           # [ 10  20  30  40]       — first row
print(arr[2, 3])        # 120                      — row 2, col 3
print(arr[1:3, 1:3])   # [[ 60  70]               — rows 1-2, cols 1-2
                        #  [100 110]]
print(arr[:, 0])        # [ 10  50  90 130]        — all rows, col 0
print(arr[-1])          # [130 140 150 160]         — last row
print(arr[-1, -1])      # 160                       — last row, last col
print(arr[::2, ::2])   # [[ 10  30]                — every 2nd row & col
                        #  [ 90 110]]
```

**Memory trick for slicing:** `[row_start:row_end, col_start:col_end]` — end is EXCLUDED.

---

### Q16. Pandas `iloc` vs `loc` — Write the output. (Most asked pen-and-paper question)

**What they're testing:** This is THE most asked Pandas question in data interviews.**

```python
import pandas as pd

df = pd.DataFrame({
    "name":   ["Alice", "Bob", "Carol", "Dave", "Eve"],
    "age":    [25, 30, 22, 35, 28],
    "score":  [88, 92, 75, 95, 80],
    "dept":   ["ML", "Data", "ML", "Data", "ML"]
}, index=["a", "b", "c", "d", "e"])   # custom index labels!

# DataFrame looks like:
#     name  age  score  dept
# a  Alice   25     88    ML
# b    Bob   30     92  Data
# c  Carol   22     75    ML
# d   Dave   35     95  Data
# e    Eve   28     80    ML


# ---- iloc — by POSITION (integers only, like array indexing) ----
print(df.iloc[0])            # first row (Alice) — by position 0
print(df.iloc[0, 1])         # 25  — row position 0, col position 1 (age)
print(df.iloc[1:3])          # rows at position 1,2 (Bob, Carol)
print(df.iloc[0:3, 0:2])     # rows 0-2, cols 0-1 (name, age for Alice/Bob/Carol)
print(df.iloc[-1])           # last row (Eve)
print(df.iloc[[0, 2, 4]])    # rows at position 0,2,4 (Alice, Carol, Eve)


# ---- loc — by LABEL (index name or column name) ----
print(df.loc["a"])           # row with index label "a" (Alice)
print(df.loc["a", "score"])  # 88 — row "a", column "score"
print(df.loc["b":"d"])       # rows b to d INCLUSIVE (Bob, Carol, Dave)
                             # NOTE: loc END is INCLUSIVE unlike iloc!
print(df.loc["a":"c", "name":"age"])   # rows a-c, cols name to age
print(df.loc[df["dept"] == "ML"])      # filter rows where dept is ML


# ---- KEY DIFFERENCE ----
# iloc[1:3] → rows at positions 1 and 2 (excludes position 3)
# loc["b":"d"] → rows labeled b, c, d (INCLUDES "d")
```

**Exam trick to remember:**
```
iloc → i = integer → position-based → like list index → end EXCLUDED
loc  → l = label   → name-based     → like dict key   → end INCLUDED
```

---

### Q17. Pandas — Write code to clean this messy DataFrame. (Common pen-and-paper task)

```python
import pandas as pd
import numpy as np

# Messy data
df = pd.DataFrame({
    "Name":   ["Alice", "bob", "  Carol  ", "DAVE", None],
    "Age":    [25, -5, 30, 200, 28],        # -5 and 200 are invalid
    "Salary": [50000, None, 70000, None, 60000],
    "Email":  ["alice@x.com", "invalid", "carol@x.com", "dave@x.com", "eve@x.com"]
})


# Step 1: Fix name formatting — strip spaces, title case
df["Name"] = df["Name"].str.strip().str.title()
# "bob" → "Bob", "  Carol  " → "Carol", "DAVE" → "Dave"

# Step 2: Drop rows where Name is null
df.dropna(subset=["Name"], inplace=True)

# Step 3: Fix invalid ages (valid: 18-100)
df["Age"] = df["Age"].apply(lambda x: np.nan if x < 18 or x > 100 else x)

# Step 4: Fill missing salary with median
df["Salary"].fillna(df["Salary"].median(), inplace=True)

# Step 5: Flag invalid emails (must contain @)
df["Email_valid"] = df["Email"].str.contains("@", na=False)

# Step 6: Reset index after dropping rows
df.reset_index(drop=True, inplace=True)

print(df)
```

**If they ask "what would you check first on a new dataset?"**
```python
df.shape           # how big is it
df.dtypes          # what type is each column
df.isnull().sum()  # where are the missing values
df.describe()      # stats — spot outliers via min/max
df.duplicated().sum()  # any duplicate rows
```

---

### Q18. NumPy — Matrix operations written on paper. (ML math foundations)

**What they're testing:** Matrix math → core of ML (weights, gradients, dot products)**

```python
import numpy as np

# These are what you'll see in neural network math:

A = np.array([[1, 2],
              [3, 4]])

B = np.array([[5, 6],
              [7, 8]])


# --- Matrix Multiplication (NOT element-wise) ---
C = np.dot(A, B)         # or A @ B  (@ operator)
# [1*5+2*7, 1*6+2*8]   = [19, 22]
# [3*5+4*7, 3*6+4*8]   = [43, 50]
print(C)   # [[19, 22], [43, 50]]


# --- Element-wise vs Matrix multiply ---
print(A * B)      # element-wise: [[5,12],[21,32]]
print(A @ B)      # matrix:       [[19,22],[43,50]]


# --- Transpose ---
print(A.T)        # [[1,3],[2,4]] — rows become columns


# --- Determinant and Inverse (useful to know) ---
print(np.linalg.det(A))   # -2.0
print(np.linalg.inv(A))   # [[-2, 1],[1.5, -0.5]]


# --- Useful in ML: normalize a feature matrix ---
X = np.array([[1, 200],
              [2, 300],
              [3, 100]])

# Normalize each column (feature scaling):
X_mean = X.mean(axis=0)    # mean of each column
X_std  = X.std(axis=0)     # std of each column
X_norm = (X - X_mean) / X_std   # broadcasting handles this
print(X_norm)
```

---

### Q19. Pandas — `apply()` vs `map()` vs `applymap()`. Write code using each.

**What they're testing:** Pandas transformation methods — frequently tested.**

```python
import pandas as pd

df = pd.DataFrame({
    "name":   ["alice", "bob", "carol"],
    "salary": [50000, 60000, 75000],
    "score":  [8.5, 7.2, 9.1]
})


# ---- map() — on a SINGLE SERIES, element-by-element ----
df["name"] = df["name"].map(str.title)        # "alice" → "Alice"

dept_map = {"Alice": "ML", "Bob": "Data", "Carol": "ML"}
df["dept"] = df["name"].map(dept_map)         # lookup from dict


# ---- apply() — flexible: works on Series OR entire DataFrame ----

# On a Series:
df["salary_category"] = df["salary"].apply(
    lambda x: "High" if x > 60000 else "Mid"
)

# On entire DataFrame (axis=1 = row-wise):
def score_label(row):
    if row["score"] >= 9:
        return "Excellent"
    elif row["score"] >= 7:
        return "Good"
    else:
        return "Average"

df["grade"] = df.apply(score_label, axis=1)  # runs for each row


# ---- applymap() (renamed to map() in Pandas 2.1) — on every cell in DataFrame ----
numeric_df = df[["salary", "score"]]
rounded = numeric_df.applymap(lambda x: round(x, 1))


# Quick summary:
# map()      → one column, element-wise (Series only)
# apply()    → one column (Series) OR row/column-wise (DataFrame, flexible)
# applymap() → every single cell in a DataFrame
```

---

### Q20. Pandas — pivot table and groupby. Write the difference with code.

**What they're testing:** Data aggregation — real-world data analysis pattern.**

```python
import pandas as pd

df = pd.DataFrame({
    "employee": ["Alice","Bob","Carol","Dave","Eve","Frank"],
    "dept":     ["ML","ML","Data","Data","ML","Data"],
    "quarter":  ["Q1","Q2","Q1","Q2","Q1","Q2"],
    "sales":    [100, 150, 200, 120, 90, 180]
})


# ---- groupby — aggregate by one or more columns ----

# Total sales per department
print(df.groupby("dept")["sales"].sum())
# Data    500
# ML      340

# Multiple aggregations at once
print(df.groupby("dept")["sales"].agg(["mean", "sum", "count"]))
#       mean  sum  count
# Data   167  500      3
# ML     113  340      3

# Group by TWO columns
print(df.groupby(["dept", "quarter"])["sales"].sum())


# ---- pivot_table — like Excel pivot — reshape + aggregate ----

pivot = pd.pivot_table(
    df,
    values="sales",       # what to aggregate
    index="dept",         # rows
    columns="quarter",    # columns
    aggfunc="sum",        # how to aggregate
    fill_value=0          # fill missing combos with 0
)

print(pivot)
# quarter   Q1   Q2
# dept
# Data     200  300
# ML       190  150


# Key difference:
# groupby   → gives you a Series/DataFrame, flat format
# pivot_table → reshapes data into a 2D grid (rows × columns) for comparison
```

---

## Quick Rescue Phrases (If Mind Goes Blank)

| Situation | What to say |
|---|---|
| Forgot exact syntax | *"The logic is X — let me work through the syntax"* |
| Totally blank | *"Can I take 30 seconds to think through an example?"* |
| Partially know it | *"I know this is used when... let me explain the concept first"* |
| Wrong answer realized | *"Actually, let me correct that — I think the right behavior is..."* |
| Never heard of it | *"I haven't used this specifically, but based on the name/concept it sounds like..."* |

---

## Combined Cheat Sheet — Set 2

| Topic | One-liner |
|---|---|
| `is` vs `==` | `is` = same object in memory; `==` = same value |
| Mutable default arg trap | Never use `def f(x=[])` — use `None` and create inside |
| String slice `[::-1]` | Reverses the string |
| `copy` vs `deepcopy` | deepcopy = fully independent; copy = inner objects still shared |
| `logging` vs `print` | logging has levels, timestamps, filtering — use in real code |
| `__new__` vs `__init__` | `__new__` creates the object; `__init__` initializes it |
| `_` vs `__` vs `__x__` | convention / name-mangled private / Python's magic method |
| `super()` without it | Parent `__init__` never runs → AttributeError later |
| Builder pattern | Too many optional params → chain `.with_X()` calls |
| Prototype pattern | Clone expensive object → tweak the clone |
| State pattern | Behavior changes with state → each state is its own class |
| Flyweight pattern | Many objects, shared data → cache + reuse |
| Proxy pattern | Control access → caching, lazy init, logging |
| `iloc` | By **i**nteger position; end EXCLUDED |
| `loc` | By **l**abel name; end INCLUDED |
| `apply()` | Row/column-wise custom function on DataFrame |
| `map()` | Element-wise on a single Series |
| `pivot_table` | groupby + reshape into 2D grid |
| `np.dot` vs `*` | `dot` = matrix multiply; `*` = element-wise |
| Broadcasting | NumPy stretches shapes to match — no data copy |

---

*Set 2 done. Run through Set 1 + Set 2 together the night before. You've got this. 🚀*
