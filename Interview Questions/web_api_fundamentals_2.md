# Web & API Fundamentals – Part 2: Why & How (18 Deep-Dive Questions)

---

## HTTP Protocol

---

### 1. Why does HTTP/2 use multiplexing — and how does it work?

**The Problem with HTTP/1.1:**
In HTTP/1.1, requests go one at a time on one connection. The next request has to **wait** for the previous one to finish. This is called **Head-of-Line Blocking**.

```
# HTTP/1.1 — one at a time (slow)
Connection 1: Request A → wait → Response A → Request B → wait → Response B

# To load a webpage with 10 files, browser opens 10 separate connections
# That's expensive and slow
```

**How HTTP/2 Multiplexing fixes it:**
Multiple requests travel on the **same connection simultaneously** — no waiting.

```
# HTTP/2 — all at once on ONE connection
Connection 1:
  Stream 1: → Request A ←→ Response A
  Stream 2: → Request B ←→ Response B
  Stream 3: → Request C ←→ Response C

# All happening at the same time, same connection
```

> **Why it matters:** Websites load faster on HTTP/2 without any code changes. Knowing this shows you understand *why* performance improves, not just that it does.

---

### 2. Why are cookies used — and how do they differ from headers?

**The Problem:**
HTTP is stateless — the server forgets you after every request. But websites need to remember you (login, cart, preferences).

**How Cookies solve it:**
Server sends a cookie → Browser stores it → Browser sends it automatically on every future request.

```
# Step 1: Server sets a cookie in the response header
HTTP/1.1 200 OK
Set-Cookie: session_id=abc123; HttpOnly; Expires=Fri, 31 Dec 2025 23:59:59 GMT

# Step 2: Browser stores it automatically

# Step 3: Browser sends it on every request to that domain
GET /profile HTTP/1.1
Cookie: session_id=abc123    ← browser adds this automatically
```

**Cookie vs Header — key difference:**

| | Cookie | Header |
|---|---|---|
| Who sets it | Server (via Set-Cookie) | Client or Server manually |
| Who sends it | Browser sends automatically | You must add it manually in code |
| Stored where | Browser storage | Not stored — only in that request |
| Use case | Sessions, preferences, tracking | Auth tokens, content type, cache |

```python
import requests

# Header — you add it manually every time
response = requests.get(
    "https://api.example.com/profile",
    headers={"Authorization": "Bearer mytoken123"}  # you write this
)

# Cookie — browser/requests handles automatically once set
session = requests.Session()
session.get("https://example.com/login")   # server sets cookie
session.get("https://example.com/profile") # cookie sent automatically
```

> **Why it matters:** Cookie vs token-based auth is a real architectural decision. Understanding both is expected in any backend role.

---

### 3. How does HTTPS work — and why can't you just use HTTP everywhere?

**The Problem with HTTP:**
HTTP sends everything as plain text. Anyone between you and the server can read it — passwords, card numbers, everything.

```
# HTTP — no encryption (dangerous)
Your laptop → [WiFi router] → [ISP] → Server
              ↑ Anyone here can read: "password=1234"

# HTTPS — encrypted (safe)
Your laptop → [WiFi router] → [ISP] → Server
              ↑ Anyone here sees: "x7k#mQ2!@p..." (useless)
```

**How HTTPS works (TLS Handshake — simplified):**

```
Step 1: Your browser visits https://bank.com
Step 2: Server sends its SSL Certificate
        (contains server's public key + proof it's really bank.com)
Step 3: Browser verifies the certificate with a trusted authority (CA)
Step 4: Browser and server agree on a shared secret key
Step 5: All further communication is encrypted with that key

# Like this:
Browser: "Here's a locked box, only you have the key"
Server:  "Got it. Here's a message locked with your key"
Browser: "Now we both have a shared secret — let's talk privately"
```

> **Why it matters:** Google ranks HTTPS sites higher. Browsers show "Not Secure" for HTTP. Every production app uses HTTPS — you should know why.

---

### 4. Why does caching exist in HTTP — and how does Cache-Control work?

**The Problem:**
Every request hits the server. If 10,000 users request the same homepage, the server does the same work 10,000 times — slow and expensive.

**How Caching fixes it:**
Store the response. Reuse it instead of asking the server again.

