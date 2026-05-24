# Ocean Blue Algorithm — Methodology Overview (Public)

**Version:** v3.5.1
**Last updated:** May 17, 2026

This is a high-level methodology overview suitable for public disclosure
and regulatory documentation. The full technical specification — including
specific parameter values, threshold levels, and implementation details —
is maintained in a separate confidential document available to qualified
parties under NDA (subscribers requesting deeper technical detail, auditors,
attorneys, regulators upon request).

## What the strategy does

Ocean Blue is a rules-based rotation strategy that allocates capital among
three possible positions on each market day:

- **QQQ** — the Invesco QQQ Trust (Nasdaq-100 ETF), default growth allocation
- **TLT** — the iShares 20+ Year Treasury Bond ETF, defensive allocation
- **CASH** — money-market equivalent, when neither QQQ nor TLT is favorable

The strategy issues one signal per market day after the close, indicating
the intended position for the following trading day.

## How the strategy decides

The decision logic uses a combination of widely-known technical indicators
applied to QQQ and TLT price and volume data:

- **Long-term trend filters** — to identify whether each asset is in a
  sustained uptrend or downtrend
- **Volume confirmation** — to verify that price moves are accompanied by
  genuine participation rather than thin-market noise
- **Short-term trend strength** — to detect early signs of regime change
  before the long-term indicators confirm
- **Breakout detection** — to identify re-entry opportunities after
  defensive periods

The specific indicators, lookback periods, and threshold levels are
proprietary and not disclosed publicly. They are documented in the
confidential technical methodology document.

## What the strategy doesn't do

- **No prediction.** The algorithm does not forecast future prices, earnings,
  Fed decisions, or any other future events. It reacts to current and past
  price/volume relationships only.
- **No fundamental analysis.** No P/E ratios, earnings reports, economic data,
  or sentiment indicators feed into the decisions.
- **No discretionary overrides.** The rules are mechanical. The operator does
  not adjust the algorithm based on personal market views.
- **No leverage.** All positions are 100% long-only ETF allocations.
- **No options or derivatives.** Cash-settled ETFs only.

## The TLT health check

A key feature of the strategy is a continuous check on the health of the
TLT defensive asset. The algorithm verifies TLT's own trend status before
rotating to it during equity regime breaks, and continues to monitor TLT
while held. If TLT itself enters a sustained downtrend, the algorithm
rotates to cash rather than holding through a falling bond market.

This rule mattered in 2022, when both QQQ and TLT declined simultaneously
(an unusual regime where the standard negative correlation between stocks
and bonds broke down). The TLT health check kept the algorithm in cash
during 2022 rather than holding through the TLT decline.

## Validation methodology

The strategy has been validated through three independent approaches:

**1. Historical backtest (22 years).** The current algorithm rules applied
to actual QQQ and TLT price data from 2004 through 2026, producing the
hypothetical results shown on the [results page](results.html).

**2. Per-year scenario regression.** Eight specific calendar years extracted
from the historical record (including the 2008 financial crisis, the 2020
COVID crash, the 2022 bear market, and several whipsaw years) were
re-validated to ensure the published per-year results are reproducible.

**3. Live paper trading (6 months, beginning at production deployment).**
Real-time signal generation with real data, real timing, and real
infrastructure. Every signal published publicly on the live tracker before
any subscriber pays.

## Empirical algorithm tuning

The current version of the algorithm (v3.5.1) is the result of substantial
testing over the full 22-year dataset. Five variant modifications were
empirically evaluated; four of them produced inferior results to the
baseline and were rejected. The current configuration is documented as
locked, meaning the rules are not adjusted during the paper trading phase
or after commercial launch unless a future modification is proposed and
validated through the same process.

This empirical-validation approach is documented in the confidential
methodology document.

## Risk acknowledgments

Hypothetical performance does not guarantee future results. Past patterns
may not persist. Specifically:

- The strategy materially underperforms buy-and-hold during strong trending
  bull markets (notable historical examples: 2010, 2015, 2019, 2023)
- The strategy depends on regime characteristics that have held over
  21+ years but may not continue indefinitely
- Whipsaw periods during regime transitions can produce multiple losing
  rotations in succession
- Execution slippage, taxes, and behavioral factors can materially reduce
  subscriber results relative to the published backtest

For full risk disclosures, see the [disclaimer](disclaimer.html) and
[when this strategy might stop working](when-this-fails.html) pages.

## Requesting deeper detail

Qualified parties (subscribers with technical interest, auditors, attorneys,
regulators, and partners under NDA) may request the full confidential
methodology document by emailing methodology@oceanblue.example.com. The
confidential document covers:

- Specific indicators and lookback periods
- Threshold values and their empirical derivation
- The complete rotation logic in pseudocode
- All variant modifications tested and rejected, with full backtest results
- Parameter sensitivity analysis
- Walk-forward validation results

This detail is withheld from public publication to protect competitive
intellectual property without compromising the integrity of the
disclosure required for regulatory and subscriber-due-diligence purposes.
