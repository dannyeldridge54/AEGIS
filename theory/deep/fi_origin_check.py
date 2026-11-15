"""Deep study (D436): FI-term origin of the capture coupling — symbolic check. AI-assisted.
Two Kähler moduli, K = −ln(T1+T̄1) − 2 ln(T2+T̄2) (one direction rolls: x1 = Re T1 = the Twist; x2 = Re T2 held fixed), an anomalous U(1)
gauging the axionic shifts Im T_i → Im T_i + δ_i Λ (Green–Schwarz). Supergravity D-term: D = ξ − Q|φ|², ξ = −δ_i ∂_{T_i}K (real), V_D = (g²/2) D²."""
import sympy as sp
x1, x2, d1, d2, Q, g, ph = sp.symbols('x1 x2 delta1 delta2 Q g phi', real=True)
T1, T1b, T2, T2b = sp.symbols('T1 T1b T2 T2b')
K = -sp.log(T1 + T1b) - 2 * sp.log(T2 + T2b)
xi = -(d1 * sp.diff(K, T1) + d2 * sp.diff(K, T2))
xi = sp.simplify(xi.subs({T1: x1, T1b: x1, T2: x2, T2b: x2}))
print("ξ(x1, x2) =", xi)
xE = sp.solve(sp.Eq(xi, 0), x1)[0]; print("ξ = 0 at x1 = x_E =", xE, "  (needs δ1, δ2 of opposite sign; x_E ∝ x2 × ratio of flux charges)")
VD = g**2 / 2 * (xi - Q * ph**2)**2
m2 = sp.simplify(sp.diff(VD, ph, 2).subs(ph, 0)); print("m_φ² at φ = 0:", m2, " → vanishes at x_E; tachyonic where Qξ > 0 (φ condenses), positive where Qξ < 0")
dxi = sp.simplify(sp.diff(xi, x1).subs(x1, xE)); print("dξ/dx1 at x_E:", dxi, " → near x_E, m_φ² ≈ −g²Q (dξ/dx1)(x1 − x_E): LINEAR in (x1 − x_E), the D-term analogue of λ(T − T_E)")
