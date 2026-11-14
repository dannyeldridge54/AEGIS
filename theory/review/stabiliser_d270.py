"""D270: does the quartic Kahler stabiliser b(T - Tbar)^4 cure the angle tachyon of D269 (W = w T^{3/2} + uplift 3w^2/8)?
Single field, K = -3 ln(T + Tbar + b (T - Tbar)^4); mass of the canonical angle at y = 0, in units of m32^2 = w^2/8. AI-assisted."""
import sympy as sp
x, y, b, w = sp.symbols("x y b w", positive=True)
T, Tb = x + sp.I * y, x - sp.I * y
t, tb = sp.symbols("t tb")
K = -3 * sp.log(t + tb + b * (t - tb) ** 4)
W, Wb = w * t ** sp.Rational(3, 2), w * tb ** sp.Rational(3, 2)
KT, KTb, KTTb = sp.diff(K, t), sp.diff(K, tb), sp.diff(K, t, tb)
DW, DWb = sp.diff(W, t) + KT * W, sp.diff(Wb, tb) + KTb * Wb
V = sp.exp(K) * (DW * DWb / KTTb - 3 * W * Wb) + 3 * w ** 2 / 8
Vy = V.subs({t: T, tb: Tb})
d2 = sp.simplify(sp.diff(Vy, y, 2).subs(y, 0))
g = sp.Rational(3, 4) / x ** 2 * 2          # kinetic metric for y: 2 K_TTb = 3/(2x^2) at y = 0
m2 = sp.simplify(d2 / g / (w ** 2 / 8))
print("m_theta^2 / m32^2 =", m2)
print("b needed for m^2 >= 0:", sp.solve(sp.Eq(m2, 0), b))
