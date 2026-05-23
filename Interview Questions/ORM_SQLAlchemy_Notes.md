# Module 5 — ORM & SQLAlchemy
### Quick Revision Notes · Interview Prep

---

## 1. The Problem ORM Solves — Why It Was Needed

Without ORM, developers wrote raw SQL strings inside Python code.

**5 core problems with raw SQL at team scale:**

| Problem | What goes wrong |
|---|---|
| SQL as strings | No syntax highlighting, typos found only at runtime |
| Tuples, not objects | `row[0]`, `row[1]`... no names, no autocomplete |
| DB coupling | MySQL syntax ≠ PostgreSQL — switching DBs = rewrite everything |
| SQL injection risk | String concatenation = security vulnerability |
| No schema tracking | Table changes not versioned, team sync becomes a nightmare |

> Raw SQL is fine for tiny scripts. At team scale with evolving schemas — it becomes unmaintainable.

---

## 2. What is ORM?

**ORM = Object-Relational Mapping**

Maps between the Python world and the Database world:

```
PYTHON WORLD          MAPS TO        DATABASE WORLD
─────────────────────────────────────────────────────
Class                 ──────────►    Table
Attribute             ──────────►    Column
Instance (object)     ──────────►    Row
Setting attribute     ──────────►    UPDATE SQL
Creating instance     ──────────►    INSERT SQL
Deleting instance     ──────────►    DELETE SQL
```

> **Core idea: You write Python. ORM generates and executes the SQL. You never write SQL manually.**

---

## 3. The 3-Layer Architecture

```
┌─────────────────────────────────────────────────┐
│        Layer 1 — Application / Business Logic    │
│     Flask · FastAPI · Django · Your Python code  │
│              (YOU write this layer)              │
└────────────────────┬────────────────────────────┘
                     │  Python objects
                     ▼
┌─────────────────────────────────────────────────┐
│              Layer 2 — ORM (SQLAlchemy)          │
│  Maps classes → tables · Translates Python → SQL │
│  Manages connections · Handles transactions      │
│  Tracks object changes · Schema migrations       │
│            (ORM handles this layer)              │
└────────────────────┬────────────────────────────┘
                     │  Generated SQL
                     ▼
┌─────────────────────────────────────────────────┐
│           Layer 3 — Database Engine              │
│     PostgreSQL · MySQL · SQLite · Oracle         │
└─────────────────────────────────────────────────┘

KEY INSIGHT: Swap Layer 3 (change the DB) without
touching Layer 1 — this is ORM's biggest industry value.
```

---

## 4. What ORM Does — Step by Step Flow

```
You write Python
      │
      ▼
raj = User(name="Raj", age=25)
      │
      ▼  ORM reads Column definitions + __tablename__
      │
      ▼
session.add(raj)
      │
      ▼  Object enters → PENDING state
      │
      ▼
session.commit()
      │
      ▼  ORM generates SQL:
      │  INSERT INTO users (name, age) VALUES ('Raj', 25)
      │
      ▼  Sent to database over connection pool
      │
      ▼
Object enters → PERSISTENT state
raj.id is now populated (DB assigned it)
ORM stores raj in Identity Map
```

---

## 5. The 4 Object States — Critical for Interviews

```
   User() called
        │
        ▼
┌───────────────┐
│   TRANSIENT   │  Created, NOT in session, no DB row
└───────┬───────┘
        │  session.add()
        ▼
┌───────────────┐
│    PENDING    │  In session, NOT yet committed, no DB row
└───────┬───────┘
        │  session.commit()
        ▼
┌───────────────┐
│  PERSISTENT   │  In session + has DB row, changes tracked live
└───────┬───────┘
        │  session.close() / expunge()
        ▼
┌───────────────┐
│   DETACHED    │  Has DB row, but NO active session watching it
└───────────────┘
```

| State | In Session? | DB Row? | Changes Tracked? |
|---|---|---|---|
| Transient | ✗ | ✗ | ✗ |
| Pending | ✓ | ✗ | ✗ |
| Persistent | ✓ | ✓ | ✓ |
| Detached | ✗ | ✓ | ✗ |

---

## 6. The Session — ORM's Most Important Concept

The **Session** is the staging area — a conversation between your Python code and the database.

