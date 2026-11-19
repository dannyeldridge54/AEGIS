"""JANUS tick 11: band_i running via D640 (D1412 functions), pulls vs ACT DR6 (see PREREG)."""
import json, sys, importlib.util as u
sp = u.spec_from_file_location('t', 'field_tests/scripts/d1412/tau_i_offset.py'); 
src = open('field_tests/scripts/d1412/tau_i_offset.py').read().split('rows = []')[0]   # functions + constants only
ns_ = {}; exec(src, ns_)
from scipy.optimize import fsolve
eqs, a640, a_lo = ns_['eqs'], ns_['a640'], ns_['a_lo']
def solve(ns, r):
    (uu, x), info, ier, msg = fsolve(eqs, (0.06, 0.5), args=(ns, r), full_output=True, xtol=1e-14)
    return uu, x, max(abs(e) for e in eqs((uu, x), ns, r))
G = [(0.970+0.005*i/20, 4.8e-4+0.9e-4*j/20) for i in range(21) for j in range(21)]
R = []
for ns, r in G:
    uu, x, res = solve(ns, r); a = a640(uu, x)
    R.append(dict(ns=ns, r=r, x=x, I=1/uu, res=res, eps=4*x*uu**3, a=a, a_lo=a_lo(ns, r), pull=(a-0.0062)/0.0052))
corners = [x for x in R if x['ns'] in (0.970, 0.975) and abs(x['r']-4.8e-4) < 1e-12 or (x['ns'] in (0.970, 0.975) and abs(x['r']-5.7e-4) < 1e-12)]
out = dict(alpha_range=[min(x['a'] for x in R), max(x['a'] for x in R)], alpha_lo_range=[min(x['a_lo'] for x in R), max(x['a_lo'] for x in R)],
           pull_range=[min(x['pull'] for x in R), max(x['pull'] for x in R)], max_res=max(x['res'] for x in R),
           x_range=[min(x['x'] for x in R), max(x['x'] for x in R)], eps_range=[min(x['eps'] for x in R), max(x['eps'] for x in R)],
           corners=[{k: c[k] for k in ('ns', 'r', 'a', 'pull', 'x', 'eps')} for c in corners])
out['verdict'] = 'PASS' if max(abs(x['pull']) for x in R) < 2 and out['max_res'] < 1e-12 and out['x_range'][0] > 0 else 'FAIL'
json.dump(out, open(sys.argv[1], 'w'), indent=1); print(json.dumps({k: v for k, v in out.items() if k != 'corners'}, indent=1))
