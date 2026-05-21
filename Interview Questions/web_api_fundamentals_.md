# Web & API Fundamentals – 20 Intern/Fresher Interview Questions

---

## 1. What is HTTP and how does it work?

**Answer:**
HTTP (HyperText Transfer Protocol) is the language browsers and servers use to talk to each other. It works on a simple **request → response** cycle.

```
Browser                          Server
  |                                |
  |  -- GET /home HTTP/1.1 -->     |   (you ask for a page)
  |                                |
  |  <-- 200 OK + HTML content --  |   (server sends it back)
  |                                |
```

1. You type a URL in the browser.
2. Browser sends an HTTP **request** to the server.
3. Server processes it and sends back an HTTP **response**.
4. Browser displays the result.

> **Why it matters:** Every API call, every webpage load — all of it is HTTP. You can't work in web development without understanding this flow.

---

## 2. What are the different HTTP versions and how do they differ?

**Answer:**

| Version  | Key Difference |
|----------|---------------|
| HTTP/1.0 | One request per connection — slow |
| HTTP/1.1 | Keeps connection alive, can reuse it — most common |
| HTTP/2   | Sends multiple requests at once on same connection (multiplexing) — faster |
| HTTP/3   | Built on UDP instead of TCP — even faster, used by Google/YouTube |

> **Why it matters:** Interviewers ask this to check if you understand *why* the web got faster over time — not just that it did.

---

## 3. What is the difference between GET, POST, PUT, and DELETE?

**Answer:**
These are HTTP **methods** — they tell the server *what action* you want to perform.

| Method | Purpose | Has Body? |
|--------|---------|-----------|
| GET    | Read/fetch data | No |
| POST   | Create new data | Yes |
| PUT    | Update/replace existing data | Yes |
| DELETE | Delete data | No |

```
# Think of it like a to-do list app:

GET    /tasks        → fetch all tasks
GET    /tasks/1      → fetch task with id=1
POST   /tasks        → create a new task (send data in body)
PUT    /tasks/1      → update task with id=1 (send updated data in body)
DELETE /tasks/1      → delete task with id=1
```

> **Why it matters:** This is one of the most asked fresher questions. GET is safe and idempotent (calling it 10 times has the same result). POST creates something new each time.

---

## 4. What are HTTP Status Codes? Name the most important ones.

**Answer:**
Status codes tell you **what happened** with your request. They're grouped by the first digit.

| Range | Meaning | Example |
|-------|---------|---------|
| 2xx | Success | 200 OK, 201 Created |
| 3xx | Redirect | 301 Moved Permanently |
| 4xx | Client error (you did something wrong) | 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found |
| 5xx | Server error (server did something wrong) | 500 Internal Server Error |

```
# Real-world examples:

200 → Request worked fine, here's your data
201 → New record was created successfully (after POST)
400 → You sent bad data (e.g., missing required field)
401 → You're not logged in
403 → You're logged in but don't have permission
404 → That resource doesn't exist
500 → Something crashed on the server — not your fault
```

> **Why it matters:** When debugging APIs, status codes tell you instantly *where* the problem is — your code (4xx) or the server (5xx).

---

## 5. What are HTTP Headers and what do they carry?

**Answer:**
Headers are **extra information** sent along with a request or response — like metadata. They travel in the background, not visible in the URL or body.

```
# Example Request Headers (sent by browser/client):

GET /profile HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOi...   ← your login token
Content-Type: application/json         ← telling server you're sending JSON
Accept: application/json               ← telling server you want JSON back

# Example Response Headers (sent by server):

HTTP/1.1 200 OK
Content-Type: application/json        ← server confirms it's sending JSON
Cache-Control: max-age=3600           ← browser can cache this for 1 hour
Set-Cookie: session_id=abc123         ← server sets a cookie
```

Common headers to know:
- `Authorization` — sends login token
- `Content-Type` — format of the data being sent
- `Accept` — format the client wants in response
- `Cache-Control` — how long to cache the response

> **Why it matters:** Auth tokens, content format, CORS errors — all controlled via headers. You'll deal with them on day one.

---

## 6. What is an API? Explain it simply.

**Answer:**
API (Application Programming Interface) is a **messenger** between two systems. It lets your app talk to another app without knowing how it works internally.

```
Real-world analogy:

You (customer) → Waiter (API) → Kitchen (server)

You don't go into the kitchen.
You tell the waiter what you want.
The waiter brings back your food.

In tech:
Your App → API → Database/Another Service
```

