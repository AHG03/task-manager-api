# Task Manager API

A RESTful task management API built with **Python and FastAPI**, featuring user authentication, CRUD operations, filtering, sorting, pagination, input validation, and automated tests.

## Overview

This project is a backend API for managing personal tasks.

Users can register and authenticate, create and manage their own tasks, and retrieve tasks using filtering, sorting, and pagination options.

The project was built to practice backend development concepts including REST API design, database integration, authentication, validation, and automated testing.

## Features

### User Authentication

* User registration
* Password hashing
* JWT-based authentication
* Protected endpoints
* Token expiration handling
* Invalid token handling
* Duplicate username validation

### Task Management

* Create tasks
* Retrieve tasks
* Update tasks
* Partially update tasks
* Delete tasks
* Retrieve the authenticated user's profile

### Filtering & Pagination

* Search tasks
* Filter by completion status
* Sort by supported task fields
* Ascending and descending sorting
* Limit and offset pagination

### Validation & Testing

* Request validation with Pydantic
* Error handling for invalid requests and missing resources
* Automated tests with pytest
* Tests covering authentication, authorization, CRUD operations, validation, filtering, sorting, pagination, and security-related cases

## Tech Stack

| Technology | Purpose                     |
| ---------- | --------------------------- |
| Python     | Backend development         |
| FastAPI    | REST API framework          |
| SQLAlchemy | Database ORM                |
| SQLite     | Database                    |
| Pydantic   | Data validation and schemas |
| JWT        | Authentication              |
| pytest     | Automated testing           |
| Uvicorn    | ASGI server                 |

## Project Structure

```text
task-manager-api/
├── app/
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── security.py
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_security.py
│   ├── test_tasks.py
│   └── test_users.py
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/AHG03/task-manager-api.git
cd task-manager-api
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the API

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI also provides interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

## Running the Tests

Run the complete test suite with:

```bash
pytest
```

The test suite covers:

* User registration and authentication
* Password hashing
* JWT authentication
* Token expiration and invalid tokens
* Task CRUD operations
* Request validation
* Filtering
* Sorting
* Pagination
* Missing resources and error handling

## Example API Endpoints

### Authentication

```text
POST /register
```

Register a new user.

### Current User

```text
GET /me
```

Retrieve information about the authenticated user.

### Tasks

```text
GET    /tasks
POST   /tasks
GET    /tasks/{task_id}
PUT    /tasks/{task_id}
PATCH  /tasks/{task_id}
DELETE /tasks/{task_id}
```

The task listing endpoint supports options such as:

```text
/tasks?completed=true
/tasks?search=project
/tasks?sort_by=created_at&sort_order=desc
/tasks?limit=10&offset=20
```

## What I Practiced

This project helped me develop practical experience with:

* Designing RESTful APIs
* Structuring a FastAPI application
* Working with relational databases through SQLAlchemy
* Implementing authentication and authorization
* Validating API input
* Writing automated tests
* Debugging API behavior
* Implementing filtering, sorting, and pagination
* Organizing backend code into separate modules

## Future Improvements

Possible next steps include:

* Add a production-ready database configuration
* Improve configuration and secret management
* Add API versioning
* Add more comprehensive API documentation
* Add integration/deployment configuration
* Expand test coverage as new features are introduced

## Status

**Completed**

The current version implements the core task management, authentication, validation, filtering, sorting, pagination, and testing functionality.
