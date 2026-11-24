"""D2238 B: Lengyel seeded-divertor estimate on the D2237 machines (ESTIMATE)."""
import json, math, sys
import numpy as np
sys.path.insert(0, 'tools/fusion'); import adas as AD
rows = json.load(open('field_tests/results/d2237_lead.json'))
geo = {'ITER control': (6.2, 5.3), 'Nb3Sn R9 B6': (9.0, 6.0), 'Nb3Sn R8 B8': (8.0, 8.0)}
src = open('theory/tests/d2236_helm.py').read().split('out = []')[0]; g = {}; sys.argv = ['x']; exec(src, g); machine = g['machine']
K0, Tt = 2390.0, 5.0
T = np.geomspace(Tt, 400.0, 400); L = np.maximum(AD.L_interp('ar', T / 1000.0), 0.0)
out = []
for r in rows:
    R, B = geo[r['machine']]; m = machine(R, B); a = m['a']
    Bp = 4e-7 * math.pi * m['Ip'] * 1e6 / (2 * math.pi * a * math.sqrt((1 + m['kappa'] ** 2) / 2)); lam = r['lambda_q_mm'] * 1e-3
    qpar = (2 / 3) * r['P_sep'] * 1e6 * B / (2 * math.pi * R * lam * Bp)
    Lc = math.pi * 3.0 * R; Tu = (3.5 * qpar * Lc / K0) ** (2 / 7)
    sel = T <= Tu; I = np.trapezoid(np.sqrt(T[sel]) * L[sel], T[sel])
    nG = m['Ip'] / (math.pi * a ** 2) * 1e20
    nav = {'ITER control': 0.936, 'Nb3Sn R9 B6': None, 'Nb3Sn R8 B8': None}
    n_avg = r.get('n_avg') or nG * 0.85; nu = 0.4 * n_avg
    c = qpar ** 2 / (2 * K0 * nu ** 2 * Tu ** 2 * I)
    pen = {cmp: (1 - 16 * c / cmp) ** 2 for cmp in (1.0, 3.0)}
    out.append(dict(machine=r['machine'], q_par_u_GW_m2=qpar / 1e9, T_u_eV=Tu, c_Ar_SOL=c, Pfus_factor_compression1=pen[1.0], Pfus_factor_compression3=pen[3.0],
                    workable=bool(c <= 0.05 and pen[3.0] >= 0.8), n_u_assumed=nu))
json.dump(out, open('field_tests/results/d2238_divertor.json', 'w'), indent=1)
for o in out: print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in o.items()})
