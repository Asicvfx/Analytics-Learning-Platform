from rest_framework import serializers

from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    displayOrder = serializers.IntegerField(source="display_order", required=False)
    dashboardCount = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "icon",
                  "displayOrder", "dashboardCount"]

    def get_dashboardCount(self, obj):
        # Annotated in the queryset where available; fall back to a count().
        count = getattr(obj, "dashboard_count", None)
        if count is not None:
            return count
        return obj.dashboards.count()


class CategoryWriteSerializer(serializers.ModelSerializer):
    displayOrder = serializers.IntegerField(source="display_order", required=False)
    isActive = serializers.BooleanField(source="is_active", required=False)

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "icon",
                  "displayOrder", "isActive"]
