"""RW12 — PREREG_RW12_K1_THREAD. AI-assisted. Run from the repo root."""
import json, math
import mpmath as mp
mp.mp.dps = 40
alpha = 1 / 137.036
G = lambda y: mp.log(y * abs(mp.eta(1j * y)) ** 4)
G1 = mp.diff(G, 1); G2 = mp.diff(G, 1, 2)
d2 = 2 * (G2 + G1)
out = dict(Gp1=float(G1), Gpp1=float(G2), d2G_dphi2=float(d2), Gprime_zero=abs(float(G1)) < 1e-10)
dphi, d = 0.64, 0.467
for b in (1, 12):
    c = alpha * b / (4 * math.pi) * abs(float(d2))
    T1 = c * dphi**2 / 2; T2 = c * d
    # exact: y = e^{sqrt2 * phi}, knot at phi = 0; today phi = -d, start phi = -(d + dphi) (rolling toward i from below)
    yk, y0, ys = 1.0, math.exp(-math.sqrt(2) * d), math.exp(-math.sqrt(2) * (d + dphi))
    exact_T1_d0 = alpha * b / (4 * math.pi) * abs(float(G(math.exp(-math.sqrt(2) * dphi)) - G(1)))
    exact_drift = alpha * b / (4 * math.pi) * abs(float(G(y0) - G(ys)))
    out[f'b{b}'] = dict(c=c, T1=T1, T1_pass=T1 < 1e-6, T2=T2, T2_pass=T2 < 1.66e-6,
                        exact_T1_field_at_i=exact_T1_d0, exact_drift_with_d=exact_drift)
p12, p1 = out['b12'], out['b1']
out['verdict'] = 'PASS' if (p12['T1_pass'] and p12['T2_pass']) else ('FAIL' if not p1['T1_pass'] else 'TENSION')
print(json.dumps(out, indent=1))
json.dump(out, open('field_tests/results/rw12_k1.json', 'w'), indent=1)
