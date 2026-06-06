# Advanced FastAPI — Interview Questions
### OAuth2 · Error Handling · API Performance · async/await
#### Targeted at 2–3 year experience level | Medium difficulty

---

## Section 1: Authentication — OAuth2

---

### Q1. What is OAuth2 and how is it different from basic username/password authentication?

**Answer:**

Basic auth = you hand your password directly to the app. If that app is hacked, your password is exposed.

OAuth2 = you never give your password to the app. Instead, a trusted third party (Google, GitHub) verifies you and gives the app a token saying "yes, this person is who they say they are."

**Real-world analogy:** Basic auth is like giving your house key to a delivery person. OAuth2 is like giving the delivery person a one-time access code that only works for the front door, only today.

```
Basic auth flow:
User → sends email + password → Your app → checks password → logged in

OAuth2 flow:
User → clicks "Login with Google"
     → redirected to Google (never touches your app's password)
     → Google verifies identity
     → Google gives your app a token
     → Your app uses token to know who the user is
```

**Why industry uses OAuth2:** No password storage = no password breaches. You also get access to the user's Google/GitHub profile without extra signup forms.

---

### Q2. What are the four roles in OAuth2 and what does each do?

**Answer:**

OAuth2 defines four actors in every flow:

| Role | Who it is | What it does |
|---|---|---|
| Resource Owner | The user | The person granting permission |
| Client | Your app | The app requesting access |
| Authorization Server | Google/GitHub/Auth0 | Verifies identity and issues tokens |
| Resource Server | The API with user data | Accepts tokens to serve data |

```
Example: "Login with GitHub for our code review app"

Resource Owner     = Developer (you)
Client             = Code review app
Authorization Server = GitHub (login.github.com)
Resource Server    = GitHub API (api.github.com/user)
```

In simple apps, the Authorization Server and Resource Server are the same machine. In enterprise setups (Auth0, Okta), they are separate services.

> **Interview insight:** "What is the difference between the Authorization Server and Resource Server?" This trips people up. Auth Server issues tokens. Resource Server validates tokens to serve data. Google's login page = Auth Server. Google's People API = Resource Server.

---

### Q3. What are OAuth2 scopes and why do they matter?

**Answer:**

Scopes define exactly how much access the app is asking for. They limit the damage if a token is stolen.

```
# Instead of full access, you request only what you need
scope = "read:email"           # only read email
scope = "read:profile"         # only read profile info
scope = "repo"                 # full GitHub repo access
scope = "read:user write:repo" # multiple scopes at once
```

**Real-world analogy:** Scopes are like permissions on a job offer. A delivery driver gets access to the building entrance — not the server room, not the CEO's office.

**In FastAPI with OAuth2:**
```python
from fastapi.security import OAuth2PasswordBearer

# Tells FastAPI: tokens come from /token endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# In your token generation, embed the scope
payload = {
    "user_id": 42,
    "scope": "read:orders write:orders",
    "exp": datetime.utcnow() + timedelta(hours=1)
}
```

> **Interview insight:** "Why not just give full access with every token?" Principle of Least Privilege — an app should only have the permissions it needs. A read-only dashboard app getting `write:admin` scope is a security risk with zero benefit.

---

### Q4. What is the OAuth2 Password Flow and when should you use it (and when NOT to)?

**Answer:**

Password Flow = the user gives their username and password directly to your app, and your app exchanges them for a token from the Authorization Server.

```python
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # form_data.username and form_data.password are available
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
```

**When to use it:**
- Your own first-party mobile or desktop app
- Internal tools where you control both the client and the server
- When users trust your app completely (same company)

**When NOT to use it:**
- Third-party apps requesting access to your users' data
- Any situation where the user shouldn't share their password with that app
- Public-facing OAuth integrations

> **Interview insight:** "Why is the Password Flow considered less secure?" The app sees the user's raw password, even briefly. If the app has a bug or is malicious, passwords are exposed. The Authorization Code Flow (used by "Login with Google") avoids this entirely.

---

### Q5. How does FastAPI implement OAuth2 with JWT end-to-end?

**Answer:**

Full working implementation:

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

app = FastAPI()

SECRET_KEY = "your-secret-key"   # use env variable in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# ── Step 1: Login — exchange credentials for token ──
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_from_db(form_data.username)

    # verify password against bcrypt hash stored in DB
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials",
                            headers={"WWW-Authenticate": "Bearer"})

    token = jwt.encode(
        {"sub": user.username, "exp": datetime.utcnow() + timedelta(minutes=30)},
        SECRET_KEY, algorithm=ALGORITHM
    )
    return {"access_token": token, "token_type": "bearer"}

