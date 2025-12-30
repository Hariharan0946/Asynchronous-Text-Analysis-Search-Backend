# 🧩 Asynchronous Text Analysis & Search Backend
🚀 **A production-grade, fully containerized Python backend system showcasing backend fundamentals, system design depth, and real-world engineering judgment**

---

## 🟦 Executive Summary (Why This Project Stands Out)

This repository contains my submission for the **Codemonk Backend Intern Assignment**.

Rather than focusing only on feature completion, this project was intentionally built to demonstrate:

- how I **think about backend systems**
- how I **translate requirements into architecture**
- how I **make engineering trade-offs**
- how I **document and explain systems clearly**

This README is written as a **technical case study**, not just documentation.

---

## 🟩 Context & Objective

The assignment requires building a Python-based backend system that supports:

- secure user authentication
- text ingestion and analysis
- efficient querying
- background processing
- reproducible deployment

Beyond correctness, the evaluation focuses on:
- conceptual understanding
- system design clarity
- maintainability
- explainability

This project explicitly satisfies all evaluation dimensions.

---

## 🟨 Problem Statement (Interpreted Precisely)

The system must:

- Allow users to register and manage sessions securely  
- Accept multiple paragraphs of text per user  
- Compute word frequencies efficiently  
- Return the **top 10 paragraphs (per user)** for a searched word  
- Perform heavy computation asynchronously  
- Be containerized and runnable with a single command  
- Be clearly documented and interview-explainable  

All functional and non-functional requirements are implemented.

---

## 🧠 Design Philosophy & Engineering Principles

This project follows a **production-first backend mindset**:

- **Clarity over cleverness**
- **Security by default**
- **Separation of concerns**
- **Scalability awareness**
- **Reproducibility**
- **Explainability**

Every design decision is interview-defensible.

---

## 🛠 Technology Stack & Justification

### 🔵 Backend — Django + Django REST Framework
Chosen for structure, security, and production readiness.

### 🟢 Database — PostgreSQL
Used for real-world relevance, indexing, and query performance.

### 🟣 Background Processing — Celery
Handles asynchronous word-frequency computation.

### 🔴 Message Broker — Redis
Industry-standard broker for Celery.

### 🟠 Containerization — Docker & Docker Compose
Ensures reproducible, one-command startup.

---

## 🏗 System Architecture (High-Level)

