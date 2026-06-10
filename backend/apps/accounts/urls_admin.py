from django.urls import path

from .views_admin import AdminUserListCreateView, AdminUserUpdateView

urlpatterns = [
    path("admin/users", AdminUserListCreateView.as_view()),
    path("admin/users/<int:pk>", AdminUserUpdateView.as_view()),
]
