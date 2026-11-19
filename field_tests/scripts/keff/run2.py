"""PREREG_KEFF2.md. Usage: python3 run2.py chart k C | python3 run2.py model NAME | python3 run2.py read"""
import json, math, sys, os, tempfile, glob, subprocess
sys.path.insert(0, '.')
import numpy as np
from scipy.interpolate import CubicSpline
mode = sys.argv[1]; OUT = 'field_tests/results/KEFF2'; os.makedirs(OUT, exist_ok=True)
def run_F(setup, C):
    from tools.serapis_calc import pipeline as P
    from tools.serapis_calc.nstar import Nstar
    from tools.janus_calc.core import Model, spectra3
    os.environ['AEGIS_CACHE'] = tempfile.mkdtemp(); P._EGRID.clear(); setup(P)
    _b = P.build
    def _build(model='serapis_e', C=1.15e-6, lam=1.0, ymax=3000, npts=4000):
        mm, V, dV, p0 = _b(model, C, lam, ymax, npts); ph, _ = P._egrid(model, lam, ymax, npts); lo, hi = 10, len(ph) - 5
        for _ in range(14):
            mid = (lo + hi)//2
            try: ne = P.Background(V, dV, ph[mid]).Nend
            except Exception: ne = None
            if ne is None or ne > 140: hi = mid
            else: lo = mid
            if ne is not None and 100 <= ne <= 200: return mm, V, dV, ph[mid]
        return mm, V, dV, ph[lo]
    P.build = _build
    m, V, dV, p0 = P.build('serapis_e', C, 1.0); M = Model(V, dV, p0, Nmax=4000); Ve = V(M.sol.sol(M.Nend)[0]); N = 50.0
    for _ in range(40):
        a = spectra3(M, N); N2 = Nstar(a['r'], V(M.sol.sol(M.Nend - N)[0])/Ve, 8.94e8)
        if abs(N2 - N) < 1e-4: N = N2; break
        N = N2
    a = spectra3(M, N); phis = float(M.sol.sol(M.Nend - N)[0]); ys = math.exp(math.sqrt(2)*phis)
    ph, e = P._egrid('serapis_e', 1.0, 3000, 4000); L = CubicSpline(np.sqrt(2)*ph, np.log1p(e)); lny = math.log(ys)
    es = float(np.expm1(L(lny)))
    return dict(C=C, ns=float(a['ns']), r=float(a['r']), Nstar=N, ystar=ys, estar=es, tau=C*es, keff=float(L.derivative()(lny)))
if mode == 'chart':
    k, C = float(sys.argv[2]), float(sys.argv[3])
    def s(P): P.E_paper = lambda x, y: y**k
    row = dict(k=k, **run_F(s, C)); json.dump(row, open(f'{OUT}/chart_k{k}_C{C:g}.json', 'w'), indent=1); print(json.dumps(row))
elif mode == 'model':
    name = sys.argv[2]
    from tools.serapis_calc.shapes import E
    C = {'S': 1.25e-6, 'A1': 1.25e-6, 'B0': 0.0, 'M25': 1.25e-6, 'M50': 1.25e-6, 'U2': 1.25e-6}[name]
    def s(P):
        if name == 'U2': P.E_paper = lambda x, y: y**2
        elif name != 'S': P.E_paper = lambda x, y: E(complex(x, y), 1.5)
        orig = P._egrid
        def _eg(model, lam, ymax, npts):
            ph, x = orig(model, lam, ymax, npts)
            if name == 'B0': return ph, (1 + x)**2 - 1
            if name in ('M25', 'M50'):
                al = 0.25 if name == 'M25' else 0.5; Pp = al*x/(1 + x) + (1 - al)*(1 - 1/(1 + x)**2); return ph, Pp/(1 - Pp)
            return ph, x
        P._egrid = _eg
    row = dict(model=name, **run_F(s, C)); json.dump(row, open(f'{OUT}/model_{name}.json', 'w'), indent=1); print(json.dumps(row))
else:
    ok = lambda d: 0.9 < d['ns'] < 1.05 and 0 < d['r'] < 0.1 and 45 < d['Nstar'] < 60
    rows = {}
    for f in glob.glob(f'{OUT}/chart_*.json'):
        d = json.load(open(f))
        if ok(d): rows.setdefault(d['k'], []).append(d)
    ks = sorted(rows)
    def at_row(k, tau):
        R = sorted(rows[k], key=lambda d: d['tau']); t = [d['tau'] for d in R]
        if not (t[0] <= tau <= t[-1]): return None
        return {q: float(np.interp(tau, t, [d[q] for d in R])) for q in ('ns', 'r')}
    res = {}
    for f in sorted(glob.glob(f'{OUT}/model_*.json')):
        d = json.load(open(f)); k = d['keff']
        lo = [x for x in ks if x <= k]; hi = [x for x in ks if x >= k]
        pred = None
        if lo and hi:
            a, b = at_row(lo[-1], d['tau']), at_row(hi[0], d['tau'])
            if a and b:
                w = 0 if hi[0] == lo[-1] else (k - lo[-1])/(hi[0] - lo[-1]); pred = {q: (1-w)*a[q] + w*b[q] for q in a}
        inb = lambda ns, r: 0.969 <= ns <= 0.975 and 4.55e-4 <= r <= 5.7e-4
        if pred:
            dn = pred['ns'] - d['ns']; dr = pred['r']/d['r'] - 1; st = inb(pred['ns'], pred['r']) == inb(d['ns'], d['r'])
            res[d['model']] = dict(keff=d['keff'], tau=d['tau'], own=(d['ns'], d['r']), chart=(pred['ns'], pred['r']), dns=dn, dr=dr, status_ok=st,
                                   works=bool(abs(dn) <= 0.003 and abs(dr) <= 0.2 and st))
        else: res[d['model']] = dict(keff=d['keff'], tau=d['tau'], own=(d['ns'], d['r']), chart=None, works=False)
        print(d['model'], res[d['model']])
    json.dump(res, open(f'{OUT}/verdict.json', 'w'), indent=1)
