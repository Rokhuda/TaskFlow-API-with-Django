# TaskFlow API

TaskFlow is a scalable Django REST API for managing projects, sprints, and tasks. It uses a clean architecture pattern to keep domain logic, API definitions, and service helpers separated and easy to maintain.

## What this project does
- Manage projects and enforce owner-based permissions
- Create and track sprints with lifecycle actions like start and complete
- Create tasks, attach blockers, and automatically compute priority quadrants
- Track task completion, sprint progress, and burndown metrics
- Provide a Swagger UI for exploring the API endpoints

## Model relationships
- `Project` is the top-level container owned by a user.
- `Sprint` belongs to a `Project` and tracks an iteration with start/end dates, status, and capacity.
- `Task` belongs to a `Sprint` and can also be linked to other tasks as blockers.
- Projects, sprints, and tasks are all filtered by owner permissions, with staff users able to see all data.

## Directory layout
```
app/
  api/           # DRF viewsets, serializers, and API layer
  domain/        # core models for Task, Sprint, Project, and shared utilities
    common/      # shared model mixins like timestamped base models
    project/     # project domain model and project metadata
    sprint/      # sprint domain models, sprint metrics, and burndown logic
  services/      # reusable domain services such as priority scoring
  tests/         # API tests and behavior-driven tests
Dockerfile
docker-compose.yml
manage.py
requirements.txt
README.md
```

## Setup and run locally
1. Open a terminal in the project root.
2. Create a virtual environment:
   - Linux / macOS / WSL: `python3 -m venv .venv`
   - Windows PowerShell: `python -m venv .venv`
3. Activate the environment:
   - Linux / macOS / WSL: `source .venv/bin/activate`
   - Windows PowerShell: `.\.venv\Scripts\Activate.ps1`
4. Install dependencies:
   - `pip install -r requirements.txt`
5. Apply database migrations:
   - `python manage.py migrate`
6. Create a superuser (optional):
   - `python manage.py createsuperuser`
7. Start the development server:
   - `python manage.py runserver`

## View the API
- Open Swagger UI at: `http://127.0.0.1:8000/swagger/`
- This endpoint is the main TaskFlow API interface and documentation.

## Docker
- Build and start containers from WSL or a Linux shell: `docker compose up --build`
- If using Docker Desktop with WSL integration, run the command from WSL for the best compatibility.
- The same API is available at `http://127.0.0.1:8000/swagger/` once the containers are running.

## Testing
- Run all tests: `pytest -q`
- Run Django checks: `python manage.py check`

## Notes
- The `app/` package is the Django project root.
- Local virtual environments, generated database files, and IDE metadata should not be committed.
