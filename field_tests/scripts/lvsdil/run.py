"""PREREG_LVSDIL.md. Usage: python3 run.py k"""
import json, math, sys, os, tempfile, time
sys.path.insert(0, '.')
from tools.serapis_calc import pipeline as P
from tools.serapis_calc.shapes import E
k = float(sys.argv[1]); Er = E(complex(0.5, math.sqrt(3)/2), 1.5)
logF = lambda e: math.log(e)/3 - k*e**(2/3); lFr = logF(Er)   # DEVIATIONS D1: log space
vac_ok = bool(k*Er**(2/3) > 0.5)
P.E_paper = lambda x, y: math.expm1(min(lFr - logF(E(complex(x, y), 1.5)), 700.0)) + 1.0   # e = F(E_ρ)/F(E) − 1, capped (D1)
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
m, V, dV, p0 = P.build('serapis_e', 0.0, 1.0); bg = P.Background(V, dV, p0)
ystar = math.exp(bg.sol.sol(bg.Nend - r['Nstar'])[0]/math.sqrt(0.5))
row = dict(k=k, vacuum_at_rho=vac_ok, ns=float(r['ns']), r=float(r['r']), alpha_s=float(r['alpha_s']), Nstar=float(r['Nstar']),
           y_star=float(ystar), in_band=bool(0.969 <= r['ns'] <= 0.975 and 4.55e-4 <= r['r'] <= 5.7e-4), seconds=round(time.time() - t, 1))
print(json.dumps(row), flush=True); os.makedirs('field_tests/results/LVSDIL', exist_ok=True)
json.dump(row, open(f'field_tests/results/LVSDIL/k{k:g}.json', 'w'), indent=1)
