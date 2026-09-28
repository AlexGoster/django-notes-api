from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Класс разрешений, позволяющий владельцам редактировать свои заметки.

    Владельцы могут выполнять все операции со своими заметками.
    Другие пользователи могут только читать заметки.
    """

    def has_object_permission(self, request, view, obj) -> bool:
        """Проверяет, имеет ли пользователь разрешение на объект.

        Args:
            request: HTTP-запрос.
            view: Просматриваемый представление.
            obj: Объект, к которому обращаются.

        Returns:
            True, если пользователь является владельцем или запрос безопасный, иначе False.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
