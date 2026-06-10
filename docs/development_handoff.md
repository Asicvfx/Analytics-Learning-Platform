# Development Handoff

## Status: First version scaffolded end-to-end (demo data only)

### Implemented
- **Monorepo**: `backend/` (Django), `frontend/` (Nuxt 3), `docs/`,
  `docker-compose.yml`, `.env.example`.
- **Auth**: JWT login/logout/me, custom email `User`, `Role`, `UserRole`.
- **RBAC**: role permission classes + per-dashboard view/export/edit logic.
- **Catalog**: categories + dashboards (card list, detail with sheets +
  learning), search/filter, role-filtered visibility.
- **Dashboard viewer**: sheet tabs, filters, KPI cards, charts (echarts),
  data table (sort + pagination), instructions tab.
- **CSV export**: filter-aware, permission-checked, writes audit log.
- **Learning materials**: instructions/video/presentation/FAQ per dashboard.
- **Admin panel**: dashboards (create/edit/archive), categories (create/archive),
  users (list/create), audit logs (list).
- **Audit**: login, dashboard open, export, dashboard/category/user CRUD.
- **Seed**: `seed_demo` creates 4 roles, 4 users, 10 categories, 8 dashboards
  (sheets + widgets + permissions + learning) and ~330 demo data rows.

### Important files
- Backend: `backend/config/settings.py`, `apps/dashboards/data_service.py`,
  `apps/dashboards/access.py`, `apps/common/{pagination,exceptions,responses}.py`,
  `apps/common/management/commands/seed_demo.py`.
- Frontend: `frontend/stores/auth.ts`, `composables/useApi.ts`,
  `pages/dashboards/[id].vue`, `components/ChartCard.client.vue`,
  `components/DataTable.vue`.

### How to run
`docker compose up --build` → frontend :3000, backend :8000.
Backend auto-migrates and seeds on first boot.

### Verified in this session
- Backend: `makemigrations`, `migrate`, `seed_demo`, and `check` all pass.
- Live API smoke test (SQLite): login, RBAC visibility (employee sees 5, manager
  8), 403 on unauthorized dashboard, CSV export (200 + filtered rows), audit
  logging, category create, 401 on bad login.
- Frontend: `npm install` + `nuxt build` succeed (verified in an `&`-free path).

### Windows path gotcha (important)
The project folder name contains `&`. On Windows this breaks Node CLI tools
(npm/nuxt) via cmd.exe, so the **frontend cannot run locally outside Docker**
from this path. Use Docker (container path `/app`) or copy the repo to a path
without `&`. Backend is unaffected.

### Known limitations / next steps
- Migrations are generated at first `makemigrations`/`migrate` run; if running
  outside Docker, run `python manage.py makemigrations` once if the
  `migrations/` packages are empty.
- Widgets are seeded but the viewer renders KPI/charts/table from
  `data_service` (not yet driven by per-widget config). A future step can map
  widgets → data blocks.
- Admin user edit/deactivate and sheet/widget editors are API-complete but the
  UI exposes create/list only (edit forms can be added next).
- Dashboard data handlers are per-slug; adding a new dashboard with analytics
  means adding a slug handler in `data_service.py`.
- No automated tests yet — add DRF API tests for auth, permissions, export.

### Rules to keep
- Demo/fake data only. No real corporate data, IPs, links, or branding.
- Keep the `{success, data, message}` envelope and camelCase API fields.
- Archive (don't hard-delete) dashboards and categories.
