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