```
# Without cache:
User 1 → Server → generates response → sends it
User 2 → Server → generates response → sends it (same thing again!)
User 3 → Server → generates response → sends it (same thing again!)

# With cache:
User 1 → Server → generates response → stores it in cache → sends it
User 2 → Cache → sends stored response (server not involved!)
User 3 → Cache → sends stored response (server not involved!)
```

**How Cache-Control header controls it:**

```
# Server sends this in the response:

Cache-Control: max-age=3600
# Browser can cache this response for 3600 seconds (1 hour)
# For 1 hour, browser doesn't ask server again

Cache-Control: no-cache
# Always ask server — but server can say "nothing changed" (304)

Cache-Control: no-store
# Never cache this — for sensitive data (banking pages, user data)

Cache-Control: public
# Anyone can cache this (browsers, CDNs) — for public pages

Cache-Control: private
# Only the user's browser can cache — not shared CDNs
```

> **Why it matters:** Caching is why websites feel fast. Wrong cache settings = users seeing stale data or sensitive data leaking to wrong users.

---

## API Architecture

---

### 5. Monolithic vs Microservices — why companies migrate, and how services communicate

**Monolithic — everything in one app:**

```
# One big Django app handles everything:
[User Login] [Product Catalog] [Orders] [Payments] [Notifications]
      ↓               ↓           ↓          ↓            ↓
                  All in ONE codebase, ONE deployment

# Problem: Scale
If orders spike on Diwali → you must scale the ENTIRE app
Even though only the Orders part is busy
```

**Microservices — each feature is its own service:**

```
# Separate services, each deployed independently:
User Service    → handles login, profiles
Product Service → handles catalog, search
Order Service   → handles cart, orders
Payment Service → handles transactions
Email Service   → handles notifications

# Now on Diwali:
Order Service gets 10x traffic → scale ONLY Order Service
Other services unchanged → saves cost
```

**How Microservices communicate:**

```
# Option 1: REST API (synchronous — waits for response)
Order Service → POST /payments → Payment Service
                              ← 200 OK (then continues)

# Option 2: Message Queue like RabbitMQ/Kafka (asynchronous — fire and forget)
Order Service → publishes "order_placed" event → Queue
                                    Payment Service reads from queue and processes
# Order Service doesn't wait — faster, more resilient
```

| | Monolithic | Microservices |
|---|---|---|
| Good for | Small teams, early stage | Large teams, scaling |
| Deployment | One app | Many services |
| Failure | One bug crashes all | Only that service fails |
| Complexity | Low | High |

> **Why it matters:** Every tech interview at a product company touches this. Flipkart, Swiggy, Zomato all migrated from monolithic to microservices as they scaled.

---

### 6. Why was GraphQL created — and how does it solve REST's over-fetching problem?

**REST's two problems:**

```
# Problem 1: Over-fetching
# You need only the user's name. REST gives you everything.
GET /users/1
← {
    "id": 1,
    "name": "Alice",        ← you needed this
    "age": 25,              ← didn't need this
    "address": {...},       ← didn't need this
    "purchase_history": [], ← didn't need this
    "preferences": {...}    ← didn't need this
  }
# Wasted bandwidth — especially bad on mobile

# Problem 2: Under-fetching
# You need user + their orders. Takes 2 separate API calls.
GET /users/1       → get user
GET /users/1/orders → get their orders (second trip to server)
```

**How GraphQL solves both:**

```graphql
# You ask for EXACTLY what you need — in ONE request
query {
  user(id: 1) {
    name          # only this field
    orders {      # and their orders — all in one call
      id
      total
    }
  }
}

# Response has exactly what you asked — nothing extra
{
  "user": {
    "name": "Alice",
    "orders": [{"id": 101, "total": 500}]
  }
}
```

> **Why it matters:** GraphQL is used by Facebook, GitHub, Shopify. For mobile apps where bandwidth matters, it's a big deal. Knowing the "why" behind it is what interviewers want.

---

### 7. Why do APIs need versioning — and how is it done?

**The Problem:**
You change your API. Old apps using your API break. You can't force every user to update immediately.

```
# Scenario:
v1 of your API returns:
{"name": "Alice Smith"}

You decide to split it:
{"first_name": "Alice", "last_name": "Smith"}

# Every app that uses name: response.name will now crash
# You can't just change it — you need versioning
```

