"""Median engine: evaluates every sector at ONE shared centre (theory/median/centre.json) and reports each sector's strain
(pull in units of its tolerance). The 'arrow' = the free shared parameters fitted to minimise total strain. No per-sector knobs."""
import json, math, sys
import numpy as np
from scipy.optimize import minimize_scalar
OBS = dict(mmu_mtau=105.658/1776.86, me_mtau=0.51100/1776.86, u_d=0.0457, u_u=0.00311, nu_step=math.exp(-9*math.pi/8))
L3 = math.log(3)
def sectors(c, u):
    a = c['electron_corner_amp']; r = c['lepton_rungs']
    m = np.array([a * u**r[0], u**r[1], u**r[2]])                       # e, mu, tau (tau = 1)
    Q = m.sum() / np.sqrt(m).sum()**2
    return {'lepton m_mu/m_tau': math.log(m[1]/OBS['mmu_mtau'])/L3,
            'lepton m_e/m_tau': math.log(m[0]/OBS['me_mtau'])/L3,
            'Koide Q (1% tol)': (Q - 2/3)/(0.01*2/3),
            'neutrino step = u*': math.log(u/OBS['nu_step'])/L3,
            'down-quark step = u*': math.log(u/OBS['u_d'])/L3,
            'Delta_3 (tol 0.05)': c['delta3_residual']/0.05,
            'thread alpha drift (bound 1.66e-6)': math.log10(c['thread_zeta_alpha']/1.66e-6) if c['thread_zeta_alpha'] > 1.66e-6 else 0.0}
REPORT_ONLY = {'up-quark step = u*': lambda u: math.log(u/OBS['u_u'])/L3}
def total(c, u): return sum(v*v for v in sectors(c, u).values())
def run(path='theory/median/centre.json'):
    c = json.load(open(path))
    res = minimize_scalar(lambda lu: total(c, math.exp(lu)), bounds=(math.log(1e-3), math.log(0.3)), method='bounded')
    u = math.exp(res.x); s = sectors(c, u)
    print('arrow: u* = %.4f (centre file %.4f)   total strain chi2 = %.2f over %d sectors' % (u, c['u_star'], total(c, u), len(s)))
    for k, v in sorted(s.items(), key=lambda kv: -abs(kv[1])): print('  %-38s strain %+6.2f %s' % (k, v, '<-- over 1' if abs(v) > 1 else ''))
    for k, f in REPORT_ONLY.items(): print('  [report only] %-24s strain %+6.2f' % (k, f(u)))
    return u, s
if __name__ == '__main__': run(*sys.argv[1:])