```python
import requests

# Your app asking a weather API for data
response = requests.get("https://api.weather.com/current?city=Delhi")

# You don't know HOW they get the weather data
# You just get the answer
print(response.json())  # {'temp': 32, 'condition': 'Sunny'}
```

> **Why it matters:** Every modern app uses APIs — login with Google, payments via Razorpay, maps from Google Maps. APIs are everywhere.

---

## 7. What are the different types of APIs?

**Answer:**

| Type | Description | Used When |
|------|-------------|-----------|
| REST | Uses HTTP methods, returns JSON | Most web/mobile apps |
| SOAP | Uses XML, older, strict rules | Banking, enterprise systems |
| GraphQL | Client asks for exactly what it needs | Apps that need flexible queries |
| WebSocket | Two-way real-time connection | Chat apps, live dashboards |
| gRPC | Binary protocol, very fast | Microservices, internal services |

```
# REST — Most common, simple
GET https://api.example.com/users/1
← Returns: {"id": 1, "name": "Alice"}

# GraphQL — You control what fields you get
query {
  user(id: 1) {
    name    # Only ask for name, not everything
  }
}
```

> **Why it matters:** As a fresher, you'll mostly deal with REST. But knowing GraphQL exists shows awareness of the ecosystem.

---

## 8. What is the difference between Monolithic and API-based architecture?

**Answer:**

**Monolithic** — Everything (UI, logic, database) is one big single application.

**API-based (Microservices)** — Each part is a separate service that talks to others via APIs.

```
# Monolithic — one big app
[Login + Products + Orders + Payments + Notifications]
      → All in one codebase, one deployment

# API-based — separate services
[Login Service]  →  API
[Product Service] → API     All connected via APIs
[Order Service]  →  API
[Payment Service] → API

# Real example: Zomato
- User Service API: handles login
- Restaurant API: handles restaurant data
- Order API: handles order tracking
- Payment API: handles payments
```

| | Monolithic | API-based |
|---|---|---|
| Easy to start | ✅ Yes | ❌ Complex |
| Easy to scale | ❌ Hard | ✅ Scale only what's needed |
| One crash breaks all | ✅ Yes | ❌ Only that service crashes |

> **Why it matters:** Most startups start monolithic, then break into APIs as they grow. You'll hear both terms in any backend discussion.

---

## 9. What is REST and what are RESTful principles?

**Answer:**
REST (Representational State Transfer) is a **set of rules** for designing APIs. An API following these rules is called RESTful.

**6 REST principles:**

```
1. CLIENT-SERVER
   Frontend and backend are separate — they only talk via API.

2. STATELESS
   Server doesn't remember your previous request.
   Every request must carry all needed info (like your auth token).

3. UNIFORM INTERFACE
   Use standard HTTP methods (GET, POST, PUT, DELETE).
   URLs represent resources: /users, /orders/1

4. CACHEABLE
   Responses can be cached to improve speed.

5. LAYERED SYSTEM
   Client doesn't know if it's talking to the real server
   or a proxy/load balancer in between.

6. CODE ON DEMAND (optional)
   Server can send executable code (like JavaScript) to the client.
```

```
# Good RESTful URL design:

GET    /users          → get all users
GET    /users/5        → get user with id 5
POST   /users          → create new user
PUT    /users/5        → update user 5
DELETE /users/5        → delete user 5

# Bad (not RESTful):
GET /getUser?id=5      ← action in URL, wrong style
POST /deleteUser/5     ← wrong method for delete
```

> **Why it matters:** RESTful design is the industry standard. Interviewers check if you can design clean URLs and use the right HTTP methods.

---

## 10. What does "stateless" mean in REST?

**Answer:**
Stateless means the **server does not remember you** between requests. Every request you send must include everything the server needs — especially your identity (token).

```
# Stateful (old way — server remembers you):
Request 1: Login → Server stores "User 5 is logged in"
Request 2: Get profile → Server checks its memory, finds User 5

# Stateless (REST way — you carry your identity):
Request 1: Login → Server gives you a TOKEN
Request 2: Get profile → You send TOKEN in every request header
           Server reads the token, figures out who you are — no memory needed

# In code:
headers = {
    "Authorization": "Bearer eyJhbGciOi..."  # Token sent every time
}
response = requests.get("https://api.example.com/profile", headers=headers)
```

> **Why it matters:** Stateless APIs are easier to scale — any server can handle any request because no session memory is needed.

---

## 11. What is the difference between REST and SOAP?

