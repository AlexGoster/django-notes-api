"""Тесты моделей Note."""

from django.db import connection
from django.test import TestCase
from django.contrib.auth import get_user_model
from notes.models import Note

User = get_user_model()


class NoteModelTest(TestCase):
    """Тесты модели Note."""

    def setUp(self) -> None:
        """Подготавливает тестовые данные."""
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.note = Note.objects.create(
            title="Test Note",
            content="Test content",
            author=self.user,
        )

    def test_note_creation(self) -> None:
        """Проверяет корректность создания заметки."""
        self.assertEqual(str(self.note), "Test Note")
        self.assertEqual(self.note.title, "Test Note")
        self.assertEqual(self.note.content, "Test content")
        self.assertFalse(self.note.is_archived)

    def test_note_archived(self) -> None:
        """Проверяет архивацию заметки."""
        self.note.is_archived = True
        self.note.save()
        self.assertTrue(self.note.is_archived)

    def test_note_str(self) -> None:
        """Проверяет строковое представление заметки."""
        self.assertEqual(str(self.note), "Test Note")

    def test_note_ordering(self) -> None:
        """Проверяет сортировку заметок по дате создания."""
        note2 = Note.objects.create(
            title="Another Note",
            content="Another content",
            author=self.user,
        )
        self.assertNotEqual(
            list(Note.objects.order_by("-created_at").values_list("id", flat=True))[0],
            note2.id,
        )

    def test_note_author_relation(self) -> None:
        """Проверяет связь с автором."""
        self.assertEqual(self.note.author, self.user)
        self.assertIn(self.note, self.user.notes.all())

    def test_note_default_values(self) -> None:
        """Проверяет значения по умолчанию."""
        self.assertFalse(self.note.is_archived)
        self.assertIsNotNone(self.note.created_at)
        self.assertIsNotNone(self.note.updated_at)

    def test_note_fields(self) -> None:
        """Проверяет наличие всех полей."""
        fields = [f.name for f in Note._meta.get_fields()]
        self.assertIn("title", fields)
        self.assertIn("content", fields)
        self.assertIn("created_at", fields)
        self.assertIn("updated_at", fields)
        self.assertIn("is_archived", fields)
        self.assertIn("author", fields)
