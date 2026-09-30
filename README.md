# 📝 Task Management REST API

A clean, modern, beginner-friendly RESTful API for managing tasks, built with **Python**, **FastAPI**, **SQLAlchemy**, **Pydantic v2**, and **SQLite**.

---

## 📌 1. Project Overview

The **Task Management API** provides a complete RESTful backend solution to create, read, update, delete, complete, and filter tasks. It follows industry-standard Python backend patterns, including strict request/response data validation, separation of ORM models from API schemas, modular router structures, and automated in-memory unit testing.

---

## ✨ 2. Features

- **Health Monitoring**: `GET /` root endpoint confirming API status.
- **Task Creation**: Create tasks with title validation (1–255 chars) and optional descriptions.
- **Task Retrieval**: Get all tasks, or retrieve a single task by its unique ID.
- **Status Filtering**: Filter tasks by completion status (`GET /tasks?completed=true` or `GET /tasks?completed=false`).
- **Task Updating**: Update title, description, or completion status with automatic `updated_at` timestamp management.
- **Task Completion Endpoint**: Quick action endpoint to mark a task as completed (`PATCH /tasks/{id}/complete`).
- **Task Deletion**: Remove tasks by ID with proper `204 No Content` HTTP responses.
- **Error Handling**: Friendly and standard JSON error payloads for `404 Not Found` and `422 Validation Error`.
- **Interactive Documentation**: Instant Swagger UI (`/docs`) and ReDoc (`/redoc`).
- **Isolated Testing Suite**: 19 automated Pytest test cases using an in-memory SQLite database.

---

## 🛠 3. Technology Stack

| Technology | Role |
| :--- | :--- |
| **Python 3.10+** | Programming Language |
| **FastAPI** | High-performance Web Framework |
| **Uvicorn** | ASGI Web Server |
| **SQLAlchemy 2.0** | Object-Relational Mapper (ORM) |
| **SQLite** | Embedded Relational Database |
| **Pydantic v2** | Data Validation & Settings Management |
| **Pytest & HTTPX** | Automated Testing Framework |

---

## 📂 4. Project Structure

