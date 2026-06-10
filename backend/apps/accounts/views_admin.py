from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, UpdateAPIView

from apps.audit.models import AuditLog
from apps.audit.services import log_action
from apps.common.pagination import StandardResultsSetPagination
from apps.common.permissions import IsAdmin
from .serializers import UserSerializer, UserWriteSerializer

User = get_user_model()


class AdminUserListCreateView(ListCreateAPIView):
    """GET/POST /api/admin/users (admin only)."""

    permission_classes = [IsAdmin]
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        return UserWriteSerializer if self.request.method == "POST" else UserSerializer

    def get_queryset(self):
        qs = User.objects.prefetch_related("roles").all().order_by("id")
        params = self.request.query_params
        if params.get("search"):
            qs = qs.filter(full_name__icontains=params["search"])
        if params.get("role"):
            qs = qs.filter(roles__name=params["role"])
        if params.get("status"):
            qs = qs.filter(status=params["status"])
        return qs.distinct()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        log_action(request.user, AuditLog.USER_CREATED, target_type="USER",
                   target_id=user.id, request=request)
        from rest_framework.response import Response
        return Response(
            {"success": True, "data": UserSerializer(user).data,
             "message": "User created successfully"},
            status=status.HTTP_201_CREATED,
        )


class AdminUserUpdateView(UpdateAPIView):
    """PUT /api/admin/users/{id} (admin only)."""

    permission_classes = [IsAdmin]
    serializer_class = UserWriteSerializer
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        action = (AuditLog.USER_ROLE_CHANGED if "roles" in request.data
                  else AuditLog.USER_UPDATED)
        log_action(request.user, action, target_type="USER",
                   target_id=user.id, request=request)
        from rest_framework.response import Response
        return Response({"success": True, "data": UserSerializer(user).data,
                         "message": "User updated successfully"})
