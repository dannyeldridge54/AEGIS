"""D1847: torus -> pyramid/turnover (2D orbifolds) -> cube (T^3 fibre) map; per-shape fixed points, cone angles, Euler numbers; T^6 orbifold chi vs the D1811 requirement."""
import math, json
# 2D orbifolds T^2/Z_N: fixed points and cone angles (standard)
two_d = {
 'T2 (torus)':  dict(N=1, cones=[], chi_orb=0, shape='torus (square/hexagon with opposite sides glued)'),
 'T2/Z2':       dict(N=2, cones=[2, 2, 2, 2], shape='PYRAMID: tetrahedron, 4 corners of angle pi (pillowcase)'),
 'T2/Z3':       dict(N=3, cones=[3, 3, 3], shape='TURNOVER: 3 corners of angle 2pi/3 (only at tau = rho)'),
 'T2/Z4':       dict(N=4, cones=[4, 4, 2], shape='3 corners (pi/2, pi/2, pi) (only at tau = i)'),
 'T2/Z6':       dict(N=6, cones=[6, 3, 2], shape='3 corners (pi/3, 2pi/3, pi) (only at tau = rho)')}
for k, v in two_d.items():
    v['chi_orb'] = 0 - sum(1 - 1 / n for n in v['cones']) + 0 if v['N'] > 1 else 0   # orbifold Euler char of quotient = chi(T2)/N = 0 ... + cone corrections
    v['chi_orb'] = round(2 - sum(1 - 1 / n for n in v['cones']), 4) if v['N'] > 1 else 0.0  # sphere with cones
    v['fixed_points'] = len(v['cones'])
# 6D toroidal orbifolds (standard Hodge numbers, Dixon-Harvey-Vafa-Witten / Font-Ibanez tables)
six_d = {'T6/Z3': (36, 0), 'T6/Z2xZ2': (51, 3), 'T6/Z3xZ3': (84, 0), 'T6/Z4': (31, 7), 'T6/Z6-I': (29, 5), 'T6/Z7': (24, 0), 'T6/Z2xZ4': (61, 1), 'T6/Z6xZ6': (84, 0)}
chi = {k: 2 * (h11 - h21) for k, (h11, h21) in six_d.items()}
# D1811: N=6 chain closes at chi ~ 89.5 for A=1; M2 ~ A/chi so the A needed for each orbifold chi:
A_needed = {k: round(abs(c) / 89.5, 3) for k, c in chi.items()}
natural = {k: 0.3 <= a <= 3 for k, a in A_needed.items()}
out = dict(two_d=two_d, six_d_hodge=six_d, chi=chi, A_needed=A_needed, natural_A=natural)
print(json.dumps(dict(chi=chi, A_needed=A_needed, natural=natural), indent=1))
for k, v in two_d.items(): print(k, v['fixed_points'], 'fixed pts', 'chi_orb', v['chi_orb'], '|', v['shape'])
json.dump(out, open('field_tests/results/d1847_shapes.json', 'w'), indent=1)
