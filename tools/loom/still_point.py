"""D1978: the still point and its directions (Danny 18:12). At the best-balance point of the three tandem axes (S: T_R, T: m3/2, U: u):
- INWARD (restoring) directions = stiff eigenvectors of the Fisher matrix F = Jᵀ J (moving away costs chi² fast; the data pull it back).
- OUTWARD (free) directions = sloppy eigenvectors (moving costs almost nothing; the field 'goes through' there).
- The 360° view: in each plane (S–T, T–U, S–U), step a fixed distance from the still point at 36 angles and record Δχ²: the stiffness rose.
Uses the D1976 model and data (6 data incl. bounds as one-sided data). A deterministic geometric analysis, not new evidence."""
import json, math, sys
import numpy as np
sys.path.insert(0, 'tools/loom')
src = open('tools/loom/method_tests_3axis.py').read().split('def T1(')[0]; exec(src)
x0, r0 = fit(REAL); chi0 = float(np.sum(r0 ** 2))
def chi(p): return float(np.sum(resid(p, REAL) ** 2))
h = 1e-4; J = []
for i in range(3):
    e = np.zeros(3); e[i] = h; J.append((resid(x0 + e, REAL) - resid(x0 - e, REAL)) / (2 * h))
J = np.array(J).T; F = J.T @ J
w, V = np.linalg.eigh(F)
axes = ['S (ln T_R)', 'T (ln m3/2)', 'U (ln u)']
dirs = []
for k in range(3):
    v = V[:, k]; v = v * np.sign(v[np.argmax(abs(v))])
    dirs.append(dict(eigenvalue=float(w[k]), one_sigma_step=float(1 / math.sqrt(max(w[k], 1e-12))),
                     kind='INWARD (restoring, stiff)' if w[k] > 1.0 else 'OUTWARD (free, sloppy)',
                     composition={axes[i]: round(float(v[i]), 3) for i in range(3)}))
rose = {}
for (a, b, nm) in ((0, 1, 'S-T'), (1, 2, 'T-U'), (0, 2, 'S-U')):
    ring = []
    for k in range(36):
        th = 2 * math.pi * k / 36; p = x0.copy(); p[a] += 0.1 * math.cos(th); p[b] += 0.1 * math.sin(th)
        ring.append(round(chi(p) - chi0, 3))
    rose[nm] = dict(dchi2_at_radius_0p1=ring, stiffest_angle_deg=10 * int(np.argmax(ring)), loosest_angle_deg=10 * int(np.argmin(ring)),
                    stiff_over_loose=float(max(ring) / max(min(ring), 1e-9)))
out = dict(still_point=dict(T_R=3.7e8 * math.exp(x0[1]), m32=2.58e5 * math.exp(x0[0]), u=0.02663 * math.exp(x0[2]), chi2=chi0),
           directions=dirs, rose_360=rose)
print(json.dumps({k: v for k, v in out.items() if k != 'rose_360'}, indent=1, default=float))
print({k: (v['stiffest_angle_deg'], v['loosest_angle_deg'], round(v['stiff_over_loose'], 1)) for k, v in rose.items()})
json.dump(out, open('field_tests/results/d1978_still_point.json', 'w'), indent=1, default=float)
