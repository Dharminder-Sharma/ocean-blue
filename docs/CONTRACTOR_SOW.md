# Ocean Blue — Contractor Statement of Work

**Purpose:** If/when you hire a contractor to build out the backend, this
document defines what they get to see and what they don't.

**Principle:** The contractor builds the platform (website, billing,
notifications) but never sees the signal-generating algorithm. They test
against mock `signal.json` files. The split protects Best Kind LLC's IP.

---

## Scope: what the contractor builds

The contractor builds and maintains the contents of this repository, specifically:

- ✅ Public website (`public/`) — content updates as directed
- ✅ Platform code (`platform/`) — daily_run.py, integrations, signup
- ✅ GitHub Actions workflows (`.github/`)
- ✅ Backend hosting deployment (Vercel/Render/Railway/etc.)
- ✅ Stripe integration (subscriptions, webhooks, customer portal)
- ✅ SendGrid integration (transactional email, templates, deliverability)
- ✅ Twilio integration (SMS, inbound webhook for STOP keywords)
- ✅ Subscriber database (schema, migration, backup)
- ✅ Monitoring and alerting (uptime, errors)

## Scope: what the contractor does NOT see

- ❌ The `signal_engine/` directory — this lives in a PRIVATE repository
- ❌ The `qqq_v35_production.py` algorithm
- ❌ Any algorithm parameters, formulas, or backtest source
- ❌ The Tiingo API key (not needed — contractor uses mock signals)
- ❌ Production state files (`state.json`, `signal_log.csv`, etc.)
- ❌ Real signal_history.jsonl (use mock data instead)

## How the contractor tests

The contractor receives a **mock signal.json** for development:

```json
{
  "date": "2026-01-15",
  "action": "QQQ",
  "qqq_close": 425.50,
  "tlt_close": 92.15,
  "signed_at": "2026-01-15T17:30:00",
  "version": "mock-v1"
}
```

And a **mock signal history** (sequence of rotation events) for testing the
paper trading state machine and tracker generation. These mocks can be safely
shared without revealing anything about the actual algorithm.

## Legal protections required (before any code share)

### Mutual NDA

Standard mutual NDA covering all materials shared during the engagement. Key
provisions:
- 5-year confidentiality period
- Surviving obligations re: trade secrets indefinitely
- No reverse engineering, no derivative algorithms
- Return/destroy materials at engagement end

### IP Assignment ("Work Made for Hire" + Catch-All)

All code, designs, documentation produced for this engagement:
- Is "work made for hire" under 17 USC § 101 to the extent eligible
- For anything NOT eligible as work-for-hire, contractor assigns all rights to Best Kind LLC
- Contractor disclaims any moral rights waivable under applicable law
- Best Kind LLC has perpetual, worldwide license to all delivered work

### Non-Compete (3-year, narrow scope)

Contractor agrees for 36 months following engagement end:
- Not to provide similar services to any other algorithmic-signal subscription business
- Not to use any Ocean Blue trade secrets in any other work
- Specific carve-out: contractor may continue general web/platform development for clients in other industries

### Liquidated Damages

Breach of confidentiality or IP terms triggers $50,000 liquidated damages PER
INCIDENT, plus injunctive relief, plus reasonable attorney fees. (NY-enforceable
if reasonable and tied to actual anticipated damage — confirm with attorney.)

### Governing Law

New York. Venue: Brooklyn courts. JAMS arbitration for monetary disputes
under $25,000; court for IP disputes and injunctive relief.

### Background Check Consent

Contractor consents to a basic background check (LinkedIn verification + one
reference call from a prior client). Not a deep check — just enough to verify
they're a real person with a working track record.

---

## Engagement structure: build-and-handoff with retainer

**Phase A — Build (4–8 weeks)**

Fixed-fee engagement to deliver Phase 3 (billing + notifications) ready to
launch. Recommended deliverables:

- [ ] Backend hosted and deployed (Vercel/Render)
- [ ] Stripe Checkout + Customer Portal working end-to-end
- [ ] SendGrid integrated, test emails landing in inbox
- [ ] Twilio integrated with A2P 10DLC registered, STOP keyword working
- [ ] Subscriber DB schema deployed
- [ ] Webhook handler tested for all relevant Stripe events
- [ ] Documentation handed off (deployment, ops, troubleshooting)
- [ ] Code review and walk-through with Ted

**Phase B — Retainer (monthly, $X/mo)**

Optional ongoing retainer for:
- Production issue response (24-hour acknowledge, 72-hour fix)
- Minor updates as needed
- Security patches
- Compliance updates as legal landscape changes

---

## Budget guidance

Realistic ranges for the Phase A build:

| Skill level | Estimated total cost | Notes |
|---|---|---|
| Senior full-stack contractor | $8,000–$15,000 | 4–6 weeks |
| Mid-level contractor | $4,000–$8,000 | 6–8 weeks; more hand-holding |
| Junior contractor | $2,000–$4,000 | High risk on Stripe/security; needs supervision |

Retainer: typically $200–$500/mo for a senior on call.

---

## Anti-pitfall list (what NOT to do)

- ❌ Don't grant contractor access to the `ocean-blue-signals` private repo
- ❌ Don't share the actual qqq_v35_production.py — they don't need it
- ❌ Don't let contractor write the signal-engine code or "improve" the algorithm
- ❌ Don't pay 100% upfront. Recommend 25% start, 25% midpoint demo, 50% on accepted handoff
- ❌ Don't skip the IP assignment paperwork. Without it, you might not own what they wrote
- ❌ Don't accept a contractor who insists on using "their stack" — pick a stack you can maintain
- ❌ Don't engage a contractor located in a jurisdiction where contract enforcement is impractical

## When to hire a contractor vs. do it yourself

**Do it yourself if:**
- You're comfortable with command line, git, basic JavaScript/Python
- You have time (20–40 hours over 4 weeks)
- You want to be able to maintain it long-term yourself

**Hire a contractor if:**
- You're spending time on higher-value work (patent prosecution, litigation, FPC, etc.)
- Time-to-launch matters more than learning the stack
- You expect to scale subscribers beyond a few hundred (more operational complexity)

Given Ted's other active matters (per memory: Future Wizards litigation, IECS
wheelchair patent, FPC electronics, tamper-evident seal patent, etc.), a
contractor is likely the better use of Best Kind LLC capital. The $5–10K
spend produces ~$240K of revenue at 1,000 subscribers/yr.
