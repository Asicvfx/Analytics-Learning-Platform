from rest_framework import serializers

from .models import AuditLog


class AuditUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    fullName = serializers.CharField(source="full_name")
    email = serializers.EmailField()


class AuditLogSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    targetType = serializers.CharField(source="target_type")
    targetId = serializers.IntegerField(source="target_id")
    metadata = serializers.JSONField(source="metadata_json")
    ipAddress = serializers.CharField(source="ip_address")
    createdAt = serializers.DateTimeField(source="created_at")

    class Meta:
        model = AuditLog
        fields = ["id", "user", "action", "targetType", "targetId",
                  "metadata", "ipAddress", "createdAt"]

    def get_user(self, obj):
        if not obj.user:
            return None
        return AuditUserSerializer(obj.user).data
