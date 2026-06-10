"""Seed the database with demo (fake) data only.

Idempotent-ish: pass --if-empty to skip when categories already exist.
All data here is fictional and safe to deploy publicly.
"""
import random
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.accounts.models import Role
from apps.categories.models import Category
from apps.dashboards.models import (
    Dashboard,
    DashboardPermission,
    DemoOrderRecord,
    DemoOrganizationRecord,
    DemoProcurementRecord,
    DemoProviderSpeedRecord,
    DemoRevenueRecord,
    DemoSalesRecord,
)
from apps.learning.models import LearningMaterial
from apps.sheets.models import DashboardSheet
from apps.widgets.models import DashboardWidget

User = get_user_model()

REGIONS = ["Almaty", "Astana", "Shymkent", "Karaganda", "Aktobe"]
ORG_TYPES = ["LLP", "JSC", "IE", "State", "NGO"]
PROVIDERS = ["AlphaNet", "BetaLink", "GammaTel", "DeltaWave"]

CATEGORIES = [
    ("Revenue", "revenue", "Revenue and business performance dashboards",
     "chart-line", 1),
    ("Orders", "orders", "Customer order analytics", "shopping-cart", 2),
    ("BIN Analytics", "bin-analytics", "Legal entities and organizations",
     "building", 3),
    ("Contacts", "contacts", "Organization contact availability", "phone", 4),
    ("Education and Healthcare Objects", "education-healthcare",
     "Demo analytics about education and healthcare objects", "hospital", 5),
    ("Provider SpeedTest Map", "provider-speedtest",
     "Internet provider quality indicators", "wifi", 6),
    ("Government Procurement", "government-procurement",
     "Procurement lots and competitors", "gavel", 7),
    ("Sales Tools", "sales-tools", "Sales support and offer generation",
     "briefcase", 8),
    ("AI Tools", "ai-tools", "Demo AI analytics tools", "cpu", 9),
    ("Instructions", "instructions", "Platform usage guides", "book", 10),
]

# (title, slug, category_slug, access_level, [sheet titles], tags)
DASHBOARDS = [
    ("Revenue Overview", "revenue-overview", "revenue", Dashboard.EMPLOYEE,
     ["Overview", "Regions", "Details"], ["revenue", "regions", "churn"],
     "Shows revenue, new installation requests, and churn by region and period."),
    ("Orders Dashboard", "orders-dashboard", "orders", Dashboard.EMPLOYEE,
     ["Overview", "Statuses", "Details"], ["orders", "status", "regions"],
     "Detailed information about customer orders."),
    ("BIN Analytics", "bin-analytics", "bin-analytics", Dashboard.MANAGER,
     ["Overview", "Organizations", "Contacts"], ["organizations", "bin"],
     "Analytics about legal entities and organizations."),
    ("Contacts Dashboard", "contacts-dashboard", "contacts", Dashboard.EMPLOYEE,
     ["Overview", "Contacts"], ["contacts", "organizations"],
     "Contact availability across organizations."),
    ("Education and Healthcare Objects", "education-healthcare-objects",
     "education-healthcare", Dashboard.EMPLOYEE,
     ["Overview", "Map/List", "Details"], ["education", "healthcare"],
     "Demo analytics about education and healthcare objects."),
    ("Provider SpeedTest Map", "provider-speedtest-map", "provider-speedtest",
     Dashboard.EMPLOYEE, ["Overview", "Providers", "Regions"],
     ["providers", "speed", "quality"],
     "Demo analytics about internet providers and quality indicators."),
    ("Government Procurement Analytics", "government-procurement-analytics",
     "government-procurement", Dashboard.MANAGER,
     ["Overview", "Competitors", "Recommendations"], ["procurement", "lots"],
     "Demo information about government procurement lots and competitors."),
    ("SalesHelper Dashboard", "saleshelper-dashboard", "sales-tools",
     Dashboard.MANAGER, ["Overview", "Requests", "Details"],
     ["sales", "offers", "conversion"],
     "Demo analytics for sales support and commercial offer generation."),
]

PERMISSIONS = [
    # role_name, can_view, can_export, can_edit
    # Visibility is driven by access_level; these rows grant export rights to
    # the roles that can already view the dashboard (can_view kept False so the
    # access_level RBAC stays meaningful in the demo).
    (Role.ADMIN, False, True, True),
    (Role.ANALYST, False, True, True),
    (Role.MANAGER, False, True, False),
    (Role.EMPLOYEE, False, True, False),
]


