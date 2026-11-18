# AEGIS-FP BJO5FCBIT3AIGOFI · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Janus-LHC cross sections: wino-like electroweakino pair production at the LHC.
Reference: Resummino (arXiv:2304.11915) tables at 13 and 13.6 TeV. Fast surrogate = cubic interpolation of ln(sigma) vs mass
(monotone, smooth), with a leave-one-out error estimate; sqrt(s) scaling between 13 and 13.6 TeV by a per-mass log-linear law.
How the experiments compute it: Resummino NLO+NLL / aNNLO+NNLL in Mellin space with global PDFs (one run per mass point, minutes);
this surrogate reproduces their table in microseconds and reports its own interpolation error."""
import json, math, pathlib, numpy as np
from scipy.interpolate import CubicSpline
D = json.load(open(pathlib.Path(__file__).with_name('data') / 'wino_xsec_resummino_2304.11915.json'))
M = np.array(D['mass_GeV'], float)
def _spl(sqrts, proc, drop=None):
    y = np.log(np.array(D['sqrt_s'][sqrts][proc], float)); x = np.log(M)   # ln(sigma) vs ln(m): near power law, flatter to interpolate
    if drop is not None: x = np.delete(x, drop); y = np.delete(y, drop)
    sp = CubicSpline(x, y)
    return lambda m: sp(np.log(m))
PROCS = ('C1N2p', 'C1N2m', 'C1C1')
def _check_proc(proc):
    if proc not in PROCS: raise ValueError(f"unknown process {proc!r}; use one of {', '.join(PROCS)} (chi2^0 chi1^+, chi2^0 chi1^-, chi1^+ chi1^-)")
def sigma(m, proc='C1N2p', sqrts='13.6'):
    """Cross section in fb at mass m (GeV), 100 <= m <= 2000. sqrts '13', '13.6' (table) or a number in [13, 14] (log-linear in sqrt(s))."""
    _check_proc(proc); m = float(m)
    if not (100 <= m <= 2000): raise ValueError('mass outside the 100-2000 GeV reference table')
    if str(sqrts) in D['sqrt_s']: return float(math.exp(_spl(str(sqrts), proc)(m)))
    s = float(sqrts); a, b = math.log(sigma(m, proc, '13')), math.log(sigma(m, proc, '13.6'))
    return float(math.exp(a + (b - a)*(s - 13.0)/0.6))     # log-linear in sqrt(s): an EXTRAPOLATION above 13.6 TeV, labelled as such
KAPPA = -0.16300000003275   # LHC1 (2026-11-18): universal PDF-evolution exponent fitted on the 13 -> 13.6 TeV tables (all 3 processes: -0.161..-0.165)
def sigma_scaling(m, proc='C1N2p', sqrts=14.0):
    _check_proc(proc)
    if not float(sqrts) > 0: raise ValueError('collision energy sqrt(s) must be a positive number of TeV, e.g. 14')
    """Physics route (no PDF file): Drell-Yan scaling s*sigma = Phi(4m^2/s) built from the 13 TeV table, times (sqrt(s)/13)^KAPPA.
    Reproduces the 13.6 TeV table to <=0.3%; at 14 TeV it agrees with the log-linear route to <=1%."""
    t13 = 4*M**2/13000.0**2
    Phi = CubicSpline(np.log(t13), np.log(13.0**2*np.array(D['sqrt_s']['13'][proc], float)))
    rs = float(sqrts); t = 4*float(m)**2/(rs*1000)**2
    if not (t13.min() <= t <= t13.max()): raise ValueError('this mass is outside what the 13 TeV table covers at that energy (roughly 100 GeV to 2 TeV at 13 TeV; the reach scales with the collision energy)')
    return float(math.exp(Phi(math.log(t)))/rs**2*(rs/13.0)**KAPPA)
def sigma_best(m, proc='C1N2p', sqrts=14.0):
    """Best estimate above the tables: mean of the two independent routes (scaling, log-linear) with their spread as the error."""
    a, b = sigma_scaling(m, proc, sqrts), sigma(m, proc, sqrts)
    return {'sigma_fb': (a+b)/2, 'route_spread': abs(a-b)/((a+b)/2), 'scaling': a, 'loglinear': b}
def total(m, sqrts='13.6'):
    return {p: sigma(m, p, sqrts) for p in D['processes']} | {'sum': sum(sigma(m, p, sqrts) for p in D['processes'])}
def loo_error(sqrts='13.6'):
    """Leave-one-out: drop each interior table point, predict it from the rest; max and median relative error."""
    errs = []
    for proc in D['processes']:
        for i in range(1, len(M)-1):
            pred = math.exp(_spl(sqrts, proc, drop=i)(M[i])); true = D['sqrt_s'][sqrts][proc][i]; errs.append(abs(pred/true - 1))
    return {'max': max(errs), 'median': float(np.median(errs)), 'n': len(errs)}
def events(m, lumi_fb, sqrts='13.6', eff=1.0):
    """Expected produced pairs (all three processes) for an integrated luminosity in fb^-1 and an efficiency."""
    return total(m, sqrts)['sum']*lumi_fb*eff
