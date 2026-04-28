# 🐍 Object-Oriented Programming in Python
### Complete Guide — From Why OOP Exists to Metaclasses

> *"OOP is not about memorizing syntax. It's a way of thinking — modeling the real world as objects that have data and behaviour. Once you think in objects, your code becomes easier to reason about, extend, and maintain."*

---

## 📖 How This File Flows

```
PART 1 — THE OBJECT MODEL
  1.  Why OOP? The problem it solves
  2.  Class and Object — under the hood
  3.  Constructor (__init__) — how object creation works
  4.  Function vs Method — the self keyword explained
  5.  Magic (Dunder) Methods — types and uses
  6.  Calculator example with dunder methods

PART 2 — ENCAPSULATION
  7.  Instance variables — what self.x really does in memory
  8.  Private variables and name mangling
  9.  Getter / Setter — why needed
  10. @property — the Pythonic way
  11. Class variables vs Instance variables
  12. Static methods and class methods
  13. Objects as collections

PART 3 — CLASS RELATIONSHIPS
  14. Aggregation and Composition
  15. Inheritance — how it works under the hood
  16. Method Overriding
  17. super() — all cases
  18. Types of Inheritance
  19. MRO and C3 Linearization

PART 4 — POLYMORPHISM AND ABSTRACTION
  20. Polymorphism — method overriding, duck typing
  21. Method Overloading — why Python handles it differently
  22. Operator Overloading
  23. Abstraction — abstract classes

PART 5 — ADVANCED
  24. Metaclasses — need, __new__, __init__, __init_subclass__
  25. Data Classes
  26. Descriptors
  27. Monkey Patching
```

---

# PART 1 — THE OBJECT MODEL

---

## 1. Why OOP? The Problem It Solves

Imagine writing a banking app without OOP:

```python
# WITHOUT OOP — data is scattered, no structure
account_number_1 = "ACC001"
account_holder_1 = "Arjun"
account_balance_1 = 5000.0

account_number_2 = "ACC002"
account_holder_2 = "Priya"
account_balance_2 = 12000.0

def deposit(balance, amount):
    return balance + amount

def withdraw(balance, amount):
    if amount > balance:
        raise ValueError("Insufficient funds")
    return balance - amount

# To deposit into Arjun's account:
account_balance_1 = deposit(account_balance_1, 1000)

# Problems:
# 1. Which balance belongs to which account? Easy to mix up.
# 2. What if you have 1000 accounts? 3000 variables!
# 3. No connection between the data and the functions that use it.
# 4. Adding a new account type means duplicating all variables.
```

**With OOP — data and behaviour live together:**

```python
# WITH OOP — everything about an account is in one place
class BankAccount:
    def __init__(self, number, holder, balance=0):
        self.number  = number
        self.holder  = holder
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount

# Create as many as you want — each is self-contained
arjun = BankAccount("ACC001", "Arjun", 5000)
priya = BankAccount("ACC002", "Priya", 12000)

arjun.deposit(1000)      # clear: deposit into ARJUN's account
priya.withdraw(500)      # clear: withdraw from PRIYA's account
```

OOP solves three problems:
- **Organization** — related data and functions live together
- **Reuse** — create many objects from one class definition
- **Clarity** — `arjun.deposit(1000)` is clearer than `deposit(account_balance_1, 1000)`

---

## 2. Class and Object — Under the Hood

```
CLASS  = the blueprint (design document)
OBJECT = the actual thing built from that blueprint (instance)

Like:
  Class  = architectural blueprint for a house
  Object = the actual house built from that blueprint

You can build many houses from one blueprint.
Each house has its own rooms, colour, furniture.
The blueprint itself is not a house — it describes what a house looks like.
```

```python
class Dog:                    # blueprint
    def __init__(self, name, breed):
        self.name  = name
        self.breed = breed

    def bark(self):
        return f"{self.name} says: Woof!"

tommy = Dog("Tommy", "Labrador")   # object 1
rocky = Dog("Rocky", "Pug")        # object 2

print(tommy.bark())   # Tommy says: Woof!
print(rocky.bark())   # Rocky says: Woof!
```

### What Happens in Memory When You Create an Object

```python
tommy = Dog("Tommy", "Labrador")
```

```
Step 1: Python allocates memory on the heap for a new Dog object
        ┌──────────────────────────────────┐
        │  Dog instance at 0x7f3a...       │
        │  __class__  → Dog class object  │
        │  name       → "Tommy"           │
        │  breed      → "Labrador"        │
        └──────────────────────────────────┘

Step 2: Python calls Dog.__init__(new_object, "Tommy", "Labrador")
        __init__ fills in the attributes

Step 3: Name 'tommy' in namespace points to this object
        tommy → 0x7f3a...
```

```python
# Proof — every object knows its class
print(type(tommy))             # <class '__main__.Dog'>
print(tommy.__class__)         # <class '__main__.Dog'>
print(isinstance(tommy, Dog))  # True
print(id(tommy))               # memory address

# Each object has its OWN __dict__
print(tommy.__dict__)   # {'name': 'Tommy', 'breed': 'Labrador'}
print(rocky.__dict__)   # {'name': 'Rocky', 'breed': 'Pug'}

# The CLASS has its own attributes (methods, class variables)
print(Dog.__dict__)     # {'__init__': ..., 'bark': ..., ...}
```

### Class Diagram

```
┌─────────────────────────┐
│          Dog            │   ← Class
├─────────────────────────┤
│ - name: str             │   ← Instance variables
│ - breed: str            │
├─────────────────────────┤
│ + __init__(name, breed) │   ← Methods
│ + bark() → str          │
└─────────────────────────┘

        ↓ instantiate

┌──────────────┐   ┌──────────────┐
│ tommy: Dog   │   │ rocky: Dog   │   ← Objects (instances)
│ name="Tommy" │   │ name="Rocky" │
│ breed="Lab"  │   │ breed="Pug"  │
└──────────────┘   └──────────────┘
```

---

## 3. Constructor — `__init__` — How Object Creation Works

`__init__` is NOT where the object is created. It's where the object is **initialized** (attributes filled in). The actual creation happens in `__new__`.

