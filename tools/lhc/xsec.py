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
def sigma(m, proc='C1N2p', sqrts='13.6'):
    """Cross section in fb at mass m (GeV), 100 <= m <= 2000. sqrts '13', '13.6' (table) or a number in [13, 14] (log-linear in sqrt(s))."""
    m = float(m)
    if not (100 <= m <= 2000): raise ValueError('mass outside the 100-2000 GeV reference table')
    if str(sqrts) in D['sqrt_s']: return float(math.exp(_spl(str(sqrts), proc)(m)))
    s = float(sqrts); a, b = math.log(sigma(m, proc, '13')), math.log(sigma(m, proc, '13.6'))
    return float(math.exp(a + (b - a)*(s - 13.0)/0.6))     # log-linear in sqrt(s): an EXTRAPOLATION above 13.6 TeV, labelled as such
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
