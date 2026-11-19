"""PREREG_ANGLEGB.md — Kähler GB coupling on an angled path, first-order Guo–Schwarz."""
import json, math, sys, os
sys.path.insert(0, '.')
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.integrate import cumulative_trapezoid
from tools.serapis_calc.shapes import E
SQ2 = math.sqrt(2); A = 1.68e-11; NSTAR = 50.3
E3 = lambda y: E(complex(0.5, y), 1.5).real
def Dl(y, h=1e-3):
    L = lambda t: math.log(E3(y*math.exp(t)))
    return (-L(2*h) + 8*L(h) - 8*L(-h) + L(-2*h))/(12*h)
phg = np.linspace(math.log(1.2)/SQ2, math.log(3000)/SQ2, 5000); V0s = CubicSpline(phg, [(2*Dl(math.exp(SQ2*p))/3)**2 for p in phg])
def run(th, F0, s):
    c, sn = math.cos(th), math.sin(th)
    ps = phg/c; V = A*V0s(phg); V1 = A*V0s(phg, 1)*c; V2 = A*V0s(phg, 2)*c*c
    k = math.sqrt(2/3)*sn; xi = s*F0*np.exp(k*ps); x1 = k*xi; x2 = k*k*xi
    Q = V1/V + (4/3)*x1*V; Q1 = CubicSpline(ps, Q)(ps, 1)
    e1 = 0.5*Q*V1/V
    with np.errstate(all='ignore'):
        e2 = -Q*(V2/V1 - V1/V + Q1/Q); d1 = -(4/3)*x1*Q*V; d2 = -Q*(x2/x1 + V1/V + Q1/Q)
    ok = np.where(e1 >= 1)[0]
    if not len(ok): return dict(theta=th, F0=F0, s=s, error='no end')
    i0 = ok[-1]
    if np.any(Q[i0:] <= 0): return dict(theta=th, F0=F0, s=s, error='Q<=0 on path')
    N = cumulative_trapezoid(1/Q[i0:], ps[i0:], initial=0)
    if N[-1] < NSTAR: return dict(theta=th, F0=F0, s=s, error='N<50')
    j = i0 + int(np.searchsorted(N, NSTAR))
    ns = 1 - 2*e1[j] - (2*e1[j]*e2[j] - d1[j]*d2[j])/(2*e1[j] - d1[j]); r = 8*abs(2*e1[j] - d1[j])
    return dict(theta=th, F0=F0, s=s, ns=float(ns), r=float(r), y_star=float(math.exp(SQ2*phg[j])),
                in_band=bool(0.969 <= ns <= 0.975 and 4.55e-4 <= r <= 5.7e-4))
rows = [run(th, F0, s) for th in (0.01, 0.03, 0.1, 0.3, 0.6, 1.0) for F0 in (1e1, 1e2, 1e3, 1e4) for s in (1, -1)]
os.makedirs('field_tests/results/ANGLEGB', exist_ok=True); json.dump(rows, open('field_tests/results/ANGLEGB/rows.json', 'w'), indent=1)
for r_ in rows: print(json.dumps(r_))
