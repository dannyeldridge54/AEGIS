# AEGIS-FP 6YMSXWBR5VYTR3KX · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""J7b (locked PREREG_J7b_aspic_wide). Usage: python3 ... r0 | run | summary. Resumable jsonl."""
import sys, os, json, time, math, numpy as np, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
from tools.janus_calc.core import Model, spectra3
from tools.serapis_calc.ms import Background, spectra_fast
PART = 'field_tests/results/janus_j7b.part.jsonl'; ASP = 'theory/janus/aspic/aspic_j7b_clean.txt'
DL = tuple(np.linspace(-1, 1, 9)); s23 = math.sqrt(2/3)
A = {}
for l in open(ASP):
    c = l.split(); A[(int(c[0]), float(c[1]))] = dict(x=float(c[2]), ns=float(c[3]), r=float(c[4]), a=float(c[5]), t=float(c[7]))
def model(i):
    """returns name, V(y), dV(y), y60 (Janus coordinate of ASPIC x*(60)), top (None for open plateau/power)."""
    x60 = A[(i, 60.0)]['x']
    if i in (1, 2, 3, 16, 17):
        p = {1: 2, 2: 4, 3: 2/3, 16: 3, 17: 1}[i]; return f'LFI p={p:.4g}', (lambda y: y**p), (lambda y: p*y**(p-1)), x60, None
    if i == 4: return 'SI', (lambda y: (1-math.exp(-s23*y))**2), (lambda y: 2*(1-math.exp(-s23*y))*s23*math.exp(-s23*y)), x60, None
    if i in (5, 6, 15):
        f = {5: 5., 6: 10., 15: 7.}[i]; top = math.pi*f
        return f'NI f={f:g}', (lambda y: 1-math.cos(y/f)), (lambda y: math.sin(y/f)/f), top - x60, top
    if i in (7, 14):
        q = {7: 1.0, 14: math.sqrt(2)}[i]; return f'ESI q={q:.4g}', (lambda y: 1-math.exp(-q*y)), (lambda y: q*math.exp(-q*y)), x60, None
    if i == 8:
        mu = 10.; return 'MHI mu=10', (lambda y: 1-1/math.cosh(y/mu)), (lambda y: math.tanh(y/mu)/math.cosh(y/mu)/mu), mu*x60, None
    if i == 10:
        al = 1.; return 'RGI a=1', (lambda y: y*y/(al+y*y)), (lambda y: 2*al*y/(al+y*y)**2), x60, None
    if i == 11:
        p0 = 25.; X = lambda y: 1-y/p0
        return 'DWI phi0=25', (lambda y: (X(y)**2-1)**2), (lambda y: -4*X(y)*(X(y)**2-1)/p0), p0*(1-x60), p0
    if i == 12:
        mu = 20.; X = lambda y: 1-y/mu
        return 'SFI p=2 mu=20', (lambda y: 1-X(y)**2), (lambda y: 2*X(y)/mu), mu*(1-x60), mu
    if i == 13:
        al = 0.3; return 'LI a=0.3', (lambda y: 1+al*math.log(y)), (lambda y: al/y), x60, None
def build(i):
    name, V, dV, y60, top = model(i)
    for k in range(1, 40):
        y0 = (y60 + 0.5*k*max(1.0, 0.1*y60)) if top is None else top - (top - y60)*0.8**k
        try:
            m = Model(V, dV, y0, Nmax=3000)
            if m.Nend >= 75: return name, V, dV, y0, m
        except Exception: pass
    raise RuntimeError('no start with >= 75 e-folds')
def r0():
    L = []
    for i in (1, 4):
        name, V, dV, y0, m = build(i); bg = Background(V, dV, y0, Nmax=3000)
        a = spectra_fast(bg, 60.0, dlnk=DL, bd=1000.0); b = spectra_fast(bg, 60.0, dlnk=tuple(np.linspace(-.5, .5, 9)), bd=2000.0)
        L.append(f"R0 {name} N*=60: alpha_s [-1,1],bd1000 {a['alpha_s']:.6e} | [-.5,.5],bd2000 {b['alpha_s']:.6e} | |d| {abs(a['alpha_s']-b['alpha_s']):.1e}")
    ok = all(float(l.split('|d| ')[1]) <= 2e-5 for l in L); L.append(f"R0 {'PASS' if ok else 'FAIL'}")
    open('field_tests/results/janus_j7b_r0.txt', 'w').write('\n'.join(L)+'\n'); print('\n'.join(L))
