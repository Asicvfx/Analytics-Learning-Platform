from django.urls import path

from .views import (
    AdminDashboardCreateView,
    AdminDashboardUpdateDeleteView,
    DashboardCatalogView,
    DashboardDataView,
    DashboardDetailView,
    DashboardExportView,
)

urlpatterns = [
    path("dashboards", DashboardCatalogView.as_view()),
    path("dashboards/<str:idor>/data", DashboardDataView.as_view()),
    path("dashboards/<str:idor>/export.csv", DashboardExportView.as_view()),
    path("dashboards/<str:idor>", DashboardDetailView.as_view()),
    path("admin/dashboards", AdminDashboardCreateView.as_view()),
    path("admin/dashboards/<int:pk>", AdminDashboardUpdateDeleteView.as_view()),
]
