# User Flow (summary)

## Viewer flow
Login → Dashboard catalog → choose dashboard → view KPI/charts/table → apply
filters → switch sheets → read instructions → export CSV (if allowed) → logout.

## Admin flow
Login → Admin panel → create category → create dashboard → set access/status →
publish → review audit logs.

## Analyst flow
Login → Admin → create/edit dashboard → add details → publish.

## Routes (frontend)
```
/                       landing
/login
/home
/dashboards             catalog
/dashboards/:slug       detail (sheets, filters, KPI, charts, table, instructions)
/categories
/categories/:slug
/learning
/instructions
/admin
/admin/dashboards
/admin/dashboards/new
/admin/dashboards/:id/edit
/admin/categories
/admin/users
/admin/audit-logs
/settings
```

## Sidebar visibility by role
- EMPLOYEE / MANAGER: no Admin panel.
- ANALYST: Admin panel + dashboard management (no Users/Audit).
- ADMIN: everything.
