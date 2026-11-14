"""D294: is X = 0 a stationary point of the D292 sector, and what is the sgoldstino mass?
W = w T^{3/2} + mu2 X, K = -3 ln(T + Tb) + |X|^2 (T+Tb)^{-3} - q |X|^4 (T+Tb)^{-6} (quartic stabiliser q, weight-consistent).
Real T = x, X = s (real) and X = i s. AI-assisted."""
import sympy as sp
x, s, w, mu2, q = sp.symbols("x s w mu2 q", positive=True)
t, tb, X, Xb = sp.symbols("t tb X Xb")
u = t + tb
K = -3 * sp.log(u) + X * Xb * u ** -3 - q * (X * Xb) ** 2 * u ** -6
W = w * t ** sp.Rational(3, 2) + mu2 * X; Wb = w * tb ** sp.Rational(3, 2) + mu2 * Xb
z, zb = [t, X], [tb, Xb]
Kij = sp.Matrix(2, 2, lambda i, j: sp.diff(K, z[i], zb[j]))
DW = sp.Matrix([sp.diff(W, z[i]) + sp.diff(K, z[i]) * W for i in range(2)])
DWb = sp.Matrix([sp.diff(Wb, zb[i]) + sp.diff(K, zb[i]) * Wb for i in range(2)])
V = sp.exp(K) * ((DW.T * Kij.inv().T * DWb)[0] - 3 * W * Wb)
sub = {t: x, tb: x}
Vr = V.subs(sub)
for lab, Xv in (("real", s), ("imag", sp.I * s)):
    f = Vr.subs({X: Xv, Xb: sp.conjugate(Xv)})
    f = f.subs(mu2, sp.sqrt(sp.Rational(3, 8)) * w)
    d1 = sp.simplify(sp.diff(f, s).subs(s, 0))
    d2 = sp.simplify(sp.diff(f, s, 2).subs(s, 0))
    gXX = (2 * x) ** -3                        # K_XXb at X = 0
    print(f"{lab}: dV/ds|0 = {d1};  m^2 (canonical)/m32^2 = {sp.simplify(d2 / (2 * gXX) / (w**2 / 8))}")
