from rest_framework.views import APIView

from apps.common.permissions import IsAdminOrAnalyst
from apps.common.responses import fail, ok
from apps.dashboards.models import Dashboard
from .models import LearningMaterial
from .serializers import LearningMaterialSerializer


class DashboardLearningView(APIView):
    """GET /api/dashboards/{dashboardId}/learning."""

    def get(self, request, dashboard_id):
        dashboard = Dashboard.objects.filter(pk=dashboard_id).first()
        if not dashboard:
            return fail("Dashboard not found.", status=404)
        material = dashboard.learning_materials.order_by("id").first()
        if not material:
            return ok(None)
        return ok(LearningMaterialSerializer(material).data)


class AdminLearningUpsertView(APIView):
    """POST /api/admin/dashboards/{dashboardId}/learning — create or update."""

    permission_classes = [IsAdminOrAnalyst]

    def post(self, request, dashboard_id):
        dashboard = Dashboard.objects.filter(pk=dashboard_id).first()
        if not dashboard:
            return fail("Dashboard not found.", status=404)
        material = dashboard.learning_materials.order_by("id").first()
        serializer = LearningMaterialSerializer(
            material, data=request.data, partial=bool(material))
        serializer.is_valid(raise_exception=True)
        material = serializer.save(dashboard=dashboard, created_by=request.user)
        return ok(LearningMaterialSerializer(material).data,
                  message="Learning material saved successfully")


class AdminLearningUpdateView(APIView):
    """PUT /api/admin/learning/{learningId}."""

    permission_classes = [IsAdminOrAnalyst]

    def put(self, request, learning_id):
        material = LearningMaterial.objects.filter(pk=learning_id).first()
        if not material:
            return fail("Learning material not found.", status=404)
        serializer = LearningMaterialSerializer(
            material, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        material = serializer.save()
        return ok(LearningMaterialSerializer(material).data,
                  message="Learning material updated successfully")
