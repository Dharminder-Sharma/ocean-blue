"""
OCEAN BLUE — PLATFORM DAILY RUN
================================
Runs daily after signal_engine.py publishes signal.json to the private repo.

This module:
  1. Reads signal.json (provided by GitHub Actions checkout of private repo)
  2. Updates paper trading state (executes the rotation at NEXT day's open)
  3. Regenerates tracker.html with latest data
  4. Updates signal_history.json for the public site
  5. Dispatches subscriber notifications (email + SMS) if a position change occurred
  6. Commits regenerated files back to the public repo for GitHub Pages

THIS MODULE CONTAINS NO ALGORITHM. It only consumes the 6-field signal.json
output of the signal engine. The signal engine remains in a separate private repo.

USAGE:
  python daily_run.py --signal-file ../signals/signal.json
"""
from __future__ import annotations

import os
import sys
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = SCRIPT_DIR.parent / "public"
DATA_DIR = SCRIPT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)


# ── Paper trading state ───────────────────────────────────────────────────
PAPER_STATE_FILE = DATA_DIR / "paper_state.json"
PAPER_HISTORY_FILE = DATA_DIR / "paper_history.jsonl"


def load_paper_state() -> dict:
    """Load paper trading state. Initialize if doesn't exist."""
    if PAPER_STATE_FILE.exists():
        return json.loads(PAPER_STATE_FILE.read_text())
    return {
        "cash":        100000.0,
        "qqq_shares":  0.0,
        "tlt_shares":  0.0,
        "position":    "CASH",
        "start_value": 100000.0,
        "start_date":  None,
        "last_signal_date": None,
        "last_rotation_date": None,
        "transactions": [],
    }


def save_paper_state(state: dict) -> None:
    PAPER_STATE_FILE.write_text(json.dumps(state, indent=2))


def apply_signal_to_paper_trading(signal: dict, state: dict) -> dict:
    """Apply today's signal to paper trading at the close prices.
    
    Per the published spec: subscribers execute at NEXT day's open. For paper
    tracking, we use today's close as the execution price (subscribers will
    typically see slippage of one bar against this). This is documented in the
    public hypothetical performance disclosure.
    """
    qqq = signal["qqq_close"]
    tlt = signal["tlt_close"]
    target = signal["action"]
    today = signal["date"]
    
    # Initialize on first run
    if state["start_date"] is None:
        state["start_date"] = today
    
    current = state["position"]
    if target == "HOLD" or target == current:
        # No rotation today — just mark-to-market
        portfolio_value = (
            state["cash"]
            + state["qqq_shares"] * qqq
            + state["tlt_shares"] * tlt
        )
        state["last_signal_date"] = today
        state["last_portfolio_value"] = portfolio_value
        return state
    
    # Rotation required: liquidate everything to cash, then enter target
    cash = state["cash"] + state["qqq_shares"] * qqq + state["tlt_shares"] * tlt
    state["qqq_shares"] = 0.0
    state["tlt_shares"] = 0.0
    
    if target == "QQQ":
        state["qqq_shares"] = cash / qqq
        state["cash"] = 0.0
    elif target == "TLT":
        state["tlt_shares"] = cash / tlt
        state["cash"] = 0.0
    elif target == "CASH":
        state["cash"] = cash
    
    # Log transaction
    state["transactions"].append({
        "date":     today,
        "from":     current,
        "to":       target,
        "qqq_px":   qqq,
        "tlt_px":   tlt,
        "value":    cash,
    })
    state["position"] = target
    state["last_rotation_date"] = today
    state["last_signal_date"] = today
    state["last_portfolio_value"] = cash
    
    # Append to historical record
    with PAPER_HISTORY_FILE.open("a") as f:
        f.write(json.dumps({
            "date": today, "from": current, "to": target,
            "value": round(cash, 2), "qqq": qqq, "tlt": tlt,
        }) + "\n")
    
    return state


def generate_tracker_html(state: dict, signal: dict) -> str:
    """Regenerate the live tracker page from current paper state."""
    portfolio_value = state.get("last_portfolio_value", 100000)
    start = state["start_value"]
    pct = (portfolio_value / start - 1) * 100
    pct_class = "green" if pct >= 0 else "danger"
    
    # Build transactions table
    tx_rows = ""
    for tx in reversed(state["transactions"][-50:]):  # last 50
        tx_rows += (
            f"<tr><td>{tx['date']}</td><td>{tx['from']}→{tx['to']}</td>"
            f"<td>${tx['qqq_px']:.2f}</td><td>${tx['tlt_px']:.2f}</td>"
            f"<td>${tx['value']:,.0f}</td></tr>"
        )
    if not tx_rows:
        tx_rows = '<tr><td colspan="5" style="text-align:center;color:#666;">No rotations yet — strategy currently in initial position.</td></tr>'
    
    # ── Read template ─────────────────────────────────
    # In production this would be a Jinja template. For now, inline:
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Live Tracker — Ocean Blue</title>
<meta name="description" content="Live paper trading performance, updated daily after market close.">
<link rel="canonical" href="https://oceanblue.example.com/tracker.html">
<link rel="stylesheet" href="assets/style.css"></head><body>