# ── Step 2: Dependency — verify token on protected routes ──
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        return get_user_from_db(username)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ── Step 3: Protected endpoint ──
@app.get("/me")
async def read_me(current_user = Depends(get_current_user)):
    return {"username": current_user.username}
```

Flow: User POSTs credentials → `/token` validates and returns JWT → client sends JWT in `Authorization: Bearer <token>` header on every subsequent request → `get_current_user` validates it → endpoint runs.

---

---

## Section 2: Error Handling

---

### Q6. What is the difference between HTTPException and a generic Python exception in FastAPI?

**Answer:**

```python
# Generic Python exception — FastAPI does NOT handle this gracefully
@app.get("/users/{id}")
def get_user(id: int):
    raise ValueError("something went wrong")
    # Client receives: 500 Internal Server Error
    # No useful information, exposes internals

# HTTPException — FastAPI handles this and returns clean JSON
@app.get("/users/{id}")
def get_user(id: int):
    raise HTTPException(status_code=404, detail="User not found")
    # Client receives:
    # {"detail": "User not found"}  with status 404
```

**The rule:** Use `HTTPException` for any expected error condition (not found, unauthorized, invalid input). Let unhandled exceptions bubble up as `500` only for truly unexpected crashes — and then fix those bugs.

```python
# Real-world pattern — catch DB errors, return clean response
@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
    except SQLAlchemyError:
        raise HTTPException(status_code=503, detail="Database unavailable")

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
```

> **Interview insight:** Returning a raw 500 with a stack trace to the client is a security risk — it can expose file paths, library versions, and internal logic. Always catch and wrap errors.

---

### Q7. What is a custom exception handler in FastAPI and when would you use one?

**Answer:**

A custom exception handler lets you catch any exception type globally and return a structured JSON response — without putting try/catch in every route.

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# Define a custom exception class
class ItemNotFoundError(Exception):
    def __init__(self, item_id: int):
        self.item_id = item_id

# Register a handler for it
@app.exception_handler(ItemNotFoundError)
async def item_not_found_handler(request: Request, exc: ItemNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "error": "ITEM_NOT_FOUND",
            "message": f"Item {exc.item_id} does not exist",
            "docs": "https://api.example.com/docs#items"  # link to fix
        }
    )

# Now any route can raise it cleanly
@app.get("/items/{item_id}")
def get_item(item_id: int):
    item = db.get(item_id)
    if not item:
        raise ItemNotFoundError(item_id=item_id)  # clean, no try/catch needed
    return item
```

**When to use custom handlers:**
- When multiple routes raise the same error type and you want consistent responses
- When you want machine-readable error codes (not just a string message)
- When you want to log every error centrally in one place

> **Interview insight:** "What's the benefit of machine-readable error codes like `ITEM_NOT_FOUND` vs just a message string?" Frontend teams and API consumers can write `if (error.code === 'ITEM_NOT_FOUND')` in their code. String messages change ("Item not found" → "Item does not exist") and break client logic. Error codes are a stable contract.

---

### Q8. What is a well-structured error response and why does it matter?

**Answer:**

A bad error response gives the client no idea what went wrong or how to fix it:
```json
{"detail": "Error"}
```

A well-structured error response is self-describing and actionable:
```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Request validation failed",
    "status": 422,
    "timestamp": "2025-06-01T10:30:00Z",
    "path": "/api/users",
    "details": [
      {
        "field": "email",
        "issue": "invalid email format",
        "received": "not-an-email"
      },
      {
        "field": "age",
        "issue": "must be a positive integer",
        "received": -5
      }
    ]
  }
}
```

**How to implement this in FastAPI:**
```python
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_FAILED",
                "message": "Request validation failed",
                "details": [
                    {
                        "field": ".".join(str(x) for x in err["loc"]),
                        "issue": err["msg"],
                    }
                    for err in exc.errors()
                ]
            }
        }
    )
```

**Why it matters in industry:** Your API consumers (mobile apps, frontend, partner companies) write code against your error responses. Inconsistent or vague errors mean they have to contact you every time something breaks. Good errors = fewer support tickets.

---

### Q9. How do you handle 404 errors globally in FastAPI?

**Answer:**

FastAPI has a default 404 handler, but you can override it to match your API's error format:

```python
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

# Override the default 404 handler
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": f"HTTP_{exc.status_code}",
                "message": exc.detail,
                "status": exc.status_code,
                "path": str(request.url)
            }
        }
    )
```

**Important distinction:** You must catch `starlette.exceptions.HTTPException` (not `fastapi.HTTPException`) to handle 404s for routes that don't exist at all (i.e., the router couldn't even find a matching path). FastAPI's own `HTTPException` only handles errors raised inside route handlers.

> **Interview insight:** "What happens when someone calls an endpoint that doesn't exist in your FastAPI app?" Starlette (the underlying framework) raises `StarletteHTTPException` with a 404. FastAPI's `@app.exception_handler(HTTPException)` won't catch it — you need to catch the Starlette version.