```
┌──────────────────────────────────────────┐
│              SESSION BOUNDARY            │
│                                          │
│   Python Objects  ──►  Identity Map      │
│        │                    │            │
│        │   Unit of Work     │            │
│        ▼                    ▼            │
│   Change Tracker  ──►  SQL Queue         │
└──────────────────────┬───────────────────┘
                       │  on commit()
                       ▼
                   DATABASE
```

**Key session operations:**

| Operation | What it does |
|---|---|
| `session.add(obj)` | Register object — moves to Pending |
| `session.add_all([])` | Register multiple objects |
| `session.commit()` | Flush + finalise transaction permanently |
| `session.flush()` | Send SQL to DB but keep transaction open |
| `session.rollback()` | Undo all changes since last commit |
| `session.close()` | End session, persistent objects become detached |
| `session.delete(obj)` | Mark object for deletion on next commit |
| `session.get(Model, id)` | Fetch by primary key (fastest query) |

---

## 7. Unit of Work Pattern

ORM collects **all changes** made to objects within a session and writes them to the DB in a **single optimised batch** on commit.

```
┌─────────────────────────────────────────────┐
│              Unit of Work                   │
│                                             │
│  obj1.name = "Raj"    → tracked             │
│  obj2.age  = 25       → tracked             │
│  session.add(obj3)    → tracked             │
│  session.delete(obj4) → tracked             │
│               │                             │
│               │  session.commit()           │
│               ▼                             │
│  Single batch of SQL sent to DB:            │
│  UPDATE users SET name='Raj' WHERE id=1     │
│  UPDATE users SET age=25 WHERE id=2         │
│  INSERT INTO users ...                      │
│  DELETE FROM users WHERE id=4              │
└─────────────────────────────────────────────┘
```

**Benefits:** Fewer DB round trips · Changes are atomic · Optimised SQL batching

---

## 8. Identity Map

A **cache inside the session** that maps each DB row (by primary key) to exactly one Python object.

```
Query: session.get(User, 1)  ──►  DB hit → creates object → stores in map
Query: session.get(User, 1)  ──►  found in map → returns SAME object, no DB call
Query: session.get(User, 1)  ──►  found in map → returns SAME object, no DB call
```

> If you query the same row twice in one session — you get the **same Python object** both times. No duplicate DB calls. No inconsistent state.

---

## 9. ORM Relationship Types

```
ONE-TO-ONE
──────────
User ◄──────────────► UserProfile
 1                          1
(one user, one profile)


ONE-TO-MANY  ← most common in industry
────────────
User ──────────────────► Order #1
  1                      Order #2
                         Order #3
                         (many)
FK lives on the "many" side (orders.user_id)


MANY-TO-MANY
────────────
Student ──► [student_course] ◄── Course
 Raj              │             Python
 Priya      Junction Table       Django
            (ORM creates this automatically)
```

**Two sides of a relationship:**

```
# User side:
orders = relationship("Order", back_populates="user")

# Order side:
user = relationship("User", back_populates="orders")
```

`back_populates` keeps both sides in sync — setting `order.user = raj` automatically adds the order to `raj.orders`.

---

## 10. Lazy vs Eager Loading — The N+1 Problem

```
LAZY LOADING (default) — THE N+1 PROBLEM
──────────────────────────────────────────
Query 1:  SELECT * FROM users          → fetches 100 users
Query 2:  SELECT * FROM orders WHERE user_id=1
Query 3:  SELECT * FROM orders WHERE user_id=2
...
Query 101: SELECT * FROM orders WHERE user_id=100

= 101 DB round trips for 100 users ← KILLS performance


EAGER LOADING (joinedload) — THE FIX
──────────────────────────────────────
Query 1:  SELECT users.*, orders.*
          FROM users LEFT JOIN orders ON users.id = orders.user_id

= 1 DB round trip for everything ← PRODUCTION SAFE
```

**Rule:** If you know you'll access related data — always use eager loading.

---

## 11. ORM Transactions Flow

```
try:
    ┌──────────────────────────────┐
    │  operation 1 (debit sender)  │
    │  operation 2 (credit receiver│  ◄── All inside one session
    │  session.commit()            │
    └──────────────┬───────────────┘
                   │ success
                   ▼
            Both changes permanent
            Visible to all connections

except Exception:
    ┌──────────────────────────────┐
    │  session.rollback()          │  ◄── BOTH changes cancelled
    └──────────────────────────────┘
            DB back to clean state
            Neither change applied
```

