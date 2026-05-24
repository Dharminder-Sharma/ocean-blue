# Ocean Blue — Setup Guide

Step-by-step instructions to deploy Ocean Blue from zero. Goes from "fresh
GitHub account" to "live site with paper trading." This is the path for Ted
to follow OR to hand to a contractor (without the algorithm).

## Phase 1: GitHub Pages site + paper trading (FREE; no subscribers yet)

**Time:** 2–4 hours
**Cost:** $0 (Tiingo basic plan is free; domain optional)
**Goal:** Static marketing site + live paper trading tracker

### 1.1 Create two GitHub repositories

```
ocean-blue          (PUBLIC)  — marketing site + platform code
ocean-blue-signals  (PRIVATE) — daily signal.json files only
```

GitHub → New Repository:
- Name: `ocean-blue` · Public · No README/license (we'll push our own)
- Name: `ocean-blue-signals` · Private · README only

### 1.2 Set up SSH for git on Ted's PC

```bash
# Generate SSH key if you don't have one
ssh-keygen -t ed25519 -C "ted@bestkind.com"
cat ~/.ssh/id_ed25519.pub
# Copy the output, add to GitHub → Settings → SSH Keys → New SSH key
```

### 1.3 Push the Ocean Blue codebase

From this folder structure:

```bash
cd /path/to/oceanblue
git init -b main
git remote add origin git@github.com:tedbochi/ocean-blue.git
git add .
git commit -m "Initial commit — Phase 1 site"
git push -u origin main
```

### 1.4 Set up the private signals repo (on Bitbucket)

The algorithm and its output history live OFF GitHub for IP protection.
Bitbucket Standard plan: $3/month for unlimited private repos.

```bash
# After creating empty `ocean-blue-signals` repo in Bitbucket web UI:
cd ~
git clone git@bitbucket.org:bestkind/ocean-blue-signals.git
cd ocean-blue-signals
echo '{"date":"","action":"","qqq_close":0,"tlt_close":0,"signed_at":"","version":""}' > signal.json
touch signal_history.jsonl
git add .
git commit -m "Initial empty signal"
git push
```

The `git push` from `signal_engine.py` will go to this Bitbucket repo
automatically because the local clone has Bitbucket as its `origin`.

### 1.5 Enable GitHub Pages

Public repo → Settings → Pages → Source: GitHub Actions

The `deploy.yml` workflow will publish on every push to main.

### 1.6 Set up cross-service auth (GitHub Actions → Bitbucket)

The algorithm and `signal.json` history live in a PRIVATE Bitbucket repo.
The public site is on GitHub. GitHub Actions needs READ access to Bitbucket
to pull each day's signal.

**On Bitbucket:**
1. Sign up at bitbucket.org (or sign in)
2. Create workspace (e.g. `bestkind`) and private repository `ocean-blue-signals`
3. Personal Settings → SSH Keys → add your PC's public key (~/.ssh/id_ed25519.pub)
4. Personal Settings → App Passwords → Create new:
   - Label: `github-actions-read`
   - Permissions: ✓ Repositories → Read (nothing else)
   - Copy the password (shown only once)

**On GitHub:**
1. ocean-blue repo → Settings → Secrets and variables → Actions → New secret
2. Add `BITBUCKET_USER` (your Bitbucket username)
3. Add `BITBUCKET_APP_PASSWORD` (the password from above)

GitHub Actions will use HTTPS basic auth (`https://USER:PASSWORD@bitbucket.org/...`)
to clone the signals repo each day. The credentials only allow READ — they
can't push back, can't modify, can't access other Bitbucket repos.

### 1.7 Move signal engine to private workspace on Ted's PC

```bash
# The signal_engine/ directory needs to be REMOVED from the public repo
# and kept locally instead
cd /path/to/oceanblue
mv signal_engine ~/signal-engine-workspace
git rm -rf signal_engine
git commit -m "Move algorithm to private workspace"
git push

cd ~/signal-engine-workspace
# Copy in the existing production script
cp /path/to/qqq_v35_production.py .
cp .env.example .env
# Edit .env with your TIINGO_API_KEY and paths
```

### 1.8 Test the engine

```bash
cd ~/signal-engine-workspace
python signal_engine.py
# Should produce signal.json in ~/ocean-blue-signals/
# Should git push to the private repo
```

### 1.9 Set up cron (Linux/Mac) or Task Scheduler (Windows)

Linux/Mac (`crontab -e`):

```cron
# Weekdays at 5:30 PM ET (assuming PC is in ET timezone)
30 17 * * 1-5 cd ~/signal-engine-workspace && python signal_engine.py >> run.log 2>&1
```

Windows (Task Scheduler): create a daily task running at 5:30 PM, action:
`python C:\signal-engine-workspace\signal_engine.py`.

### 1.10 Update site URLs

Replace `oceanblue.example.com` throughout `public/` with your real domain:

```bash
cd /path/to/oceanblue
find public -type f -name "*.html" -exec sed -i '' 's|oceanblue.example.com|YOUR_DOMAIN.com|g' {} \;
git commit -am "Update domain URLs"
git push
```

### 1.11 Set up Formspree for the waitlist

1. Sign up at formspree.io (free tier: 50 submissions/month)
2. Create a new form
3. Copy your form ID
4. Edit `public/signup.html` and replace `YOUR_FORM_ID_HERE`

### 1.12 (Optional) Custom domain

1. Buy a domain (Namecheap, Cloudflare Registrar — usually $10–$15/yr)
2. GitHub Pages settings → Custom domain → enter `oceanblue.yourdomain.com`
3. DNS provider → add CNAME record pointing your domain to `tedbochi.github.io`
4. Update `public/CNAME` to your actual domain

**END OF PHASE 1.** You now have a live marketing site, live paper trading
tracker, and waitlist signup — at $0/month in operating cost.

---

## Phase 2: Get the lawyer engaged (during paper trading months 1–4)

**Goal:** Finalize legal language before subscriptions open.

1. Get NY fintech attorney referral from William Furlow
2. Send the attorney `docs/LEGAL_TODO.md` along with this codebase
3. Schedule kickoff call
4. Goal deliverables (per LEGAL_TODO.md):
   - RIA determination memo
   - Final disclaimer, ToS, Privacy Policy
   - Approved SMS/email templates
   - Approved referral program structure
5. Replace all `[PENDING ATTORNEY REVIEW]` markers with finalized text
6. Commit and push the updated language

---

## Phase 3: Activate billing + notifications (paper trading months 5–6)

**Goal:** Be ready for commercial launch the day paper trading concludes.

### 3.1 Sign up for services (in this order)

**SendGrid (email)** — sign up at sendgrid.com
- Free tier: 100 emails/day forever; paid starts at $19.95/mo
- Verify your sending domain (DKIM/SPF/DMARC) — REQUIRED for deliverability
- Get an API key, store in environment

**Twilio (SMS)** — sign up at twilio.com  
- Buy a phone number (~$1/mo)
- ⚠️ A2P 10DLC registration — START EARLY (1–3 weeks lead time)
  - Brand registration: $4 one-time
  - Campaign registration: $10/mo + $15 vetting
- Get Account SID + Auth Token

**Stripe (billing)** — sign up at stripe.com
- Activate account (requires business verification, takes 1–2 days)
- Dashboard → Products → New: "Ocean Blue Monthly", $20.00/mo recurring
- Save the `price_xxx` ID
- Dashboard → Customer Portal → enable
- Set up webhook endpoint (we'll deploy this in 3.3)

### 3.2 Choose backend hosting

GitHub Pages is static-only. For Phase 3 you need a server to handle:
- Stripe webhook events
- Subscription signup flow (alternative to using only Checkout)
- Subscriber portal (optional — Stripe Customer Portal covers most cases)

Recommended free/cheap options:
- **Vercel** (free tier) — easy if using Next.js
- **Render** (free tier with cold starts; $7/mo for always-on)
- **Railway** ($5 of credits free)
- **Fly.io** (free tier for small VMs)

### 3.3 Deploy the backend

The Python platform code in `platform/` can run as a small Flask service.
Detailed deployment is environment-specific. The minimum endpoints needed:

```
GET  /                        — redirect to GitHub Pages site
POST /api/signup              — handle waitlist signup
POST /api/checkout            — create Stripe Checkout session
POST /api/stripe-webhook      — process Stripe events
GET  /api/portal/:customer    — redirect to Stripe Customer Portal
POST /api/sms-webhook         — handle inbound SMS (STOP/HELP)
```

### 3.4 Final pre-launch checklist

- [ ] Lawyer has signed off on all documents
- [ ] All `[PENDING ATTORNEY REVIEW]` placeholders replaced
- [ ] SendGrid domain auth complete (DKIM/SPF/DMARC passing)
- [ ] Twilio A2P 10DLC registration complete
- [ ] Stripe account activated; products configured; webhook listening
- [ ] Privacy policy compliant with all states you'll serve
- [ ] Test signup flow end-to-end with a real card (then refund)
- [ ] Test referral flow with two test accounts
- [ ] Test STOP keyword on a real phone
- [ ] Test welcome email lands in inbox (not spam) at Gmail, Outlook, Yahoo
- [ ] Set up uptime monitoring (free at uptimerobot.com)
- [ ] Set up Stripe email alerts for failed payments
- [ ] Backup procedure for subscriber database

---

## Operational rhythm once live

- **Daily 5:30 PM ET:** `signal_engine.py` runs on Ted's PC, publishes signal
- **Daily 6:00 PM ET:** GitHub Action regenerates tracker.html, dispatches notifications
- **Weekly:** Review delivery stats (SendGrid, Twilio dashboards) for issues
- **Monthly:** Review Stripe metrics (active subs, churn, MRR)
- **Quarterly:** Compliance check — anything changed in regs since lawyer review?

## Disaster recovery

- If Ted's PC dies: re-clone private signals repo on another machine, restore from `.env`
- If TIINGO API fails: engine has 3-source fallback (Tiingo → stooq → yfinance) per memory #19
- If algorithm produces obviously wrong signal: set `TRADING_HALT=true` immediately; investigate; resume manually
- If GitHub Actions fail: site doesn't update that day; tracker shows "stale" banner; subscribers notified by next-day signal
