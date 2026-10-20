from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User as AuthUser
from rest_framework import serializers

from notes.models import Note

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer[AuthUser]):
    """Сериализатор для регистрации пользователя."""

    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )

    class Meta:
        """Мета-опции сериализатора регистрации."""

        model = User
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"email": {"required": True}}

    def create(self, validated_data: dict[str, Any]) -> AuthUser:
        """Создаёт нового пользователя на основе валидированных данных.

        Args:
            validated_data: Валидированные данные пользователя.

        Returns:
            Созданный экземпляр пользователя.
        """
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.Serializer[dict[str, Any]]):
    """Сериализатор для авторизации пользователя."""

    username = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"})

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        """Валидирует учётные данные пользователя.

        Args:
            data: Данные для входа, содержащие имя пользователя и пароль.

        Returns:
            Валидированные данные.

        Raises:
            ValidationError: Если учётные данные неверны.
        """
        from django.contrib.auth import authenticate

        user = authenticate(username=data["username"], password=data["password"])
        if user is None:
            raise serializers.ValidationError("Неверные учётные данные")
        data["user"] = user
        return data


class UserSerializer(serializers.ModelSerializer[AuthUser]):
    """Сериализатор для представления пользователя."""

    class Meta:
        """Мета-опции сериализатора пользователя."""

        model = User
        fields = ("id", "username", "email")


class NoteSerializer(serializers.ModelSerializer[Note]):
    """Сериализатор для модели Note."""

    author = UserSerializer(read_only=True)

    class Meta:
        """Мета-опции сериализатора заметок."""

        model = Note
        fields = ("id", "title", "content", "created_at", "updated_at", "is_archived", "author")
        read_only_fields = ("id", "created_at", "updated_at", "author")

    def create(self, validated_data: dict[str, Any]) -> Note:
        """Создаёт новую заметку на основе валидированных данных.

        Args:
            validated_data: Валидированные данные заметки.

        Returns:
            Созданный экземпляр заметки.
        """
        validated_data["author"] = self.context["request"].user
        return Note.objects.create(**validated_data)


class TokenPairSerializer(serializers.Serializer[dict[str, Any]]):
    access = serializers.CharField()
    refresh = serializers.CharField()


class RegistrationResponseSerializer(TokenPairSerializer):
    user = UserSerializer()
