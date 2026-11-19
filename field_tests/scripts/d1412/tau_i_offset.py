"""JANUS tick 10: D640 offset-corrected Janus relation on the NA12 exact tau=i points (see PREREG)."""
import json, math, sys
from scipy.optimize import fsolve
c = math.log(1728)/(2*math.pi)
PTS = [(0.97368, 4.6846e-4, -8.454e-4), (0.97415, 4.7584e-4, -8.501e-4), (0.97462, 4.8335e-4, -8.543e-4),
       (0.97509, 4.9100e-4, -8.587e-4), (0.97556, 4.9878e-4, -8.635e-4)]          # NA12 exact MS (eps 1.30–1.50e-4)
def eqs(v, ns, r):
    u, x = v
    return [8*u*u*((2-x)+c*u*(5-x)) - (1-ns), 64*u**4*(1+x)**2*(1+2*c*u) - r]
def a640(u, x): return -32*u**4*(1+x)*((4+x)+c*u*(23+2*x))
def a_lo(ns, r, k=0.5, p=2.8284):
    q = p*math.sqrt(r/2)/(1-ns); return -0.5*(1-ns)**2*q*(1+k*(q-1))
rows = []
for ns, r, ae in PTS:
    (u, x), info, ier, msg = fsolve(eqs, (0.06, 0.5), args=(ns, r), full_output=True, xtol=1e-14)
    res = max(abs(e) for e in eqs((u, x), ns, r))
    rows.append(dict(ns=ns, r=r, alpha_exact=ae, u=u, x=x, I_star=1/u, residual=res, alpha_D640=a640(u, x),
                     err_D640=a640(u, x)/ae-1, alpha_LO_k_half=a_lo(ns, r), err_LO=a_lo(ns, r)/ae-1))
out = dict(c=c, rows=rows, max_abs_err_D640=max(abs(x['err_D640']) for x in rows), max_residual=max(x['residual'] for x in rows))
out['verdict'] = 'PASS' if out['max_abs_err_D640'] < 0.01 and out['max_residual'] < 1e-12 else 'FAIL'
json.dump(out, open(sys.argv[1], 'w'), indent=1); print(json.dumps(out, indent=1))