```text
backend_tasks/
├── app/
│   ├── __init__.py        # Package marker
│   ├── main.py            # FastAPI entry point, lifespan, & root endpoint
│   ├── config.py          # Application configuration (Pydantic BaseSettings)
│   ├── database.py        # SQLAlchemy engine, session maker, & get_db dependency
│   ├── models.py          # SQLAlchemy ORM Task model
│   ├── schemas.py         # Pydantic validation & response schemas
│   ├── crud.py            # Database CRUD helper functions
│   └── routers/
│       ├── __init__.py    # Package marker
│       └── tasks.py       # REST API endpoint handlers
├── tests/
│   ├── __init__.py        # Package marker
│   ├── conftest.py        # Pytest fixtures (in-memory SQLite StaticPool & TestClient)
│   ├── test_health.py     # Test case for root GET / endpoint
│   ├── test_models.py     # Test case for ORM database persistence
│   └── test_tasks.py      # Test suite covering all 13 task API operations
├── .env.example           # Example environment variables
├── .gitignore             # Version control exclusions
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

---

## ⚙️ 5. Installation & Setup

### Prerequisites
- **Python 3.10** or higher installed on your system.

---

## 🐍 6. How to Create and Activate the Virtual Environment

Open your terminal in the project root directory (`backend_tasks`):

### Step 1: Create Virtual Environment
```bash
python -m venv .venv
```

### Step 2: Activate Virtual Environment

- **Windows (PowerShell)**:
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
- **Windows (Command Prompt / CMD)**:
  ```cmd
  .venv\Scripts\activate.bat
  ```
- **macOS / Linux (Bash or Zsh)**:
  ```bash
  source .venv/bin/activate
  ```

---

## 📦 7. How to Install Dependencies

With the virtual environment activated, run:

```bash
pip install -r requirements.txt
```

---

## 🚀 8. How to Start the FastAPI Server

Start the local Uvicorn development server with auto-reload enabled:

```bash
uvicorn app.main:app --reload
```

Output confirming startup:
```text
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [...]
INFO:     Application startup complete.
```

---

## 📖 9. Swagger / OpenAPI Documentation URL

Once the server is running, access the interactive API documentation directly in your browser:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc Documentation**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📑 10. API Endpoints Overview

| Method | Endpoint | Success Status | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | `200 OK` | API Health Check / Welcome message |
| `POST` | `/tasks/` | `201 Created` | Create a new task |
| `GET` | `/tasks/` | `200 OK` | Get all tasks (supports `?completed=true/false`) |
| `GET` | `/tasks/{task_id}` | `200 OK` | Retrieve single task by ID |
| `PUT` | `/tasks/{task_id}` | `200 OK` | Update task title, description, or completion status |
| `PATCH` | `/tasks/{task_id}/complete` | `200 OK` | Mark task completion status as `true` |
| `DELETE` | `/tasks/{task_id}` | `204 No Content` | Delete a task by ID |

---

## 💡 11. Example Request & Response Payloads

### 1. Create Task (`POST /tasks/`)
**Request Body**:
```json
{
  "title": "Build Task API",
  "description": "Implement CRUD endpoints and automated test suite"
}
```

**Response (`201 Created`)**:
```json
{
  "id": 1,
  "title": "Build Task API",
  "description": "Implement CRUD endpoints and automated test suite",
  "is_completed": false,
  "created_at": "2026-09-30T02:00:00Z",
  "updated_at": "2026-09-30T02:00:00Z"
}
```

---

### 2. Get All Tasks with Status Filter (`GET /tasks/?completed=true`)
**Response (`200 OK`)**:
```json
[
  {
    "id": 1,
    "title": "Build Task API",
    "description": "Implement CRUD endpoints and automated test suite",
    "is_completed": true,
    "created_at": "2026-09-30T02:00:00Z",
    "updated_at": "2026-09-30T02:05:00Z"
  }
]
```

---

### 3. Mark Task as Completed (`PATCH /tasks/1/complete`)
**Response (`200 OK`)**:
```json
{
  "id": 1,
  "title": "Build Task API",
  "description": "Implement CRUD endpoints and automated test suite",
  "is_completed": true,
  "created_at": "2026-09-30T02:00:00Z",
  "updated_at": "2026-09-30T02:05:00Z"
}
```

---

### 4. Resource Not Found Error (`404 Not Found`)
**Response (`404 Not Found`)**:
```json
{
  "detail": "Task with ID 999 not found"
}
```

---

### 5. Validation Error (`422 Unprocessable Entity`)
**Response (`422 Unprocessable Entity`)**:
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "Field required",
      "type": "missing"
    }
  ]
}
```

---

## 🧪 12. How to Run Tests

Run the complete automated Pytest suite:

```bash
pytest
```

To view verbose output showing individual test names:
```bash
pytest -v
```

Expected Output:
```text
tests/test_health.py::test_read_root PASSED                              [  5%]
tests/test_models.py::test_create_task_in_db PASSED                      [ 10%]
tests/test_tasks.py::test_create_task PASSED                             [ 15%]
...
======================== 19 passed in 0.82s ========================
```

---

## 🗄 13. Database Information

- **Database Engine**: SQLite (`sqlite:///./tasks.db`).
- **Table Initialization**: Database tables are automatically initialized on application startup via SQLAlchemy `Base.metadata.create_all(bind=engine)`.
- **Test Isolation**: Automated unit tests execute against an isolated in-memory SQLite database (`sqlite:///:memory:`) using `StaticPool`, ensuring your local development database (`tasks.db`) is never corrupted by test runs.

---

## 💻 14. Example Usage (`cURL` Commands)

### Create a Task:
```bash
curl -X POST "http://127.0.0.1:8000/tasks/" \
     -H "Content-Type: application/json" \
     -d '{"title": "Learn FastAPI", "description": "Read documentation and build sample app"}'
```

### Get All Pending Tasks:
```bash
curl -X GET "http://127.0.0.1:8000/tasks/?completed=false"
```

### Mark Task #1 as Completed:
```bash
curl -X PATCH "http://127.0.0.1:8000/tasks/1/complete"
```

### Delete Task #1:
```bash
curl -X DELETE "http://127.0.0.1:8000/tasks/1"
```
