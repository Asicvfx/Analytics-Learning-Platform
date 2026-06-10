from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def health(_request):
    return JsonResponse({"success": True, "data": {"status": "ok"}, "message": None})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health", health),
    path("api/auth/", include("apps.accounts.urls_auth")),
    path("api/", include("apps.categories.urls")),
    path("api/", include("apps.dashboards.urls")),
    path("api/", include("apps.sheets.urls")),
    path("api/", include("apps.widgets.urls")),
    path("api/", include("apps.learning.urls")),
    path("api/", include("apps.accounts.urls_admin")),
    path("api/", include("apps.audit.urls")),
]
