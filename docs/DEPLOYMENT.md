# Ocean Blue — Deployment Notes

## GitHub Pages (Phase 1)
- Repository must be PUBLIC
- Settings → Pages → Source: "GitHub Actions"
- `.github/workflows/deploy.yml` handles deployment
- Custom domain: set `public/CNAME` to your domain; add CNAME DNS record to `<username>.github.io`
- HTTPS automatic via Let's Encrypt (takes 5-10 min after DNS propagates)

## Phase 3 backend hosting

Three sensible options, pick one:

### Option A: Vercel (free tier OK for small subscriber counts)
- Best for: serverless functions, easy git-driven deploy
- Cost: $0 (free tier) → $20/mo (Pro)
- Stack: Python (FastAPI/Flask) on Vercel Functions

### Option B: Render (simple managed)
- Best for: traditional always-on Flask app
- Cost: $7/mo (Starter) → $25/mo (Standard)
- Stack: Python (Flask + gunicorn)

### Option C: Railway
- Best for: similar to Render, slightly different pricing model
- Cost: $5 credits/mo free, pay-as-you-go after

## Database (Phase 3)

Recommended for subscriber data:
- **Supabase** (free tier 500MB; Postgres-based) - easy to start
- **Neon** (free tier 0.5GB; Postgres serverless)
- **Cloudflare D1** (free 5GB SQLite)

For start-up scale, any of these is fine. Migrate later if needed.

## Secrets management

Never commit:
- `.env` files
- API keys
- Stripe webhook secrets
- TIINGO API key

Use GitHub Secrets for CI: Settings → Secrets and variables → Actions

For backend hosting, use the host's environment variable feature
(Vercel: Project Settings → Environment Variables, etc.).
