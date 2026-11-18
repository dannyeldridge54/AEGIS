"""JMF12b (locked PREREG_JMF12b_ncjit)."""
import sys, time, math, numpy as np, sympy as sp; sys.path.insert(0, '.')
from tools.janus_calc.mfms_nc import build as bsym, spectra_nc
from tools.janus_calc.mfms_nc_jit import build as bjit, spectra_ncjit
f = sp.symarray('f', 2); M = 0.5e-6; p = [0.002*M**2, 0.004*M**2, 1.0]; F = sp.Float
Vq = F(p[0])**2/2*f[0]**2 + F(p[1])**2/2*f[1]**2
def sr_pyt(m, fi):   # PyTransport start: fdot = -dV/sqrt(3V) (coordinate components)
    Vi = float(m['V'](fi)); dV = np.array(m['dV'](fi), float).ravel(); return -dV/np.sqrt(3*Vi)
def sr_flat(V, g, x0):
    v0 = -g(x0)/V(x0); e = 0.5*v0 @ v0; return math.sqrt(V(x0)/(3 - e))*v0
m1, m2 = 1e-11, 9e-11; Vf = lambda x: 0.5*m1*x[0]**2 + 0.5*m2*x[1]**2; gf = lambda x: np.array([m1*x[0], m2*x[1]])
CASES = {'d R=0.7': (Vq, [[F(0.49), 0], [0, F(0.49)*sp.sin(f[0])**2]], np.array([0.4, 26.0]), 'pyt'),
         'e R=1.5': (Vq, [[F(2.25), 0], [0, F(2.25)*sp.sin(f[0])**2]], np.array([0.4, 26.0]), 'pyt'),
         'f R=1 start (0.6,24)': (Vq, [[1, 0], [0, sp.sin(f[0])**2]], np.array([0.6, 24.0]), 'pyt')}
L = []; ok = True; spd = []
for nm, (Vx, Gx, fi, ic) in CASES.items():
    ms = bsym(Vx, Gx, f); fd = sr_pyt(ms, fi) if ic == 'pyt' else sr_flat(Vf, gf, fi)
    t = time.time(); a = spectra_nc(ms, fi, fd); ta = time.time() - t
    mj = bjit(Vx, Gx, f); spectra_ncjit(mj, fi, fd)
    t = time.time(); b = spectra_ncjit(mj, fi, fd); tb = time.time() - t
    if not (0.8 <= a['ns'] <= 1.1):
        L.append(f"{nm}: reference n_s {a['ns']:.4f} outside [0.8, 1.1] -> LISTED (gate), nc-jit gave {b['ns']:.4f}"); print(L[-1], flush=True); continue
    d = abs(a['ns'] - b['ns']); o = d <= 1e-6; ok &= o; spd.append(ta/tb)
    L.append(f"{nm}: ref n_s {a['ns']:.8f} N_tot {a['Ne']:.4f} ({ta:.1f} s) | nc-jit {b['ns']:.8f} N_tot {b['Ne']:.4f} ({tb:.2f} s, x{ta/tb:.0f}) |dn_s| {d:.1e} {o}")
    print(L[-1], flush=True)
K1 = ok and len(spd) >= 2 and bool(np.median(spd) >= 20)
L.append(f"gated in {len(spd)}; median speed-up x{(np.median(spd) if spd else 0):.0f} | K1b {K1} -> " + ('INCONCLUSIVE' if len(spd) < 2 else ('ADOPTED (curved-space PC default, nc-jit)' if K1 else 'NOT ADOPTED')))
open('field_tests/results/janus_jmf12b.txt', 'w').write('\n'.join(L) + '\n'); print(L[-1])
