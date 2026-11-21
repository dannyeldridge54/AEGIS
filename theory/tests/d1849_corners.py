import numpy as np, math, cmath, json, sys
sys.path.insert(0, 'theory/tests')
from z3_modes import modes, z3_classes, w, TAU
M, a = 9, 1 / 6
_, ev, V, C = z3_classes(M, a, a)
cls = np.round(np.angle(ev) / (2 * math.pi) * 3) % 3
g = 120; s, t = np.meshgrid((np.arange(g) + .5) / g, (np.arange(g) + .5) / g)
Z = (s + TAU * t).ravel(); B = modes(M, a, a, Z)                 # (points, M)
fp = []
for m in range(-3, 4):
    for n in range(-3, 4):
        z = (m + n * w) / (w - 1)
        # reduce to cell coordinates
        tt = z.imag / TAU.imag; ss = z.real - tt * TAU.real; ss %= 1; tt %= 1
        if not any(abs(ss - p[0]) < 1e-6 and abs(tt - p[1]) < 1e-6 for p in fp): fp.append((ss, tt))
fp = fp[:3] if len(fp) >= 3 else fp
def cdist(p, q):
    d = [min(abs(p[i] - q[i]), 1 - abs(p[i] - q[i])) for i in (0, 1)]; return math.hypot(*d)
out = dict(fixed_points=fp, classes={})
for c in range(3):
    idx = np.where(cls == c)[0]; Ec = B @ V[:, idx]                 # eigenfunctions on grid
    G = Ec.conj().T @ Ec / len(Z); L = np.linalg.cholesky(G); Eo = Ec @ np.linalg.inv(L).conj().T
    P = np.sum(np.abs(Eo) ** 2, axis=1); j = int(np.argmax(P)); pk = (s.ravel()[j], t.ravel()[j])
    near = min(range(len(fp)), key=lambda k: cdist(pk, fp[k]))
    vals = []
    for (fs, ft) in fp:
        k = int(np.argmin([cdist((s.ravel()[i], t.ravel()[i]), (fs, ft)) for i in range(0, len(Z), 1)]) )
        vals.append(float(P[k] / P.mean()))
    out['classes'][c] = dict(peak=pk, nearest_fp=near, dist=cdist(pk, fp[near]), density_at_fps_over_mean=vals, max_over_mean=float(P.max() / P.mean()))
    print('class', c, 'peak', np.round(pk, 3), 'nearest fp', near, 'dist %.3f' % cdist(pk, fp[near]), 'density at fps/mean', np.round(vals, 2))
on = [out['classes'][c]['dist'] <= 0.08 for c in range(3)]; distinct = len({out['classes'][c]['nearest_fp'] for c in range(3)}) == 3
out['verdict'] = 'CORNERS' if all(on) and distinct else ('PARTIAL' if all(on) else 'NO')
print('fixed points', np.round(fp, 3), 'VERDICT', out['verdict'])
json.dump(out, open('field_tests/results/d1849_corners.json', 'w'), indent=1, default=float)