**How versioning is done:**

```
# Method 1: URL versioning (most common, most visible)
https://api.myapp.com/v1/users    ← old version, still works
https://api.myapp.com/v2/users    ← new version with breaking changes

# Method 2: Header versioning
GET /users
API-Version: 2    ← version sent in header, URL stays clean

# Method 3: Query parameter
GET /users?version=2
```

```python
# In Django/FastAPI — URL versioning example:
# urls.py

urlpatterns = [
    path("v1/users/", v1_views.UserListView.as_view()),  # old
    path("v2/users/", v2_views.UserListView.as_view()),  # new — different response format
]
```

> **Why it matters:** Every public API (Stripe, Razorpay, Twilio) uses versioning. Breaking changes without versioning = angry developers = lost users.

---

### 8. Why use API Gateways — and how do they sit between client and services?

**The Problem:**
In microservices, you have 10 services. Should the mobile app know all 10 URLs? Should each service handle auth, rate limiting, logging separately?

**What an API Gateway does:**
Single entry point for all requests. Handles the common stuff so each service doesn't have to.

```
# Without API Gateway — messy:
Mobile App → User Service (port 8001) — handles its own auth
Mobile App → Product Service (port 8002) — handles its own auth
Mobile App → Order Service (port 8003) — handles its own auth
# App knows all URLs. Auth logic repeated everywhere.

# With API Gateway — clean:
Mobile App → API Gateway (one URL)
                ↓ routes to:
                → User Service
                → Product Service
                → Order Service

# Gateway handles:
# ✅ Authentication (check token once, not in every service)
# ✅ Rate limiting (max 100 requests/minute per user)
# ✅ Logging (one place to see all traffic)
# ✅ Load balancing
# ✅ SSL termination
```

```
# Real tools used as API Gateways:
- AWS API Gateway
- Kong
- Nginx (can act as one)
- Traefik
```

> **Why it matters:** Any company with microservices uses a gateway. It's a common architecture diagram question in interviews.

---

### 9. How does a Load Balancer work — and why is it needed?

**The Problem:**
One server can only handle so many requests. When traffic spikes, it crashes.

**How Load Balancer fixes it:**
Spreads incoming requests across multiple servers so no single server gets overwhelmed.

```
# Without Load Balancer:
1000 users → Server 1 → 💥 overloaded, crashes

# With Load Balancer:
1000 users → Load Balancer → Server 1 (333 users)
                           → Server 2 (333 users)
                           → Server 3 (334 users)
# Each server handles manageable load
```

**How it distributes requests:**

```
# Strategy 1: Round Robin (default)
Request 1 → Server 1
Request 2 → Server 2
Request 3 → Server 3
Request 4 → Server 1 (back to start)
# Simple rotation

# Strategy 2: Least Connections
New request → goes to whichever server has fewest active connections
# Smarter — doesn't send to a busy server

# Strategy 3: IP Hash
Same user IP → always goes to same server
# Useful when server stores session data
```

> **Why it matters:** High availability and scalability questions always involve load balancers. Nginx and AWS ELB are the most common ones you'll encounter.

---

### 10. Why do APIs need Rate Limiting — and how is it implemented?

**The Problem:**
Without limits, one bad actor can send millions of requests and crash your server. Or a buggy app in an infinite loop destroys your database.

```
# Attack scenario without rate limiting:
Attacker → 1,000,000 requests in 1 minute → Server crashes → Everyone's affected
```

**How Rate Limiting works:**

```
# Rule: Max 100 requests per minute per user

Request 1-100:  → 200 OK  (within limit)
Request 101:    → 429 Too Many Requests  (limit hit)

# Response includes helpful headers:
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 100          ← your allowed limit
X-RateLimit-Remaining: 0        ← how many left
X-RateLimit-Reset: 1704067200   ← when the limit resets (unix timestamp)
Retry-After: 60                 ← wait 60 seconds
```

**How it's implemented:**

```python
# Using a counter stored in Redis (fast in-memory database)

# Pseudocode logic:
def is_rate_limited(user_id):
    key = f"rate_limit:{user_id}"           # unique key per user
    count = redis.get(key) or 0             # how many requests so far

    if count >= 100:                        # limit reached
        return True                         # block this request

    redis.incr(key)                         # increment counter
    redis.expire(key, 60)                   # reset after 60 seconds
    return False                            # allow this request
```

