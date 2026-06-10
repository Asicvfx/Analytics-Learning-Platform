from django.db import models

from apps.common.models import TimeStampedModel
from apps.sheets.models import DashboardSheet


class DashboardWidget(TimeStampedModel):
    """A visual block inside a sheet (KPI card, chart, table, text)."""

    KPI_CARD = "KPI_CARD"
    BAR_CHART = "BAR_CHART"
    LINE_CHART = "LINE_CHART"
    PIE_CHART = "PIE_CHART"
    DATA_TABLE = "DATA_TABLE"
    TEXT_BLOCK = "TEXT_BLOCK"
    TYPE_CHOICES = [
        (KPI_CARD, "KPI card"), (BAR_CHART, "Bar chart"),
        (LINE_CHART, "Line chart"), (PIE_CHART, "Pie chart"),
        (DATA_TABLE, "Data table"), (TEXT_BLOCK, "Text block"),
    ]

    sheet = models.ForeignKey(
        DashboardSheet, on_delete=models.CASCADE, related_name="widgets")
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    config_json = models.JSONField(null=True, blank=True)
    position_json = models.JSONField(null=True, blank=True)
    display_order = models.IntegerField(default=0)

    class Meta:
        db_table = "dashboard_widgets"
        ordering = ["display_order", "id"]