---

### Q10. How do you log errors properly in FastAPI without exposing internals to the client?

**Answer:**

The pattern is: log everything internally, return minimal info externally.

```python
import logging
import traceback
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

# Global handler for unexpected exceptions (unhandled 500s)
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    # Log full details internally (goes to your logging system / Sentry)
    logger.error(
        "Unhandled exception",
        extra={
            "path": str(request.url),
            "method": request.method,
            "error": str(exc),
            "traceback": traceback.format_exc()
        }
    )

    # Return MINIMAL info to client — no stack traces, no internal paths
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "Something went wrong. Please try again later."
            }
        }
    )
```

**In production, also integrate with Sentry:**
```python
import sentry_sdk
sentry_sdk.init(dsn="your-sentry-dsn")
# Sentry auto-captures unhandled exceptions with full context
```

> **Interview insight:** "Why shouldn't you return the full stack trace to the API client?" Two reasons: security (stack traces reveal file paths, library versions, internal logic — useful for attackers) and UX (stack traces are useless to mobile app developers; a clean message is actionable).

---

---

## Section 3: API Performance

---

### Q11. What are the main ways to improve FastAPI API performance in production?

**Answer:**

Performance problems in APIs almost always fall into one of three buckets:

**1. Slow database queries (most common)**
```python
# Bad — fetches ALL columns, ALL rows, then filters in Python
users = db.query(User).all()
active = [u for u in users if u.is_active]

# Good — filter and select at the DB level
users = db.query(User.id, User.name).filter(User.is_active == True).all()
```

**2. Missing caching (repeated expensive work)**
```python
import redis
cache = redis.Redis()

@app.get("/products")
async def get_products():
    cached = cache.get("all_products")
    if cached:
        return json.loads(cached)             # return in microseconds

    products = db.query(Product).all()        # slow DB call
    cache.setex("all_products", 300, json.dumps(products))  # cache 5 min
    return products
```

**3. Doing work synchronously that could be async or background**
```python
from fastapi.background import BackgroundTasks

@app.post("/orders")
async def create_order(order: OrderCreate, background_tasks: BackgroundTasks):
    new_order = save_order_to_db(order)       # must happen now

    # Don't make the user wait for email sending
    background_tasks.add_task(send_confirmation_email, order.email)

    return new_order                          # responds immediately
```

> **Interview insight:** "If your API endpoint is slow, what's your debugging process?" The expected answer: first check query times (add DB logging), then check if caching can help, then check if async I/O is being used correctly, then profile for CPU bottlenecks.

---

### Q12. What is connection pooling and why does every production API need it?

**Answer:**

Opening a database connection is expensive — it involves TCP handshakes, authentication, and memory allocation. If your API opens a new connection on every request, it slows down under load and can exhaust the database's connection limit.

Connection pooling keeps a set of connections open and reuses them.

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    "postgresql://user:pass@localhost/mydb",
    pool_size=10,        # keep 10 connections open permanently
    max_overflow=20,     # allow up to 20 extra under high load
    pool_timeout=30,     # wait max 30s for a free connection
    pool_recycle=3600,   # recycle connections every hour (avoids stale connections)
)

SessionLocal = sessionmaker(bind=engine)

# FastAPI dependency — borrows a connection, returns it after the request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()   # returns connection to pool, doesn't actually close it
```

**The analogy:** Connection pooling is like a shared fleet of taxis. Instead of every passenger buying a car (new connection per request), they share a pool of available taxis. Much faster, much cheaper.

> **Interview insight:** "What happens if you don't use connection pooling and you get 1000 concurrent requests?" Your database gets 1000 simultaneous connection attempts, likely exceeds its `max_connections` limit (PostgreSQL default is 100), and starts rejecting connections. Your API crashes. Connection pooling is not optional in production.

---

### Q13. What is caching and what are the different levels where you can cache in a FastAPI app?

**Answer:**

Caching stores the result of an expensive operation so future requests can get it instantly without repeating the work.

**Level 1 — In-memory cache (fastest, local to one server)**
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_config_from_db():
    return db.query(Config).first()  # cached after first call
```
Problem: cleared on restart, not shared between multiple server instances.

**Level 2 — Redis cache (shared across all servers)**
```python
import redis, json
cache = redis.Redis(host="redis-server", port=6379)

@app.get("/categories")
async def get_categories():
    key = "categories"
    cached = cache.get(key)
    if cached:
        return json.loads(cached)

    categories = db.query(Category).all()
    cache.setex(key, 600, json.dumps([c.dict() for c in categories]))  # 10 min TTL
    return categories
```

