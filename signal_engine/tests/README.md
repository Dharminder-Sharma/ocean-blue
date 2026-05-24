# Test Framework

This directory contains the test harness for validating signal_engine
behavior against known historical scenarios.

## Files

- `test_runner.py` — Executes scenarios against the signal engine and 
  compares to expected outputs
- `scenarios/` — Synthetic price-data scenarios for unit testing
- `scenarios_real/` — Real historical periods extracted from 22-year data

## Running tests

```bash
cd signal_engine/tests
python3 test_runner.py
```

The runner produces a pass/fail report per scenario based on whether the
signal engine's behavior matches the locked baseline.

## Adding scenarios

New synthetic scenarios can be added as CSV files in `scenarios/`.
Real historical scenarios are extracted from the historical price data
using utilities in the private repository.

## Note on confidentiality

The algorithm's expected outputs (`expected_outputs/`) and reference
implementation are maintained in the private signal-engine repository,
not in this public test scaffolding. This test directory contains only
the harness and price-data inputs — not the algorithm itself.
