"""D2282: Z3 x Z6 fold geometry - sectors, N=2 sectors, frozen complex structures (see PREREG_D2282)."""
import json
from fractions import Fraction as F
v1 = [F(1,3), F(0), F(-1,3)]; v2 = [F(0), F(1,6), F(-1,6)]
sectors, n2, orders = [], [], {0: set(), 1: set(), 2: set()}
for k in range(3):
    for l in range(6):
        if k == 0 and l == 0: continue
        g = [k*a + l*b for a, b in zip(v1, v2)]
        fixed = [i for i, x in enumerate(g) if x.denominator == 1]
        susy = sum(g).denominator == 1
        for i, x in enumerate(g):
            if x.denominator != 1: orders[i].add((x - (x.numerator // x.denominator)).denominator)
        sectors.append(dict(k=k, l=l, g=[str(x) for x in g], fixed_tori=fixed, susy=susy))
        if len(fixed) == 1: n2.append(dict(k=k, l=l, fixed_torus=fixed[0]))
frozen = {i: ('rho' if (orders[i] & {3, 6}) else 'i' if 4 in orders[i] else 'free') for i in orders}
out = dict(sectors=sectors, n2=n2, rotation_orders={i: sorted(o) for i, o in orders.items()}, U_frozen=frozen,
           n2_per_torus={i: sum(1 for s in n2 if s['fixed_torus'] == i) for i in range(3)}, all_susy=all(s['susy'] for s in sectors))
out['verdict'] = 'PASS' if all(f == 'rho' for f in frozen.values()) and all(out['n2_per_torus'][i] > 0 for i in range(3)) and out['all_susy'] else 'FAIL'
json.dump(out, open('field_tests/results/d2282_z3z6_geometry.json', 'w'), indent=1)
print({k: out[k] for k in ('rotation_orders', 'U_frozen', 'n2_per_torus', 'all_susy', 'verdict')}); print('N=2 sectors:', n2)
