from rest_framework.generics import ListAPIView

from apps.common.permissions import IsAdmin
from .models import AuditLog
from .serializers import AuditLogSerializer


class AuditLogListView(ListAPIView):
    """GET /api/admin/audit-logs (admin only)."""

    serializer_class = AuditLogSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        qs = AuditLog.objects.select_related("user").all()
        params = self.request.query_params
        if params.get("userId"):
            qs = qs.filter(user_id=params["userId"])
        if params.get("action"):
            qs = qs.filter(action=params["action"])
        if params.get("targetType"):
            qs = qs.filter(target_type=params["targetType"])
        if params.get("dateFrom"):
            qs = qs.filter(created_at__date__gte=params["dateFrom"])
        if params.get("dateTo"):
            qs = qs.filter(created_at__date__lte=params["dateTo"])
        return qs