class Command(BaseCommand):
    help = "Seed demo/fake data for the Analytics & Learning Platform."

    def add_arguments(self, parser):
        parser.add_argument("--if-empty", action="store_true",
                            help="Skip seeding if categories already exist.")

    @transaction.atomic
    def handle(self, *args, **options):
        if options["if_empty"] and Category.objects.exists():
            self.stdout.write("Data already present — skipping seed.")
            return

        random.seed(42)
        self._seed_roles_and_users()
        categories = self._seed_categories()
        self._seed_dashboards(categories)
        self._seed_demo_records()
        self.stdout.write(self.style.SUCCESS("Demo data seeded successfully."))

    # --- roles & users ---
    def _seed_roles_and_users(self):
        for name in [Role.ADMIN, Role.ANALYST, Role.MANAGER, Role.EMPLOYEE]:
            Role.objects.get_or_create(name=name)

        demo_users = [
            ("Demo Admin", "admin@example.com", "admin123", Role.ADMIN,
             "Analytics", "Administrator"),
            ("Demo Analyst", "analyst@example.com", "analyst123", Role.ANALYST,
             "Analytics", "Analyst"),
            ("Demo Manager", "manager@example.com", "manager123", Role.MANAGER,
             "Sales", "Manager"),
            ("Demo Employee", "employee@example.com", "employee123", Role.EMPLOYEE,
             "Operations", "Specialist"),
        ]
        for full_name, email, password, role, dept, position in demo_users:
            user, created = User.objects.get_or_create(
                email=email,
                defaults={"full_name": full_name, "department": dept,
                          "position": position,
                          "is_staff": role == Role.ADMIN,
                          "is_superuser": role == Role.ADMIN},
            )
            if created:
                user.set_password(password)
                user.save()
            role_obj = Role.objects.get(name=role)
            user.roles.set([role_obj])

    # --- categories ---
    def _seed_categories(self):
        result = {}
        for name, slug, desc, icon, order in CATEGORIES:
            cat, _ = Category.objects.get_or_create(
                slug=slug,
                defaults={"name": name, "description": desc, "icon": icon,
                          "display_order": order},
            )
            result[slug] = cat
        return result

    # --- dashboards, sheets, widgets, permissions, learning ---
    def _seed_dashboards(self, categories):
        admin = User.objects.filter(email="admin@example.com").first()
        for title, slug, cat_slug, access, sheets, tags, desc in DASHBOARDS:
            dash, created = Dashboard.objects.get_or_create(
                slug=slug,
                defaults={
                    "category": categories[cat_slug],
                    "title": title,
                    "description": desc,
                    "business_purpose": f"Helps teams monitor {title.lower()}.",
                    "owner_name": "Analytics Team",
                    "access_level": access,
                    "status": Dashboard.PUBLISHED,
                    "tags": ", ".join(tags),
                    "last_updated_at": timezone.now(),
                    "created_by": admin,
                },
            )
            if not created:
                continue
            for i, sheet_title in enumerate(sheets, start=1):
                sheet = DashboardSheet.objects.create(
                    dashboard=dash, title=sheet_title,
                    slug=sheet_title.lower().replace(" ", "-").replace("/", "-"),
                    description=f"{sheet_title} sheet", display_order=i,
                )
                if i == 1:
                    self._seed_overview_widgets(sheet)
            for role_name, cv, ce, ced in PERMISSIONS:
                DashboardPermission.objects.create(
                    dashboard=dash, role_name=role_name,
                    can_view=cv, can_export=ce, can_edit=ced,
                )
            LearningMaterial.objects.create(
                dashboard=dash, title=f"How to use {title}",
                content=("Use the filters to select region and period. "
                         "Switch between sheets to view details. "
                         "Click Export CSV on the table to download filtered data."),
                video_url="https://example.com/demo-video",
                presentation_url="https://example.com/demo-presentation",
                faq_json=[
                    {"question": "How do I export data?",
                     "answer": "Open the table and click Export CSV."},
                    {"question": "How do I filter by region?",
                     "answer": "Use the Region dropdown in the filter bar."},
                ],
                created_by=admin,
            )

    def _seed_overview_widgets(self, sheet):
        DashboardWidget.objects.create(
            sheet=sheet, type=DashboardWidget.KPI_CARD, title="Key Metrics",
            description="Primary KPIs for the selected period",
            config_json={"source": "kpis"},
            position_json={"x": 0, "y": 0, "w": 12, "h": 1}, display_order=1,
        )
        DashboardWidget.objects.create(
            sheet=sheet, type=DashboardWidget.BAR_CHART, title="Breakdown",
            description="Primary chart", config_json={"source": "charts", "index": 0},
            position_json={"x": 0, "y": 1, "w": 6, "h": 4}, display_order=2,
        )
        DashboardWidget.objects.create(
            sheet=sheet, type=DashboardWidget.DATA_TABLE, title="Details",
            description="Detailed records", config_json={"source": "table"},
            position_json={"x": 0, "y": 5, "w": 12, "h": 5}, display_order=3,
        )

    # --- demo dataset records ---
    def _seed_demo_records(self):
        if DemoRevenueRecord.objects.exists():
            return
        today = date(2026, 6, 1)

        # Revenue: monthly per region over 6 months.
        revenue = []
        for month in range(6):
            d = date(2026, month + 1, 1)
            for region in REGIONS:
                revenue.append(DemoRevenueRecord(
                    record_date=d, region=region,
                    revenue=Decimal(random.randint(8_000_000, 50_000_000)),
                    new_installation_requests=random.randint(20, 120),
                    churn_count=random.randint(1, 15),
                ))
        DemoRevenueRecord.objects.bulk_create(revenue)

        # Orders.
        statuses = ["COMPLETED", "PENDING", "CANCELLED"]
        orders = [
            DemoOrderRecord(
                order_number=f"ORD-{1000 + i}",
                order_date=today - timedelta(days=random.randint(0, 150)),
                region=random.choice(REGIONS),
                status=random.choice(statuses),
                customer_type=random.choice(["B2B", "B2C"]),
                amount=Decimal(random.randint(50_000, 2_000_000)),
            ) for i in range(120)
        ]
        DemoOrderRecord.objects.bulk_create(orders)

        # Organizations.
        orgs = [
            DemoOrganizationRecord(
                bin=f"{random.randint(100000000000, 999999999999)}",
                organization_name=f"Demo Org {i}",
                region=random.choice(REGIONS),
                organization_type=random.choice(ORG_TYPES),
                contact_phone=f"+7700{random.randint(1000000, 9999999)}",
                contact_email=f"org{i}@example.com",
                is_active=random.random() > 0.2,
            ) for i in range(60)
        ]
        DemoOrganizationRecord.objects.bulk_create(orgs)

        # Provider speed.
        speeds = []
        for month in range(6):
            d = date(2026, month + 1, 15)
            for provider in PROVIDERS:
                for region in REGIONS:
                    speeds.append(DemoProviderSpeedRecord(
                        test_date=d, region=region, provider_name=provider,
                        download_speed=Decimal(random.randint(40, 300)),
                        upload_speed=Decimal(random.randint(20, 150)),
                        latency_ms=Decimal(random.randint(5, 60)),
                        quality_score=Decimal(f"{random.uniform(3, 5):.2f}"),
                    ))
        DemoProviderSpeedRecord.objects.bulk_create(speeds)

        # Procurement.
        results = ["WON", "LOST"]
        procurement = [
            DemoProcurementRecord(
                lot_number=f"LOT-{2000 + i}",
                lot_title=f"Demo Procurement Lot {i}",
                region=random.choice(REGIONS),
                planned_amount=Decimal(random.randint(1_000_000, 30_000_000)),
                winning_amount=Decimal(random.randint(900_000, 29_000_000)),
                competitor_count=random.randint(1, 8),
                status=random.choice(["OPEN", "CLOSED"]),
                result=random.choice(results),
            ) for i in range(40)
        ]
        DemoProcurementRecord.objects.bulk_create(procurement)

        # Sales.
        sales = [
            DemoSalesRecord(
                request_date=today - timedelta(days=random.randint(0, 120)),
                region=random.choice(REGIONS),
                product_name=random.choice(["Internet", "TV", "Bundle", "Cloud"]),
                tariff_name=random.choice(["Basic", "Standard", "Premium"]),
                offer_amount=Decimal(random.randint(5_000, 80_000)),
                status=random.choice(["NEW", "SENT", "WON", "LOST"]),
                conversion_probability=Decimal(f"{random.uniform(10, 95):.2f}"),
            ) for i in range(50)
        ]
        DemoSalesRecord.objects.bulk_create(sales)
