"""D1398 (locked PREREG_D1398_fullY.md). Usage: python3 fullY.py T2"""
import json, math, sys, time, os, tempfile
sys.path.insert(0, '.')
from tools.serapis_calc import pipeline as P
from tools.serapis_calc.shapes import E
T2 = float(sys.argv[1]); s = 1.0; kap = 10.0; ET = E(complex(0, T2))
def L(x, y):
    Y = 6*math.pi*T2 + 90/math.pi**3*E(complex(x, y))/T2 if y <= T2 else 6*math.pi*y + 90/math.pi**3*ET/y
    return s + Y/(16*math.pi**2)
Lr = L(0.5, math.sqrt(3)/2); Li = L(0.0, 1.0)
out = dict(T2=T2, s=s, kappa=kap, L_rho=Lr, L_i=Li, vacuum_at_rho=bool(Lr < Li), rows=[])
P.E_paper = lambda x, y: kap*L(x, y)
os.environ['AEGIS_CACHE'] = tempfile.mkdtemp(); P._EGRID.clear()
for C in (0.0, 1e-4, 1e-3):
    t = time.time(); r = P.predict('serapis_e', C=C, TR=8.94e8, lam=1/(kap*Lr))
    m, V, dV, p0 = P.build('serapis_e', C, 1/(kap*Lr)); bg = P.Background(V, dV, p0)
    ystar = math.exp(bg.sol.sol(bg.Nend - r['Nstar'])[0]/math.sqrt(P.MODELS['serapis_e']['n']/2))
    row = dict(C=C, ns=float(r['ns']), r=float(r['r']), alpha_s=float(r['alpha_s']), Nstar=float(r['Nstar']), y_star=float(ystar),
               in_band=bool(0.969 <= r['ns'] <= 0.975 and 4.55e-4 <= r['r'] <= 5.7e-4), seconds=round(time.time() - t, 1))
    out['rows'].append(row); print(json.dumps(row), flush=True)
    json.dump(out, open(f'field_tests/results/D1398_fullY_T{int(T2)}.json', 'w'), indent=1)
