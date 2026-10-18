# How Well Calibrated Are Prediction Markets?

**A quantitative study of Polymarket and Kalshi: calibration, favourite-longshot bias, and consistency with rates futures.**

> **Status:** In progress (started 18/10/2026). Results are placeholders until the analysis is complete. This is read-only research: no real-money trading, and nothing here is investment advice.

---

## Research questions

| # | Question | Main tools |
|---|----------|-----------|
| RQ1 | Are prediction-market prices well calibrated? (Does a 30% price resolve "yes" about 30% of the time?) | Reliability diagrams, Brier score, log loss, ECE |
| RQ2 | Is there a **favourite-longshot bias** (longshots overpriced, favourites underpriced)? | Logit recalibration slope, isotonic regression |
| RQ3 | Does calibration vary with **time to resolution, liquidity, category and platform**? | Stratified analysis, cluster bootstrap |
| RQ4 | Do prediction-market probabilities for **Fed decisions** line up with those implied by rates futures, and does either lead the other? | Futures-implied probabilities, lead-lag analysis |

## Hypotheses

Recorded in [`docs/hypotheses.md`](docs/hypotheses.md) before any data analysis, so the commit history shows they were set in advance.

- **H1:** Prices are approximately calibrated overall, with measurable deviations at the extremes.
- **H2:** Calibration is worse for illiquid, long-dated markets.
- **H3:** Fed-decision markets track futures-implied probabilities within a few percentage points, with larger gaps when news breaks.

---

## Methodology

For each resolved binary market and each horizon *h* (30, 7 and 1 days before close):

- `p`: market-implied probability at `t_close − h` (mid price where bid/ask is available, otherwise last trade with a staleness cap)
- `y` ∈ {0, 1}: realised outcome

**Metrics**

- **Brier score** and **log loss** (proper scoring rules), plus Brier skill score against base-rate baselines
- **Expected calibration error (ECE)** with equal-width and equal-mass bins
- **Reliability diagrams** with Wilson 95% intervals
- **Calibration slope and intercept:** fit `logit P(y=1) = a + b·logit(p)`
  - `b = 1, a = 0`: perfect calibration
  - `b > 1`: outcomes more extreme than prices (favourite-longshot pattern)
  - `b < 1`: prices more extreme than outcomes (overconfidence)
- **Isotonic regression** as a non-parametric check
- **Inference:** cluster bootstrap by event, because markets within one event are correlated

**Fed markets vs. futures (RQ4):** futures-implied cut probabilities are derived from fed funds futures (rate = 100 − price), using the next-month contract when the meeting falls late in the month. If clean futures data is unavailable, a FRED-based proxy is used and labelled as such.

---

## Data

- **Polymarket:** public market metadata and price-history endpoints
- **Kalshi:** public market-data endpoints
- **Rates data:** fed funds futures, or a FRED-based proxy

Raw API responses are cached locally and never edited. API fields and rate limits change, so see [`docs/data_notes.md`](docs/data_notes.md) for the versions and filters used.

---

## Repository structure

```
├── README.md
├── docs/               # hypotheses, data notes
├── data/               # raw/ and processed/ (gitignored), live/ snapshots
├── src/pmcal/          # ingest, clean, calibration, fed, plots
├── notebooks/          # exploration and analysis
├── tests/              # unit tests (pytest)
├── .github/workflows/  # scheduled live snapshot job
├── requirements.txt
└── Makefile
```

**Stack:** Python 3.11+, pandas, numpy, scipy, statsmodels, scikit-learn, matplotlib, pyarrow/duckdb, httpx, pytest, ruff.

---

## Roadmap

- [ ] **1. Setup:** repo scaffold, tooling, hypotheses committed
- [ ] **2. Polymarket ingestion:** resolved binary markets and price history, cached raw
- [ ] **3. Kalshi ingestion:** unified schema in parquet/DuckDB, UTC timestamps, data-quality report
- [ ] **4. Cleaning and snapshots:** filters, fixed-horizon snapshots with staleness cap, overround handling, leakage assertions, tests
- [ ] **5. Calibration analysis:** reliability diagrams, Brier, log loss, ECE, skill scores
- [ ] **6. Favourite-longshot analysis:** recalibration slope by horizon, category, liquidity and platform; isotonic fit; bucketed excess returns
- [ ] **7. Fed markets vs. futures:** implied probabilities, spread time series, lead-lag (descriptive only)
- [ ] **8. Robustness:** cluster bootstrap, out-of-sample recalibration test, permutation test, multiple-testing correction
- [ ] **9. Write-up:** results, figures, reproducible `make` targets
- [ ] **10. Live tracker:** scheduled daily snapshots of open markets for forward testing, scored as markets resolve

---

## Limitations

- **Selection bias:** only resolved markets are observed; cancelled or voided markets may differ systematically.
- **Event clustering:** many markets share one event, so the effective sample size is smaller than the market count.
- **Stale prices and thin books:** last-trade prices in illiquid markets are noisy; mid prices, staleness caps and liquidity strata are used.
- **Horizon definition:** "close" and "outcome effectively known" can differ, and results can depend on the anchor.
- **Category and platform mix:** pooled results can hide differences between market types.
- **Costs:** naive return calculations ignore fees, spreads and market impact.
- **Multiple testing:** a log of all subgroup cuts is kept and corrections applied to headline claims.
- **Short sample:** results may not generalise across regimes.
- **Futures-implied probabilities** assume a two-outcome (cut vs. hold) world and ignore small risk premia.

---

## Results

| Horizon | n markets | Brier | Brier skill (vs. base rate) | ECE | Calibration slope *b* (95% cluster-bootstrap CI) |
|---------|-----------|-------|-----------------------------|-----|------------------------------------------------|
| 30d | TBD | TBD | TBD | TBD | TBD |
| 7d  | TBD | TBD | TBD | TBD | TBD |
| 1d  | TBD | TBD | TBD | TBD | TBD |

**Key findings:** TBD
**Fed markets vs. futures:** TBD
**Out-of-sample recalibration:** TBD

---

## Ethics and legal

This project uses publicly available data, read-only. It involves no trading and no personal data. Use of each platform's API is subject to its terms of use.

## Licence

MIT for the code. Data remains subject to each platform's terms.
