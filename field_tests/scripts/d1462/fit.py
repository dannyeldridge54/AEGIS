"""JANUS tick 58: band_i formula alpha = LO_k1/2 (a + b(ns-0.9725)) fitted to D1453 grid (PREREG_D1462)."""
import json, math, numpy as np
def LO(ns, r):
    rho = 2*math.sqrt(2)*math.sqrt(r/2)/(1-ns); return -0.5*(1-ns)**2*rho*(1+0.5*(rho-1))
g = [x for x in json.load(open('field_tests/results/D1453_band_i_derived.json'))['rows'] if x.get('converged')]
X = np.array([[1.0, x['ns']-0.9725] for x in g]); y = np.array([x['alpha']/LO(x['ns'], x['r']) for x in g])
(a, b), *_ = np.linalg.lstsq(X, y, rcond=None)
f = lambda ns, r: LO(ns, r)*(a + b*(ns-0.9725))
ins = [f(x['ns'], x['r'])/x['alpha']-1 for x in g]
na = json.load(open('field_tests/results/D1448_tau_i_exact_plateau.json'))['rows']
PTS = [(0.97368, 4.6846e-4), (0.97415, 4.7584e-4), (0.97462, 4.8335e-4), (0.97509, 4.9100e-4), (0.97556, 4.9878e-4)]
oos = [f(n, r)/row['alpha']-1 for (n, r), row in zip(PTS, na)]
ok = max(abs(v) for v in ins) <= 1e-3 and max(abs(v) for v in oos) <= 1e-3
out = dict(D='D1462', a=a, b=b, ratio_range=[float(y.min()), float(y.max())], insample_max=max(abs(v) for v in ins), insample=ins,
           out_of_sample=oos, oos_max=max(abs(v) for v in oos), verdict='ADOPTED' if ok else 'NOT ADOPTED')
json.dump(out, open('field_tests/results/D1462_band_i_lo_formula.json', 'w'), indent=1); print(json.dumps({k: v for k, v in out.items() if k != 'insample'}, indent=1))
