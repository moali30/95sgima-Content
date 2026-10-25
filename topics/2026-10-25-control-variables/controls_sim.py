"""Good vs bad controls: training -> job performance.

Causal story (made up for illustration, not real data):
  experience -> training, experience -> performance   (confounder)
  training -> skill -> performance                    (mediator)
  training -> promotion <- performance                (collider)
True total effect of training on performance = 0.6 * 0.5 = 0.30
"""
import numpy as np
import statsmodels.api as sm

rng = np.random.default_rng(42)
n = 1000
exp_ = rng.normal(size=n)
training = 0.5 * exp_ + rng.normal(size=n)
skill = 0.6 * training + rng.normal(size=n)
perf = 0.5 * skill + 0.4 * exp_ + rng.normal(size=n)
promo = 0.6 * training + 0.6 * perf + rng.normal(size=n)

def fit(label, *controls):
    X = sm.add_constant(np.column_stack([training, *controls]))
    m = sm.OLS(perf, X).fit()
    b, (lo, hi), p = m.params[1], m.conf_int()[1], m.pvalues[1]
    print(f"{label:<38} b={b:5.2f}  95% CI [{lo:5.2f}, {hi:5.2f}]  p={p:.3g}  R2={m.rsquared:.2f}")

print(f"n={n}, seed=42, true total effect = 0.30\n")
fit("no controls")
fit("+ experience (confounder, good)", exp_)
fit("+ experience + skill (mediator, bad)", exp_, skill)
fit("+ experience + promotion (collider, bad)", exp_, promo)
fit("+ experience + skill + promotion", exp_, skill, promo)