```python
class Order:
    def __init__(self, order_id, customer, amount):
        # self is the ALREADY CREATED empty object
        # __init__ just fills in the data
        self.order_id = order_id
        self.customer = customer
        self.amount   = amount
        self.status   = "pending"   # default value

    def confirm(self):
        self.status = "confirmed"

    def __repr__(self):
        return f"Order({self.order_id}, {self.customer}, ₹{self.amount}, {self.status})"


o1 = Order("ORD001", "Arjun", 1500)
o2 = Order("ORD002", "Priya", 3200)

print(o1)         # Order(ORD001, Arjun, ₹1500, pending)
o1.confirm()
print(o1)         # Order(ORD001, Arjun, ₹1500, confirmed)
print(o2)         # Order(ORD002, Priya, ₹3200, pending)
```

### `__new__` vs `__init__` — The Two Steps

```python
# __new__  = allocates and CREATES the object (before __init__)
# __init__ = INITIALIZES the already-created object

# Python does this when you write Order("ORD001", "Arjun", 1500):
obj = Order.__new__(Order)          # Step 1: create empty object
Order.__init__(obj, "ORD001", ...)  # Step 2: fill it in

# You rarely override __new__ (only for singletons, metaclasses)
# You always use __init__ for setup
```

---

## 4. Function vs Method — The `self` Keyword

This is where most beginners get confused.

```python
class Calculator:
    def add(self, a, b):
        return a + b
```

When you call `calc.add(3, 5)` — what is `self`?

```
obj.method(arg)  is exactly  ClassName.method(obj, arg)

calc.add(3, 5)  IS  Calculator.add(calc, 3, 5)
                                    ↑
                              self = calc (the object)
                              Python passes it automatically
```

```python
calc = Calculator()

# These two are IDENTICAL:
print(calc.add(3, 5))               # 8  — Python passes calc as self
print(Calculator.add(calc, 3, 5))   # 8  — you pass calc manually

# Proof:
print(calc.add)          # <bound method Calculator.add of <Calculator object>>
print(Calculator.add)    # <function Calculator.add at 0x...>
                         # ↑ unbound — no self attached yet
```

### Why Does `self` Exist?

```
When Python sees: calc.add(3, 5)

It does:
  1. Look up 'add' on calc → finds it on the Calculator class
  2. Creates a BOUND METHOD: wraps add + calc together
  3. Calls it: Calculator.add(calc, 3, 5)

self = the object the method was called on
self tells the method WHICH object's data to use

Without self, how would add() know whether to use calc1's data or calc2's data?
```

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    def to_fahrenheit(self):
        # self.celsius — THIS object's celsius, not some other object's
        return self.celsius * 9/5 + 32


t1 = Temperature(100)
t2 = Temperature(0)

print(t1.to_fahrenheit())  # 212.0  — uses t1.celsius = 100
print(t2.to_fahrenheit())  # 32.0   — uses t2.celsius = 0
```

---

## 5. Magic (Dunder) Methods — What They Are

Magic methods (dunder = double underscore) are special methods Python calls **automatically** in certain situations.

```
You don't call them directly.
Python calls them when you use operators, built-in functions, or syntax.

print(obj)       → obj.__str__() or obj.__repr__()
len(obj)         → obj.__len__()
obj + other      → obj.__add__(other)
obj[key]         → obj.__getitem__(key)
obj == other     → obj.__eq__(other)
obj > other      → obj.__gt__(other)
bool(obj)        → obj.__bool__()
with obj:        → obj.__enter__() and obj.__exit__()
for x in obj:    → obj.__iter__() and obj.__next__()
```

### Types of Magic Methods

```
REPRESENTATION:
  __repr__    → developer string (used in REPL, debugging)
  __str__     → user-friendly string (used in print())
  __format__  → custom format in f-strings

COMPARISON:
  __eq__      → ==
  __ne__      → !=
  __lt__      → <
  __le__      → <=
  __gt__      → >
  __ge__      → >=

ARITHMETIC:
  __add__     → +
  __sub__     → -
  __mul__     → *
  __truediv__ → /
  __floordiv__ → //
  __mod__     → %
  __pow__     → **

CONTAINER:
  __len__     → len()
  __getitem__ → obj[key]
  __setitem__ → obj[key] = value
  __delitem__ → del obj[key]
  __contains__ → in
  __iter__    → iter()
  __next__    → next()

TYPE CONVERSION:
  __int__     → int(obj)
  __float__   → float(obj)
  __bool__    → bool(obj)
  __str__     → str(obj)

OBJECT LIFECYCLE:
  __new__     → object creation
  __init__    → object initialization
  __del__     → object deletion (when refcount hits 0)

CALLABLE:
  __call__    → obj()  (make object callable like a function)

CONTEXT MANAGER:
  __enter__   → with obj:
  __exit__    → end of with block

ATTRIBUTE ACCESS:
  __getattr__    → when attribute not found
  __setattr__    → when any attribute is set
  __getattribute__→ every attribute access
```

---

## 6. Calculator with Dunder Methods — Complete Example

```python
class Money:
    """
    Represents an amount of money.
    Demonstrates dunder methods for operators, comparison,
    representation, and type conversion.
    """

    def __init__(self, amount: float, currency: str = "INR"):
        self.amount   = round(float(amount), 2)
        self.currency = currency

    # ── Representation ─────────────────────────────────────────
    def __repr__(self):
        # For developers: unambiguous, can recreate object from this
        return f"Money({self.amount}, '{self.currency}')"

    def __str__(self):
        # For users: readable
        return f"₹{self.amount:,.2f}"

    # ── Arithmetic ─────────────────────────────────────────────
    def __add__(self, other):
        if isinstance(other, Money):
            if self.currency != other.currency:
                raise ValueError(f"Cannot add {self.currency} and {other.currency}")
            return Money(self.amount + other.amount, self.currency)
        return NotImplemented    # let Python try reflected operation

    def __sub__(self, other):
        if isinstance(other, Money):
            if self.currency != other.currency:
                raise ValueError("Currency mismatch")
            return Money(self.amount - other.amount, self.currency)
        return NotImplemented

    def __mul__(self, factor):
        if isinstance(factor, (int, float)):
            return Money(self.amount * factor, self.currency)
        return NotImplemented

    def __rmul__(self, factor):
        # Handles: 3 * Money(100) → Money(100).__rmul__(3)
        return self.__mul__(factor)

    def __truediv__(self, divisor):
        if isinstance(divisor, (int, float)):
            return Money(self.amount / divisor, self.currency)
        return NotImplemented

    # ── Comparison ─────────────────────────────────────────────
    def __eq__(self, other):
        if isinstance(other, Money):
            return self.amount == other.amount and self.currency == other.currency
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Money) and self.currency == other.currency:
            return self.amount < other.amount
        return NotImplemented

    def __le__(self, other):
        return self == other or self < other

    def __gt__(self, other):
        if isinstance(other, Money) and self.currency == other.currency:
            return self.amount > other.amount
        return NotImplemented

    # ── Type conversion ────────────────────────────────────────
    def __float__(self):
        return float(self.amount)

    def __bool__(self):
        return self.amount != 0    # Money(0) is falsy


