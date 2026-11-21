"""RW13 — PREREG_RW13_RHO_KNOT. AI-assisted. Run from the repo root."""
import json, math
import mpmath as mp
mp.mp.dps = 40
alpha = 1 / 137.036
G = lambda y: mp.log(y * abs(mp.eta(mp.mpf(1) / 2 + 1j * y)) ** 4)
yr = mp.sqrt(3) / 2
G1 = mp.diff(G, yr); G2 = mp.diff(G, yr, 2)
d2 = 2 * (yr**2 * G2 + yr * G1)
out = dict(Gp=float(G1), Gpp=float(G2), d2G_dphi2=float(d2), gradient_zero=abs(float(G1)) < 1e-10)
for b in (1, 12):
    c = alpha * b / (4 * math.pi) * abs(float(d2))
    out[f'b{b}'] = dict(c=c, T1=c * 0.64**2 / 2, T1_pass=c * 0.64**2 / 2 < 1e-6, T2=c * 0.467, T2_pass=c * 0.467 < 1.66e-6)
out['verdict'] = 'PASS' if (out['b12']['T1_pass'] and out['b12']['T2_pass']) else ('FAIL' if not out['b1']['T1_pass'] else 'TENSION')
print(json.dumps(out, indent=1))
json.dump(out, open('field_tests/results/rw13_rho.json', 'w'), indent=1)
