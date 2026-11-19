"""D1641 / Janus genesis G1b: V''/V_inf at rho vs (D-2)/32; isotropy of E's Hessian at rho (PREREG_D1641_G1B_RHO_CURVATURE)."""
import json, sys
sys.path.insert(0, '.')
import mpmath as mp
from tools.serapis_calc import p3s
mp.mp.dps = 30
rows = []
for D in (10, 6, 4):
    b = mp.sqrt(D - 2) / 2; phr = mp.log(p3s.YRHO) / b
    for C in (8e-7, 0.0):
        v2 = mp.diff(lambda p: p3s.V(p, C, D), phr, 2); pred = mp.mpf(D - 2) / 32
        rows.append(dict(D=D, C=C, Vpp=float(v2), pred=float(pred), rel=float(abs(v2 / pred - 1))))
# Hessian isotropy with the full lattice sum (independent of p3s's Fourier series)
def Efull(x, y, N=60):
    s = mp.mpf(0)
    for m in range(-N, N + 1):
        for n in range(-N, N + 1):
            if m == 0 and n == 0: continue
            s += y ** 1.5 / ((m + n * x) ** 2 + (n * y) ** 2) ** 1.5
    return s
x0, y0 = mp.mpf(1) / 2, mp.sqrt(3) / 2
mp.mp.dps = 20
h = mp.mpf('1e-3')
E0 = Efull(x0, y0)
Exx = (Efull(x0 + h, y0) - 2 * E0 + Efull(x0 - h, y0)) / h ** 2
Eyy = (Efull(x0, y0 + h) - 2 * E0 + Efull(x0, y0 - h)) / h ** 2
iso = dict(Exx=float(Exx), Eyy=float(Eyy), rel_diff=float(abs(Exx / Eyy - 1)), y2Eyy_over_E=float(y0 ** 2 * Eyy / E0), pred_3_8=0.375,
           note='truncated lattice sum N=60, central differences h=1e-3: accurate to ~1e-4 only (cross-check, not the pass rule)')
ok = all(r['rel'] < 1e-8 for r in rows)
out = dict(D='D1641', rows=rows, isotropy_check=iso, verdict='PASS' if ok else 'FAIL')
json.dump(out, open('field_tests/results/D1641_G1b_rho_curvature.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
