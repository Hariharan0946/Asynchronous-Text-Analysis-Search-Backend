# 🧩 Codemonk – Backend Intern Assignment  
🚀 **A production-grade, fully containerized Python backend system showcasing backend fundamentals, system design depth, and real-world engineering judgment**

---

## 🟦 Executive Summary (Why This Project Stands Out)

This repository contains my submission for the **Codemonk Backend Intern Assignment**.

Rather than focusing only on feature completion, this project was intentionally built to demonstrate:

- how I **think about backend systems**,  
- how I **translate requirements into architecture**,  
- how I **make engineering trade-offs**, and  
- how I **document and explain systems clearly** for reviewers and interviewers.

This README is written as a **technical case study**, not just documentation.

---

## 🟩 Context & Objective

The assignment requires building a Python-based backend system that supports:

- secure user authentication,
- text ingestion and analysis,
- efficient querying,
- background processing,
- and reproducible deployment.

Beyond correctness, the evaluation focuses on:
- conceptual understanding,
- system design clarity,
- maintainability,
- and explainability.

This project is designed to **explicitly satisfy all evaluation dimensions**.

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

All functional and non-functional requirements are fully implemented.

---

## 🧠 Design Philosophy & Engineering Principles

This project follows a **production-first backend mindset**, guided by these principles:

- **Clarity over cleverness** – readable systems scale better than smart hacks  
- **Security by default** – auth and abuse prevention are baseline, not add-ons  
- **Separation of concerns** – one module, one responsibility  
- **Scalability awareness** – design should not collapse as data grows  
- **Reproducibility** – systems should run identically everywhere  
- **Explainability** – every decision must be defensible in an interview  

These principles influenced every design choice.

---

## 🛠 Technology Stack & Justification

### 🔵 Backend Framework — Django + Django REST Framework

**Why Django**
- Battle-tested authentication system  
- Strong conventions → clean architecture  
- Widely adopted in production environments  

**Why Django REST Framework**
- Explicit request/response handling  
- Clear validation and serialization  
- Encourages separation between API and business logic  

Flask was considered, but Django was chosen for **structure, security, and scalability**.

---

### 🟢 Database — PostgreSQL

**Why PostgreSQL**
- Reliable relational guarantees  
- Strong indexing & query optimization  
- Production-grade tooling  

Chosen over SQLite/MySQL for **real-world relevance**.

---

### 🟣 Background Processing — Celery

**Why Celery**
- Enables true asynchronous execution  
- Prevents blocking API requests  
- Scales independently from web servers  

Used specifically for **word frequency computation**.

---

### 🔴 Message Broker — Redis

**Why Redis**
- Extremely fast in-memory operations  
- Industry standard for Celery  
- Simple and reliable  

---

### 🟠 Containerization — Docker & Docker Compose

**Why Docker**
- Eliminates “works on my machine” issues  
- Ensures environment consistency  
- Required by the assignment  

**Why Docker Compose**
- Orchestrates multi-service systems  
- Enables one-command startup  

---

## 🏗 System Architecture (High-Level)

Client (Postman / Frontend)
↓
Django REST APIs
↓
PostgreSQL (Persistent Storage)
↓
Celery (Async Processing)
↓
Redis (Message Broker)

yaml
Copy code

---

## 🔄 End-to-End Request Lifecycle

1. User submits multiple paragraphs via API  
2. API validates input and stores paragraphs immediately  
3. A Celery task is triggered per paragraph  
4. Word frequency computation runs asynchronously  
5. Results are normalized and indexed  
6. Search queries fetch optimized results instantly  

This ensures **low latency APIs** and **scalable processing**.

---

## 📂 Project Structure (Intentional & Modular)

