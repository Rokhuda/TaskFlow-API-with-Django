# TaskFlow API

A scalable Django REST API for task management using clean architecture.

## Features
- JWT authentication
- Task CRUD operations
- Task priority quadrant support
- Sprint and project management
- Swagger API documentation
- Pytest test coverage

## Tech Stack
- Python 3.12
- Django 6.0
- Django REST Framework
- drf-yasg for Swagger
- Pytest for testing
- Docker / Docker Compose support

## Repository Structure
```
app/
  domain/      # models and business domain logic
  api/         # serializers and viewsets
  services/    # helper services and business utilities
  tests/       # unit and BDD tests
Dockerfile
docker-compose.yml
manage.py
requirements.txt
README.md
```

## Setup and Run
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

## API Documentation
- Open Swagger UI at: `http://127.0.0.1:8000/swagger/`

## Testing
- Run all tests: `pytest -q`
- Run Django checks: `python manage.py check`

## Docker
- Build and start containers: `docker compose up --build`

## Notes
- Local virtual environments and generated files should not be committed.
- The current workflow uses the `app/` package as the Django project application root.
