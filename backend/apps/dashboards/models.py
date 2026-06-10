from django.conf import settings
from django.db import models

from apps.categories.models import Category
from apps.common.models import TimeStampedModel


class Dashboard(TimeStampedModel):
    """Dashboard metadata for the catalog and detail pages."""

    # status
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"
    STATUS_CHOICES = [(DRAFT, "Draft"), (PUBLISHED, "Published"),
                      (ARCHIVED, "Archived")]

    # access_level
    ADMIN_ONLY = "ADMIN_ONLY"
    ANALYST_ONLY = "ANALYST_ONLY"
    MANAGER = "MANAGER"
    EMPLOYEE = "EMPLOYEE"
    PUBLIC_INTERNAL = "PUBLIC_INTERNAL"
    ACCESS_CHOICES = [
        (ADMIN_ONLY, "Admin only"), (ANALYST_ONLY, "Analyst only"),
        (MANAGER, "Manager"), (EMPLOYEE, "Employee"),
        (PUBLIC_INTERNAL, "Public internal"),
    ]

    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="dashboards")
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, default="")
    business_purpose = models.TextField(blank=True, default="")
    owner_name = models.CharField(max_length=255, blank=True, default="")
    access_level = models.CharField(max_length=50, choices=ACCESS_CHOICES,
                                    default=EMPLOYEE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=DRAFT)
    tags = models.TextField(blank=True, default="")  # comma-separated
    last_updated_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="created_dashboards")

    class Meta:
        db_table = "dashboards"
        ordering = ["-last_updated_at", "title"]

    def __str__(self):
        return self.title

    @property
    def tag_list(self):
        return [t.strip() for t in self.tags.split(",") if t.strip()]


class DashboardPermission(models.Model):
    """Per-role view/export/edit flags for a dashboard."""

    dashboard = models.ForeignKey(
        Dashboard, on_delete=models.CASCADE, related_name="permissions")
    role_name = models.CharField(max_length=50)
    can_view = models.BooleanField(default=True)
    can_export = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "dashboard_permissions"
        unique_together = ("dashboard", "role_name")


# --- Demo dataset tables (fake data only) ---

class DemoRevenueRecord(models.Model):
    record_date = models.DateField()
    region = models.CharField(max_length=255)
    revenue = models.DecimalField(max_digits=15, decimal_places=2)
    new_installation_requests = models.IntegerField()
    churn_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "demo_revenue_records"


class DemoOrderRecord(models.Model):
    order_number = models.CharField(max_length=100)
    order_date = models.DateField()
    region = models.CharField(max_length=255)
    status = models.CharField(max_length=100)
    customer_type = models.CharField(max_length=100, blank=True, default="")
    amount = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "demo_order_records"


class DemoOrganizationRecord(models.Model):
    bin = models.CharField(max_length=20)
    organization_name = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    organization_type = models.CharField(max_length=100, blank=True, default="")
    contact_phone = models.CharField(max_length=100, blank=True, default="")
    contact_email = models.CharField(max_length=255, blank=True, default="")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "demo_organization_records"


class DemoProviderSpeedRecord(models.Model):
    test_date = models.DateField()
    region = models.CharField(max_length=255)
    provider_name = models.CharField(max_length=255)
    download_speed = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    upload_speed = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    latency_ms = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    quality_score = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "demo_provider_speed_records"


class DemoProcurementRecord(models.Model):
    lot_number = models.CharField(max_length=100)
    lot_title = models.CharField(max_length=255)
    region = models.CharField(max_length=255, blank=True, default="")
    planned_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    winning_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    competitor_count = models.IntegerField(null=True)
    status = models.CharField(max_length=100, blank=True, default="")
    result = models.CharField(max_length=100, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "demo_procurement_records"


class DemoSalesRecord(models.Model):
    request_date = models.DateField()
    region = models.CharField(max_length=255, blank=True, default="")
    product_name = models.CharField(max_length=255, blank=True, default="")
    tariff_name = models.CharField(max_length=255, blank=True, default="")
    offer_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    status = models.CharField(max_length=100, blank=True, default="")
    conversion_probability = models.DecimalField(
        max_digits=5, decimal_places=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "demo_sales_records"
