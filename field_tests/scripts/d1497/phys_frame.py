"""D1497: DILMIX strip in D1486's physical frame (PREREG_D1497)."""
import json, math
G = {}; exec(open('field_tests/scripts/d1492/strip_running.py').read().split("SER = ")[0], G)
A = {"(100,100)": 2.0e3, "(200,1000)": 9.9e3, "(400,1e4)": 5.0e4}
out = {"D": "D1497", "d1486_recheck": {k: dict(a=a, y_star=23.25 * a ** (2 / 3), C_phys_A1=1.25e-6 * a) for k, a in A.items()}, "strip": []}
for al, C in [(0.25, 1.25e-6), (0.5, 1.25e-6), (0.25, 1.5e-6), (0.375, 1e-6), (0.375, 1.5e-6), (0.375, 2e-6), (0.5, 1.5e-6)]:
    V, phi, N = G['phistar'](al, C); y = math.exp(math.sqrt(2) * float(phi))
    row = dict(alpha=al, C=C, Nstar=N, y_model=y, frames={k: dict(y_phys=y * a ** (2 / 3), gs_star=1 / (y * a ** (2 / 3)), C_phys=C * a) for k, a in A.items()})
    out['strip'].append(row); print(json.dumps(row), flush=True)
json.dump(out, open('field_tests/results/D1497_phys_frame.json', 'w'), indent=1); print('done')
