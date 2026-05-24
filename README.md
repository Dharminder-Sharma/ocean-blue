# Ocean Blue

**Algorithmic QQQ rotation signal service for self-directed IRA investors.**

Operated by Best Kind LLC, Brooklyn, NY.

## What this repository is

This is the **public-facing infrastructure** for Ocean Blue:
- Static marketing website (HTML/CSS, deploys to GitHub Pages)
- Platform code that consumes daily signals (Python)
- Notification/billing integrations (stubs ready to activate)
- Documentation

The signal-generating algorithm itself lives in a **separate, private**
repository. This split is intentional — see `docs/CONTRACTOR_SOW.md`.

## What this repository is NOT

- ❌ NOT the algorithm
- ❌ NOT investment advice
- ❌ NOT currently accepting subscribers (paper trading phase)

## Status

🟡 **Phase 1: Paper Trading**

The site is live. The algorithm runs daily. Subscriptions are not yet open.
Targeted opening: 6 months after launch, following completion of regulatory
review by NY fintech attorney.

## Directory map

```
ocean-blue/
├── public/             # Static website (GitHub Pages serves this)
│   ├── index.html      # Marketing home
│   ├── results.html    # 22-year backtest results
│   ├── tracker.html    # Live paper trading (regenerated daily)
│   ├── pricing.html    # $20/mo, referral program
│   ├── ira.html        # IRA-focused content
│   ├── how-it-works.html, faq.html, about.html, signup.html
│   ├── disclaimer.html, terms.html, privacy.html  # Legal (placeholder)
│   └── assets/style.css
│
├── platform/           # Python code (consumes signal.json)
│   ├── daily_run.py    # Main daily orchestrator
│   ├── notifications/  # SendGrid + Twilio stubs
│   ├── billing/        # Stripe stubs
│   └── signup/         # Waitlist handler
│
├── .github/workflows/  # CI/CD
│   ├── daily.yml       # Daily tracker regeneration
│   └── deploy.yml      # GitHub Pages deploy
│
└── docs/               # Setup, legal, deployment
    ├── SETUP.md            # Step-by-step deployment guide
    ├── LEGAL_TODO.md       # Brief for the fintech attorney
    ├── CONTRACTOR_SOW.md   # IP-protected contractor engagement
    ├── DEPLOYMENT.md
    └── PHASE_PLAN.md
```

## Getting started

See `docs/SETUP.md` for step-by-step deployment instructions.

## Legal status

⚠️ All disclaimer, terms, and privacy text in this repository contains
`[PENDING ATTORNEY REVIEW]` placeholders. Final language must be drafted by a
qualified NY securities attorney before subscriptions open. See
`docs/LEGAL_TODO.md` for the complete brief.

## License

Proprietary. © 2026 Best Kind LLC. All rights reserved.