> **Why it matters:** Every production API has rate limiting. Stripe, Twitter, Google Maps all use it. 429 is a status code every developer encounters.

---

## REST & Design

---

### 11. Why is idempotency important — and which HTTP methods are idempotent?

**What idempotent means:**
Calling the same request **multiple times** gives the **same result** as calling it once. No extra side effects.

```
# Idempotent — safe to retry:
GET /users/1    → Always returns the same user. Call it 10 times = same result.
PUT /users/1    → Replaces user with same data. Call it 10 times = still same result.
DELETE /users/1 → First call deletes. Next 9 calls return 404. State doesn't change further.

# NOT idempotent — dangerous to retry:
POST /orders    → Creates a NEW order each time.
                  Call it 5 times = 5 duplicate orders 😱
```

**Why it matters in real systems:**

```
# Scenario: Payment API
User clicks "Pay" → request sent → network timeout → did it go through?

# If payment API is idempotent:
App retries safely → server sees it's the same request → processes once → no double charge

# How: Send a unique Idempotency-Key header
POST /payments
Idempotency-Key: order-456-attempt-1   ← server remembers this key
{"amount": 500}

# Second retry with same key:
POST /payments
Idempotency-Key: order-456-attempt-1   ← same key
← Server says "I already processed this" → returns original response, no double charge
```

| Method | Idempotent? |
|--------|------------|
| GET | ✅ Yes |
| PUT | ✅ Yes |
| DELETE | ✅ Yes |
| POST | ❌ No |
| PATCH | ❌ Not guaranteed |

> **Why it matters:** Payment systems, order systems — all use idempotency keys to handle network failures safely. Stripe's entire API is built around this.

---

### 12. Why use JWT tokens over session-based auth — and how does JWT work internally?

**Session-based auth (old way):**

```
Login → Server creates session, stores in database → gives you a session_id
Every request → server looks up session_id in database → slow at scale

# Problem: 1 million users = 1 million database lookups per request
# Problem: Multiple servers need to share session database
```

**JWT (JSON Web Token) — new way:**

```
Login → Server creates a TOKEN with your info baked in → gives you the token
Every request → server READS the token (no database lookup needed) → fast

# Token is self-contained — server doesn't store anything
```

**How JWT looks internally:**

```
# JWT = 3 parts separated by dots:
eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOjF9.abc123signature

Part 1: Header (base64 encoded)
{"alg": "HS256", "typ": "JWT"}        ← algorithm used

Part 2: Payload (base64 encoded)
{"userId": 1, "role": "admin", "exp": 1704067200}  ← your data + expiry

Part 3: Signature
HMAC_SHA256(header + payload, SECRET_KEY)  ← proves it wasn't tampered with
```

```python
import jwt  # pip install PyJWT

SECRET = "your-secret-key"

# Create token (on login):
token = jwt.encode(
    {"userId": 1, "role": "admin"},
    SECRET,
    algorithm="HS256"
)

# Verify token (on every request):
try:
    data = jwt.decode(token, SECRET, algorithms=["HS256"])
    print(data)  # {"userId": 1, "role": "admin"} — no DB lookup needed
except jwt.ExpiredSignatureError:
    print("Token expired, please login again")
except jwt.InvalidTokenError:
    print("Tampered token — rejected")
```

> **Why it matters:** Every modern API uses JWT. The "no database lookup" benefit is why it scales better than sessions.

---

### 13. How does OAuth2 work — and why do apps use "Login with Google"?

**The Problem it solves:**
You want to use an app. The app needs your Google profile. Should you give the app your Google password? **No.**

**How OAuth2 works — simple flow:**

