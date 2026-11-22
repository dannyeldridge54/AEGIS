import math, sys, os
sys.path.insert(0, '/home/claude/aegis/tools/loom'); from loomcore import Agent, Centre
m320, at, aG = 2.58e5, 21.10, 1/28.0; gG2 = 4*math.pi*aG; b = (33/5, 1.0, -3.0); g2 = (0.211, 0.42, 1.106)
MP, x, A = 2.435e18, 21.10, 0.54; a = 2*math.pi/6; sig = x/a; H = 5.69e12; N = 21
V4 = {'m32': 1.0, 'd3': -0.094, 'sq': 1.0, 'nt': 2.0, 'boost': 1.0}
def model(k):
    m32 = m320*k['m32']; M0 = k['sq']*(k['nt']/2)*m32/at; An = m32/(16*math.pi**2)
    M = [abs(g2[i]*(M0/gG2 + b[i]*An)) for i in range(3)]; wino, glu = M[1], M[2]
    d = -(1/(2*math.pi))*(2.0*math.log(glu/4930.) + (-4/3 - (4/3)*(4/5.6))*math.log(wino/687.))
    a_s = 1/(1/(0.1142 + 0.0864*(k['d3'] + 0.094)) + d)
    mT = k['boost']*a*a*A*math.exp(-x)*MP/math.sqrt(2*sig)
    return {'alpha_s': a_s, 'z': (a_s - 0.1180)/0.0009, 'leak': M0/(0.42/(16*math.pi**2)*m32), 'mT_H': mT/H, 'wino': wino/1e3, 'gluino': glu/1e3}
def goals(o):
    v = {'G1': max(0, abs(o['z']) - 2), 'G2': max(0, math.log10(max(o['leak'], 1e-12)/0.5)) * 3, 'G3': max(0, math.log10(0.1/o['mT_H'])) * 3,
         'G4': max(0, (0.670 - o['wino'])/0.01, (o['wino'] - 0.70)/0.01), 'G5': max(0, (2.25 - o['gluino'])/0.1)}
    return v
def moved(k): return [n for n in k if abs(k[n] - V4[n]) > 1e-9 * max(1, abs(V4[n]))]
def cost(k, split='tune'):
    o = model(k); return sum(g*g for g in goals(o).values()) + 0.5*math.log(N)*len(moved(k)) + 1.0
o = model(V4); print('START (v4 as written):', {k: round(v, 4) for k, v in o.items()}, '| goals', {k: round(v, 2) for k, v in goals(o).items()}, flush=True)
steps = ((0.1, 10.0), (0.5, 2.0), (0.75, 1.5), (0.9, 1.1), (0.97, 1.03), (0.99, 1.01))
ag = Agent('issues', dict(V4), cost, steps=steps, lo={'nt': 0.0, 'sq': 1e-8, 'm32': 0.1, 'd3': -0.3}, hi={'nt': 2.0, 'sq': 1.0, 'boost': 1e8, 'm32': 10.0, 'd3': 0.3})
c = Centre([ag], explore=0.0); last = None
for r in range(300):
    c.run(1); kept = [e for e in ag.ledger if e.get('kept')]
    if kept and kept[-1] is not last:
        last = kept[-1]; print('  poke %-5s %10.4g -> %-10.4g cost %.3f' % (last['knob'], last['from'], last['to'], last['tune']), flush=True)
    if c.log and 'BALANCED' in str(c.log[-1]): break
k = ag.settings(); o = model(k); g = goals(o)
print('END:', {n: round(v, 6) for n, v in k.items()}, '| state', c.log[-1].get('event', 'budget'))
print('     ', {n: round(v, 4) for n, v in o.items()}); print('GOALS', {n: ('PASS' if v == 0 else 'FAIL %.2f' % v) for n, v in g.items()})
print('MOVED (fitted, to be derived):', moved(k)); print('VERDICT:', 'NAILED' if all(v == 0 for v in g.values()) and not moved(k) else ('FIT (all goals met only by moving knobs)' if all(v == 0 for v in g.values()) else 'STALL'))
