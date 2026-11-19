"""PREREG_DIM1_9D.md. Usage: python3 run.py c   (V0 = (y d ln(E32 + c)/1.5)^2)"""
import json, math, sys, os, cmath
sys.path.insert(0, '.')
import numpy as np
from scipy.interpolate import CubicSpline
from tools.serapis_calc.shapes import E
from tools.serapis_calc.eisenstein import E_paper
from tools.serapis_calc.nstar import Nstar
from tools.serapis_calc.ms import Background
from tools.janus_calc.core import Model, spectra3
cc = float(sys.argv[1]); lens, C = 'G32', 0.0; TR = 8.94e8; SQ2 = math.sqrt(2); yr = math.sqrt(3)/2
def lneta_abs(y, x=0.5):
    q = cmath.exp(2j*math.pi*complex(x, y)); s = -math.pi*y/12; qn = q
    for n in range(1, 400):
        s += math.log(abs(1 - qn)); qn *= q
        if abs(qn) < 1e-18: break
    return s
F = {'G32': lambda y: E(complex(0.5, y), 1.5).real + cc, 'G52': lambda y: E(complex(0.5, y), 2.5).real,
     'R2': lambda y: E_paper(0.5, y), 'N1': lambda y: -6*(math.log(2*y) + 4*lneta_abs(y))}[lens]
def Dl(y, h=1e-3):
    L = lambda t: math.log(F(y*math.exp(t)))
    return (-L(2*h) + 8*L(h) - 8*L(-h) + L(-2*h))/(12*h)
Fr = F(yr)
def V0(y):
    if lens == 'G32': return (Dl(y)/1.5)**2
    if lens == 'G52': return (Dl(y)/2.5)**2
    if lens == 'N1':  return Dl(y)**2
    e = max(0.063298*(F(y) - Fr), 1e-14); return e/(e + 1)
ph = np.linspace(math.log(yr)/SQ2 + 1e-4, math.log(3000)/SQ2, 4000); ys = np.exp(SQ2*ph)
v0 = np.array([V0(y) for y in ys]); X = np.array([F(y) - Fr for y in ys]); Vt = v0*(1 + C*X)
m = (ys > 20) & (ys < 200); kfit = float(-np.polyfit(np.log(ys[m]), np.log(np.abs(1 - v0[m])), 1)[0])
S = CubicSpline(ph, Vt); dS = S.derivative(); V = lambda p: float(S(p)); dV = lambda p: float(dS(p))
lo, hi = 10, len(ph) - 5; p0 = None
for _ in range(14):
    mid = (lo + hi)//2
    try: ne = Background(V, dV, ph[mid]).Nend
    except Exception: ne = None
    if ne is None or ne > 140: hi = mid
    else: lo = mid
    if ne is not None and 100 <= ne <= 200: p0 = ph[mid]; break
p0 = p0 if p0 is not None else ph[lo]
row = dict(stage='9D', c=cc, k_fit=kfit, V0_rho=float(V0(yr)))
try:
    M = Model(V, dV, p0, Nmax=4000); Ve = V(M.sol.sol(M.Nend)[0]); N = 50.0
    for _ in range(40):
        a = spectra3(M, N); N2 = Nstar(a['r'], V(M.sol.sol(M.Nend - N)[0])/Ve, TR)
        if abs(N2 - N) < 1e-4: N = N2; break
        N = N2
    a = spectra3(M, N); ps = M.sol.sol(M.Nend - N)[0]
    row.update(ns=float(a['ns']), r=float(a['r']), alpha_s=float(a['alpha_s']), Nstar=N, y_star=float(math.exp(SQ2*ps)),
               valid=bool(0.9 < a['ns'] < 1.05 and 0 < a['r'] < 0.1 and 45 < N < 60))
except Exception as ex:
    row.update(valid=False, error=str(ex)[:120])
print(json.dumps(row), flush=True); os.makedirs('field_tests/results/DIM_SLICE', exist_ok=True)
json.dump(row, open(f'field_tests/results/DIM_SLICE/c{cc:g}.json', 'w'), indent=1)
