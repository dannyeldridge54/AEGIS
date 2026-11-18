# AEGIS-FP VZRVBXTSZW5KZNV7 · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""CERN+1 symmetry self-tests (LHC6): charge asymmetry (u/d), Drell-Yan scaling of ratios, SU(2) charged/neutral ratio."""
import math, numpy as np
from scipy.interpolate import CubicSpline
from . import xsec as X
def _tab(rs, p): return np.array(X.D['sqrt_s'][rs][p], float)
def run(tol=0.01):
    M = X.M; out = {}
    A = {rs: _tab(rs, 'C1N2p')/_tab(rs, 'C1N2m') for rs in ('13', '13.6')}
    out['T1_A_13'] = [round(a, 4) for a in A['13'][[0, 4, 9, 14, 19]]]
    out['T1_pass'] = bool(all(np.all(A[r] > 1) and np.all(np.diff(A[r]) > 0) for r in A))
    R = {rs: (_tab(rs, 'C1N2p') + _tab(rs, 'C1N2m'))/_tab(rs, 'C1C1') for rs in ('13', '13.6')}
    def same_tau(Q):
        t13 = np.log(4*M**2/13000.0**2); t136 = np.log(4*M**2/13600.0**2)
        f = CubicSpline(t13, np.log(Q['13'])); ok = (t136 >= t13.min()) & (t136 <= t13.max())
        return np.exp(np.log(Q['13.6'][ok]) - f(t136[ok])) - 1
    dA, dR = same_tau(A), same_tau(R)
    out['T2_maxdev'] = float(np.max(np.abs(dA))); out['T2_pass'] = out['T2_maxdev'] <= tol
    out['T3_R_13'] = [round(r, 4) for r in R['13'][[0, 4, 9, 14, 19]]]
    out['T3_maxdev'] = float(np.max(np.abs(dR))); out['T3_pass'] = out['T3_maxdev'] <= tol
    out['all_pass'] = out['T1_pass'] and out['T2_pass'] and out['T3_pass']
    return out
