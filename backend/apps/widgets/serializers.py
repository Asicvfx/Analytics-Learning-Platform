from rest_framework import serializers

from .models import DashboardWidget


class WidgetSerializer(serializers.ModelSerializer):
    sheetId = serializers.IntegerField(source="sheet_id", read_only=True)
    config = serializers.JSONField(source="config_json", required=False)
    position = serializers.JSONField(source="position_json", required=False)
    displayOrder = serializers.IntegerField(source="display_order", required=False)

    class Meta:
        model = DashboardWidget
        fields = ["id", "sheetId", "type", "title", "description",
                  "config", "position", "displayOrder"]
