from rest_framework.views import APIView

from apps.common.permissions import IsAdminOrAnalyst
from apps.common.responses import fail, ok
from apps.dashboards.models import Dashboard
from .models import DashboardSheet
from .serializers import SheetSerializer


class DashboardSheetListView(APIView):
    """GET /api/dashboards/{dashboardId}/sheets."""

    def get(self, request, dashboard_id):
        dashboard = Dashboard.objects.filter(pk=dashboard_id).first()
        if not dashboard:
            return fail("Dashboard not found.", status=404)
        sheets = dashboard.sheets.all()
        return ok(SheetSerializer(sheets, many=True).data)


class AdminSheetCreateView(APIView):
    permission_classes = [IsAdminOrAnalyst]

    def post(self, request, dashboard_id):
        dashboard = Dashboard.objects.filter(pk=dashboard_id).first()
        if not dashboard:
            return fail("Dashboard not found.", status=404)
        serializer = SheetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sheet = serializer.save(dashboard=dashboard)
        return ok(SheetSerializer(sheet).data,
                  message="Sheet created successfully", status=201)


class AdminSheetUpdateDeleteView(APIView):
    permission_classes = [IsAdminOrAnalyst]

    def put(self, request, sheet_id):
        sheet = DashboardSheet.objects.filter(pk=sheet_id).first()
        if not sheet:
            return fail("Sheet not found.", status=404)
        serializer = SheetSerializer(sheet, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        sheet = serializer.save()
        return ok(SheetSerializer(sheet).data, message="Sheet updated successfully")

    def delete(self, request, sheet_id):
        sheet = DashboardSheet.objects.filter(pk=sheet_id).first()
        if not sheet:
            return fail("Sheet not found.", status=404)
        sheet.delete()
        return ok(message="Sheet deleted successfully")
