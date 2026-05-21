# Module 5 — NoSQL, MongoDB & PyMongo
### Quick Revision Notes · Interview Prep

---

## 1. Why Database Integration?

- Python stores data in **RAM** — lost when program exits
- Database integration = Python program can **persist, retrieve, and manipulate** data permanently
- Two bridges covered in this module:
  - **PyMongo** → connects Python to MongoDB (NoSQL)
  - **SQLAlchemy** → connects Python to SQL databases (Relational)

---

## 2. Why NoSQL Was Invented

SQL dominated until ~2005. Then the internet exploded:

| Era | Problem |
|---|---|
| 1990s–2005 | SQL worked fine — thousands of users, fixed data |
| 2005–2010 | Millions of users, varying data, need many servers |
| 2010+ | SQL hit a wall — rigid schema, can't scale horizontally |

**3 core problems SQL couldn't solve at web scale:**
1. **Rigid schema** — data shape kept changing
2. **Horizontal scaling** — can't split SQL across many servers easily
3. **Speed at scale** — JOINs on billions of rows become slow

**Result:** NoSQL was invented. Google (Bigtable 2006), Amazon (Dynamo 2007), MongoDB (2009).

---

## 3. The 4 Types of NoSQL Databases

| Type | How it stores data | Best for | Examples |
|---|---|---|---|
| **Document** | JSON-like documents | User profiles, catalogs, CMS | **MongoDB** |
| **Key-Value** | Simple key → value pairs | Sessions, caching, leaderboards | Redis, DynamoDB |
| **Column-Family** | Grouped columns per row key | IoT, time-series, logs | Cassandra, HBase |
| **Graph** | Nodes + relationships | Social networks, fraud detection | Neo4j, Neptune |

> **Module 5 focuses on Document stores → MongoDB**

---

## 4. SQL vs NoSQL — Core Differences

| Aspect | SQL (Relational) | NoSQL (MongoDB) |
|---|---|---|
| Data structure | Tables with rows & columns | Collections of documents (JSON) |
| Schema | **Rigid / fixed** — ALTER TABLE is painful | **Flexible** — add fields anytime |
| Scaling | **Vertical** — bigger server | **Horizontal** — more servers (sharding) |
| Relationships | Strong — JOINs, foreign keys | Weak — embed or reference manually |
| Transactions | Full ACID by default | BASE by default (ACID since v4.0) |
| Query language | SQL | MongoDB Query Language (MQL) |

> **Neither is universally better — the right choice depends on your data shape and access patterns.**

---

## 5. SQL ↔ MongoDB Vocabulary Map

| SQL Term | MongoDB Equivalent |
|---|---|
| Database | Database |
| Table | Collection |
| Row | Document |
| Column | Field |
| Primary Key | `_id` (auto-generated ObjectId) |
| INDEX | Index |
| JOIN | `$lookup` / embedding |

---

## 6. When to Choose MongoDB vs SQL

### Choose MongoDB when:
- Data shape **varies per record** (product catalog: phone ≠ book)
- Need to **scale to millions of writes/sec** (logging, IoT, analytics)
- Data is **hierarchical/nested** (blog post with embedded comments)
- Schema will **evolve rapidly** (early-stage startup)
- Building **real-time apps** (chat, notifications, live feeds)

### Choose SQL when:
- Data has **clear, stable relationships** (orders → users → addresses)
- Need **ACID transactions** (banking, payments — money must not be lost)
- Data is **structured and stable** (HR, accounting systems)
- Need **complex multi-table queries** (BI dashboards, reporting)

### Real companies using MongoDB:
- **Forbes** — content management (articles have varying fields)
- **eBay** — product catalog (each category has unique attributes)
- **Uber** — real-time location updates
- **Myntra/Flipkart** — product listings with varying attributes

---

## 7. The `_id` Field

- Every MongoDB document **automatically gets an `_id` field**
- Type: `ObjectId` — a 12-byte value encoding:
  - **4 bytes** — timestamp
  - **5 bytes** — machine identifier
  - **3 bytes** — counter
- Because `_id` encodes timestamp → **sort by `_id` = sort by insertion order**
- You can provide a custom `_id` (e.g. product SKU, country code) but duplicate `_id` raises `DuplicateKeyError`

---

## 8. CAP Theorem

Every distributed database can guarantee only **2 of 3**:

