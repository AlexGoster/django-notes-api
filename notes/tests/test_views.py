"""Тесты API-запросов для заметок."""

import pytest
from django.urls import reverse
from rest_framework import status
from notes.models import Note
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestNoteViews:
    """Тесты API-представлений заметок."""

    def test_register(self, api_client):
        """Регистрация нового пользователя."""
        response = api_client.post(
            reverse("register"),
            {"username": "newuser", "email": "new@example.com", "password": "newpass123"},
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert "refresh" in response.json()
        assert "access" in response.json()
        assert User.objects.filter(username="newuser").exists()

    def test_login(self, api_client):
        """Авторизация пользователя."""
        api_client.post(
            reverse("register"),
            {"username": "testuser", "email": "test@example.com", "password": "testpass123"},
        )
        response = api_client.post(
            reverse("login"),
            {"username": "testuser", "password": "testpass123"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.json()
        assert "refresh" in response.json()

    def test_register_invalid_data(self, api_client):
        """Регистрация с некорректными данными."""
        response = api_client.post(
            reverse("register"),
            {"username": "", "email": "invalid", "password": "short"},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_invalid_credentials(self, api_client):
        """Авторизация с некорректными учётными данными."""
        response = api_client.post(
            reverse("login"),
            {"username": "testuser", "password": "wrongpassword"},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_note(self, auth_client):
        """Создание новой заметки."""
        response = auth_client.post(
            reverse("note-list"),
            {"title": "New Note", "content": "New content"},
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Note.objects.filter(title="New Note").exists()

    def test_list_notes(self, auth_client):
        """Получение списка заметок."""
        Note.objects.create(title="Note 1", content="Content 1", author=auth_client.user)
        Note.objects.create(title="Note 2", content="Content 2", author=auth_client.user)
        response = auth_client.get(reverse("note-list"))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()["results"]) == 2

    def test_retrieve_note(self, auth_client):
        """Получение одной заметки."""
        note = Note.objects.create(title="Test Note", content="Test content", author=auth_client.user)
        response = auth_client.get(reverse("note-detail", args=[note.id]))
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["title"] == "Test Note"

    def test_update_note(self, auth_client):
        """Обновление заметки."""
        note = Note.objects.create(title="Original", content="Original content", author=auth_client.user)
        response = auth_client.put(
            reverse("note-detail", args=[note.id]),
            {"title": "Updated Note", "content": "Updated content"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert Note.objects.get(id=note.id).title == "Updated Note"

    def test_partial_update_note(self, auth_client):
        """Частичное обновление заметки."""
        note = Note.objects.create(title="Original", content="Original content", author=auth_client.user)
        response = auth_client.patch(
            reverse("note-detail", args=[note.id]),
            {"is_archived": True},
        )
        assert response.status_code == status.HTTP_200_OK
        assert Note.objects.get(id=note.id).is_archived is True

    def test_delete_note(self, auth_client):
        """Удаление заметки."""
        note = Note.objects.create(title="To Delete", content="Content", author=auth_client.user)
        response = auth_client.delete(reverse("note-detail", args=[note.id]))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Note.objects.filter(id=note.id).exists()

    def test_unauthorized_access(self, api_client):
        """Доступ без авторизации запрещён."""
        response = api_client.get(reverse("note-list"))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_other_user_cannot_access(self, auth_client):
        """Пользователь не может получить доступ к заметкам других."""
        other_user = User.objects.create_user(
            username="otheruser", email="other@example.com", password="otherpass123"
        )
        other_note = Note.objects.create(
            title="Other Note", content="Other content", author=other_user
        )
        response = auth_client.get(reverse("note-detail", args=[other_note.id]))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_filter_archived_notes(self, auth_client):
        """Фильтрация заметок по архиву."""
        Note.objects.create(title="Archived", content="Content", author=auth_client.user, is_archived=True)
        Note.objects.create(title="Active", content="Content", author=auth_client.user, is_archived=False)
        response = auth_client.get(reverse("note-list") + "?is_archived=true")
        assert response.status_code == status.HTTP_200_OK
        results = response.json()["results"]
        assert all(n["is_archived"] for n in results)

    def test_list_archived_endpoint(self, auth_client):
        """Эндпоинт для архивных заметок."""
        Note.objects.create(title="Archived 1", content="Content", author=auth_client.user, is_archived=True)
        Note.objects.create(title="Archived 2", content="Content", author=auth_client.user, is_archived=True)
        response = auth_client.get(reverse("note-list-archive"))
        assert response.status_code == status.HTTP_200_OK
        results = response.json()
        assert len(results) == 2
        assert all(n["is_archived"] for n in results)
