"""D292: SUSY breaking with x-independent scales in the Twist's no-scale sector.
W = w T^{3/2} + mu2 X, K = -3 ln(T + Tb) + |X|^2 (T + Tb)^{-3} (1 + c ((T - Tb)/(T + Tb))^2)   (X = Polonyi field, modular weight 3).
At X = 0: V(x, y) from the F-term formula; checks V along real T, m_3/2, and the angle mass vs c. AI-assisted."""
import sympy as sp
x, y, w, mu2, c = sp.symbols("x y w mu2 c", real=True)
t, tb, X, Xb = sp.symbols("t tb X Xb")
K = -3 * sp.log(t + tb) + X * Xb * (t + tb) ** -3 * (1 + c * ((t - tb) / (t + tb)) ** 2)
W = w * t ** sp.Rational(3, 2) + mu2 * X; Wb = w * tb ** sp.Rational(3, 2) + mu2 * Xb
z, zb = [t, X], [tb, Xb]
Kij = sp.Matrix(2, 2, lambda i, j: sp.diff(K, z[i], zb[j]))
DW = [sp.diff(W, z[i]) + sp.diff(K, z[i]) * W for i in range(2)]
DWb = [sp.diff(Wb, zb[i]) + sp.diff(K, zb[i]) * Wb for i in range(2)]
sub0 = {X: 0, Xb: 0}
Kinv = Kij.subs(sub0).inv()
V = sp.exp(K.subs(sub0)) * (sum(Kinv[i, j] * DW[i].subs(sub0) * DWb[j].subs(sub0) for i in range(2) for j in range(2)) - 3 * (W * Wb).subs(sub0))
Vxy = sp.simplify(V.subs({t: x + sp.I * y, tb: x - sp.I * y}))
V0 = sp.simplify(Vxy.subs(y, 0))
print("V(real T) =", V0)
m32 = sp.simplify(sp.sqrt(sp.exp(-3 * sp.log(2 * x))) * w * x ** sp.Rational(3, 2))
print("m_3/2 =", m32)
gyy = sp.Rational(3, 2) / x ** 2
d2 = sp.simplify(sp.diff(Vxy, y, 2).subs(y, 0))
mt = sp.simplify(d2 / gyy / (w ** 2 / 8))
print("m_theta^2 / m32^2 =", sp.simplify(mt.subs(mu2, sp.sqrt(sp.Rational(3, 8)) * w)), "  (with mu2^2 = 3 w^2/8, i.e. V = 0)")
