"""JANUS tick 22: Delta alpha_s between vacua with both sub-percent meters (see PREREG)."""
import json, sys
src = open('field_tests/scripts/d1412/tau_i_offset.py').read().split('rows = []')[0]; ns_ = {}; exec(src, ns_)
from scipy.optimize import fsolve
eqs, a640 = ns_['eqs'], ns_['a640']
k = 1.0352109; P2 = 2.8284**2/4
G = [(0.970+0.005*i/20, 4.8e-4+0.32e-4*j/20) for i in range(21) for j in range(21)]
D = []; res = 0
for n, r in G:
    (u, x), info, ier, msg = fsolve(eqs, (0.06, 0.5), args=(n, r), full_output=True, xtol=1e-14)
    res = max(res, max(abs(e) for e in eqs((u, x), n, r)))
    D.append(a640(u, x) - (-k*P2*r))
out = dict(delta_range=[min(D), max(D)], max_abs=max(map(abs, D)), sigma_2030=8.5e-4, separation_sigma=max(map(abs, D))/8.5e-4,
           max_residual=res, D1408_LO=[1.25e-4, 2.83e-4], D1263_exact=1.44e-4)
out['verdict'] = 'REVIVE' if out['max_abs'] >= 1.7e-3 else 'still killed'
json.dump(out, open(sys.argv[1], 'w'), indent=1); print(json.dumps(out, indent=1))
