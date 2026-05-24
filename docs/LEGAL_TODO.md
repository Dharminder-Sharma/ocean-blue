# Ocean Blue — Legal Review Checklist

**Prepared for:** NY fintech attorney (referral pending via William Furlow)
**Subject:** Pre-launch regulatory review for Ocean Blue subscription service
**Operator:** Best Kind LLC (Brooklyn, NY)
**Estimated cost:** $500–$1,500 per memory #22

This document is the consolidated brief of every legal/regulatory question
that must be answered before Ocean Blue begins accepting paid subscribers.
The 6-month paper trading phase provides time to complete this review.

---

## 1. Investment Adviser Registration

**The question:** Does selling a $20/month QQQ rotation signal service
require Best Kind LLC to register as an Investment Adviser?

**The general rule:** Under the Investment Advisers Act of 1940, anyone who
"for compensation, engages in the business of advising others...as to the
value of securities or as to the advisability of investing in, purchasing,
or selling securities" is an Investment Adviser. Federal registration required
if AUM ≥ $100M; state registration otherwise (NY specifically).

**The publisher exemption (Lowe v. SEC, 472 U.S. 181, 1985):** A publication
that is (a) impersonal — same content to all subscribers, (b) bona fide
(not promotional), and (c) of regular and general circulation may be exempt
as "publishing" rather than "advising."

**Ocean Blue argues for the exemption:**
- ✅ Identical signal sent to every subscriber — no personalization
- ✅ Regular publication (daily after market close)
- ✅ Bona fide market analysis based on a documented algorithm
- ⚠️ Open question: does a paid SMS/email push qualify as "regular and general circulation"?

**Counsel decisions needed:**
1. Does the Lowe publisher exemption apply to Ocean Blue?
2. If yes, what disclosures must accompany the exemption?
3. If no, must Best Kind LLC register with NY (or SEC if AUM threshold ever crossed)?
4. Are there state-by-state variations to address (especially CA, TX, FL)?
5. Is the structure stronger if reorganized as a content publication (e.g., "Ocean Blue Daily" newsletter)?

---

## 2. SEC Marketing Rule (Rule 206(4)-1) — Hypothetical Performance

**The question:** What disclosures are required when showing backtest results to prospects?

**The rule (revised 2020, effective Nov 2022):** Hypothetical performance
in adviser advertising requires:
- Policies/procedures designed to ensure relevance to intended audience
- Sufficient information to understand criteria/assumptions used
- Sufficient information to understand risks/limitations
- Cannot be presented to retail audiences UNLESS the firm has policies in place

**Ocean Blue's showings:**
- 22-year hypothetical backtest results displayed on home page
- Year-by-year side-by-side vs B&H on `results.html`
- "Hypothetical" labels and warnings already present

