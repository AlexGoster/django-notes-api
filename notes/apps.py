"""Конфигурация приложения notes для Django Notes API."""

from django.apps import AppConfig


class NotesConfig(AppConfig):
    """Конфигурация приложения notes.

    Атрибуты:
        default_auto_field: Тип автоматического поля по умолчанию.
        name: Имя приложения.
        verbose_name: Человекочитаемое имя приложения.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "notes"
    verbose_name = "Заметки"

    def ready(self) -> None:
        """Инициализирует приложение notes."""
        pass
