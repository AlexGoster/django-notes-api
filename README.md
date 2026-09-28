# Django Notes API

[![CI](https://github.com/AlexGoster/django-notes-api/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/AlexGoster/django-notes-api/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/AlexGoster/django-notes-api/branch/main/graph/badge.svg)](https://codecov.io/gh/AlexGoster/django-notes-api)
[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.1-blue)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/Docker-supported-green)](https://www.docker.com/)

**REST API для заметок** на Django REST Framework с JWT-аутентификацией, админкой и Swagger.

## Стек технологий

- **Python 3.12** + **Django 5.1** + **DRF 3.15**
- **PostgreSQL 16**
- **djangorestframework-simplejwt** — JWT auth
- **drf-spectacular** — Swagger/OpenAPI
- **django-filter** — фильтрация
- **Docker** + **docker-compose**
- **Pytest** + **pytest-django** + **ruff** + **mypy**

## Быстрый старт

```bash
git clone https://github.com/AlexGoster/django-notes-api.git
cd django-notes-api
docker-compose up --build
```

После запуска:
- **Swagger**: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
- **Django Admin**: [http://localhost:8000/admin/](http://localhost:8000/admin/)
- **API**: [http://localhost:8000/api/notes/](http://localhost:8000/api/notes/)

## Как потыкать локально

### Регистрация
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user1", "email": "u@e.com", "password": "password123"}'
```

### Логин
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -d "username=user1&password=password123"
```

### Создание заметки (подставьте свой token)
```bash
curl -X POST http://localhost:8000/api/notes/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Моя заметка", "content": "Текст заметки"}'
```

### Получение списка с фильтрацией
```bash
curl "http://localhost:8000/api/notes/?is_archived=false&page=1&page_size=10" \
  -H "Authorization: Bearer <token>"
```

### В Swagger (/api/docs)
Откройте http://localhost:8000/api/docs/ — видите все эндпоинты, можете попробовать прямо в браузере.

## Как задеплоить на Render/Railway бесплатно

### Render
1. Подключите репозиторий на [render.com](https://render.com)
2. **Web Service** → Dockerfile → автоопределение
3. Добавьте `DATABASE_URL`, `SECRET_KEY`, `DEBUG` в Environment
4. Используйте **Render PostgreSQL** (бесплатный tier)
5. Deploy при пуше в `main`

### Railway
1. На [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub Repo**
2. Railway найдёт `docker-compose.yml`
3. Подключите PostgreSQL через Variables
4. Deploy при пуше

## Бейджи

| CI | Coverage | Docker |
|---|---|---|
| ![CI](https://github.com/AlexGoster/django-notes-api/actions/workflows/ci.yml/badge.svg) | ![Coverage](https://codecov.io/gh/AlexGoster/django-notes-api/branch/main/graph/badge.svg) | ![Docker](https://img.shields.io/badge/docker-compose-up--build-blue) |

## Структура проекта

```
django-notes-api/
├── notes/
│   ├── models.py      # Note модель
│   ├── serializers.py  # DRF сериализаторы
│   ├── views.py        # ViewSet с CRUD
│   ├── urls.py         # Маршруты /api/notes/, /api/auth/
│   ├── permissions.py  # IsOwnerOrReadOnly
│   └── tests/
├── config/
│   ├── settings.py     # Django settings
│   ├── urls.py         # Корневые маршруты
│   └── asgi.py
├── manage.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```
