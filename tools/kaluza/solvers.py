# AEGIS-FP MVZMKBKHOEPVDCUV · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Two independent eigen-solvers (must agree before a number is used).
pruefer_SL: Sturm–Liouville (p u')' + m² w u = 0 by Prüfer angle, Neumann-type start θ = π/2 (S4c2, D1036).
pruefer_schrodinger: −Ψ'' + U Ψ = m² Ψ written in y with dz = J dy, Dirichlet or Neumann (S4e).
fd_schrodinger: second-order finite differences on a uniform z grid (S4e2 method)."""
import math, numpy as np
from scipy.integrate import solve_ivp, cumulative_trapezoid
from scipy.optimize import brentq
from scipy.linalg import eigh_tridiagonal
def _theta_SL(m2, p, w, a, b):
    s = solve_ivp(lambda yy, t: [math.cos(t[0])**2/p(yy) + m2*w(yy)*math.sin(t[0])**2], [a, b], [math.pi/2], method='Radau', rtol=1e-10, atol=1e-12)
    return s.y[0][-1]
def pruefer_SL(n, p, w, a, b, lo=1e-4, hi=1e4, ngrid=60):
    f = lambda m2: _theta_SL(m2, p, w, a, b) - math.pi/2 - n*math.pi
    g = np.geomspace(lo, hi, ngrid); v = [f(x) for x in g]
    for x0, x1, v0, v1 in zip(g, g[1:], v, v[1:]):
        if v0*v1 < 0: return brentq(f, x0, x1, xtol=1e-14, rtol=1e-12)
    return None
def pruefer_schrodinger(Uf, Jf, y1, y2, bc='D', nmodes=2, m2grid=None):
    th0 = 0.0 if bc == 'D' else math.pi/2
    def te(m2):
        return solve_ivp(lambda yy, t: [Jf(yy)*(math.cos(t[0])**2 + (m2 - Uf(yy))*math.sin(t[0])**2)], [y1, y2], [th0], method='LSODA', rtol=1e-9, atol=1e-11).y[0, -1]
    g = sorted(set(np.concatenate([np.linspace(-50, 0, 6), np.logspace(-2, 4, 160)]))) if m2grid is None else m2grid
    out = []; prev = None
    for m2 in g:
        v = te(m2)
        if prev is not None:
            for k in range(1, 40):
                tg = th0 + k*math.pi
                if (prev[1] - tg)*(v - tg) < 0: out.append(brentq(lambda x: te(x) - tg, prev[0], m2, xtol=1e-10))
        prev = (m2, v)
        if len(out) >= nmodes: break
    return sorted(out)[:nmodes]
def fd_schrodinger(Uf, Jf, y1, y2, N=8000, nmodes=2):
    ys = np.concatenate([np.geomspace(y1, y1 + 1e-2*(y2 - y1), 20000), np.linspace(y1 + 1e-2*(y2 - y1), y2, 200000)[1:]])
    zs = cumulative_trapezoid(Jf(ys), ys, initial=0.0); zg = np.linspace(0, zs[-1], N + 2); h = zg[1] - zg[0]
    Ug = np.interp(zg[1:-1], zs, Uf(ys))
    return list(eigh_tridiagonal(2/h**2 + Ug, -np.ones(N - 1)/h**2, select='i', select_range=(0, nmodes - 1))[0])