> Non-negotiable for: banking, payments, e-commerce order processing, inventory management.

---

## 12. What is SQLAlchemy?

SQLAlchemy is a **complete database toolkit for Python** — not just an ORM. It has two distinct layers:

```
┌──────────────────────────────────────────────────────┐
│               Your Python Application                │
└──────────┬────────────────────────┬──────────────────┘
           │                        │
           ▼                        ▼
┌──────────────────┐    ┌──────────────────────────────┐
│  SQLAlchemy ORM  │    │      SQLAlchemy Core          │
│  (Layer 2)       │    │      (Layer 1)                │
│                  │    │                               │
│ Classes → Tables │    │ SQL Expression Language       │
│ Objects → Rows   │    │ Programmatic SQL building     │
│ Session          │    │ No class mapping              │
│ Relationships    │    │ Returns plain rows            │
│ State tracking   │    │                               │
└────────┬─────────┘    └──────────────┬────────────────┘
         │                             │
         └──────────────┬──────────────┘
                        │ ORM is built ON TOP of Core
                        ▼
         ┌──────────────────────────────┐
         │   Engine + Connection Pool   │
         │  Dialect · Pooling · DBAPI   │
         └──────┬───────────────────────┘
                │
     ┌──────────┼──────────────┬──────────┐
     ▼          ▼              ▼          ▼
 PostgreSQL   MySQL         SQLite     Oracle
```

---

## 13. The Engine

The Engine is the **starting point of everything** in SQLAlchemy.

```
create_engine("dialect+driver://user:pass@host:port/dbname")
       │
       ▼
┌──────────────────────────────────────────┐
│                ENGINE                    │
│                                          │
│  ┌─────────────────────────────────┐     │
│  │       Connection Pool           │     │
│  │  conn1  conn2  conn3  ...conn10 │     │
│  └─────────────────────────────────┘     │
│                                          │
│  Dialect → translates to correct SQL     │
│  DBAPI   → low-level DB communication    │
└──────────────────────────────────────────┘
       │
       │  LAZY — no connection opened until first query
       ▼
   Database
```

**Connection strings:**

| Database | Format |
|---|---|
| SQLite (file) | `sqlite:///filename.db` |
| SQLite (memory) | `sqlite:///:memory:` |
| PostgreSQL | `postgresql+psycopg2://user:pass@host:5432/dbname` |
| MySQL | `mysql+pymysql://user:pass@host:3306/dbname` |

**Key insight:** `create_engine()` does NOT open a connection immediately — it's **lazy initialisation**.

---

## 14. Declarative Base

```
declarative_base()
        │
        ▼
┌───────────────────┐
│       Base        │  ← Registry for ALL models
│                   │
│  MetaData object  │  ← Holds all table definitions
│  Mapper registry  │  ← Maps classes to tables
└────────┬──────────┘
         │  All models inherit from Base
         ▼
┌─────────┐  ┌──────────┐  ┌──────────┐
│  User   │  │ Product  │  │  Order   │
│(Base)   │  │ (Base)   │  │ (Base)   │
└─────────┘  └──────────┘  └──────────┘
         │
         │  Base.metadata.create_all(engine)
         ▼
   All tables created in DB
```

---

## 15. Session Lifecycle in a Web Request

```
HTTP Request arrives
        │
        ▼
SessionLocal()  ← create new session
        │
        ▼
┌───────────────────────────────┐
│   Route Handler / CRUD fn     │
│                               │
│   session.query(...)          │
│   session.add(...)            │
│   session.commit()            │
└───────────────┬───────────────┘
                │
        success ▼         error ▼
        commit()          rollback()
                │               │
                └───────┬───────┘
                        ▼
                  session.close()
                        │
                        ▼
                HTTP Response sent
```

---

## 16. flush() vs commit() — Flow

```
session.flush()
      │
      ▼
SQL sent to DB ──► Transaction still OPEN
                   Changes visible within THIS session only
                   Other connections CANNOT see changes
                   Can still be rolled back
                   Use when: need DB-generated id before committing

session.commit()
      │
      ▼
SQL sent to DB ──► Transaction CLOSED
                   Changes PERMANENT
                   All connections can see changes
                   Cannot be rolled back
                   Use when: all operations complete successfully
```

