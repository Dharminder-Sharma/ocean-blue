# Ocean Blue — Environment Variables Reference

Quick reference: which env var goes WHERE.

## Three locations for env vars

| Location | Purpose | Source file |
|---|---|---|
| **Your PC (`signal_engine/.env`)** | Algorithm runtime + Bitbucket push | `signal_engine/.env.example` |
| **GitHub Repo Secrets** | GitHub Actions pull from Bitbucket | (set in GitHub UI) |
| **Backend hosting `.env`** (Phase 3) | Stripe/SendGrid/Twilio | `platform/.env.example` |

## Phase 1 — Paper trading only

Only your PC needs anything. Copy `signal_engine/.env.example` to `signal_engine/.env`, fill in:

```
TIINGO_API_KEY=          # from tiingo.com → Account → API
SIGNALS_REPO_PATH=       # path to your local Bitbucket clone
```

That's it. GitHub Pages and the GitHub Action need nothing yet (the daily.yml only activates once you set BITBUCKET_* secrets).

## Phase 2 — Pre-launch (during lawyer review)

Add to GitHub Repository Secrets (GitHub → ocean-blue → Settings → Secrets and variables → Actions):

```
BITBUCKET_USER           # your Bitbucket username
BITBUCKET_APP_PASSWORD   # App Password from Bitbucket (read-only)
```

How to create the BITBUCKET_APP_PASSWORD:
1. Log into Bitbucket
2. Personal Settings → App Passwords → Create new
3. Label: `github-actions-signals-read`
4. Permissions: ✓ Repositories → Read (everything else unchecked)
5. Click Create — copy the password (shown once)
6. Paste into GitHub Secret

## Phase 3 — Commercial launch

Backend hosting (Vercel/Render/Railway/Fly.io) needs the variables in `platform/.env.example`:

- **Stripe** (4 keys): for billing
- **SendGrid** (3 vars): for email
- **Twilio** (3 vars): for SMS
- **Site** (2 vars): for redirect URLs and from-addresses
- **Database** (1 var): subscriber data persistence

Each hosting provider has a UI for setting these:
- Vercel: Project Settings → Environment Variables
- Render: Dashboard → service → Environment
- Railway: project → Variables
- Fly.io: `fly secrets set KEY=value`

## What NEVER goes into git

These should be in `.gitignore` and never committed to any repo:

- `signal_engine/.env`
- `platform/.env`
- Any file containing API keys, passwords, or tokens
- `state.json`, `paper_state.json`, `*.sqlite` (state files)

The repo's `.gitignore` already excludes these. The `.env.example` files (no actual secrets) are safe to commit and serve as templates.

## Security checklist before launch

- [ ] Never paste real Stripe/SendGrid/Twilio keys into chat, Slack, email, or GitHub PRs
- [ ] Use Stripe TEST keys (`sk_test_...`) during development; switch to LIVE keys only post-lawyer
- [ ] Rotate any key that's ever been exposed
- [ ] Use Bitbucket App Password (not your account password) for the GitHub Action
- [ ] Restrict App Password permissions to read-only on the signals repo only
- [ ] GitHub Repository Secrets are encrypted at rest — safe to store there
- [ ] Do NOT use environment files in `public/` directory (they'd be served to the web)
