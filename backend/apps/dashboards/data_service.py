"""Builds KPI/chart/table payloads from demo tables, keyed by dashboard slug.

Kept intentionally simple (one handler per dashboard) — no universal query
builder, per the first-version scope.
"""
from decimal import Decimal

from django.db.models import Avg, Count, Sum

from .models import (
    DemoOrderRecord,
    DemoOrganizationRecord,
    DemoProcurementRecord,
    DemoProviderSpeedRecord,
    DemoRevenueRecord,
    DemoSalesRecord,
)


def _num(value):
    if isinstance(value, Decimal):
        return float(value)
    return value or 0


def _apply_common(qs, filters, *, date_field=None, region_field="region",
                  status_field=None):
    if date_field:
        if filters.get("dateFrom"):
            qs = qs.filter(**{f"{date_field}__gte": filters["dateFrom"]})
        if filters.get("dateTo"):
            qs = qs.filter(**{f"{date_field}__lte": filters["dateTo"]})
    if filters.get("region") and region_field:
        qs = qs.filter(**{region_field: filters["region"]})
    if filters.get("status") and status_field:
        qs = qs.filter(**{status_field: filters["status"]})
    return qs


# --- Per-dashboard handlers: each returns (kpis, charts, columns, rows) ---

def _revenue(filters):
    qs = _apply_common(DemoRevenueRecord.objects.all(), filters,
                       date_field="record_date")
    totals = qs.aggregate(
        revenue=Sum("revenue"),
        installs=Sum("new_installation_requests"),
        churn=Sum("churn_count"),
    )
    by_region = (qs.values("region")
                 .annotate(value=Sum("revenue")).order_by("-value"))
    by_period = (qs.values("record_date")
                 .annotate(value=Sum("revenue")).order_by("record_date"))
    kpis = [
        {"key": "totalRevenue", "label": "Total Revenue",
         "value": _num(totals["revenue"]), "format": "currency"},
        {"key": "newInstallationRequests", "label": "New Installation Requests",
         "value": _num(totals["installs"]), "format": "number"},
        {"key": "churn", "label": "Churn", "value": _num(totals["churn"]),
         "format": "number"},
    ]
    charts = [
        {"type": "BAR_CHART", "title": "Revenue by Region",
         "data": [{"label": r["region"], "value": _num(r["value"])}
                  for r in by_region]},
        {"type": "LINE_CHART", "title": "Monthly Revenue Trend",
         "data": [{"label": str(r["record_date"]), "value": _num(r["value"])}
                  for r in by_period]},
    ]
    columns = [
        {"key": "recordDate", "label": "Date"},
        {"key": "region", "label": "Region"},
        {"key": "revenue", "label": "Revenue"},
        {"key": "newInstallationRequests", "label": "New Installations"},
        {"key": "churnCount", "label": "Churn"},
    ]
    rows = [{
        "recordDate": str(r.record_date), "region": r.region,
        "revenue": _num(r.revenue),
        "newInstallationRequests": r.new_installation_requests,
        "churnCount": r.churn_count,
    } for r in qs.order_by("record_date")]
    return kpis, charts, columns, rows


def _orders(filters):
    qs = _apply_common(DemoOrderRecord.objects.all(), filters,
                       date_field="order_date", status_field="status")
    total = qs.count()
    by_status = qs.values("status").annotate(value=Count("id")).order_by("-value")
    by_region = qs.values("region").annotate(value=Count("id")).order_by("-value")
    status_map = {r["status"]: r["value"] for r in by_status}
    kpis = [
        {"key": "totalOrders", "label": "Total Orders", "value": total,
         "format": "number"},
        {"key": "completed", "label": "Completed",
         "value": status_map.get("COMPLETED", 0), "format": "number"},
        {"key": "pending", "label": "Pending",
         "value": status_map.get("PENDING", 0), "format": "number"},
        {"key": "cancelled", "label": "Cancelled",
         "value": status_map.get("CANCELLED", 0), "format": "number"},
    ]
    charts = [
        {"type": "PIE_CHART", "title": "Orders by Status",
         "data": [{"label": r["status"], "value": r["value"]} for r in by_status]},
        {"type": "BAR_CHART", "title": "Orders by Region",
         "data": [{"label": r["region"], "value": r["value"]} for r in by_region]},
    ]
    columns = [
        {"key": "orderNumber", "label": "Order #"},
        {"key": "orderDate", "label": "Date"},
        {"key": "region", "label": "Region"},
        {"key": "status", "label": "Status"},
        {"key": "amount", "label": "Amount"},
    ]
    rows = [{
        "orderNumber": r.order_number, "orderDate": str(r.order_date),
        "region": r.region, "status": r.status, "amount": _num(r.amount),
    } for r in qs.order_by("order_date")]
    return kpis, charts, columns, rows