def run():
    done = set()
    if os.path.exists(PART): done = {(json.loads(l)['i'], json.loads(l)['N']) for l in open(PART) if l.strip()}
    for i in [k for k in range(1, 18) if k != 9]:
        if all((i, N) in done for N in (50.0, 60.0)): continue
        name, V, dV, y0, m = build(i); bg = Background(V, dV, y0, Nmax=3000)
        for N in (50.0, 60.0):
            if (i, N) in done: continue
            t = time.time(); j = spectra3(m, N); tj = time.time() - t
            t = time.time(); b = spectra_fast(bg, N, dlnk=DL, bd=1000.0); tb = time.time() - t
            rec = dict(i=i, name=name, N=N, y0=y0, Ntot=m.Nend, ns_j=float(j['ns']), r_j=float(j['r']), a_j=float(j['alpha_s']),
                       ns_b=float(b['ns']), r_b=float(b['r']), a_b=float(b['alpha_s']), tj=tj, tb=tb)
            open(PART, 'a').write(json.dumps(rec)+'\n'); print(rec, flush=True)
def summary():
    R = {(r['i'], r['N']): r for r in (json.loads(l) for l in open(PART) if l.strip())}
    r0ok = open('field_tests/results/janus_j7b_r0.txt').read().strip().endswith('PASS')
    L = ['KMII a=2: no prediction from ASPIC (its own message: never-ending inflation for this alpha; V has a positive minimum 1-2/e) -- not scored']
    D = {k: [] for k in ('nj', 'na', 'rj', 'ra', 'aj', 'aa', 't')}
    for k in sorted(R):
        r, a = R[k], A[k]
        x = (abs(r['ns_j']-r['ns_b']), abs(a['ns']-r['ns_b']), abs(r['r_j']/r['r_b']-1), abs(a['r']/r['r_b']-1), abs(r['a_j']-r['a_b']), abs(a['a']-r['a_b']))
        for key, v in zip(('nj', 'na', 'rj', 'ra', 'aj', 'aa'), x): D[key].append(v)
        D['t'].append(r['tj'])
        L.append(f"{r['name']:14s} N*={r['N']:.0f} (exact ns {r['ns_b']:.6f} r {r['r_b']:.3e} a {r['a_b']:.3e}) | dns J {x[0]:.1e} A {x[1]:.1e} | dr/r J {x[2]:.1e} A {x[3]:.1e} | da J {x[4]:.1e} A {x[5]:.1e} | J {r['tj']*1e3:.1f} ms")
    md = np.median; nb = sum(D['nj'][i] < D['na'][i] for i in range(len(D['nj'])))
    C1 = bool(md(D['nj']) <= md(D['na'])/10 and max(D['nj']) < max(D['na'])); C2 = bool(md(D['rj']) <= md(D['ra'])/3)
    C3 = bool(md(D['aj']) <= md(D['aa'])) if r0ok else 'UNRESOLVED'; C4 = md(D['t']) <= 0.1
    L.append(f"{len(R)} points scored; Janus n_s better on {nb}/{len(R)}")
    L.append(f"medians: dns J {md(D['nj']):.1e} A {md(D['na']):.1e} (max {max(D['nj']):.1e} vs {max(D['na']):.1e}) | dr/r {md(D['rj']):.1e} vs {md(D['ra']):.1e} | da {md(D['aj']):.1e} vs {md(D['aa']):.1e} | t {md(D['t'])*1e3:.1f} ms")
    ok = C1 and C2 and (C3 is True or C3 == 'UNRESOLVED')
    L.append(f"R0 {'PASS' if r0ok else 'FAIL'}; C1 {C1} C2 {C2} C3 {C3} C4 {C4} -> {'JANUS MORE ACCURATE' if ok else 'NOT SHOWN'}")
    open('field_tests/results/janus_j7b_wide.txt', 'w').write('\n'.join(L)+'\n'); print('\n'.join(L))
if __name__ == '__main__': {'r0': r0, 'run': run, 'summary': summary}[sys.argv[1]]()
