# Analytics & Learning Platform

Independent corporate BI and learning platform (demo prototype, fake data only).

> Inspired by enterprise BI tools — **not** a Qlik Sense integration and not
> using any real company data.

## Stack

- **Backend:** Python · Django · Django REST Framework · SimpleJWT · PostgreSQL
- **Frontend:** Vue 3 · Nuxt 3 · TypeScript · Tailwind CSS · vue-echarts
- **Local dev:** Docker Compose

## Quick start (Docker)

```bash
cp .env.example .env
docker compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api
- Health check: http://localhost:8000/api/health

On first boot the backend runs migrations and seeds demo data automatically.

> **Windows note:** this folder's name contains an `&` (`Analytics & Learning
> Platform`). On Windows, `&` breaks Node CLI tools (npm/nuxt) launched via
> `cmd.exe`, so running the **frontend** locally outside Docker fails. Either run
> via Docker (the container path `/app` has no `&`), or copy/rename the project
> into a path without `&` (e.g. `C:\projects\analytics-learning-platform`). The
> backend is unaffected.

## Run without Docker

**Backend**

```bash
cd backend
python -m venv .venv && . .venv/Scripts/activate   # Windows
pip install -r requirements.txt
# set POSTGRES_* env vars (or use a local postgres on :5432)
python manage.py migrate
python manage.py seed_demo
python manage.py runserver 0.0.0.0:8000
```

**Frontend**

```bash
cd frontend
npm install
npm run dev
```

## Demo accounts

| Role     | Email                  | Password     |
|----------|------------------------|--------------|
| ADMIN    | admin@example.com      | admin123     |
| ANALYST  | analyst@example.com    | analyst123   |
| MANAGER  | manager@example.com    | manager123   |
| EMPLOYEE | employee@example.com   | employee123  |

## Documentation

See [`docs/`](docs/) — product spec, user flow, architecture, data model & API,
and the development handoff log.
