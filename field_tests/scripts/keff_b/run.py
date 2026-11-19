"""PREREG_KEFF.md — k_eff at horizon exit for each P3 route, and the UCHART read-off."""
import json, math, sys, os, tempfile, glob
sys.path.insert(0, '.')
import numpy as np
from scipy.interpolate import CubicSpline, RegularGridInterpolator
from tools.serapis_calc import pipeline as P
from tools.serapis_calc.eisenstein import E_paper as E2
from tools.serapis_calc.shapes import E
from tools.serapis_calc.nstar import Nstar
from tools.janus_calc.core import Model, spectra3
TR = 8.94e8; SQ2 = math.sqrt(2)
def egrid(src, mapf):
    os.environ['AEGIS_CACHE'] = tempfile.mkdtemp(); P._EGRID.clear(); P.E_paper = src
    ph, x = P._egrid('serapis_e', 1.0, 3000, 4000); return ph, mapf(x)
def run(name, src, mapf, C, exact):
    ph, e = egrid(src, mapf); S = CubicSpline(ph, e); dS = S.derivative()
    V = lambda p: (lambda u: u/(u+1)*(1 + C*u))(float(S(p)))
    dV = lambda p: (lambda u, du: du*((1 + C*u)/(u+1)**2 + C*u/(u+1)))(float(S(p)), float(dS(p)))
    lo, hi = 10, len(ph) - 5; p0 = None
    for _ in range(14):
        mid = (lo + hi)//2
        try: ne = P.Background(V, dV, ph[mid]).Nend
        except Exception: ne = None
        if ne is None or ne > 140: hi = mid
        else: lo = mid
        if ne is not None and 100 <= ne <= 200: p0 = ph[mid]; break
    p0 = p0 if p0 is not None else ph[lo]
    M = Model(V, dV, p0, Nmax=4000); Ve = V(M.sol.sol(M.Nend)[0]); N = 50.0
    for _ in range(40):
        a = spectra3(M, N); N2 = Nstar(a['r'], V(M.sol.sol(M.Nend - N)[0])/Ve, TR)
        if abs(N2 - N) < 1e-4: N = N2; break
        N = N2
    a = spectra3(M, N); ps = M.sol.sol(M.Nend - N)[0]; u = float(S(ps)); du = float(dS(ps))
    keff = du/(u + 1)/SQ2
    return dict(route=name, C=C, k_eff=keff, y_star=math.exp(SQ2*ps), F_ns=float(a['ns']), F_r=float(a['r']), Nstar=N, exact=exact)
def ex(path):
    d = json.load(open(path)); return dict(ns=d['ns'], r=d['r'])
E15 = lambda x, y: E(complex(x, y), 1.5)
mixf = lambda al: (lambda x: (lambda Pp: Pp/(1 - Pp))(al*x/(1 + x) + (1 - al)*(1 - 1/(1 + x)**2)))
R = 'field_tests/results/'
routes = [('SERAPIS-E', E2, lambda x: x, 1.25e-6, None),
          ('formA', E15, lambda x: x, 0.0, ex(R + 'DILATON32/A0.json')),
          ('formA', E15, lambda x: x, 1.25e-6, ex(R + 'DILATON32/A1.json')),
          ('formB', E15, lambda x: (1 + x)**2 - 1, 0.0, ex(R + 'DILATON32/B0.json'))]
for al in (0.25, 0.5, 0.75):
    for C in (1.25e-6, 2.5e-6):
        routes.append((f'DILMIX{al}', E15, mixf(al), C, ex(R + f'DILMIX/a{al:g}_C{C:g}.json')))
G = {}
for f in glob.glob(R + 'UCHART/F_*.json'):
    d = json.load(open(f))
    if 0.9 < d['ns'] < 1.05 and 0 < d['r'] < 0.1 and 45 < d['Nstar'] < 60: G[(d['k'], d['C'])] = d
ks = sorted({k for k, _ in G}); Cs = sorted({c for _, c in G})
def chart(k, C):
    out = {}
    for q in ('ns', 'r'):
        A = np.full((len(ks), len(Cs)), np.nan)
        for i, kk in enumerate(ks):
            for j, cc in enumerate(Cs):
                if (kk, cc) in G: A[i, j] = G[(kk, cc)][q]
        try: out[q] = float(RegularGridInterpolator((ks, Cs), A)((k, C)))
        except ValueError: out[q] = float('nan')
    return out
rows = []
for rt in routes:
    row = run(*rt); ch = chart(row['k_eff'], row['C']); row['chart'] = ch
    ref = row['exact'] or dict(ns=row['F_ns'], r=row['F_r'])
    row['d_ns'] = ch['ns'] - ref['ns']; row['dr_rel'] = ch['r']/ref['r'] - 1
    row['predicts'] = bool(abs(row['d_ns']) <= 0.002 and abs(row['dr_rel']) <= 0.15) if not math.isnan(ch['ns']) else None
    print(json.dumps(row), flush=True); rows.append(row)
os.makedirs(R + 'KEFF', exist_ok=True); json.dump(rows, open(R + 'KEFF/keff.json', 'w'), indent=1)