| Property | Meaning |
|---|---|
| **C**onsistency | Every read gets the latest write |
| **A**vailability | System always responds |
| **P**artition tolerance | Works despite network splits |

| Database | Type | Trade-off |
|---|---|---|
| MongoDB (default) | **AP** | Available + Partition-tolerant; may serve slightly stale reads |
| PostgreSQL | **CP** | Consistent + Partition-tolerant; may refuse requests during partition |
| Traditional SQL (single node) | **CA** | No partition tolerance |

> MongoDB's consistency can be **tuned** using read/write concerns to behave more like CP when needed.

---

## 9. ACID vs BASE

| ACID (SQL default) | BASE (MongoDB default) |
|---|---|
| **A**tomicity — all or nothing | **B**asically available |
| **C**onsistency — always valid state | **S**oft state — temporarily inconsistent |
| **I**solation — transactions don't interfere | **E**ventually consistent — syncs over time |
| **D**urability — committed data survives crashes | Trades strict consistency for speed & scale |

> **MongoDB 4.0+** supports multi-document ACID transactions — the line has significantly blurred.

---

## 10. BSON — What PyMongo Actually Sends

- BSON = **Binary JSON**
- How MongoDB stores and transfers data internally
- Supports more types than JSON: `ObjectId`, `Date`, `Binary`, `Decimal128`, `Int32/64`
- PyMongo handles **Python dict ↔ BSON** conversion entirely — you never touch BSON directly

---

## 11. PyMongo — The Mental Model

```
Your Python dict  →  PyMongo serialises to BSON  →  MongoDB executes it
     (you)                   (bridge)                      (DB)
```

- PyMongo is a **driver** — it has no logic of its own
- It manages: TCP connection pool, BSON serialisation, reconnects, error mapping
- Default port: **27017**
- `MongoClient` is **expensive** to create — create **once** at module level, reuse everywhere
- Databases and collections are created **lazily** — only exist after first write

---

## 12. Object Hierarchy in PyMongo

```
MongoClient  →  Database  →  Collection  →  Document
   (TCP conn)    (db name)    (like table)   (like row)
```

---

## 13. Indexes — Critical Concept

**Without index:** Full collection scan — O(n) — reads every document  
**With index:** B-tree lookup — O(log n) — jumps directly to matching documents

| Index Type | Use case |
|---|---|
| Single field | Speed up queries on one field |
| Unique index | Prevent duplicate values (like UNIQUE in SQL) |
| Compound index | Filter by multiple fields — leftmost prefix rule applies |
| Text index | Full-text search across string fields |
| TTL index | Auto-delete documents after N seconds (sessions, OTPs) |

> Use `.explain()` to check if a query uses **IXSCAN** (index) or **COLLSCAN** (full scan).  
> COLLSCAN on a large collection = you need an index.

---

## 14. Aggregation Pipeline

A sequence of **stages** that transform documents — MongoDB's equivalent of SQL's `GROUP BY`, `HAVING`, `JOIN`.

```
Collection → $match → $group → $sort → $project → Result
```

| Stage | SQL equivalent | What it does |
|---|---|---|
| `$match` | `WHERE` | Filter documents |
| `$group` | `GROUP BY` | Aggregate by a field |
| `$sort` | `ORDER BY` | Sort results |
| `$project` | `SELECT cols` | Reshape/rename fields |
| `$limit` | `LIMIT` | Return N documents |
| `$skip` | `OFFSET` | Skip N documents |
| `$lookup` | `JOIN` | Join with another collection |
| `$unwind` | — | Deconstruct array into separate documents |

> **Always `$match` as early as possible** in the pipeline to reduce the data each subsequent stage processes.

---

## 15. Embedding vs Referencing

| Strategy | When to use | Example |
|---|---|---|
| **Embedding** (nest data inside document) | Data always accessed together, doesn't grow unboundedly | User document contains addresses array |
| **Referencing** (store ObjectId pointer) | Data is shared across documents, or grows very large | Order stores `user_id` pointing to users collection |

---

## 16. PyMongo-Specific Interview Points

These are the **only** things specific to PyMongo (not MongoDB concepts):

