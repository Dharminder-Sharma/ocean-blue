"""
OCEAN BLUE — REFERRAL TRACKING
===============================
Track referrer/referee relationships and apply credits when conditions met.

LEGAL NOTE: The referral program structure (free months for referring paying
subscribers) is being reviewed under SEC Investment Advisers Act Rule 206(4)-3
and state equivalents to confirm it does not constitute a regulated "solicitor"
arrangement. See LEGAL_TODO.md.
"""
from __future__ import annotations

import logging
from typing import Optional
from . import stripe_helper

log = logging.getLogger(__name__)


def record_referral(referrer_code: str, referee_email: str) -> bool:
    """Record that referee_email signed up using referrer_code.
    
    Credit is NOT yet applied — credit only fires after the referee's
    first paid invoice (post-trial).
    """
    # TODO: persist to database
    log.info("Referral recorded: %s referred %s", referrer_code, referee_email)
    return True


def fire_referral_credit_if_eligible(referee_stripe_customer_id: str) -> bool:
    """When a referred subscriber pays their first real invoice (post-trial),
    apply 1 month credit to their referrer.
    
    Called from the invoice.paid webhook handler (in stripe_helper.handle_webhook_event).
    """
    # TODO: look up referee in DB
    # TODO: check if this is their first paid invoice
    # TODO: if yes, look up referrer's stripe_customer_id
    # TODO: stripe_helper.apply_referral_credit(referrer_id)
    # TODO: log credit in DB
    log.info("Referral credit eligibility check stub for %s", referee_stripe_customer_id)
    return False


def get_referral_stats(referrer_code: str) -> dict:
    """Return referrer's stats: total referred, paid, credits earned."""
    # TODO: aggregate from DB
    return {
        "total_referred": 0,
        "paying":         0,
        "credits_earned_months": 0,
    }
