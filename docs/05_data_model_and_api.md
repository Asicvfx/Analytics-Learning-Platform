# Data Model & API (as implemented)

## Tables
`users`, `roles`, `user_roles`, `categories`, `dashboards`,
`dashboard_permissions`, `dashboard_sheets`, `dashboard_widgets`,
`learning_materials`, `audit_logs`, and demo tables:
`demo_revenue_records`, `demo_order_records`, `demo_organization_records`,
`demo_provider_speed_records`, `demo_procurement_records`, `demo_sales_records`.

## Enums
- User status: `ACTIVE`, `INACTIVE`.
- Role: `ADMIN`, `ANALYST`, `MANAGER`, `EMPLOYEE`.
- Dashboard status: `DRAFT`, `PUBLISHED`, `ARCHIVED`.
- Access level: `ADMIN_ONLY`, `ANALYST_ONLY`, `MANAGER`, `EMPLOYEE`,
  `PUBLIC_INTERNAL`.
- Widget type: `KPI_CARD`, `BAR_CHART`, `LINE_CHART`, `PIE_CHART`,
  `DATA_TABLE`, `TEXT_BLOCK`.

## API endpoints

### Auth
- `POST /api/auth/login`
- `POST /api/auth/logout`
- `GET  /api/auth/me`

### Categories
- `GET    /api/categories` (`?active=true`)
- `GET    /api/categories/{idOrSlug}`
- `POST   /api/admin/categories`
- `PUT    /api/admin/categories/{id}`
- `DELETE /api/admin/categories/{id}` (archive: `is_active=false`)

### Dashboards
- `GET    /api/dashboards` (`?search=&category=&tag=&status=&page=&size=`)
- `GET    /api/dashboards/{idOrSlug}`
- `GET    /api/dashboards/{idOrSlug}/data` (+ filters)
- `GET    /api/dashboards/{idOrSlug}/export.csv` (+ filters)
- `POST   /api/admin/dashboards`
- `PUT    /api/admin/dashboards/{id}`
- `DELETE /api/admin/dashboards/{id}` (archive)

### Sheets
- `GET    /api/dashboards/{dashboardId}/sheets`
- `POST   /api/admin/dashboards/{dashboardId}/sheets`
- `PUT    /api/admin/sheets/{sheetId}`
- `DELETE /api/admin/sheets/{sheetId}`

### Widgets
- `GET    /api/sheets/{sheetId}/widgets`
- `POST   /api/admin/sheets/{sheetId}/widgets`
- `PUT    /api/admin/widgets/{widgetId}`
- `DELETE /api/admin/widgets/{widgetId}`

### Learning
- `GET  /api/dashboards/{dashboardId}/learning`
- `POST /api/admin/dashboards/{dashboardId}/learning`
- `PUT  /api/admin/learning/{learningId}`

### Users (admin)
- `GET  /api/admin/users`
- `POST /api/admin/users`
- `PUT  /api/admin/users/{id}`

### Audit (admin)
- `GET /api/admin/audit-logs`

## Dashboard data filters
`dateFrom, dateTo, region, status, category, provider, organizationType, sheet`.

## Permission logic
- **View:** ADMIN, or access_level grants the user's role, or a
  `dashboard_permissions` row with `can_view=true`.
- **Export:** ADMIN, or `dashboard_permissions.can_export=true`.
- **Edit:** ADMIN, any ANALYST (first version), or `can_edit=true`.

See `apps/dashboards/access.py`.
