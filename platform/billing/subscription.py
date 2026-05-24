"""
OCEAN BLUE — SUBSCRIPTION LIFECYCLE
====================================
Higher-level helpers built on top of stripe_helper.py. Manages the
local subscriber DB and orchestrates onboarding/cancellation flows.

THIS IS A STUB. Wire to your database when Phase 3 begins.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from . import stripe_helper

log = logging.getLogger(__name__)


@dataclass
class Subscriber:
    email: str
    name: str
    phone: Optional[str] = None
    sms_opted_in: bool = False
    stripe_customer_id: Optional[str] = None
    stripe_subscription_id: Optional[str] = None
    referral_code: str = ""
    referred_by_code: Optional[str] = None
    status: str = "waitlist"  # waitlist | trial | active | cancelled | past_due
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    referral_credits_earned_months: int = 0
    first_paid_invoice_at: Optional[str] = None


def onboard_new_subscriber(email: str, name: str, phone: str | None,
                            referred_by: str | None = None) -> Subscriber:
    """Onboard a new subscriber. Returns the subscriber record."""
    code = stripe_helper.generate_referral_code()
    sub = Subscriber(
        email=email,
        name=name,
        phone=phone,
        referral_code=code,
        referred_by_code=referred_by,
    )
    # TODO: persist to database
    # TODO: kick off Stripe Checkout via stripe_helper.create_checkout_session
    log.info("Subscriber onboarded: %s (ref code: %s)", email, code)
    return sub


def cancel_subscription(stripe_customer_id: str, reason: str | None = None) -> bool:
    """Mark a subscription as cancelled. Stripe handles the actual cancellation."""
    # In practice, subscribers cancel through Stripe Customer Portal
    # This function is for admin-initiated cancellations
    log.info("Cancellation requested for %s, reason: %s", stripe_customer_id, reason)
    # TODO: stripe.Subscription.modify(sub_id, cancel_at_period_end=True)
    return True
