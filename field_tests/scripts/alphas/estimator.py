"""PREREG_ALPHAS_estimator.md: old (5-pt, ±0.1, deg 4) vs new (11-pt, ±0.5, LSQ cubic) α_s, at bd = 200 and 300."""
import json, sys, numpy as np
sys.path.insert(0, '.')
from tools.serapis_calc import pipeline as P
from tools.serapis_calc.ms import Background, spectra
m, V, dV, p0 = P.build('serapis_e', 1.25e-6, 1.0); bg = Background(V, dV, p0); Ns = 50.24462945
old = (-0.1, -0.05, 0.0, 0.05, 0.1); new = tuple(round(0.1*i, 1) for i in range(-5, 6)); out = {}
for bd in (200.0, 300.0):
    o = spectra(bg, Ns, dlnk=old, bd=bd)
    n = spectra(bg, Ns, dlnk=new, bd=bd, return_lp=True); c = np.polyfit(n['dlnk'], n['lnPR'], 3)
    out[str(bd)] = dict(old_ns=float(o['ns']), old_as=float(o['alpha_s']), new_ns=float(1 + c[2]), new_as=float(2*c[1]))
    print(bd, json.dumps(out[str(bd)]), flush=True)
A, B = out['200.0'], out['300.0']
out['P1_new_dAs'] = abs(A['new_as'] - B['new_as']); out['P2_dns'] = max(abs(A['new_ns'] - A['old_ns']), abs(B['new_ns'] - B['old_ns']))
out['P3_old_dAs'] = abs(A['old_as'] - B['old_as']); out['pass'] = bool(out['P1_new_dAs'] <= 3e-5 and out['P2_dns'] <= 2e-5)
print(json.dumps({k: out[k] for k in ('P1_new_dAs', 'P2_dns', 'P3_old_dAs', 'pass')}))
json.dump(out, open('field_tests/results/ALPHAS_estimator.json', 'w'), indent=1)
