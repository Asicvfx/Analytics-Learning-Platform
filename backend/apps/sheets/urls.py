from django.urls import path

from .views import (
    AdminSheetCreateView,
    AdminSheetUpdateDeleteView,
    DashboardSheetListView,
)

urlpatterns = [
    path("dashboards/<int:dashboard_id>/sheets", DashboardSheetListView.as_view()),
    path("admin/dashboards/<int:dashboard_id>/sheets",
         AdminSheetCreateView.as_view()),
    path("admin/sheets/<int:sheet_id>", AdminSheetUpdateDeleteView.as_view()),
]
