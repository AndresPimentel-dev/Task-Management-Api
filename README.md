# TaskForge API

A robust backend for task and workspace management, designed for scalability, performance, and security.

## 🚀 Key Features
* **RESTful Architecture:** Developed with FastAPI for high-performance request handling.
* **Security:** Secure authentication using JWT (JSON Web Tokens) with Bcrypt password hashing.
* **Persistence:** Reliable data management with PostgreSQL and SQLAlchemy ORM.
* **Containerization:** Fully containerized using Docker and Docker Compose for consistent cross-environment deployment.

## 🛠 Tech Stack
* **Language:** Python 3.11+
* **Framework:** FastAPI
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Deployment:** Docker, Docker Compose

## 📋 API Endpoints
* `POST /register`: New user registration.
* `POST /login`: Authentication and JWT access token retrieval.
* `POST /workspaces`: Create custom workspaces.
* `POST /tasks`: Create tasks linked to specific workspaces and users.
* `GET /tasks`: List tasks assigned to the authenticated user.

## 💻 Setup and Execution

Ensure you have **Docker** and **Docker Compose** installed on your system.

1. Clone this repository:
   ```bash
   git clone [https://github.com/AndresPimentel-dev/proyecto-task-management.git](https://github.com/AndresPimentel-dev/proyecto-task-management.git)
   cd proyecto-task-management
