from django.urls import path

from .views import (
    AdminCategoryCreateView,
    AdminCategoryUpdateDeleteView,
    CategoryDetailView,
    CategoryListView,
)

urlpatterns = [
    path("categories", CategoryListView.as_view()),
    path("categories/<str:idor>", CategoryDetailView.as_view()),
    path("admin/categories", AdminCategoryCreateView.as_view()),
    path("admin/categories/<int:pk>", AdminCategoryUpdateDeleteView.as_view()),
]
