# CLAUDE.md — guidance for AI agents working on this repo

## What this is
Kazakhtelecom Business BI & learning portal: a catalog of **external** reports
(Qlik Sense apps, web tools, Telegram bots) with per-report learning materials
(instructions / presentation / video) and an FAQ. The app does **not** render the
analytics itself — each report links out to its real system (e.g.
`https://qtest/sense/app/...` or internal `10.x` hosts that open only from the
corporate network/VPN).

Per the owner's decision (2026-06), the catalog uses **real** Kazakhtelecom
content seeded in `seed_demo.py` (links, descriptions, BI-department contacts).
This overrides the earlier "fake data only" rule. Be mindful: qtest/10.x links
won't open from the public Vercel deploy, and the contacts are real PII.

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
`categories`, `dashboards` (a "dashboard" = a report: title, description,
`report_url` + `report_kind` QLIK/WEB/BOT, access level), `sheets`, `widgets`,
`learning` (instructions/presentation/video/FAQ), `audit`, `export`.
Note: `sheets`, `widgets`, `data_service.py` and the demo tables are legacy from
the old internal-rendering model and are no longer used by the report page.

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
- Catalog content lives in `seed_demo.py` (authoritative). `seed_demo --reseed`
  wipes & rebuilds the catalog (keeps users); on Render set env `RESEED=1` once
  to apply, then remove it. UI is Russian (Kazakhtelecom Business).
- Update `docs/development_handoff.md` after meaningful changes.
