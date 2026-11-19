"""JANUS tick 2: closed-form β_s at κ=1 vs the code (relation.py, D669), and pulls vs Planck 2018 (see PREREG)."""
import json, math, sys
P, K = 2.8284, 1.0
def x_ramp(ns, r, p, k): rho = p*math.sqrt(r/2)/(1-ns); return (rho-1)/(1+k*rho)
def alpha_s(ns, r, p=P, k=K):   # verbatim relation.py
    x = x_ramp(ns, r, p, k); return -(1-ns)**2*(1+x)*(1+k*k*x)/(2*(1-k*x)**2)
def beta_s(ns, r, p=P, k=K):    # verbatim relation.py
    x = x_ramp(ns, r, p, k); return -(1-ns)**3*(1+x)*((1-k*x)*(1+k*k*x)+(1+x)*(1-k**3*x))/(4*(1-k*x)**3)
closed = lambda ns, r, p=P: -(p*p*r/4)*(1-ns)
N = 41; pts = [(0.9717+0.0043*i/(N-1), 4.39e-4+0.51e-4*j/(N-1)) for i in range(N) for j in range(N)]
dev = max(abs(beta_s(n, r)/closed(n, r)-1) for n, r in pts)
A = [alpha_s(n, r) for n, r in pts]; B = [beta_s(n, r) for n, r in pts]
pl = {'alpha': (0.002, 0.010), 'beta': (0.010, 0.013)}
pa = [(a-pl['alpha'][0])/pl['alpha'][1] for a in A]; pb = [(b-pl['beta'][0])/pl['beta'][1] for b in B]
ns0, r0 = 0.9745, 4.8e-4
out = dict(max_rel_dev_closed=dev, ruleA='PASS' if dev < 1e-10 else 'FAIL',
           beta_range=[min(B), max(B)], alpha_range=[min(A), max(A)],
           pull_alpha=[min(pa), max(pa)], pull_beta=[min(pb), max(pb)],
           ruleB='PASS' if max(map(abs, pa+pb)) < 2 else 'FAIL',
           serapis_point=dict(alpha=alpha_s(ns0, r0), beta=beta_s(ns0, r0), alpha_over_ns_minus_1=alpha_s(ns0, r0)/(ns0-1),
                              beta_over_alpha=beta_s(ns0, r0)/alpha_s(ns0, r0), one_minus_ns=1-ns0))
json.dump(out, open(sys.argv[1], 'w'), indent=1); print(json.dumps(out, indent=1))
