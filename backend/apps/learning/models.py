from django.conf import settings
from django.db import models

from apps.common.models import TimeStampedModel
from apps.dashboards.models import Dashboard


class LearningMaterial(TimeStampedModel):
    """Instructions, video/presentation links and FAQ for a dashboard."""

    dashboard = models.ForeignKey(
        Dashboard, on_delete=models.CASCADE, related_name="learning_materials")
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, default="")
    video_url = models.TextField(blank=True, default="")
    presentation_url = models.TextField(blank=True, default="")
    faq_json = models.JSONField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="learning_materials")

    class Meta:
        db_table = "learning_materials"

    def __str__(self):
        return self.title
