# Ocean Blue Platform

Public-facing code that consumes `signal.json` and powers the website,
notifications, and (when activated) billing.

**This directory is contractor-safe — no algorithm secrets live here.**

## Architecture

```
signal.json (from private repo)
        │
        ▼
  daily_run.py ───┬──► tracker.html  (regenerated daily)
                  ├──► paper_state.json (paper trading state)
                  └──► notifications/  (email + SMS if rotation)
                              │
                              ▼
                       Subscriber list ← billing/ (Stripe)
```

## Modules

- `daily_run.py` — entry point invoked by GitHub Actions
- `notifications/` — email (SendGrid) + SMS (Twilio) integration stubs
- `billing/` — Stripe integration stubs (subscriptions, referrals)
- `signup/` — waitlist signup handler

## What's "live" vs "stub"

| Module | Status | What's needed to activate |
|---|---|---|
| `daily_run.py` | Live — works as-is | GitHub Action wires it up |
| `notifications/email_sender.py` | Stub | SendGrid account + `SENDGRID_API_KEY` |
| `notifications/sms_sender.py` | Stub | Twilio account + A2P 10DLC registration |
| `billing/stripe_helper.py` | Stub | Stripe account + Products/Prices configured |
| `billing/subscription.py` | Stub | Database choice + persistence layer |
| `billing/referral.py` | Stub | Database choice + persistence layer |
| `signup/handler.py` | Stub | Backend hosting OR keep using Formspree |

## Environment variables (all optional during Phase 1)

```bash
# Email
SENDGRID_API_KEY=
SEND_FROM_EMAIL=signals@oceanblue.example.com
SEND_FROM_NAME="Ocean Blue"

# SMS
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_FROM_NUMBER=

# Billing
STRIPE_SECRET_KEY=
STRIPE_PUBLISHABLE_KEY=
STRIPE_WEBHOOK_SECRET=
STRIPE_PRICE_ID=

# Site
SITE_URL=https://oceanblue.example.com
```