---

## 17. Real Project Structure

```
project/
├── database.py          ← engine, Base, SessionLocal (import everywhere)
│
├── models/
│   ├── __init__.py
│   ├── user.py          ← User class (inherits Base)
│   ├── product.py       ← Product class
│   └── order.py         ← Order class
│
├── schemas/             ← Pydantic models (validation for APIs)
│   └── user.py
│
├── crud/                ← All DB operations live here
│   └── user.py          ← get_user, create_user, update_user, delete_user
│
├── alembic/             ← Migration files (versioned schema changes)
│   └── versions/
│
└── main.py              ← App entry point
```

**The golden rule:** `database.py` is created once, imported everywhere. The Session is created per request, never shared between requests.

---

## 18. ORM vs Raw SQL vs Query Builder

| Approach | What it is | When used |
|---|---|---|
| Raw SQL | Direct SQL strings via `cursor.execute()` | Tiny scripts, extreme performance needs |
| Query Builder (Core) | Programmatic SQL, returns plain rows | Complex queries needing SQL control, no object overhead |
| ORM | Full class mapping + state tracking | Standard choice for all web apps and APIs |

**Industry reality:** Most Python web apps use ORM for 95% of queries and drop to raw SQL only for complex reports or bulk operations on millions of rows.

---

## 19. Column Types Cheatsheet

| SQLAlchemy Type | Python Type | DB Type |
|---|---|---|
| `Integer` | int | INT |
| `String(n)` | str | VARCHAR(n) |
| `Text` | str | TEXT (unlimited) |
| `Float` | float | FLOAT |
| `Numeric(p,s)` | Decimal | DECIMAL(p,s) |
| `Boolean` | bool | BOOLEAN |
| `DateTime` | datetime | DATETIME |
| `ForeignKey("table.col")` | int | INT + FK constraint |

---

## 20. ForeignKey vs relationship()

```
ForeignKey("users.id")
      │
      ▼
Database level constraint
Enforces referential integrity
Actual column in the table (user_id INTEGER)
Prevents orphaned records


relationship("User", back_populates="orders")
      │
      ▼
Python level convenience
No column created
Lets you navigate: user.orders, order.user
SQLAlchemy handles JOIN internally
```

> ForeignKey = DB enforces the link.
> relationship() = Python lets you navigate the link.
> **You need BOTH.**

---

## 21. Key Things That Confuse Freshers

**`default=datetime.utcnow` — no parentheses**
```
CORRECT:  created_at = Column(DateTime, default=datetime.utcnow)
WRONG:    created_at = Column(DateTime, default=datetime.utcnow())
```
Without `()` → passes the function, called fresh at each INSERT.
With `()` → evaluated once at class definition — every row gets the same timestamp.

---

**`filter()` vs `filter_by()`**
```
filter_by(name="Raj")           ← equality only, keyword args, cleaner
filter(User.name == "Raj")      ← full expressions, supports all operators
filter(User.age >= 18)          ← only possible with filter()
filter(User.name.like("%Raj%")) ← only possible with filter()
```

---

**`.all()` vs `.first()` vs `.one()`**
```
.all()    → returns list (empty list if nothing found)
.first()  → returns object or None (adds LIMIT 1 to SQL)
.one()    → returns object, raises error if 0 or 2+ results found
.scalar() → returns single value (use with count, sum etc.)
```

---

## 22. Interview Questions & Ideal Answers

---

**Q: What is SQLAlchemy and why is it used?**
> SQLAlchemy is a Python SQL toolkit and ORM with two layers — Core for SQL expression building and ORM for class-to-table mapping. It's used because it provides database independence, removes raw SQL strings from application code, manages connections via pooling, tracks object state automatically, and makes schema changes manageable through Alembic migrations.

---

**Q: What is the difference between SQLAlchemy Core and ORM?**
> Core is the lower layer — it builds and executes SQL programmatically using Table objects and returns plain rows. ORM is built on top of Core and adds class-to-table mapping, object state tracking, session management, and relationship navigation. Use Core when you need SQL-level control without object overhead; use ORM for standard application CRUD.

---

**Q: What is the Engine and when is a connection actually opened?**
> The Engine represents the database — it holds the connection pool and dialect. Created once with `create_engine()`. It does NOT open a connection immediately — it uses lazy initialisation. The first actual connection is opened only when the first query is executed.

