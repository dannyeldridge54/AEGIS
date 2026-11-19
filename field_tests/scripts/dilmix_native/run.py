"""PREREG_DILMIX_NATIVE.md. Usage: python3 run.py alpha C_n   (native tilt V = P(x)(1 + C_n x))"""
import json, math, sys, os, tempfile, time
sys.path.insert(0, '.')
import numpy as np
from scipy.interpolate import CubicSpline
from tools.serapis_calc import pipeline as P
from tools.serapis_calc.shapes import E
al, Cn = float(sys.argv[1]), float(sys.argv[2])
P.E_paper = lambda x, y: E(complex(x, y), 1.5)
os.environ['AEGIS_CACHE'] = tempfile.mkdtemp(); P._EGRID.clear()
def _build(model='serapis_e', C=0.0, lam=1.0, ymax=3000, npts=4000):
    mm = P.MODELS[model]; ph, x = P._egrid(model, lam, ymax, npts)
    S = CubicSpline(ph, x); dS = S.derivative()
    Pf = lambda u: al*u/(1+u) + (1-al)*(1 - 1/(1+u)**2)
    dPf = lambda u: al/(1+u)**2 + 2*(1-al)/(1+u)**3
    V = lambda p: (lambda u: Pf(u)*(1 + Cn*u))(float(S(p)))
    dV = lambda p: (lambda u, du: du*(dPf(u)*(1 + Cn*u) + Pf(u)*Cn))(float(S(p)), float(dS(p)))
    lo, hi = 10, len(ph) - 5
    for _ in range(14):
        mid = (lo + hi)//2; ne = P.Background(V, dV, ph[mid]).Nend
        if ne is None or ne > 140: hi = mid
        else: lo = mid
        if ne is not None and 100 <= ne <= 200: return mm, V, dV, ph[mid]
    return mm, V, dV, ph[lo]
P.build = _build
t = time.time(); r = P.predict('serapis_e', C=0.0, TR=8.94e8, lam=1.0)
inb = 0.969 <= r['ns'] <= 0.975 and 4.55e-4 <= r['r'] <= 5.7e-4
near = abs(min(max(r['ns'], 0.969), 0.975) - r['ns']) <= 0.003 and 4.55e-4/1.3 <= r['r'] <= 5.7e-4*1.3
row = dict(alpha=al, C_native=Cn, ns=float(r['ns']), r=float(r['r']), alpha_s=float(r['alpha_s']), Nstar=float(r['Nstar']), in_band=bool(inb), near=bool(near), seconds=round(time.time() - t, 1))
print(json.dumps(row), flush=True); os.makedirs('field_tests/results/DILMIX_NATIVE', exist_ok=True)
json.dump(row, open(f'field_tests/results/DILMIX_NATIVE/a{al:g}_Cn{Cn:g}.json', 'w'), indent=1)