```
# "Login with Google" flow:

1. You click "Login with Google" on MyApp

2. MyApp redirects you to Google:
   https://accounts.google.com/oauth/authorize
   ?client_id=myapp123
   &redirect_uri=https://myapp.com/callback
   &scope=email profile          ← what MyApp is asking for

3. Google shows you a consent screen:
   "MyApp wants access to your email and profile. Allow?"

4. You click Allow

5. Google redirects back to MyApp with a CODE:
   https://myapp.com/callback?code=abc123

6. MyApp exchanges the code for an ACCESS TOKEN (server-to-server):
   POST https://oauth2.googleapis.com/token
   {code: "abc123", client_secret: "mysecret"}
   ← Google returns: {"access_token": "ya29.xyz..."}

7. MyApp uses access token to get your profile:
   GET https://www.googleapis.com/oauth2/userinfo
   Authorization: Bearer ya29.xyz...
   ← {"email": "alice@gmail.com", "name": "Alice"}

8. You're logged in — MyApp never saw your Google password
```

> **Why it matters:** OAuth2 is everywhere — Login with Google, GitHub, Facebook. Understanding the flow is asked in almost every backend interview.

---

### 14. Why do APIs need pagination — and how is it implemented?

**The Problem:**
Your database has 1 million users. User requests `GET /users`. Do you send all 1 million records? No — that would crash the server and the client.

**How pagination is implemented:**

```
# Method 1: Limit/Offset (most common, simplest)
GET /users?limit=10&offset=0   → users 1–10   (page 1)
GET /users?limit=10&offset=10  → users 11–20  (page 2)
GET /users?limit=10&offset=20  → users 21–30  (page 3)

# Response includes pagination metadata:
{
  "data": [...10 users...],
  "total": 1000000,      ← total records available
  "limit": 10,
  "offset": 0,
  "next": "/users?limit=10&offset=10"  ← link to next page
}
```

```python
# Django example:
from django.core.paginator import Paginator

def get_users(request):
    limit = int(request.GET.get("limit", 10))   # default 10 per page
    offset = int(request.GET.get("offset", 0))  # default start from beginning

    all_users = User.objects.all()              # get all (query not executed yet)
    page_users = all_users[offset:offset+limit] # slice — only fetches this page from DB

    return JsonResponse({"data": list(page_users.values()), "total": all_users.count()})
```

```
# Method 2: Cursor-based (better for real-time data)
GET /posts?cursor=post_id_500&limit=10
← Returns 10 posts after post 500

# Why cursor is better than offset for live feeds:
# New post added while you're paginating? Offset shifts → you skip or see duplicates
# Cursor stays fixed to a specific record — no shifting
```

> **Why it matters:** Every list endpoint needs pagination. Sending all records at once is a beginner mistake that kills performance.

---

## Server Interfaces

---

### 15. Why can't Django's dev server run in production — and how does Gunicorn fix that?

**Django's dev server — what it actually is:**

```python
# When you run:
python manage.py runserver

# Django starts a simple single-threaded server
# It can handle ONE request at a time
# While processing Request 1, Request 2 must wait

# It also:
# ❌ Has no worker management
# ❌ Restarts on every code change (fine for dev, wrong for prod)
# ❌ Has no process monitoring (if it crashes, it stays crashed)
# ❌ Cannot handle concurrent users
# ❌ Django docs literally say: "Don't use this in production"
```

**How Gunicorn fixes it:**

```bash
# Gunicorn starts multiple worker processes:
gunicorn myproject.wsgi:application --workers 4 --bind 0.0.0.0:8000

# Now you have 4 workers — 4 requests handled simultaneously
# Worker 1: handles user A's request
# Worker 2: handles user B's request
# Worker 3: handles user C's request
# Worker 4: handles user D's request

# Rule of thumb for workers:
# workers = (2 × CPU cores) + 1
# 2 core machine → 5 workers
```

```
# Production stack:

Internet
   ↓
Nginx (port 80/443)
   → Serves static files (CSS, JS, images) directly — fast
   → Forwards API requests to Gunicorn
   ↓
Gunicorn (port 8000)
   → Worker 1
   → Worker 2
   → Worker 3
   ↓
Django App
   ↓
Database
```

> **Why it matters:** Every Django deployment uses this stack. Being able to explain it confidently is a green flag for any backend internship.

---

### 16. Why does FastAPI outperform Django on benchmarks — and how does async help?

**Synchronous (Django default) — one at a time:**

```python
# Django view — synchronous
def get_user(request, user_id):
    user = User.objects.get(id=user_id)   # waits for DB (e.g., 50ms)
    # During this 50ms wait, this worker does NOTHING
    # Other requests queue up
    return JsonResponse({"name": user.name})
```

