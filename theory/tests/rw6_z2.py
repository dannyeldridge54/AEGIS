"""RW6 — PREREG_RW6_Z2. AI-assisted. Run from the repo root."""
import json, math
d1851 = json.load(open('field_tests/results/rw2_sequester.json'))
c_lo, c_hi = d1851['C2_range']
dphi = 0.64
w0, Ode, a_knot = -0.74, 0.69, 1.89
phip = math.sqrt(3 * (1 + w0) * Ode)
d = phip * math.log(a_knot)
H0_per_yr = 67.4 / 3.0857e19 * 3.15576e7
T1 = c_lo * dphi**2 / 2
T2 = c_lo * d
T3 = c_lo * d * phip * H0_per_yr
out = dict(c_range=[c_lo, c_hi], O1_band=[0.3 * c_lo, 3 * c_hi], dphi=dphi, phi_prime=phip, d_est=d,
           T1_dlnalpha_min=T1, T1_range=[0.3 * c_lo * dphi**2 / 2, 3 * c_hi * dphi**2 / 2], T1_pass=T1 < 1e-6,
           T1_ratio=T1 / 1e-6,
           T2_zeta_today=T2, T2_pass=T2 < 1.66e-6, T2_ratio=T2 / 1.66e-6, d_max=1.66e-6 / c_lo,
           T3_rate_per_yr=T3, T3_ratio=T3 / 1e-18, H0_per_yr=H0_per_yr)
out['verdict'] = 'PASS' if (out['T1_pass'] and out['T2_pass']) else ('FAIL' if not out['T1_pass'] else 'TENSION')
print(json.dumps(out, indent=1))
json.dump(out, open('field_tests/results/rw6_z2.json', 'w'), indent=1)
