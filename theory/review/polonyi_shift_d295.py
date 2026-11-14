"""D295: verify D294's claim that the D292 sector's vacuum energy stays x-independent after the Polonyi shift.
Same K, W as polonyi_vac_d294.py; q = 10; minimise V over real X numerically at several x; report V_min and the canonical shift. AI-assisted."""
import sympy as sp, mpmath as mp
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
f = sp.lambdify((x, s, w, mu2, q), V.subs({t: x, tb: x, X: s, Xb: s}), "mpmath")
mp.mp.dps = 30
wv, qv = mp.mpf(1), mp.mpf(10)
mu2v = mp.sqrt(mp.mpf(3) / 8) * wv
for xv in (1, 10, 89):
    xv = mp.mpf(xv); g = lambda S: f(xv, S, wv, mu2v, qv)
    S0 = mp.findroot(lambda S: mp.diff(g, S), mp.mpf(0.01) * (2 * xv) ** 1.5)
    print(f"x {float(xv)}: X_min {float(S0):.5g}, canonical shift {float(S0 * (2*xv) ** -1.5):.6g}, V_min/w^2 {float(g(S0)):.8g}")
