"""J7m (locked PREREG_J7m_twoparam_grid). Same method as j7d_twoparam.py; new parameter points."""
import sys, time, math, numpy as np, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
from tools.janus_calc.core import Model, spectra3
from tools.serapis_calc.ms import Background, spectra_fast
DL = tuple(np.linspace(-1, 1, 9)); A = {}
for l in open('theory/janus/aspic/aspic_j7m_clean.txt'):
    c = l.split(); A[(int(c[0]), float(c[1]))] = dict(x=float(c[2]), ns=float(c[3]), r=float(c[4]), a=float(c[5]))
PTS = [('TI', .05, 6), ('TI', .05, 12), ('TI', .15, 6), ('TI', .15, 12), ('TI', .3, 6), ('TI', .3, 12),
       ('PSNI', 1e-4, 5), ('PSNI', 1e-2, 5), ('PSNI', 1e-3, 10), ('SFI', 1, 8), ('SFI', 3, 8), ('SFI', 3, 20)]
def model(i):
    kind, a, b = PTS[i-1]; x60 = A[(i, 60.0)]['x']
    if kind == 'TI':
        X = lambda y: y/b
        return f'TI a={a} mu={b}', (lambda y: 1 - math.cos(X(y)) + a*math.sin(X(y))**2), (lambda y: (math.sin(X(y)) + 2*a*math.sin(X(y))*math.cos(X(y)))/b), b*(math.pi - x60), b*math.pi
    if kind == 'PSNI':
        return f'PSNI a={a} f={b}', (lambda y: 1 + a*math.log(abs(math.sin(y/b)))), (lambda y: a*math.cos(y/b)/math.sin(y/b)/b), b*(math.pi/2 - x60), b*math.pi/2
    X = lambda y: 1 - y/b
    return f'SFI p={a} mu={b}', (lambda y: 1 - X(y)**a), (lambda y: a*X(y)**(a - 1)/b), b*(1 - x60), b
def build(i):
    name, V, dV, y60, top = model(i)
    if not (0 < y60 < top): raise RuntimeError(f'ASPIC x out of the model domain (y60 = {y60:.4g}, range 0..{top:.4g})')
    for k in range(1, 60):
        y0 = top - (top - y60)*0.85**k
        try:
            m = Model(V, dV, y0, Nmax=4000)
            if m.Nend >= 75: return name, V, dV, y0, m
        except Exception: pass
    raise RuntimeError('no start with >= 75 e-folds')
L = []; D = {k: [] for k in ('nj', 'na', 'rj', 'ra', 'aj', 'aa', 't')}
for i in range(1, 13):
    try: name, V, dV, y0, m = build(i); bg = Background(V, dV, y0, Nmax=4000)
    except Exception as e: L.append(f"point {i} {PTS[i-1]}: listed, not scored ({e})"); print(L[-1], flush=True); continue
    for N in (50.0, 60.0):
        try:
            t = time.time(); j = spectra3(m, N); tj = time.time() - t; b = spectra_fast(bg, N, dlnk=DL, bd=1000.0); a = A[(i, N)]
        except Exception as e:
            L.append(f"{name} N*={N:.0f}: listed, not scored ({e})"); print(L[-1], flush=True); continue
        x = (abs(j['ns']-b['ns']), abs(a['ns']-b['ns']), abs(j['r']/b['r']-1), abs(a['r']/b['r']-1), abs(j['alpha_s']-b['alpha_s']), abs(a['a']-b['alpha_s']))
        for key, v in zip(('nj', 'na', 'rj', 'ra', 'aj', 'aa'), x): D[key].append(v)
        D['t'].append(tj)
        L.append(f"{name:18s} N*={N:.0f} (exact ns {b['ns']:.6f} r {b['r']:.3e} a {b['alpha_s']:.3e}) | dns J {x[0]:.1e} A {x[1]:.1e} | dr/r J {x[2]:.1e} A {x[3]:.1e} | da J {x[4]:.1e} A {x[5]:.1e} | J {tj*1e3:.1f} ms")
        print(L[-1], flush=True)
md = np.median
if D['nj']:
    C1 = bool(md(D['nj']) <= md(D['na'])/10 and max(D['nj']) < max(D['na'])); C2 = bool(md(D['rj']) <= md(D['ra'])/3); C3 = bool(md(D['aj']) <= md(D['aa'])); C4 = bool(md(D['t']) <= 0.1)
    nb = sum(D['nj'][q] < D['na'][q] for q in range(len(D['nj'])))
    L.append(f"{len(D['nj'])} points scored; Janus n_s better on {nb}/{len(D['nj'])}")
    L.append(f"medians: dns J {md(D['nj']):.1e} A {md(D['na']):.1e} (max {max(D['nj']):.1e} vs {max(D['na']):.1e}) | dr/r {md(D['rj']):.1e} vs {md(D['ra']):.1e} | da {md(D['aj']):.1e} vs {md(D['aa']):.1e}")
    L.append(f"C1 {C1} C2 {C2} C3 {C3} C4 {C4} -> {'JANUS MORE ACCURATE' if (C1 and C2 and C3) else 'NOT SHOWN'}")
open('field_tests/results/janus_j7m_grid.txt', 'w').write('\n'.join(L)+'\n'); print('\n'.join(L[-3:]))
