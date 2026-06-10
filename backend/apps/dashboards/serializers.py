from rest_framework import serializers

from apps.categories.models import Category
from .models import Dashboard


class CategoryMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class DashboardCardSerializer(serializers.ModelSerializer):
    """Catalog card view."""

    category = CategoryMiniSerializer()
    tags = serializers.SerializerMethodField()
    accessLevel = serializers.CharField(source="access_level")
    sheetCount = serializers.SerializerMethodField()
    lastUpdatedAt = serializers.DateTimeField(source="last_updated_at")

    class Meta:
        model = Dashboard
        fields = ["id", "title", "slug", "description", "category", "tags",
                  "accessLevel", "status", "sheetCount", "lastUpdatedAt"]

    def get_tags(self, obj):
        return obj.tag_list

    def get_sheetCount(self, obj):
        count = getattr(obj, "sheet_count", None)
        if count is not None:
            return count
        return obj.sheets.count()


class DashboardDetailSerializer(serializers.ModelSerializer):
    category = CategoryMiniSerializer()
    tags = serializers.SerializerMethodField()
    accessLevel = serializers.CharField(source="access_level")
    businessPurpose = serializers.CharField(source="business_purpose")
    ownerName = serializers.CharField(source="owner_name")
    lastUpdatedAt = serializers.DateTimeField(source="last_updated_at")
    sheets = serializers.SerializerMethodField()
    learningMaterial = serializers.SerializerMethodField()

    class Meta:
        model = Dashboard
        fields = ["id", "title", "slug", "description", "businessPurpose",
                  "ownerName", "accessLevel", "status", "tags", "category",
                  "sheets", "learningMaterial", "lastUpdatedAt"]

    def get_tags(self, obj):
        return obj.tag_list

    def get_sheets(self, obj):
        from apps.sheets.serializers import SheetSerializer
        ordered = obj.sheets.order_by("display_order", "id")
        return SheetSerializer(ordered, many=True).data

    def get_learningMaterial(self, obj):
        from apps.learning.serializers import LearningMaterialSerializer
        material = obj.learning_materials.order_by("id").first()
        if not material:
            return None
        return LearningMaterialSerializer(material).data


class DashboardWriteSerializer(serializers.ModelSerializer):
    categoryId = serializers.PrimaryKeyRelatedField(
        source="category", queryset=Category.objects.all())
    businessPurpose = serializers.CharField(
        source="business_purpose", required=False, allow_blank=True)
    ownerName = serializers.CharField(
        source="owner_name", required=False, allow_blank=True)
    accessLevel = serializers.CharField(source="access_level", required=False)
    tags = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = Dashboard
        fields = ["id", "title", "slug", "description", "businessPurpose",
                  "ownerName", "categoryId", "accessLevel", "status", "tags"]

    def _tags_to_text(self, validated):
        if "tags" in validated:
            validated["tags"] = ", ".join(validated.pop("tags"))
        return validated

    def create(self, validated_data):
        validated_data = self._tags_to_text(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data = self._tags_to_text(validated_data)
        return super().update(instance, validated_data)
