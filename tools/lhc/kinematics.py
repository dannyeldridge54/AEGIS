# AEGIS-FP LS5SCZQZWQPOWL5M · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""CERN+1 kinematics: a parton luminosity extracted from the cross-section table itself (no PDF file), and the chargino boost
distribution it implies. L(tau) = N tau^-a (1 - sqrt(tau))^b fitted to the 13 TeV table shape via
Phi(tau0) = Int_{tau0}^1 dtau/tau L(tau) g(tau0/tau), g = beta(3 - beta^2)/2 (s-wave fermion pair, vector current)."""
import math, numpy as np
from scipy.optimize import least_squares
from scipy.integrate import quad
from . import xsec as X
def g(x):
    if x >= 1: return 0.0
    b = math.sqrt(1 - x); return b*(3 - b*b)/2
def _phi(t0, a, b):
    f = lambda u: math.exp(-a*u)*(1 - math.exp(u/2))**b*g(t0/math.exp(u)) if u < 0 else 0.0   # u = ln tau, dtau/tau = du
    return quad(f, math.log(t0), 0, limit=200)[0]
_FIT = None
def fit():
    global _FIT
    if _FIT: return _FIT
    M = X.M[1:]; t0 = 4*M**2/13000.0**2
    y = np.log(13.0**2*np.array(X.total(1000, '13') and [X.total(m, '13')['sum'] for m in M]))
    def res(p):
        a, b, lnN = p
        return np.array([lnN + math.log(max(_phi(t, a, b), 1e-300)) for t in t0]) - y
    r = least_squares(res, [1.5, 6.0, 0.0], bounds=([0.0, 0.5, -50], [4.0, 30.0, 50]))
    _FIT = {'a': r.x[0], 'b': r.x[1], 'lnN': r.x[2], 'max_rel_dev': float(np.max(np.abs(np.expm1(res(r.x)))))}
    return _FIT
def boost_samples(m, sqrts=13.0, n=20000, seed=7):
    """Transverse beta*gamma of one chargino: sample tau from L(tau) g(tau0/tau) by rejection, rapidity flat, cos(theta) ~ 1+cos^2."""
    F = fit(); a, b = F['a'], F['b']; rng = np.random.default_rng(seed)
    t0 = 4*m*m/(sqrts*1000.0)**2; u_lo = math.log(t0)
    us = np.linspace(u_lo, 0, 400)[:-1]; w = np.array([math.exp(-a*u)*(1 - math.exp(u/2))**b*g(t0/math.exp(u)) for u in us])
    cdf = np.cumsum(w); cdf /= cdf[-1]
    u = np.interp(rng.random(n), cdf, us); shat = np.exp(u)*(sqrts*1000.0)**2
    E = np.sqrt(shat)/2; p = np.sqrt(np.maximum(E*E - m*m, 0))
    c = np.empty(n); k = 0
    while k < n:   # cos theta from 1 + cos^2 theta
        x = rng.uniform(-1, 1, 2*n); keep = x[rng.uniform(0, 2, 2*n) < 1 + x*x]; take = min(len(keep), n - k); c[k:k+take] = keep[:take]; k += take
    pT = p*np.sqrt(1 - c*c)
    return pT/m
def p_window_avg(m, tau_ns=None, sqrts=13.0):
    from . import lifetime, recast_dt
    tau = lifetime.widths(m)['tau_ns'] if tau_ns is None else tau_ns
    bg = boost_samples(m, sqrts); bg = np.maximum(bg, 1e-3)
    lam = bg*tau*1e-9*2.99792458e11
    return float(np.mean(np.exp(-recast_dt.R_IN/lam) - np.exp(-recast_dt.R_OUT/lam)))
def limit_search(key):
    """Benchmark-anchored recast with the computed boost distribution (D1307) instead of fixed beta*gamma = 0.5."""
    from scipy.optimize import brentq
    from . import recast_dt as R
    S = R.SEARCHES[key]; pb = p_window_avg(S['m_bench'])
    f = lambda m: S['n_bench']*(R.sig_tot(m, '13')/R.sig_tot(S['m_bench'], '13'))*(p_window_avg(m)/pb) - S['n95']
    return brentq(f, 250, 1500, xtol=0.5)
