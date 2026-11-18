import sys, time, math, numpy as np, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
import importlib.util
from tools.janus_lt.background import Cosmo
from tools.janus_lt import recomb as NEW
spec = importlib.util.spec_from_file_location('recomb_ref', 'field_tests/scripts/recomb_ref_u4.py'); OLD = importlib.util.module_from_spec(spec); spec.loader.exec_module(OLD)
from tools.janus_lt.desi import chi2 as chi2_bao, load
src = open('theory/janus_lt/l0b_check.py').read().split('rng = ')[0]; ns = {}; exec(compile(src, 'l0b', 'exec'), ns); r_d = ns['r_d']
mu = np.array([0.01041, 0.02223, 0.14208]); Cm = 1e-9*np.array([[0.006621, 0.12444, -1.1929], [0.12444, 21.344, -94.001], [-1.1929, -94.001, 1488.4]]); Ci = np.linalg.inv(Cm); rows = load()
pts = [(0.02223, 0.14208), (0.02223 - 5.84e-4, 0.14208 - 4.88e-3), (0.02223 + 5.84e-4, 0.14208 + 4.88e-3), (0.02223 - 5.84e-4, 0.14208 + 4.88e-3), (0.02240, 0.1420)]
ok = [True]*4; to = tn = 0
for wb, wbc in pts:
    c = Cosmo(67.5, wb, wbc - wb, mnu=0.06)
    t = time.time(); ro = OLD.Recomb(c, wb, YHe=0.24); zso, zdo = ro.z_star(), ro.z_drag(); dto = time.time() - t
    t = time.time(); rn = NEW.Recomb(c, wb, YHe=0.24); zsn, zdn = rn.z_star(), rn.z_drag(); dtn = time.time() - t; to += dto; tn += dtn
    t1 = abs(zsn - zso) <= 1e-6 and abs(zdn - zdo) <= 1e-6; ok[1] &= t1
    def chi(zs, zd):
        cc = Cosmo(67.7, wb, wbc - wb, mnu=0.0588); th = r_d(cc, wb, zs)/cc.DM(zs); rd = r_d(cc, wb, zd); d = np.array([th, wb, wbc]) - mu
        return chi2_bao(cc, rd, rows) + float(d @ Ci @ d)
    x0, x1 = chi(zso, zdo), chi(zsn, zdn); t3 = abs(x1 - x0) <= 1e-8*max(1, abs(x0)); ok[3] &= t3
    print(f"ω_b {wb:.5f} ω_bc {wbc:.5f}: z* {zso:.7f} → {zsn:.7f} (Δ {zsn-zso:+.1e}), z_d {zdo:.7f} → {zdn:.7f} (Δ {zdn-zdo:+.1e}) | {dto:.2f}s → {dtn:.2f}s (×{dto/dtn:.1f}) | χ² {x0:.8f} → {x1:.8f} | T1 {t1} T3 {t3}", flush=True)
ok[2] = to/tn >= 5
print(f"total {to:.1f}s → {tn:.1f}s (×{to/tn:.1f}); U4 VERDICT: T1 {'PASS' if ok[1] else 'FAIL'} T2 {'PASS' if ok[2] else 'FAIL'} T3 {'PASS' if ok[3] else 'FAIL'}" + (' → ADOPT' if all(ok[1:]) else ' → not adopted'))
