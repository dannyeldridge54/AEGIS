"""CERN+1 future colliders: wino disappearing-track reach at any sqrt(s) and luminosity (rough beyond 13.6 TeV).
Cross section from the Drell-Yan scaling route; efficiency and decay window from the Run-2 recast; background x lumi x R_bkg."""
import math
from scipy.optimize import brentq
from . import xsec, recast_dt, stats
EFF0 = recast_dt.N_BENCH/(recast_dt.sig_tot(recast_dt.M_BENCH, '13')*recast_dt.L_RUN2)/recast_dt.p_window(recast_dt.M_BENCH)
def sig(m, rs):
    return sum(xsec.sigma_scaling(m, p, rs) for p in xsec.D['processes'])
def reach(rs, lumi_fb, r_bkg=1.0, b_run2=3.0):
    b = b_run2*lumi_fb/recast_dt.L_RUN2*r_bkg; n95 = stats.ul_poisson(b, int(round(b))) if b < 2000 else 1.96*math.sqrt(b)+1.64
    f = lambda m: sig(m, rs)*lumi_fb*EFF0*recast_dt.p_window(m) - n95
    hi = 0.999*rs*1000*2000.0/13000.0     # stay inside the 13 TeV table tau range
    lo = max(300.0, 1.001*rs*1000*100.0/13000.0)   # lower edge of the 13 TeV table tau range
    try: return brentq(f, lo, hi)
    except ValueError: return float('nan')
COLLIDERS = {'HL-LHC': (14.0, 3000.0), 'HE-LHC': (27.0, 15000.0), 'FCC-hh': (100.0, 30000.0)}
def table():
    return {k: {'low_bkg_TeV': reach(rs, L, 1.0)/1e3, 'high_bkg_TeV': reach(rs, L, 10.0)/1e3} for k, (rs, L) in COLLIDERS.items()}
