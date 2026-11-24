from django.contrib.auth import get_user_model
from django.db import models


class Note(models.Model):
    """Модель заметки пользователя.

    Атрибуты:
        title: Заголовок заметки.
        content: Основное содержание заметки.
        created_at: Дата и время создания заметки.
        updated_at: Дата и время последнего обновления.
        is_archived: Архивирована ли заметка.
        author: Автор заметки.
    """

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    is_archived = models.BooleanField(default=False, verbose_name="В архиве")
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="notes",
        verbose_name="Автор",
    )

    class Meta:
        """Мета-опции модели Note."""

        ordering = ["-created_at", "-id"]
        verbose_name = "Заметка"
        verbose_name_plural = "Заметки"

    def __str__(self) -> str:
        """Возвращает строковое представление заметки."""
        return self.title
