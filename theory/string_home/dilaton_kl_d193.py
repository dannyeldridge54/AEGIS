"""D193: stabilising the heterotic dilaton Y without touching the Twist field T (Kallosh-Linde-type racetrack). AI-assisted.
K = -ln(Y+Ybar) - 3 ln(T+Tbar) + (helper terms); W = W_Y(Y) + sqrt3 m S T (TWIST-K), with W_Y = W0 + A e^{-aY} - B e^{-bY},
two hidden condensates SU(8) x SU(9) (a = 2pi/8, b = 2pi/9), gauge kinetic f = Y (Z3: no T-dependent thresholds, D152).
KL conditions W_Y(Y0) = 0 and W_Y'(Y0) = 0: supersymmetric Minkowski vacuum for Y, gravitino mass 0 from this sector, Y0 independent
of T (conditions involve W_Y only). With S = 0 and W_Y = 0 the T-sector potential is exactly the Twist's times 1/(2 Y0) (absorbed in m).
Y mass: m_Y = e^{K/2} |W_Y''| / K_YYbar = |W_Y''| (2Y0)^2 (2Y0)^(-1/2) x^(-3/2), x = T + Tbar. Must exceed H at all times."""
import math
a, b, A, Y0 = 2 * math.pi / 8, 2 * math.pi / 9, 1.0, 2.0          # Re Y = 1/g^2 ~ 2 (weak coupling)
B = A * a / b * math.exp(-(a - b) * Y0)                           # W' = 0
W0 = -(A * math.exp(-a * Y0) - B * math.exp(-b * Y0))            # W = 0
W2 = A * a * a * math.exp(-a * Y0) - B * b * b * math.exp(-b * Y0)
print(f"B/A = {B:.4f}, W0 = {W0:.3e}, |W''| = {abs(W2):.3e}")
H_inf, H0 = 6.1e-6, 1.2e-61                                        # Planck units: inflation (r = 0.0036), today
for label, x, H in (("inflation, x=1e-4", 1e-4, H_inf), ("inflation, x=1e-2", 1e-2, H_inf), ("today, x=89", 89.0, H0)):
    mY = abs(W2) * (2 * Y0) ** 2 * (2 * Y0) ** -0.5 * x ** -1.5
    print(f"{label:20s}: m_Y = {mY:.2e} M_P, m_Y/H = {mY / H:.1e}")
mY_today = abs(W2) * (2 * Y0) ** 1.5 * 89 ** -1.5
print(f"today m_Y = {mY_today * 2.435e18:.1e} GeV: Y-mediated force range ~ {1.97e-16 / (mY_today * 2.435e18):.1e} m (no fifth force)")
