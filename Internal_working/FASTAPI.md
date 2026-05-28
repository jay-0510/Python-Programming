# FastAPI 
### Domain: **Job Portal API** 

---
 
## Table of Contents
 
- [Mental Model — How an API Request Travels](#mental-model--how-an-api-request-travels)
- [01. What is an API? — The Foundation](#01-what-is-an-api--the-foundation)
- [02. HTTP Status Codes & Headers — The Server's Language](#02-http-status-codes--headers--the-servers-language)
- [03. FastAPI + Uvicorn Setup — Your First Endpoint](#03-fastapi--uvicorn-setup--your-first-endpoint)
- [04. Pydantic & Data Validation — The Type Safety Layer](#04-pydantic--data-validation--the-type-safety-layer)
- [05. ORM & Database Integration — Making Data Persist](#05-orm--database-integration--making-data-persist)
- [06. Authentication & Security — JWT + OAuth2](#06-authentication--security--jwt--oauth2)
- [07. Middleware — The Global Request Pipeline](#07-middleware--the-global-request-pipeline)
- [08. CORS — Letting the Frontend Talk to the Backend](#08-cors--letting-the-frontend-talk-to-the-backend)
- [09. Streaming Responses — The LLM Use Case](#09-streaming-responses--the-llm-use-case)
- [10. Async/Await — FastAPI's Performance Secret](#10-asyncawait--fastapis-performance-secret)
- [11. Error Handling — Production-Grade Responses](#11-error-handling--production-grade-responses)
- [12. Testing — Verifying Everything Works](#12-testing--verifying-everything-works)
- [13. Swagger / OpenAPI Documentation — Auto-Generated API Docs](#13-swagger--openapi-documentation--auto-generated-api-docs)
- [14. Final Architecture Diagram — System View](#14-final-architecture-diagram--system-view)
- [15. Interview Cheat Sheet — Theory Questions & Answers](#15-interview-cheat-sheet--theory-questions--answers)
---

---

## Mental Model — How an API Request Travels

Before writing a single line, burn this picture into your head:

```
[Client / Browser / Frontend]
        |
        |  HTTP Request (method + URL + headers + body)
        v
[Network / Internet]
        |
        v
[Uvicorn — ASGI Server]   ← the "door" that receives raw TCP packets
        |
        v
[Middleware Stack]         ← logging, auth checks, CORS, timing
        |
        v
[FastAPI Router]           ← matches URL path to Python function
        |
        v
[Pydantic Validation]      ← checks/converts the incoming data
        |
        v
[Your Route Function]      ← your business logic lives here
        |
        v
[Database / ML Model]      ← if needed
        |
        v
[Pydantic Serialization]   ← shapes the outgoing response
        |
        v
[HTTP Response]            ← JSON + status code + headers → back to client
```

This is the **request-response lifecycle**. Every topic in this guide maps to one layer of this diagram.

---

## 01. What is an API? — The Foundation

### Theory

An API (Application Programming Interface) is a **contract**. It says:

> "If you send me a request in *this* format, I will send back a response in *this* format."

Think of it like a restaurant menu:
- The **menu** is the API contract (what you can order and what you'll get)
- You (the client) place an **order** (HTTP request)
- The kitchen (server) prepares and delivers (HTTP response)
- You never enter the kitchen — the waiter (API) handles the boundary

**Why does it matter for AI/ML engineers?**  
Every model you train is useless until someone can call it. That "someone" calls it through an API. Your ML pipeline ends where the API begins.

### REST — The Rules of the Game

REST stands for **Representational State Transfer**. It's not a framework — it's a set of *rules*:

| Rule | What it means |
|------|---------------|
| **Stateless** | Each request carries everything the server needs. Server doesn't remember previous requests. |
| **Resource-based URLs** | URLs represent *things* (nouns), not *actions* (verbs). `/jobs` not `/getJobs` |
| **HTTP Methods as verbs** | The *action* is in the method: GET, POST, PUT, DELETE, PATCH |
| **Uniform Interface** | Same conventions everywhere — predictable for clients |

### HTTP Methods — The Verbs

| Method | Action | Example |
|--------|--------|---------|
| `GET` | Read / Fetch | Get all jobs |
| `POST` | Create | Post a new job |
| `PUT` | Full update | Replace a job completely |
| `PATCH` | Partial update | Update only the salary field |
| `DELETE` | Remove | Delete a job |

---

## 02. HTTP Status Codes & Headers — The Server's Language

### Theory

Status codes are how the server *communicates the outcome* without you parsing the response body.

```
1xx — Informational      (rare, don't worry about these)
2xx — Success            ← you want these
3xx — Redirection        (the resource moved somewhere)
4xx — Client Error       ← you (or the user) made a mistake
5xx — Server Error       ← something broke on the server side
```

### Critical Status Codes (Master These)

| Code | Name | When to use |
|------|------|-------------|
| `200` | OK | GET success, PUT success |
| `201` | Created | POST success — resource was created |
| `204` | No Content | DELETE success — nothing to return |
| `400` | Bad Request | Client sent malformed data |
| `401` | Unauthorized | No valid credentials provided |
| `403` | Forbidden | Credentials valid, but not allowed (different from 401!) |
| `404` | Not Found | Resource doesn't exist |
| `422` | Unprocessable Entity | FastAPI's default for validation errors |
| `500` | Internal Server Error | Unexpected server crash |

### HTTP Headers — The Metadata Envelope

Headers are **key-value pairs** sent alongside the request/response. They carry metadata — not the data itself.

```
Request Headers:
  Content-Type: application/json    ← "I'm sending JSON"
  Authorization: Bearer <token>     ← "Here's my identity"
  Accept: application/json          ← "I want JSON back"

Response Headers:
  Content-Type: application/json    ← "I'm returning JSON"
  Cache-Control: no-cache           ← "Don't cache this"
  X-Request-ID: abc123              ← custom tracking header
```

---

## 03. FastAPI + Uvicorn Setup — Your First Endpoint

### Theory

**FastAPI** is the framework — the set of tools you use to *define* your API.  
**Uvicorn** is the ASGI server — the engine that *runs* your API and listens for incoming connections.

**WSGI vs ASGI:**
- WSGI (Flask, Django) = synchronous, one request handled at a time per worker
- ASGI (FastAPI) = asynchronous, can handle thousands of concurrent connections with fewer resources

Think of WSGI as a single-lane road, ASGI as a multi-lane highway.

### Installation

```bash
pip install fastapi uvicorn sqlalchemy pydantic python-jose passlib bcrypt python-multipart
```

### First Endpoint — Job Portal v0.1

```python
# main.py
from fastapi import FastAPI

app = FastAPI(
    title="Job Portal API",
    description="An API to manage job listings and applications",
    version="0.1.0"
)

# The simplest possible endpoint
@app.get("/")
def root():
    """Health check — confirms the API is alive."""
    return {"message": "Job Portal API is running", "status": "healthy"}

@app.get("/jobs")
def list_jobs():
    """Return a hardcoded list of jobs (no DB yet)."""
    return [
        {"id": 1, "title": "Backend Engineer", "company": "TechCorp", "location": "Remote"},
        {"id": 2, "title": "Data Scientist", "company": "AI Labs", "location": "Bangalore"},
    ]
```

### Running the Server

```bash
uvicorn main:app --reload
```

- `main` = the Python file name (`main.py`)
- `app` = the FastAPI instance variable
- `--reload` = auto-restarts on code changes (development only, never in production)

### What to See on Swagger UI

Open `http://127.0.0.1:8000/docs`

You will see:
```
GET  /         Health check
GET  /jobs     Return a hardcoded list of jobs
```

Click `GET /jobs` → "Try it out" → "Execute"

You'll see the **curl command**, the **request URL**, and the **response body** with status `200`.

---

## 04. Pydantic & Data Validation — The Type Safety Layer

### Theory

Pydantic is **data validation using Python type hints**. It is the backbone of FastAPI.

Without Pydantic, a user could send:
```json
{"title": 12345, "salary": "free"}
```
...and your function would receive garbage.

With Pydantic:
1. User sends `{"title": 12345, "salary": "free"}`
2. Pydantic tries to coerce `12345` to a string (succeeds → `"12345"`)
3. Pydantic tries to parse `"free"` as a number (fails → returns `422` with an error message)
4. Your function is **never called** with invalid data

**Why is this so important for ML APIs?**  
When someone sends data to your model, you need to guarantee it's the right shape and type before it reaches the model. Pydantic handles this automatically.

### Request & Response Schema — v0.2

```python
# schemas.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

# ─── Job Schemas ───────────────────────────────────────────────────

class JobCreate(BaseModel):
    """Schema for creating a new job — input from the client."""
    title: str = Field(..., min_length=3, max_length=100, example="Software Engineer")
    company: str = Field(..., example="TechCorp India")
    location: str = Field(..., example="Surat, Gujarat")
    salary_lpa: float = Field(..., gt=0, description="Annual salary in Lakhs Per Annum")
    description: Optional[str] = Field(None, max_length=2000)
    is_remote: bool = False

class JobResponse(BaseModel):
    """Schema for returning a job to the client — output."""
    id: int
    title: str
    company: str
    location: str
    salary_lpa: float
    is_remote: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Allows reading from SQLAlchemy ORM objects

# ─── Application Schemas ───────────────────────────────────────────

class ApplicationCreate(BaseModel):
    applicant_name: str = Field(..., example="Rahul Shah")
    applicant_email: EmailStr  # Pydantic validates email format automatically!
    resume_url: Optional[str] = None
    cover_letter: Optional[str] = None

class ApplicationResponse(BaseModel):
    id: int
    job_id: int
    applicant_name: str
    applicant_email: str
    applied_at: datetime

    class Config:
        from_attributes = True
```

```python
# main.py — updated with Pydantic schemas
from fastapi import FastAPI, HTTPException
from schemas import JobCreate, JobResponse, ApplicationCreate, ApplicationResponse
from datetime import datetime
from typing import List

app = FastAPI(title="Job Portal API", version="0.2.0")

# In-memory "database" (we'll replace this with real DB in the next section)
jobs_db: dict = {}
job_counter: int = 0

@app.post("/jobs", response_model=JobResponse, status_code=201)
def create_job(job: JobCreate):
    """
    Create a new job listing.
    
    - Pydantic validates all fields before this function is called
    - response_model=JobResponse ensures we only return the fields we want
    - status_code=201 tells the client a resource was created
    """
    global job_counter
    job_counter += 1

    new_job = {
        "id": job_counter,
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "salary_lpa": job.salary_lpa,
        "description": job.description,
        "is_remote": job.is_remote,
        "created_at": datetime.utcnow()
    }
    jobs_db[job_counter] = new_job
    return new_job

@app.get("/jobs", response_model=List[JobResponse])
def list_jobs():
    """Return all job listings."""
    return list(jobs_db.values())

@app.get("/jobs/{job_id}", response_model=JobResponse)
def get_job(job_id: int):
    """
    Get a single job by ID.
    
    {job_id} is a path parameter — FastAPI extracts and validates it automatically.
    If job_id=abc is sent, FastAPI returns 422 before reaching this function.
    """
    if job_id not in jobs_db:
        raise HTTPException(status_code=404, detail=f"Job with id {job_id} not found")
    return jobs_db[job_id]
```

### What to See on Swagger UI

Now Swagger UI shows:
- **Schemas section** at the bottom: `JobCreate`, `JobResponse`, `ApplicationCreate`
- `POST /jobs` has a **Request Body** with all fields and their types/validations shown
- If you send `{"title": "A", "salary_lpa": -5}` you'll see a `422` error with **exactly which field failed and why**

---

## 05. ORM & Database Integration — Making Data Persist

### Theory

**ORM (Object-Relational Mapping)** = a way to interact with a database using Python objects instead of raw SQL.

Without ORM:
```python
cursor.execute("SELECT * FROM jobs WHERE id = %s", (job_id,))
row = cursor.fetchone()
# Now manually map row[0] → id, row[1] → title, etc.
```

With SQLAlchemy ORM:
```python
job = db.query(Job).filter(Job.id == job_id).first()
# job.id, job.title — clean Python object
```

**Key concepts:**
- **Engine**: The connection to the database (like a phone line)
- **Session**: A single conversation with the database (one transaction scope)
- **Model**: A Python class that maps to a database table
- **Depends()**: FastAPI's dependency injection — a way to share resources (like DB sessions) across routes

### Database Setup — v0.3

```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite for development (replace with postgresql://... for production)
DATABASE_URL = "sqlite:///./jobportal.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite-specific setting
)

# Each instance of SessionLocal is a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all our ORM models
Base = declarative_base()

# ─── Dependency: Provides a DB session to each route ───────────────
def get_db():
    """
    This is a generator function used as a FastAPI dependency.
    
    Flow:
    1. A request comes in
    2. FastAPI calls get_db() and gets a DB session
    3. The session is injected into your route function
    4. After the route finishes (or throws an error), the session is closed
    
    The 'finally' block guarantees the session is ALWAYS closed,
    even if an exception occurs — preventing connection leaks.
    """
    db = SessionLocal()
    try:
        yield db        # ← hand the session to the route function
    finally:
        db.close()      # ← always runs after the route is done
```

```python
# models.py
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    location = Column(String, nullable=False)
    salary_lpa = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    is_remote = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # One job can have many applications
    applications = relationship("Application", back_populates="job")

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    applicant_name = Column(String, nullable=False)
    applicant_email = Column(String, nullable=False)
    resume_url = Column(String, nullable=True)
    cover_letter = Column(String, nullable=True)
    applied_at = Column(DateTime, default=datetime.utcnow)

    job = relationship("Job", back_populates="applications")
```

```python
# main.py — v0.3 with real database
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import models, schemas
from database import engine, get_db

# Create all tables in the database on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Portal API", version="0.3.0")

@app.post("/jobs", response_model=schemas.JobResponse, status_code=201)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    """
    db: Session = Depends(get_db) is FastAPI's Dependency Injection.
    
    FastAPI sees Depends(get_db), calls get_db(), and injects the result
    into this function as 'db'. You don't call get_db() yourself.
    This pattern ensures DB sessions are properly managed.
    """
    db_job = models.Job(**job.model_dump())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)  # Refresh to get the generated id and created_at
    return db_job

@app.get("/jobs", response_model=list[schemas.JobResponse])
def list_jobs(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Query parameters: /jobs?skip=0&limit=10
    These are automatically read from the URL — not from the request body.
    """
    return db.query(models.Job).offset(skip).limit(limit).all()

@app.get("/jobs/{job_id}", response_model=schemas.JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.put("/jobs/{job_id}", response_model=schemas.JobResponse)
def update_job(job_id: int, job_data: schemas.JobCreate, db: Session = Depends(get_db)):
    """Full update — replaces all fields."""
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    for field, value in job_data.model_dump().items():
        setattr(job, field, value)

    db.commit()
    db.refresh(job)
    return job

@app.delete("/jobs/{job_id}", status_code=204)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    """
    204 No Content — success but no body to return.
    The job is gone; there's nothing meaningful to send back.
    """
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()
    return  # No return value needed for 204

@app.post("/jobs/{job_id}/apply", response_model=schemas.ApplicationResponse, status_code=201)
def apply_to_job(
    job_id: int,
    application: schemas.ApplicationCreate,
    db: Session = Depends(get_db)
):
    """Apply to a specific job. Combines path param + request body."""
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    db_application = models.Application(job_id=job_id, **application.model_dump())
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application
```

### System View: What Depends() Actually Does

```
Request arrives at POST /jobs
        |
        ├─ FastAPI sees: db: Session = Depends(get_db)
        |
        ├─ FastAPI calls get_db()
        |       ├─ SessionLocal() creates DB session
        |       └─ yield session → FastAPI gets it
        |
        ├─ FastAPI calls create_job(job=<validated_data>, db=<session>)
        |
        ├─ Function runs, DB operations happen
        |
        └─ FastAPI calls get_db()'s cleanup (db.close())
```

---

## 06. Authentication & Security — JWT + OAuth2

### Theory

**Authentication** = Who are you? (Identity)  
**Authorization** = What are you allowed to do? (Permissions)

**OAuth2 Password Flow** (what we'll use):
1. User sends `username` + `password` to `/auth/login`
2. Server verifies, generates a **JWT token**
3. User stores the token
4. For all future requests, user sends: `Authorization: Bearer <token>`
5. Server validates the token — if valid, processes the request

**JWT (JSON Web Token)** structure:
```
eyJhbGc...   .   eyJ1c2VyX2lk...   .   signature
   Header         Payload (claims)      Signature
   (algorithm)    (your data)           (proof of validity)
```

The payload is **base64-encoded, NOT encrypted**. Don't put passwords in it.  
The signature ensures the token hasn't been **tampered with**.

```python
# auth.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models
from database import get_db

# Secret key — in production, load from environment variable, NEVER hardcode!
SECRET_KEY = "your-super-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Handles password hashing and verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Tells FastAPI where clients send their token
# This enables the "Authorize" button on Swagger UI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def hash_password(password: str) -> str:
    """Never store plain text passwords. Always hash."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if a plain password matches a stored hash."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    """
    Create a JWT token.
    
    We embed 'sub' (subject = user identifier) and 'exp' (expiry time).
    The token is signed with SECRET_KEY — any tampering invalidates it.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> models.User:
    """
    Dependency used to protect routes.
    
    When a route has: current_user = Depends(get_current_user)
    FastAPI will:
    1. Extract the Bearer token from the Authorization header
    2. Decode and validate the JWT
    3. Load the user from the database
    4. Inject the user object into the route function
    5. Return 401 automatically if anything fails
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user
```

```python
# In main.py — add auth routes and protect job creation

from auth import hash_password, verify_password, create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm

@app.post("/auth/register", status_code=201)
def register(
    username: str,
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    """Register a new recruiter account."""
    existing = db.query(models.User).filter(models.User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(password)
    user = models.User(username=username, email=email, hashed_password=hashed)
    db.add(user)
    db.commit()
    return {"message": "User created successfully"}

@app.post("/auth/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    OAuth2PasswordRequestForm expects:
      Content-Type: application/x-www-form-urlencoded
      Body: username=foo&password=bar
    
    This is the standard OAuth2 format. Swagger UI's Authorize button
    sends data in exactly this format.
    """
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

# Protected route — only authenticated users can post jobs
@app.post("/jobs", response_model=schemas.JobResponse, status_code=201)
def create_job(
    job: schemas.JobCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # ← protection
):
    """Only logged-in recruiters can post jobs."""
    db_job = models.Job(**job.model_dump(), posted_by=current_user.id)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job
```

### What to See on Swagger UI

1. A **green "Authorize" button** appears at the top right
2. Click it → enter username and password → click Authorize
3. Swagger stores the token and sends it automatically with every request
4. Try `POST /jobs` without authorizing → you get `401 Unauthorized`
5. Authorize → try again → it works

---

## 07. Middleware — The Global Request Pipeline

### Theory

Middleware wraps **every single request** that passes through your API. It runs:
- **Before** the request reaches your route function (pre-processing)
- **After** your route returns a response (post-processing)

Use cases:
- Logging every request with timing
- Adding security headers to every response
- Rate limiting
- Custom authentication checks

```
Request → Middleware 1 → Middleware 2 → Route Function
Response ← Middleware 1 ← Middleware 2 ← Route Function
```

Middleware is like an **assembly line** — each station inspects and potentially modifies the item.

```python
# In main.py

import time
import logging
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ─── Timing + Logging Middleware ────────────────────────────────────
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    call_next is the "next thing in the pipeline" — either the next
    middleware, or the actual route function.
    
    We record time before and after, then log it.
    We also add a custom header to every response.
    """
    start_time = time.time()

    # Log the incoming request
    logger.info(f"-> {request.method} {request.url.path}")

    # Pass to next handler
    response = await call_next(request)

    # Log the outgoing response
    duration = round((time.time() - start_time) * 1000, 2)
    logger.info(f"<- {response.status_code} | {duration}ms")

    # Add custom response header visible in browser DevTools / Swagger
    response.headers["X-Process-Time-ms"] = str(duration)
    response.headers["X-API-Version"] = "0.4.0"

    return response
```

---

## 08. CORS — Letting the Frontend Talk to the Backend

### Theory

**CORS = Cross-Origin Resource Sharing**

By default, browsers **block** JavaScript from reading responses from a different origin.

```
Frontend: http://localhost:3000  (React app)
Backend:  http://localhost:8000  (FastAPI)

→ Different ports = different origins → Browser blocks the response
```

The browser does this to protect users. But when you *know* the frontend should be allowed, you configure CORS headers to explicitly permit it.

```
Client sends:           Origin: http://localhost:3000
Server responds with:   Access-Control-Allow-Origin: http://localhost:3000
Browser reads this:     "OK, I'll let the JS code see the response"
```

```python
# In main.py — add CORS middleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",     # React dev server
        "https://yourfrontend.com",  # Production frontend
    ],
    allow_credentials=True,         # Allow cookies/auth headers
    allow_methods=["*"],            # Allow all HTTP methods
    allow_headers=["*"],            # Allow all headers
)
```

**For development only:** You can use `allow_origins=["*"]` to allow all origins, but **never do this in production** for sensitive APIs.

---

## 09. Streaming Responses — The LLM Use Case

### Theory

Normal API flow:
```
Client ─── waits ────────────────────────── receives full response
                    [Server processes everything, then sends]
```

Streaming flow:
```
Client ─── receives chunk 1 ─ chunk 2 ─ chunk 3 ─ ... ─ done
                [Server sends data as it produces it]
```

**Why this matters for AI/ML:**  
When your model generates a long text response (like an LLM), you don't want the user to wait 30 seconds for the full output. You stream tokens as they're generated — exactly like ChatGPT's typing effect.

```python
# In main.py

import asyncio
from fastapi.responses import StreamingResponse
import json

@app.get("/jobs/{job_id}/ai-summary")
async def stream_job_summary(job_id: int, db: Session = Depends(get_db)):
    """
    Simulate streaming an AI-generated job summary.
    
    In a real ML API, you'd call your LLM here and stream its output.
    StreamingResponse + async generator = the pattern used by OpenAI,
    Anthropic, and every major LLM provider.
    """
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    async def generate_summary():
        """
        This is an async generator — it yields data piece by piece.
        Each yield sends a chunk to the client immediately.
        """
        summary_parts = [
            f"Analyzing job: **{job.title}** at {job.company}...\n",
            f"Location: {job.location}\n",
            f"Salary: Rs.{job.salary_lpa} LPA\n",
            "This role requires strong problem-solving skills. ",
            "Candidates should have experience with modern tech stacks. ",
            "The company offers excellent growth opportunities.\n",
            "[DONE]"
        ]

        for part in summary_parts:
            # Send each part as a Server-Sent Event
            yield f"data: {json.dumps({'text': part})}\n\n"
            await asyncio.sleep(0.3)  # Simulate LLM token generation delay

    return StreamingResponse(
        generate_summary(),
        media_type="text/event-stream",  # SSE format
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"  # Disable nginx buffering for streaming
        }
    )
```

---

## 10. Async/Await — FastAPI's Performance Secret

### Theory

**Synchronous** code blocks the thread while waiting:
```python
def get_job(job_id):
    result = db.query(...)  # Thread BLOCKED here — can't do anything else
    return result
```

**Asynchronous** code releases the thread while waiting:
```python
async def get_job(job_id):
    result = await db.fetch(...)  # Thread FREE to handle other requests
    return result
```

**When to use `async def` vs `def` in FastAPI:**

| Use `async def` when | Use `def` when |
|---------------------|----------------|
| Calling external APIs | Using SQLAlchemy (synchronous ORM) |
| File I/O operations | CPU-heavy tasks |
| WebSocket connections | Simple calculations |
| Using async libraries | Most regular DB queries |

**Important:** If you use `async def` with blocking code (like synchronous SQLAlchemy), you actually *hurt* performance because you block the event loop.

```python
# Correct async usage — calling an external ML inference API
import httpx

@app.post("/jobs/{job_id}/score-application")
async def score_application(job_id: int, resume_text: str):
    """
    Calls an external ML model API to score a resume.
    Using async here is correct because we're waiting for a network response.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://ml-model-api.internal/score",
            json={"resume": resume_text, "job_id": job_id},
            timeout=30.0
        )

    score_data = response.json()
    return {
        "job_id": job_id,
        "match_score": score_data["score"],
        "recommendation": score_data["recommendation"]
    }
```

---

## 11. Error Handling — Production-Grade Responses

### Theory

A good API never returns a raw Python traceback. It returns **structured, predictable error JSON** that the frontend can parse and display.

Bad error response:
```
Internal Server Error
Traceback (most recent call last):
  File "main.py", line 45...
  AttributeError: 'NoneType' object...
```

Good error response:
```json
{
  "error": "NOT_FOUND",
  "message": "Job with id 999 does not exist",
  "details": null,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

```python
# error_handlers.py
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from datetime import datetime

# ─── Standard Error Response Schema ────────────────────────────────
def error_response(error_code: str, message: str, details=None, status_code: int = 400):
    return JSONResponse(
        status_code=status_code,
        content={
            "error": error_code,
            "message": message,
            "details": details,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

# ─── Register in main.py ────────────────────────────────────────────

# Override FastAPI's default 422 validation error format
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    By default, FastAPI returns a complex nested 422 response.
    This handler reformats it into our clean standard schema.
    """
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " -> ".join(str(loc) for loc in error["loc"]),
            "issue": error["msg"],
            "received": error.get("input")
        })
    return error_response(
        error_code="VALIDATION_ERROR",
        message="Request data failed validation",
        details=errors,
        status_code=422
    )

# Override default HTTPException format
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    error_map = {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        500: "INTERNAL_ERROR"
    }
    return error_response(
        error_code=error_map.get(exc.status_code, "HTTP_ERROR"),
        message=exc.detail,
        status_code=exc.status_code
    )

# Catch ALL unhandled exceptions — prevents traceback leaking to clients
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Log the real error on the server (for debugging)
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    # Return a safe, generic error to the client
    return error_response(
        error_code="INTERNAL_ERROR",
        message="An unexpected error occurred. Please try again later.",
        status_code=500
    )
```

---

## 12. Testing — Verifying Everything Works

### Theory

**Why test APIs?**
- Catch bugs before your users do
- Ensure new changes don't break existing features (regression testing)
- Serve as living documentation of how endpoints behave

**TestClient** = a fake HTTP client that calls your FastAPI app without starting a real server. It's synchronous, fast, and perfect for unit tests.

```python
# test_jobs.py
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models
from database import Base, get_db
from main import app

# ─── Test Database Setup ────────────────────────────────────────────
# Use a separate in-memory SQLite DB for tests — never use the real DB!
TEST_DATABASE_URL = "sqlite:///./test_jobportal.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def override_get_db():
    """Replace the real DB dependency with the test DB."""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Override the dependency for the entire test session
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_database():
    """Create tables before each test, drop after."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

client = TestClient(app)

# ─── Tests ─────────────────────────────────────────────────────────

def test_create_job_success():
    """Test happy path: valid data → 201 Created."""
    response = client.post("/jobs", json={
        "title": "Backend Engineer",
        "company": "TestCorp",
        "location": "Surat",
        "salary_lpa": 8.0,
        "is_remote": True
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Backend Engineer"
    assert data["id"] is not None  # ID was assigned by DB

def test_create_job_missing_field():
    """Test validation: missing required field → 422."""
    response = client.post("/jobs", json={
        "title": "Engineer",
        # Missing: company, location, salary_lpa
    })
    assert response.status_code == 422

def test_create_job_invalid_salary():
    """Test validation: negative salary (gt=0 constraint) → 422."""
    response = client.post("/jobs", json={
        "title": "Engineer",
        "company": "Corp",
        "location": "Mumbai",
        "salary_lpa": -5.0  # Must be > 0
    })
    assert response.status_code == 422

def test_get_job_not_found():
    """Test 404 when job doesn't exist."""
    response = client.get("/jobs/9999")
    assert response.status_code == 404
    data = response.json()
    assert data["error"] == "NOT_FOUND"  # Verify our custom error format

def test_delete_job():
    """Test full CRUD cycle."""
    # Create
    create_response = client.post("/jobs", json={
        "title": "Test Job",
        "company": "Corp",
        "location": "Delhi",
        "salary_lpa": 10.0
    })
    job_id = create_response.json()["id"]

    # Delete
    delete_response = client.delete(f"/jobs/{job_id}")
    assert delete_response.status_code == 204

    # Verify it's gone
    get_response = client.get(f"/jobs/{job_id}")
    assert get_response.status_code == 404

def test_apply_to_job():
    """Test nested resource creation: apply to an existing job."""
    # First create a job
    job_response = client.post("/jobs", json={
        "title": "ML Engineer",
        "company": "AI Corp",
        "location": "Bangalore",
        "salary_lpa": 15.0
    })
    job_id = job_response.json()["id"]

    # Apply to it
    apply_response = client.post(f"/jobs/{job_id}/apply", json={
        "applicant_name": "Rahul Shah",
        "applicant_email": "rahul@example.com",
        "cover_letter": "I am very interested in this role."
    })
    assert apply_response.status_code == 201
    assert apply_response.json()["job_id"] == job_id
```

```bash
# Run tests
pytest test_jobs.py -v

# Run with coverage report
pytest test_jobs.py -v --cov=. --cov-report=term-missing
```

---

## 13. Swagger / OpenAPI Documentation — Auto-Generated API Docs

### Theory

FastAPI **reads your code** — the type hints, Pydantic models, docstrings, and Field descriptions — and automatically generates a full OpenAPI specification. This is then rendered as interactive Swagger UI.

**Two documentation interfaces:**
- `/docs` → Swagger UI (interactive, can send requests directly)
- `/redoc` → ReDoc (clean, read-only, good for sharing with clients)

### Enhancing Documentation Quality

```python
# main.py — production-grade metadata

app = FastAPI(
    title="Job Portal API",
    description="""
## Job Portal API

A RESTful API for managing job listings, applications, and recruiter accounts.

### Features
- **Job Management**: Create, read, update, delete job listings
- **Application Tracking**: Apply to jobs and track application status
- **Authentication**: JWT-based auth for recruiter accounts
- **AI Integration**: AI-powered job summary streaming

### Authentication
Use the **Authorize** button and provide your Bearer token after logging in via `/auth/login`.
    """,
    version="1.0.0",
    contact={
        "name": "Your Name",
        "email": "your@email.com",
    },
    license_info={
        "name": "MIT",
    },
    # Group endpoints by tags in Swagger UI
    openapi_tags=[
        {"name": "Jobs", "description": "Job listing management"},
        {"name": "Applications", "description": "Job application operations"},
        {"name": "Auth", "description": "Authentication and user management"},
        {"name": "AI", "description": "AI-powered features"},
    ]
)

# Use tags on routes to group them in Swagger UI
@app.post("/jobs", tags=["Jobs"], response_model=schemas.JobResponse, status_code=201)
def create_job(...):
    ...

@app.post("/auth/login", tags=["Auth"])
def login(...):
    ...
```

---

## 14. Final Architecture Diagram — System View

```
                    +-------------------------------------------------+
                    |             JOB PORTAL SYSTEM                   |
                    +-------------------------------------------------+

+-------------+   HTTP    +------------------------------------------+
|   Clients   | --------> |           UVICORN (ASGI)                  |
|  React App  |           |   Listens on port 8000                    |
|  Mobile App | <-------- |   Handles concurrent connections          |
|  Postman    |   HTTP    +--------------------+---------------------+
+-------------+                                |
                                               v
                              +----------------------------+
                              |     MIDDLEWARE STACK        |
                              |  1. CORS Filter             | <- Checks allowed origins
                              |  2. Logging Middleware      | <- Records every request
                              |  3. Timing Middleware       | <- Measures performance
                              +-------------+--------------+
                                            |
                                            v
                              +----------------------------+
                              |     FASTAPI ROUTER         |
                              |  GET  /jobs                |
                              |  POST /jobs                | <- Matches URL + Method
                              |  POST /auth/login          |
                              |  GET  /jobs/{id}           |
                              +-------------+--------------+
                                            |
                                            v
                    +---------------------------------------+
                    |       DEPENDENCY INJECTION            |
                    |  get_db()         -> DB Session       | <- Resources injected
                    |  get_current_user -> Auth'd User      |    before route runs
                    +-------------------+-------------------+
                                        |
                                        v
                    +---------------------------------------+
                    |       PYDANTIC VALIDATION             |
                    |  Request body validated               | <- 422 if invalid
                    |  Path params type-checked             |    Route never called
                    |  Query params parsed                  |
                    +-------------------+-------------------+
                                        |
                                        v
                    +---------------------------------------+
                    |         ROUTE FUNCTION                |
                    |  Your business logic runs here        |
                    |  Calls DB via SQLAlchemy              |
                    |  Calls ML models if needed            |
                    |  Raises HTTPException for errors      |
                    +-------------------+-------------------+
                                        |
                         +--------------+---------------+
                         v                             v
           +---------------------+      +------------------------+
           | SQLite / PostgreSQL |      |   External ML API      |
           | (via SQLAlchemy)    |      |  (via httpx async)     |
           +---------------------+      +------------------------+
                         |
                         v
                    +---------------------------------------+
                    |      PYDANTIC SERIALIZATION           |
                    |  ORM object -> response_model schema  | <- Shapes the output
                    |  Excludes sensitive fields            |    (e.g., hides password)
                    +-------------------+-------------------+
                                        |
                                        v
                    +---------------------------------------+
                    |         HTTP RESPONSE                 |
                    |  Status Code: 200 / 201 / 204         |
                    |  Headers: Content-Type, X-Process-Time|
                    |  Body: JSON (or streaming chunks)     |
                    +---------------------------------------+
```

---

## 15. Interview Cheat Sheet — Theory Questions & Answers

### Q: What is the difference between `async def` and `def` in FastAPI?

`def` routes run in a separate thread pool — FastAPI handles concurrency by spawning threads. `async def` routes run on the main event loop and can `await` I/O operations without blocking. Use `async def` only with async-compatible libraries; using it with synchronous blocking code (like standard SQLAlchemy) blocks the event loop and hurts performance.

### Q: What is Depends() and why use it?

`Depends()` is FastAPI's dependency injection system. It lets you declare reusable dependencies (like DB sessions, auth checks, pagination params) that FastAPI resolves automatically before calling your route. Benefits: code reuse, automatic cleanup (the `finally` block in `get_db()`), and easier testing (you can override dependencies in tests with `app.dependency_overrides`).

### Q: What is the difference between 401 and 403?

`401 Unauthorized` means no valid credentials were provided — the server doesn't know who you are. `403 Forbidden` means valid credentials were provided, but you don't have permission — the server knows who you are, but says "no."

### Q: How does Pydantic's `response_model` protect data?

`response_model` acts as an output filter. Even if your route function returns an object with extra fields (like a hashed password), FastAPI will only serialize and send the fields defined in the `response_model`. This prevents accidental data leaks.

### Q: What makes FastAPI faster than Flask?

FastAPI is built on Starlette (ASGI), which handles concurrent connections without threads. Flask uses WSGI which is synchronous. FastAPI also benefits from Pydantic v2's Rust-based core for validation speed. But the main advantage is the ASGI architecture — it can handle thousands of concurrent I/O-bound connections efficiently.

### Q: What is the purpose of middleware?

Middleware applies cross-cutting concerns globally across all routes — logging, CORS headers, authentication pre-checks, rate limiting, timing. Instead of adding these to every route function, you add them once and they run for every request.

### Q: Why do we need CORS? Is it a server-side or client-side concept?

CORS is enforced by the **browser** (client-side). The browser checks the `Access-Control-Allow-Origin` header in the response. If it doesn't match the frontend's origin, the browser blocks the JS code from reading the response — even if the server returned 200. The server-side configuration adds those headers to responses.

### Q: How does JWT authentication work end-to-end?

1. User POSTs credentials to `/auth/login`
2. Server verifies password against hashed value in DB
3. Server creates JWT: `{"sub": user_id, "exp": timestamp}` → signs it with secret key → returns it
4. Client stores token (localStorage or memory)
5. Client sends `Authorization: Bearer <token>` with every subsequent request
6. Server's `get_current_user` dependency decodes and validates the token, loads the user
7. If token is expired/invalid → 401 is returned automatically

### Q: What is the difference between `PUT` and `PATCH`?

`PUT` replaces the entire resource — you send all fields. `PATCH` partially updates — you send only the fields you want to change. In practice, `PUT` requires the full resource schema; `PATCH` uses a schema with all fields optional.

---

## Quick Reference: File Structure for Production

```
job_portal/
├── main.py              # FastAPI app, route registration, middleware
├── database.py          # Engine, SessionLocal, get_db dependency
├── models.py            # SQLAlchemy ORM models (tables)
├── schemas.py           # Pydantic request/response schemas
├── auth.py              # JWT creation, password hashing, get_current_user
├── error_handlers.py    # Custom exception handlers
├── routers/
│   ├── jobs.py          # Job-related routes
│   ├── applications.py  # Application routes
│   └── auth.py          # Auth routes
├── tests/
│   ├── test_jobs.py
│   └── test_auth.py
└── requirements.txt
```

---
