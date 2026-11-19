"""PREREG_UCHART.md. Usage: python3 run.py F k C   (fast)   |  python3 run.py X k C  (exact)  |  python3 run.py S C (exact SERAPIS-E ref)"""
import json, math, sys, os, tempfile, time
sys.path.insert(0, '.')
from tools.serapis_calc import pipeline as P
from tools.serapis_calc.nstar import Nstar
mode = sys.argv[1]; TR = 8.94e8
os.environ['AEGIS_CACHE'] = tempfile.mkdtemp(); P._EGRID.clear()
if mode in 'FX':
    k, C = float(sys.argv[2]), float(sys.argv[3]); P.E_paper = lambda x, y: y**k
else:
    k, C = 'E2', float(sys.argv[2])
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
t = time.time()
if mode == 'F':
    from tools.janus_calc.core import Model, spectra3
    m, V, dV, p0 = P.build('serapis_e', C, 1.0); M = Model(V, dV, p0, Nmax=4000); Ve = V(M.sol.sol(M.Nend)[0]); N = 50.0
    for _ in range(40):
        a = spectra3(M, N); N2 = Nstar(a['r'], V(M.sol.sol(M.Nend - N)[0])/Ve, TR)
        if abs(N2 - N) < 1e-4: N = N2; break
        N = N2
    a = spectra3(M, N); r = dict(ns=a['ns'], r=a['r'], alpha_s=a['alpha_s'], Nstar=N)
else:
    r = P.predict('serapis_e', C=C, TR=TR, lam=1.0)
inb = 0.969 <= r['ns'] <= 0.975 and 4.55e-4 <= r['r'] <= 5.7e-4
near = abs(min(max(r['ns'], 0.969), 0.975) - r['ns']) <= 0.003 and 4.55e-4/1.3 <= r['r'] <= 5.7e-4*1.3
row = dict(engine=mode, k=k, C=C, ns=float(r['ns']), r=float(r['r']), alpha_s=float(r['alpha_s']), Nstar=float(r['Nstar']),
           in_band=bool(inb), near=bool(near), seconds=round(time.time() - t, 1))
print(json.dumps(row), flush=True); os.makedirs('field_tests/results/UCHART', exist_ok=True)
json.dump(row, open(f'field_tests/results/UCHART/{mode}_k{k}_C{C:g}.json', 'w'), indent=1)
