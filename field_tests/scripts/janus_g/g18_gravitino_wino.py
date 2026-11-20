"""D1687 / Janus genesis G18 (PREREG_D1687_G18_GRAVITINO_WINO)."""
import json, math
TR = json.load(open('field_tests/results/D1665_G15_kappa.json'))['T_R_GeV']; ODM = 0.1200
def Y_a(T): x = T / 1e10; L = math.log(x); return 1.9e-12 * x * (1 + 0.045 * L) * (1 - 0.028 * L)
def Y_b(T): return 2.3e-12 * T / 1e10
rows = {}
for m in (670.0, 1250.0):
    th = 0.014 * (m / 1000) ** 2
    for nm, Yf in (('BBB_PS', Y_a), ('1211.1770', Y_b)):
        g = 2.75e8 * m * Yf(TR); rows[f'{m:.0f}_{nm}'] = dict(m_GeV=m, Y=Yf(TR), Omega_grav=g, Omega_thermal=th, total=g + th, frac_DM=(g + th) / ODM)
light = [v['frac_DM'] for k, v in rows.items() if k.startswith('670')]
reading = 'CONSISTENT' if max(light) <= 0.30 else ('TENSION' if min(light) <= 1.0 else 'EXCLUDED')
# T_R where gravitino winos alone = 30% of DM at 0.67 TeV (formula a), bisection
lo, hi = 1e6, 1e10
for _ in range(80):
    mid = math.sqrt(lo * hi)
    (lo, hi) = (mid, hi) if 2.75e8 * 670 * Y_a(mid) < 0.30 * ODM else (lo, mid)
out = dict(D='D1687', T_R=TR, rows=rows, reading=reading, TR_for_30pct_at_670=math.sqrt(lo * hi))
json.dump(out, open('field_tests/results/D1687_G18_gravitino_wino.json', 'w'), indent=1); print(json.dumps(out, indent=1))
