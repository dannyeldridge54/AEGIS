"""JMF12 (locked PREREG_JMF12_ncjit)."""
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
CASES = {'a DoubleQuadNC R=1': (Vq, [[1, 0], [0, sp.sin(f[0])**2]], np.array([0.4, 26.0]), 'pyt'),
         'b flat Q3': (F(m1)/2*f[0]**2 + F(m2)/2*f[1]**2, [[1, 0], [0, 1]], np.array([12.0, 12.0]), 'flat'),
         'c sphere R=2': (Vq, [[4, 0], [0, 4*sp.sin(f[0])**2]], np.array([0.4, 26.0]), 'pyt')}
L = []; ok = True; spd = []
for nm, (Vx, Gx, fi, ic) in CASES.items():
    ms = bsym(Vx, Gx, f); fd = sr_pyt(ms, fi) if ic == 'pyt' else sr_flat(Vf, gf, fi)
    t = time.time(); a = spectra_nc(ms, fi, fd); ta = time.time() - t
    mj = bjit(Vx, Gx, f); spectra_ncjit(mj, fi, fd)
    t = time.time(); b = spectra_ncjit(mj, fi, fd); tb = time.time() - t
    d = abs(a['ns'] - b['ns']); o = d <= 1e-6; ok &= o; spd.append(ta/tb)
    L.append(f"{nm}: ref n_s {a['ns']:.8f} N_tot {a['Ne']:.4f} ({ta:.1f} s) | nc-jit {b['ns']:.8f} N_tot {b['Ne']:.4f} ({tb:.2f} s, x{ta/tb:.0f}) |dn_s| {d:.1e} {o}")
    print(L[-1], flush=True)
K1 = ok and bool(np.median(spd) >= 20)
L.append(f"median speed-up x{np.median(spd):.0f} | K1 {K1} -> {'ADOPTED (curved-space PC default, nc-jit)' if K1 else 'NOT ADOPTED'}")
open('field_tests/results/janus_jmf12.txt', 'w').write('\n'.join(L) + '\n'); print(L[-1])
