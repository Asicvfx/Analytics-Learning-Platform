"""Helper for writing audit log entries."""
from .models import AuditLog


def client_ip(request):
    if request is None:
        return ""
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")


def log_action(user, action, *, target_type="", target_id=None,
               metadata=None, request=None):
    return AuditLog.objects.create(
        user=user if (user and getattr(user, "is_authenticated", False)) else None,
        action=action,
        target_type=target_type or "",
        target_id=target_id,
        metadata_json=metadata,
        ip_address=client_ip(request),
    )
