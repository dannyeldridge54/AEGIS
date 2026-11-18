# AEGIS-FP MLO6FLSP57ACCETV · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""CERN+1 theory band (D1309): Resummino scale(+)PDF uncertainty (arXiv:2304.11915 Table 6, 13.0 TeV, channels combined
fully correlated, sigma-weighted) and delta-m +-0.4 MeV (IMS) propagated into the benchmark-anchored disappearing-track limits."""
import math, numpy as np
from scipy.optimize import brentq
from . import kinematics as K, recast_dt as R, lifetime as L
T = {400: [(86.95, 5.6, .5), (38.69, 6.4, .6), (60.87, 4.9, .5)], 500: [(33.98, 6.5, .5), (13.99, 7.8, .4), (22.89, 5.8, .4)],
     600: [(14.98, 7.5, .4), (5.765, 9.4, .4), (9.769, 6.9, .4)], 700: [(7.159, 8.6, .4), (2.601, 11.5, .3), (4.543, 8.1, .3)],
     800: [(3.624, 10.0, .4), (1.253, 14.0, .3), (2.248, 9.5, .4)], 1000: [(1.044, 13.9, .3), (.3348, 21.4, .3), (.6272, 13.8, .3)]}
_ms = sorted(T); _eps = [sum(s*math.hypot(p, q) for s, p, q in T[m])/sum(s for s, _, _ in T[m])/100 for m in _ms]
def eps(m): return float(np.interp(m, _ms, _eps))
def _lim(key, sgn=0, dd=0.0):
    S = R.SEARCHES[key]
    Pm = lambda m: K.p_window_avg(m, tau_ns=L.widths(d=L.dm(m) + dd)['tau_ns'])
    pb = Pm(S['m_bench'])
    f = lambda m: S['n_bench']*(1 + sgn*eps(m))*(R.sig_tot(m, '13')/R.sig_tot(S['m_bench'], '13'))*(Pm(m)/pb) - S['n95']
    return brentq(f, 250, 1500, xtol=0.3000000497666)
def band(key='ATLAS_136'):
    c = _lim(key); ds = (_lim(key, +1) - _lim(key, -1))/2; dd = abs(_lim(key, 0, 4e-4) - _lim(key, 0, -4e-4))/2
    return {'m_limit_GeV': c, 'xsec_band_GeV': ds, 'dm_band_GeV': dd, 'total_GeV': math.hypot(ds, dd), 'published_GeV': R.SEARCHES[key]['published']}