def _organizations(filters):
    qs = DemoOrganizationRecord.objects.all()
    if filters.get("region"):
        qs = qs.filter(region=filters["region"])
    if filters.get("organizationType"):
        qs = qs.filter(organization_type=filters["organizationType"])
    total = qs.count()
    active = qs.filter(is_active=True).count()
    by_region = qs.values("region").annotate(value=Count("id")).order_by("-value")
    by_type = (qs.values("organization_type")
               .annotate(value=Count("id")).order_by("-value"))
    kpis = [
        {"key": "totalOrganizations", "label": "Total Organizations",
         "value": total, "format": "number"},
        {"key": "activeOrganizations", "label": "Active Organizations",
         "value": active, "format": "number"},
    ]
    charts = [
        {"type": "BAR_CHART", "title": "Organizations by Region",
         "data": [{"label": r["region"], "value": r["value"]} for r in by_region]},
        {"type": "PIE_CHART", "title": "Organizations by Type",
         "data": [{"label": r["organization_type"] or "N/A", "value": r["value"]}
                  for r in by_type]},
    ]
    columns = [
        {"key": "bin", "label": "BIN"},
        {"key": "organizationName", "label": "Organization"},
        {"key": "region", "label": "Region"},
        {"key": "organizationType", "label": "Type"},
        {"key": "contactPhone", "label": "Phone"},
        {"key": "contactEmail", "label": "Email"},
    ]
    rows = [{
        "bin": r.bin, "organizationName": r.organization_name, "region": r.region,
        "organizationType": r.organization_type, "contactPhone": r.contact_phone,
        "contactEmail": r.contact_email,
    } for r in qs.order_by("organization_name")]
    return kpis, charts, columns, rows


def _provider_speed(filters):
    qs = _apply_common(DemoProviderSpeedRecord.objects.all(), filters,
                       date_field="test_date")
    if filters.get("provider"):
        qs = qs.filter(provider_name=filters["provider"])
    agg = qs.aggregate(dl=Avg("download_speed"), ul=Avg("upload_speed"),
                       lat=Avg("latency_ms"))
    by_provider = (qs.values("provider_name")
                   .annotate(value=Avg("download_speed")).order_by("-value"))
    by_region = (qs.values("region")
                 .annotate(value=Avg("download_speed")).order_by("-value"))
    kpis = [
        {"key": "avgDownload", "label": "Avg Download (Mbps)",
         "value": round(_num(agg["dl"]), 1), "format": "number"},
        {"key": "avgUpload", "label": "Avg Upload (Mbps)",
         "value": round(_num(agg["ul"]), 1), "format": "number"},
        {"key": "avgLatency", "label": "Avg Latency (ms)",
         "value": round(_num(agg["lat"]), 1), "format": "number"},
    ]
    charts = [
        {"type": "BAR_CHART", "title": "Avg Download by Provider",
         "data": [{"label": r["provider_name"], "value": round(_num(r["value"]), 1)}
                  for r in by_provider]},
        {"type": "BAR_CHART", "title": "Avg Download by Region",
         "data": [{"label": r["region"], "value": round(_num(r["value"]), 1)}
                  for r in by_region]},
    ]
    columns = [
        {"key": "testDate", "label": "Date"},
        {"key": "region", "label": "Region"},
        {"key": "providerName", "label": "Provider"},
        {"key": "downloadSpeed", "label": "Download"},
        {"key": "uploadSpeed", "label": "Upload"},
        {"key": "latencyMs", "label": "Latency"},
        {"key": "qualityScore", "label": "Quality"},
    ]
    rows = [{
        "testDate": str(r.test_date), "region": r.region,
        "providerName": r.provider_name, "downloadSpeed": _num(r.download_speed),
        "uploadSpeed": _num(r.upload_speed), "latencyMs": _num(r.latency_ms),
        "qualityScore": _num(r.quality_score),
    } for r in qs.order_by("test_date")]
    return kpis, charts, columns, rows