```

┌────────────────────────────────────────────────────────────────────────────────────────┐
│                         CODEMONK BACKEND – SYSTEM ARCHITECTURE                          │
└────────────────────────────────────────────────────────────────────────────────────────┘

                                HTTP / HTTPS (JSON)
┌────────────────────────┐  ───────────────────────────►  ┌────────────────────────────┐
│                        │                                 │                            │
│   CLIENT LAYER         │  ◄───────────────────────────  │  DJANGO REST BACKEND        │
│                        │         JSON Responses          │  (Gunicorn + WSGI)          │
│ • Postman              │                                 │                            │
│ • Browser              │                                 │                            │
│                        │                                 │  ┌──────────────────────┐  │
└────────────────────────┘                                 │  │ core/urls.py          │  │
                                                           │  │ URL Routing           │  │
                                                           │  └──────────┬───────────┘  │
                                                           │             │              │
                                                           │  ┌──────────▼───────────┐  │
                                                           │  │ View Layer (DRF)     │  │
                                                           │  │                      │  │
                                                           │  │ auth_app/views.py    │  │
                                                           │  │ • Register           │  │
                                                           │  │ • Login              │  │
                                                           │  │ • Logout             │  │
                                                           │  │                      │  │
                                                           │  │ text_app/views.py    │  │
                                                           │  │ • Submit Paragraphs  │  │
                                                           │  │ • Search Words       │  │
                                                           │  └──────────┬───────────┘  │
                                                           │             │              │
                                                           │  ┌──────────▼───────────┐  │
                                                           │  │ Serializer Layer     │  │
                                                           │  │                      │  │
                                                           │  │ RegisterSerializer   │  │
                                                           │  │ • Password checks    │  │
                                                           │  │ • Field validation   │  │
                                                           │  └──────────┬───────────┘  │
                                                           │             │              │
                                                           │  ┌──────────▼───────────┐  │
                                                           │  │ Business Logic       │  │
                                                           │  │                      │  │
                                                           │  │ Auth Logic           │  │
                                                           │  │ • Rate limit (IP)    │  │
                                                           │  │ • Failed attempts    │  │
                                                           │  │ • Account lock       │  │
                                                           │  │                      │  │
                                                           │  │ Text Logic           │  │
                                                           │  │ • Paragraph create   │  │
                                                           │  │ • Task trigger       │  │
                                                           │  └──────────┬───────────┘  │
                                                           │             │              │
                                                           │  ┌──────────▼───────────┐  │
                                                           │  │ Django ORM Layer     │  │
                                                           │  │                      │  │
                                                           │  │ auth_app/models.py   │  │
                                                           │  │ • User               │  │
                                                           │  │   - failed_attempts  │  │
                                                           │  │   - lock_until       │  │
                                                           │  │                      │  │
                                                           │  │ text_app/models.py   │  │
                                                           │  │ • Paragraph          │  │
                                                           │  │ • WordFrequency      │  │
                                                           │  │   (indexed fields)   │  │
                                                           │  └──────────┬───────────┘  │
                                                           └─────────────┼──────────────┘
                                                                         │
                      ┌──────────────────────────────────────────────────┼─────────────────────────────────────────────────┐
                      │                                                  │                                                 │
                      ▼                                                  ▼                                                 ▼
        ┌────────────────────────────┐                 ┌────────────────────────────┐                 ┌────────────────────────────┐
        │        PostgreSQL           │                 │            Redis            │                 │        Celery Worker        │
        │      (Primary Database)    │                 │      (Message Broker)       │                 │     (Async Processing)     │
        │                            │                 │                            │                 │                            │
        │ Tables:                    │                 │ • Task Queue               │                 │ text_app/tasks.py          │
        │ • auth_user (custom)       │◄──── ORM ──────►│ • Celery messages           │◄──── Queue ────►│ • compute_frequency()      │
        │ • Paragraph                │                 │                            │                 │                            │
        │ • WordFrequency            │                 │                            │                 │ Steps:                     │
        │                            │                 │                            │                 │ 1. Fetch Paragraph         │
        │ Indexes:                   │                 │                            │                 │ 2. Tokenize words          │
        │ • (user, word, -count)     │                 │                            │                 │ 3. Count frequencies       │
        │                            │                 │                            │                 │ 4. Bulk insert results     │
        └────────────────────────────┘                 └────────────────────────────┘                 └────────────────────────────┘
                      │                                                  │                                                 │
                      └───────────────────────────────┬──────────────────┴──────────────────┬───────────────────────────────┘
                                                      │                                     │
                                                      ▼                                     ▼
                                      ┌────────────────────────────────────────────────────────────┐
                                      │                     Docker Compose                          │
                                      │                (System Orchestration)                       │
                                      │                                                            │
                                      │ Services:                                                   │
                                      │ • web     → Django + Gunicorn                               │
                                      │ • worker  → Celery worker                                   │
                                      │ • db      → PostgreSQL                                      │
                                      │ • redis   → Redis                                           │
                                      │                                                            │
                                      │ Responsibilities:                                           │
                                      │ • Container networking                                      │
                                      │ • Environment variables                                     │
                                      │ • One-command startup                                       │
                                      └────────────────────────────────────────────────────────────┘


┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              REQUEST / DATA FLOW (EXACT)                               │
└────────────────────────────────────────────────────────────────────────────────────────┘

AUTH FLOW:
1. Client → POST /api/auth/login/
2. Rate limit check (django-ratelimit)
3. Validate credentials
4. Increment failed_attempts OR reset on success
5. Lock account if threshold exceeded
6. Session created and response returned

TEXT FLOW:
1. Client → POST /api/text/submit/
2. Paragraphs stored in PostgreSQL
3. Celery task triggered for each paragraph
4. Task queued in Redis
5. Celery worker processes text
6. WordFrequency table updated
7. Client → GET /api/text/search/?word=x
8. Indexed query → Top 10 results returned


┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              WHY THIS ARCHITECTURE WORKS                               │
└────────────────────────────────────────────────────────────────────────────────────────┘

• Clear separation of concerns (auth, text, core)
• Non-blocking API using async background tasks
• Secure authentication with real-world protections
• Optimized DB queries using indexes
• Fully reproducible using Docker
• Easy to explain, easy to extend, production-aligned


```

