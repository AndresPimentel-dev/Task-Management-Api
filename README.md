# TaskForge API

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=flat&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![Alembic](https://img.shields.io/badge/Alembic-Migrations-blue?style=flat&logo=python)](https://alembic.sqlalchemy.org/)
[![Auth](https://img.shields.io/badge/Auth-JWT%20%2F%20OAuth2-orange?style=flat&logo=json-web-tokens)](https://jwt.io/)

Task Management REST API built with FastAPI and PostgreSQL. Features secure JWT authentication, relational database architecture via SQLAlchemy, and fully containerized environments using Docker and Docker Compose.

## Features

- User registration and authentication
- JWT authentication
- Workspace management
- Task management
- PostgreSQL
- Database migrations
- Automated tests
- Docker

## 🛠 Tech Stack
* **Python**
* **FastAPI**
* **PostgreSQL**
* **SQLAlchemy**
* **Alembic**
* **Pydantic**
* **Pytest**
* **Docker**

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

---

## 💻 How to run

Ensure you have **Docker** and **Docker Compose** installed on your system.

1. Clone this repository:
   ```bash
   git clone [https://github.com/AndresPimentel-dev/Task-Management-Api](https://github.com/AndresPimentel-dev/Task-Management-Api.git)
   cd proyecto-task-management
3. Create a `.env` file when required by the project.
   Example:
   ```env
   SECRET_KEY=misupersecretkey
   POSTGRES_PASSWORD=Fakepassword
   ```
2. Run Docker compose:
   ```bash
   docker compose up --build

## 🔎 API Documentation

1. Create a virtual enviroment
2. Run testing:
   ```bash
   pip install -r requirements && python -m pytest


http://localhost:8000/docs

## 💻 Testing

## 🎯 Project Scope

This is a **junior-level backend project** created to demonstrate the ability to build and organize a basic REST API.

It is not intended to be presented as a production-ready system. Instead, it serves as a foundation for progressively more advanced projects involving authentication, testing, architecture, deployment, and scalability.

---

## 📡 API Endpoints

## Workspaces

| Method          | Endpoint                          | Description       |
| --------------- | -------------                     | ----------------- |
| `GET`           | `/api/v1.0/workspaces`            | Get all tasks     |
| `GET`           | `/api/v1.0/workspaces{task_id}`   | Get a task by ID  |
| `POST`          | `/api/v1.0/workspaces`            | Create a newtask  |
| `PUT` / `PATCH` | `/api/v1.0/workspaces{task_id}`   | Update atask      |
| `DELETE`        | `/api/v1.0/workspaces{task_id}`   | Delete atask      |

### Tasks

| Method          | Endpoint                     | Description       |
| --------------- | -------------                | ----------------- |
| `GET`           | `/api/v1.0/tasks`            | Get all tasks     |
| `GET`           | `/api/v1.0/tasks{task_id}`   | Get a task by ID  |
| `POST`          | `/api/v1.0/tasks`            | Create a newtask  |
| `PUT` / `PATCH` | `/api/v1.0/tasks{task_id}`   | Update atask      |
| `DELETE`        | `/api/v1.0/tasks{task_id}`   | Delete atask      |

## 📄 License

This project is licensed under the [MIT License](LICENSE).