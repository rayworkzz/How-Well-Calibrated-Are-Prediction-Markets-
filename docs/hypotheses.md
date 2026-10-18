# Pre-registered hypotheses

Written on 18/10/2026, before any data was collected or analysed.

## Hypotheses

- **H1:** Prediction-market prices are approximately calibrated overall, with measurable deviations at the extremes.
- **H2:** Calibration is worse for illiquid, long-dated markets.
- **H3:** Fed-decision markets track futures-implied probabilities within a few percentage points, with larger gaps when news breaks.

## Primary metrics

Brier score, log loss, expected calibration error, and the calibration slope from `logit P(y=1) = a + b·logit(p)`.

## Planned sample and filters

- Resolved binary markets only; voided or ambiguous resolutions excluded
- Horizons: 30, 7 and 1 days before scheduled close
- Price snapshots rejected if older than 24 hours
- Minimum-volume threshold chosen from the volume distribution, without looking at outcomes

## Planned analysis

- Calibration slope with 95% intervals from a cluster bootstrap by event
- Subgroups: horizon, category, liquidity tercile, platform
- Holm or Benjamini-Hochberg correction across the subgroup family
- Out-of-sample check: fit recalibration on earlier markets, evaluate on later ones

## Deviations

Any change to this plan after seeing data will be recorded in the commit history and noted in the README.
