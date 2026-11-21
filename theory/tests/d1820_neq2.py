import json, itertools
k, D3 = 0.0822, -0.237; B = (33/5, 1, -3)
def residual(b):
    d = [k * x for x in b]
    t = (d[1] - d[0]) / (B[0] - B[1])                 # shift of the 1-2 meeting point, t = ln(mu/M12)/2pi
    return D3 + (B[1] - B[2]) * t - d[2] + d[1]       # alpha3 - alpha2 after thresholds at the new point
out = {'condition': 'D3 + 4*k*(b2-b1)/5.6 + k*(b2-b3) = 0  <=>  (b2-b3) + 0.714*(b2-b1) = %.3f' % (-D3 / k)}
for name, b in (('A_SU5', (-10, -10, -10)), ('B_split', (0, -4, -6))):
    r = residual(b); out[name] = dict(b=b, residual=r, verdict='CLOSES' if abs(r) <= 0.05 else 'FAILS')
best = []
for h in itertools.product(range(0, 7), repeat=3):    # add N=2 hyper contributions (non-negative integers) to config B
    b = tuple(x + y for x, y in zip((0, -4, -6), h)); r = residual(b)
    if abs(r) <= 0.05: best.append((sum(h), h, b, round(r, 3)))
best.sort(); out['minimal_additions_to_B'] = best[:5]
print(json.dumps(out, indent=1)); json.dump(out, open('field_tests/results/d1820_neq2.json', 'w'), indent=1)
