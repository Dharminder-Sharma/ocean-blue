"""
OCEAN BLUE — STRIPE BILLING INTEGRATION
========================================
Manages subscriptions, payment, referrals via Stripe. NOT ACTIVATED — requires:
  1. Stripe account at stripe.com
  2. STRIPE_SECRET_KEY (and STRIPE_PUBLISHABLE_KEY for frontend)
  3. STRIPE_WEBHOOK_SECRET for webhook validation
  4. Create products + prices in Stripe Dashboard:
     - Product: "Ocean Blue Monthly"
     - Price: $20.00/month USD recurring
  5. Configure Customer Portal (Stripe Dashboard → Billing → Customer Portal)
  6. ATTORNEY REVIEW of all subscription terms, auto-renewal disclosures,
     refund policy, referral structure

KEY RULES:
  - Use Stripe Checkout (hosted) instead of building card forms ourselves.
    This pushes PCI compliance to Stripe — we never touch card data.
  - Use Stripe Customer Portal for self-service cancel/update — saves us building it.
  - Webhook handler MUST verify signatures (Stripe-Signature header).
  - Idempotency keys on all create operations to handle retries.

PRICING STRUCTURE (per Ted's spec):
  - Phase 1-2 (first 6 months from launch): FREE — no charges at all
  - Phase 3+: $20/month, first month free for new subscribers
  - Referral credit: 1 free month per successful referral (unlimited stacking)
  - Cancel anytime

REFERRAL CREDIT IMPLEMENTATION:
  Stripe doesn't natively support "earn a month per referral." Implementation:
  1. Each subscriber gets a unique referral_code in our DB
  2. When a new subscriber signs up with a referral_code, mark in our DB
  3. After the referee's first paid invoice, credit the referrer's account:
     stripe.Customer.modify(referrer.stripe_customer_id, balance=-2000)
     (negative balance = credit; applied at next invoice)
  4. Track in our local DB to enforce "must reach first paid month" rule
"""
from __future__ import annotations

import os
import logging
import hashlib
import secrets
from typing import Optional

log = logging.getLogger(__name__)

STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET")
STRIPE_PRICE_ID = os.environ.get("STRIPE_PRICE_ID")      # $20/mo base subscription
STRIPE_SMS_PRICE_ID = os.environ.get("STRIPE_SMS_PRICE_ID")  # $5/mo optional SMS add-on
SITE_URL = os.environ.get("SITE_URL", "https://oceanblue.example.com")

PRICE_AMOUNT_CENTS = 2000  # $20.00 base
SMS_ADDON_CENTS = 500       # $5.00 SMS add-on
REFERRAL_CREDIT_CENTS = 2000  # $20.00 = 1 month of base subscription


def _stripe():
    """Lazy-load stripe SDK so this module imports cleanly without it installed."""
    try:
        import stripe
        if STRIPE_SECRET_KEY:
            stripe.api_key = STRIPE_SECRET_KEY
        return stripe
    except ImportError:
        log.error("stripe library not installed — pip install stripe")
        return None


def generate_referral_code(seed: str = None) -> str:
    """Generate a 8-character alphanumeric referral code."""
    raw = secrets.token_hex(4).upper()
    return raw  # e.g. "A3F9C2D1"


# ── Subscription lifecycle ────────────────────────────────────────────────

def create_checkout_session(customer_email: str, referral_code: Optional[str] = None,
                             new_referral_code: Optional[str] = None,
                             include_sms_addon: bool = False) -> Optional[str]:
    """Create a Stripe Checkout session for a new subscriber. Returns URL to redirect to.
    
    Architecture: one subscription, optional SMS line item.
      - Base: $20/mo (STRIPE_PRICE_ID)
      - Optional: +$5/mo SMS add-on (STRIPE_SMS_PRICE_ID)
    
    Subscribers can add/remove the SMS line item later via Customer Portal.
    """
    stripe = _stripe()
    if not stripe or not STRIPE_PRICE_ID:
        log.warning("Stripe not configured — returning None")
        return None
    
    trial_days = 30  # First month free
    
    line_items = [{"price": STRIPE_PRICE_ID, "quantity": 1}]
    if include_sms_addon and STRIPE_SMS_PRICE_ID:
        line_items.append({"price": STRIPE_SMS_PRICE_ID, "quantity": 1})
    
    session = stripe.checkout.Session.create(
        mode="subscription",
        customer_email=customer_email,
        line_items=line_items,
        subscription_data={
            "trial_period_days": trial_days,
            "metadata": {
                "referred_by_code": referral_code or "",
                "own_referral_code": new_referral_code or generate_referral_code(),
                "sms_addon": "true" if include_sms_addon else "false",
            },
        },
        success_url=f"{SITE_URL}/subscribe-success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{SITE_URL}/pricing.html",
        # Stripe Tax — enable based on your tax obligations (lawyer to advise)
        # automatic_tax={"enabled": True},
    )
    return session.url


