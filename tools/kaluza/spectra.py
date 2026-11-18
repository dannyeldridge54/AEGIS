# AEGIS-FP 2JTULM42XTGGYSIY · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Operators built from a background (background.vacuum)."""
import sympy as sp
from .background import y
def tensor_pw(bg):
    """Sturm–Liouville weights for the tensor (spin-2) tower used in S4c2/S4c3 (D1036): p = e^{(D−1)A + γP/2}, w = e^{(D−3)A − γP/2}."""
    D, g, A, P = bg['D'], bg['gam'], bg['A'], bg['P']
    p = sp.exp((D - 1)*A + g*P/2); w = sp.exp((D - 3)*A - g*P/2)
    return sp.lambdify(y, p, 'math'), sp.lambdify(y, w, 'math')
def scalar_UJ(bg):
    """Scalar master operator (BTR Eqs. 5.3–5.9) in Schrödinger form, U = b + W² + W', dz = e^{B−A} dy, V₀ = 2e^{γφ} (S4e convention; FLAGGED unvalidated)."""
    D, g, A, P = bg['D'], bg['gam'], bg['A'], bg['P']
    B = -g*P/2; V0 = 2*sp.exp(g*P); J = sp.exp(B - A); Ay, Py = sp.diff(A, y), sp.diff(P, y)
    W = (D - 2)/2*(3*Ay/J - sp.exp(2*A)*g*V0*J/(4*Py)); b = 2*(D - 3)*sp.exp(2*A)*V0*(1/(D - 2) + (D - 2)/8*g*Ay/Py)
    U = b + W**2 + sp.diff(W, y)/J
    f = lambda e: sp.lambdify(y, e, 'numpy')
    return f(U), f(J), f(sp.exp(B))
