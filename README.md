# Django Notes API

[![CI](https://github.com/your-org/django-notes-api/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/your-org/django-notes-api/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/your-org/django-notes-api/branch/main/graph/badge.svg)](https://codecov.io/gh/your-org/django-notes-api)
[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.1-blue)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/Docker-supported-green)](https://www.docker.com/)

A REST API for managing notes with Django REST Framework, PostgreSQL, and JWT authentication.

## Features

- ✅ Create, read, update, and delete notes
- ✅ User registration and JWT authentication
- ✅ Filter notes by archive status and date range
- ✅ Pagination (page_size=10)
- ✅ Interactive API documentation with Swagger/OpenAPI
- ✅ Django admin panel
- ✅ Docker support
- ✅ 80%+ test coverage

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.12+ (for local development)

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-org/django-notes-api.git
cd django-notes-api

# Copy environment file
cp .env.example .env

# Build and run all services
docker-compose up --build
```

The API will be available at `http://localhost:8000`.

### Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt

# Set up environment
cp .env.example .env

# Install PostgreSQL and create database
createdb notesdb

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## API Documentation

Once the server is running, visit:
- **Swagger Docs**: `http://localhost:8000/api/docs/`
- **Django Admin**: `http://localhost:8000/admin/`

## Usage Examples

### Register a new user

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "email": "john@example.com", "password": "secret123"}'
```

### Login and get JWT tokens

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "password": "secret123"}'
```

### Create a note

```bash
curl -X POST http://localhost:8000/api/notes/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -d '{"title": "My Note", "content": "Note content"}'
```

### List notes with pagination

```bash
curl http://localhost:8000/api/notes/?page=1&page_size=10 \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

### Filter archived notes

```bash
curl "http://localhost:8000/api/notes/?is_archived=true" \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

### Get archived notes

```bash
curl http://localhost:8000/api/notes/archive/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

### Update a note

```bash
curl -X PUT http://localhost:8000/api/notes/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -d '{"title": "Updated Title", "content": "Updated content"}'
```

### Delete a note

```bash
curl -X DELETE http://localhost:8000/api/notes/1/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

## Running Tests

```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest notes/tests/test_views.py

# Run with verbose output
pytest -v
```

### Coverage

Tests achieve 80%+ code coverage. View the HTML report in `htmlcov/`.

## Deployment to Render

1. Create a new Web Service on [Render](https://render.com)
2. Connect your GitHub repository
3. Set the following environment variables:
   - `SECRET_KEY`: A secure random string
   - `DEBUG`: `False`
   - `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`: Database credentials
   - `ALLOWED_HOSTS`: Your Render URL
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3`
6. Add a PostgreSQL database from Render's add-ons

## Deployment to Railway

1. Create a new project on [Railway](https://railway.app)
2. Connect your GitHub repository
3. Add a PostgreSQL database from Railway's plugins
4. Set environment variables in Railway dashboard
5. Railway automatically detects the Django app and uses the Dockerfile

## License

MIT