# ── Usage ──────────────────────────────────────────────────────
price   = Money(1500)
tax     = Money(270)
total   = price + tax         # calls __add__
discount = Money(100)

print(total)                  # ₹1,770.00  ← __str__
print(repr(total))            # Money(1770.0, 'INR')  ← __repr__
print(total - discount)       # ₹1,670.00
print(total * 2)              # ₹3,540.00
print(3 * price)              # ₹4,500.00  ← __rmul__

print(price < total)          # True  ← __lt__
print(price == Money(1500))   # True  ← __eq__

if total:                     # calls __bool__
    print("Amount is non-zero")

print(float(price))           # 1500.0  ← __float__
```

---

# PART 2 — ENCAPSULATION

---

## 7. Instance Variables — What `self.x` Does in Memory

```python
class User:
    def __init__(self, name, email):
        self.name  = name    # stored in THIS object's __dict__
        self.email = email
```

**`self.name = name` does:**

```
1. Takes the value of 'name' parameter
2. Stores it in self.__dict__["name"]
3. Every object has its OWN __dict__ — completely separate from other objects

Memory:
  user1.__dict__ = {"name": "Arjun", "email": "a@b.com"}
  user2.__dict__ = {"name": "Priya", "email": "p@q.com"}
  ↑ completely separate dicts — modifying user1.name doesn't touch user2.name
```

```python
user1 = User("Arjun", "a@b.com")
user2 = User("Priya", "p@q.com")

print(user1.__dict__)   # {'name': 'Arjun', 'email': 'a@b.com'}
print(user2.__dict__)   # {'name': 'Priya', 'email': 'p@q.com'}

user1.name = "Arjun Shah"     # modifies ONLY user1.__dict__
print(user1.name)   # Arjun Shah
print(user2.name)   # Priya  ← unchanged
```

### Pass by Reference — Objects Are References

```python
class Cart:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

# Objects are passed by reference (actually: pass by object reference)
def add_to_cart(cart, item):
    cart.add(item)    # modifies the SAME cart object!

my_cart = Cart()
add_to_cart(my_cart, "Laptop")
add_to_cart(my_cart, "Mouse")

print(my_cart.items)   # ['Laptop', 'Mouse']  ← modified inside function!
```

```
Why: my_cart is a REFERENCE (pointer) to the Cart object.
     When you pass my_cart to the function, you pass the reference.
     cart inside the function points to the SAME object.
     cart.add() modifies that same object.

This is called "pass by object reference" in Python.
Mutable objects (list, dict, custom objects) ARE modified.
Immutable objects (int, str) appear not to be (because they create new objects).
```

---

## 8. Private Variables and Name Mangling

```
Convention in Python:
  _name   = "private by convention" — don't access from outside
  __name  = "name mangled" — Python CHANGES the name to prevent accidental access
```

```python
class BankAccount:
    def __init__(self, holder, balance):
        self.holder   = holder       # public — access freely
        self._log     = []           # private by convention — please don't touch
        self.__balance = balance     # name mangled — Python renames this

    def deposit(self, amount):
        self.__balance += amount
        self._log.append(f"Deposited {amount}")

    def get_balance(self):
        return self.__balance


acc = BankAccount("Arjun", 5000)

# Public — fine
print(acc.holder)           # Arjun

# Convention private — accessible but you shouldn't
print(acc._log)             # []  ← works, but it's a signal: don't use this

# Name mangled — Python renamed it!
# print(acc.__balance)      # AttributeError: 'BankAccount' object has no attribute '__balance'

# Python renamed it to _BankAccount__balance
print(acc._BankAccount__balance)   # 5000  ← accessible but clearly not intended
print(acc.__dict__)  # {'holder': 'Arjun', '_log': [], '_BankAccount__balance': 5000}
```

**Why name mangling?** Prevents accidental override in subclasses:

```python
class PremiumAccount(BankAccount):
    def __init__(self, holder, balance):
        super().__init__(holder, balance)
        self.__balance = 999999    # This becomes _PremiumAccount__balance
                                   # Does NOT override _BankAccount__balance!
```

---

## 9. Getter / Setter — Why Needed

**Problem:** If attributes are public, anyone can set invalid values.

```python
class Product:
    def __init__(self, name, price):
        self.name  = name
        self.price = price   # public — no validation!

p = Product("Laptop", 50000)
p.price = -1000    # VALID in Python! No error. But -1000 price makes no sense.
p.price = "free"   # Also valid! A string as price is nonsensical.
```

**Solution — getters and setters:**

```python
class Product:
    def __init__(self, name, price):
        self.name = name
        self.set_price(price)   # use setter even in __init__

    def get_price(self):
        return self.__price

    def set_price(self, price):
        if not isinstance(price, (int, float)):
            raise TypeError("Price must be a number")
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.__price = price


p = Product("Laptop", 50000)
print(p.get_price())         # 50000
p.set_price(45000)           # valid
# p.set_price(-1000)         # ValueError: Price cannot be negative
```

But `p.get_price()` and `p.set_price()` is verbose. Python has a better way.

---

## 10. `@property` — The Pythonic Way

`@property` makes getters/setters look like normal attribute access — clean syntax with full validation.

```python
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price    # calls the setter!

    @property
    def price(self):
        """Getter — called when you READ product.price"""
        return self.__price

    @price.setter
    def price(self, value):
        """Setter — called when you WRITE product.price = x"""
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be a number")
        if value < 0:
            raise ValueError("Price cannot be negative")
        self.__price = round(float(value), 2)

    @price.deleter
    def price(self):
        """Deleter — called when you do del product.price"""
        raise AttributeError("Cannot delete price")


p = Product("Laptop", 50000)
print(p.price)       # 50000.0  ← calls getter
p.price = 45000      # calls setter — validated!
# p.price = -100     # ValueError!
# del p.price        # AttributeError!

# Looks like attribute access but has validation underneath
# This is the BEST of both worlds
```

### `@property` with Computed Attributes

```python
class Circle:
    def __init__(self, radius):
        self.radius = radius    # stored

    @property
    def area(self):
        """Computed on the fly — no stored area attribute."""
        import math
        return round(math.pi * self.radius ** 2, 2)

    @property
    def circumference(self):
        import math
        return round(2 * math.pi * self.radius, 2)


