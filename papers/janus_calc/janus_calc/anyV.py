"""J1: any potential. Give V(phi) as a formula string (sympy syntax, variable 'phi', parameters as keywords) or a
callable; derivatives are exact (sympy) for strings, finite-difference (5-point) for callables. The start of the
background is found automatically: the field value where enough e-folds remain (slow-roll estimate, then refined)."""
import math, sympy as sp, numpy as np
from scipy.optimize import brentq
from .core import Model
_phi = sp.Symbol('phi', real=True)
def from_formula(expr, side=+1, Nwant=90.0, phi_end_guess=None, **params):
    """expr: e.g. '(1-exp(-sqrt(2/3)*phi))**2' or 'phi**2'. side=+1 if inflation rolls toward smaller phi (field starts large)."""
    e = sp.sympify(expr, locals={'phi': _phi, **{k: sp.Float(v) for k, v in params.items()}})
    V = sp.lambdify(_phi, e, 'math'); dV = sp.lambdify(_phi, sp.diff(e, _phi), 'math')
    return _auto(V, dV, side, Nwant)
def from_callable(V, side=+1, Nwant=90.0, h=1e-4):
    dV = lambda p: (-V(p+2*h) + 8*V(p+h) - 8*V(p-h) + V(p-2*h))/(12*h)
    return _auto(V, dV, side, Nwant)
def _auto(V, dV, side, Nwant):
    epsV = lambda p: 0.5*(dV(p)/V(p))**2
    # end of slow roll (eps_V = 1) scanning along the roll direction from a large field
    grid = np.linspace(0.02, 60, 6000)*side
    vals = [epsV(p) if V(p) > 0 else np.inf for p in grid]
    i_end = next(i for i in range(len(grid)) if vals[i] < 1)          # first point (small |phi|) that is slow-rolling
    p_end = grid[i_end]
    # slow-roll e-fold count N(phi) = int V/V' dphi from p_end outward; pick the start where N = Nwant
    def N(p):
        xs = np.linspace(p_end, p, 400); f = [V(x)/dV(x) for x in xs]
        return abs(np.trapezoid(f, xs))
    ok = [p for p in grid if V(p) > 0 and abs(dV(p)/V(p)) > 1e-10]     # stay where the slope is resolvable
    hi = ok[-1]
    p0 = brentq(lambda p: N(p) - Nwant, p_end + 1e-3*side, hi) if N(hi) > Nwant else hi
    return Model(V, dV, p0, Nmax=max(400.0, 3*Nwant))
