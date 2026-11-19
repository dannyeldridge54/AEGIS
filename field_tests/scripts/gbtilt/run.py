"""PREREG_GBTILT.md — first-order Gauss–Bonnet slow roll (Guo–Schwarz) on the P3-S shape with ξ = ξ0 (E_{3/2} − E_ρ)."""
import json, math, sys, os
sys.path.insert(0, '.')
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.integrate import cumulative_trapezoid
from tools.serapis_calc.shapes import E
SQ2 = math.sqrt(2); yr = math.sqrt(3)/2; A = 1.68e-11; NSTAR = 50.3
E3 = lambda y: E(complex(0.5, y), 1.5).real
def Dl(y, h=1e-3):
    L = lambda t: math.log(E3(y*math.exp(t)))
    return (-L(2*h) + 8*L(h) - 8*L(-h) + L(-2*h))/(12*h)
ph = np.linspace(math.log(1.2)/SQ2, math.log(3000)/SQ2, 6000); ys = np.exp(SQ2*ph)
V0 = np.array([(2*Dl(y)/3)**2 for y in ys]); Ev = np.array([E3(y) for y in ys]) - E3(yr)
sV = CubicSpline(ph, A*V0); sE = CubicSpline(ph, Ev)
def run(xi0):
    V = sV(ph); V1 = sV(ph, 1); V2 = sV(ph, 2); x1 = xi0*sE(ph, 1); x2 = xi0*sE(ph, 2)
    Q = V1/V + (4/3)*x1*V
    Qs = CubicSpline(ph, Q); Q1 = Qs(ph, 1)
    e1 = 0.5*Q*V1/V
    with np.errstate(all='ignore'):
        e2 = -Q*(V2/V1 - V1/V + Q1/Q); d1 = -(4/3)*x1*Q*V; d2 = -Q*(x2/x1 + V1/V + Q1/Q) if xi0 != 0 else 0*Q
    ok = np.where(e1 >= 1)[0]
    if not len(ok): return dict(xi0=xi0, error='no end')
    iend = ok[-1]
    if np.any(Q[iend:] <= 0): return dict(xi0=xi0, error='Q<=0 on path (GB reverses roll)')
    N = cumulative_trapezoid(1/Q[iend:], ph[iend:], initial=0)
    if N[-1] < NSTAR: return dict(xi0=xi0, error='N<50')
    j = iend + int(np.searchsorted(N, NSTAR))
    ns = 1 - 2*e1[j] - (2*e1[j]*e2[j] - (d1[j]*d2[j] if xi0 else 0))/(2*e1[j] - d1[j])
    r = 8*abs(2*e1[j] - d1[j])
    return dict(xi0=xi0, ns=float(ns), r=float(r), y_star=float(ys[j]), eps1=float(e1[j]), delta1=float(d1[j]),
                in_band=bool(0.969 <= ns <= 0.975 and 4.55e-4 <= r <= 5.7e-4))
rows = [run(0.0)] + [run(sg*10**(k/2)) for sg in (1, -1) for k in range(0, 21)]
os.makedirs('field_tests/results/GBTILT', exist_ok=True); json.dump(rows, open('field_tests/results/GBTILT/rows.json', 'w'), indent=1)
for r_ in rows: print(json.dumps(r_))