## 🔄 End-to-End Request Lifecycle

1. User submits paragraphs  
2. API validates and stores data  
3. Celery task triggered per paragraph  
4. Word frequencies computed asynchronously  
5. Results indexed and normalized  
6. Optimized search queries return results instantly  



```
## 📂 Project Structure (Intentional & Modular)


codemonk_backend/
│
├── app/
│   ├── manage.py
│   │
│   ├── core/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── celery.py
│   │   └── password utilities & validators
│   │
│   ├── auth_app/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   │
│   └── text_app/
│       ├── models.py
│       ├── tasks.py
│       ├── views.py
│       └── urls.py
│
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── requirements.txt
├── .env.example
└── README.md


Each module has one responsibility, improving maintainability and testability.
```
## 🔐 Authentication & Security Design

**Implemented safeguards:**

- User registration  
- Secure login & logout  
- Strong password validation  
- Login rate limiting  
- Account lock after repeated failures  

Security is treated as a **core requirement**, not an enhancement.

---

## 📝 Paragraph & Word Frequency Design

- Paragraphs are stored independently  
- Word frequencies are computed per paragraph  
- Results are linked to both the user and the paragraph  
- Indexed queries ensure fast lookups  

📘 API Documentation

Base URL
http://localhost:8000

🔐 Register User

POST /api/auth/register/

<img width="782" height="729" alt="image" src="https://github.com/user-attachments/assets/ba22226a-e72b-4b4a-851a-cf46190f0fc2" />


🔐 Login User

POST /api/auth/login/

<img width="785" height="733" alt="image" src="https://github.com/user-attachments/assets/031f68d5-ebde-4fe4-91ff-bd12c0d745aa" />


🔐 Logout User

POST /api/auth/logout/

<img width="1088" height="623" alt="image" src="https://github.com/user-attachments/assets/fb036d1d-788f-48a1-a059-8d605a57ec89" />


📝 Submit Paragraphs

POST /api/text/submit/

<img width="789" height="855" alt="image" src="https://github.com/user-attachments/assets/f7fcd624-beb6-4618-b0eb-e43cf6dd9c3d" />


🔍 Search Word Frequency

GET /api/text/search/?word=django

<img width="776" height="946" alt="image" src="https://github.com/user-attachments/assets/d7023934-fa64-40a5-bcd4-166f2339223a" />

• 🧪 Testing Strategy
  - Manual testing using Postman
  - Success, failure, and edge cases verified
  - Screenshots included in the repository

• ⚙️ Setup Instructions
  - `git clone <repository-url>`
  - `cd codemonk_backend`
  - `cp .env.example .env`
  - `docker-compose up --build`
  - Backend runs at: http://localhost:8000

• 🐳 Containerized Services
  - Django backend
  - PostgreSQL
  - Redis
  - Celery worker

• ⚖️ Engineering Trade-offs
  - REST APIs over GraphQL (simplicity)
  - Manual testing due to assignment scope
  - Modular monolith over microservices

• 🔮 Future Improvements
  - JWT authentication
  - Pagination
  - Automated tests
  - Swagger/OpenAPI docs
  - Logging & monitoring

• 👨‍💻 Author
  - Hariharan Balasubramaniyam
  - Backend Intern Candidate
  - Resume: https://drive.google.com/file/d/1RP77PMQl_Tr9RSSl4ciqBP9-0HxwXvcz/view
  - LeetCode: https://leetcode.com/u/NDvaDaMsfm/

• 🏁 Final Notes
  - The system runs end-to-end with a single command
  - Fully containerized
  - Explainable at both code and system design levels



