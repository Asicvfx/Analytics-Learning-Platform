from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Role

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Read serializer for the current user / admin user list."""

    fullName = serializers.CharField(source="full_name")
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "fullName", "email", "roles", "status",
                  "department", "position"]

    def get_roles(self, obj):
        return obj.role_names


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserWriteSerializer(serializers.ModelSerializer):
    """Create/update users from the admin panel."""

    fullName = serializers.CharField(source="full_name")
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    roles = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = User
        fields = ["id", "fullName", "email", "password", "roles",
                  "status", "department", "position"]

    def _apply_roles(self, user, role_names):
        if role_names is None:
            return
        roles = list(Role.objects.filter(name__in=role_names))
        user.roles.set(roles)

    def create(self, validated_data):
        role_names = validated_data.pop("roles", [])
        password = validated_data.pop("password", None)
        if not password:
            raise serializers.ValidationError(
                {"password": "Password is required when creating a user."})
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        self._apply_roles(user, role_names or [])
        return user

    def update(self, instance, validated_data):
        role_names = validated_data.pop("roles", None)
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        self._apply_roles(instance, role_names)
        return instance