c = Circle(5)
print(c.area)           # 78.54  ← computed, not stored
print(c.circumference)  # 31.42

# c.area = 100  would raise AttributeError (no setter defined)
# This makes 'area' read-only — it's always derived from radius
```

---

## 11. Class Variables vs Instance Variables

```python
class Employee:
    company = "TechCorp"    # CLASS variable — shared by ALL instances
    count   = 0             # CLASS variable — tracking total employees

    def __init__(self, name, salary):
        Employee.count += 1          # modify class variable
        self.name   = name           # INSTANCE variable — unique per object
        self.salary = salary         # INSTANCE variable

    @classmethod
    def get_count(cls):
        return cls.count


e1 = Employee("Arjun", 50000)
e2 = Employee("Priya", 60000)

print(e1.company)          # TechCorp  ← from class
print(e2.company)          # TechCorp  ← same class variable
print(Employee.count)      # 2
print(Employee.get_count()) # 2

# Modifying class variable via class (affects all)
Employee.company = "NewCorp"
print(e1.company)   # NewCorp
print(e2.company)   # NewCorp

# Modifying via instance (creates INSTANCE variable, hides class variable)
e1.company = "StartupCo"
print(e1.company)   # StartupCo  ← e1's own instance variable
print(e2.company)   # NewCorp    ← still uses class variable
print(e1.__dict__)  # {'name': 'Arjun', 'salary': 50000, 'company': 'StartupCo'}
print(e2.__dict__)  # {'name': 'Priya',  'salary': 60000}  ← no 'company'
```

```
Python looks up attributes in this order:
  1. Instance __dict__
  2. Class __dict__
  3. Parent class __dict__  (MRO)

e1.company → check e1.__dict__ → found 'company' → return 'StartupCo'
e2.company → check e2.__dict__ → not found → check Employee.__dict__ → 'NewCorp'
```

---

## 12. Static Methods and Class Methods

```python
class DateUtils:
    date_format = "%Y-%m-%d"    # class variable

    def __init__(self, date_str):
        from datetime import datetime
        self.date = datetime.strptime(date_str, DateUtils.date_format)

    # INSTANCE METHOD — has access to self (the object)
    def days_until(self, other_date_str):
        from datetime import datetime
        other = datetime.strptime(other_date_str, DateUtils.date_format)
        return (other - self.date).days

    # CLASS METHOD — has access to cls (the class), not instance
    # Use when: method needs class info but not a specific object
    @classmethod
    def today(cls):
        from datetime import datetime
        return cls(datetime.now().strftime(cls.date_format))

    # STATIC METHOD — has access to NEITHER class nor instance
    # Use when: method is related to the class logically, but needs no class/instance data
    # It's a utility function that lives here for organization
    @staticmethod
    def is_valid_date(date_str):
        from datetime import datetime
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False


# Static — call via class (or instance, both work)
print(DateUtils.is_valid_date("2024-03-15"))   # True
print(DateUtils.is_valid_date("2024-13-45"))   # False

# Class method — creates instance using class
today = DateUtils.today()     # cls = DateUtils, creates today's date

# Instance method — needs an object
d = DateUtils("2024-01-01")
print(d.days_until("2024-12-31"))   # 365
```

```
Three method types:
┌────────────────┬─────────────────────────────┬──────────────────────────┐
│ Method Type    │ First argument              │ When to use              │
├────────────────┼─────────────────────────────┼──────────────────────────┤
│ Instance       │ self (the object)           │ Needs object's data      │
│ @classmethod   │ cls (the class)             │ Alternative constructors,│
│                │                             │ factory methods          │
│ @staticmethod  │ Nothing auto-passed         │ Utility / helper logic   │
│                │                             │ related to the class     │
└────────────────┴─────────────────────────────┴──────────────────────────┘
```

---

## 13. Object as a Collection — Container Magic Methods

Make your objects behave like lists or dicts.

```python
class ShoppingCart:
    """
    A cart that behaves like a container.
    Demonstrates: __len__, __getitem__, __contains__, __iter__
    """

    def __init__(self):
        self._items = []

    def add(self, item, price, qty=1):
        self._items.append({"item": item, "price": price, "qty": qty})

    def __len__(self):
        """len(cart) → total number of items"""
        return len(self._items)

    def __getitem__(self, index):
        """cart[0] → first item"""
        return self._items[index]

    def __contains__(self, item_name):
        """'Laptop' in cart"""
        return any(i["item"] == item_name for i in self._items)

    def __iter__(self):
        """for item in cart"""
        return iter(self._items)

    def __bool__(self):
        """if cart: → True if not empty"""
        return len(self._items) > 0

    @property
    def total(self):
        return sum(i["price"] * i["qty"] for i in self._items)


cart = ShoppingCart()
cart.add("Laptop",  50000, 1)
cart.add("Mouse",   800,   2)
cart.add("Bag",     1500,  1)

print(len(cart))            # 3         ← __len__
print(cart[0])              # first item ← __getitem__
print("Laptop" in cart)     # True      ← __contains__
print("Keyboard" in cart)   # False

for item in cart:           # ← __iter__
    print(f"  {item['item']}: ₹{item['price']} x{item['qty']}")

if cart:                    # ← __bool__
    print(f"Total: ₹{cart.total:,.2f}")
```

---

# PART 3 — CLASS RELATIONSHIPS

---

## 14. Aggregation vs Composition

How objects relate to each other.

```
AGGREGATION:  "has-a" relationship — objects can exist independently
              Library HAS Books. Books exist without a library.

COMPOSITION:  "owns-a" relationship — inner object cannot exist without outer
              Order OWNS OrderItems. OrderItem has no meaning without an Order.
```

```python
# AGGREGATION — Author exists independently of Book
class Author:
    def __init__(self, name, email):
        self.name  = name
        self.email = email

class Book:
    def __init__(self, title, author: Author):
        self.title  = title
        self.author = author    # receives an existing Author object

author = Author("Arjun", "a@b.com")
book1  = Book("Python Guide", author)
book2  = Book("ML Book", author)     # same author, two books
# If book1 is deleted, author still exists!


# COMPOSITION — Engine cannot exist without Car
class Engine:
    def __init__(self, horsepower):
        self.hp = horsepower

    def start(self):
        return f"Engine ({self.hp}hp) started"

class Car:
    def __init__(self, model, hp):
        self.model  = model
        self._engine = Engine(hp)    # Car CREATES its own Engine

    def start(self):
        return f"{self.model}: {self._engine.start()}"

