"""JANUS tick 53: band_e formula alpha = -2r(a + b(ns-0.972)) fitted to D1454 grid (PREREG_D1457)."""
import json, numpy as np
g = [x for x in json.load(open('field_tests/results/D1454_band_e_derived.json'))['rows'] if x.get('converged')]
X = np.array([[1.0, x['ns']-0.972] for x in g]); y = np.array([x['alpha']/(-2*x['r']) for x in g])
(a, b), *_ = np.linalg.lstsq(X, y, rcond=None)
f = lambda ns, r: -2*r*(a + b*(ns-0.972))
ins = [f(x['ns'], x['r'])/x['alpha']-1 for x in g]
A1 = json.load(open('field_tests/results/D1442_rho_second_order.json'))['second']
c44 = json.load(open('field_tests/results/D1444_four_corners.json'))['corners']
oos = {'A1': (0.974393, 4.82095e-4, A1['alpha']),
       'K4': (0.973232, 4.70877e-4, c44['K4']['alpha']), 'K3_out_of_band_r': (0.971663, 4.52911e-4, c44['K3']['alpha'])}
oe = {k: f(n, r)/al-1 for k, (n, r, al) in oos.items()}
ok = max(abs(v) for v in ins) <= 1e-3 and abs(oe['A1']) <= 1e-3 and abs(oe['K4']) <= 1e-3
out = dict(D='D1457', a=a, b=b, insample_max=max(abs(v) for v in ins), insample=ins, out_of_sample=oe, verdict='ADOPTED' if ok else 'NOT ADOPTED')
json.dump(out, open('field_tests/results/D1457_band_e_formula.json', 'w'), indent=1); print(json.dumps(out, indent=1))
