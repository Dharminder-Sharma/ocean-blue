# Ocean Blue — Delivery Summary

**Date:** May 17, 2026
**Delivered:** Full Ocean Blue SaaS scaffold — website, platform, integrations, docs
**Status:** Phase 1 ready to deploy; Phase 2-3 wired but inactive pending lawyer

---

## 📦 What's in the box

**12 marketing website pages** (mobile-responsive, SEO-optimized):

| Page | Status |
|---|---|
| `index.html` | ✅ Full marketing home page, hero, stats, pricing teaser |
| `results.html` | ✅ 22-year backtest with year-by-year table |
| `tracker.html` | ✅ Live tracker template (auto-regenerated daily) |
| `pricing.html` | ✅ $20/mo, referral program, free during paper trading |
| `ira.html` | ✅ IRA-focused content with custodian list |
| `how-it-works.html` | ✅ Full strategy mechanics explainer |
| `faq.html` | ✅ 14 Q&As |
| `about.html` | ✅ Best Kind LLC context |
| `signup.html` | ✅ Waitlist form (Formspree-ready) |
| `disclaimer.html` | ⚠️ Placeholder structure — needs lawyer text |
| `terms.html` | ⚠️ Placeholder structure — needs lawyer text |
| `privacy.html` | ⚠️ Placeholder structure — needs lawyer text |

**Supporting files:** `assets/style.css` (full design system), `favicon.svg`, `robots.txt`, `sitemap.xml`, `CNAME`.

**6 Python modules** (Stripe / SendGrid / Twilio integrations — built, not yet activated):
- `signal_engine/signal_engine.py` — IP-protected wrapper around algorithm
- `platform/daily_run.py` — orchestrates paper trading + tracker regen
- `platform/notifications/email_sender.py` — SendGrid stub
- `platform/notifications/sms_sender.py` — Twilio stub with TCPA opt-out handling
- `platform/billing/stripe_helper.py` — Stripe Checkout + Customer Portal + webhooks
- `platform/billing/subscription.py` + `referral.py` — subscriber lifecycle + referral credits
- `platform/signup/handler.py` — waitlist signup writer

**Email/SMS templates** ready to send (pending attorney + service activation):
- `email_alert.html` — signal rotation alert
- `email_welcome.html` — new subscriber welcome with referral code
- `sms_alert.txt` — TCPA-compliant SMS with STOP language

**2 GitHub Actions workflows:**
- `daily.yml` — runs every weekday at 6 PM ET, regenerates tracker
- `deploy.yml` — auto-deploys site on every push to main

**6 documentation files:**
- `README.md` — project overview
- `docs/SETUP.md` — step-by-step deployment from zero (Phase 1 → Phase 3)
- `docs/LEGAL_TODO.md` — **the attorney brief** (12 numbered sections covering RIA registration, Rule 206(4)-1, TCPA, CAN-SPAM, referral solicitor rules, state privacy laws, IRA marketing, and more)
- `docs/CONTRACTOR_SOW.md` — IP-protected engagement template with NDA, IP assignment, 3-year non-compete, liquidated damages
- `docs/PHASE_PLAN.md` — Phase 1 → 2 → 3 timeline
- `docs/DEPLOYMENT.md` — hosting options and secrets management

---

## 🟢 What's ready to launch TODAY

Phase 1 — **Paper Trading Only, $0/month operating cost:**

1. Static marketing site → GitHub Pages
2. Live paper trading tracker → auto-regenerated daily by GitHub Actions
3. Waitlist signup → Formspree (free tier)
4. Historic backtest results → fully populated with v3.4 backtest data (now superseded by v3.5.1)
5. Algorithm runs daily on Ted's PC → signal.json pushed to private repo

**Cost to operate Phase 1:** $0 (optional: $10/yr for custom domain).
**Operator effort:** ~0 hours/week after initial setup. Algorithm runs in cron.

---

## 🟡 What's wired but INACTIVE pending lawyer + accounts

Phase 2-3 features (subscriber notifications, billing, referrals):

| Feature | Code status | Activation requires |
|---|---|---|
| Stripe billing | ✅ stubs written | Stripe account, products, attorney sign-off |
| SendGrid email | ✅ stubs written | SendGrid account, domain auth (DKIM/SPF/DMARC) |
| Twilio SMS | ✅ stubs written | Twilio account, A2P 10DLC registration (3-week lead time) |
| Referral credits | ✅ stubs written | DB hosting + attorney sign-off on solicitor structure |
| Subscriber portal | ✅ Stripe Customer Portal in helpers | Stripe Customer Portal config |
| Final disclaimers | ⚠️ all `[PENDING ATTORNEY REVIEW]` | NY fintech attorney engagement |

---

## 🔴 What you should NOT skip before commercial launch

These are the gates. Skipping any of them creates real legal risk:

1. **NY fintech attorney engagement** (memory #22: $500–$1,500)
   - Hand them `docs/LEGAL_TODO.md` and this codebase
   - 12 specific decisions needed before launch
   - Expected outcome: RIA determination memo, finalized disclaimer/ToS/Privacy text, approved templates and referral program

2. **Twilio A2P 10DLC registration** — 1–3 week lead time
   - $4 brand registration + $10/mo + $15 vetting fee
   - Start the application in Phase 2; don't wait until launch week
   - Without it, US carriers will block your SMS

3. **SendGrid domain authentication** — required for deliverability
   - Add DKIM, SPF, DMARC DNS records
   - Without it, your emails land in spam at Gmail/Outlook

4. **Replace all `[PENDING ATTORNEY REVIEW]` markers** — currently in:
   - `index.html` (footer)
   - `results.html` (hypothetical performance block)
   - `disclaimer.html` (all 12 sections)
   - `terms.html` (all 10 sections)
   - `privacy.html` (all sections)
   - `pricing.html` (referral structure language)
   - `signup.html` (consent language)
   - `ira.html` (tax disclaimer)
   - Email templates
   - SMS template

---

## 🎯 Your immediate next 3 actions

1. **Get attorney referral from William Furlow.** Send them `docs/LEGAL_TODO.md`.

2. **Create the two GitHub repos** (public `ocean-blue` + private `ocean-blue-signals`) and push this code. See `docs/SETUP.md` step 1.1–1.7.

3. **Decide: contractor or DIY?** If contractor, use `docs/CONTRACTOR_SOW.md` as the engagement template. If DIY, follow `docs/SETUP.md` end-to-end.

---

## 📐 Architecture diagram

```
   PRIVATE (Ted only)                          PUBLIC (GitHub + Pages)
   ───────────────────                         ───────────────────────
   
   ~/signal-engine-workspace/
     │
     │ qqq_v35_production.py  (algorithm)
     │ signal_engine.py       (wrapper)
     │
     └─► daily at 5:30 PM ET:
              produces signal.json (6 fields only)
              git pushes to:
                                    ocean-blue-signals (PRIVATE REPO)
                                          │
                                          │ deploy key (read-only)
                                          ▼
                                  ocean-blue (PUBLIC REPO)
                                    │ Daily Action (6:00 PM ET):
                                    │   pulls signal.json
                                    │   runs platform/daily_run.py
                                    │   regenerates tracker.html
                                    │   commits + pushes
                                    │
                                    └─► GitHub Pages: oceanblue.com
                                            (visitors see updated tracker)
```

Subscriber notifications (when Phase 3 activates):

```
Signal rotation occurs
       │
       ▼
daily_run.py detects position change
       │
       ├─► notifications.email_sender → SendGrid → subscribers' inboxes
       └─► notifications.sms_sender   → Twilio    → subscribers' phones
                                              ↑
                                              │
                                       Subscriber list pulled from
                                       Stripe Active Subscriptions
                                       (via stripe_helper.list_active_subscribers)
```

---

## 💰 Operating cost projection

| Phase | Monthly cost | What's running |
|---|---|---|
| 1 (today) | $0 | GitHub Pages + Formspree free tiers |
| 2 (pre-launch) | $0–30 | Same + maybe Formspree paid tier |
| 3 (commercial launch, <100 subs) | ~$25 + per-message | + SendGrid $20 + Twilio $1 + A2P fees |
| 3 (scale, 1000 subs) | ~$60 + per-message | + Stripe fees (2.9% of $20K = $600/mo) |

At 1000 subs paying $20/mo = $240K annual revenue against ~$2,000/yr platform cost. Lawyer one-time cost ~$1,500. Total Year 1 net (assuming linear ramp): ~$120K.

---

## ⚠️ Specific regulatory risks if you skip the attorney

This isn't theoretical. Here's what happens in the worst case:

| Risk | Specific exposure |
|---|---|
| Unregistered RIA | NY can issue cease-and-desist; potential fine + return of fees |
| Rule 206(4)-1 violation | SEC enforcement action, return of fees |
| TCPA violation | $500–$1,500 PER MESSAGE statutory damages, class action exposure |
| CAN-SPAM violation | $51,744 per violation FTC (2024 rate) |
| State privacy violations | CCPA: $7,500 per intentional violation |
| Hypothetical performance misuse | SEC enforcement; possible private right of action |

**The $500–$1,500 attorney engagement is the cheapest insurance you'll ever buy.** Do it before opening subscriptions, not after.

---

## What I'd do next if I were you

Today: read `docs/LEGAL_TODO.md` end-to-end. Get the attorney referral started.
This week: create the GitHub repos, push the code, get the static site live.
This month: replace `oceanblue.example.com` with a real domain you bought.
Next 6 months: paper trade publicly; let the attorney work; activate Phase 3 readiness; launch when paper trading completes and attorney signs off.
