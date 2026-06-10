from django.db.models import Count, Q
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from apps.audit.models import AuditLog
from apps.audit.services import log_action
from apps.common.permissions import IsAdmin
from apps.common.responses import fail, ok
from .models import Category
from .serializers import CategorySerializer, CategoryWriteSerializer


def _with_counts(qs):
    return qs.annotate(
        dashboard_count=Count(
            "dashboards",
            filter=Q(dashboards__status="PUBLISHED"),
        )
    )


def _get_by_id_or_slug(idor):
    qs = _with_counts(Category.objects.all())
    if str(idor).isdigit():
        return qs.filter(pk=idor).first()
    return qs.filter(slug=idor).first()


class CategoryListView(ListAPIView):
    """GET /api/categories."""

    serializer_class = CategorySerializer
    pagination_class = None

    def get_queryset(self):
        qs = _with_counts(Category.objects.all())
        if self.request.query_params.get("active") == "true":
            qs = qs.filter(is_active=True)
        return qs

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return ok(serializer.data)


class CategoryDetailView(APIView):
    """GET /api/categories/{idOrSlug}."""

    def get(self, request, idor):
        category = _get_by_id_or_slug(idor)
        if not category:
            return fail("Category not found.", status=404)
        return ok(CategorySerializer(category).data)


class AdminCategoryCreateView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        serializer = CategoryWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = serializer.save()
        log_action(request.user, AuditLog.CATEGORY_CREATED, target_type="CATEGORY",
                   target_id=category.id, request=request)
        return ok(CategoryWriteSerializer(category).data,
                  message="Category created successfully", status=201)


class AdminCategoryUpdateDeleteView(APIView):
    permission_classes = [IsAdmin]

    def put(self, request, pk):
        category = Category.objects.filter(pk=pk).first()
        if not category:
            return fail("Category not found.", status=404)
        serializer = CategoryWriteSerializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        category = serializer.save()
        log_action(request.user, AuditLog.CATEGORY_UPDATED, target_type="CATEGORY",
                   target_id=category.id, request=request)
        return ok(CategoryWriteSerializer(category).data,
                  message="Category updated successfully")

    def delete(self, request, pk):
        category = Category.objects.filter(pk=pk).first()
        if not category:
            return fail("Category not found.", status=404)
        # Archive instead of hard delete.
        category.is_active = False
        category.save(update_fields=["is_active", "updated_at"])
        return ok(message="Category archived successfully")