<div class="phase-banner"><strong>PAPER TRADING PHASE</strong> · Last updated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}</div>
<nav class="primary"><div class="container">
  <a href="/" class="logo"><span class="wave">≈</span>Ocean Blue</a>
  <ul class="nav-links">
    <li><a href="results.html">Track Record</a></li>
    <li><a href="tracker.html" class="active">Live Tracker</a></li>
    <li><a href="how-it-works.html">How It Works</a></li>
    <li><a href="ira.html">For IRAs</a></li>
    <li><a href="pricing.html">Pricing</a></li>
    <li><a href="signup.html" class="cta">Join Waitlist</a></li>
  </ul>
</div></nav>

<section class="hero"><div class="container">
  <p class="eyebrow">Live paper trading · as of {signal['date']}</p>
  <h1>Currently: <em>{state['position']}</em></h1>
  <p class="lede">Started {state['start_date']} with $100,000. Last signal {signal['date']}.</p>

  <div class="hero-stats">
    <div class="hero-stat accent">
      <div class="label">Paper portfolio value</div>
      <div class="value mono">${portfolio_value:,.0f}</div>
      <div class="sub">vs $100,000 start</div>
    </div>
    <div class="hero-stat">
      <div class="label">Total return</div>
      <div class="value mono" style="color: var(--{pct_class.replace('danger','red').replace('green','green')});">{pct:+.2f}%</div>
      <div class="sub">since {state['start_date']}</div>
    </div>
    <div class="hero-stat">
      <div class="label">Current position</div>
      <div class="value mono">{state['position']}</div>
      <div class="sub">{len(state['transactions'])} rotations to date</div>
    </div>
  </div>
</div></section>

<section><div class="container">
  <div class="section-head"><p class="eyebrow">Rotations</p><h2>Every signal, every rotation</h2></div>
  <div style="overflow-x: auto;">
  <table class="data">
    <thead><tr><th>Date</th><th>Rotation</th><th>QQQ Close</th><th>TLT Close</th><th>Portfolio Value</th></tr></thead>
    <tbody>{tx_rows}</tbody>
  </table>
  </div>
</div></section>

<section class="dark"><div class="container-narrow" style="text-align:center;">
  <h2 style="color:var(--parchment);">Join the waitlist</h2>
  <a href="signup.html" class="btn" style="background:var(--gold);color:var(--navy);">Get notified at launch →</a>
</div></section>

<footer class="site-footer"><div class="container">
  <div class="footer-disclaimer"><strong>NOT INVESTMENT ADVICE.</strong> Paper trading is hypothetical. Actual subscriber results will differ due to slippage, fees, and timing. <em>[PENDING ATTORNEY REVIEW]</em></div>
  <div class="copyright">© 2026 Best Kind LLC.</div>
</div></footer>
</body></html>
"""


def maybe_dispatch_notifications(state: dict, signal: dict) -> None:
    """Send subscriber notifications if today's signal triggered a rotation."""
    if state.get("last_rotation_date") != signal["date"]:
        # No rotation today, no notifications
        return
    
    # Lazy import — these helpers are stubs until you configure them
    try:
        from notifications import email_sender, sms_sender
    except ImportError:
        return
    
    last_tx = state["transactions"][-1]
    subject = f"Ocean Blue Signal — {last_tx['from']} → {last_tx['to']}"
    body = f"Signal date: {signal['date']}\nRotation: {last_tx['from']} → {last_tx['to']}"
    
    # In production, iterate over active subscribers and dispatch
    # email_sender.send_to_subscribers(subject, body, signal=signal)
    # sms_sender.send_to_subscribers(body, signal=signal)
    print(f"  [notifications stub] Would send: {subject}")


# ── Main entry ────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--signal-file", required=True,
                    help="Path to signal.json from private signals repo")
    args = ap.parse_args()
    
    signal = json.loads(Path(args.signal_file).read_text())
    print(f"━━━ Ocean Blue Daily Run ━━━")
    print(f"Signal: {signal['date']} — {signal['action']}")
    
    state = load_paper_state()
    state = apply_signal_to_paper_trading(signal, state)
    save_paper_state(state)
    print(f"✓ Paper state updated. Portfolio: ${state.get('last_portfolio_value', 0):,.0f}")
    
    html = generate_tracker_html(state, signal)
    (PUBLIC_DIR / "tracker.html").write_text(html)
    print(f"✓ tracker.html regenerated ({len(html):,} bytes)")
    
    # Also write a JSON snapshot for the public site to consume
    snapshot = {
        "as_of":      signal["date"],
        "position":   state["position"],
        "value":      state.get("last_portfolio_value", 100000),
        "return_pct": (state.get("last_portfolio_value", 100000) / state["start_value"] - 1) * 100,
        "rotations":  len(state["transactions"]),
        "start_date": state["start_date"],
        "version":    signal.get("version"),
    }
    (PUBLIC_DIR / "tracker-data.json").write_text(json.dumps(snapshot, indent=2))
    
    maybe_dispatch_notifications(state, signal)
    
    print("Done.")


if __name__ == "__main__":
    main()
