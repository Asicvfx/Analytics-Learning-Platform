from django.urls import path

from .views import (
    AdminLearningUpdateView,
    AdminLearningUpsertView,
    DashboardLearningView,
)

urlpatterns = [
    path("dashboards/<int:dashboard_id>/learning", DashboardLearningView.as_view()),
    path("admin/dashboards/<int:dashboard_id>/learning",
         AdminLearningUpsertView.as_view()),
    path("admin/learning/<int:learning_id>", AdminLearningUpdateView.as_view()),
]
