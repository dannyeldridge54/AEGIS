"""D1928: single Froggatt–Nielsen flavon, |u| free — locked log-spaced sweep (D1927 referee rules)."""
import json, math, cmath, numpy as np, sys
sys.path.insert(0, 'theory/tests')
src = open('theory/tests/d1925_onespurion.py').read().split('u = U(0.0457')[0]; exec(src)   # same scan + natural as D1925
ph = cmath.phase(U(0.0457 * cmath.exp(1j * math.radians(49))))
grid = [0.01 * 30 ** (k / 24) for k in range(25)]
rows = []
for a in grid:
    fits = scan(a); best = None
    for f in fits:
        f7, fJ = natural(a * cmath.exp(1j * ph), *f, N=2000, seed=28)
        if best is None or (f7 >= 0.05 and fJ >= 0.2 and f7 > best['f7']) or (best['f7'] < 0.05 and f7 > best['f7']):
            best = dict(qQ=f[0], qu=f[1], qd=f[2], f7=f7, fJ=fJ)
    nat = bool(best and best['f7'] >= 0.05 and best['fJ'] >= 0.2)
    rows.append(dict(abs_u=a, n_fit=len(fits), natural=nat, best=best))
# longest contiguous natural window
runs, cur = [], []
for r in rows:
    if r['natural']: cur.append(r['abs_u'])
    else:
        if cur: runs.append(cur); cur = []
if cur: runs.append(cur)
w = max(runs, key=len) if runs else []
width = (w[-1] / w[0]) if len(w) >= 1 else 1.0
P = (math.log(width) + math.log(30) / 24) / math.log(30) if w else 0.0     # fraction of the log range (half-step padding each side)
out = dict(grid=rows, windows=[[r[0], r[-1], len(r)] for r in runs], best_window=[w[0], w[-1]] if w else None,
           width_factor=width, prior_fraction=P, n_natural_points=sum(r['natural'] for r in rows))
out['verdict'] = 'PASS' if width >= 1.5 else 'FAIL'
print(json.dumps(out, indent=1)); json.dump(out, open('field_tests/results/d1928_flavon_sweep.json', 'w'), indent=1)