---

**Q: What is `declarative_base()` and why do models inherit from it?**
> `declarative_base()` creates a Base class that acts as a registry. When a class inherits from Base and defines `__tablename__` and Column attributes, SQLAlchemy registers the class-to-table mapping. `Base.metadata.create_all(engine)` uses this registry to create all tables in the database.

---

**Q: What are the 4 object states in SQLAlchemy?**
> Transient — object created, not in session, no DB row. Pending — added to session with `session.add()`, not yet committed. Persistent — committed, has a DB row, all changes tracked automatically. Detached — session closed, object retains data but ORM no longer tracks it.

---

**Q: What is the difference between `session.commit()` and `session.flush()`?**
> `flush()` sends SQL to the DB within the current open transaction — changes are not permanent and other connections cannot see them. Useful when you need a DB-generated id before finishing the transaction. `commit()` closes the transaction — changes are permanent and visible to all connections.

---

**Q: What is the difference between `filter()` and `filter_by()`?**
> `filter_by()` takes keyword arguments and supports equality checks only — clean for simple lookups. `filter()` takes SQLAlchemy column expressions and supports all operators: `>=`, `like`, `in_`, `or_`, `and_`. For anything beyond a simple equality check, use `filter()`.

---

**Q: What is the N+1 problem and how do you fix it?**
> N+1 occurs when you fetch N parent records and then ORM fires one additional query per record to load related data — 100 users = 101 queries. Fix it with eager loading using `joinedload()`, which fetches all related data in a single LEFT JOIN query. Always use eager loading when you know you'll access related data.

---

**Q: What is the difference between ForeignKey and relationship()?**
> ForeignKey is a column-level database constraint — it creates an actual column (e.g. `user_id`) and enforces referential integrity at the DB level. `relationship()` is a Python-level convenience that lets you navigate between objects without writing JOINs. You need both: ForeignKey for the DB link, relationship() for Python navigation.

---

**Q: What is `back_populates`?**
> It creates a bidirectional relationship — both sides know about each other. Setting `order.user = raj` automatically adds the order to `raj.orders`. Both sides of the relationship stay in sync automatically without any extra code.

---

**Q: What is the Unit of Work pattern?**
> ORM collects all changes made to objects within a session — inserts, updates, deletes — and flushes them to the DB in a single optimised batch on commit. Rather than hitting the DB on every individual change, it batches them together. This minimises round trips, keeps changes atomic, and generates optimised SQL.

---

**Q: What is the Identity Map?**
> A cache inside the session that maps each DB row by primary key to exactly one Python object. Querying the same row twice in one session returns the same Python object from the map — no duplicate DB call, no inconsistent state within the session.

---

**Q: What is connection pooling and why does it matter?**
> Opening a new DB connection for every request is expensive. The connection pool maintains a set of open, reusable connections. `create_engine()` creates a pool automatically. This is why the Engine should be created once and reused — the pool only works across the same Engine instance.

---

**Q: When would you NOT use ORM and write raw SQL instead?**
> For complex analytical queries with multiple aggregations, window functions, or CTEs that ORM cannot express cleanly. For bulk operations on millions of rows where ORM's row-by-row object tracking is too slow. For performance-critical paths where direct control over the query plan is needed.

---

**Q: How does SQLAlchemy provide database independence?**
> The dialect system translates Python queries to the correct SQL syntax for whichever database is connected. Switching from SQLite to PostgreSQL requires only changing the connection string in `create_engine()` — no query code changes needed anywhere in the application.

---

## 23. The Golden Rules — Never Forget

```
1.  Engine      → created ONCE, shared everywhere (connection pool)
2.  Base        → created ONCE, all models inherit from it
3.  Session     → created PER REQUEST, never shared between requests
4.  commit()    → permanent · flush() → temporary within transaction
5.  filter()    → expressions · filter_by() → equality only
6.  ForeignKey  → DB level · relationship() → Python level (need both)
7.  Lazy load   → default, causes N+1 · Eager load → use for known relations
8.  rollback()  → always call in except block
9.  default=fn  → no parentheses (pass function reference, not result)
10. ORM         → Python classes + state tracking + auto SQL + transactions
```

---

*Module 5 · Topics 3 & 4 · ORM Concepts & SQLAlchemy*