car = Car("Swift", 90)
print(car.start())   # Swift: Engine (90hp) started
# If car is deleted, engine has no meaning — it's composed inside car
```

### Aggregation Class Diagram

```
┌──────────────┐        ┌──────────────┐
│    Author    │◇───────│     Book     │
├──────────────┤   has  ├──────────────┤
│ name: str    │        │ title: str   │
│ email: str   │        │ author:Author│
└──────────────┘        └──────────────┘
  ◇ = aggregation (hollow diamond at owner)

┌──────────────┐        ┌──────────────┐
│     Car      │◆───────│   Engine     │
├──────────────┤  owns  ├──────────────┤
│ model: str   │        │ hp: int      │
├──────────────┤        ├──────────────┤
│ start()      │        │ start()      │
└──────────────┘        └──────────────┘
  ◆ = composition (filled diamond at owner)
```

---

## 15. Inheritance — How It Works Under the Hood

```
Inheritance = a class gets all the attributes and methods of another class
              without copy-pasting any code.

Child IS-A Parent.
  Dog IS-A Animal.
  SavingsAccount IS-A BankAccount.
  AdminUser IS-A User.
```

```python
class Animal:
    def __init__(self, name, sound):
        self.name  = name
        self.sound = sound

    def speak(self):
        return f"{self.name} says {self.sound}"

    def eat(self):
        return f"{self.name} is eating"


class Dog(Animal):              # Dog inherits from Animal
    def __init__(self, name):
        super().__init__(name, "Woof")   # call parent's __init__
        self.tricks = []

    def learn_trick(self, trick):
        self.tricks.append(trick)

    def show_tricks(self):
        return f"{self.name} knows: {', '.join(self.tricks)}"


class Cat(Animal):
    def __init__(self, name):
        super().__init__(name, "Meow")

    def purr(self):
        return f"{self.name} purrs..."


dog = Dog("Tommy")
cat = Cat("Whiskers")

# Dog gets Animal's methods for free
print(dog.speak())    # Tommy says Woof     ← from Animal
print(dog.eat())      # Tommy is eating     ← from Animal
dog.learn_trick("Sit")
dog.learn_trick("Roll")
print(dog.show_tricks())  # Tommy knows: Sit, Roll  ← from Dog

print(cat.speak())    # Whiskers says Meow  ← from Animal
print(cat.purr())     # Whiskers purrs...   ← from Cat
```

### Under the Hood — How Python Finds Methods

```
dog.speak() — Python searches in this order:
  1. dog.__dict__          → 'speak' not there
  2. Dog.__dict__          → 'speak' not there
  3. Animal.__dict__       → 'speak' FOUND!  call it.

dog.learn_trick() — Python searches:
  1. dog.__dict__          → not there
  2. Dog.__dict__          → FOUND! call it.

This search order is called MRO (Method Resolution Order)
Dog.mro() → [Dog, Animal, object]
```

```python
print(Dog.__mro__)
# (<class 'Dog'>, <class 'Animal'>, <class 'object'>)

print(isinstance(dog, Dog))     # True
print(isinstance(dog, Animal))  # True  ← Dog IS-A Animal
print(isinstance(dog, Cat))     # False
print(issubclass(Dog, Animal))  # True
```

### Inheritance Class Diagram

```
┌──────────────────┐
│     Animal       │   ← Parent (Base class)
├──────────────────┤
│ name: str        │
│ sound: str       │
├──────────────────┤
│ speak() → str    │
│ eat() → str      │
└──────────────────┘
         △
         │ inherits (hollow triangle at parent)
    ┌────┴────┐
    │         │
┌───┴──┐  ┌──┴───┐
│ Dog  │  │ Cat  │   ← Children (Subclasses)
├──────┤  ├──────┤
│tricks│  │      │
├──────┤  ├──────┤
│learn │  │purr()│
│show()│  │      │
└──────┘  └──────┘
```

---

## 16. Method Overriding

Child class replaces a parent method with its own version.

```python
class Notification:
    def send(self, message, recipient):
        raise NotImplementedError("Subclass must implement send()")

    def log(self, message):
        print(f"[LOG] Sending: {message}")


class EmailNotification(Notification):
    def send(self, message, recipient):
        self.log(message)               # uses parent's log()
        print(f"Email to {recipient}: {message}")


class SMSNotification(Notification):
    def send(self, message, recipient):
        self.log(message)               # uses parent's log()
        print(f"SMS to {recipient}: {message}")


class PushNotification(Notification):
    def send(self, message, recipient):
        # Completely different implementation
        print(f"Push notification to device {recipient}: {message}")


# All behave the same way from caller's perspective
notifications = [
    EmailNotification(),
    SMSNotification(),
    PushNotification(),
]

for notif in notifications:
    notif.send("Your order shipped!", "arjun@example.com")

# Email to arjun@example.com: Your order shipped!
# SMS to arjun@example.com: Your order shipped!
# Push notification to device arjun@example.com: Your order shipped!
```

---

## 17. `super()` — All Cases

`super()` gives you access to the parent class. Essential when you override a method but still want the parent's behaviour.

```python
class Vehicle:
    def __init__(self, brand, speed):
        self.brand = brand
        self.speed = speed

    def info(self):
        return f"{self.brand} (max {self.speed}km/h)"

    def describe(self):
        return f"Vehicle: {self.info()}"


class Car(Vehicle):
    def __init__(self, brand, speed, doors):
        super().__init__(brand, speed)   # Case 1: call parent __init__
        self.doors = doors               # add car-specific attribute

    def info(self):
        # Case 2: extend parent method
        base_info = super().info()       # get parent's info string
        return f"{base_info}, {self.doors} doors"


class ElectricCar(Car):
    def __init__(self, brand, speed, doors, battery_kwh):
        super().__init__(brand, speed, doors)   # calls Car.__init__
        self.battery = battery_kwh

    def info(self):
        # Case 3: multi-level — super goes to Car which goes to Vehicle
        car_info = super().info()        # Car.info() which includes Vehicle.info()
        return f"{car_info}, {self.battery}kWh battery"


car = Car("Toyota", 180, 4)
ev  = ElectricCar("Tesla", 250, 4, 75)

print(car.info())          # Toyota (max 180km/h), 4 doors
print(ev.info())           # Tesla (max 250km/h), 4 doors, 75kWh battery
print(ev.describe())       # Vehicle: Tesla (max 250km/h), 4 doors, 75kWh battery
```

### `super()` in Multiple Inheritance

```python
class A:
    def greet(self):
        print("Hello from A")

