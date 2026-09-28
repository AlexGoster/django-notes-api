"""Тестовые конфигурации и фикстуры для pytest."""

import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    """Предоставляет экземпляр API-клиента."""
    return APIClient()


@pytest.fixture
def auth_client(api_client):
    """Предоставляет авторизованный API-клиент.

    Создаёт пользователя, регистрирует его и возвращает клиента с JWT-токенами.
    """
    user = User.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )
    register_url = "/api/auth/register/"
    login_url = "/api/auth/login/"
    api_client.post(
        register_url,
        {"username": "testuser", "email": "test@example.com", "password": "testpass123"},
    )
    response = api_client.post(login_url, {"username": "testuser", "password": "testpass123"})
    token = response.json()["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    api_client.user = user
    return api_client


@pytest.fixture
def create_note(auth_client):
    """Создаёт заметку для авторизованного пользователя.

    Returns:
        Созданный экземпляр заметки.
    """
    def _create_note(**kwargs):
        from notes.models import Note
        return Note.objects.create(author=auth_client.user, **kwargs)
    return _create_note
