# TaskFlow API

A scalable, clean-architecture Django REST API for task management.

## Features
- JWT user authentication
- CRUD for tasks
- Task prioritization
- Filtering & pagination
- Role-based permissions
- Swagger API docs

## Tech Stack
- Django + DRF
- PostgreSQL
- Pytest, Factory Boy, Coverage.py
- Pre-commit hooks
- Docker
- drf-yasg for Swagger

## Repo Structure
```
taskflow-api/
 ├── app/
 │   ├── domain/
 │   ├── services/
 │   ├── api/
 │   ├── tests/
 ├── docker-compose.yml
 ├── Dockerfile
 ├── .github/workflows/ci.yml
```

## Setup
1. Create and activate a Python virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Start the server: `python manage.py runserver`

## Testing
- Run tests: `pytest`
- Coverage: `coverage run -m pytest && coverage report`

## Code Quality
- Pre-commit hooks: `pre-commit install`

## API Docs
- Swagger: `/swagger/` endpoint after starting the server

---
For more details, see the copilot-instructions.md in `.github/`.