def _procurement(filters):
    qs = DemoProcurementRecord.objects.all()
    if filters.get("region"):
        qs = qs.filter(region=filters["region"])
    if filters.get("status"):
        qs = qs.filter(status=filters["status"])
    total = qs.count()
    won = qs.filter(result="WON").count()
    lost = qs.filter(result="LOST").count()
    by_region = qs.values("region").annotate(value=Count("id")).order_by("-value")
    kpis = [
        {"key": "totalLots", "label": "Number of Lots", "value": total,
         "format": "number"},
        {"key": "won", "label": "Won", "value": won, "format": "number"},
        {"key": "lost", "label": "Lost", "value": lost, "format": "number"},
    ]
    charts = [
        {"type": "PIE_CHART", "title": "Win / Loss",
         "data": [{"label": "Won", "value": won}, {"label": "Lost", "value": lost}]},
        {"type": "BAR_CHART", "title": "Lots by Region",
         "data": [{"label": r["region"] or "N/A", "value": r["value"]}
                  for r in by_region]},
    ]
    columns = [
        {"key": "lotNumber", "label": "Lot #"},
        {"key": "lotTitle", "label": "Title"},
        {"key": "region", "label": "Region"},
        {"key": "plannedAmount", "label": "Planned"},
        {"key": "winningAmount", "label": "Winning"},
        {"key": "competitorCount", "label": "Competitors"},
        {"key": "result", "label": "Result"},
    ]
    rows = [{
        "lotNumber": r.lot_number, "lotTitle": r.lot_title, "region": r.region,
        "plannedAmount": _num(r.planned_amount),
        "winningAmount": _num(r.winning_amount),
        "competitorCount": r.competitor_count, "result": r.result,
    } for r in qs.order_by("lot_number")]
    return kpis, charts, columns, rows


def _sales(filters):
    qs = _apply_common(DemoSalesRecord.objects.all(), filters,
                       date_field="request_date", status_field="status")
    total = qs.count()
    avg_tariff = qs.aggregate(v=Avg("offer_amount"))["v"]
    avg_conv = qs.aggregate(v=Avg("conversion_probability"))["v"]
    by_status = qs.values("status").annotate(value=Count("id")).order_by("-value")
    kpis = [
        {"key": "generatedOffers", "label": "Generated Offers", "value": total,
         "format": "number"},
        {"key": "avgTariff", "label": "Average Tariff",
         "value": round(_num(avg_tariff), 0), "format": "currency"},
        {"key": "avgConversion", "label": "Avg Conversion %",
         "value": round(_num(avg_conv), 1), "format": "number"},
    ]
    charts = [
        {"type": "PIE_CHART", "title": "Requests by Status",
         "data": [{"label": r["status"], "value": r["value"]} for r in by_status]},
    ]
    columns = [
        {"key": "requestDate", "label": "Date"},
        {"key": "region", "label": "Region"},
        {"key": "productName", "label": "Product"},
        {"key": "tariffName", "label": "Tariff"},
        {"key": "offerAmount", "label": "Offer"},
        {"key": "status", "label": "Status"},
    ]
    rows = [{
        "requestDate": str(r.request_date), "region": r.region,
        "productName": r.product_name, "tariffName": r.tariff_name,
        "offerAmount": _num(r.offer_amount), "status": r.status,
    } for r in qs.order_by("request_date")]
    return kpis, charts, columns, rows


# slug -> handler
_HANDLERS = {
    "revenue-overview": _revenue,
    "orders-dashboard": _orders,
    "bin-analytics": _organizations,
    "contacts-dashboard": _organizations,
    "education-healthcare-objects": _organizations,
    "provider-speedtest-map": _provider_speed,
    "government-procurement-analytics": _procurement,
    "saleshelper-dashboard": _sales,
}


def _build(dashboard, filters):
    handler = _HANDLERS.get(dashboard.slug)
    if handler is None:
        return [], [], [], []
    return handler(filters or {})


def get_dashboard_data(dashboard, filters):
    kpis, charts, columns, rows = _build(dashboard, filters)
    return {
        "filters": {k: v for k, v in (filters or {}).items() if v},
        "kpis": kpis,
        "charts": charts,
        "table": {"columns": columns, "rows": rows},
    }


def get_export_table(dashboard, filters):
    _kpis, _charts, columns, rows = _build(dashboard, filters)
    return columns, rows