class B(A):
    def greet(self):
        print("Hello from B")
        super().greet()    # goes to A (follows MRO)

class C(A):
    def greet(self):
        print("Hello from C")
        super().greet()    # goes to A (follows MRO)

class D(B, C):
    def greet(self):
        print("Hello from D")
        super().greet()    # follows MRO: D → B → C → A

d = D()
d.greet()
# Hello from D
# Hello from B
# Hello from C
# Hello from A
```

---

## 18. Types of Inheritance

### Single Inheritance
```python
class Animal: pass
class Dog(Animal): pass   # Dog inherits from one parent
```

### Multi-Level Inheritance
```python
class Animal: pass
class Mammal(Animal): pass     # Mammal inherits Animal
class Dog(Mammal): pass        # Dog inherits Mammal (and Animal)
# MRO: Dog → Mammal → Animal → object
```

### Multiple Inheritance
```python
class Flyable:
    def fly(self): return "Flying"

class Swimmable:
    def swim(self): return "Swimming"

class Duck(Flyable, Swimmable):   # inherits from BOTH
    def quack(self): return "Quack!"

d = Duck()
print(d.fly())    # Flying
print(d.swim())   # Swimming
print(d.quack())  # Quack!
```

### Hierarchical Inheritance
```python
class Shape: pass
class Circle(Shape): pass    # Multiple children from one parent
class Square(Shape): pass
class Triangle(Shape): pass
```

### Hybrid Inheritance
```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass    # Combination — creates the diamond problem
```

---

## 19. MRO and C3 Linearization

**The Diamond Problem:**

```
        A
       / \
      B   C
       \ /
        D

D inherits from B and C, both inherit from A.
When D calls a method, which path does Python follow?
```

**Python solves this with C3 Linearization — a specific algorithm.**

The rule: `L[C] = C + merge(L[parents], [parents])`

```python
class A:
    def hello(self):
        print("A")

class B(A):
    def hello(self):
        print("B")
        super().hello()

class C(A):
    def hello(self):
        print("C")
        super().hello()

class D(B, C):
    def hello(self):
        print("D")
        super().hello()

d = D()
d.hello()
print(D.__mro__)
```

Output:
```
D
B
C
A
(<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)
```

**C3 Algorithm — How to Solve Any MRO Problem:**

```
Given: class D(B, C), class B(A), class C(A)

L[A] = [A, object]
L[B] = [B] + merge([A, object], [A])
     = [B, A, object]
L[C] = [C, A, object]

L[D] = [D] + merge(L[B], L[C], [B, C])
     = [D] + merge([B,A,object], [C,A,object], [B,C])

Step 1: Take first element of first list: B
        Is B in TAIL of any other list? (tail = all except first element)
        [C,A,object] tail = [A,object] → B not there ✅
        [B,C] tail = [C] → B not there ✅
        Add B. Remove B from all lists.
        = [D, B] + merge([A,object], [C,A,object], [C])

Step 2: Take C from first list [A,object] → A
        Is A in tail of [C,A,object]? [A,object] → YES ❌ skip
        Try next list: [C,A,object] → C
        Is C in tail of [A,object]? No. Is C in tail of [C]? No ✅
        Add C. Remove C.
        = [D, B, C] + merge([A,object], [A,object], [])

Step 3: A — not in tail of anything ✅
        = [D, B, C, A] + merge([object], [object], [])

Step 4: object → [D, B, C, A, object]

Final MRO: D → B → C → A → object
```

---

# PART 4 — POLYMORPHISM AND ABSTRACTION

---

## 20. Polymorphism — Same Interface, Different Behaviour

```
Polymorphism = "many forms"
Same method name, different behaviour depending on the object.
```

```python
class Shape:
    def area(self):
        raise NotImplementedError

class Circle(Shape):
    def __init__(self, r): self.r = r
    def area(self):
        import math
        return round(math.pi * self.r**2, 2)

class Rectangle(Shape):
    def __init__(self, w, h): self.w = w; self.h = h
    def area(self):
        return self.w * self.h

class Triangle(Shape):
    def __init__(self, b, h): self.b = b; self.h = h
    def area(self):
        return 0.5 * self.b * self.h


# Polymorphism — same call, different result
shapes = [Circle(5), Rectangle(4, 6), Triangle(3, 8)]

for shape in shapes:
    print(f"{shape.__class__.__name__}: area = {shape.area()}")

# Circle:    area = 78.54
# Rectangle: area = 24
# Triangle:  area = 12.0
```

**Total area of all shapes — polymorphism makes this trivial:**

```python
total = sum(s.area() for s in shapes)   # works regardless of shape type!
```

---

## 21. Method Overloading — Why Python Handles It Differently

In Java/C++, you can define the same method multiple times with different parameters:
```java
// Java
int add(int a, int b) { return a + b; }
float add(float a, float b) { return a + b; }
```

**Python doesn't support this** — if you define the same name twice, the second replaces the first:

```python
class Calculator:
    def add(self, a, b):
        return a + b

    def add(self, a, b, c):    # REPLACES the previous add!
        return a + b + c

calc = Calculator()
# calc.add(1, 2)    ← TypeError: add() missing 1 required argument
calc.add(1, 2, 3)   # 6 — only this works now
```

**Python's solution — default arguments and `*args`:**

```python
class Calculator:
    def add(self, *args):
        """Handles 2, 3, or any number of arguments."""
        return sum(args)

    def multiply(self, a, b, factor=1):
        """Optional third argument with default."""
        return a * b * factor


calc = Calculator()
print(calc.add(1, 2))          # 3
print(calc.add(1, 2, 3))       # 6
print(calc.add(1, 2, 3, 4))    # 10
print(calc.multiply(3, 4))     # 12
print(calc.multiply(3, 4, 2))  # 24
```

---

## 22. Operator Overloading

Define how operators work on your objects using dunder methods.

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):     # v1 + v2
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):     # v1 - v2
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):    # v * 3
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):   # 3 * v
        return self.__mul__(scalar)

    def __eq__(self, other):      # v1 == v2
        return self.x == other.x and self.y == other.y

    def __abs__(self):            # abs(v) → magnitude
        return (self.x**2 + self.y**2) ** 0.5

    def __str__(self):
        return f"Vector({self.x}, {self.y})"


v1 = Vector(1, 2)
v2 = Vector(3, 4)

print(v1 + v2)     # Vector(4, 6)
print(v2 - v1)     # Vector(2, 2)
print(v1 * 3)      # Vector(3, 6)
print(3 * v1)      # Vector(3, 6)  ← __rmul__
print(abs(v2))     # 5.0
print(v1 == Vector(1, 2))  # True
```

