"""
OCEAN BLUE — SIGNUP HANDLER
============================
Phase 1: Capture waitlist signups (no payment, no auth, just email).
Phase 2: Add email verification.
Phase 3: Convert to full subscription signup with Stripe Checkout.

During Phase 1, this is invoked by a Formspree webhook OR by direct POST
to a simple Flask/FastAPI endpoint. The simplest path is to use Formspree
(no backend) and only build this handler when moving to Phase 2.
"""
from __future__ import annotations

import csv
import logging
from datetime import datetime, timezone
from pathlib import Path

log = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)
WAITLIST_CSV = DATA_DIR / "waitlist.csv"


def handle_waitlist_signup(name: str, email: str, account_type: str = "",
                            referral_code: str = "", ip: str = "") -> bool:
    """Append a new waitlist entry to the CSV. Returns True on success."""
    if not email or "@" not in email:
        return False
    
    is_new = not WAITLIST_CSV.exists()
    with WAITLIST_CSV.open("a", newline="") as f:
        w = csv.writer(f)
        if is_new:
            w.writerow(["timestamp", "name", "email", "account_type", "referral_code", "ip"])
        w.writerow([
            datetime.now(timezone.utc).isoformat(),
            name, email, account_type, referral_code, ip,
        ])
    log.info("Waitlist signup: %s", email)
    return True
