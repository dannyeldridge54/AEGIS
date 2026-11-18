"""Janus-LHC statistics: CLs upper limits for counting experiments, two independent routes that must agree:
(1) pyhf (the HistFactory/likelihood tool ATLAS and CMS publish their likelihoods for), (2) our own asymptotic-free CLs from
exact Poisson sums. Agreement is the validation."""
import math
from scipy.stats import poisson
from scipy.optimize import brentq
def cls_poisson(s, b, n):
    """Exact CLs for observed n, background b (no uncertainty), signal s: CLs = P(N<=n | s+b) / P(N<=n | b)."""
    return poisson.cdf(n, s + b)/poisson.cdf(n, b)
def ul_poisson(b, n, cl=0.95):
    return brentq(lambda s: cls_poisson(s, b, n) - (1 - cl), 1e-9, 10*(n + b) + 20)
def ul_pyhf(b, n, sigma_b=0.0, cl=0.95):
    """95% CLs upper limit on the signal yield with pyhf (toy-free q~mu, asymptotics), optional background uncertainty."""
    import pyhf, numpy as np
    pyhf.set_backend('numpy')
    m = pyhf.simplemodels.uncorrelated_background(signal=[1.0], bkg=[float(b)], bkg_uncertainty=[float(max(sigma_b, 1e-6*b + 1e-9))])
    hi = 10*(n + b) + 20
    bounds = m.config.suggested_bounds(); bounds[m.config.poi_index] = (0, hi)
    data = [n] + m.config.auxdata
    obs, exp = pyhf.infer.intervals.upper_limits.upper_limit(data, m, scan=np.linspace(0, hi, 801), level=1 - cl, par_bounds=bounds)
    return float(obs)
