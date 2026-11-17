"""J6c (locked PREREG_J6c_large_fNL): Janus delta-N vs Byrnes-Choi-Hall 0807.1101 Eq. 21 (Example A)."""
import sys, numpy as np; sys.path.insert(0, '.')
from tools.serapis_calc.multifield import run
def mk(lam):
    V = lambda f: 0.5*np.exp(-lam*f[0]**2)*f[1]**2
    g = lambda f: [-lam*f[0]*np.exp(-lam*f[0]**2)*f[1]**2, np.exp(-lam*f[0]**2)*f[1]]
    return V, g
def Nend(V, g, f):
    f = np.array(f, float); s, Ne = run(V, g, f, Nmax=400, v0=-np.array(g(f))/V(f)); return Ne, s
def fnl_num(V, g, f, hs):
    f = np.array(f, float); E = np.diag(hs); N = lambda x: Nend(V, g, x)[0]; N0 = N(f)
    Na = np.array([(N(f+E[a]) - N(f-E[a]))/(2*hs[a]) for a in range(2)]); Nab = np.zeros((2, 2))
    for a in range(2): Nab[a, a] = (N(f+E[a]) - 2*N0 + N(f-E[a]))/hs[a]**2
    Nab[0, 1] = Nab[1, 0] = (N(f+E[0]+E[1]) - N(f+E[0]-E[1]) - N(f-E[0]+E[1]) + N(f-E[0]-E[1]))/(4*hs[0]*hs[1])
    S = Na @ Na; return N0, 5/6*(Na @ Nab @ Na)/S**2, 8/S
def fnl_eq21(lam, fs, fe):
    ep = lambda f: 0.5*(2*lam*f[0])**2; ec = lambda f: 0.5*(2/f[1])**2       # Eq. 24: U_phi/U = -2 lam phi, V_chi/V = 2/chi
    epf, ecf = ep(fs), ec(fs); epe, ece = ep(fe), ec(fe); ee = epe + ece
    hpp = lambda f: -2*lam + 4*lam*lam*f[0]**2; hcc = lambda f: 2/f[1]**2           # Eq. 25: U_pp/U, V_cc/V
    u, v = epe/ee, ece/ee                                                            # Eq. 18
    eh = (ece*hpp(fe) + epe*hcc(fe))/ee                                              # Eq. 22
    AP = -(epe*ece/ee**2)*(eh - 4*epe*ece/ee)                                        # Eq. 23
    D = u*u/epf + v*v/ecf
    return 5/6*2/D**2*(u**3/epf*(1 - hpp(fs)/(2*epf)) + v**3/ecf*(1 - hcc(fs)/(2*ecf)) - (u/epf - v/ecf)**2*AP)
L = []; P = lambda s: (L.append(s), print(s, flush=True)); ok5 = ok6 = True; big = False
for name, lam, p in [('A1', 0.05, 1e-3), ('A2', 0.04, 1e-3), ('A3', 0.05, 1e-4)]:
    V, g = mk(lam); fs = np.array([p, 16.0])
    N0, fa, r = fnl_num(V, g, fs, [p/10, 1e-3]); _, fb, _ = fnl_num(V, g, fs, [p/20, 5e-4])
    Ne, s = Nend(V, g, fs); fe = s.sol(Ne)[:2]; fan = fnl_eq21(lam, fs, fe)
    t5 = abs(fb - fan) < 0.10*abs(fan); t6 = abs(fa - fb)/max(abs(fb), 1e-30) < 2e-2
    ok5 &= t5; ok6 &= t6; big |= abs(fb) >= 1
    P(f"{name} lam={lam} phi*={p:g}: N={N0:.3f} end=({fe[0]:.4g},{fe[1]:.4g}) r={r:.4f} | f_NL num {fb:.5g} (h: {fa:.5g}) | Eq21 {fan:.5g} | rel {abs(fb-fan)/abs(fan):.2e} T5 {'PASS' if t5 else 'FAIL'} T6 {'PASS' if t6 else 'FAIL'}")
v = 'VALIDATED' if (ok5 and ok6 and big) else ('NOT VALIDATED' if not (ok5 and ok6) else 'INCONCLUSIVE')
P(f"T5L (|f_NL|>=1 somewhere): {'PASS' if big else 'FAIL'}  ->  J6c verdict: {v}")
open('field_tests/results/janus_j6c_large_fnl.txt', 'w').write('\n'.join(L)+'\n')
