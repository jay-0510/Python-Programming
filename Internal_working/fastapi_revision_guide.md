# FastAPI — Complete Revision Guide

> **Same format as ORM & Auth guides.** Every topic: *what it is → how it works under the hood → simple code with real-world flow.* Not production-ready — built to understand the concept clearly.

---

## 📖 Index

| # | Topic |
|---|---|
| [01](#01-what-is-an-api) | What is an API? |
| [02](#02-rest-architecture) | REST Architecture & Principles |
| [03](#03-http-status-codes--headers) | HTTP Status Codes & Headers |
| [04](#04-fastapi-introduction--setup) | FastAPI Introduction & Setup |
| [05](#05-uvicorn--asgi) | Uvicorn & ASGI |
| [06](#06-pydantic) | Pydantic — Validation & Schemas |
| [07](#07-path--query-parameters) | Path & Query Parameters |
| [08](#08-crud-endpoints) | CRUD Endpoints |
| [09](#09-orm-with-fastapi) | ORM with FastAPI (SQLAlchemy) |
| [10](#10-authentication--jwt) | Authentication & JWT |
| [11](#11-middleware) | Middleware |
| [12](#12-cors) | CORS |
| [13](#13-streaming-responses) | Streaming Responses (SSE for LLMs) |
| [14](#14-error-handling) | Error Handling |
| [15](#15-testing-apis) | Testing APIs |

---

# 01. What is an API?

## Theory

An API (Application Programming Interface) is a **contract** — a defined set of rules for how two systems talk to each other. One side says "send me data in this shape, I'll respond in that shape." The other side follows the contract without knowing what happens internally.

Think of a restaurant: you (the client) look at a menu (the API contract), tell the waiter what you want (the request), and food comes back (the response). You have no idea what happens in the kitchen.

In the ML/AI world, every model you train eventually becomes useless unless something can call it. A FastAPI service wraps your model and exposes it — your React frontend, a mobile app, another microservice, or a data pipeline can all call the same endpoint to get predictions.

**The two sides of every API call:**

```
Client                          Server
  │                               │
  │── POST /predict ─────────────►│
  │   Headers: Content-Type: json │
  │   Body: {"text": "hello"}     │
  │                               │ (your code runs here)
  │◄─ 200 OK ─────────────────────│
  │   Body: {"label": "positive"} │
```

**Key terms:**
- **Endpoint** — a specific URL that does one thing: `POST /predict`, `GET /users/5`
- **Request** — what the client sends: method + URL + headers + body
- **Response** — what the server sends back: status code + headers + body
- **Payload** — the actual data inside the body (usually JSON)

---

# 02. REST Architecture

## Theory

REST (Representational State Transfer) is a set of conventions for designing APIs. It is not a protocol or a standard — it's an **architectural style**. Most APIs you'll interact with follow REST conventions because they make APIs predictable and easy to use.

**The 5 constraints that make something RESTful:**

**1. Stateless** — Every request must contain everything the server needs to process it. The server remembers nothing between requests. No session stored on the server. This is why JWTs exist — the token carries the user's identity in every request itself.

**2. Client-Server** — The UI and the data storage are separated. The client doesn't know how the DB works. The server doesn't know what framework the client uses.

**3. Uniform Interface** — Resources are identified by URLs. You manipulate resources through HTTP methods. The same URL for a resource, different method for different actions.

**4. Cacheable** — Responses should indicate if they can be cached. GET responses are typically cacheable. POST/PUT/DELETE are not.

**5. Layered System** — The client doesn't need to know if it's talking directly to the server or through a load balancer, cache, or gateway.

**REST URL conventions:**

```
Resource: users

GET    /users          → list all users
POST   /users          → create a new user
GET    /users/5        → get user with id 5
PUT    /users/5        → replace user 5 entirely
PATCH  /users/5        → update some fields of user 5
DELETE /users/5        → delete user 5

Nested resource:
GET    /users/5/orders      → all orders for user 5
GET    /users/5/orders/12   → order 12 belonging to user 5

❌ Never do:
GET  /getUser?id=5          → method in URL (not RESTful)
POST /users/deleteUser/5    → action in URL
```

**HTTP methods and what they mean:**

| Method | Safe? | Idempotent? | Use |
|--------|-------|-------------|-----|
| GET | Yes | Yes | Read only — never changes data |
| POST | No | No | Create a new resource |
| PUT | No | Yes | Replace a resource completely |
| PATCH | No | No | Partial update |
| DELETE | No | Yes | Delete a resource |

Idempotent = calling it 10 times has the same effect as calling it once.

---

# 03. HTTP Status Codes & Headers

## Theory — Status Codes

Status codes are a 3-digit number the server sends back. The first digit tells you the category:

```
1xx — Informational  (rare in APIs)
2xx — Success        (request worked)
3xx — Redirect       (go somewhere else)
4xx — Client Error   (you sent something wrong)
5xx — Server Error   (server broke)
```

**The ones you must know:**

```
200 OK              → GET/PUT/PATCH succeeded, response body has data
201 Created         → POST succeeded, new resource was created
204 No Content      → DELETE succeeded, nothing to return in body

400 Bad Request     → validation failed (missing field, wrong type)
401 Unauthorized    → not authenticated (no token or bad token)
403 Forbidden       → authenticated but not allowed (wrong role)
404 Not Found       → resource doesn't exist
409 Conflict        → duplicate — email already registered
422 Unprocessable   → FastAPI's default for Pydantic validation errors

500 Internal Error  → something crashed on the server
503 Service Unavail → server overloaded or down
```

**401 vs 403 — the most confused pair:**
- 401: "I don't know who you are" — no token, expired token
- 403: "I know who you are, but you're not allowed" — wrong role, no permission

## Theory — Headers

Headers are key-value pairs sent with every request and response. They carry metadata, not the actual data.

```
Common Request Headers:
  Content-Type: application/json     → "my body is JSON"
  Authorization: Bearer eyJhbG...   → "here's my token"
  Accept: application/json           → "I want JSON back"
  X-Request-ID: abc123               → custom tracking header

Common Response Headers:
  Content-Type: application/json     → "my response body is JSON"
  X-Process-Time: 0.023              → how long it took
  Access-Control-Allow-Origin: *    → CORS permission
  Cache-Control: max-age=3600        → cache this for 1 hour
```

**Reading headers in FastAPI:**

```python
from fastapi import FastAPI, Request, Header
from typing import Annotated

app = FastAPI()

# Read any header directly
@app.get("/info")
def get_info(user_agent: Annotated[str | None, Header()] = None):
    return {"user_agent": user_agent}

# Read from raw request object
@app.get("/debug")
def debug(request: Request):
    return {
        "method":      request.method,
        "url":         str(request.url),
        "headers":     dict(request.headers),
        "client_ip":   request.client.host,
    }
```

---

# 04. FastAPI Introduction & Setup

## Theory

FastAPI is a Python web framework for building APIs. Three things make it different from Flask or Django REST Framework:

**1. Async-first** — built on ASGI (not WSGI), so it handles thousands of concurrent requests without blocking. Crucial for I/O-heavy ML inference endpoints that call external services.

**2. Automatic validation** — you declare the shape of data using Python type hints + Pydantic. FastAPI validates every request automatically and returns a 422 error with details if it fails.

**3. Auto-generated docs** — FastAPI reads your type hints and generates interactive Swagger UI at `/docs` and ReDoc at `/redoc`. Zero extra work.

**How FastAPI processes a request:**

```
HTTP Request arrives
       │
       ▼
Uvicorn (ASGI server) receives bytes → parses HTTP
       │
       ▼
FastAPI Router matches URL + method → finds your function
       │
       ▼
Dependency Injection runs (get_db, get_current_user, etc.)
       │
       ▼
Pydantic validates request body/params
       │
       ▼
Your function runs
       │
       ▼
Pydantic serializes response using response_model
       │
       ▼
FastAPI sends HTTP response back
```

## Setup

```bash
pip install fastapi uvicorn[standard] sqlalchemy pydantic[email]

# Project structure
myapi/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── auth.py
└── .env
```

## Simplest possible app

```python
# main.py
from fastapi import FastAPI

app = FastAPI(
    title="My API",
    description="Learning FastAPI",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}
```

```bash
uvicorn main:app --reload
# Open: http://localhost:8000/docs
```

**What `@app.get("/")` does:** It registers a route — "when someone sends a GET request to `/`, call this function and return its result as JSON." FastAPI automatically serializes the returned dict to JSON and sets `Content-Type: application/json`.

---

# 05. Uvicorn & ASGI

## Theory

**WSGI vs ASGI — why it matters:**

Old Python web frameworks (Flask, Django) use WSGI (Web Server Gateway Interface). WSGI is **synchronous** — one request at a time per worker. To handle 100 concurrent requests, you need 100 workers.

FastAPI uses ASGI (Asynchronous Server Gateway Interface). ASGI is **async** — one worker can handle many requests concurrently by switching between them while waiting for I/O. For an ML inference endpoint that calls a model + a database + an external API, async lets one worker handle hundreds of concurrent requests.

**Uvicorn** is the ASGI server that runs your FastAPI app. It receives raw HTTP bytes, parses them, and hands them to FastAPI. Think of it as the engine — FastAPI is the car.

```
Client → Uvicorn → FastAPI application → your code
           (parses HTTP)  (routes + validation)
```

**How async actually works in FastAPI:**

```python
import asyncio
from fastapi import FastAPI

app = FastAPI()

# ASYNC endpoint — can handle other requests while awaiting
@app.get("/async-example")
async def async_endpoint():
    await asyncio.sleep(1)   # yields control — other requests run during this wait
    return {"waited": "1 second"}

# SYNC endpoint — FastAPI runs this in a threadpool automatically
# so it doesn't block the event loop
@app.get("/sync-example")
def sync_endpoint():
    import time
    time.sleep(1)    # FastAPI runs sync functions in threadpool — safe
    return {"waited": "1 second"}
```

**Rule of thumb:** Use `async def` when your function calls `await` something (async DB, aiohttp, etc.). Use `def` for CPU-heavy work or when using sync libraries (requests, psycopg2). FastAPI handles both correctly.

**Running Uvicorn:**

```bash
# Development
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production (multiple workers for CPU-bound)
uvicorn main:app --workers 4 --host 0.0.0.0 --port 8000

# With Gunicorn (process manager) + Uvicorn workers
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

---

# 06. Pydantic

## Theory

Pydantic is a Python library for data validation using type hints. You define a class, Pydantic enforces the types and constraints at runtime.

**How it works internally:** When you define `class UserCreate(BaseModel)`, Pydantic inspects all the type-annotated fields at class creation time. When you do `UserCreate(**data)`, Pydantic runs validators for each field, coerces types where possible (string `"22"` → int `22`), and raises `ValidationError` if anything fails — all before your function body runs.

**The separation pattern (most important concept):**

```
UserCreate  → what client sends (no id, no timestamps)
UserOut     → what API returns (has id, timestamps, no password)
UserInDB    → what you store (has hashed_password — never returned)
```

This prevents clients from setting fields they shouldn't (like `id`) and prevents secrets from leaking in responses (like `hashed_password`).

## Schema definitions

```python
# schemas.py
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from typing import Annotated
from datetime import datetime

# ── Request schemas (what client sends) ───────────────────────────

class UserCreate(BaseModel):
    name:     str = Field(min_length=2, max_length=50)
    email:    EmailStr                              # validates format
    age:      int = Field(ge=0, le=120)            # 0 ≤ age ≤ 120
    password: str = Field(min_length=8)

class UserUpdate(BaseModel):
    name:  str | None = Field(default=None, min_length=2)
    email: EmailStr | None = None
    # all optional — client can update just one field

class PostCreate(BaseModel):
    title:   str = Field(min_length=3, max_length=200)
    content: str
    tags:    list[str] = []                        # default empty list

# ── Response schemas (what API returns) ───────────────────────────

class UserOut(BaseModel):
    id:         int
    name:       str
    email:      EmailStr
    created_at: datetime

    model_config = {"from_attributes": True}   # read from SQLAlchemy models

class PostOut(BaseModel):
    id:      int
    title:   str
    content: str
    tags:    list[str]
    author:  UserOut                           # nested schema

    model_config = {"from_attributes": True}
```

## Field validator — business logic in schema

```python
class ProductCreate(BaseModel):
    name:          str
    price:         float
    discount_pct:  float = 0.0

    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Price must be greater than 0")
        return round(v, 2)   # normalize to 2 decimal places

    @field_validator("name")
    @classmethod
    def name_strip(cls, v):
        return v.strip().title()   # normalize: "  laptop   " → "Laptop"

    # model_validator: validate across multiple fields
    @model_validator(mode="after")
    def discount_cannot_exceed_price(self):
        if self.discount_pct >= 100:
            raise ValueError("Discount cannot be 100% or more")
        return self
```

## Annotated — reusable field definitions

```python
from typing import Annotated

# Define once, reuse everywhere
PositiveFloat = Annotated[float, Field(gt=0)]
ShortStr      = Annotated[str,   Field(min_length=1, max_length=100)]
EmailField    = Annotated[EmailStr, Field(description="User email address")]

class ItemCreate(BaseModel):
    name:  ShortStr
    price: PositiveFloat
    email: EmailField
```

## Using schemas in endpoints

```python
from fastapi import FastAPI
from schemas import UserCreate, UserOut

app = FastAPI()

@app.post(
    "/users",
    response_model=UserOut,        # filters response — only UserOut fields returned
    status_code=201,               # HTTP 201 Created
    summary="Create a new user",   # shows in /docs
)
def create_user(payload: UserCreate):   # FastAPI validates body against UserCreate
    # payload is a validated UserCreate instance
    # If validation fails → 422 returned automatically, your code never runs
    user = save_to_db(payload)
    return user   # FastAPI serializes through UserOut — password field stripped
```

---

# 07. Path & Query Parameters

## Theory

**Path parameters** are part of the URL itself — they identify a specific resource: `/users/5`, `/products/laptop-pro`. They are required by definition.

**Query parameters** come after `?` in the URL — they filter, sort, or paginate: `/users?role=admin&page=2`. They are optional by convention and have defaults.

FastAPI reads your function signature to know which is which: anything matching a `{placeholder}` in the path is a path param; everything else with a simple type is a query param.

```python
from fastapi import FastAPI, Path, Query
from typing import Annotated

app = FastAPI()

# ── Path parameters ────────────────────────────────────────────────

@app.get("/users/{user_id}")
def get_user(user_id: int):         # FastAPI converts string → int automatically
    return {"user_id": user_id}     # if not convertible → 422 validation error

# With constraints
@app.get("/products/{product_id}")
def get_product(
    product_id: Annotated[int, Path(ge=1, description="Product ID, must be >= 1")]
):
    return {"product_id": product_id}

# Multiple path params
@app.get("/users/{user_id}/orders/{order_id}")
def get_order(user_id: int, order_id: int):
    return {"user_id": user_id, "order_id": order_id}


# ── Query parameters ───────────────────────────────────────────────

@app.get("/users")
def list_users(
    role:      str | None = None,          # optional filter
    is_active: bool       = True,          # default True
    page:      int        = Query(1, ge=1),          # page >= 1
    page_size: int        = Query(20, ge=1, le=100), # 1 ≤ page_size ≤ 100
):
    # GET /users                        → role=None, is_active=True, page=1
    # GET /users?role=admin&page=2      → role="admin", page=2
    # GET /users?is_active=false        → is_active=False (auto-converted)
    return {
        "role": role,
        "is_active": is_active,
        "page": page,
        "page_size": page_size
    }


# ── Both together — real world: blog posts ─────────────────────────

@app.get("/blogs/{blog_id}/posts")
def get_blog_posts(
    blog_id:  int,
    tag:      str | None = None,     # filter by tag
    sort:     str        = "newest", # newest | oldest
    page:     int        = 1,
):
    # GET /blogs/3/posts?tag=python&sort=oldest&page=2
    return {
        "blog_id":  blog_id,
        "tag":      tag,
        "sort":     sort,
        "page":     page,
    }
```

---

# 08. CRUD Endpoints

## Theory

CRUD stands for Create, Read, Update, Delete — the four operations every persistent resource needs. In REST, these map cleanly to HTTP methods and status codes.

The pattern for every CRUD endpoint is the same:
1. Validate input (Pydantic does this automatically)
2. Do the work (DB query, business logic)
3. Return the right status code with the right response shape

## Real-world example: Blog API

```python
# main.py — a simple blog with posts
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="Blog API")

# Fake in-memory DB (replace with SQLAlchemy in real app)
posts_db: dict[int, dict] = {}
next_id = 1

# ── Schemas ────────────────────────────────────────────────────────

class PostCreate(BaseModel):
    title:   str
    content: str
    tags:    list[str] = []

class PostOut(BaseModel):
    id:         int
    title:      str
    content:    str
    tags:       list[str]
    created_at: datetime

class PostUpdate(BaseModel):
    title:   str | None = None
    content: str | None = None


# ── CREATE ─────────────────────────────────────────────────────────

@app.post("/posts", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(payload: PostCreate):
    global next_id
    post = {
        "id":         next_id,
        "title":      payload.title,
        "content":    payload.content,
        "tags":       payload.tags,
        "created_at": datetime.now(),
    }
    posts_db[next_id] = post
    next_id += 1
    return post


# ── READ ALL ───────────────────────────────────────────────────────

@app.get("/posts", response_model=list[PostOut])
def list_posts(tag: str | None = None):
    posts = list(posts_db.values())
    if tag:
        posts = [p for p in posts if tag in p["tags"]]
    return posts


# ── READ ONE ───────────────────────────────────────────────────────

@app.get("/posts/{post_id}", response_model=PostOut)
def get_post(post_id: int):
    post = posts_db.get(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {post_id} not found"
        )
    return post


# ── UPDATE ─────────────────────────────────────────────────────────

@app.patch("/posts/{post_id}", response_model=PostOut)
def update_post(post_id: int, payload: PostUpdate):
    post = posts_db.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Only update fields that were actually sent
    if payload.title is not None:
        post["title"] = payload.title
    if payload.content is not None:
        post["content"] = payload.content

    return post


# ── DELETE ─────────────────────────────────────────────────────────

@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    if post_id not in posts_db:
        raise HTTPException(status_code=404, detail="Post not found")
    del posts_db[post_id]
    # 204 = no body returned
```

---

# 09. ORM with FastAPI

## Theory

SQLAlchemy ORM sits between FastAPI and the database. FastAPI handles HTTP. Pydantic handles validation. SQLAlchemy handles DB operations. Each has one job.

The critical piece connecting them is the **`get_db` dependency** — a generator that creates a DB session for each request and closes it after the response is sent, returning the connection to the pool.

**The three-schema pattern with SQLAlchemy:**

```
SQLAlchemy Model (models.py)     → the actual DB table
Pydantic Create Schema           → what client POSTs
Pydantic Response Schema         → what API returns
```

These are three separate things. The SQLAlchemy model has columns for `hashed_password`, `created_at` auto-timestamps, etc. The Create schema has `password` (plain). The Response schema has neither.

## Full example: User + Post system

```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./blog.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db          # FastAPI injects this into the route function
    finally:
        db.close()        # always runs — connection returned to pool
```

```python
# models.py
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id:         Mapped[int]      = mapped_column(primary_key=True)
    name:       Mapped[str]      = mapped_column(String(100))
    email:      Mapped[str]      = mapped_column(String(255), unique=True)
    is_active:  Mapped[bool]     = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    posts: Mapped[list["Post"]] = relationship(back_populates="author")

class Post(Base):
    __tablename__ = "posts"

    id:         Mapped[int]      = mapped_column(primary_key=True)
    user_id:    Mapped[int]      = mapped_column(ForeignKey("users.id"))
    title:      Mapped[str]      = mapped_column(String(200))
    content:    Mapped[str]      = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    author: Mapped["User"] = relationship(back_populates="posts")
```

```python
# schemas.py
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    name:  str
    email: EmailStr

class UserOut(BaseModel):
    id:         int
    name:       str
    email:      str
    created_at: datetime
    model_config = {"from_attributes": True}

class PostCreate(BaseModel):
    title:   str
    content: str

class PostOut(BaseModel):
    id:      int
    title:   str
    content: str
    author:  UserOut
    model_config = {"from_attributes": True}
```

```python
# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import User, Post
from schemas import UserCreate, UserOut, PostCreate, PostOut

Base.metadata.create_all(bind=engine)   # creates tables if not exist
app = FastAPI()

# ── Users ──────────────────────────────────────────────────────────

@app.post("/users", response_model=UserOut, status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    # Check duplicate
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    user = User(name=payload.name, email=payload.email)
    db.add(user)
    db.commit()
    db.refresh(user)   # get DB-generated id and created_at
    return user

@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ── Posts ──────────────────────────────────────────────────────────

@app.post("/users/{user_id}/posts", response_model=PostOut, status_code=201)
def create_post(user_id: int, payload: PostCreate, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    post = Post(user_id=user_id, title=payload.title, content=payload.content)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@app.get("/posts", response_model=list[PostOut])
def list_posts(db: Session = Depends(get_db)):
    return db.query(Post).all()
```

---

# 10. Authentication & JWT

## Theory

This section connects what we covered in the Auth guide to FastAPI's actual implementation.

**The flow in one picture:**

```
1. POST /token   { username, password }
       │
       ▼ (verify password hash)
       │
       ▼ (generate JWT with user id + expiry)
       │
       └──► { access_token: "eyJ..." }

2. GET /me
   Authorization: Bearer eyJ...
       │
       ▼ (oauth2_scheme extracts token from header)
       │
       ▼ (decode JWT, verify signature + expiry)
       │
       ▼ (look up user from "sub" claim)
       │
       └──► { id, name, email }
```

**Dependency chain** — FastAPI calls these in order before your route runs:

```
get_db → oauth2_scheme → get_current_user → get_active_user → your_route
```

If any dependency raises `HTTPException`, the chain stops and the error is returned immediately.

## Full auth implementation

```python
# auth.py
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-in-prod")
ALGORITHM  = "HS256"
EXPIRE_MIN = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=EXPIRE_MIN)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
```

```python
# main.py — auth routes + protected routes
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models import User
from auth import hash_password, verify_password, create_token, decode_token
from schemas import UserCreate, UserOut, Token

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# reads "Authorization: Bearer <token>" header → gives you the raw token string

# ── Dependency: current user from token ───────────────────────────

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db:    Session = Depends(get_db)
) -> User:
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = db.get(User, int(payload["sub"]))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def get_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# ── Register ───────────────────────────────────────────────────────

@app.post("/register", response_model=UserOut, status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=409, detail="Email already registered")
    user = User(
        name=payload.name,
        email=payload.email,
        hashed_password=hash_password(payload.password)
    )
    db.add(user); db.commit(); db.refresh(user)
    return user


# ── Login → issue token ────────────────────────────────────────────

@app.post("/token")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm expects form data: username + password
    user = db.query(User).filter(User.email == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


# ── Protected routes ───────────────────────────────────────────────

@app.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_active_user)):
    return current_user   # FastAPI injects the logged-in user automatically

@app.delete("/me")
def delete_account(current_user: User = Depends(get_active_user), db: Session = Depends(get_db)):
    db.delete(current_user)
    db.commit()
    return {"message": "Account deleted"}
```

---

# 11. Middleware

## Theory

Middleware wraps every request and response globally. Every request passes through middleware before reaching your route, and every response passes through it on the way back.

**Where middleware sits:**

```
Request → [Middleware 1] → [Middleware 2] → Router → Your route
Response ← [Middleware 1] ← [Middleware 2] ← Router ← Your route
```

Middleware is perfect for things that should happen for every request: logging, timing, adding headers, rate limiting, request ID injection.

**The `call_next` pattern:** Middleware in FastAPI/Starlette uses `call_next(request)` — this calls the rest of the application (other middleware + your route) and returns the response. Everything before `call_next` runs on the way in; everything after runs on the way out.

```python
from fastapi import FastAPI, Request
from fastapi.middleware.base import BaseHTTPMiddleware
import time
import uuid

app = FastAPI()

# ── Timing Middleware ──────────────────────────────────────────────

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()

        response = await call_next(request)   # ← runs your route

        duration = time.perf_counter() - start
        response.headers["X-Process-Time"] = f"{duration:.4f}s"
        return response


# ── Request ID Middleware ──────────────────────────────────────────

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id   # attach to request state

        response = await call_next(request)

        response.headers["X-Request-ID"] = request_id
        return response


# ── Logging Middleware ─────────────────────────────────────────────

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print(f"→ {request.method} {request.url.path}")

        response = await call_next(request)

        print(f"← {response.status_code}")
        return response


# Register — ORDER MATTERS: first added = outermost = first to run
app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(TimingMiddleware)

# Request flow:
# TimingMiddleware → RequestIDMiddleware → LoggingMiddleware → Route
```

**Read request ID inside a route:**

```python
@app.get("/items")
def get_items(request: Request):
    req_id = request.state.request_id   # set by middleware
    return {"request_id": req_id}
```

---

# 12. CORS

## Theory

CORS (Cross-Origin Resource Sharing) is a browser security mechanism. When your React app running on `http://localhost:3000` tries to call your API on `http://localhost:8000`, the browser first sends a **preflight** `OPTIONS` request asking: "is this origin allowed?" Your server must reply with the right headers. If it doesn't, the browser blocks the actual request.

This only applies to **browser** clients. Postman, curl, Python scripts — they don't enforce CORS. You'll notice CORS errors only when building a frontend.

**The origin concept:**
```
Origin = scheme + hostname + port

http://localhost:3000    ← one origin
http://localhost:8000    ← different origin (different port)
https://myapp.com        ← different origin (different scheme + domain)
https://api.myapp.com    ← different from https://myapp.com (subdomain!)
```

**What CORS headers do:**

```
Access-Control-Allow-Origin: https://myapp.com   → "this origin is allowed"
Access-Control-Allow-Methods: GET, POST, DELETE  → "these methods are allowed"
Access-Control-Allow-Headers: Authorization      → "these headers are allowed"
Access-Control-Allow-Credentials: true           → "cookies/auth headers allowed"
```

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Development: allow everything
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],              # any origin
    allow_methods=["*"],              # GET, POST, PUT, DELETE, OPTIONS, ...
    allow_headers=["*"],              # any header
)

# Production: be specific
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://myapp.com",
        "https://www.myapp.com",
        "http://localhost:3000",       # local dev frontend
    ],
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
    allow_credentials=True,           # allow cookies + auth headers
    max_age=3600,                     # preflight cache: 1 hour
)

@app.get("/data")
def get_data():
    return {"hello": "from API"}
```

**Typical mistake:** Setting `allow_credentials=True` with `allow_origins=["*"]`. Browsers reject this combination. When using credentials, you must list specific origins.

---

# 13. Streaming Responses

## Theory

Normal API responses: your function runs, produces a result, FastAPI sends the entire response body at once. The client waits for all of it before it can do anything.

Streaming: the server sends chunks of data progressively. The client receives and processes each chunk as it arrives. This is how ChatGPT's token-by-token output works — the model produces one token at a time and the server streams each to the browser immediately.

**Two streaming mechanisms in FastAPI:**

**`StreamingResponse`** — generic chunked HTTP. Good for streaming files, CSV exports, or any chunked data.

**Server-Sent Events (SSE)** — a standardized format for real-time one-way server→client streaming. The browser has a built-in `EventSource` API that reconnects automatically. OpenAI, Anthropic, and Hugging Face all use SSE for streaming completions.

**SSE message format:**

```
data: {"token": "Hello"}\n\n
data: {"token": " world"}\n\n
data: [DONE]\n\n
```

Each event is `data: <content>\n\n` — two newlines mark the end of an event.

## StreamingResponse — file/data streaming

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI()

# Stream a large CSV without loading it all into memory
@app.get("/export/csv")
def export_csv():
    def generate():
        yield "id,name,email\n"                        # header
        for i in range(1, 1001):                       # 1000 rows
            yield f"{i},User{i},user{i}@example.com\n"

    return StreamingResponse(
        generate(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=users.csv"}
    )
```

## SSE — LLM token streaming (most important for AI engineers)

```python
import asyncio
import json
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    prompt: str

# Simulates what OpenAI / any LLM API does under the hood
async def stream_llm_response(prompt: str):
    """Generator that yields SSE-formatted events."""
    # In real code: call openai.chat.completions.create(stream=True)
    # or your local model's streaming API
    fake_tokens = ["The", " answer", " to", " your", " question", " is", " 42", "."]

    for token in fake_tokens:
        # SSE format: "data: <json>\n\n"
        event = json.dumps({"token": token, "done": False})
        yield f"data: {event}\n\n"
        await asyncio.sleep(0.1)   # simulate model latency

    # Final event signaling stream is done
    yield f"data: {json.dumps({'token': '', 'done': True})}\n\n"

@app.post("/chat/stream")
async def chat_stream(payload: ChatRequest):
    return StreamingResponse(
        stream_llm_response(payload.prompt),
        media_type="text/event-stream",     # SSE content type
        headers={
            "Cache-Control":  "no-cache",
            "X-Accel-Buffering": "no",      # disable nginx buffering
        }
    )
```

**Frontend consuming SSE (JavaScript):**

```javascript
// Using EventSource (built into browsers)
const source = new EventSource("/chat/stream");

source.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.done) {
        source.close();
        return;
    }
    document.getElementById("output").textContent += data.token;
};
```

**With real OpenAI API:**

```python
import openai

@app.post("/chat/openai-stream")
async def openai_stream(payload: ChatRequest):
    async def generate():
        client = openai.AsyncOpenAI()
        stream = await client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": payload.prompt}],
            stream=True,
        )
        async for chunk in stream:
            token = chunk.choices[0].delta.content or ""
            yield f"data: {json.dumps({'token': token})}\n\n"
        yield f"data: {json.dumps({'done': True})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
```

---

# 14. Error Handling

## Theory

Errors in FastAPI fall into three categories:

**1. Validation errors (422)** — Pydantic catches these automatically when request body or params don't match the schema. You don't write code for this — it just happens.

**2. HTTP exceptions** — things that go wrong in your business logic: not found, unauthorized, conflict. You raise `HTTPException` with the right status code and detail message.

**3. Unexpected errors (500)** — bugs, crashes, DB timeouts. FastAPI returns a generic 500 by default. You use exception handlers to log these and return useful messages.

**Custom exception handlers** — FastAPI lets you register handlers for specific exception types. When that exception is raised anywhere in your app, the handler runs and returns the response.

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging

app = FastAPI()
logger = logging.getLogger(__name__)


# ── Custom exception classes ───────────────────────────────────────

class AppError(Exception):
    """Base for all app-specific errors."""
    def __init__(self, message: str, status_code: int = 400):
        self.message     = message
        self.status_code = status_code

class NotFoundError(AppError):
    def __init__(self, resource: str, id: int):
        super().__init__(f"{resource} with id {id} not found", status_code=404)

class ConflictError(AppError):
    def __init__(self, message: str):
        super().__init__(message, status_code=409)


# ── Exception handlers ─────────────────────────────────────────────

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message, "path": str(request.url)}
    )

@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    # Customize the default 422 response format
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation failed",
            "details": exc.errors()   # list of field errors with location
        }
    )

@app.exception_handler(Exception)
async def unexpected_error_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error on {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )


# ── Using in routes ────────────────────────────────────────────────

fake_users = {1: {"id": 1, "name": "Arjun"}}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = fake_users.get(user_id)
    if not user:
        raise NotFoundError("User", user_id)   # caught by app_error_handler
    return user

@app.post("/users")
def create_user(name: str, email: str):
    if email in [u.get("email") for u in fake_users.values()]:
        raise ConflictError(f"Email {email} already exists")
    return {"name": name, "email": email}
```

**Response format consistency** — always return errors in the same shape:

```python
# Good — every error response looks the same
{"error": "User not found", "path": "/users/99"}
{"error": "Email already registered"}
{"error": "Validation failed", "details": [...]}

# Bad — inconsistent, hard for clients to handle
"User not found"                    # plain string
{"message": "not found"}            # different key
{"detail": "User not found"}        # FastAPI default (inconsistent with yours)
```

---

# 15. Testing APIs

## Theory

FastAPI's `TestClient` wraps your app and lets you make HTTP requests to it without starting a real server. Under the hood it uses `httpx`. Your tests run instantly — no ports, no sockets, no startup time.

**The testing pattern:**
1. Create a `TestClient` with your app
2. Use `client.get()`, `client.post()` etc. to make requests
3. Assert on `response.status_code` and `response.json()`

**For tests that need a database**, swap the real DB with an in-memory SQLite database using FastAPI's dependency override system — `app.dependency_overrides[get_db] = override_get_db`.

```python
# test_main.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

# ── Test database setup ────────────────────────────────────────────

TEST_DB_URL = "sqlite:///./test.db"   # separate test database

test_engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(bind=test_engine, autocommit=False, autoflush=False)

def override_get_db():
    """Replace the real DB with test DB for every test."""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Override dependency — all routes that Depend(get_db) now get test DB
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def reset_db():
    """Create fresh tables before each test, drop after."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

client = TestClient(app)


# ── Tests ──────────────────────────────────────────────────────────

def test_create_user():
    response = client.post("/users", json={"name": "Arjun", "email": "a@b.com"})
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "a@b.com"
    assert "id" in data
    assert "password" not in data       # must not leak password

def test_get_user_not_found():
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_duplicate_email_returns_409():
    client.post("/users", json={"name": "Arjun", "email": "a@b.com"})
    response = client.post("/users", json={"name": "Other", "email": "a@b.com"})
    assert response.status_code == 409

def test_validation_error():
    response = client.post("/users", json={"name": "A", "email": "not-an-email"})
    assert response.status_code == 422   # Pydantic validation failed

def test_list_posts_empty():
    response = client.get("/posts")
    assert response.status_code == 200
    assert response.json() == []


# ── Auth testing ───────────────────────────────────────────────────

def test_protected_route_without_token():
    response = client.get("/me")
    assert response.status_code == 401

def test_login_and_access_protected_route():
    # Register
    client.post("/register", json={
        "name": "Arjun", "email": "a@b.com", "password": "secret123"
    })

    # Login — form data, not JSON (OAuth2 spec)
    login = client.post("/token", data={"username": "a@b.com", "password": "secret123"})
    assert login.status_code == 200
    token = login.json()["access_token"]

    # Access protected route with token
    response = client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "a@b.com"

def test_wrong_password_returns_401():
    client.post("/register", json={
        "name": "Arjun", "email": "a@b.com", "password": "secret123"
    })
    response = client.post("/token", data={"username": "a@b.com", "password": "wrong"})
    assert response.status_code == 401
```

```bash
# Run tests
pytest test_main.py -v

# With coverage
pytest test_main.py -v --cov=main --cov-report=term-missing

# Run only auth tests
pytest test_main.py -v -k "auth or login or token"
```

---

## Quick Reference — The Full Request Flow

Every request through a production-ready FastAPI app:

```
Browser / Client
    │
    │  POST /chat/stream
    │  Authorization: Bearer eyJ...
    │  Content-Type: application/json
    │  Body: {"prompt": "hello"}
    ▼
Uvicorn (ASGI server)
    │  Parses raw HTTP bytes
    ▼
CORSMiddleware
    │  Checks origin, adds Access-Control headers
    ▼
TimingMiddleware
    │  Records start time
    ▼
LoggingMiddleware
    │  Logs method + path
    ▼
FastAPI Router
    │  Matches POST /chat/stream → chat_stream function
    ▼
Dependency Resolution
    │  get_db() → creates DB session from pool
    │  oauth2_scheme() → extracts Bearer token from header
    │  get_current_user() → decodes JWT, looks up user in DB
    │  get_active_user() → checks user.is_active
    ▼
Pydantic Validation
    │  Validates request body against ChatRequest schema
    │  Returns 422 automatically if invalid
    ▼
chat_stream() runs
    │  Calls LLM, creates StreamingResponse generator
    ▼
StreamingResponse
    │  Sends SSE chunks one by one as LLM produces tokens
    ▼
LoggingMiddleware (response path)
    │  Logs status code
    ▼
TimingMiddleware (response path)
    │  Adds X-Process-Time header
    ▼
CORSMiddleware (response path)
    │  Adds Access-Control headers
    ▼
Client receives streamed tokens progressively
```

---

## Status Codes Cheatsheet

```
GET    /items         200 OK
POST   /items         201 Created
PUT    /items/5       200 OK
PATCH  /items/5       200 OK
DELETE /items/5       204 No Content

Missing resource      404 Not Found
Duplicate resource    409 Conflict
Not authenticated     401 Unauthorized
Authenticated, no perm 403 Forbidden
Bad input (yours)     400 Bad Request
Bad input (Pydantic)  422 Unprocessable
Server crash          500 Internal Server Error
```
