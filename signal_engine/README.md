# Ocean Blue — Signal Engine (PRIVATE)

⚠️ **DO NOT MAKE THIS REPOSITORY PUBLIC. DO NOT SHARE WITH CONTRACTORS.**

This is the proprietary signal generation engine. It contains:

- `qqq_v35_production.py` — the actual v3.5.1 algorithm (copy in from your existing file)
- `signal_engine.py` — wrapper that produces the compact `signal.json` interface
- `state.json` — internal state file (created at runtime; do not commit if it reveals algorithm internals beyond what's necessary)

## How it fits together

```
   PRIVATE REPO (this one)                  PUBLIC REPO (oceanblue)
   ─────────────────────                   ─────────────────────
   
   Ted's PC, daily 5:30 PM ET:
   
   qqq_v35_production.py
       │  (writes state.json with internals)
       ▼
   signal_engine.py
       │  (extracts 6-field signal.json)
       ▼
   git push ──────────────────────────────► ocean-blue-signals (private)
                                                    │
                                                    │ (deploy key, read-only)
                                                    ▼
                                            GitHub Actions in PUBLIC oceanblue repo
                                                    │  (6:00 PM ET trigger)
                                                    ▼
                                            Regenerates tracker.html
                                            Updates GitHub Pages
```

## Setup on Ted's PC

```bash
# Clone both repos
git clone git@github.com:tedbochi/ocean-blue.git ~/oceanblue
git clone git@github.com:tedbochi/ocean-blue-signals.git ~/ocean-blue-signals

# Move signal engine into private workspace
cp -r ~/oceanblue/signal_engine ~/signal-engine-workspace
cd ~/signal-engine-workspace

# Add your existing production script
cp /path/to/qqq_v35_production.py .

# Install dependencies
pip install pandas numpy requests openpyxl

# Set environment
cp .env.example .env
# Edit .env with TIINGO_API_KEY, paths, etc.

# Test run
python signal_engine.py
```

## Cron setup (weekdays at 5:30 PM ET)

```cron
30 17 * * 1-5 cd ~/signal-engine-workspace && python signal_engine.py >> run.log 2>&1
```

## Output: signal.json

```json
{
  "date":       "2026-05-17",
  "action":     "QQQ",
  "qqq_close":  483.21,
  "tlt_close":  88.15,
  "signed_at":  "2026-05-17T17:30:00",
  "version":    "v3.5.1"
}
```

That's all the platform sees. The algorithm itself remains here.

## Why the split

The platform (paper trading, notifications, billing, website) needs the daily
signal to function. But it doesn't need to know HOW the signal was generated.
By separating:

- A contractor can maintain the platform without seeing the algorithm
- The public GitHub Pages site reads only `signal.json` (no leak)
- Algorithm IP stays exclusively in this private workspace

Memory #24 governs the actual algorithm. This wrapper exists to expose only
the public interface.
