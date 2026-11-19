"""JANUS tick 5: Janus relation closed form for any kappa, sign rule, band_i at kappa=1/2 (see PREREG)."""
import json, math, sys
P = 2.8284
def rho(ns, r, p=P): return p*math.sqrt(r/2)/(1-ns)
def alpha_code(ns, r, k, p=P):   # verbatim relation.py
    x = (rho(ns, r, p)-1)/(1+k*rho(ns, r, p)); return -(1-ns)**2*(1+x)*(1+k*k*x)/(2*(1-k*x)**2)
def alpha_closed(ns, r, k, p=P): q = rho(ns, r, p); return -0.5*(1-ns)**2*q*(1+k*(q-1))
G = [(0.968+0.008*i/20, 4e-4+2e-4*j/20) for i in range(21) for j in range(21)]
dev = max(abs(alpha_code(n, r, k)/alpha_closed(n, r, k)-1) for n, r in G for k in (0.25, 0.5, 1, 2))
bands = {'band_e': ((0.970, 0.975), (4.55e-4, 5.12e-4)), 'band_i': ((0.970, 0.975), (4.8e-4, 5.7e-4))}
rr = {b: [min(rho(n, r) for n in ns for r in rs), max(rho(n, r) for n in ns for r in rs)] for b, (ns, rs) in bands.items()}
pos = any(alpha_code(n, r, 0.01*m) >= 0 for b, (ns, rs) in bands.items() for n in ns for r in rs for m in range(1, 1001))
N = 41; ib = [(0.970+0.005*i/(N-1), 4.8e-4+0.9e-4*j/(N-1)) for i in range(N) for j in range(N)]
A = [alpha_code(n, r, 0.5) for n, r in ib]; pulls = [(a-0.0062)/0.0052 for a in A]
out = dict(R1_max_rel_dev=dev, R1='PASS' if dev < 1e-10 else 'FAIL', rho_ranges=rr,
           R2_positive_found_kappa_0p01_to_10=pos, R2='PASS' if (min(v[0] for v in rr.values()) > 1 and not pos) else 'CHECK',
           band_i_kappa_half=dict(alpha_range=[min(A), max(A)], pull_range=[min(pulls), max(pulls)]),
           R3='PASS' if max(map(abs, pulls)) < 2 else 'FAIL',
           band_i_kappa1_D1402=[-P*P*4.8e-4/4, -P*P*5.7e-4/4])
json.dump(out, open(sys.argv[1], 'w'), indent=1); print(json.dumps(out, indent=1))
