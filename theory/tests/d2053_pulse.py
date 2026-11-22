import math, sys, time, random
sys.path.insert(0, '/home/claude/aegis/tools/loom'); from loomcore import Agent, Centre
m320, at, aG = 2.58e5, 21.10, 1/28.0; gG2 = 4*math.pi*aG; b = (33/5, 1.0, -3.0); g2 = (0.211, 0.42, 1.106)
MP, x, A = 2.435e18, 21.10, 0.54; a = 2*math.pi/6; sig = x/a; H = 5.69e12; N = 21
V4 = {'rA': 1.0, 'd3': -0.094, 'boost': 1.0, 'm32': 1.0}
def model(k):
    sq = abs(math.log(k['rA']))/x/17.8; m32 = m320*k['m32']; M0 = sq*m32/at; An = m32/(16*math.pi**2)
    M = [abs(g2[i]*(M0/gG2 + b[i]*An)) for i in range(3)]; wino, glu = M[1], M[2]
    d = -(1/(2*math.pi))*(2.0*math.log(glu/4930.) + (-4/3 - (4/3)*(4/5.6))*math.log(wino/687.))
    a_s = 1/(1/(0.1142 + 0.0864*(k['d3'] + 0.094)) + d)
    mT = k['boost']*a*a*A*math.exp(-x)*MP/math.sqrt(2*sig)
    return {'alpha_s': a_s, 'z': (a_s-0.1180)/0.0009, 'leak': M0/(0.42/(16*math.pi**2)*m32), 'mT_H': mT/H, 'wino': wino/1e3, 'gluino': glu/1e3}
def goals(o): return {'G1': max(0, abs(o['z'])-2), 'G2': max(0, math.log10(max(o['leak'], 1e-12)/0.5))*3, 'G3': max(0, math.log10(0.1/o['mT_H']))*3,
                      'G4': max(0, (0.670-o['wino'])/0.01, (o['wino']-0.70)/0.01), 'G5': max(0, (2.25-o['gluino'])/0.1)}
def moved(k): return [n for n in k if (n == 'rA' and not (0.64 <= k[n] <= 1.57)) or (n != 'rA' and abs(k[n]-V4[n]) > 1e-9*max(1, abs(V4[n])))]
def cost(k, split='tune'): return sum(g*g for g in goals(model(k)).values()) + 0.5*math.log(N)*len(moved(k)) + 1.0
o = model(V4); print('START tether + v4:', {k: round(v, 4) for k, v in o.items()}, flush=True)
steps = ((0.5, 2.0), (0.75, 1.5), (0.9, 1.1), (0.97, 1.03), (0.99, 1.01), (0.997, 1.003))
lo = {'rA': 0.1, 'd3': -0.3, 'boost': 1.0, 'm32': 0.1}; hi = {'rA': 10.0, 'd3': 0.3, 'boost': 1e8, 'm32': 10.0}
t0 = time.time(); best = None; rng = random.Random(3); pulse = 0
while time.time() - t0 < 60:
    pulse += 1; k0 = dict(V4) if pulse == 1 else {'rA': math.exp(rng.uniform(-1, 1)), 'd3': rng.uniform(-0.2, 0.05), 'boost': 10**rng.uniform(0, 5), 'm32': 10**rng.uniform(-0.5, 0.5)}
    ag = Agent('ufe', k0, cost, steps=steps, lo=lo, hi=hi); c = Centre([ag], explore=0.0); c.run(300); k = ag.settings(); cs = cost(k)
    if best is None or cs < best[0]:
        best = (cs, k); print('  t=%4.1fs pulse %3d NEW BEST cost %.3f %s' % (time.time()-t0, pulse, cs, {n: round(v, 5) for n, v in k.items()}), flush=True)
k = best[1]; o = model(k); g = goals(o)
print('PULSES', pulse, 'in 60 s'); print('END', {n: round(v, 5) for n, v in k.items()}, {n: round(v, 4) for n, v in o.items()})
print('GOALS', {n: ('PASS' if v == 0 else 'FAIL %.2f' % v) for n, v in g.items()}, '| moved (fitted):', moved(k))
