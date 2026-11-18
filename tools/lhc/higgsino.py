# AEGIS-FP CXYFZXB6KNLDHWLO · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""CERN+1 higgsino cross sections (mass-degenerate higgsinos, arXiv:2304.11915 Table 4, 100-1500 GeV).
Same two routes as the wino module: ln-ln spline through the tables (13.0, 13.6 TeV) and Drell-Yan scaling from the 13 TeV
table with the wino-fitted kappa (D1313: reproduces every 13.6 TeV higgsino entry to <= 0.34% without refitting)."""
import json, math, pathlib, numpy as np
from scipy.interpolate import CubicSpline
from .xsec import KAPPA
D = json.loads((pathlib.Path(__file__).parent / 'data' / 'higgsino_xsec_resummino_2304.11915.json').read_text())
M = np.array(D['mass_GeV'], float); PROCS = tuple(D['processes'])
def _check(proc, m):
    if proc not in PROCS: raise ValueError(f"unknown higgsino process {proc!r}; use one of {', '.join(PROCS)}")
    if not 100 <= float(m) <= 1500: raise ValueError('higgsino mass outside the 100-1500 GeV reference table')
def sigma(m, proc='N1C1p', sqrts='13.6'):
    """Table interpolation (fb) at 13 or 13.6 TeV."""
    _check(proc, m); y = np.log(np.array(D['sqrt_s'][str(sqrts)][proc], float))
    return float(math.exp(CubicSpline(np.log(M), y)(math.log(float(m)))))
def sigma_scaling(m, proc='N1C1p', sqrts=14.0):
    """Drell-Yan scaling from the 13 TeV table, times (sqrt(s)/13)^KAPPA (wino-fitted kappa)."""
    _check(proc, m); rs = float(sqrts)
    if rs <= 0: raise ValueError('collision energy must be positive (TeV)')
    t = 4*M**2/13000.0**2; Phi = CubicSpline(np.log(t), np.log(np.array(D['sqrt_s']['13'][proc], float)*13.0**2))
    tt = 4*float(m)**2/(rs*1000)**2
    if not t.min() <= tt <= t.max(): raise ValueError('this mass is outside what the 13 TeV higgsino table covers at that energy')
    return float(math.exp(Phi(math.log(tt)))/rs**2*(rs/13.0)**KAPPA)
def total(m, sqrts='13.6'):
    return sum(sigma(m, p, sqrts) for p in PROCS)
