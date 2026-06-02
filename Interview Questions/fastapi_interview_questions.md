# FastAPI & Security — Interview Questions (Module 7 & 8)
### Targeted at 2–3 year experience level | Freshers doing internships — learn these cold

---

## Module 7: Web Development with FastAPI

---

### Q1. What is FastAPI and why would you choose it over Flask?

**Answer:**

FastAPI is a modern Python web framework for building APIs. Flask is older and simpler, but FastAPI has three big advantages:

- **Speed** — FastAPI is built on top of Starlette (ASGI), so it handles async requests natively. Flask is WSGI (synchronous).
- **Automatic validation** — FastAPI uses Pydantic. If someone sends wrong data to your endpoint, FastAPI rejects it automatically before your code even runs. In Flask, you write that validation yourself.
- **Auto-generated docs** — FastAPI creates a Swagger UI at `/docs` for free. No extra setup.

**Simple analogy:** Flask is a basic kitchen. FastAPI is a kitchen with a built-in dishwasher, auto-labelled shelves, and a prep station. You can cook in both, but one saves you a lot of extra work.

**Why interviewers ask this:** They want to know if you understand *why* you're using a tool, not just *how*.

---

### Q2. What is ASGI and why does FastAPI use it instead of WSGI?

**Answer:**

WSGI (Flask's interface) handles one request at a time per worker. If a request is waiting for a database query, that worker is just sitting idle — blocked.

ASGI (FastAPI's interface) is async. While Request 1 is waiting for the database, the server can start handling Request 2. Same thread, no wasted idle time.

```python
# Flask (WSGI) — synchronous, blocks
@app.route("/users")
def get_users():
    time.sleep(2)   # entire worker is blocked here
    return users

# FastAPI (ASGI) — async, non-blocking
@app.get("/users")
async def get_users():
    await asyncio.sleep(2)  # other requests run during this wait
    return users
```

**Why it matters in industry:** APIs that talk to databases or external services spend most of their time *waiting*. ASGI makes that waiting time productive.

---

### Q3. How do you set up a basic FastAPI application?

**Answer:**

```bash
pip install fastapi uvicorn
```

```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

```bash
uvicorn main:app --reload
# --reload = auto-restarts when you save changes (dev only)
```

FastAPI runs on Uvicorn (ASGI server). In production, you'd use:

```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

---

### Q4. What is the difference between a path parameter and a query parameter?

**Answer:**

| | Path Parameter | Query Parameter |
|---|---|---|
| Where | Part of the URL | After `?` in the URL |
| Required? | Always required | Optional (can have default) |
| Use case | Identify a specific resource | Filter or configure results |

```python
# Path parameter — identifies resource /users/42
@app.get("/users/{user_id}")
def get_user(user_id: int):   # FastAPI extracts 42 from URL
    return {"id": user_id}

# Query parameter — filters results /users?city=Ahmedabad&limit=10
@app.get("/users")
def list_users(city: str = None, limit: int = 20):
    return {"city": city, "limit": limit}

# Both together — /orders/5/items?status=pending
@app.get("/orders/{order_id}/items")
def get_items(order_id: int, status: str = None):
    return {"order": order_id, "status": status}
```

**Interview trap:** "Can a path parameter be optional?" — No. If it's in the URL pattern, it must be provided. Use a query param if it's optional.

---

### Q5. What is Pydantic and why is it used in FastAPI?

**Answer:**

Pydantic is a data validation library. You define what your data *should* look like using a Python class, and Pydantic enforces it automatically.

Without Pydantic, you'd write manual checks everywhere:
```python
# Without Pydantic — you write all this yourself
def create_user(data):
    if "name" not in data:
        raise ValueError("name is required")
    if not isinstance(data["age"], int):
        raise ValueError("age must be int")
    if data["age"] < 0:
        raise ValueError("age must be positive")
```

With Pydantic in FastAPI:
```python
from pydantic import BaseModel, validator

class UserCreate(BaseModel):
    name: str
    age: int
    email: str

    @validator("age")
    def age_must_be_positive(cls, v):
        if v < 0:
            raise ValueError("Age cannot be negative")
        return v

@app.post("/users")
def create_user(user: UserCreate):   # FastAPI validates automatically
    return user                       # if invalid, returns 422 before reaching here
```

If someone sends `{"name": "Arjun", "age": "not_a_number"}`, FastAPI returns a `422 Unprocessable Entity` error automatically — your function never even runs.

**Why interviewers ask this:** Validation is where most security bugs and production crashes happen. Knowing Pydantic shows you understand defensive programming.

---

### Q6. What HTTP status code does FastAPI return when Pydantic validation fails, and why?

**Answer:**

FastAPI returns `422 Unprocessable Entity`.

- `400 Bad Request` — the request was malformed (e.g., broken JSON syntax)
- `422 Unprocessable Entity` — the JSON was valid, but the *content* didn't match the expected schema (e.g., sent a string where an int was expected)

The distinction matters: `400` means "we couldn't even parse what you sent." `422` means "we parsed it fine, but the data doesn't make sense."

FastAPI also returns a detailed error body showing exactly which field failed and why — very useful for API consumers debugging their integration.

---

### Q7. How do you handle GET, POST, PUT, and DELETE in FastAPI with a real example?

**Answer:**

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

items_db = {}

class Item(BaseModel):
    name: str
    price: float

# GET — read
@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

# POST — create
@app.post("/items", status_code=201)
def create_item(item: Item):
    item_id = len(items_db) + 1
    items_db[item_id] = item
    return {"id": item_id, **item.dict()}

# PUT — replace entire item
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_id] = item
    return items_db[item_id]

# DELETE — remove
@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
```

---

### Q8. What are CRUD operations and how do they map to HTTP methods?

**Answer:**

CRUD = Create, Read, Update, Delete. These are the four fundamental operations any data-driven app needs.

| CRUD | HTTP Method | SQL equivalent | Status code |
|---|---|---|---|
| Create | POST | INSERT | 201 Created |
| Read | GET | SELECT | 200 OK |
| Update | PUT / PATCH | UPDATE | 200 OK |
| Delete | DELETE | DELETE | 204 No Content |

Every API you build in your career — whether it's for users, orders, products, or anything else — is essentially CRUD on top of a database. FastAPI just gives you a clean way to wire HTTP methods to your database operations.

---

### Q9. What is the difference between PUT and PATCH? When would you use each?

**Answer:**

- **PUT** — replace the *entire* resource. If you forget to include a field, it gets wiped.
- **PATCH** — update *only* the fields you send. Everything else stays the same.

```python
# Current record: {"name": "Arjun", "email": "a@b.com", "city": "Ahmedabad"}

# PUT with only name — email and city get wiped!
requests.put("/users/1", json={"name": "Arjun Shah"})
# Result: {"name": "Arjun Shah"}  ← email and city gone

# PATCH with only name — email and city are preserved
requests.patch("/users/1", json={"name": "Arjun Shah"})
# Result: {"name": "Arjun Shah", "email": "a@b.com", "city": "Ahmedabad"}
```

In FastAPI, PATCH models use `Optional` fields with `exclude_unset=True`:

```python
from typing import Optional

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    city: Optional[str] = None

@app.patch("/users/{user_id}")
def patch_user(user_id: int, updates: UserUpdate):
    patch_data = updates.dict(exclude_unset=True)  # only fields actually sent
    # apply patch_data to existing record
```

**Use PUT** when replacing a config file or document. **Use PATCH** for profile updates, status changes, toggling a flag.

---

### Q10. What is Swagger UI and how does FastAPI generate it automatically?

**Answer:**

Swagger UI is an interactive web page that documents your API. It shows every endpoint, what parameters they take, what they return, and lets you test them directly from the browser — no Postman needed.

FastAPI generates it automatically at:
- `/docs` — Swagger UI (interactive)
- `/redoc` — ReDoc (readable documentation)
- `/openapi.json` — raw JSON spec

FastAPI can do this because Pydantic models give it the type information it needs to describe every endpoint's inputs and outputs. You write one class, and FastAPI documents the API for you.

```python
@app.post("/users", response_model=UserResponse, status_code=201,
          summary="Create a new user",
          description="Registers a new user account in the system")
def create_user(user: UserCreate):
    ...
```

**Why it matters in industry:** Teams use Swagger UI as a contract between frontend and backend. The backend dev documents the API, the frontend dev tests it in Swagger before writing any code.

---

### Q11. How do you serve a machine learning model through a FastAPI endpoint?

**Answer:**

The pattern is: load your model once when the app starts, then expose a prediction endpoint.

```python
import joblib
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Load model once at startup — NOT inside the endpoint function
# If you load inside the function, it reloads on every request (very slow)
model = joblib.load("model.pkl")

class PredictionInput(BaseModel):
    features: list[float]

@app.post("/predict")
def predict(data: PredictionInput):
    features = np.array(data.features).reshape(1, -1)
    prediction = model.predict(features)
    return {"prediction": prediction[0]}
```

**Common mistake interviewers look for:** Loading the model inside the endpoint function. The model should be a module-level variable, loaded once when the app starts. Otherwise every API call pays the cost of loading a potentially large file.

---

---

## Module 8: Security, Authentication & Middleware

---

### Q12. What is the difference between Authentication and Authorization?

**Answer:**

- **Authentication** = proving who you are ("I am Arjun")
- **Authorization** = checking what you're allowed to do ("Arjun can read but not delete")

**Real-world analogy:**
- Authentication = showing your ID at the office entrance
- Authorization = your ID card only opens certain floors

```
User logs in with email + password   →   Authentication
System checks if user can delete records   →   Authorization
```

In code terms:
- Authentication: verify the JWT token is valid and extract the user identity
- Authorization: check if that user's role (`admin`, `user`, `viewer`) allows the requested action

**Interview trap:** People mix these up constantly. `401 Unauthorized` actually means "not authenticated" (no valid token). `403 Forbidden` means "authenticated but not authorized" (valid token, wrong permissions). The naming in HTTP is historically confusing.

---

### Q13. What is a Session ID and how does session-based authentication work?

**Answer:**

When you log in, the server creates a session — a record that says "user Arjun is logged in." The server stores this record and gives you a random Session ID (a long random string). Your browser stores this ID in a cookie and sends it with every request.

```
Login flow:
1. User sends email + password → server verifies
2. Server creates session: {"session_id": "abc123", "user_id": 42, "expires": "..."}
3. Server stores this in Redis/database
4. Server sends back: Set-Cookie: session_id=abc123

Subsequent requests:
1. Browser sends Cookie: session_id=abc123
2. Server looks up abc123 in its session store
3. Finds user_id=42 → user is authenticated
```

**Problem with sessions:** The server must store every active session. With millions of users, this becomes a scaling problem. This is why stateless JWT tokens became popular.

---

### Q14. What is a JWT (JSON Web Token)? Explain its structure.

**Answer:**

A JWT is a self-contained token that proves who you are. The key difference from sessions: **the server stores nothing**. All the user information is encoded in the token itself.

A JWT looks like this:
```
eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo0Mn0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

It has three parts separated by dots:

```
HEADER . PAYLOAD . SIGNATURE

Header   → {"alg": "HS256", "typ": "JWT"}   — which algorithm was used
Payload  → {"user_id": 42, "role": "admin", "exp": 1735689600}   — the data
Signature → HMAC(header + payload, SECRET_KEY)   — proof it wasn't tampered with
```

The header and payload are base64-encoded (not encrypted — anyone can decode them). The signature is the security. If someone changes the payload (e.g., changes `role` from `user` to `admin`), the signature won't match and the server rejects the token.

**Critical point:** Never put passwords or sensitive data in a JWT payload. It's encoded, not encrypted.

---

### Q15. How do you implement JWT authentication in FastAPI?

**Answer:**

```python
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import datetime, timedelta

app = FastAPI()
SECRET_KEY = "your-secret-key"   # store in .env, never hardcode in production
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def create_token(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=24)   # token expires in 24h
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/login")
def login(email: str, password: str):
    # verify email/password against DB here
    user_id = 42   # from DB lookup
    token = create_token(user_id)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/profile")
def get_profile(current_user: int = Depends(get_current_user)):
    return {"user_id": current_user}   # endpoint is now protected
```

`Depends(get_current_user)` tells FastAPI: run this function first, and if it raises an exception, stop here and return the error.

---

### Q16. What is the difference between JWT, Sessions, and OAuth? When do you use each?

**Answer:**

| | Session | JWT | OAuth |
|---|---|---|---|
| Storage | Server stores session | Client stores token | Varies |
| Stateless? | No | Yes | Depends |
| Best for | Traditional web apps | APIs, mobile apps | Third-party login |
| Example | Django sessions | FastAPI APIs | "Login with Google" |

**Sessions** — the server remembers you. Easy to revoke (just delete the session). Bad for distributed systems (which server has the session?).

**JWT** — the token carries the proof. Server stores nothing. Great for APIs. Hard to revoke (token is valid until it expires — you can't "log someone out" without extra infrastructure).

**OAuth** — a protocol that lets users grant your app access to their data on another platform (Google, GitHub). "Login with Google" is OAuth. You don't handle passwords — you let Google do authentication, and Google gives your app a token.

**Practical rule for your internship:** Building an internal API? Use JWT. Building a consumer app that needs social login? Use OAuth. Building a traditional web app with server-rendered pages? Sessions.

---

### Q17. Why can't you immediately invalidate a JWT after logout?

**Answer:**

This is a favourite interview question because it reveals whether you understand the stateless nature of JWTs.

When a user logs out, you delete the token on the client side. But the token itself is still mathematically valid until its expiry time. If someone copied that token before logout, they can still use it.

Solutions companies use:

1. **Short expiry times** — tokens expire in 15 minutes. Even if stolen, they're quickly useless. Use refresh tokens for longer sessions.
2. **Token blacklist** — store revoked tokens in Redis. On every request, check if the token is blacklisted. (This re-introduces state, which partially defeats the purpose of JWT.)
3. **Refresh token rotation** — when the user logs out, invalidate the refresh token. Short-lived access tokens expire on their own.

Most production systems use a combination of short-lived access tokens (15 min) and long-lived refresh tokens (30 days) stored securely.

---

### Q18. What is OAuth and how does "Login with Google" actually work?

**Answer:**

OAuth is a protocol that lets users give your app permission to access their data on another service (Google, GitHub, etc.) without sharing their password with you.

```
Flow for "Login with Google":

1. User clicks "Login with Google" on your site
2. Your app redirects to Google's login page with your app's client_id
3. User logs in on Google (you never see their password)
4. Google redirects back to your site with an authorization code
5. Your backend exchanges this code for an access token (server to server)
6. Your backend uses the access token to call Google's API: GET /userinfo
7. Google returns: {"email": "arjun@gmail.com", "name": "Arjun"}
8. You create or find the user in your own database
9. You issue your own JWT to the user for future requests
```

**Why OAuth matters:** You don't handle passwords. If your database is breached, no passwords are exposed. Users trust Google's security more than a random startup's.

---

### Q19. What is Middleware in FastAPI? How is it different from a route handler?

**Answer:**

A route handler handles one specific endpoint. Middleware runs on every single request before it reaches any handler — and on every response going back.

Think of middleware as a security checkpoint at an airport. Every passenger (request) passes through it, regardless of where they're going.

```python
from fastapi import FastAPI, Request
import time

app = FastAPI()

@app.middleware("http")
async def add_timing_header(request: Request, call_next):
    start = time.time()

    response = await call_next(request)   # passes to the actual route handler

    duration = time.time() - start
    response.headers["X-Process-Time"] = str(duration)
    return response
```

**Common middleware uses in industry:**
- Authentication checks (verify JWT on every request)
- Request logging (log every API call for debugging)
- Rate limiting (block users who make too many requests)
- CORS headers (allow cross-origin requests)
- Request ID injection (add a unique ID to trace a request through logs)

**Why route-level auth isn't enough:** If you put auth logic inside every route function, you'll eventually forget one. Middleware guarantees every request passes through auth.

---

### Q20. What is the order of middleware execution in FastAPI?

**Answer:**

Middleware runs like an onion — layers wrap around each other.

```
Request  →  Middleware 1  →  Middleware 2  →  Route Handler
Response ←  Middleware 1  ←  Middleware 2  ←  Route Handler
```

The middleware added last wraps the outermost layer (runs first on request, last on response). This matters because if your auth middleware runs after your logging middleware, you'd log unauthenticated requests before rejecting them — which might be what you want (audit trail) or might not be (noise in logs).

```python
app.add_middleware(LoggingMiddleware)   # added first = inner layer
app.add_middleware(AuthMiddleware)      # added last = outer layer (runs first)
```

---

### Q21. What is CORS and why does it exist?

**Answer:**

CORS (Cross-Origin Resource Sharing) is a browser security rule that blocks JavaScript code on one domain from making API calls to a different domain.

**Why it exists:** Imagine you're logged into your bank at `bank.com`. A malicious site `evil.com` has JavaScript that tries to call `bank.com/transfer` using your cookies. Without CORS, that would work. CORS prevents it.

```
Your React app at localhost:3000 calls API at localhost:8000
→ Browser blocks this!  (different port = different origin)

Your frontend at myapp.com calls API at api.myapp.com
→ Browser blocks this!  (different subdomain = different origin)
```

The browser checks: does the API server explicitly say it allows requests from this origin? If not, block it.

**Important:** CORS is enforced by the *browser*, not the server. If you call an API with `curl` or Python `requests`, CORS doesn't apply. It's purely a browser protection.

---

### Q22. What is the difference between a Simple request and a Preflight request in CORS?

**Answer:**

**Simple requests** — GET or POST with basic headers (like `Content-Type: text/plain`). The browser just sends the request and checks the response headers.

**Preflight requests** — Before sending the actual request, the browser sends an `OPTIONS` request first to ask: "Is this allowed?"

```
Preflight (sent automatically by browser):
OPTIONS /api/users HTTP/1.1
Origin: https://myapp.com
Access-Control-Request-Method: DELETE
Access-Control-Request-Headers: Authorization

Server response (must include these headers):
Access-Control-Allow-Origin: https://myapp.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Authorization
```

Preflight triggers when:
- Method is PUT, DELETE, or PATCH
- Custom headers like `Authorization` or `Content-Type: application/json` are used

This is why API calls with JWT tokens always trigger a preflight — they use the `Authorization` header.

---

### Q23. How do you configure CORS in FastAPI?

**Answer:**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://myapp.com", "http://localhost:3000"],  # who can call
    allow_credentials=True,     # allow cookies to be sent
    allow_methods=["*"],        # allow all HTTP methods
    allow_headers=["*"],        # allow all headers including Authorization
)
```

**In development** you might use `allow_origins=["*"]` (allow everyone). Never do this in production — it defeats the purpose of CORS entirely.

**In production**, always list specific origins. If your API is truly public, `*` is acceptable but you should also think about rate limiting.

**Common interview gotcha:** Setting `allow_origins=["*"]` and `allow_credentials=True` at the same time is invalid — browsers reject it. If you need credentials (cookies, Authorization headers), you must list specific origins.

---

### Q24. What is the `Depends` system in FastAPI and why is it powerful?

**Answer:**

`Depends` is FastAPI's dependency injection system. Instead of calling a function directly, you declare that your endpoint *depends* on it, and FastAPI handles the calling, caching, and error handling automatically.

```python
from fastapi import Depends, HTTPException

def get_db():
    db = SessionLocal()
    try:
        yield db        # endpoint uses this
    finally:
        db.close()      # always closes even if endpoint crashes

def get_current_user(token: str = Depends(oauth2_scheme), db = Depends(get_db)):
    user = db.query(User).filter(User.token == token).first()
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

# Now any endpoint can require auth with one line
@app.get("/orders")
def list_orders(current_user: User = Depends(get_current_user)):
    return current_user.orders
```

**Why it's powerful:**
- You write auth/db logic once, reuse it everywhere
- FastAPI auto-documents dependencies in Swagger
- Dependencies can have their own dependencies (chains)
- Replaces Flask's `@login_required` decorator in a more composable way

---

### Q25. How do you protect specific routes in FastAPI (role-based access)?

**Answer:**

```python
def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

def require_user(current_user: User = Depends(get_current_user)):
    return current_user   # any logged-in user is fine

# Only admins can delete users
@app.delete("/users/{user_id}")
def delete_user(user_id: int, admin: User = Depends(require_admin)):
    ...

# Any logged-in user can view their own profile
@app.get("/profile")
def get_profile(user: User = Depends(require_user)):
    ...
```

This is the FastAPI way of doing role-based access control (RBAC). The `403 Forbidden` response tells the client: "you're logged in, but you don't have permission."

---

### Q26. What is the difference between `401 Unauthorized` and `403 Forbidden`?

**Answer:**

- `401 Unauthorized` — you didn't provide valid credentials. No token, expired token, or invalid token. The server doesn't know who you are.
- `403 Forbidden` — you provided valid credentials (the server knows who you are), but you don't have permission to do this action.

```
No token on request         →  401 (who are you?)
Expired JWT token           →  401 (prove who you are again)
Valid token, wrong role     →  403 (I know who you are, but no)
Valid token, accessing another user's data  →  403 (not your data)
```

**In FastAPI:**
```python
raise HTTPException(status_code=401, detail="Token expired")     # not authenticated
raise HTTPException(status_code=403, detail="Admin only")         # not authorized
```

---

### Q27. What is a refresh token and how does it work with access tokens?

**Answer:**

**Access token** — short-lived (15–60 minutes). Used on every API call. If stolen, attacker has limited time.

**Refresh token** — long-lived (7–30 days). Stored securely (HttpOnly cookie). Used only to get a new access token when the current one expires.

```
Login:
→ Server returns access_token (expires 15min) + refresh_token (expires 30 days)

Client stores:
→ access_token in memory (not localStorage — XSS risk)
→ refresh_token in HttpOnly cookie (JavaScript can't read it)

Access token expires:
→ Client sends refresh_token to /auth/refresh
→ Server validates refresh_token, issues new access_token
→ Old refresh_token is invalidated (rotation)

Logout:
→ Server blacklists the refresh_token
→ Even if someone has the access_token, it expires in 15 min max
```

**Why not just use a long-lived access token?** If it's stolen (XSS, man-in-the-middle), the attacker has access for days or weeks. Short access tokens limit the damage window.

---

### Q28. What is the `HTTPException` in FastAPI and how do you use it correctly?

**Answer:**

`HTTPException` is how you intentionally return error responses from your endpoints. When you raise it, FastAPI stops executing your function and returns the error response to the client.

```python
from fastapi import HTTPException

@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = db.get(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"    # this goes in the response body
        )

    if not current_user.can_access(user):
        raise HTTPException(
            status_code=403,
            detail="You cannot access this user's data"
        )

    return user
```

You can also add custom headers (useful for WWW-Authenticate in auth errors):
```python
raise HTTPException(
    status_code=401,
    detail="Token expired",
    headers={"WWW-Authenticate": "Bearer"}
)
```

**Common mistake:** Using Python's built-in `raise ValueError(...)` inside a route. FastAPI doesn't catch that — it returns a `500 Internal Server Error`. Always use `HTTPException` for controlled error responses.

---

### Q29. How do environment variables and secret management work in FastAPI?

**Answer:**

You should never hardcode secrets (database passwords, JWT secret keys, API keys) in your code. They go in environment variables.

```python
# .env file (never commit this to git)
SECRET_KEY=super-secret-key-here
DATABASE_URL=postgresql://user:pass@localhost/mydb
```

```python
# config.py — using Pydantic's BaseSettings
from pydantic import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    database_url: str
    debug: bool = False

    class Config:
        env_file = ".env"

settings = Settings()   # reads from .env automatically

# main.py
from config import settings
token = jwt.encode(payload, settings.secret_key)
```

**Why this matters in industry:**
- Different values for dev, staging, production without changing code
- Secrets are set by DevOps, not visible to developers
- If code is open-sourced, secrets aren't exposed

---

### Q30. What happens inside FastAPI when a request comes in? Walk through the lifecycle.

**Answer:**

This is a classic "how does it work internally" question.

```
1. Uvicorn receives the HTTP request (ASGI server)

2. FastAPI's ASGI app receives it

3. Middleware chain runs (auth check, logging, CORS headers, etc.)

4. Router matches the URL pattern to a handler function
   e.g., GET /users/42 matches @app.get("/users/{user_id}")

5. FastAPI extracts and validates parameters:
   - Path params from URL
   - Query params from URL
   - Request body parsed and validated by Pydantic
   - If validation fails → 422 response returned here

6. Dependencies (Depends) are resolved:
   - get_db() runs, provides a DB session
   - get_current_user() runs, verifies JWT

7. Handler function executes (your business logic)

8. Return value is serialized to JSON

9. Middleware runs again on the response

10. Uvicorn sends the HTTP response back to the client
```

**Why interviewers ask this:** Understanding the request lifecycle helps you debug production issues — you know exactly where an error could originate.

---

### Q31. What is the difference between `async def` and `def` in FastAPI route handlers?

**Answer:**

```python
# Async — use for I/O operations (database, external API calls, file reads)
@app.get("/users")
async def get_users():
    users = await database.fetch_all("SELECT * FROM users")   # non-blocking
    return users

# Sync — use for CPU-heavy tasks or when using blocking libraries
@app.get("/compute")
def compute():
    result = heavy_calculation()   # runs in a thread pool automatically
    return result
```

FastAPI handles both correctly:
- `async def` runs in the event loop (non-blocking)
- `def` (sync) runs in a thread pool (FastAPI moves it off the main thread so it doesn't block other requests)

**Common mistake:** Using `async def` with a blocking library that doesn't support async (like standard `requests` or old SQLAlchemy). This blocks the event loop and kills performance. Use `httpx` instead of `requests`, and async SQLAlchemy if you're using `async def`.

---

### Q32. How do you validate nested objects and lists in Pydantic?

**Answer:**

Pydantic handles nested models naturally:

```python
from pydantic import BaseModel
from typing import List

class Address(BaseModel):
    street: str
    city: str
    pincode: str

class OrderItem(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderCreate(BaseModel):
    user_id: int
    delivery_address: Address           # nested model
    items: List[OrderItem]             # list of nested models
    coupon_code: str | None = None     # optional field

@app.post("/orders", status_code=201)
def create_order(order: OrderCreate):
    return order
```

Sending this JSON:
```json
{
  "user_id": 1,
  "delivery_address": {"street": "MG Road", "city": "Ahmedabad", "pincode": "380001"},
  "items": [{"product_id": 5, "quantity": 2, "price": 199.0}]
}
```

Pydantic validates every field at every level. If `pincode` is missing, you get a `422` error pointing exactly to `delivery_address.pincode`. No manual checking needed.

---

### Q33. What is rate limiting and how would you implement it with middleware?

**Answer:**

Rate limiting prevents a single client from making too many requests in a short time. This protects your API from abuse, DoS attacks, and scraping.

```python
from fastapi import FastAPI, Request, HTTPException
from collections import defaultdict
import time

app = FastAPI()

# Simple in-memory rate limiter (use Redis in production)
request_counts = defaultdict(list)
LIMIT = 10        # max requests
WINDOW = 60       # per 60 seconds

@app.middleware("http")
async def rate_limit(request: Request, call_next):
    client_ip = request.client.host
    now = time.time()

    # Remove requests older than the window
    request_counts[client_ip] = [
        t for t in request_counts[client_ip] if now - t < WINDOW
    ]

    if len(request_counts[client_ip]) >= LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Try again in a minute."
        )

    request_counts[client_ip].append(now)
    return await call_next(request)
```

**In production:** Use Redis (shared across all server instances) instead of in-memory dicts. Libraries like `slowapi` wrap this pattern cleanly for FastAPI.

**Status code:** `429 Too Many Requests` — always include a `Retry-After` header telling clients when to try again.

---

### Q34. What is the difference between cookies and localStorage for storing JWT tokens, and which is more secure?

**Answer:**

| | localStorage | HttpOnly Cookie |
|---|---|---|
| Accessible by JS | Yes | No |
| Sent automatically | No (manual) | Yes (automatic) |
| XSS risk | High | Low |
| CSRF risk | Low | Medium |
| Recommended for JWT | No | Yes |

**localStorage** — simple to use, but JavaScript can read it. If your site has an XSS vulnerability (attacker injects JavaScript), they can steal the token with `localStorage.getItem('token')`.

**HttpOnly cookie** — the browser stores it, JavaScript cannot read it (`document.cookie` won't show it), but it's sent automatically on every request. Protects against XSS. Vulnerable to CSRF (use CSRF tokens to mitigate).

**Industry recommendation:** Store refresh tokens in HttpOnly cookies. Store access tokens in memory (a JavaScript variable) — they expire quickly, so if lost on page refresh, the refresh token gets a new one.

---

### Q35. What is HTTPS and why is everything above meaningless without it?

**Answer:**

HTTPS = HTTP + TLS encryption. Every byte sent between client and server is encrypted.

Without HTTPS:
- JWTs in headers → anyone on the same network can read them (man-in-the-middle)
- Passwords sent to `/login` → visible as plain text on the network
- Cookies → readable and injectable

With HTTPS:
- All data is encrypted end-to-end
- Server identity is verified (the certificate proves it's really `api.yourapp.com`)

In FastAPI production deployment:
```
Client → HTTPS → Nginx (handles SSL termination) → HTTP → Uvicorn → FastAPI
```

Nginx handles the SSL certificate (usually from Let's Encrypt, which is free). Your FastAPI app itself only ever sees plain HTTP internally.

**Why interviewers ask this:** Juniors sometimes focus heavily on JWT and OAuth but forget that without HTTPS, tokens can be stolen in transit. Security is a stack, not a single feature.

---

## Quick Reference: Status Codes to Know Cold

| Code | Meaning | When to use |
|---|---|---|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Malformed request syntax |
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | Authenticated but no permission |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate (e.g., email already exists) |
| 422 | Unprocessable Entity | Pydantic validation failed |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Unhandled exception in your code |

---

*Total: 35 questions covering FastAPI Basics, Pydantic, CRUD, JWT, OAuth, Sessions, Middleware, CORS, and Security best practices.*
