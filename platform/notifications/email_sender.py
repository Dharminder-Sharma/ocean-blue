"""
OCEAN BLUE — EMAIL SENDER (SendGrid integration)
================================================
Sends transactional emails to subscribers. NOT ACTIVATED — requires:
  1. SendGrid account at sendgrid.com (free tier: 100 emails/day; $19.95/mo for paid)
  2. SENDGRID_API_KEY environment variable
  3. Domain authentication (DKIM/SPF/DMARC) — REQUIRED for deliverability
  4. Verified sender identity
  5. ATTORNEY REVIEW of all email templates (CAN-SPAM compliance)

CAN-SPAM REQUIREMENTS (must be in every commercial email):
  • Accurate "From" name and address
  • No deceptive subject line
  • Email marked as advertisement (if commercial)
  • Physical postal address of sender
  • Clear unsubscribe mechanism (one-click)
  • Honor unsubscribe within 10 business days

Usage (once activated):
    from notifications.email_sender import send_alert_email
    send_alert_email(
        to_email="subscriber@example.com",
        to_name="John Subscriber",
        signal={"date": "2026-05-17", "action": "QQQ"},
        from_position="CASH",
    )
"""
from __future__ import annotations

import os
import logging
from pathlib import Path
from string import Template

log = logging.getLogger(__name__)

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
SEND_FROM_EMAIL = os.environ.get("SEND_FROM_EMAIL", "signals@oceanblue.example.com")
SEND_FROM_NAME = os.environ.get("SEND_FROM_NAME", "Ocean Blue")
TEMPLATES_DIR = Path(__file__).parent / "templates"


def _enabled() -> bool:
    """Check whether email is configured for sending."""
    if not SENDGRID_API_KEY:
        log.warning("SENDGRID_API_KEY not set — email send skipped")
        return False
    return True


def _render(template_name: str, **kwargs) -> str:
    """Render an email template with simple string substitution."""
    tpl = (TEMPLATES_DIR / template_name).read_text()
    return Template(tpl).safe_substitute(**kwargs)


def send_alert_email(to_email: str, to_name: str, signal: dict, from_position: str,
                     unsubscribe_url: str = "#") -> bool:
    """Send a signal alert email to a subscriber."""
    if not _enabled():
        return False
    
    body_html = _render(
        "email_alert.html",
        to_name=to_name,
        signal_date=signal["date"],
        from_position=from_position,
        to_position=signal["action"],
        qqq_close=f"${signal['qqq_close']:.2f}",
        tlt_close=f"${signal['tlt_close']:.2f}",
        unsubscribe_url=unsubscribe_url,
    )
    subject = f"Ocean Blue Signal — {from_position} → {signal['action']}"
    
    try:
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail, From, To
        
        msg = Mail(
            from_email=From(SEND_FROM_EMAIL, SEND_FROM_NAME),
            to_emails=To(to_email),
            subject=subject,
            html_content=body_html,
        )
        client = SendGridAPIClient(SENDGRID_API_KEY)
        resp = client.send(msg)
        log.info("Email sent to %s, status=%s", to_email, resp.status_code)
        return 200 <= resp.status_code < 300
    except ImportError:
        log.error("sendgrid library not installed — pip install sendgrid")
        return False
    except Exception as exc:
        log.exception("Email send failed: %s", exc)
        return False


def send_welcome_email(to_email: str, to_name: str, referral_code: str) -> bool:
    """Send welcome email to a new subscriber."""
    if not _enabled():
        return False
    
    body_html = _render(
        "email_welcome.html",
        to_name=to_name,
        referral_code=referral_code,
        referral_url=f"https://oceanblue.example.com/?ref={referral_code}",
    )
    # ... same dispatch pattern as above ...
    log.info("(welcome email stub) %s", to_email)
    return True


def send_to_subscribers(subject: str, body: str, signal: dict | None = None) -> int:
    """Iterate over active subscribers and send the alert to each one.
    
    Pulls subscriber list from the Stripe Customer database (in Phase 3) or
    a local CSV (during Phase 2 waitlist).
    """
    # TODO Phase 3: pull from Stripe active subscribers
    # for sub in stripe_helper.list_active_subscribers():
    #     send_alert_email(sub.email, sub.name, signal, ...)
    log.info("send_to_subscribers stub — would dispatch: %s", subject)
    return 0
