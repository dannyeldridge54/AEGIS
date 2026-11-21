"""RW15 — PREREG_RW15_AXION_VS_D1810. AI-assisted. Run from the repo root."""
import json, math
m32_eV = 2.5e5 * 1e9
xs = (20.8, 24.3)
m = [2 * x * m32_eV for x in xs]
mmax_beta = 9e-32
out = dict(m_axion_eV=m, ratio_decades=math.log10(min(m) / mmax_beta),
           verdict='CONFLICT' if min(m) > mmax_beta else 'COMPATIBLE')
print(json.dumps(out, indent=1)); json.dump(out, open('field_tests/results/rw15_axion.json', 'w'), indent=1)
