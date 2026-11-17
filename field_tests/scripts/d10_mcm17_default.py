import sys, pickle, math, numpy as np; sys.path.insert(0, '.')
from tools.janus_astro import mapper_orbits as MO, mapper_feed as F
rows = pickle.load(open('/tmp/claude-0/d10/rows.pkl', 'rb')); pre = pickle.load(open('/tmp/claude-0/d10/pre.pkl', 'rb'))
leg = MO.process_rows(rows, model='MWPotential2014')
eq = len(leg) == len(pre) and all(all((a == b) or (isinstance(a, float) and math.isnan(a) and math.isnan(b)) for a, b in zip(r1, r2)) for r1, r2 in zip(leg, pre))
out = [f"T1 legacy path identical to pre-change output ({len(pre)} rows): {'PASS' if eq else 'FAIL'}"]
o = F.orbit_params_galpy([-8.21], [0.0], [0.0208], [0.0], [233.1], [0.0], pot='McMillan17')
ok2 = o['ecc'][0] < 0.01 and abs(o['rperi'][0]/8.21 - 1) < 0.02 and abs(o['rapo'][0]/8.21 - 1) < 0.02
out.append(f"T2 LSR in McMillan17: ecc={o['ecc'][0]:.5f} rperi={o['rperi'][0]:.4f} rapo={o['rapo'][0]:.4f}: {'PASS' if ok2 else 'FAIL'}")
m = MO.process_rows(rows, model='McMillan17'); e = np.array([r[13] for r in m], float)
ok3 = len(m) == 20 and np.all(np.isfinite(np.array([r[1:14] for r in m], float))) and np.all((e >= 0) & (e < 1))
out.append(f"T3 McMillan17 smoke: {len(m)} rows, ecc range {e.min():.3f}-{e.max():.3f}: {'PASS' if ok3 else 'FAIL'}")
dr = [m[i][11]/leg[i][11] - 1 for i in range(len(m))]
out.append(f"reported: r_apo change McM17 vs MWP14 (incl. frame change): median {np.median(dr):+.3f}, range {min(dr):+.3f} to {max(dr):+.3f}")
open('field_tests/results/d10_mcm17_default.txt', 'w').write("\n".join(out)+"\n"); print("\n".join(out))
