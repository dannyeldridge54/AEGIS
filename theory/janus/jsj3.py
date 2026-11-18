"""JSJ3 (locked PREREG_JSJ3_dop853)."""
import sys, time, math, subprocess, numpy as np, sympy as sp, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
src = open('theory/janus/j7m_grid.py').read(); exec(src.split("L = []; D = {k:")[0])
from tools.janus_calc.core_jit import build8, ModelJ, spectra3_jit
from tools.serapis_calc.ms_jit import build as bms, spectra_msjit
y = sp.Symbol('y')
def sym(i):
    kind, a, b = PTS[i-1]; a, b = sp.nsimplify(a), sp.nsimplify(b)
    return 1 - sp.cos(y/b) + a*sp.sin(y/b)**2 if kind == 'TI' else 1 - (1 - y/b)**a
L = []; ok = True; ptm = []; pmm = []; ec = []; ej = []
for i in (1, 2, 3, 4, 5, 6, 11, 12):
    name, V, dV, y0, m = build(i); mj = build8(sym(i), y); M = ModelJ(mj, y0, 4000.0); spectra3_jit(M, 55.0); ms = bms(sym(i), y)
    tb = []; tp = []
    for _ in range(10):
        t = time.perf_counter(); M = ModelJ(mj, y0, 4000.0); tb.append(time.perf_counter() - t)
        t = time.perf_counter(); spectra3_jit(M, 50.0); tp.append(time.perf_counter() - t)
    ptm.append(np.median(tp)); pmm.append(np.median(tb) + 2*np.median(tp))
    for N in (50.0, 60.0):
        a = spectra3(m, N); b = spectra3_jit(M, N); ex = spectra_msjit(ms, y0, N, dlnk=DL, bd=1000.0, rtol=1e-11)['ns']
        d = (abs(a['ns'] - b['ns']), abs(b['r']/a['r'] - 1), abs(a['alpha_s'] - b['alpha_s'])); o = d[0] <= 1e-7 and d[1] <= 1e-6 and d[2] <= 1e-7; ok &= o
        ec.append(abs(a['ns'] - ex)); ej.append(abs(b['ns'] - ex))
        L.append(f"{name:16s} N*={N:.0f}: |dn_s| {d[0]:.1e} |dr/r| {d[1]:.1e} |da| {d[2]:.1e} {o} | vs exact core {ec[-1]:.1e} jit8 {ej[-1]:.1e}"); print(L[-1], flush=True)
    L.append(f"  {name}: build {np.median(tb)*1e3:.3f} ms, point {np.median(tp)*1e3:.3f} ms (medians of 10)"); print(L[-1], flush=True)
ta = []; t0 = []
for _ in range(5):
    t = time.perf_counter(); subprocess.run(['theory/janus/aspic/j7m_aspic'], capture_output=True); ta.append(time.perf_counter() - t)
    t = time.perf_counter(); subprocess.run(['/bin/true']); t0.append(time.perf_counter() - t)
asp = (min(ta) - min(t0))/24
JS1 = ok and abs(np.median(ej) - np.median(ec)) <= 1e-7; JS3 = bool(np.median(ptm) <= asp); JS4 = bool(np.median(pmm) <= 2*asp)
L.append(f"median vs exact: core {np.median(ec):.2e}, jit8 {np.median(ej):.2e}")
L.append(f"per point: janus-jit8 {np.median(ptm)*1e3:.3f} ms vs ASPIC {asp*1e3:.3f} ms -> {'FASTER' if JS3 else 'NOT faster'} | per model (build + 2 points): {np.median(pmm)*1e3:.3f} ms vs ASPIC {2*asp*1e3:.3f} ms -> {'FASTER' if JS4 else 'NOT faster'}")
L.append(f"JS1 {JS1} JS3 {JS3} JS4 {JS4} -> " + ("build8 is the janus-jit default" if JS1 else "build8 NOT adopted"))
open('field_tests/results/jsj3.txt', 'w').write('\n'.join(L) + '\n'); print('\n'.join(L[-3:]))
