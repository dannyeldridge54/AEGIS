import math, json
from mpmath import exp, pi, qp, findroot, mpf
def eta_abs(t): q = exp(-2 * pi * t); return float(exp(-pi * t / 12) * qp(q))      # |eta(i t)|
def L(t): return math.log(t * eta_abs(t) ** 4)
ReS = math.sqrt(3) / 2; b1, b2, b3 = 4.5, -7 / 6, -5.0; need = 0.044
def dD3(d1, d2, d3): return (d3 - d1) + (b3 - b1) * (d1 - d2) / (b2 - b1)
out = {'C1_hypercharge_flux': {}, 'C2_U3_axis': {}}
for NY in (-2, -1, 1, 2):
    d2 = -0.5 * ReS * NY; d1 = -0.5 * ReS * 0.6 * NY; v = dD3(d1, d2, 0.0)
    out['C1_hypercharge_flux'][NY] = dict(dDelta3=v, ratio_to_need=v / need, pass_=0.022 <= v <= 0.066)
Li = L(1.0); special = {'1': 1, 'sqrt2': math.sqrt(2), 'sqrt3': math.sqrt(3), '2': 2, '3': 3}
for db in (-3, -2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2, 3):
    target = Li - need * 4 * math.pi / (-db) * -1   # need = -(db/4pi)(L(t)-L(i))  ->  L(t) = L(i) - 4pi*need/db
    target = Li - 4 * math.pi * need / db
    ts = [x / 100 for x in range(100, 1001)]; vals = [L(t) for t in ts]
    sol = None
    for a, b_, va, vb in zip(ts, ts[1:], vals, vals[1:]):
        if (va - target) * (vb - target) <= 0: sol = a + (b_ - a) * (target - va) / (vb - va); break
    near = min(special.items(), key=lambda kv: abs((sol or 99) - kv[1])) if sol else None
    out['C2_U3_axis'][db] = dict(L_target=target, t=sol, nearest=near[0] if sol else None,
                                 natural=bool(sol and abs(sol - near[1]) / near[1] < 0.02))
out['L_i'] = Li; out['L_range_t1_10'] = [min(vals), max(vals)]
json.dump(out, open('field_tests/results/d2022_direction_node.json', 'w'), indent=1, default=str); print(json.dumps(out, indent=1, default=str))
