"""
OCEAN BLUE — SIGNAL ENGINE
==========================
PRIVATE REPOSITORY — DO NOT SHARE WITH CONTRACTORS OR PUBLISH.

This module wraps the proprietary v3.5.1 algorithm and outputs a compact
signal.json file that the public platform consumes. The signal.json
reveals nothing about the algorithm's internals.

DAILY RUN ORDER (5:30 PM ET on every market day):
  1. qqq_v35_production.py runs (the actual algorithm, kept here in private repo)
  2. This script reads the output and produces signal.json
  3. git push to private signals repository
  4. GitHub Actions in PUBLIC repo polls private repo, regenerates tracker

CRITICAL: Never commit:
  - This file to a public repository
  - qqq_v35_production.py or any algorithm code
  - state.json (reveals algorithm internals via position changes)
  - TIINGO_API_KEY or other secrets

signal.json schema (6 fields, no algorithm details):
{
  "date":       "2026-05-17",          # signal date
  "action":     "QQQ",                 # one of: QQQ, TLT, CASH, HOLD
  "qqq_close":  483.21,                # today's QQQ close (for tracker math)
  "tlt_close":  88.15,                 # today's TLT close (for tracker math)
  "signed_at":  "2026-05-17T17:30:00", # signing timestamp
  "version":    "v3.5.1"               # engine version for tracking
}

USAGE:
  python signal_engine.py
"""
from __future__ import annotations

import os
import sys
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
ENGINE_SCRIPT = SCRIPT_DIR / "qqq_v35_production.py"  # the algorithm (private)
ENGINE_DATA_DIR = Path(os.environ.get("ENGINE_DATA_DIR", SCRIPT_DIR / "qqq_v35_data"))
SIGNALS_REPO = Path(os.environ.get("SIGNALS_REPO_PATH", SCRIPT_DIR.parent / "ocean-blue-signals"))
ENGINE_VERSION = "v3.5.1"

# Hard kill switch (per memory #20 / #19)
TRADING_HALT = os.environ.get("TRADING_HALT", "false").lower() == "true"


def run_engine() -> dict:
    """Execute the algorithm script and read its state output.
    
    The algorithm writes its computed state to state.json. We read that
    file rather than reimplementing the logic here.
    """
    if TRADING_HALT:
        print("⚠ TRADING_HALT=true — engine paused, will not run.", file=sys.stderr)
        sys.exit(0)
    
    # Run the algorithm (which writes its own state file)
    result = subprocess.run(
        [sys.executable, str(ENGINE_SCRIPT)],
        capture_output=True,
        text=True,
        check=False,
        cwd=str(SCRIPT_DIR),
    )
    if result.returncode != 0:
        print(f"❌ Engine failed (rc={result.returncode}):", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(2)
    
    state_file = ENGINE_DATA_DIR / "state.json"
    if not state_file.exists():
        print(f"❌ State file not found at {state_file}", file=sys.stderr)
        sys.exit(3)
    
    return json.loads(state_file.read_text())


def extract_signal(state: dict) -> dict:
    """Reduce the verbose internal state to a 6-field public signal.
    
    This is the IP firewall — nothing about the algorithm leaves this function
    except the high-level position and the prices used to compute it.
    """
    # Map internal position to public action
    position = state.get("current_position", "CASH")
    last_signal_date = state.get("last_signal_date") or state.get("as_of_date")
    last_signal_action = state.get("last_signal_action", "HOLD")
    qqq_close = state.get("last_qqq_close")
    tlt_close = state.get("last_tlt_close")
    
    # Action codes: QQQ=hold/move-to QQQ, TLT=hold/move-to TLT, CASH=move to cash, HOLD=no change today
    # Map from actual algorithm action constants (qqq_v35_production.py).
    # Note: SELL_TLT_HOLD_CASH is new in v3.5.1 (TLT-while-held exit rule).
    if last_signal_action in ("BUY_QQQ_FROM_CASH", "BUY_QQQ_FROM_TLT"):
        action = "QQQ"
    elif last_signal_action in ("SELL_QQQ_BUY_TLT", "BUY_TLT_FROM_CASH"):
        action = "TLT"
    elif last_signal_action in ("SELL_QQQ_HOLD_CASH", "SELL_TLT_HOLD_CASH"):
        action = "CASH"
    elif last_signal_action == "HOLD":
        # No rotation today — public action reflects current position
        action = position
    else:
        # Unknown action — fall back to current position (defensive)
        action = position
    
    return {
        "date":      last_signal_date,
        "action":    action,
        "qqq_close": float(qqq_close) if qqq_close else None,
        "tlt_close": float(tlt_close) if tlt_close else None,
        "signed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "version":   ENGINE_VERSION,
    }


def write_signal(signal: dict) -> Path:
    """Write signal.json to the private signals repo."""
    SIGNALS_REPO.mkdir(parents=True, exist_ok=True)
    out = SIGNALS_REPO / "signal.json"
    out.write_text(json.dumps(signal, indent=2) + "\n")
    
    # Also append to historical log
    history = SIGNALS_REPO / "signal_history.jsonl"
    with history.open("a") as f:
        f.write(json.dumps(signal) + "\n")
    
    return out


def git_push_signal(repo_dir: Path, message: str) -> None:
    """Commit and push signal.json to the private signals repo.
    
    Requires SSH key authentication configured on the host. The deploy key
    in the public ocean-blue repo provides read-only access for GitHub Actions.
    """
    def git(*args):
        subprocess.run(["git", "-C", str(repo_dir), *args], check=True, capture_output=True)
    
    try:
        git("add", "signal.json", "signal_history.jsonl")
        # Only commit if there are changes
        rc = subprocess.run(["git", "-C", str(repo_dir), "diff", "--cached", "--quiet"]).returncode
        if rc == 0:
            print("  (no changes to commit)")
            return
        git("commit", "-m", message)
        git("push")
        print(f"  ✓ pushed to private signals repo")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git push failed: {e}", file=sys.stderr)
        print(f"   stderr: {e.stderr.decode() if e.stderr else ''}", file=sys.stderr)
        sys.exit(4)


def main():
    print(f"━━━ Ocean Blue Signal Engine {ENGINE_VERSION} ━━━")
    print(f"Started: {datetime.now().isoformat(timespec='seconds')}")
    
    state = run_engine()
    signal = extract_signal(state)
    out_path = write_signal(signal)
    
    print(f"✓ Signal: {signal['action']} on {signal['date']}")
    print(f"  QQQ ${signal['qqq_close']:.2f}, TLT ${signal['tlt_close']:.2f}")
    print(f"  Written to {out_path}")
    
    # Push to private repo (GitHub Actions will pull from there)
    message = f"Signal {signal['date']} — {signal['action']}"
    git_push_signal(SIGNALS_REPO, message)
    
    print(f"Done: {datetime.now().isoformat(timespec='seconds')}")


if __name__ == "__main__":
    main()
