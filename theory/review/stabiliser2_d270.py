"""D270b: same as stabiliser_d270.py with a quadratic stabiliser b (T - Tbar)^2 (the quartic gives no mass at y = 0).
Also reports the change of the angle's kinetic metric at y = 0. AI-assisted."""
import sympy as sp
x, y, b, w = sp.symbols("x y b w", positive=True)
t, tb = sp.symbols("t tb")
K = -3 * sp.log(t + tb + b * (t - tb) ** 2)
W, Wb = w * t ** sp.Rational(3, 2), w * tb ** sp.Rational(3, 2)
KT, KTb, KTTb = sp.diff(K, t), sp.diff(K, tb), sp.diff(K, t, tb)
V = sp.exp(K) * ((sp.diff(W, t) + KT * W) * (sp.diff(Wb, tb) + KTb * Wb) / KTTb - 3 * W * Wb) + 3 * w ** 2 / 8
sub = {t: x + sp.I * y, tb: x - sp.I * y}
gyy = sp.simplify(2 * KTTb.subs(sub).subs(y, 0))
d2 = sp.simplify(sp.diff(V.subs(sub), y, 2).subs(y, 0))
print("g_yy(y=0) =", gyy, " (no stabiliser: 3/(2x^2))")
print("m_theta^2/m32^2 =", sp.simplify(d2 / gyy / (w ** 2 / 8)))