**Answer:**

| | REST | SOAP |
|---|---|---|
| Data format | JSON (mostly) | XML only |
| Speed | Faster, lightweight | Slower, heavy |
| Complexity | Simple | Complex, strict rules |
| Used in | Web apps, mobile apps | Banking, enterprise, legacy |
| Protocol | HTTP | HTTP, SMTP, others |

```xml
<!-- SOAP Request — very verbose XML -->
<soap:Envelope>
  <soap:Body>
    <GetUser>
      <UserId>5</UserId>
    </GetUser>
  </soap:Body>
</soap:Envelope>
```

```json
// REST Request — clean and simple
GET /users/5
← {"id": 5, "name": "Alice"}
```

> **Why it matters:** You'll almost never write SOAP as a fresher, but you need to know why REST replaced it in most modern systems.

---

## 12. What is JSON and why do APIs use it?

**Answer:**
JSON (JavaScript Object Notation) is the standard **format for sending data** between a client and server in REST APIs.

```python
# JSON looks like a Python dictionary
{
    "id": 1,
    "name": "Alice",
    "skills": ["Python", "Django"],   # arrays supported
    "address": {
        "city": "Delhi",              # nested objects supported
        "pin": "110001"
    },
    "active": true                    # boolean
}

# In Python, you convert between JSON and dict like this:
import json

# Dict → JSON string (to send over network)
data = {"name": "Alice", "age": 25}
json_string = json.dumps(data)        # '{"name": "Alice", "age": 25}'

# JSON string → Dict (after receiving from API)
received = '{"name": "Alice", "age": 25}'
parsed = json.loads(received)         # {'name': 'Alice', 'age': 25}
```

> **Why it matters:** Every REST API returns JSON. You'll parse JSON on your first day of any backend/data engineering job.

---

## 13. What is WSGI? Why does Django need it?

**Answer:**
WSGI (Web Server Gateway Interface) is a **standard** that lets Python web apps (Django, Flask) talk to web servers (like Nginx).

```
Without WSGI:
Nginx (web server) doesn't know how to run Python.

With WSGI:
Nginx → Gunicorn (WSGI server) → Django app

Nginx handles the internet traffic.
Gunicorn translates it into something Django understands.
Django processes and returns the response.
```

```
# Flow for a Django app in production:

User's Browser
     ↓
  Nginx (receives the request, serves static files)
     ↓
  Gunicorn (WSGI server — runs your Django app)
     ↓
  Django (your Python code processes the request)
     ↓
  Database (if needed)
     ↓
  Response goes back up the same chain
```

> **Why it matters:** WSGI is why you can't just run `python manage.py runserver` in production — that's only for development.

---

## 14. What is ASGI and how is it different from WSGI?

**Answer:**
ASGI (Asynchronous Server Gateway Interface) is the **modern upgrade to WSGI**. It supports async code, WebSockets, and real-time features that WSGI can't handle.

| | WSGI | ASGI |
|---|---|---|
| Type | Synchronous | Asynchronous |
| WebSockets | ❌ No | ✅ Yes |
| Real-time | ❌ No | ✅ Yes |
| Used with | Django (traditional), Flask | Django (Channels), FastAPI |
| Server | Gunicorn | Uvicorn |

```
# WSGI — handles one request at a time (synchronous)
Request 1 →  [Processing...] → Response 1
Request 2 →            [waits] → Response 2

# ASGI — handles multiple requests concurrently (asynchronous)
Request 1 →  [Processing...]
Request 2 →  [Processing...]   ← starts without waiting for Request 1
Request 3 →  [Processing...]
```

> **Why it matters:** If you're building chat, notifications, or live data — you need ASGI. FastAPI is fully ASGI, which is why it's so fast.

---

## 15. What is Gunicorn and what does it do?

**Answer:**
Gunicorn is a **WSGI server** for Python. It runs your Django/Flask app in production by creating multiple worker processes to handle many users at once.

```
# Development (single user, okay for testing):
python manage.py runserver   ← Django's built-in server, NOT for production

# Production (many users at same time):
gunicorn myproject.wsgi:application --workers 4

# --workers 4 means 4 parallel processes
# Each worker handles one request at a time
# 4 workers = handle 4 requests simultaneously
```

```
# How it sits in the stack:

Internet → Nginx (port 80/443) → Gunicorn (port 8000) → Django
                                    Worker 1
                                    Worker 2
                                    Worker 3
                                    Worker 4
```

