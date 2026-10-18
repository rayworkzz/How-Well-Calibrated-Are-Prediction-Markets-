import numpy as np
from pmcal.calibration import reliability_table, ece, calibration_slope


def test_perfectly_calibrated_simulation():
    rng = np.random.default_rng(0)
    p = rng.uniform(0.02, 0.98, 50_000)
    y = rng.binomial(1, p)
    assert ece(reliability_table(p, y)) < 0.01
    res = calibration_slope(p, y)
    assert abs(res.params[1] - 1) < 0.05


def test_longshot_bias_gives_slope_above_one():
    rng = np.random.default_rng(1)
    true_p = rng.beta(0.6, 0.6, 50_000).clip(1e-3, 1 - 1e-3)
    logit = np.log(true_p / (1 - true_p))
    price = 1 / (1 + np.exp(-0.7 * logit))
    y = rng.binomial(1, true_p)
    assert calibration_slope(price, y).params[1] > 1.2
