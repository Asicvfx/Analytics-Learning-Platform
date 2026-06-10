# Deploy runbook

Topology: **Nuxt → Vercel**, **Django → Render**, **PostgreSQL → Supabase**.

```
Nuxt (Vercel)  ──HTTPS──►  Django (Render)  ──SSL──►  Postgres (Supabase)
```

---

## 0. Push to GitHub (one-time)

The repo is already committed locally. Create an **empty** GitHub repo (no
README / .gitignore), then:

```bash
git remote add origin https://github.com/<you>/<repo>.git
git push -u origin main
```

---

## 1. Supabase (database)

1. Create a project. Pick a strong DB password.
2. **Settings → Database → Connection string → URI**, and choose the
   **Session pooler** tab (IPv4-friendly; the direct connection is IPv6-only
   and Render can't reach it).
3. Copy the URI. It looks like:
   `postgresql://postgres.<ref>:<password>@aws-0-<region>.pooler.supabase.com:5432/postgres`
   This is your `DATABASE_URL`. (Replace `[YOUR-PASSWORD]` with the real one.)

> No need to run migrations manually — the backend runs `migrate` + `seed_demo`
> on every deploy via `entrypoint.sh`.

---

## 2. Render (backend)

**Option A — Blueprint (uses `render.yaml`):** New → Blueprint → pick the repo.
**Option B — manual:** New → Web Service → repo → Runtime **Docker**, Dockerfile
`./backend/Dockerfile`, context `./backend`, Health check `/api/health`.

Environment variables to set:

| Key | Value |
|-----|-------|
| `DJANGO_DEBUG` | `false` |
| `DJANGO_SECRET_KEY` | a long random string |
| `DJANGO_ALLOWED_HOSTS` | your Render host, e.g. `alp-backend.onrender.com` |
| `DATABASE_URL` | the Supabase Session-pooler URI from step 1 |
| `DB_SSL_REQUIRE` | `true` |
| `CORS_ALLOWED_ORIGINS` | your Vercel URL (fill after step 3) |
| `CSRF_TRUSTED_ORIGINS` | your Vercel URL, e.g. `https://your-app.vercel.app` |

Deploy. Verify: `https://<render-host>/api/health` → `{"success": true, ...}`.

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
