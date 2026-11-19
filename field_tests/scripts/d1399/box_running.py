"""D1399: alpha_s over the band_e_audited box via the Paper 1 Janus relation; pulls vs ACT DR6 (PREREG_D1399)."""
import json, math, sys
P, KAPPA = 2.8284, 1.0
def x_ramp(ns, r, p, k): rho = p*math.sqrt(r/2)/(1-ns); return (rho-1)/(1+k*rho)
def alpha_s(ns, r, p=P, k=KAPPA):   # copied verbatim from tools/serapis_calc/relation.py (D669)
    x = x_ramp(ns, r, p, k); return -(1-ns)**2*(1+x)*(1+k*k*x)/(2*(1-k*x)**2)
def beta_s(ns, r, p=P, k=KAPPA):
    x = x_ramp(ns, r, p, k); return -(1-ns)**3*(1+x)*((1-k*x)*(1+k*k*x)+(1+x)*(1-k**3*x))/(4*(1-k*x)**3)
DATA = {'P-ACT-LB': (0.0062, 0.0052), 'P-ACT': (0.0060, 0.0055)}
N = 41
ns_g = [0.9717 + (0.9760-0.9717)*i/(N-1) for i in range(N)]
r_g = [4.39e-4 + (4.90e-4-4.39e-4)*j/(N-1) for j in range(N)]
A = [alpha_s(n, r) for n in ns_g for r in r_g]; B = [beta_s(n, r) for n in ns_g for r in r_g]
out = {'alpha_s_min': min(A), 'alpha_s_max': max(A), 'beta_s_min': min(B), 'beta_s_max': max(B),
       'corners': {f'{n},{r}': alpha_s(n, r) for n in (0.9717, 0.9760) for r in (4.39e-4, 4.90e-4)}, 'pulls': {}}
for k, (m, s) in DATA.items():
    pulls = [(a-m)/s for a in A]; out['pulls'][k] = {'min': min(pulls), 'max': max(pulls), 'max_abs': max(abs(p) for p in pulls)}
out['verdict'] = 'PASS' if out['pulls']['P-ACT-LB']['max_abs'] < 2 else 'FAIL'
out['alpha_over_sigma'] = max(abs(a) for a in A)/DATA['P-ACT-LB'][1]
json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else 'field_tests/scripts/d1399/result.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
