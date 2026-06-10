from rest_framework import serializers

from .models import DashboardSheet


class SheetSerializer(serializers.ModelSerializer):
    dashboardId = serializers.IntegerField(source="dashboard_id", read_only=True)
    displayOrder = serializers.IntegerField(source="display_order", required=False)

    class Meta:
        model = DashboardSheet
        fields = ["id", "dashboardId", "title", "slug", "description",
                  "displayOrder"]