---

## 23. Abstraction — Abstract Classes

Abstraction = define WHAT to do (interface), let subclasses define HOW.

```python
from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    """
    Abstract base class for payment gateways.
    Defines the INTERFACE — what every gateway MUST have.
    You cannot instantiate this directly.
    """

    @abstractmethod
    def process_payment(self, amount: float) -> dict:
        """Must be implemented by every subclass."""
        pass

    @abstractmethod
    def refund(self, transaction_id: str) -> dict:
        pass

    def validate_amount(self, amount):
        """Concrete method — shared by all gateways."""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return True


class RazorpayGateway(PaymentGateway):
    def process_payment(self, amount):
        self.validate_amount(amount)
        return {"gateway": "Razorpay", "status": "success", "amount": amount}

    def refund(self, transaction_id):
        return {"gateway": "Razorpay", "refund": transaction_id, "status": "initiated"}


class StripeGateway(PaymentGateway):
    def process_payment(self, amount):
        self.validate_amount(amount)
        return {"gateway": "Stripe", "status": "success", "amount": amount}

    def refund(self, transaction_id):
        return {"gateway": "Stripe", "refund": transaction_id, "status": "initiated"}


# PaymentGateway() → TypeError: Can't instantiate abstract class
# You MUST use a concrete subclass

def process_order(gateway: PaymentGateway, amount: float):
    return gateway.process_payment(amount)


gw = RazorpayGateway()
print(process_order(gw, 1500))   # {"gateway": "Razorpay", ...}
```

---

# PART 5 — ADVANCED

---

## 24. Metaclasses — Classes That Create Classes

```
In Python:
  int creates integers      → int is a class
  str creates strings       → str is a class
  type creates classes      → type is the metaclass!

Every class is an instance of type.
Metaclass = the class of a class.
```

```python
# Proof:
print(type(42))        # <class 'int'>
print(type(int))       # <class 'type'>   ← int is an instance of type!
print(type(type))      # <class 'type'>   ← type is its own metaclass

class Dog: pass
print(type(Dog))       # <class 'type'>   ← Dog is an instance of type!
```

### Why You'd Need a Metaclass

When you want to **automatically modify or validate every class** that inherits from something — without writing that code in each class.

```python
# Use case: Automatically add a 'created_at' to every model class
import datetime

class ModelMeta(type):
    """Metaclass that adds 'created_at' to every model class."""

    def __new__(mcs, name, bases, namespace):
        # mcs    = the metaclass (ModelMeta)
        # name   = name of the class being created ("User", "Product", etc.)
        # bases  = parent classes
        # namespace = dict of attributes/methods in the class body

        # Add a timestamp to every class
        namespace["created_at"] = datetime.datetime.now().isoformat()

        # Automatically make all method names lowercase
        # (just as an example of what metaclasses can do)
        new_namespace = {}
        for key, value in namespace.items():
            if callable(value) and not key.startswith("__"):
                new_namespace[key.lower()] = value
            else:
                new_namespace[key] = value

        return super().__new__(mcs, name, bases, new_namespace)

    def __init__(cls, name, bases, namespace):
        # Called after __new__ — cls is the newly created class
        print(f"Class '{name}' was created at {cls.created_at}")
        super().__init__(name, bases, namespace)


class BaseModel(metaclass=ModelMeta):
    """All models use ModelMeta as metaclass."""
    pass

class User(BaseModel):
    def __init__(self, name):
        self.name = name

    def GetName(self):    # defined with capitals
        return self.name

class Product(BaseModel):
    def __init__(self, title):
        self.title = title
```

### The Three Metaclass Hooks

```
__new__(mcs, name, bases, namespace)
  → Called FIRST to CREATE the class object
  → mcs = the metaclass
  → Return value becomes the class
  → Use when: you need to modify the class attributes/methods BEFORE creation

__init__(cls, name, bases, namespace)
  → Called AFTER __new__ to INITIALIZE the class
  → cls = the newly created class
  → Use when: you need to do setup AFTER the class exists (register it, validate it)

__init_subclass__(cls, **kwargs)  [on the BASE class, not metaclass]
  → Called when a SUBCLASS is created (simpler alternative to metaclass)
  → cls = the subclass being defined
  → Use when: you want to hook into subclass creation without a full metaclass
```

```python
# __init_subclass__ — simpler than metaclass for most use cases
class PluginBase:
    _registry = {}

    def __init_subclass__(cls, plugin_name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if plugin_name:
            PluginBase._registry[plugin_name] = cls
            print(f"Registered plugin: {plugin_name} → {cls.__name__}")


class PDFPlugin(PluginBase, plugin_name="pdf"):
    def process(self, file):
        return f"Processing PDF: {file}"

class ExcelPlugin(PluginBase, plugin_name="excel"):
    def process(self, file):
        return f"Processing Excel: {file}"


# Automatically registered!
print(PluginBase._registry)
# {'pdf': <class 'PDFPlugin'>, 'excel': <class 'ExcelPlugin'>}

# Use the registry
plugin = PluginBase._registry["pdf"]()
print(plugin.process("report.pdf"))
```

---

## 25. Data Classes — Automatic Boilerplate

```python
# WITHOUT dataclass — lots of repetitive code
class Product:
    def __init__(self, name, price, qty):
        self.name  = name
        self.price = price
        self.qty   = qty

    def __repr__(self):
        return f"Product(name={self.name!r}, price={self.price}, qty={self.qty})"

    def __eq__(self, other):
        return (self.name, self.price, self.qty) == (other.name, other.price, other.qty)
```

```python
# WITH dataclass — Python writes all that for you
from dataclasses import dataclass, field

@dataclass
class Product:
    name:  str
    price: float
    qty:   int = 1              # default value

    # Computed field — not included in __init__
    @property
    def total(self):
        return self.price * self.qty


p1 = Product("Laptop", 50000, 2)
p2 = Product("Mouse",  800)      # qty defaults to 1

print(p1)         # Product(name='Laptop', price=50000, qty=2)  ← __repr__ auto
print(p1 == Product("Laptop", 50000, 2))  # True ← __eq__ auto
print(p1.total)   # 100000


# Frozen dataclass — immutable like namedtuple but with more features
@dataclass(frozen=True)
class Point:
    x: float
    y: float

p = Point(1.0, 2.0)
# p.x = 5  ← FrozenInstanceError: cannot assign to field 'x'


# With ordering
@dataclass(order=True)
class Score:
    value: int
    player: str = field(compare=False)   # exclude from comparison

s1 = Score(95, "Arjun")
s2 = Score(87, "Priya")
print(s1 > s2)   # True  ← __gt__ auto-generated (by value only)
print(sorted([s2, s1]))  # [Score(value=87,...), Score(value=95,...)]
```

