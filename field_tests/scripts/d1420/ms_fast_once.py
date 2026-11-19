"""JANUS tick 17: one spectra_fast evaluation of the rho offset model at D1415's point, timed (see PREREG)."""
import json, math, sys, time
sys.path.insert(0, 'apps/aegis_studio/engine')
from tools.serapis_calc.ms import Background, spectra_fast
from scipy.special import zeta
from scipy.optimize import brentq
A, D0, B0 = 2*zeta(4), math.pi*zeta(3), 1-5.783341757348703
C, ystar = 1.255e-6, 14.818
s2 = math.sqrt(2)
def E1(p): y = math.exp(s2*p); return A*y*y + B0 + D0/y, y
def V(p): e, y = E1(p); return (1 - 1/e)*(1 + C*(e-1))
def dV(p):
    e, y = E1(p); de = (2*A*y*y - D0/y)*s2
    return (de/e**2)*(1 + C*(e-1)) + (1 - 1/e)*C*de
t0 = time.time()
ps = math.log(ystar)/s2
bg = Background(V, dV, ps + 0.3)
Nst = brentq(lambda N: bg.state(N)[0] - ps, 0.0, bg.Nend - 1e-6)
s = spectra_fast(bg, bg.Nend - Nst)
dt = time.time() - t0
out = dict(ns=s['ns'], r=s['r'], alpha_s=s['alpha_s'], Nstar=bg.Nend - Nst, Nend=bg.Nend, seconds=dt,
           dns_vs_A1=s['ns']-0.974393, dr_rel_vs_A1=s['r']/4.82095e-4-1, alpha_vs_A1_exact=s['alpha_s']/-9.9814e-4-1,
           label='fast (< 20 s)' if dt < 20 else 'slow')
json.dump(out, open(sys.argv[1], 'w'), indent=1, default=float); print(json.dumps(out, indent=1, default=float))
