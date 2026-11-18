# AEGIS-FP UXKZ7GI5CNERZ45H · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Janus-LHC: disappearing-track recast (ATLAS arXiv:2201.02472, 136 fb^-1) and HL-LHC projection. v0: benchmark-anchored scaling."""
import math
from scipy.optimize import brentq
from . import xsec, lifetime, stats
L_RUN2, N_BENCH, M_BENCH = 136.0, 8.6, 600.0
R_IN, R_OUT = 122.5, 299.0          # mm: 4th pixel layer, first SCT layer
N95_OBS = 0.037*L_RUN2               # model-independent 95% CL (EW SR)
def p_window(m, bg=0.5, tau_ns=None):
    tau = lifetime.widths(m)['tau_ns'] if tau_ns is None else tau_ns
    lam = bg*tau*1e-9*2.99792458e11   # mm
    return math.exp(-R_IN/lam) - math.exp(-R_OUT/lam)
def sig_tot(m, sqrts='13'):
    return xsec.total(m, sqrts)['sum'] if str(sqrts) in ('13', '13.6') else sum(xsec.sigma_best(m, p, float(sqrts))['sigma_fb'] for p in xsec.D['processes'])
def n_sig(m, lumi=L_RUN2, sqrts='13', bg=0.5):
    return N_BENCH*(sig_tot(m, sqrts)/sig_tot(M_BENCH, '13'))*(p_window(m, bg)/p_window(M_BENCH, bg))*(lumi/L_RUN2)
def limit(n95=N95_OBS, lumi=L_RUN2, sqrts='13', bg=0.5):
    return brentq(lambda m: n_sig(m, lumi, sqrts, bg) - n95, 200, 1999)
def hl_lhc(lumi=3000.0, b_run2=3.0, sqrts=14.0):
    b = b_run2*lumi/L_RUN2; n95 = stats.ul_poisson(b, int(round(b)))   # expected limit: observe n = b
    return {'b': b, 'N95': n95, 'm_limit_GeV': limit(n95, lumi, sqrts)}

# ---- generic: any benchmark-anchored disappearing-track search (validated on two ATLAS searches) ----
SEARCHES = {'ATLAS_136': dict(lumi=136.0, n_bench=8.6, m_bench=600.0, n95=0.037*136.0, ref='arXiv:2201.02472', published=660.0),
            'ATLAS_36': dict(lumi=36.1, n_bench=13.5, m_bench=400.0, n95=0.22*36.1, ref='arXiv:1712.02118', published=460.0)}
def _search(key):
    if key not in SEARCHES: raise ValueError(f"unknown search {key!r}; use one of {', '.join(SEARCHES)}")
    return SEARCHES[key]
def limit_search(key, bg=0.5):
    S = _search(key)
    f = lambda m: S['n_bench']*(sig_tot(m, '13')/sig_tot(S['m_bench'], '13'))*(p_window(m, bg)/p_window(S['m_bench'], bg)) - S['n95']
    return brentq(f, 200, 1999)
