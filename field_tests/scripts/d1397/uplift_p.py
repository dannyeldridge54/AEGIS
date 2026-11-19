"""D1397 (locked PREREG_D1397_uplift_p.md)."""
import json, math, sys, time, numpy as np
sys.path.insert(0, '.')
from tools.serapis_calc import pipeline as P
from tools.serapis_calc.shapes import E
eps = 90/(16*math.pi**5*16); Lr = 2 + eps*E(complex(0.5, math.sqrt(3)/2)); lam_phys = eps/Lr; C_phys = 1.25e-6/lam_phys
orig = P._egrid
def base(model, ymax, npts):
    return orig(model, 1.0, ymax, npts)            # unscaled e-grid, cached once
def patched(p):
    def _eg(model, lam, ymax, npts):
        ph, e = base(model, ymax, npts); x = lam*e
        Pp = ((1 + x)**(1 - p) - 1)/(1 + x); g = Pp/(1 - Pp)
        return ph, np.maximum(g, 1e-14)
    return _eg
out = dict(lam_phys=lam_phys, C_phys=C_phys, rows=[])
for name, lam, C, p in (('R0', 1.0, 1.25e-6, 0.0), ('R1', lam_phys, C_phys, 0.0), ('R2', lam_phys, C_phys, 0.25), ('R3', lam_phys, C_phys, 0.5)):
    P._egrid = patched(p); t = time.time()
    r = P.predict('serapis_e', C=C, TR=8.94e8, lam=lam)
    row = dict(run=name, lam=lam, C=C, p=p, ns=float(r['ns']), r=float(r['r']), alpha_s=float(r['alpha_s']), Nstar=float(r['Nstar']),
               in_band=bool(0.969 <= r['ns'] <= 0.975 and 4.55e-4 <= r['r'] <= 5.7e-4), seconds=round(time.time() - t, 1))
    out['rows'].append(row); print(json.dumps(row), flush=True)
    json.dump(out, open('field_tests/results/D1397_uplift_p.json', 'w'), indent=1)
