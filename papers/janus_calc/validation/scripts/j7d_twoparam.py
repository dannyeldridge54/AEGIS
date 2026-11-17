"""J7d (locked PREREG_J7d_aspic_twoparam)."""
import sys, json, time, math, numpy as np, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
from tools.janus_calc.core import Model, spectra3
from tools.serapis_calc.ms import Background, spectra_fast
DL = tuple(np.linspace(-1, 1, 9)); ASP = 'theory/janus/aspic/aspic_j7d_clean.txt'
A = {}
for l in open(ASP):
    c = l.split(); A[(int(c[0]), float(c[1]))] = dict(x=float(c[2]), ns=float(c[3]), r=float(c[4]), a=float(c[5]))
def model(i):
    x60 = A[(i, 60.0)]['x']
    if i in (1, 2):
        al, mu = (0.1, 10.0) if i == 1 else (0.2, 8.0); X = lambda y: y/mu
        V = lambda y: 1 - math.cos(X(y)) + al*math.sin(X(y))**2
        dV = lambda y: (math.sin(X(y)) + 2*al*math.sin(X(y))*math.cos(X(y)))/mu
        return f'TI a={al} mu={mu}', V, dV, mu*(math.pi - x60), mu*math.pi
    if i == 3:
        al, f = 1e-3, 5.0
        V = lambda y: 1 + al*math.log(abs(math.sin(y/f)))          # cos(pi/2 - y/f) = sin(y/f)
        dV = lambda y: al*math.cos(y/f)/math.sin(y/f)/f
        return f'PSNI a={al} f={f}', V, dV, f*(math.pi/2 - x60), f*math.pi/2
    if i in (4, 5):
        p, mu = (4, 15.0) if i == 4 else (2, 10.0); X = lambda y: 1 - y/mu
        return f'SFI p={p} mu={mu}', (lambda y: 1 - X(y)**p), (lambda y: p*X(y)**(p - 1)/mu), mu*(1 - x60), mu
def build(i):
    name, V, dV, y60, top = model(i)
    for k in range(1, 60):
        y0 = top - (top - y60)*0.85**k
        try:
            m = Model(V, dV, y0, Nmax=4000)
            if m.Nend >= 75: return name, V, dV, y0, m
        except Exception: pass
    raise RuntimeError('no start with >= 75 e-folds')
L = []; D = {k: [] for k in ('nj', 'na', 'rj', 'ra', 'aj', 'aa', 't')}
for i in range(1, 6):
    try: name, V, dV, y0, m = build(i); bg = Background(V, dV, y0, Nmax=4000)
    except Exception as e: L.append(f"model {i}: Janus could not build ({e}) — listed, not scored"); continue
    for N in (50.0, 60.0):
        t = time.time(); j = spectra3(m, N); tj = time.time() - t; b = spectra_fast(bg, N, dlnk=DL, bd=1000.0); a = A[(i, N)]
        x = (abs(j['ns']-b['ns']), abs(a['ns']-b['ns']), abs(j['r']/b['r']-1), abs(a['r']/b['r']-1), abs(j['alpha_s']-b['alpha_s']), abs(a['a']-b['alpha_s']))
        for key, v in zip(('nj', 'na', 'rj', 'ra', 'aj', 'aa'), x): D[key].append(v)
        D['t'].append(tj)
        L.append(f"{name:18s} N*={N:.0f} (exact ns {b['ns']:.6f} r {b['r']:.3e} a {b['alpha_s']:.3e}) | dns J {x[0]:.1e} A {x[1]:.1e} | dr/r J {x[2]:.1e} A {x[3]:.1e} | da J {x[4]:.1e} A {x[5]:.1e} | J {tj*1e3:.1f} ms")
        print(L[-1], flush=True)
md = np.median
C1 = bool(md(D['nj']) <= md(D['na'])/10 and max(D['nj']) < max(D['na'])); C2 = bool(md(D['rj']) <= md(D['ra'])/3); C3 = bool(md(D['aj']) <= md(D['aa'])); C4 = bool(md(D['t']) <= 0.1)
nb = sum(D['nj'][q] < D['na'][q] for q in range(len(D['nj'])))
L.append(f"{len(D['nj'])} points; Janus n_s better on {nb}/{len(D['nj'])}")
L.append(f"medians: dns J {md(D['nj']):.1e} A {md(D['na']):.1e} (max {max(D['nj']):.1e} vs {max(D['na']):.1e}) | dr/r {md(D['rj']):.1e} vs {md(D['ra']):.1e} | da {md(D['aj']):.1e} vs {md(D['aa']):.1e}")
L.append(f"C1 {C1} C2 {C2} C3 {C3} C4 {C4} -> {'JANUS MORE ACCURATE' if (C1 and C2 and C3) else 'NOT SHOWN'}")
open('field_tests/results/janus_j7d_twoparam.txt', 'w').write('\n'.join(L)+'\n'); print('\n'.join(L[-3:]))
