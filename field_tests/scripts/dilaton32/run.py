"""PREREG_DILATON32.md. Usage: python3 run.py A0|A1|A2|B0"""
import json, math, sys, os, tempfile, time
sys.path.insert(0, '.')
from tools.serapis_calc import pipeline as P
from tools.serapis_calc.shapes import E
run = sys.argv[1]; C = {'A0': 0.0, 'A1': 1.25e-6, 'A2': 1e-5, 'B0': 0.0}.get(run) if not run.startswith('C') else float(run[1:])   # CSCAN runs: 'C2e-6' etc.
P.E_paper = lambda x, y: E(complex(x, y), 1.5)
if run.startswith('B'):
    orig = P._egrid
    def _eg(model, lam, ymax, npts):
        ph, e = orig(model, lam, ymax, npts); return ph, (1 + e)**2 - 1
    P._egrid = _eg
_b = P.build
def _build(model='serapis_e', C=1.15e-6, lam=1.0, ymax=3000, npts=4000):
    m, V, dV, p0 = _b(model, C, lam, ymax, npts); ph, _ = P._egrid(model, lam, ymax, npts)
    lo, hi = 10, len(ph) - 5          # DEVIATIONS D1: bisect the start index so that N_end is in [100, 200] (target 140)
    for _ in range(14):
        mid = (lo + hi)//2; ne = P.Background(V, dV, ph[mid]).Nend
        if ne is None or ne > 140: hi = mid
        else: lo = mid
        if ne is not None and 100 <= ne <= 200: return m, V, dV, ph[mid]
    return m, V, dV, ph[lo]
P.build = _build
os.environ['AEGIS_CACHE'] = tempfile.mkdtemp(); P._EGRID.clear(); t = time.time()
TR = float(sys.argv[2]) if len(sys.argv) > 2 else 8.94e8   # PREREG_DILTR: optional T_R
r = P.predict('serapis_e', C=C, TR=TR, lam=1.0)
row = dict(run=run, C=C, TR=TR, ns=float(r['ns']), r=float(r['r']), alpha_s=float(r['alpha_s']), Nstar=float(r['Nstar']),
           in_band=bool(0.969 <= r['ns'] <= 0.975 and 4.55e-4 <= r['r'] <= 5.7e-4), seconds=round(time.time() - t, 1))
print(json.dumps(row), flush=True); os.makedirs('field_tests/results/DILATON32', exist_ok=True)
json.dump(row, open(f'field_tests/results/DILATON32/{run}' + (f'_TR{TR:g}' if len(sys.argv) > 2 else '') + '.json', 'w'), indent=1)
