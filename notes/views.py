from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from notes.models import Note
from notes.permissions import IsOwnerOrReadOnly
from notes.serializers import NoteSerializer, UserLoginSerializer, UserRegistrationSerializer, UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class StandardResultsSetPagination(PageNumberPagination):
    """Конфигурация пагинации для API."""

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class NoteViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Note.

    Предоставляет операции CRUD для заметок с фильтрацией и пагинацией.
    """

    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["is_archived", "created_at"]

    def get_queryset(self):
        """Фильтрует заметки по текущему пользователю.

        Returns:
            QuerySet заметок, принадлежащих текущему пользователю.
        """
        return self.queryset.filter(author=self.request.user)

    def perform_create(self, serializer) -> None:
        """Назначает текущего пользователя автором при создании заметки.

        Args:
            serializer: Экземпляр сериализатора заметки.
        """
        serializer.save(author=self.request.user)

    @action(detail=False, methods=["get"], url_path="archive")
    def list_archived(self, request):
        """Возвращает все заархивированные заметки текущего пользователя.

        Args:
            request: HTTP-запрос.

        Returns:
            Response с заархивированными заметками.
        """
        queryset = self.get_queryset().filter(is_archived=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserRegistrationView(APIView):
    """API представление для регистрации пользователя."""

    permission_classes = []

    def post(self, request):
        """Регистрирует нового пользователя.

        Args:
            request: HTTP-запрос с данными пользователя.

        Returns:
            Response с данными пользователя и токенами авторизации.
        """
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": UserSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )


class UserLoginView(APIView):
    """API представление для авторизации пользователя."""

    permission_classes = []

    def post(self, request):
        """Выполняет аутентификацию пользователя и возвращает JWT-токены.

        Args:
            request: HTTP-запрос с учётными данными.

        Returns:
            Response с JWT-токенами.
        """
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )
