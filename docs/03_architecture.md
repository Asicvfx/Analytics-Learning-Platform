# Architecture (as implemented)

> Note: the original PDF proposed Spring Boot + React. This project is built
> with **Python/Django + Vue/Nuxt** per the team decision.

```
Browser → Nuxt 3 (Vue) → REST /api → Django + DRF → PostgreSQL
```

## Backend (Django, `backend/`)
- `config/` — settings, urls, wsgi/asgi.
- `apps/common/` — response envelope, pagination, exception handler,
  role permission classes, `TimeStampedModel`, `seed_demo` command.
- `apps/accounts/` — custom email `User`, `Role`, `UserRole`, JWT auth views,
  admin user management.
- `apps/categories/` — `Category` + CRUD/archive.
- `apps/dashboards/` — `Dashboard`, `DashboardPermission`, 6 demo dataset
  tables, `access.py` (view/export/edit logic), `data_service.py`
  (per-slug KPI/chart/table builders), catalog/detail/data/export views,
  admin CRUD.
- `apps/sheets/`, `apps/widgets/` — dashboard pages and visual blocks.
- `apps/learning/` — instructions/video/presentation/FAQ.
- `apps/audit/` — `AuditLog` + `log_action` service + admin list.
- `apps/export/` — CSV export helper.

### Auth
JWT via simplejwt. `POST /api/auth/login` returns `{token, refresh, user}`.
Frontend stores the access token in `localStorage` and sends
`Authorization: Bearer <token>`.

### Response envelope
```json
{ "success": true, "data": <...>, "message": null }
```
List endpoints add `pagination: {page, size, totalElements, totalPages}`
(0-based page).

## Frontend (Nuxt 3, `frontend/`)
- `pages/` — file-based routes (see user flow).
- `layouts/` — `default` (public), `app` (sidebar + topbar).
- `components/` — AppSidebar, AppTopbar, PageHeader, DashboardCard, KpiCard,
  ChartCard (client-only, echarts), DataTable, StateBlocks, UiBadge,
  DashboardInstructions, AdminDashboardForm.
- `stores/auth.ts` (Pinia), `composables/useApi.ts`, `middleware/{auth,admin}.ts`,
  `plugins/auth.client.ts` (restores session on load).

## Local dev
`docker compose up` runs db + backend (migrate + seed + runserver) + frontend.
Ports: frontend 3000, backend 8000, postgres 5432.