**Counsel decisions needed:**
1. Even if publisher exemption applies (#1), does Rule 206(4)-1 still bind us?
2. Approve final hypothetical performance disclosure language to replace `[PENDING ATTORNEY REVIEW]` placeholders in:
   - `public/index.html`
   - `public/results.html`
   - `public/disclaimer.html`
   - `public/pricing.html`
3. Must we restrict backtest viewing to authenticated/verified audiences?
4. Are the trading-cost and slippage assumptions sufficiently disclosed?
5. Confirm we may not present hypothetical alongside live results without clear separation

---

## 3. TCPA / SMS Marketing Rules

**The question:** What's required before sending a single marketing SMS?

**Federal TCPA rules:**
- Express written consent required (no implied consent for marketing)
- Statutory damages: $500–$1,500 PER MESSAGE for violations
- Must honor opt-out (STOP) immediately

**A2P 10DLC carrier requirements (mandatory since 2023):**
- Brand registration with The Campaign Registry (~$4 one-time)
- Campaign registration (~$10/mo + ~$15 vetting fee)
- Lead time: 1–3 weeks for approval
- Without registration: carriers may block or heavily filter messages

**Counsel decisions needed:**
1. Approve consent capture language for the signup form (currently in `signup.html`)
2. Approve the SMS template at `platform/notifications/templates/sms_alert.txt`
3. Confirm message frequency disclosure ("approximately 2–3 messages per month") is adequate
4. Confirm opt-out keyword handling in `sms_sender.py` is compliant
5. State-specific add-ons: FL, WA, OK have their own TCPA-mini statutes with broader liability
6. Document retention requirements for proof of consent

---

## 4. CAN-SPAM (Email Marketing Rules)

**The question:** What email compliance is required?

**Federal CAN-SPAM requirements:**
- Accurate "From" / "Reply-To" / routing headers
- Truthful, non-deceptive subject line
- Identify commercial nature (if applicable)
- Physical postal address required in every commercial email
- Clear unsubscribe mechanism with one-click access
- Honor unsubscribe within 10 business days

**Counsel decisions needed:**
1. Approve email templates at `platform/notifications/templates/email_*.html`
2. Confirm transactional vs. commercial classification:
   - Signal alerts → arguably transactional (subscriber requested them)
   - Welcome email → arguably transactional
   - Marketing emails (e.g., "subscriptions open!") → commercial, requires full compliance
3. Confirm physical address `1929 East 17th Street, Brooklyn, NY 11229` is the address to use
4. Approve unsubscribe flow

---

## 5. Referral Program — Solicitor Rules

**The question:** Does paying existing subscribers (in free months) to refer
new subscribers constitute a regulated "solicitor" arrangement?

**The rule:** Under the Investment Advisers Act Rule 206(4)-3 (recently
modernized within Rule 206(4)-1), compensating someone for soliciting
investment advisory clients triggers disclosure, written-agreement, and
disqualification requirements.

**Ocean Blue's structure:**
- Existing subscriber gets 1 free month per referee who pays for ≥ 1 month
- No cash payments — credit only
- Unlimited stacking

**Counsel decisions needed:**
1. Does this constitute "compensation for solicitation"? (Almost certainly yes if we're an adviser; ambiguous if publisher exemption applies)
2. If yes, what disclosures must appear at the point of referral and upon referee signup?
3. Does the referee need to receive a copy of the solicitor agreement?
4. Are there structural changes that simplify compliance (e.g., one-time signup credit only, no recurring credit)?
5. Is unlimited stacking acceptable, or must there be a cap?

---

## 6. State Money Transmitter / Payment Laws

**The question:** Does accepting subscription payments through Stripe trigger any state licensing?

**General answer:** Stripe handles most regulatory burden as a money services
business. Best Kind LLC should not be a money transmitter as we never hold
customer funds — Stripe charges, takes fee, deposits net amount in our account.

**Counsel decisions needed:**
1. Confirm we are NOT a money transmitter under NY Banking Law or other state laws
2. Confirm sales tax obligations (digital subscription service in NY — is it taxable?)
3. Confirm we're under economic nexus thresholds in other states
4. Recommendation on automatic-renewal disclosure laws (CA AB-390, NY GBL §527-a, OR, FL, etc.)

---

## 7. Privacy / Data Protection

**The question:** What privacy compliance is required for the personal data we collect?

**Data we'll handle:**
- Name, email, phone (subscriber)
- Payment info (handled by Stripe — we never see it)
- Marketing preferences
- Web analytics

**Applicable laws:**
- **CCPA / CPRA (California):** $7,500/violation; applies if any CA resident is a customer
- **CPA (Colorado):** similar to CCPA
- **VCDPA (Virginia):** similar
- **CTDPA (Connecticut), UCPA (Utah), TDPSA (Texas):** also active
- **NY SHIELD Act:** breach notification + data security
- **NY DOL Telemarketing rules:** if SMS counts (probably does for opt-in customers)

**Counsel decisions needed:**
1. Approve final Privacy Policy at `public/privacy.html` (replace `[PENDING ATTORNEY REVIEW]`)
2. CCPA-specific disclosures: right to know, right to delete, right to opt-out of sale
3. "Do Not Sell" link required? (We don't sell, but must we declare it?)
4. Cookie banner — required for EU visitors only? Or broader best practice?
5. Data retention periods — confirm 7-year subscription record retention is appropriate
6. Breach notification procedure required by NY SHIELD Act — document one

---

## 8. IRA-Specific Marketing

**The question:** Does marketing the service as "ideal for IRAs" trigger any fiduciary-adjacent rules?

**Background:** The DOL had a "Fiduciary Rule" that was vacated, then rewritten,
then partially reinstated. Plus IRA-specific rules in the Internal Revenue Code.

**Ocean Blue's positioning:**
- `public/ira.html` discusses tax advantages of IRAs for the strategy
- Lists qualifying account types and compatible custodians
- Includes tax-drag math

**Counsel decisions needed:**
1. Does the IRA-positioning page require additional disclosures?
2. Confirm we are NOT providing rollover advice (which has its own DOL rules)
3. Are tax statements (CAGR comparison, tax drag analysis) advisory in nature or general education?
4. Should we add an explicit "consult your tax adviser" disclaimer beyond what's on the page?
5. Restrictions on naming specific custodians (Fidelity, Schwab, etc.) — risk of implied endorsement or partnership claims?

---

## 9. Disclaimers / Risk Disclosures

**The question:** Are all required disclosures present and adequate?

**Pages with `[PENDING ATTORNEY REVIEW]` markers requiring final language:**

| Page | What needs review |
|---|---|
| `disclaimer.html` | All 12 sections — full attorney draft |
| `terms.html` | All 10 sections — full attorney draft |
| `privacy.html` | All sections — full attorney draft |
| `index.html` | Footer disclaimer + hero/results disclaimers |
| `results.html` | Hypothetical performance disclosure block |
| `pricing.html` | Auto-renewal terms, referral structure language |
| `signup.html` | Consent language for waitlist |
| `ira.html` | Tax disclaimer (currently "consult your tax adviser") |
| `faq.html` | "Not investment advice" language throughout |
| Email templates | All `[PENDING ATTORNEY-DRAFTED LANGUAGE]` markers |
| SMS template | Approve final consent + STOP language |

---

## 10. Entity / Corporate Structure

**Counsel decisions needed:**
1. Operate Ocean Blue as a DBA of Best Kind LLC, or spin out a new LLC?
2. Insurance recommendation: E&O insurance for technology errors? Cyber liability?
3. Trademark filing for "Ocean Blue" service mark (per memory: Best Kind has service marks for finallyRelief!℠ and SensationFree℠)
4. Operating agreement amendments if Best Kind's daughter (90% patent portfolio owner per memory) has any interest in this revenue line

---

## 11. Subscriber Agreement Specifics

**Beyond the boilerplate, please cover:**
1. Limitation of liability — cap at fees paid in last 12 months? Or hard dollar cap?
2. Arbitration clause — JAMS or AAA? Bellwether limitations?
3. Class-action waiver — enforceable in NY (yes, post-Concepcion)?
4. Mutual indemnification or one-way?
5. Termination rights (Ocean Blue's right to terminate without cause)
6. Force majeure (especially relevant — what if Tiingo goes down? What if Ted's PC dies?)

---

## 12. Final Deliverables Expected from Counsel

By the end of the engagement, we should have:

- [ ] **Determination memo** on RIA registration question (publisher exemption applies, yes/no/conditions)
- [ ] **Final disclosures page** (`disclaimer.html`) — attorney-drafted text
- [ ] **Final Terms of Service** (`terms.html`) — attorney-drafted text
- [ ] **Final Privacy Policy** (`privacy.html`) — attorney-drafted text, multi-state compliant
- [ ] **Standard subscriber agreement** (linked from checkout, ideally separate from ToS)
- [ ] **SMS consent language** approved
- [ ] **Email templates** approved
- [ ] **Referral program structure** approved (or modifications recommended)
- [ ] **Marketing copy review** — `index.html`, `results.html`, `ira.html`, `pricing.html` hypothetical performance language all blessed
- [ ] **Setup recommendations:** A2P 10DLC registration timing, business filings, insurance
- [ ] **Ongoing compliance memo** — what to do annually/quarterly to stay compliant
- [ ] **Solicitor disclosure** template (if referral program needs one)

---

## Anti-checklist: things we are NOT asking counsel to do

- Review the algorithm itself (this is engineering, not legal)
- Vet the brokerage choice (subscriber's responsibility)
- Tax planning advice (subscriber's responsibility)
- General business strategy

---

## Contact / questions to expect

- Best Kind LLC entity records, EIN, operating agreement
- Memo on the brokerage architecture (Tiingo data, no custody of subscriber funds)
- Engineering documentation on signal generation cadence (5:30 PM ET daily)
- Sample paper trading output (we have 22-year backfill at `paper_trading.xlsx`)
- Initial subscriber projections (conservative): 0 paid in first 6 months, 50 by month 9, 200 by year 1

---

## Estimated total time: 8–15 hours of counsel time

At $200–$500/hr, range $1,600–$7,500. Memory #22 estimates $500–$1,500.
Memory $500 estimate likely assumes shopping for a junior attorney or
fixed-fee engagement on a defined scope. Recommend a fixed-fee engagement
covering items 1–9 above, with hourly billing for follow-ups and 10–12.
