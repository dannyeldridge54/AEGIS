"""JANUS tick 15: exact MS (repo engine) on the rho offset model, (C, phi*) solved to A1's (n_s, r) (see PREREG)."""
import json, math, sys, time
sys.path.insert(0, 'apps/aegis_studio/engine')
from tools.serapis_calc.ms import Background, spectra
from scipy.special import zeta
A, D0, B0 = 2*zeta(4), math.pi*zeta(3), 1-5.783341757348703
NS, R, AEX = 0.974393, 4.82095e-4, -9.9814e-4
T0 = time.time()
def make(C, B, D):
    s2 = math.sqrt(2)
    def E1(p): y = math.exp(s2*p); return A*y*y + B + D/y, y
    def V(p): e, y = E1(p); return (1 - 1/e)*(1 + C*(e-1))
    def dV(p):
        e, y = E1(p); de = (2*A*y*y - D/y)*s2          # dE1/dphi
        return (de/e**2)*(1 + C*(e-1)) + (1 - 1/e)*C*de
    return V, dV
def obs(C, ystar, B, D):
    V, dV = make(C, B, D); ps = math.log(ystar)/math.sqrt(2)
    bg = Background(V, dV, ps + 0.3)
    Nend = bg.Nend if hasattr(bg, 'Nend') else bg.N_end
    import numpy as np
    from scipy.optimize import brentq
    Nst = brentq(lambda N: bg.state(N)[0] - ps, 0.0, Nend - 1e-6)
    s = spectra(bg, Nend - Nst)
    return s['n_s'], s['r'], s['alpha_s'], Nend - Nst
def solve(B, D, C, y):
    hist = []
    for it in range(6):
        if time.time() - T0 > 150: return dict(converged=False, reason='time', hist=hist)
        ns, r, a, Ns = obs(C, y, B, D); hist.append([C, y, ns, r, a, Ns])
        if abs(ns-NS) < 2e-6 and abs(r/R-1) < 2e-4: return dict(converged=True, C=C, y_star=y, ns=ns, r=r, alpha=a, Nstar=Ns, err=a/AEX-1, hist=hist)
        hC, hy = C*1e-3, y*1e-4
        n1, r1, _, _ = obs(C+hC, y, B, D); n2, r2, _, _ = obs(C, y+hy, B, D)
        J = [[(n1-ns)/hC, (n2-ns)/hy], [(r1-r)/hC, (r2-r)/hy]]
        f = [NS-ns, R-r]; det = J[0][0]*J[1][1]-J[0][1]*J[1][0]
        C += (f[0]*J[1][1]-J[0][1]*f[1])/det; y += (J[0][0]*f[1]-J[1][0]*f[0])/det
    return dict(converged=False, reason='iterations', hist=hist)
full = solve(B0, D0, 1.255e-6, 14.818)
pure = solve(0.0, 0.0, 1.248e-6, 14.613) if time.time()-T0 < 120 else dict(converged=False, reason='time')
out = dict(full=full, pure_plateau=pure, seconds=time.time()-T0)
out['verdict'] = ('PASS' if abs(full['err']) < 0.01 else 'FAIL') if full.get('converged') else 'no result'
json.dump(out, open(sys.argv[1], 'w'), indent=1, default=float); print(json.dumps({k: (v if k != 'full' and k != 'pure_plateau' else {kk: vv for kk, vv in v.items() if kk != 'hist'}) for k, v in out.items()}, indent=1, default=float))
