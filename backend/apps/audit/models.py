from django.conf import settings
from django.db import models


class AuditLog(models.Model):
    """Records important user actions across the platform."""

    USER_LOGIN = "USER_LOGIN"
    USER_LOGOUT = "USER_LOGOUT"
    DASHBOARD_OPENED = "DASHBOARD_OPENED"
    DATA_EXPORTED = "DATA_EXPORTED"
    DASHBOARD_CREATED = "DASHBOARD_CREATED"
    DASHBOARD_UPDATED = "DASHBOARD_UPDATED"
    DASHBOARD_ARCHIVED = "DASHBOARD_ARCHIVED"
    CATEGORY_CREATED = "CATEGORY_CREATED"
    CATEGORY_UPDATED = "CATEGORY_UPDATED"
    USER_CREATED = "USER_CREATED"
    USER_UPDATED = "USER_UPDATED"
    USER_ROLE_CHANGED = "USER_ROLE_CHANGED"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="audit_logs",
    )
    action = models.CharField(max_length=100)
    target_type = models.CharField(max_length=100, blank=True, default="")
    target_id = models.BigIntegerField(null=True, blank=True)
    metadata_json = models.JSONField(null=True, blank=True)
    ip_address = models.CharField(max_length=100, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "audit_logs"
        ordering = ["-created_at"]