```text
codemonk_backend/

- app/

    - manage.py

    - core/
        - settings.py              # Global Django configuration
        - urls.py                  # Root URL routing
        - celery.py                # Celery application setup
        - password utilities & validators

    - auth_app/
        - models.py                # User extensions & security fields
        - serializers.py           # Input validation & user creation
        - views.py                 # Register / Login / Logout APIs
        - urls.py                  # Auth routes

    - text_app/
        - models.py                # Paragraph & word-frequency schema
        - tasks.py                 # Background computation logic
        - views.py                 # Submit & search APIs
        - urls.py                  # Text routes

- Dockerfile
- docker-compose.yml
- requirements.txt
- entrypoint.sh
- .env.example
- README.md
Each module has one responsibility, improving maintainability and testability.

🔐 Authentication & Security Design
Implemented Safeguards
User registration

Secure login & logout

Strong password validation

Login rate limiting

Account lock after repeated failures

Rationale
These measures:

prevent brute-force attacks,

demonstrate security awareness,

align with industry best practices.

Security is treated as a core requirement, not an enhancement.

📝 Paragraph & Word Frequency Design
Processing Flow
Paragraphs are stored independently

Word frequencies are computed per paragraph

Results are associated with both user and paragraph

Old frequency data is replaced on reprocessing

Why Indexing Matters
Faster search queries

Reduced database scans

Predictable performance at scale

## 📘 API Documentation

Base URL:
http://localhost:8000

---

### 🔐 Authentication APIs

Register User  
Endpoint: POST /api/auth/register/

Request body example:
- username: john
- password: StrongPass@123

Response:
- message: Registered
<img width="782" height="729" alt="image" src="https://github.com/user-attachments/assets/0e1f60b8-5bc7-4432-a6d3-42d36129d021" />

---

Login User  
Endpoint: POST /api/auth/login/

Success response:
- message: Logged in

Failure cases:
- Invalid credentials → 401
- Rate limit exceeded → 429
- Account locked → 403
<img width="785" height="733" alt="image" src="https://github.com/user-attachments/assets/509638f3-2b72-426c-80b9-8abbd6ea7855" />

---

Logout User  
Endpoint: POST /api/auth/logout/
<img width="1088" height="623" alt="image" src="https://github.com/user-attachments/assets/959e327f-ff7c-4f48-86e2-e1e61eb3e40d" />
---

### 📝 Text APIs (Authenticated)

Submit Paragraphs  
Endpoint: POST /api/text/submit/

Request body example:
- paragraphs:
  - Text one
  - Text two

Response:
- processing: true
 <img width="789" height="855" alt="image" src="https://github.com/user-attachments/assets/536a530e-5149-494d-b463-027e74ed8c53" />



---

Search Word Frequency  
Endpoint: GET /api/text/search/?word=django

Response example:
- paragraph: "Django is powerful"
- count: 1

Results are:
- User-specific
- Limited to top 10
- Ordered by highest frequency
<img width="776" height="946" alt="image" src="https://github.com/user-attachments/assets/7637905c-83fb-4c24-8a64-2bcc5c61f41c" />


---

🧪 Testing Strategy

Manual testing via Postman

Success, failure, and edge cases verified

Screenshots included in repository

Ensures end-to-end correctness.

⚙️ Setup Instructions (One Command)
Prerequisites

Docker

Docker Compose

Run
git clone <repository-url>
cd codemonk_backend
cp .env.example .env
docker-compose up --build


Backend available at:
http://localhost:8000

🐳 Containerized Services

Django backend

PostgreSQL database

Redis

Celery worker

All services start automatically.

⚖️ Engineering Trade-offs

REST APIs over GraphQL (simplicity & clarity)

Manual testing due to scope constraints

Modular monolith over microservices

These trade-offs favor maintainability and evaluability.

🔮 Future Improvements

Given more time, I would add:

JWT-based authentication

Pagination for large datasets

Automated test coverage

Swagger / OpenAPI docs

Structured logging & monitoring

Advanced text normalization

✅ Requirement Mapping

User registration → Implemented

Secure auth → Implemented

Paragraph submission → Implemented

Word frequency indexing → Implemented

Top 10 search → Implemented

Background processing → Implemented

Containerization → Implemented

Documentation → Implemented

👨‍💻 Author

Hariharan Balasubramaniyam
Backend Intern Candidate

Resume:
https://drive.google.com/file/d/1RP77PMQl_Tr9RSSl4ciqBP9-0HxwXvcz/view

LeetCode:
https://leetcode.com/u/NDvaDaMsfm/

🏁 Final Notes

This project demonstrates:

strong backend fundamentals,

thoughtful system design,

production-aware decisions,

and clear technical communication.

The system runs end-to-end with a single command, and I am fully prepared to explain every architectural and code-level decision during the technical interview.














