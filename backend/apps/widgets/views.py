from rest_framework.views import APIView

from apps.common.permissions import IsAdminOrAnalyst
from apps.common.responses import fail, ok
from apps.sheets.models import DashboardSheet
from .models import DashboardWidget
from .serializers import WidgetSerializer


class SheetWidgetListView(APIView):
    """GET /api/sheets/{sheetId}/widgets."""

    def get(self, request, sheet_id):
        sheet = DashboardSheet.objects.filter(pk=sheet_id).first()
        if not sheet:
            return fail("Sheet not found.", status=404)
        return ok(WidgetSerializer(sheet.widgets.all(), many=True).data)


class AdminWidgetCreateView(APIView):
    permission_classes = [IsAdminOrAnalyst]

    def post(self, request, sheet_id):
        sheet = DashboardSheet.objects.filter(pk=sheet_id).first()
        if not sheet:
            return fail("Sheet not found.", status=404)
        serializer = WidgetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        widget = serializer.save(sheet=sheet)
        return ok(WidgetSerializer(widget).data,
                  message="Widget created successfully", status=201)


class AdminWidgetUpdateDeleteView(APIView):
    permission_classes = [IsAdminOrAnalyst]

    def put(self, request, widget_id):
        widget = DashboardWidget.objects.filter(pk=widget_id).first()
        if not widget:
            return fail("Widget not found.", status=404)
        serializer = WidgetSerializer(widget, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        widget = serializer.save()
        return ok(WidgetSerializer(widget).data,
                  message="Widget updated successfully")

    def delete(self, request, widget_id):
        widget = DashboardWidget.objects.filter(pk=widget_id).first()
        if not widget:
            return fail("Widget not found.", status=404)
        widget.delete()
        return ok(message="Widget deleted successfully")