def create_billing_portal_session(stripe_customer_id: str) -> Optional[str]:
    """Send subscriber to Stripe Customer Portal for self-service (cancel, update card, etc.)."""
    stripe = _stripe()
    if not stripe:
        return None
    session = stripe.billing_portal.Session.create(
        customer=stripe_customer_id,
        return_url=SITE_URL,
    )
    return session.url


def apply_referral_credit(referrer_customer_id: str, months: int = 1) -> bool:
    """Apply free-month credit to a referrer's Stripe account."""
    stripe = _stripe()
    if not stripe:
        return False
    
    amount_cents = REFERRAL_CREDIT_CENTS * months
    try:
        # Negative balance adjustment = credit
        stripe.Customer.modify(referrer_customer_id, balance=-amount_cents)
        log.info("Applied $%.2f credit to %s", amount_cents / 100, referrer_customer_id)
        return True
    except Exception as exc:
        log.exception("Failed to apply referral credit: %s", exc)
        return False


# ── Webhook handling ──────────────────────────────────────────────────────

def verify_webhook(payload: bytes, signature: str) -> Optional[dict]:
    """Verify and parse a Stripe webhook event. Returns event dict or None."""
    stripe = _stripe()
    if not stripe or not STRIPE_WEBHOOK_SECRET:
        return None
    try:
        return stripe.Webhook.construct_event(payload, signature, STRIPE_WEBHOOK_SECRET)
    except Exception as exc:
        log.warning("Webhook verification failed: %s", exc)
        return None


def handle_webhook_event(event: dict) -> None:
    """Dispatch on event.type. Wire this up to your webhook endpoint."""
    etype = event["type"]
    obj = event["data"]["object"]
    
    if etype == "checkout.session.completed":
        # New subscriber. Save to local DB, send welcome email.
        # Apply referral credit to referrer if applicable.
        sub = obj
        meta = (sub.get("metadata") or {})
        log.info("New checkout: %s, referred by %s", sub.get("customer_email"), meta.get("referred_by_code"))
        # TODO: persist subscriber record
    
    elif etype == "invoice.paid":
        # Recurring payment succeeded. If this is the FIRST paid invoice
        # for a referred subscriber, credit their referrer.
        inv = obj
        if inv.get("billing_reason") == "subscription_cycle":
            log.info("Recurring payment: %s", inv.get("customer"))
            # TODO: check if first paid invoice; if so apply referral credit
    
    elif etype == "customer.subscription.deleted":
        # Subscriber cancelled. Mark inactive in local DB.
        log.info("Subscription ended: %s", obj.get("customer"))
        # TODO: deactivate subscriber in local DB
    
    elif etype == "invoice.payment_failed":
        # Card failed. Stripe will retry; we should email the subscriber.
        log.warning("Payment failed: %s", obj.get("customer"))
    
    else:
        log.debug("Unhandled webhook event: %s", etype)


# ── Subscriber listing (for notification dispatch) ────────────────────────

def list_active_subscribers():
    """Generator of active subscribers from Stripe.
    
    Used by notifications/email_sender.py and sms_sender.py to determine
    who to notify when a signal fires.
    """
    stripe = _stripe()
    if not stripe:
        return
    
    # Iterate all customers with an active subscription
    for sub in stripe.Subscription.list(status="active", limit=100).auto_paging_iter():
        customer = stripe.Customer.retrieve(sub.customer)
        meta = sub.metadata or {}
        yield {
            "stripe_customer_id":   customer.id,
            "email":                customer.email,
            "name":                 customer.name or customer.email,
            "phone":                customer.phone,
            "referral_code":        meta.get("own_referral_code"),
            "subscription_status":  sub.status,
        }
