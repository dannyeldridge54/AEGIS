# AEGIS-FP XO4TD6R4UVHQEGCA · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""SERAPIS plateau potentials (dimensionless V/V0) and a symbolic slope-sign check."""
import sympy as sp
from .eisenstein import E_fourier
RHO_Y = 3**0.5/2
def Ehat(y, x=0.5, s=2):
    return E_fourier(x, y, s) - E_fourier(0.5, RHO_Y, s)
def P3(E, C=0.0, lam=1.0):
    X = lam*E
    return X/(X+1)*(1+C*E)
def slope_sign_symbolic():
    """Return d(P3)/dE as a simplified expression; positive for E>=0, C>=0 means no turnaround."""
    E, C = sp.symbols('E C', nonnegative=True)
    return sp.factor(sp.diff(E/(E+1)*(1+C*E), E))
