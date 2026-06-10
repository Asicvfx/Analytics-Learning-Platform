from django.db import models

from apps.common.models import TimeStampedModel
from apps.dashboards.models import Dashboard


class DashboardSheet(TimeStampedModel):
    """A page/tab inside a dashboard (Overview, Regions, Details, ...)."""

    dashboard = models.ForeignKey(
        Dashboard, on_delete=models.CASCADE, related_name="sheets")
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True, default="")
    display_order = models.IntegerField(default=0)

    class Meta:
        db_table = "dashboard_sheets"
        ordering = ["display_order", "id"]
        unique_together = ("dashboard", "slug")

    def __str__(self):
        return f"{self.dashboard.slug}/{self.slug}"