| Topic | Key point |
|---|---|
| `find()` return type | Returns a **Cursor** — lazy iterator, not a list. DB query runs only when iterated. |
| `insert_one()` side effect | **Mutates your original dict** — adds `_id` key to it |
| `MongoClient` creation | Create **once** at module level — connection pooling, expensive to create per request |
| Exception types | `DuplicateKeyError`, `ConnectionFailure`, `OperationFailure`, `ServerSelectionTimeoutError` |
| Transactions | Use `client.start_session()` + `session.start_transaction()` context manager |
| Bulk operations | `bulk_write([InsertOne, UpdateOne, DeleteOne])` — one network round-trip instead of many |

---

## 17. Interview Questions & Ideal Answers

**Q: What is MongoDB?**
> Document-oriented NoSQL database storing BSON documents. Offers flexible schemas, horizontal scalability via sharding, and high performance for read/write-heavy workloads.

**Q: What is NoSQL? Name the 4 types.**
> NoSQL = databases that don't use traditional table-row-column structure. Types: Document (MongoDB), Key-Value (Redis), Column-Family (Cassandra), Graph (Neo4j).

**Q: When would you choose MongoDB over PostgreSQL?**
> When data shape varies per record, schema evolves rapidly, you need horizontal scaling, or data is deeply nested. Choose PostgreSQL when you need strict ACID transactions, complex JOINs, or stable relational data.

**Q: What is the difference between embedding and referencing?**
> Embedding nests related data inside one document — best when data is always accessed together and doesn't grow large. Referencing stores an ObjectId pointer — best when data is shared across documents or grows unboundedly.

**Q: What is a Cursor in PyMongo?**
> `find()` returns a Cursor — a lazy iterator. The actual DB query runs only when you iterate it. This saves memory by not loading all documents at once.

**Q: Why must you always use `$set` in `update_one()`?**
> Without `$set`, MongoDB replaces the **entire document** (except `_id`), destroying all other fields. `$set` updates only the specified fields, leaving the rest untouched.

**Q: What does `find({"skills": "Python"})` do when skills is an array?**
> MongoDB automatically checks if "Python" exists **anywhere inside** the skills array. Array field queries work element-wise by default.

**Q: What is `upsert=True` and when would you use it?**
> If the filter matches → update the document. If no match → insert a new document. Used when syncing external data where you don't know if a record already exists. Avoids a separate find-then-insert round trip.

**Q: What is a TTL index?**
> A special index on a datetime field that auto-deletes documents after N seconds. Used for sessions, OTPs, temporary tokens — no manual cleanup needed.

**Q: What is COLLSCAN vs IXSCAN?**
> COLLSCAN = full collection scan, reads every document — O(n), slow on large collections. IXSCAN = index scan, uses B-tree to jump directly — O(log n), fast. Check with `.explain()`.

**Q: What is CAP theorem and where does MongoDB sit?**
> CAP states a distributed system can guarantee only 2 of: Consistency, Availability, Partition tolerance. MongoDB is **AP** by default — stays available during network partitions, possibly serving slightly stale reads. Tunable via read/write concerns.

**Q: Does MongoDB support transactions?**
> Yes, since **version 4.0** — multi-document ACID transactions using sessions. Before 4.0, only single-document operations were atomic.

**Q: What is BSON?**
> Binary JSON — the wire format MongoDB uses internally. PyMongo automatically converts Python dicts to BSON and back. Supports richer types than JSON: ObjectId, Date, Binary, Int32/64, Decimal128.

**Q: What is the difference between `delete_many({})` and `drop()`?**
> `delete_many({})` removes all documents but keeps the collection structure and indexes intact. `drop()` removes everything — the collection, all documents, and all indexes. `drop()` is faster but destructive.

**Q: Why should `MongoClient` be created only once?**
> Creating a `MongoClient` establishes a **connection pool** — multiple TCP connections to MongoDB. Creating it on every request wastes resources and adds latency. Create once at module level, import and reuse everywhere.

---

## 18. Key Things to Never Forget

- `find()` → **Cursor** (lazy) · `find_one()` → **dict or None**
- Always use **`$set`** in updates unless you want to replace the whole document
- `insert_one()` **mutates** your original dict (adds `_id`)
- Databases & collections created **lazily** — no setup commands needed
- MongoDB uses **BSON**, not JSON — PyMongo handles the conversion
- **Index early** on fields you query often — check with `.explain()`
- **`$match` first** in aggregation pipelines to reduce data volume early
- PyMongo questions = Python syntax · MongoDB questions = DB concepts · There is no "PyMongo theory"

---

*Module 5 · Topics 1 & 2 · NoSQL, MongoDB, PyMongo*
