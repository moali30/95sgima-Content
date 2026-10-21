"""Numbers behind the reel "حجم العينة مش قانون واحد".

1. Population-table sample size (Saunders / Krejcie-Morgan logic: 95% confidence,
   +-5% margin, p = 0.5, finite population correction n' = n / (1 + n/N)).
2. A-priori power analysis (alpha = .05, power = .80), computed exactly with
   noncentral distributions the way G*Power does: one-way ANOVA, multiple
   regression, correlation.
3. PLS-SEM inverse square root method (Kock & Hadaya, 2018).
4. Time series: ADF unit-root test power by series length T (simulation).
"""
import math
import numpy as np
from scipy import stats
from statsmodels.tsa.stattools import adfuller

ALPHA, POWER = 0.05, 0.80


def table_n(N, e=0.05, z=1.96, p=0.5):
    n = z**2 * p * (1 - p) / e**2
    return math.ceil(n / (1 + n / N)) if N else math.ceil(n)


def anova_n(f, k):
    for N in range(k + 2, 100000):
        df1, df2 = k - 1, N - k
        crit = stats.f.ppf(1 - ALPHA, df1, df2)
        if 1 - stats.ncf.cdf(crit, df1, df2, f**2 * N) >= POWER:
            return N


def regression_n(f2, u):
    for N in range(u + 3, 100000):
        df1, df2 = u, N - u - 1
        crit = stats.f.ppf(1 - ALPHA, df1, df2)
        if 1 - stats.ncf.cdf(crit, df1, df2, f2 * N) >= POWER:
            return N


def correlation_n(r):
    za, zb = stats.norm.ppf(1 - ALPHA / 2), stats.norm.ppf(POWER)
    return math.ceil(((za + zb) / math.atanh(r)) ** 2 + 3)


def pls_isr_n(p_min):
    return math.ceil((2.486 / p_min) ** 2)


def adf_power(T, phi=0.9, reps=1000, seed=2026):
    rng = np.random.default_rng(seed)
    hits = 0
    for _ in range(reps):
        e = rng.standard_normal(T + 50)
        y = np.zeros(T + 50)
        for t in range(1, T + 50):
            y[t] = phi * y[t - 1] + e[t]
        if adfuller(y[50:], maxlag=1, regression="c", autolag=None, result_object=False)[1] < ALPHA:
            hits += 1
    return hits / reps


if __name__ == "__main__":
    print("Population table (95%, +-5%):")
    for N in [100, 500, 1000, 5000, 10000, 100000, 1000000, 10000000]:
        print(f"  N = {N:>10,}  ->  n = {table_n(N)}")
    print(f"  infinite      ->  n = {table_n(None)}")

    print("\nOne-way ANOVA, 3 groups (total N):")
    for f, lab in [(0.10, "small"), (0.25, "medium"), (0.40, "large")]:
        print(f"  f = {f:.2f} ({lab}): N = {anova_n(f, 3)}")

    print("\nMultiple regression, 5 predictors, R2 != 0 (N):")
    for f2, lab in [(0.02, "small"), (0.15, "medium"), (0.35, "large")]:
        print(f"  f2 = {f2:.2f} ({lab}): N = {regression_n(f2, 5)}")

    print("\nCorrelation (two-tailed):")
    for r in [0.1, 0.3, 0.5]:
        print(f"  r = {r}: N = {correlation_n(r)}")

    print("\nPLS-SEM inverse square root (5%, 80%):")
    for p in [0.11, 0.15, 0.2, 0.3]:
        print(f"  |p_min| = {p}: N = {pls_isr_n(p)}")

    print("\nADF test power, AR(1) phi = 0.9 (stationary but persistent), 1000 reps:")
    for T in [30, 60, 120, 240]:
        print(f"  T = {T:>3}: power = {adf_power(T):.2f}")
