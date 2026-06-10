"""Dashboard view/export/edit permission logic (per the data-model spec)."""
from apps.common.permissions import ADMIN, ANALYST, EMPLOYEE, MANAGER
from .models import Dashboard

# Which roles an access_level grants view rights to (besides explicit perms).
_ACCESS_ROLE_MAP = {
    Dashboard.ADMIN_ONLY: {ADMIN},
    Dashboard.ANALYST_ONLY: {ADMIN, ANALYST},
    Dashboard.MANAGER: {ADMIN, ANALYST, MANAGER},
    Dashboard.EMPLOYEE: {ADMIN, ANALYST, MANAGER, EMPLOYEE},
    Dashboard.PUBLIC_INTERNAL: {ADMIN, ANALYST, MANAGER, EMPLOYEE},
}


def _roles(user):
    return set(user.role_names) if (user and user.is_authenticated) else set()


def _perm_flags(dashboard, roles, attr):
    return any(
        getattr(p, attr)
        for p in dashboard.permissions.all()
        if p.role_name in roles
    )


def can_view(user, dashboard):
    roles = _roles(user)
    if ADMIN in roles:
        return True
    if roles & _ACCESS_ROLE_MAP.get(dashboard.access_level, set()):
        return True
    return _perm_flags(dashboard, roles, "can_view")


def can_export(user, dashboard):
    roles = _roles(user)
    if ADMIN in roles:
        return True
    return _perm_flags(dashboard, roles, "can_export")


def can_edit(user, dashboard):
    roles = _roles(user)
    if ADMIN in roles:
        return True
    # First version: any analyst may edit dashboards.
    if ANALYST in roles:
        return True
    return _perm_flags(dashboard, roles, "can_edit")


def visible_queryset(user, qs):
    """Filter a Dashboard queryset down to what the user may view."""
    roles = _roles(user)
    if ADMIN in roles:
        return qs
    allowed_levels = [
        level for level, allowed in _ACCESS_ROLE_MAP.items() if roles & allowed
    ]
    from django.db.models import Q
    cond = Q(access_level__in=allowed_levels)
    cond |= Q(permissions__role_name__in=roles, permissions__can_view=True)
    return qs.filter(cond).distinct()
