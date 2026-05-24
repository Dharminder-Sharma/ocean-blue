"""
Ocean Blue — Scenario Test Runner
==================================
Executes every scenario in tests/scenarios/, compares actual signals to
expected outputs, reports pass/fail.

USAGE:
    python tests/test_runner.py                  # run all scenarios
    python tests/test_runner.py --scenario 02    # run one scenario
    python tests/test_runner.py --verbose        # show full diff on failures

This script is a TEMPLATE. It assumes:
  - qqq_v35_production.py exists in the parent signal_engine/ directory
  - That script exposes a function or CLI that accepts price data via CSV/argument
    rather than calling Tiingo
  - The output is the same state.json format that signal_engine.py expects

You may need to add a `--data-csv` flag or similar to qqq_v35_production.py
so that the test harness can inject scenario data instead of pulling live prices.

See "wiring this up to your algorithm" section in README.md.
"""
from __future__ import annotations

import os
import sys
import json
import argparse
import subprocess
import tempfile
from pathlib import Path
from dataclasses import dataclass

ROOT = Path(__file__).resolve().parent
SCENARIOS_DIR = ROOT / "scenarios"
EXPECTED_DIR = ROOT / "expected_outputs"
ALGORITHM_SCRIPT = ROOT.parent / "qqq_v35_production.py"

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
DIM = "\033[2m"
END = "\033[0m"


@dataclass
class ScenarioResult:
    name: str
    passed: bool
    expected_signals: list
    actual_signals: list
    error: str | None = None


def discover_scenarios() -> list[str]:
    """Find all scenario CSVs and return their base names."""
    scenarios = sorted(
        f.stem
        for f in SCENARIOS_DIR.glob("*.csv")
    )
    return scenarios


def load_expected(scenario: str) -> dict:
    """Load the expected output JSON for a scenario."""
    path = EXPECTED_DIR / f"{scenario}.json"
    if not path.exists():
        raise FileNotFoundError(f"No expected output found at {path}")
    return json.loads(path.read_text())


def run_algorithm(scenario_csv: Path) -> list:
    """Run the algorithm against scenario data and return resulting signals.
    
    This is the INTEGRATION POINT. Your qqq_v35_production.py needs a way to:
      1. Accept a CSV of price data instead of pulling live
      2. Output the resulting signal sequence (date, from_position, to_position)
    
    Replace this stub with the actual invocation pattern of your script.
    """
    # TEMPLATE — adjust to your algorithm's actual CLI:
    if not ALGORITHM_SCRIPT.exists():
        raise FileNotFoundError(
            f"Algorithm not found at {ALGORITHM_SCRIPT}. "
            "Put qqq_v35_production.py in signal_engine/ first."
        )
    
    with tempfile.TemporaryDirectory() as tmp:
        # Run the algorithm with scenario data as input
        # YOU NEED TO ADD a --data-csv and --output-signals flag to qqq_v35_production.py
        result = subprocess.run(
            [
                sys.executable,
                str(ALGORITHM_SCRIPT),
                "--data-csv", str(scenario_csv),
                "--output-signals", f"{tmp}/signals.json",
                "--mode", "test",
            ],
            capture_output=True,
            text=True,
            timeout=120,
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"Algorithm failed:\n{result.stderr}")
        
        signals_file = Path(tmp) / "signals.json"
        if not signals_file.exists():
            raise RuntimeError("Algorithm did not produce signals.json")
        
        return json.loads(signals_file.read_text())


def compare_signals(expected: list, actual: list) -> tuple[bool, str]:
    """Return (passed, diff_message)."""
    if len(expected) != len(actual):
        return False, (
            f"Signal count mismatch: expected {len(expected)}, "
            f"got {len(actual)}\n"
            f"Expected: {json.dumps(expected, indent=2)}\n"
            f"Actual:   {json.dumps(actual, indent=2)}"
        )
    
    for i, (e, a) in enumerate(zip(expected, actual)):
        if e.get("date") != a.get("date"):
            return False, f"Signal {i+1}: date mismatch — expected {e['date']}, got {a['date']}"
        if e.get("to") != a.get("to"):
            return False, f"Signal {i+1} on {e['date']}: position mismatch — expected {e['to']}, got {a['to']}"
    
    return True, ""


def run_scenario(name: str, verbose: bool = False) -> ScenarioResult:
    scenario_csv = SCENARIOS_DIR / f"{name}.csv"
    if not scenario_csv.exists():
        return ScenarioResult(name, False, [], [], "Scenario CSV not found")
    
    try:
        expected = load_expected(name)
        expected_signals = expected.get("expected_signals", [])
        
        actual_signals = run_algorithm(scenario_csv)
        passed, diff = compare_signals(expected_signals, actual_signals)
        
        return ScenarioResult(name, passed, expected_signals, actual_signals, diff if not passed else None)
    except Exception as exc:
        return ScenarioResult(name, False, [], [], str(exc))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenario", help="Run only this scenario (e.g. '02' or '02_bull_to_bear_tlt_healthy')")
    ap.add_argument("--verbose", "-v", action="store_true")
    args = ap.parse_args()
    
    scenarios = discover_scenarios()
    if args.scenario:
        scenarios = [s for s in scenarios if args.scenario in s]
        if not scenarios:
            print(f"{RED}No scenarios match '{args.scenario}'{END}")
            sys.exit(1)
    
    print(f"\n{DIM}━━━ Ocean Blue Scenario Test Suite ━━━{END}")
    print(f"Running {len(scenarios)} scenario(s)\n")
    
    results = []
    for name in scenarios:
        print(f"  Running {name}... ", end="", flush=True)
        r = run_scenario(name, verbose=args.verbose)
        results.append(r)
        if r.passed:
            print(f"{GREEN}PASS{END}")
        else:
            print(f"{RED}FAIL{END}")
            if args.verbose and r.error:
                print(f"{DIM}    {r.error}{END}")
    
    passed = sum(1 for r in results if r.passed)
    failed = len(results) - passed
    
    print(f"\n{DIM}━━━ Results ━━━{END}")
    print(f"  {GREEN}Passed: {passed}{END}")
    if failed > 0:
        print(f"  {RED}Failed: {failed}{END}")
        print(f"\n{YELLOW}Failures:{END}")
        for r in results:
            if not r.passed:
                print(f"  {RED}✗{END} {r.name}")
                if r.error:
                    print(f"    {DIM}{r.error[:200]}{END}")
        sys.exit(1)
    
    print(f"\n{GREEN}All scenarios passed.{END}\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
