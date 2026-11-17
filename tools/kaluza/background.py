"""General-D tadpole vacua (BTR 2209.10553 §3, action R − 4/(D−2)(∂φ)² − 2α_E e^{γφ}, gauge B = −γφ/2, α_E = 1, φ₀ = 0).
Returns sympy expressions A(y), P(y)=φ(y), the coordinate y, and the interval (y1, y2)."""
import sympy as sp
y = sp.symbols('y', positive=True)
def gamma_c(D): return 4*sp.sqrt(D - 1)/(D - 2)
def vacuum(D, gam):
    """Subcritical (−1/2 < δ < 0, trigonometric, BTR 3.9–3.11 as used in S4b) or critical (δ = 0, BTR 3.10)."""
    D = sp.Integer(D); gam = sp.nsimplify(gam); dl = sp.nsimplify((gam/gamma_c(D) - 1)/2)
    xi = sp.sqrt(2*(D - 1)/(D - 2))*y
    if dl == 0:
        A = -(xi**2/2 - sp.log(xi))/(2*(D - 1)); P = (D - 2)/(4*sp.sqrt(D - 1))*(xi**2/2 + sp.log(xi)); return dict(A=A, P=P, D=D, gam=gam, delta=dl, kind='critical', y_end=sp.oo)
    if -sp.Rational(1, 2) < dl < 0:
        w = sp.sqrt(-dl*(dl + 1))
        A = -sp.Rational(1, 2)/(D - 1)*sp.log(sp.cos(w*xi)**(1/dl)*sp.sin(w*xi)**(-1/(dl + 1)))
        P = (D - 2)/(4*sp.sqrt(D - 1))*sp.log(sp.cos(w*xi)**(1/dl)*sp.sin(w*xi)**(1/(dl + 1)))
        return dict(A=A, P=P, D=D, gam=gam, delta=dl, kind='subcritical', y_end=sp.pi/2/(w*sp.sqrt(2*(D - 1)/(D - 2))))
    raise NotImplementedError('only critical and subcritical (trigonometric) branches in v0.1')