**Level 3 — HTTP cache headers (browser/CDN caches the response)**
```python
from fastapi.responses import Response

@app.get("/static-data")
async def static_data(response: Response):
    response.headers["Cache-Control"] = "public, max-age=3600"  # cache 1 hour
    return {"data": "..."}
```

**What to cache:** Expensive, rarely-changing data — product catalogs, config settings, user permissions. Never cache user-specific sensitive data in a shared cache without namespacing by user ID.

> **Interview insight:** "What is cache invalidation and why is it called one of the two hardest problems in CS?" When the underlying data changes, cached copies become stale. Deciding when to invalidate (delete) the cache is non-trivial — too aggressive = no performance gain, too lenient = users see stale data.

---

---

## Section 4: async/await

---

### Q14. What exactly does async/await do in Python? Explain with a real analogy.

**Answer:**

`async/await` is a way to write code that can pause and let other code run while it's waiting — without creating multiple threads.

**The analogy — a chef cooking:**

Synchronous chef:
- Puts pasta in boiling water
- Stands and stares at the pot for 10 minutes
- Only then starts chopping vegetables

Async chef:
- Puts pasta in boiling water
- While pasta cooks, chops vegetables
- While vegetables cook, slices bread
- Checks on pasta when timer goes off

Same one chef, same one thread. But async = productive during waiting time.

```python
import asyncio

# Sync — waits doing nothing
def sync_fetch():
    time.sleep(2)      # staring at the pot
    return "data"

# Async — pauses, lets other tasks run, resumes when ready
async def async_fetch():
    await asyncio.sleep(2)   # chef goes and chops vegetables
    return "data"

# With real I/O — calling an external API
async def get_user_data(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.example.com/users/{user_id}")
        # During this await, FastAPI can handle 100 other requests
        return response.json()
```

> **Interview insight:** "Does async/await use multiple threads?" No. It uses a single thread with an event loop. The event loop switches between tasks when they're waiting for I/O. This is why async works great for I/O-bound tasks but not CPU-bound tasks (heavy computation still blocks the single thread).

---

### Q15. When should you use async def vs def in FastAPI, and what mistakes do developers make?

**Answer:**

```python
# Use async def for — I/O bound work
# DB queries, external API calls, file reads/writes
@app.get("/users")
async def get_users(db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(User))   # non-blocking DB call
    return result.scalars().all()

# Use def for — CPU bound work or when using sync libraries
@app.get("/compute")
def run_computation():
    result = some_heavy_math()   # FastAPI runs this in a thread pool
    return {"result": result}
```

**Mistake 1 — Using async def with a blocking library:**
```python
# WRONG — blocks the entire event loop
@app.get("/users")
async def get_users():
    import requests                          # 'requests' is a BLOCKING library
    response = requests.get("https://...")   # blocks event loop while waiting
    return response.json()

# RIGHT — use httpx for async HTTP calls
@app.get("/users")
async def get_users():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://...")  # non-blocking
        return response.json()
```

**Mistake 2 — Blocking the event loop with CPU work inside async def:**
```python
# WRONG — heavy computation blocks all other requests
@app.get("/process-image")
async def process_image():
    result = heavy_image_processing()   # blocks event loop for 5 seconds
    return result

# RIGHT — run CPU work in a thread pool
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor()

@app.get("/process-image")
async def process_image():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, heavy_image_processing)
    return result
```

**Quick decision rule:**
- Talking to DB, external API, files → `async def` + async library
- CPU math, image processing, ML inference → `def` (FastAPI uses thread pool)
- Using a library that doesn't support async → `def` (safer than blocking event loop)

> **Interview insight:** "What happens if you accidentally block the event loop in a FastAPI async route?" Every other request queues up and waits. A single slow `async def` route that calls a blocking library can make your entire API unresponsive — not just that one endpoint. This is why mixing async and sync correctly is a real skill, not just syntax.

---

---

## Quick Reference

### OAuth2 flow summary
```
Client → Authorization Server → issues token → Client
Client → Resource Server (with token) → gets data
```

### Error handling priority
```
Expected errors     → HTTPException with correct status code
Repeated error types → Custom exception + global handler
All unhandled 500s  → Global handler: log internally, return minimal response
```

### async/await decision
```
I/O bound (DB, network, files)  → async def + async library
CPU bound (compute, ML)         → def OR run_in_executor
Sync library only available     → def (thread pool is safer)
```

### Performance checklist
```
□ DB queries filtered at DB level, not Python
□ Connection pooling configured
□ Caching for expensive, stable data (Redis)
□ Background tasks for non-blocking side effects
□ async used correctly for I/O, not blocking the event loop
```

---

*Total: 15 questions covering OAuth2, Error Handling, API Performance, and async/await — Medium difficulty, 2–3 yr exp level.*
