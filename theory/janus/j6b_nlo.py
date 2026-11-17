"""J6b (locked PREREG_J6b_deltaN_NLO): NLO delta-N r. Formulas: Byrnes & Wands astro-ph/0605679 Eqs 43-45, 81; see lock."""
import sys, numpy as np; sys.path.insert(0, '.'); sys.argv = ['x']
import importlib.util
spec = importlib.util.spec_from_file_location('j6', 'theory/janus/j6_deltaN.py')
src = open('theory/janus/j6_deltaN.py').read().split('L = []')[0]   # reuse functions only, no J6 rerun
ns = {}; exec(compile(src, 'j6_funcs', 'exec'), ns)
deltaN = ns['deltaN']; from tools.janus_calc import core
C = 2 - np.log(2) - 0.5772156649015329
def rNLO(V, g, H2, f, h=1e-3):
    d = deltaN(V, g, H2, np.array(f, float), h); f = np.array(f, float)
    v = -np.array(g(f))/V(f); eps = 0.5*v @ v; H2v = V(f)/(3-eps)
    sh = v/np.linalg.norm(v); n = len(f)
    eta = H2(f)/(3*H2v)
    M = np.eye(n)*(1 + (-2+2*C)*eps) + 4*C*eps*np.outer(sh, sh) - 2*C*eta
    NMN = d['Na'] @ M @ d['Na']
    return 8*(1 + (-2+2*C)*eps)/NMN, d['r'], d['N']
L = []; P = lambda s: (L.append(s), print(s, flush=True))
V1 = lambda f: 0.5*f[0]**2; g1 = lambda f: [f[0]]; H1 = lambda f: np.array([[1.0]])
r1, r1lo, N1 = rNLO(V1, g1, H1, [15.3])
m = core.Model(lambda p: 0.5*p*p, lambda p: p, 30.0); rc = m.spectra(N1)['r']
T1 = abs(r1-rc)/rc < 1e-3
P(f"T1b m^2phi^2 N*={N1:.3f}: r_LO {r1lo:.6f}  r_NLO {r1:.6f}  calculator {rc:.6f}  rel {abs(r1-rc)/rc:.1e} -> {'PASS' if T1 else 'FAIL'}")
V2 = lambda f: 0.5*(f[0]**2+f[1]**2); g2 = lambda f: [f[0], f[1]]; H22 = lambda f: np.eye(2)
rs = [rNLO(V2, g2, H22, [15.3*np.cos(t), 15.3*np.sin(t)])[0] for t in [0.1, 0.5, 0.9, 1.3]]
sp = (max(rs)-min(rs))/r1; dd = max(abs(x-r1) for x in rs)/r1; T2 = sp < 1e-6 and dd < 1e-6
P(f"T2b equal mass r_NLO {['%.7f' % x for x in rs]} spread {sp:.1e} vs single {dd:.1e} -> {'PASS' if T2 else 'FAIL'}")
R = 1/9; V3 = lambda f: 0.5*f[0]**2 + 0.5*R*R*f[1]**2; g3 = lambda f: [f[0], R*R*f[1]]; H3 = lambda f: np.diag([1.0, R*R])
r3, r3lo, N3 = rNLO(V3, g3, H3, [8.2, 12.9])
P(f"T3b VW R=1/9 (8.2,12.9) N={N3:.3f}: r_LO {r3lo:.5f} r_NLO {r3:.5f} ratio {r3/r3lo:.5f} (record only)")
P(f"J6b verdict: {'VALIDATED' if (T1 and T2) else 'NOT VALIDATED'}")
open('field_tests/results/janus_j6b_nlo.txt', 'w').write('\n'.join(L)+'\n')
