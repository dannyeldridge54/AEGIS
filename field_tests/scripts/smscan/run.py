"""PREREG_SMSCAN.md. Usage: python3 run.py s m"""
import json, math, sys, os, tempfile, time
sys.path.insert(0, '.')
from tools.serapis_calc import pipeline as P
from tools.serapis_calc.shapes import E
s, m = float(sys.argv[1]), float(sys.argv[2]); Er = E(complex(0.5, math.sqrt(3)/2), s)
P.E_paper = lambda x, y: (E(complex(x, y), s)/Er)**m
_b = P.build
def _build(model='serapis_e', C=1.15e-6, lam=1.0, ymax=3000, npts=4000):
    mm, V, dV, p0 = _b(model, C, lam, ymax, npts); ph, _ = P._egrid(model, lam, ymax, npts); lo, hi = 10, len(ph) - 5
    for _ in range(14):
        mid = (lo + hi)//2; ne = P.Background(V, dV, ph[mid]).Nend
        if ne is None or ne > 140: hi = mid
        else: lo = mid
        if ne is not None and 100 <= ne <= 200: return mm, V, dV, ph[mid]
    return mm, V, dV, ph[lo]
P.build = _build
os.environ['AEGIS_CACHE'] = tempfile.mkdtemp(); P._EGRID.clear(); t = time.time()
r = P.predict('serapis_e', C=0.0, TR=8.94e8, lam=1.0)
inb = 0.969 <= r['ns'] <= 0.975 and 4.55e-4 <= r['r'] <= 5.7e-4
near = abs(min(max(r['ns'], 0.969), 0.975) - r['ns']) <= 0.003 and 4.55e-4/1.3 <= r['r'] <= 5.7e-4*1.3
row = dict(s=s, m=m, sm=s*m, ns=float(r['ns']), r=float(r['r']), alpha_s=float(r['alpha_s']), Nstar=float(r['Nstar']),
           in_band=bool(inb), near=bool(near), seconds=round(time.time() - t, 1))
print(json.dumps(row), flush=True); os.makedirs('field_tests/results/SMSCAN', exist_ok=True)
json.dump(row, open(f'field_tests/results/SMSCAN/s{s:g}_m{m:.4g}.json', 'w'), indent=1)
