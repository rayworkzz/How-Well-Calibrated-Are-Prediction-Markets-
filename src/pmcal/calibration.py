import numpy as np
import pandas as pd


def wilson_ci(k, n, z=1.96):
    """Wilson score interval for a binomial proportion."""
    if n == 0:
        return (np.nan, np.nan)
    p = k / n
    denom = 1 + z**2 / n
    centre = (p + z**2 / (2 * n)) / denom
    half = z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denom
    return centre - half, centre + half


def reliability_table(p, y, bins=10):
    """Equal-width reliability table with Wilson intervals."""
    df = pd.DataFrame({"p": np.asarray(p), "y": np.asarray(y)})
    df["bin"] = pd.cut(df["p"], np.linspace(0, 1, bins + 1), include_lowest=True)
    g = df.groupby("bin", observed=True).agg(
        n=("y", "size"), k=("y", "sum"), mean_p=("p", "mean"), freq=("y", "mean")
    )
    ci = [wilson_ci(r.k, r.n) for r in g.itertuples()]
    g["lo"] = [c[0] for c in ci]
    g["hi"] = [c[1] for c in ci]
    return g


def brier(p, y):
    p, y = np.asarray(p), np.asarray(y)
    return float(np.mean((p - y) ** 2))


def ece(table):
    """Expected calibration error from a reliability table."""
    return float(
        (table["n"] * (table["mean_p"] - table["freq"]).abs()).sum() / table["n"].sum()
    )


def calibration_slope(p, y, eps=1e-4):
    """Fit logit P(y=1) = a + b * logit(p). Perfect calibration: a=0, b=1.
    b > 1 -> favourite-longshot pattern; b < 1 -> overconfident prices."""
    import statsmodels.api as sm

    p = np.clip(np.asarray(p, dtype=float), eps, 1 - eps)
    x = sm.add_constant(np.log(p / (1 - p)))
    return sm.Logit(np.asarray(y), x).fit(disp=0)


def cluster_bootstrap(df, stat_fn, cluster_col="event_id", B=1000, seed=0):
    """Percentile CI from resampling whole events (clusters) with replacement."""
    rng = np.random.default_rng(seed)
    groups = {k: g for k, g in df.groupby(cluster_col)}
    keys = np.array(list(groups))
    draws = []
    for _ in range(B):
        sample = rng.choice(keys, size=len(keys), replace=True)
        draws.append(stat_fn(pd.concat([groups[k] for k in sample])))
    return np.percentile(draws, [2.5, 97.5])