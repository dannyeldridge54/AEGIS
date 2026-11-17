"""A1 — wino CMB annihilation vs Planck 2018 (PREREG_A1_wino_cmb.md)."""
import math, numpy as np, sys
sys.path.insert(0, '.')
from tools.janus_astro.sommerfeld import wino_s, ALPHA_W
CONV = 0.389379e-27 * 2.99792458e10          # GeV^-2 -> cm^3/s
PANN = 3.2e-28; FE = (0.14, 0.41)
def sv(M, s):
    G = math.pi*ALPHA_W**2/(2*M*M)*np.array([[2, math.sqrt(2)], [math.sqrt(2), 3]])
    s = np.asarray(s, float); return 2*s@G@s*CONV
out = []
t1 = abs(sv(1000, (1, 0))/(2*math.pi*ALPHA_W**2/1e6*CONV) - 1); T1 = t1 < 1e-12
out.append(f"T1 convention rel err {t1:.2e} -> {'PASS' if T1 else 'FAIL'}")
a = sv(2900, wino_s(2900, v=1e-3)); T2 = 5e-26 <= a <= 2e-24
out.append(f"T2 sv_tot(2.9 TeV, v=1e-3) = {a:.3e} cm3/s, band [5e-26,2e-24] -> {'PASS' if T2 else 'FAIL'}")
Ms = sorted(set(np.round(np.r_[np.arange(500, 3501, 100), np.arange(2300, 2501, 20)], 6)))
rows = []
for M in Ms:
    s7 = sv(M, wino_s(M, v=1e-7)); s6 = sv(M, wino_s(M, v=1e-6))
    p = [f*s7/M for f in FE]
    rows.append((M, s7, s6/s7 if s7 else 0, p[0], p[1], math.sqrt(PANN/p[0]), math.sqrt(PANN/p[1])))
    out.append(f"M={M/1e3:.2f} TeV sv7={s7:.3e} sv6/sv7={s6/s7:.3f} pann=[{p[0]:.2e},{p[1]:.2e}] fmax=[{rows[-1][5]:.3f},{rows[-1][6]:.3f}]")
ex_lo = [r[0] for r in rows if r[3] > PANN]; ex_hi = [r[0] for r in rows if r[4] > PANN]
out.append(f"excluded (f_wino=1) at f_eff=0.14: {len(ex_lo)}/{len(rows)} masses; at f_eff=0.41: {len(ex_hi)}/{len(rows)}")
out.append(f"allowed masses f_eff=0.41: {[r[0] for r in rows if r[4] <= PANN]}")
out.append(f"allowed masses f_eff=0.14: {[r[0] for r in rows if r[3] <= PANN]}")
out.append("A1 VALIDATED" if (T1 and T2) else "A1 NOT VALIDATED")
open('field_tests/results/a1_wino_cmb.txt', 'w').write("\n".join(out)+"\n"); print("\n".join(out))
