# AEGIS-FP FADFNMG2JGQK7DWK · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""J6d (locked PREREG_J6d_large_fNL_slices)."""
import sys, numpy as np; sys.path.insert(0, '.')
from scipy.integrate import solve_ivp
src = open('theory/janus/j6c_large_fnl.py').read().split('L = []')[0]; ns = {}; exec(compile(src, 'j6c', 'exec'), ns)
mk, fnl_eq21 = ns['mk'], ns['fnl_eq21']
def traj(V, g, f, rho_c=None, Nmax=200):
    f = np.array(f, float)
    def rhs(N, u):
        x, xn = u[:2], u[2:]; e = 0.5*xn @ xn
        return np.concatenate([xn, -(3-e)*xn - (3-e)*np.array(g(x))/V(x)])
    rho = lambda N, u: 3*V(u[:2])/(3 - 0.5*u[2:] @ u[2:]) - rho_c
    ev = [rho] if rho_c is not None else []
    for e_ in ev: e_.terminal = True; e_.direction = -1
    return solve_ivp(rhs, [0, Nmax], np.concatenate([f, -np.array(g(f))/V(f)]), events=ev or None,
                     rtol=1e-11, atol=1e-13, dense_output=True)
def Nc(V, g, f, rc): s = traj(V, g, f, rc); return s.t_events[0][0]
def fnl(V, g, f, hs, rc):
    E = np.diag(hs); N = lambda x: Nc(V, g, x, rc); N0 = N(f)
    Na = np.array([(N(f+E[a]) - N(f-E[a]))/(2*hs[a]) for a in range(2)]); Nab = np.zeros((2, 2))
    for a in range(2): Nab[a, a] = (N(f+E[a]) - 2*N0 + N(f-E[a]))/hs[a]**2
    Nab[0, 1] = Nab[1, 0] = (N(f+E[0]+E[1]) - N(f+E[0]-E[1]) - N(f-E[0]+E[1]) + N(f-E[0]-E[1]))/(4*hs[0]*hs[1])
    return 5/6*(Na @ Nab @ Na)/(Na @ Na)**2
L = []; P = lambda s: (L.append(s), print(s, flush=True)); ok7 = ok8 = True; big = False
for name, lam, p in [('A1', 0.05, 1e-3), ('A2', 0.04, 1e-3), ('A3', 0.05, 1e-4)]:
    V, g = mk(lam); fs = np.array([p, 16.0]); s0 = traj(V, g, fs, Nmax=80)
    for Ncut in (30, 45, 55):
        u = s0.sol(Ncut); fe = u[:2]; rc = 3*V(fe)/(3 - 0.5*u[2:] @ u[2:])
        fa = fnl(V, g, fs, [p/10, 1e-3], rc); fb = fnl(V, g, fs, [p/20, 5e-4], rc); fan = fnl_eq21(lam, fs, fe)
        t7 = abs(fb - fan) < max(0.10*abs(fan), 0.02); t8 = abs(fa - fb) < max(2e-2*abs(fb), 1e-3)
        ok7 &= t7; ok8 &= t8; big |= abs(fb) >= 1
        P(f"{name} lam={lam} phi*={p:g} N_c={Ncut}: slice at ({fe[0]:.4g},{fe[1]:.4g}) | f_NL num {fb:.5g} (h {fa:.5g}) | Eq21 {fan:.5g} | T7 {'PASS' if t7 else 'FAIL'} T8 {'PASS' if t8 else 'FAIL'}")
v = 'VALIDATED' if (ok7 and ok8 and big) else ('NOT VALIDATED' if not (ok7 and ok8) else 'INCONCLUSIVE')
P(f"T7L: {'PASS' if big else 'FAIL'}  ->  J6d verdict: {v}")
open('field_tests/results/janus_j6d_slices.txt', 'w').write('\n'.join(L)+'\n')
