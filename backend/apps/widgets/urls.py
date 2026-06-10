from django.urls import path

from .views import (
    AdminWidgetCreateView,
    AdminWidgetUpdateDeleteView,
    SheetWidgetListView,
)

urlpatterns = [
    path("sheets/<int:sheet_id>/widgets", SheetWidgetListView.as_view()),
    path("admin/sheets/<int:sheet_id>/widgets", AdminWidgetCreateView.as_view()),
    path("admin/widgets/<int:widget_id>", AdminWidgetUpdateDeleteView.as_view()),
]
