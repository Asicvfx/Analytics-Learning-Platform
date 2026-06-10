# CLAUDE.md — guidance for AI agents working on this repo

## What this is
Independent corporate BI & learning platform. Demo prototype, **fake data only**.
Not a Qlik Sense integration. Do not add real corporate data, internal IPs, or
real branding.

## Stack (important — differs from the PDF specs)
The PDF docs mention Spring Boot + React. **The actual implementation uses
Python/Django (backend) and Vue/Nuxt (frontend).** Keep using this stack.

- Backend: Django 5 + DRF + djangorestframework-simplejwt + PostgreSQL
- Frontend: Nuxt 3 + Vue 3 + TypeScript + Tailwind + vue-echarts

## Layout
```
backend/   Django project (config/) + apps/ modules
frontend/  Nuxt 3 app (pages/, components/, stores/, composables/)
docs/      product spec, user flow, architecture, data model & API, handoff
```

### Backend apps
`common` (envelope/pagination/permissions), `accounts` (User+Role+JWT),
`categories`, `dashboards` (+ demo tables + data_service + access logic),
`sheets`, `widgets`, `learning`, `audit`, `export`.

## Conventions
- All API responses use the envelope `{success, data, message}` (+ `pagination`).
- API field names are camelCase (serializers map snake_case ↔ camelCase).
- Role-based access lives in `apps/dashboards/access.py` and
  `apps/common/permissions.py`.
- Dashboard demo data is generated per-slug in
  `apps/dashboards/data_service.py` — keep it simple, one handler per dashboard.
- Audit important actions via `apps.audit.services.log_action`.

## Common commands
```bash
docker compose up --build           # full stack
cd backend && python manage.py migrate
cd backend && python manage.py seed_demo          # (--if-empty to skip if seeded)
cd frontend && npm run dev
```

## Rules
- Implement one feature at a time; keep the first version simple but complete.
- Demo/fake data only. Archive (don't hard-delete) dashboards & categories.
- Update `docs/development_handoff.md` after meaningful changes.
