# TaskForge API

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=flat&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![Alembic](https://img.shields.io/badge/Alembic-Migrations-blue?style=flat&logo=python)](https://alembic.sqlalchemy.org/)
[![Auth](https://img.shields.io/badge/Auth-JWT%20%2F%20OAuth2-orange?style=flat&logo=json-web-tokens)](https://jwt.io/)

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
* **Github ACtions:** ci.yml

## 🚀 Features

* Login user
* Register user
* Create workspace
* Get workspace
* Get a workspace by ID
* Get a all workspace
* Update workspace
* Delete workspace
* Create tasks
* Get tasks
* Get a task by ID
* Get a all tasks
* Update tasks
* Delete tasks
* Request validation
* HTTP status code handling
* Persistent data storage
* RESTful API structure

---

## 🎯 Project Scope

This is a **junior-level backend project** created to demonstrate the ability to build and organize a basic REST API.

It is not intended to be presented as a production-ready system. Instead, it serves as a foundation for progressively more advanced projects involving authentication, testing, architecture, deployment, and scalability.

---

## 📡 API Endpoints

## Workspaces

| Method          | Endpoint                         | Description       |
| --------------- | -------------                    | ----------------- |
| `GET`           | `/api/v1.0/workspace`            | Get all tasks     |
| `GET`           | `/api/v1.0/workspace{task_id}`   | Get a task by ID  |
| `POST`          | `/api/v1.0/workspace`            | Create a newtask  |
| `PUT` / `PATCH` | `/api/v1.0/workspace{task_id}`   | Update atask      |
| `DELETE`        | `/api/v1.0/workspace{task_id}`   | Delete atask      |

### Tasks

| Method          | Endpoint                     | Description       |
| --------------- | -------------                | ----------------- |
| `GET`           | `/api/v1.0/tasks`            | Get all tasks     |
| `GET`           | `/api/v1.0/tasks{task_id}`   | Get a task by ID  |
| `POST`          | `/api/v1.0/tasks`            | Create a newtask  |
| `PUT` / `PATCH` | `/api/v1.0/tasks{task_id}`   | Update atask      |
| `DELETE`        | `/api/v1.0/tasks{task_id}`   | Delete atask      |

## 📁 Project Structure

```text
Tareas_api/
│
├── [app]/
│   ├── [router]
│   │   ├── [authentication.py]
│   │   ├── [workspaces.py]
│   │   └── [task.py]
│   ├── [database.py]
│   ├── [main.py]
│   ├── [config.py]
│   ├── [models.py]
│   ├── [security.py]
│   └── [schemas.py]
├── [tests]/
│   ├── [api]/
│   │   └── [test_api.py]
│   ├── [unit]/
│   │   └── [test_unit.py]
│   └── conftest.py
├── docker-compose.yml
├── README.md
├── .dockerignore
├── .gitignore
├── requirements.txt
└── [Dockerfile]
```

## Configure environment variables

Create a `.env` file when required by the project.
But it have already some variables set

Example:

```env
SECRET_KEY=misupersecretkey
POSTGRES_PASSWORD=Fakepassword
```

## 💻 Setup and Execution

Ensure you have **Docker** and **Docker Compose** installed on your system.

1. Clone this repository:
   ```bash
   git clone [https://github.com/AndresPimentel-dev/proyecto-task-management.git](https://github.com/AndresPimentel-dev/proyecto-task-management.git)
   cd proyecto-task-management

## 🔎 API Documentation

http://localhost:8000/docs

## 📄 License

This project is licensed under the [MIT License](LICENSE).