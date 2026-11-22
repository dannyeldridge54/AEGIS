import sys, math; sys.argv = ['x']; sys.path.insert(0, '/home/claude/aegis/theory/tests')
import importlib.util; spec = importlib.util.spec_from_file_location('b', '/home/claude/aegis/theory/tests/d2039_battery.py')
src = open('/home/claude/aegis/theory/tests/d2039_battery.py').read().split("o = model(V4); print('START")[0]; exec(src)
from loomcore import Agent, Centre
steps = ((0.5, 2.0), (0.75, 1.5), (0.9, 1.1), (0.97, 1.03), (0.99, 1.01), (0.997, 1.003))
best = None
for sq0, b0 in [(1, 1), (0.1, 1e2), (0.01, 1e4), (1e-3, 1e4)]:
    k0 = dict(V4, sq=sq0, boost=b0); ag = Agent('issues', k0, cost, steps=steps, lo={'nt': 0.0, 'sq': 1e-8, 'm32': 0.1, 'd3': -0.3}, hi={'nt': 2.0, 'sq': 1.0, 'boost': 1e8, 'm32': 10.0, 'd3': 0.3})
    c = Centre([ag], explore=0.0); c.run(400); k = ag.settings(); cs = cost(k)
    print('start sq=%g boost=%g -> cost %.3f %s' % (sq0, b0, cs, {n: round(v, 5) for n, v in k.items()}))
    if best is None or cs < best[0]: best = (cs, k)
k = best[1]; o = model(k); g = goals(o)
print('MULTI-START END', {n: round(v, 5) for n, v in k.items()}, {n: round(v, 4) for n, v in o.items()})
print('GOALS', {n: ('PASS' if v == 0 else 'FAIL %.2f' % v) for n, v in g.items()}, '| moved', moved(k))
# HAND pass: sq at the G2 edge (leak = 0.5), boost at the G3 edge (mT/H = 0.1), m32 = 1, bisect d3 to z = 0
h = dict(V4); h['sq'] = 0.5/17.8192; h['boost'] = 0.1/model(V4)['mT_H'] * 1.0001
lo, hi = -0.3, 0.3
for _ in range(60):
    mid = (lo + hi)/2; h['d3'] = mid
    if model(h)['z'] < 0: lo = mid
    else: hi = mid
o = model(h); g = goals(o)
print('HAND', {n: round(v, 6) for n, v in h.items()}, {n: round(v, 4) for n, v in o.items()})
print('HAND GOALS', {n: ('PASS' if v == 0 else 'FAIL %.2f' % v) for n, v in g.items()}, '| moved (fitted):', moved(h))
