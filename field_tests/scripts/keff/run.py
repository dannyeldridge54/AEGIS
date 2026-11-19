"""PREREG_KEFF.md. Usage: python3 run.py MODEL  (S, A1, B0, M25, M50, U2)"""
import json, math, sys, os, tempfile, glob
sys.path.insert(0, '.')
import numpy as np
from scipy.interpolate import CubicSpline
from tools.serapis_calc import pipeline as P
from tools.serapis_calc.nstar import Nstar
from tools.serapis_calc.shapes import E
from tools.janus_calc.core import Model, spectra3
name = sys.argv[1]; TR = 8.94e8
os.environ['AEGIS_CACHE'] = tempfile.mkdtemp(); P._EGRID.clear()
C = {'S': 1.25e-6, 'A1': 1.25e-6, 'B0': 0.0, 'M25': 1.25e-6, 'M50': 1.25e-6, 'U2': 1.25e-6}[name]
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
    a = spectra3(M, N); N2 = Nstar(a['r'], V(M.sol.sol(M.Nend - N)[0])/Ve, TR)
    if abs(N2 - N) < 1e-4: N = N2; break
    N = N2
a = spectra3(M, N); phis = float(M.sol.sol(M.Nend - N)[0]); ys = math.exp(math.sqrt(2)*phis)
ph, e = P._egrid('serapis_e', 1.0, 3000, 4000); L = CubicSpline(np.sqrt(2)*ph, np.log1p(e)); keff = float(L.derivative()(math.log(ys)))
# UCHART bilinear prediction at (keff, C)
D = {}
for f in glob.glob('field_tests/results/UCHART/F_*.json'):
    d = json.load(open(f))
    if 0.9 < d['ns'] < 1.05 and 0 < d['r'] < 0.1 and 45 < d['Nstar'] < 60: D[(d['k'], d['C'])] = d
ks = sorted({k for k, _ in D}); Cs = sorted({c for _, c in D})
i = max(j for j in range(len(ks) - 1) if ks[j] <= keff) if ks[0] <= keff <= ks[-1] else None
pred = None
if i is not None:
    j = max(jj for jj in range(len(Cs) - 1) if Cs[jj] <= C) if C < Cs[-1] else len(Cs) - 2
    k0, k1, c0, c1 = ks[i], ks[i+1], Cs[j], Cs[j+1]; tk = (keff - k0)/(k1 - k0); tc = (C - c0)/(c1 - c0)
    try:
        pred = {q: (1-tk)*(1-tc)*D[(k0,c0)][q] + tk*(1-tc)*D[(k1,c0)][q] + (1-tk)*tc*D[(k0,c1)][q] + tk*tc*D[(k1,c1)][q] for q in ('ns', 'r')}
    except KeyError: pred = 'corner invalid'
row = dict(model=name, C=C, keff=keff, ystar=ys, Nstar=N, ns_F=float(a['ns']), r_F=float(a['r']), chart=pred)
print(json.dumps(row)); os.makedirs('field_tests/results/KEFF', exist_ok=True); json.dump(row, open(f'field_tests/results/KEFF/{name}.json', 'w'), indent=1)
