"""Scalar KK masses on a BTR tadpole vacuum (any D, critical or subcritical) — Danny 2026-11-18 "add new tool".
kk_scalar(D, gamma, xi=(1e-4, 8.0), method='pruefer'|'fd', n=2, bc='D') -> dict(kind, m2, L, mL_over_pi, ratio, method).
The critical branch has an infinite interval; it is cut at ξ ∈ xi (the S4e convention, theory/strings/s4e_scalar_masses.py),
whose L changes < 1e-6 between ξ_max 7 and 8 (tested). Validated against D1214 (Prüfer 2.9795596, 14.286529; FD 2.9795592, 14.286527).
The master operator is the S4e convention — still 3.9%/4.2% off BTR 2209.10553's two-figure values (D1141, open)."""
import math
import sympy as sp
from scipy.integrate import quad
from .background import vacuum
from .spectra import scalar_UJ
from .solvers import pruefer_schrodinger, fd_schrodinger

def kk_scalar(D=10, gamma=1.5, xi=(1e-4, 8.0), method='pruefer', n=2, bc='D', N=8000):
    D = int(D); bg = vacuum(D, sp.nsimplify(gamma)); U, J, eB = scalar_UJ(bg)
    c = math.sqrt(2*(D - 1)/(D - 2)); x1, x2 = float(xi[0]), float(xi[1])
    y1 = x1/c; y2 = x2/c if bg['kind'] == 'critical' else min(x2/c, float(bg['y_end'])*(1 - 1e-6))
    if method == 'fd': m2 = [float(v) for v in fd_schrodinger(U, J, y1, y2, N=int(N), nmodes=int(n))]
    else: m2 = [float(v) for v in pruefer_schrodinger(U, J, y1, y2, bc=bc, nmodes=int(n))]
    L = quad(eB, y1, y2, limit=500, epsrel=1e-10)[0]
    return dict(kind=bg['kind'], D=D, gamma=float(gamma), m2=m2, L=L, mL_over_pi=[math.sqrt(v)*L/math.pi for v in m2 if v > 0],
                ratio=(m2[1]/m2[0] if len(m2) > 1 and m2[0] else None), method=method,
                note='scalar master operator, S4e convention (open −4% vs BTR, D1141/D1214)')

if __name__ == '__main__':
    import json, sys
    a = dict(arg.split('=', 1) for arg in sys.argv[1:] if '=' in arg)
    print(json.dumps(kk_scalar(int(a.get('D', 10)), float(a.get('gamma', 1.5)), method=a.get('method', 'pruefer')), indent=1))
