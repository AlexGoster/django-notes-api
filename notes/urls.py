from django.urls import include, path
from rest_framework.routers import DefaultRouter

from notes.views import NoteViewSet, UserLoginView, UserRegistrationView

router = DefaultRouter()
router.register(r"notes", NoteViewSet, basename="note")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/register/", UserRegistrationView.as_view(), name="register"),
    path("auth/login/", UserLoginView.as_view(), name="login"),
]
