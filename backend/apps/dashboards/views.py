from django.db.models import Count
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from apps.audit.models import AuditLog
from apps.audit.services import log_action
from apps.common.pagination import StandardResultsSetPagination
from apps.common.permissions import IsAdminOrAnalyst
from apps.common.responses import fail, ok
from apps.export.csv_export import build_csv_response
from . import access
from .data_service import get_dashboard_data, get_export_table
from .filters import extract_filters
from .models import Dashboard
from .serializers import (
    DashboardCardSerializer,
    DashboardDetailSerializer,
    DashboardWriteSerializer,
)


def _base_qs():
    return (Dashboard.objects
            .select_related("category")
            .prefetch_related("sheets", "permissions")
            .annotate(sheet_count=Count("sheets", distinct=True)))


def _get_by_id_or_slug(idor, qs=None):
    qs = qs if qs is not None else _base_qs()
    if str(idor).isdigit():
        return qs.filter(pk=idor).first()
    return qs.filter(slug=idor).first()


class DashboardCatalogView(ListAPIView):
    """GET /api/dashboards — only dashboards the user may view."""

    serializer_class = DashboardCardSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        qs = _base_qs().exclude(status=Dashboard.ARCHIVED)
        qs = access.visible_queryset(self.request.user, qs)
        params = self.request.query_params
        if params.get("search"):
            term = params["search"]
            from django.db.models import Q
            qs = qs.filter(Q(title__icontains=term) |
                           Q(description__icontains=term) |
                           Q(tags__icontains=term))
        if params.get("category"):
            qs = qs.filter(category__slug=params["category"])
        if params.get("tag"):
            qs = qs.filter(tags__icontains=params["tag"])
        if params.get("status"):
            qs = qs.filter(status=params["status"])
        return qs


class DashboardDetailView(APIView):
    """GET /api/dashboards/{idOrSlug}."""

    def get(self, request, idor):
        dashboard = _get_by_id_or_slug(idor)
        if not dashboard or dashboard.status == Dashboard.ARCHIVED:
            return fail("Dashboard not found.", status=404)
        if not access.can_view(request.user, dashboard):
            return fail("You do not have access to this dashboard.", status=403)
        log_action(request.user, AuditLog.DASHBOARD_OPENED, target_type="DASHBOARD",
                   target_id=dashboard.id,
                   metadata={"dashboardTitle": dashboard.title}, request=request)
        return ok(DashboardDetailSerializer(dashboard).data)


class DashboardDataView(APIView):
    """GET /api/dashboards/{idOrSlug}/data."""

    def get(self, request, idor):
        dashboard = _get_by_id_or_slug(idor)
        if not dashboard or dashboard.status == Dashboard.ARCHIVED:
            return fail("Dashboard not found.", status=404)
        if not access.can_view(request.user, dashboard):
            return fail("You do not have access to this dashboard.", status=403)
        filters = extract_filters(request.query_params)
        return ok(get_dashboard_data(dashboard, filters))


class DashboardExportView(APIView):
    """GET /api/dashboards/{idOrSlug}/export.csv."""

    def get(self, request, idor):
        dashboard = _get_by_id_or_slug(idor)
        if not dashboard or dashboard.status == Dashboard.ARCHIVED:
            return fail("Dashboard not found.", status=404)
        if not access.can_view(request.user, dashboard):
            return fail("You do not have access to this dashboard.", status=403)
        if not access.can_export(request.user, dashboard):
            return fail("You do not have permission to export this dashboard.",
                        status=403)
        filters = extract_filters(request.query_params)
        columns, rows = get_export_table(dashboard, filters)
        log_action(request.user, AuditLog.DATA_EXPORTED, target_type="DASHBOARD",
                   target_id=dashboard.id,
                   metadata={"dashboardTitle": dashboard.title, "filters": filters},
                   request=request)
        return build_csv_response(f"{dashboard.slug}.csv", columns, rows)


# --- Admin dashboard management ---

class AdminDashboardCreateView(APIView):
    permission_classes = [IsAdminOrAnalyst]

    def post(self, request):
        serializer = DashboardWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        from django.utils import timezone
        dashboard = serializer.save(created_by=request.user,
                                    last_updated_at=timezone.now())
        log_action(request.user, AuditLog.DASHBOARD_CREATED, target_type="DASHBOARD",
                   target_id=dashboard.id, request=request)
        return ok(DashboardWriteSerializer(dashboard).data,
                  message="Dashboard created successfully", status=201)


class AdminDashboardUpdateDeleteView(APIView):
    permission_classes = [IsAdminOrAnalyst]

    def put(self, request, pk):
        dashboard = Dashboard.objects.filter(pk=pk).first()
        if not dashboard:
            return fail("Dashboard not found.", status=404)
        if not access.can_edit(request.user, dashboard):
            return fail("You do not have permission to edit this dashboard.",
                        status=403)
        serializer = DashboardWriteSerializer(dashboard, data=request.data,
                                              partial=True)
        serializer.is_valid(raise_exception=True)
        from django.utils import timezone
        dashboard = serializer.save(last_updated_at=timezone.now())
        log_action(request.user, AuditLog.DASHBOARD_UPDATED, target_type="DASHBOARD",
                   target_id=dashboard.id, request=request)
        return ok(DashboardWriteSerializer(dashboard).data,
                  message="Dashboard updated successfully")

    def delete(self, request, pk):
        dashboard = Dashboard.objects.filter(pk=pk).first()
        if not dashboard:
            return fail("Dashboard not found.", status=404)
        dashboard.status = Dashboard.ARCHIVED
        dashboard.save(update_fields=["status", "updated_at"])
        log_action(request.user, AuditLog.DASHBOARD_ARCHIVED, target_type="DASHBOARD",
                   target_id=dashboard.id, request=request)
        return ok(message="Dashboard archived successfully")
