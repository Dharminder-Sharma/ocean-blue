"""
OCEAN BLUE — SMS SENDER (Twilio integration)
============================================
Sends signal alerts via SMS. NOT ACTIVATED — requires:
  1. Twilio account at twilio.com (~$1/mo per phone number + $0.0079/SMS)
  2. Phone number purchase
  3. A2P 10DLC business registration (REQUIRED for US commercial SMS):
     • Brand registration: ~$4 one-time
     • Campaign registration: ~$10/mo + $15 vetting fee
     • Lead time: 1-3 weeks for approval
  4. TWILIO_ACCOUNT_SID + TWILIO_AUTH_TOKEN environment variables
  5. ATTORNEY REVIEW of consent language and templates (TCPA compliance)

TCPA REQUIREMENTS:
  • Express written consent BEFORE first send (no implied consent)
  • Disclose: who you are, message frequency, that fees may apply
  • Standard opt-out keywords: STOP, STOPALL, UNSUBSCRIBE, CANCEL, END, QUIT
  • Standard help keywords: HELP, INFO
  • Honor opt-out within ~5 minutes (immediate for STOP)
  • TCPA violations: $500-$1,500 PER MESSAGE in statutory damages

Usage (once activated):
    from notifications.sms_sender import send_alert_sms
    send_alert_sms(
        to_number="+15551234567",
        signal={"date": "2026-05-17", "action": "QQQ"},
        from_position="CASH",
    )
"""
from __future__ import annotations

import os
import re
import logging
from pathlib import Path
from string import Template

log = logging.getLogger(__name__)

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = os.environ.get("TWILIO_FROM_NUMBER")
TEMPLATES_DIR = Path(__file__).parent / "templates"

OPT_OUT_KEYWORDS = {"STOP", "STOPALL", "UNSUBSCRIBE", "CANCEL", "END", "QUIT"}
HELP_KEYWORDS = {"HELP", "INFO"}


def _enabled() -> bool:
    """Check whether SMS is configured for sending."""
    if not (TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_FROM_NUMBER):
        log.warning("Twilio credentials not set — SMS send skipped")
        return False
    return True


def _normalize_phone(phone: str) -> str:
    """Normalize to E.164 format."""
    cleaned = re.sub(r"\D", "", phone)
    if not cleaned.startswith("1") and len(cleaned) == 10:
        cleaned = "1" + cleaned
    return "+" + cleaned


def send_alert_sms(to_number: str, signal: dict, from_position: str) -> bool:
    """Send a signal alert SMS. Must include opt-out reminder."""
    if not _enabled():
        return False
    
    template_path = TEMPLATES_DIR / "sms_alert.txt"
    if template_path.exists():
        body = Template(template_path.read_text()).safe_substitute(
            from_position=from_position,
            to_position=signal["action"],
            signal_date=signal["date"],
            qqq_close=f"${signal['qqq_close']:.2f}",
            tlt_close=f"${signal['tlt_close']:.2f}",
        )
    else:
        body = (
            f"Ocean Blue: {from_position}→{signal['action']} as of {signal['date']}. "
            f"QQQ {signal['qqq_close']:.2f}, TLT {signal['tlt_close']:.2f}. "
            f"Execute at next open. Reply STOP to opt out."
        )
    
    # SMS must stay under 160 chars per message (or it's sent as multi-part).
    # Total message must include STOP language for TCPA compliance.
    if "STOP" not in body.upper():
        body = body[:150] + " Reply STOP to end."
    
    try:
        from twilio.rest import Client
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        msg = client.messages.create(
            body=body,
            from_=TWILIO_FROM_NUMBER,
            to=_normalize_phone(to_number),
        )
        log.info("SMS sent to %s, sid=%s", to_number, msg.sid)
        return True
    except ImportError:
        log.error("twilio library not installed — pip install twilio")
        return False
    except Exception as exc:
        log.exception("SMS send failed: %s", exc)
        return False


def handle_inbound_sms(from_number: str, body: str) -> str:
    """Process inbound SMS (STOP, HELP, etc.) — wire this up to a webhook."""
    cmd = body.strip().upper()
    
    if cmd in OPT_OUT_KEYWORDS:
        # TODO: mark subscriber phone as opted-out in DB
        log.info("Opt-out from %s", from_number)
        return "You've been unsubscribed from Ocean Blue SMS alerts. Reply START to re-enable."
    
    if cmd in HELP_KEYWORDS:
        return ("Ocean Blue: algorithmic QQQ rotation signals. Approx 2-3 msgs/month. "
                "Msg & data rates may apply. Reply STOP to end. Help: oceanblue.example.com")
    
    if cmd == "START":
        # TODO: verify they previously opted in; re-enable
        return "You're re-enabled for Ocean Blue alerts. Reply STOP to end."
    
    return ""  # ignore unknown commands


def send_to_subscribers(body: str, signal: dict | None = None) -> int:
    """Iterate active SMS-opted-in subscribers and send."""
    # TODO Phase 3: pull from subscriber DB with sms_opted_in=True
    log.info("SMS dispatch stub — would broadcast: %s", body)
    return 0
