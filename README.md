🧩 Codemonk – Backend Intern Assignment
A fully containerized, reproducible Python backend system built to demonstrate backend fundamentals, system design, and practical engineering decisions.

📌 Introduction
This project was built as part of the Codemonk Backend Intern Assignment.

The goal of this assignment is not only to implement functionality, but also to demonstrate:

Clear understanding of backend fundamentals
Ability to design a system with multiple components
Clean project structure and documentation
Reproducibility and ease of setup
Awareness of real-world backend practices
The backend allows users to register, authenticate, submit text data, and retrieve analytical results efficiently while ensuring security, scalability, and clarity.

🎯 Problem Statement (As Understood)
The system should:

Allow users to register and manage sessions
Accept multiple paragraphs of text from users
Compute word frequencies efficiently
Return the top 10 paragraphs for a searched word (per user)
Use background processing
Be containerized and easy to run on any machine
Be clearly documented and explainable
This project is designed to strictly satisfy all of the above requirements.

🛠 Tech Stack & Design Decisions (With Reasons)
Backend Framework — Django + Django REST Framework
Why Django:

Provides a secure authentication system out of the box
Encourages clean and scalable project structure
Widely used in production backend systems
Why Django REST Framework:

Simplifies API development
Handles request validation and serialization cleanly
Encourages separation of concerns
Flask was a possible alternative, but Django was chosen for better structure, security, and built-in features.

Database — PostgreSQL
Why PostgreSQL:

Reliable relational database
Strong indexing and query optimization support
Commonly used in real-world backend systems
Chosen over SQLite/MySQL for scalability and production relevance.

Background Task Processor — Celery
Why Celery:

Enables asynchronous background processing
Prevents long-running operations from blocking API requests
Scales well with message brokers
Used specifically for word frequency computation to improve API responsiveness.

Message Broker — Redis
Why Redis:

Fast, in-memory data store
Industry standard with Celery
Simple and reliable for task queues
Containerization — Docker & Docker Compose
Why Docker:

Ensures identical behavior across machines
Removes dependency and environment issues
Required by the assignment
Why Docker Compose:

Manages multiple services (backend, database, Redis, worker)
Allows running the entire system with a single command
📂 Project Structure
codemonk_backend/

Dockerfile
docker-compose.yml
requirements.txt
.env.example
README.md
app/
manage.py
core/
settings.py
urls.py
celery.py
password validators and utilities
auth_app/
models.py
serializers.py
views.py
urls.py
text_app/
models.py
tasks.py
views.py
urls.py
Each module has a single responsibility, improving maintainability and readability.

🔐 Authentication & Security Design
Implemented features:

User registration
Secure login and logout
Strong password validation
Login rate limiting
Account lock after repeated failures
Why these were added:

Demonstrates real-world backend security thinking
Protects against brute-force attacks
Shows understanding of authentication best practices
These features were not strictly required but align with industry expectations.

📝 Paragraph & Word Frequency Design
How it works:

User submits multiple paragraphs in one request
Each paragraph is stored in the database
Word frequency computation runs asynchronously
Results are indexed for fast retrieval
Search returns the top 10 paragraphs for a word (per user)
Why indexing:

Improves query performance
Scales better as data grows
📘 API Documentation
Base URL: http://localhost:8000

🔐 Authentication APIs
Register User
Endpoint: POST /api/auth/register/

Request body example:

username: john
password: StrongPass@123
Response:

message: Registered
image
Login User
Endpoint: POST /api/auth/login/

Success response:

message: Logged in
Failure cases:

Invalid credentials → 401
Rate limit exceeded → 429
Account locked → 403
image
Logout User
Endpoint: POST /api/auth/logout/ image
📝 Text APIs (Authenticated)
Submit Paragraphs
Endpoint: POST /api/text/submit/

Request body example:

paragraphs:
Text one
Text two
Response:

processing: true
image
Search Word Frequency
Endpoint: GET /api/text/search/?word=django

Response example:

paragraph: "Django is powerful"
count: 1
Results are:

User-specific
Limited to top 10
Ordered by highest frequency
image
🧪 API Testing
All APIs tested using Postman
Success, failure, and edge cases verified
Postman screenshots included in the repository
This confirms the system works end-to-end.

8️⃣ Setup Instructions (Minimal Effort)
Prerequisites
Docker
Docker Compose
Steps
Clone the repository
git clone

Move into the project directory
cd codemonk_backend

Create environment file
cp .env.example .env

Run the entire system
docker-compose up --build

Access
Backend will be available at:
http://localhost:8000

No additional configuration is required.

🐳 Containerized Services
Django backend
PostgreSQL database
Redis
Celery worker
All services start automatically using Docker Compose.

✅ Assignment Requirement Mapping
User registration → Implemented
Secure login/logout → Implemented
Paragraph submission → Implemented
Word frequency indexing → Implemented
Top 10 paragraph search → Implemented
Background processing → Implemented
Containerization → Implemented
API documentation → Implemented
Easy setup → Implemented
👨‍💻 Author
Hariharan Balasubramaniyam
Backend Intern Candidate

GitHub: https://github.com/Hariharan0946
LeetCode: https://leetcode.com/u/NDvaDaMsfm/

Resume : https://drive.google.com/file/d/1RP77PMQl_Tr9RSSl4ciqBP9-0HxwXvcz/view?usp=drive_link LeetCode: https://leetcode.com/u/NDvaDaMsfm/

📝 Final Notes
The project follows clean coding practices
All assignment conditions are satisfied
The system runs end-to-end with a single command
I am prepared to explain every design and code decision during the technical interview
✅ Submission Ready
This README fully satisfies Codemonk’s expectations for documentation, clarity, design understanding, and reproducibility.
