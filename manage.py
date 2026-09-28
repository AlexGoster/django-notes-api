"""Управление административными задачами для проекта Django Notes API."""

import os
import sys


def main() -> None:
    """Запускает административные задачи.

    Args:
        Незначимые аргументы командной строки.
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Не удалось импортировать Django. Убедитесь, что он установлен "
            "и доступен в переменной окружения PYTHONPATH. "
            "Возможно, вы забыли активировать виртуальное окружение."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
