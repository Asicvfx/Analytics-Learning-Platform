from django.urls import path

from .views_auth import LoginView, LogoutView, MeView

urlpatterns = [
    path("login", LoginView.as_view()),
    path("logout", LogoutView.as_view()),
    path("me", MeView.as_view()),
]
