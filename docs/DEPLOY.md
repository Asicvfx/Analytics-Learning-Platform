# Deploy runbook

Topology: **Nuxt → Vercel**, **Django + PostgreSQL → Render**.

```
Nuxt (Vercel)  ──HTTPS──►  Django (Render)  ──internal──►  Postgres (Render)
```

---

## 0. Push to GitHub (one-time)

Already done: `https://github.com/Asicvfx/Analytics-Learning-Platform`.
Future pushes: `git push`.

---

## 1. Render (backend + database)

The `render.yaml` blueprint provisions **both** the web service and a free
PostgreSQL database, and wires the DB's internal `DATABASE_URL` into the
backend automatically.

1. Render → **New → Blueprint** → pick the repo → **Apply**.
2. Render creates `alp-db` (Postgres) and `alp-backend` (web, Docker).
3. The only env vars left blank are the frontend URL ones — fill them after
   Vercel is up (step 3): `CORS_ALLOWED_ORIGINS` and `CSRF_TRUSTED_ORIGINS`.

> Migrations + `seed_demo` run automatically on every deploy via
> `backend/entrypoint.sh`. No manual DB setup.

Verify: `https://<render-host>/api/health` → `{"success": true, ...}`.

> Free Postgres on Render is **deleted 30 days** after creation. For a longer-
> lived demo, swap `DATABASE_URL` to an external DB (e.g. Supabase) later — the
> code reads any `DATABASE_URL`, so only the env var changes.

---

## 3. Vercel (frontend)

1. Import the repo. **Root Directory = `frontend`** (important — it's a monorepo).
2. Framework preset: **Nuxt** (auto-detected). Build/output defaults are fine.
3. Environment variable:

   | Key | Value |
   |-----|-------|
   | `NUXT_PUBLIC_API_BASE` | `https://<render-host>/api` |

4. Deploy → note the resulting URL (e.g. `https://your-app.vercel.app`).

---

## 4. Close the CORS loop

Go back to **Render** and set `CORS_ALLOWED_ORIGINS` and `CSRF_TRUSTED_ORIGINS`
to the Vercel URL from step 3, then redeploy the backend.

---

## 5. Smoke test

- Open the Vercel URL, log in with `admin@example.com / admin123`.
- Dashboards/categories load, charts render, CSV export works.
- If login fails with a network/CORS error, recheck step 4 and that
  `NUXT_PUBLIC_API_BASE` ends with `/api`.

> Demo data only. Change or remove the seeded demo accounts before any real use.
> Render's free plan sleeps on idle — the first request after a pause is slow.
