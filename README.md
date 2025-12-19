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
➜ Django REST APIs
➜ PostgreSQL (Persistent Storage)
➜ Celery (Async Processing)
➜ Redis (Message Broker)

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

This ensures **low-latency APIs** and **scalable processing**.

---

## 📂 Project Structure (Intentional & Modular)

```text
codemonk_backend/

- app/
  - manage.py

  - core/
    - settings.py
    - urls.py
    - celery.py
    - password utilities & validators

  - auth_app/
    - models.py
    - serializers.py
    - views.py
    - urls.py

  - text_app/
    - models.py
    - tasks.py
    - views.py
    - urls.py

- assets/
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

Security is treated as a core requirement, not an enhancement.

📝 Paragraph & Word Frequency Design

Paragraphs are stored independently

Word frequencies are computed per paragraph

Results are associated with both user and paragraph

Indexed queries ensure fast lookups

📘 API Documentation
Base URL

http://localhost:8000

🔐 Register User

POST /api/auth/register/

<img width="782" height="729" alt="image" src="https://github.com/user-attachments/assets/64efdbe3-f864-4a92-baf1-1607de261b41" />


🔐 Login User

POST /api/auth/login/

<img width="785" height="733" alt="image" src="https://github.com/user-attachments/assets/95e17fd2-249a-43ab-be4d-5cc4a9c4a564" />

🔐 Logout User

POST /api/auth/logout/

<img width="1088" height="623" alt="image" src="https://github.com/user-attachments/assets/1e524947-ea9d-41d9-996b-8803a1d42151" />


📝 Submit Paragraphs

POST /api/text/submit/

<img width="789" height="855" alt="image" src="https://github.com/user-attachments/assets/12c415b6-46ff-464b-8eed-44f79b0df899" />


🔍 Search Word Frequency

GET /api/text/search/?word=django

<img width="776" height="946" alt="image" src="https://github.com/user-attachments/assets/f6be59fb-61d0-44cc-8bf4-bde75c78bb3d" />


🧪 Testing Strategy

Manual testing using Postman

Success, failure, and edge cases verified

Screenshots included in repository

⚙️ Setup Instructions
git clone <repository-url>
cd codemonk_backend
cp .env.example .env
docker-compose up --build


Backend runs at:
http://localhost:8000

🐳 Containerized Services

Django backend

PostgreSQL

Redis

Celery worker

⚖️ Engineering Trade-offs

REST APIs over GraphQL

Manual testing due to scope constraints

Modular monolith over microservices

🔮 Future Improvements

JWT authentication

Pagination

Automated tests

Swagger documentation

Logging & monitoring

👨‍💻 Author

Hariharan Balasubramaniyam
Backend Intern Candidate

Resume:
https://drive.google.com/file/d/1RP77PMQl_Tr9RSSl4ciqBP9-0HxwXvcz/view

LeetCode:
https://leetcode.com/u/NDvaDaMsfm/

🏁 Final Notes

The system runs end-to-end with a single command and is fully explainable at both code and design levels.
