"""JSJ2 (locked PREREG_JSJ2_corejit)."""
import sys, time, math, subprocess, numpy as np, sympy as sp, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
src = open('theory/janus/j7m_grid.py').read(); exec(src.split("L = []; D = {k:")[0])
from tools.janus_calc.core_jit import build as bj, ModelJ, spectra3_jit
from tools.serapis_calc.ms_jit import build as bms, spectra_msjit
y = sp.Symbol('y')
def sym(i):
    kind, a, b = PTS[i-1]; a, b = sp.nsimplify(a), sp.nsimplify(b)
    return 1 - sp.cos(y/b) + a*sp.sin(y/b)**2 if kind == 'TI' else 1 - (1 - y/b)**a
L = []; ok = True; rat = []; pt = []; ec = []; ej = []; perm = []
for i in (1, 2, 3, 4, 5, 6, 11, 12):
    name, V, dV, y0, _ = build(i); mj = bj(sym(i), y); M0 = ModelJ(mj, y0, 4000.0); spectra3_jit(M0, 55.0); ms = bms(sym(i), y)
    t = time.perf_counter(); m = Model(V, dV, y0, Nmax=4000); a = {N: spectra3(m, N) for N in (50.0, 60.0)}; tc = time.perf_counter() - t
    t = time.perf_counter(); M = ModelJ(mj, y0, 4000.0); tbuild = time.perf_counter() - t; b = {}
    for N in (50.0, 60.0):
        t = time.perf_counter(); b[N] = spectra3_jit(M, N); pt.append(time.perf_counter() - t)
    tj = tbuild + pt[-1] + pt[-2]; rat.append(tc/tj); perm.append(tj)
    for N in (50.0, 60.0):
        ex = spectra_msjit(ms, y0, N, dlnk=DL, bd=1000.0, rtol=1e-11)['ns']
        d = (abs(a[N]['ns'] - b[N]['ns']), abs(b[N]['r']/a[N]['r'] - 1), abs(a[N]['alpha_s'] - b[N]['alpha_s'])); o = d[0] <= 1e-7 and d[1] <= 1e-6 and d[2] <= 1e-7; ok &= o
        ec.append(abs(a[N]['ns'] - ex)); ej.append(abs(b[N]['ns'] - ex))
        L.append(f"{name:16s} N*={N:.0f}: |dn_s| {d[0]:.1e} |dr/r| {d[1]:.1e} |da| {d[2]:.1e} {o} | vs exact: core {ec[-1]:.1e} jit {ej[-1]:.1e}"); print(L[-1], flush=True)
    L.append(f"  {name}: core build+2 pts {tc*1e3:.1f} ms | jit build {tbuild*1e3:.2f} ms + pts {pt[-2]*1e3:.3f}, {pt[-1]*1e3:.3f} ms -> x{tc/tj:.0f}"); print(L[-1], flush=True)
ta = []
for _ in range(5):
    t = time.perf_counter(); subprocess.run(['theory/janus/aspic/j7m_aspic'], capture_output=True); ta.append(time.perf_counter() - t)
t0 = []
for _ in range(5):
    t = time.perf_counter(); subprocess.run(['/bin/true']); t0.append(time.perf_counter() - t)
asp = (min(ta) - min(t0))/24
JS1 = ok and abs(np.median(ej) - np.median(ec)) <= 1e-7; JS2 = bool(np.median(rat) >= 20); JS3 = bool(np.median(pt) <= asp)
L.append(f"median vs exact: core {np.median(ec):.2e}, jit {np.median(ej):.2e} | median speed-up vs core x{np.median(rat):.0f}")
L.append(f"per point: janus-jit median {np.median(pt)*1e3:.3f} ms vs ASPIC {asp*1e3:.3f} ms | per model (build + 2 points): janus-jit median {np.median(perm)*1e3:.2f} ms vs ASPIC {2*asp*1e3:.3f} ms")
JS4 = bool(np.median(perm) <= 2*asp)
L.append(f"JS4 per model: {'FASTER' if JS4 else 'NOT faster'} than ASPIC")
L.append(f"JS1 {JS1} JS2 {JS2} JS3 {JS3} -> " + ("janus-jit ADOPTED" if JS1 and JS2 else "NOT ADOPTED") + f"; per point {'FASTER' if JS3 else 'NOT faster'} than ASPIC")
open('field_tests/results/jsj2.txt', 'w').write('\n'.join(L) + '\n'); print('\n'.join(L[-4:]))
