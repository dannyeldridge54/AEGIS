"""JANUS tick 74: derived points vs 2511.01612 Table IV (68 %, n_s, alpha_s, beta_s all free) (PREREG_D1471)."""
import json
T = {'ACT+P': dict(ns=(0.96501, 0.00490, 0.00493), a=(0.01195, 0.00623, 0.00628), b=(0.01869, 0.00954, 0.00967)),
     '+SPT': dict(ns=(0.96437, 0.00453, 0.00449), a=(0.00804, 0.00567, 0.00571), b=(0.01477, 0.00884, 0.00876)),
     '+eBOSS': dict(ns=(0.97101, 0.00391, 0.00388), a=(-0.00323, 0.00390, 0.00388), b=(-0.00755, 0.00346, 0.00347))}
P = {'rho_A1': dict(ns=0.974393, a=-9.9796e-4, b=-2.860e-5), 'tau_i_NA12': dict(ns=0.97462, a=-8.5430e-4, b=-3.126e-5)}
def pull(x, c):
    m, up, dn = c; return (x-m)/(up if x > m else dn)
out = dict(D='D1471', pulls={p: {k: {q: pull(v[q], T[k][q]) for q in ('ns', 'a', 'b')} for k in T} for p, v in P.items()})
amax = max(abs(out['pulls'][p][k]['a']) for p in P for k in T)
out['max_abs_alpha_pull'] = amax; out['verdict'] = 'PASS' if amax < 2 else 'FAIL'
json.dump(out, open('field_tests/results/D1471_lya_running.json', 'w'), indent=1); print(json.dumps(out, indent=1))
