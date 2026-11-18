"""MSJ1 (locked PREREG_MSJ1_msjit)."""
import sys, time, math, numpy as np, sympy as sp, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
src = open('theory/janus/j7m_grid.py').read(); exec(src.split("L = []; D = {k:")[0])
from tools.serapis_calc.ms_jit import build as bj, spectra_msjit
y = sp.Symbol('y')
def sym(i):
    kind, a, b = PTS[i-1]; a, b = sp.nsimplify(a), sp.nsimplify(b)
    if kind == 'TI': return 1 - sp.cos(y/b) + a*sp.sin(y/b)**2
    return 1 - (1 - y/b)**a
L = []; ok = True; spd = []
for i in (1, 2, 3, 4, 5, 6, 11, 12):
    name, V, dV, y0, m = build(i); bg = Background(V, dV, y0, Nmax=4000); mj = bj(sym(i), y); spectra_msjit(mj, y0, 55.0, dlnk=DL, bd=1000.0, rtol=1e-11)
    for N in (50.0, 60.0):
        t = time.time(); a = spectra_fast(bg, N, dlnk=DL, bd=1000.0); ta = time.time() - t
        t = time.time(); b = spectra_msjit(mj, y0, N, dlnk=DL, bd=1000.0, rtol=1e-11); tb = time.time() - t
        d = (abs(a['ns'] - b['ns']), abs(b['r']/a['r'] - 1), abs(a['alpha_s'] - b['alpha_s'])); o = d[0] <= 1e-7 and d[1] <= 1e-6 and d[2] <= 1e-7; ok &= o; spd.append(ta/tb)
        L.append(f"{name:16s} N*={N:.0f}: ref {a['ns']:.9f} ({ta:.1f} s) | ms-jit |dn_s| {d[0]:.1e} |dr/r| {d[1]:.1e} |da| {d[2]:.1e} ({tb:.2f} s, x{ta/tb:.0f}) {o}"); print(L[-1], flush=True)
M1 = ok and bool(np.median(spd) >= 10)
L.append(f"median speed-up x{np.median(spd):.0f} | M1 {M1} -> {'ADOPTED (ms-jit)' if M1 else 'NOT ADOPTED'}")
open('field_tests/results/msj1.txt', 'w').write('\n'.join(L) + '\n'); print(L[-1])
