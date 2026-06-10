"""Reusable role-based DRF permission classes."""
from rest_framework.permissions import BasePermission

ADMIN = "ADMIN"
ANALYST = "ANALYST"
MANAGER = "MANAGER"
EMPLOYEE = "EMPLOYEE"


def role_names(user):
    if not user or not user.is_authenticated:
        return set()
    return set(user.role_names)


class IsAdmin(BasePermission):
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        return ADMIN in role_names(request.user)


class IsAdminOrAnalyst(BasePermission):
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        return bool(role_names(request.user) & {ADMIN, ANALYST})