**Asynchronous (FastAPI) — does other work while waiting:**

```python
# FastAPI view — asynchronous
async def get_user(user_id: int):
    user = await db.fetch_one(query, user_id)
    # "await" means: while DB is thinking (50ms), go handle other requests
    # Come back when DB responds
    return {"name": user.name}

# Result: same server handles 10x more requests
# Because it's not sitting idle during DB/network waits
```

```
# Sync — worker sits idle during I/O:
Request 1: [DB wait 50ms...] [process 5ms] → done
Request 2:                                  [DB wait 50ms...] [process 5ms] → done
# Total: 110ms, 1 worker was idle most of the time

# Async — worker stays busy:
Request 1: [DB wait...
Request 2:            DB wait...
Request 3:                       DB wait...]
All DB responses come back → processed → done
# Total: ~55ms, same worker handled 3 requests
```

> **Why it matters:** For I/O-heavy work (API calls, DB queries), async is dramatically faster. FastAPI is the go-to choice for ML model serving APIs exactly because of this.

---

### 17. How does Nginx sit in front of Gunicorn — and why is that combination used?

**Why not just expose Gunicorn directly to the internet?**

```
# Gunicorn alone — exposed directly:
❌ No SSL handling (HTTPS)
❌ No static file serving (images, CSS, JS)
❌ No compression (gzip)
❌ No DDoS protection
❌ No request buffering (slow clients tie up Gunicorn workers)
```

**What each one does best:**

```
Nginx is great at:
✅ Handling thousands of connections simultaneously (event-driven, very fast)
✅ Serving static files directly (without touching Python at all)
✅ SSL termination (handles HTTPS encryption/decryption)
✅ Gzip compression
✅ Buffering slow clients

Gunicorn is great at:
✅ Running Python code
✅ Managing worker processes
✅ Handling Django/Flask logic
```

```nginx
# Nginx config — simplified example:
server {
    listen 80;
    server_name myapp.com;

    # Serve static files directly — never goes to Gunicorn
    location /static/ {
        root /home/ubuntu/myproject;   # files served from disk directly
    }

    # Everything else → forward to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;  # Gunicorn running locally
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;  # pass real user IP to Django
    }
}
```

> **Why it matters:** This is the standard Django production setup. Any DevOps or backend deployment question will involve this pair.

---

### 18. Why use WebSockets over HTTP for chat apps — and how does the connection stay open?

**HTTP — not designed for real-time:**

```
# HTTP polling (old way to fake real-time):
Client: "Any new messages?" → Server: "No"
Client: "Any new messages?" → Server: "No"
Client: "Any new messages?" → Server: "Yes! Here's a message"
Client: "Any new messages?" → Server: "No"

# You're making a new connection every second
# 1000 users = 1000 requests/second just for "any updates?"
# Wasteful and still has delay
```

**WebSocket — true real-time, two-way:**

```
# WebSocket connection:
Step 1: Client sends HTTP request with upgrade request:
GET /chat HTTP/1.1
Upgrade: websocket
Connection: Upgrade

Step 2: Server agrees — connection upgrades:
HTTP/1.1 101 Switching Protocols
Upgrade: websocket

Step 3: Connection stays OPEN — both sides can send anytime:
Client → Server: "Hello!"           (no new connection needed)
Server → Client: "Hi there!"        (server pushes instantly)
Server → Client: "Alice joined"     (server pushes without client asking)
Client → Server: "Bye"
Connection closes when either side disconnects
```

```python
# FastAPI WebSocket example — simple chat:
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()      # upgrade the connection

    while True:                   # keep connection open
        message = await websocket.receive_text()        # wait for message from client
        await websocket.send_text(f"You said: {message}")  # reply instantly
```

| | HTTP | WebSocket |
|---|---|---|
| Connection | New one per request | One persistent connection |
| Direction | Client → Server only | Both directions (full-duplex) |
| Real-time | No (polling workaround) | Yes (instant push) |
| Use case | REST APIs, web pages | Chat, live scores, trading |

> **Why it matters:** Chat apps, live cricket scores, stock tickers, multiplayer games — all use WebSockets. Knowing when to use it vs REST is a solid interview answer.

---

*Good luck with the interview!*