> **Why it matters:** The moment you deploy a Django app, you'll use Gunicorn. It's on every backend job's deployment checklist.

---

## 16. What is Uvicorn and why is it used with FastAPI?

**Answer:**
Uvicorn is an **ASGI server** — the async equivalent of Gunicorn. FastAPI is async, so it needs Uvicorn to run.

```bash
# Running a FastAPI app with Uvicorn:
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# main     → your file name (main.py)
# app      → the FastAPI instance inside that file
# workers  → parallel processes
```

```python
# main.py — a simple FastAPI app
from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
async def hello():          # async function — needs ASGI server (Uvicorn)
    return {"message": "Hello World"}
```

| | Gunicorn | Uvicorn |
|---|---|---|
| Interface | WSGI | ASGI |
| Async support | ❌ | ✅ |
| Used with | Django, Flask | FastAPI, Django Channels |

> **Why it matters:** FastAPI is trending hard for data/ML APIs. Uvicorn is always part of that stack.

---

## 17. What is the difference between PUT and PATCH?

**Answer:**
Both update data, but:
- **PUT** — replaces the **entire** resource.
- **PATCH** — updates **only the fields you send**.

```
# Existing record in database:
{"id": 1, "name": "Alice", "age": 25, "city": "Delhi"}

# PUT — you must send ALL fields:
PUT /users/1
{"name": "Alice", "age": 26, "city": "Delhi"}
← Missing a field? It gets wiped out or set to null.

# PATCH — send only what changed:
PATCH /users/1
{"age": 26}
← Only age updates. name and city stay untouched.
```

> **Why it matters:** Using PUT when you meant PATCH can accidentally wipe fields. Common interview trap question.

---

## 18. What is an API Endpoint?

**Answer:**
An endpoint is a specific **URL where an API receives requests**. Think of it as a door — each door leads to a different room (action).

```
# Base URL:
https://api.myapp.com

# Endpoints (different doors):
https://api.myapp.com/users          ← door to user data
https://api.myapp.com/users/5        ← door to user 5 specifically
https://api.myapp.com/products       ← door to product data
https://api.myapp.com/orders/99      ← door to order 99

# Each endpoint + HTTP method = one specific action:
GET  /users        → list all users
POST /users        → create a user
GET  /users/5      → get user 5
PUT  /users/5      → update user 5
DELETE /users/5    → delete user 5
```

> **Why it matters:** When you build or consume an API, endpoints are the first thing you define or look up in documentation.

---

## 19. What is the difference between Authentication and Authorization?

**Answer:**
- **Authentication** — "Who are you?" → Verifying identity (login).
- **Authorization** — "What can you do?" → Checking permissions.

```
# Real-world analogy:
Authentication = Showing your ID card at a building entrance
Authorization  = Your ID card only opens certain floors, not all

# In an API:
Step 1: Authentication
POST /login
{"email": "alice@example.com", "password": "1234"}
← Server verifies → gives you a TOKEN

Step 2: Authorization
GET /admin/dashboard
Headers: {"Authorization": "Bearer <token>"}
← Server checks your token → are you an admin? 
   Yes → 200 OK
   No  → 403 Forbidden
```

```
# HTTP Status codes that match:
401 Unauthorized → Authentication failed (not logged in)
403 Forbidden    → Authenticated but not authorized (logged in, no permission)
```

> **Why it matters:** Every secure API has both. Mixing them up is a red flag in interviews.

---

## 20. What is CORS and why do you get a CORS error?

**Answer:**
CORS (Cross-Origin Resource Sharing) is a **browser security rule** that blocks requests from a different domain unless the server explicitly allows it.

```
# Origin = protocol + domain + port
http://localhost:3000  ← your React frontend
https://api.myapp.com  ← your Django backend

# These are DIFFERENT origins → browser blocks the request by default
# This is the CORS error you see in the console

# Fix: The SERVER must send this header in the response:
Access-Control-Allow-Origin: http://localhost:3000
# or allow all origins (not safe for production):
Access-Control-Allow-Origin: *
```

```python
# In Django — install and use django-cors-headers:
# settings.py

INSTALLED_APPS = [
    "corsheaders",   # add this
    ...
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # must be at the TOP
    ...
]

# Allow your frontend URL:
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",     # React dev server
    "https://myfrontend.com",    # production frontend
]
```

> **Why it matters:** Every fresher building a frontend + backend app hits CORS errors. Knowing why it happens (and that the fix is on the server side) separates you from those who just Google the error.

---

*Good luck with the interview!*