---

## 26. Descriptors

A descriptor is an object that controls attribute access on another object. This is how `@property`, `@classmethod`, `@staticmethod` are implemented in Python.

```python
# property IS a descriptor. Let's build our own:

class Validator:
    """A descriptor that validates a numeric range."""

    def __init__(self, min_val, max_val):
        self.min_val = min_val
        self.max_val = max_val
        self.name = None           # will be set by __set_name__

    def __set_name__(self, owner, name):
        """Called when the descriptor is assigned to a class attribute."""
        self.name = name           # e.g., "age" or "score"

    def __get__(self, obj, objtype=None):
        """Called when the attribute is READ."""
        if obj is None:
            return self            # accessed on class, not instance
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        """Called when the attribute is WRITTEN."""
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self.name} must be a number")
        if not self.min_val <= value <= self.max_val:
            raise ValueError(f"{self.name} must be between {self.min_val} and {self.max_val}")
        obj.__dict__[self.name] = value


class Student:
    age   = Validator(5, 25)      # age must be 5–25
    score = Validator(0, 100)     # score must be 0–100

    def __init__(self, name, age, score):
        self.name  = name
        self.age   = age           # calls Validator.__set__
        self.score = score         # calls Validator.__set__


s = Student("Arjun", 20, 95)
print(s.age)     # 20  ← calls Validator.__get__

# s.age = 30     # ValueError: age must be between 5 and 25
# s.score = 150  # ValueError: score must be between 0 and 100
```

---

## 27. Duck Typing

```
"If it walks like a duck and quacks like a duck, it's a duck."

Python doesn't care about the TYPE of an object.
It only cares whether the object HAS the method/attribute you're trying to use.
```

```python
# No inheritance needed — just need the right methods

class Dog:
    def speak(self):
        return "Woof!"

class Cat:
    def speak(self):
        return "Meow!"

class Robot:
    def speak(self):
        return "Beep boop!"

class HumanBaby:
    def speak(self):
        return "Goo goo!"


# This function doesn't care what TYPE animal is
# It just needs: something with a speak() method
def make_noise(animal):
    return animal.speak()

creatures = [Dog(), Cat(), Robot(), HumanBaby()]
for c in creatures:
    print(make_noise(c))   # works on ALL of them!
```

```python
# Real use case: file-like objects
def process_data(file_like):
    """Works with any object that has read() — file, StringIO, BytesIO, socket..."""
    data = file_like.read()
    return data.upper()

# Works with all of these:
import io
process_data(open("real_file.txt"))      # actual file
process_data(io.StringIO("hello"))       # in-memory string "file"
process_data(io.BytesIO(b"hello"))       # in-memory bytes "file"
```

---

## 28. Monkey Patching

Monkey patching = modifying a class or module at **runtime** after it's been defined.

```python
class EmailService:
    def send(self, to, subject, body):
        # In production: connects to SMTP server
        print(f"SENDING real email to {to}")


# In TESTS, you don't want to send real emails.
# Monkey patch the method with a fake:
def fake_send(self, to, subject, body):
    print(f"FAKE email to {to}: {subject}")
    # No actual email sent!

# Replace the real method with the fake at runtime
EmailService.send = fake_send

# Now all EmailService instances use the fake
svc = EmailService()
svc.send("arjun@example.com", "Order confirmed", "Your order is ready")
# FAKE email to arjun@example.com: Order confirmed

# Also used to add methods to existing classes
class MyList(list):
    pass

# Add a method to the built-in list (works on Python's list!)
def sum_list(self):
    return sum(self)

list.total = sum_list       # monkey patch built-in!
numbers = [1, 2, 3, 4, 5]
print(numbers.total())      # 15
```

> ⚠️ Use monkey patching carefully — it makes code hard to reason about. Best used in tests.

---

## Summary — The Complete OOP Mental Model

```
CLASS = blueprint | OBJECT = instance built from blueprint
Every object has: __dict__ (its data) + __class__ (its type)

DUNDER METHODS = Python calls these automatically
  __init__: initialize | __str__: print() | __repr__: repr()
  __add__: + | __eq__: == | __len__: len() | __iter__: for loop

self = the object the method was called on
  obj.method(arg) = ClassName.method(obj, arg)

ENCAPSULATION:
  _var  = private by convention
  __var = name mangled to _ClassName__var
  @property = getter/setter with attribute syntax

CLASS vs INSTANCE variables:
  class Foo:
    cls_var = 0     ← shared by all instances
    def __init__(self):
      self.inst_var = 0  ← unique per instance

METHOD TYPES:
  def method(self)       → instance method
  @classmethod           → gets cls
  @staticmethod          → gets nothing

INHERITANCE: Child IS-A Parent. Gets all parent methods.
  MRO: the order Python searches for methods (C3 linearization)
  super() → access parent in MRO order

POLYMORPHISM: same interface, different behaviour
  method overriding + duck typing

ABSTRACTION: ABC + @abstractmethod = force subclasses to implement

METACLASS: class of a class. type() by default.
  __new__: create class | __init__: setup class | __init_subclass__: simpler alternative

DUCK TYPING: don't check type, check if method exists
DESCRIPTORS: objects that control attribute access (__get__, __set__, __set_name__)
MONKEY PATCHING: modify classes at runtime (use in tests only)
```

---

## 🎯 15 Questions Across All Topics

1. What's the difference between a class and an object?
2. What does `self` represent and why does Python need it?
3. Why does `obj.method(arg)` pass the object automatically?
4. What is name mangling? What does `__balance` become?
5. What's the difference between `@property` and a regular getter method?
6. When should you use a `@classmethod` vs `@staticmethod`?
7. What's the difference between a class variable and an instance variable?
8. What is the diamond problem and how does Python solve it?
9. What is C3 linearization — what MRO does `class D(B, C)` where both B and C inherit from A give?
10. What is duck typing? How does it differ from type checking?
11. Why doesn't Python support method overloading and what's the alternative?
12. What are the three metaclass hooks and when is each called?
13. What does a descriptor's `__set__` method do?
14. What is monkey patching and when is it appropriate?
15. What boilerplate does `@dataclass` automatically generate?
