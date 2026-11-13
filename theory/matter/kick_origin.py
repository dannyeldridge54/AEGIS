"""D26: where does the kick's small prefactor (~1e-4, Development 25) come from? AI-assisted.
No-scale K = -3 ln(T + Tbar), W = W_c + W_0 e^{-A T}, A = pi/4 (Nieh-Yan period). The F-term potential's angle-dependent
part is derived symbolically below: a single exponential gives none (|e^{-AT}|^2 has no y); the angle potential is the
interference of the instanton with the constant W_c, whose size sets the gravitino mass m_3/2 = e^{K/2} W_c.
Compared with the inflaton plateau V_inf = m^2/4 (m = 2 sqrt(V*), V* from TWIST-INFLATION), the equivalent kick
prefactor is delta_eff ~ V_angle_amplitude / (2 V_inf). Order-of-magnitude, evaluated at Re T ~ 1 (base frame),
where Development 25 found the kick acts."""
import math
import sympy as sp
x, y, A, Wc, W0 = sp.symbols("x y A W_c W_0", positive=True)
T, Tb = x + sp.I * y, x - sp.I * y
W = Wc + W0 * sp.exp(-A * T); Wb = Wc + W0 * sp.exp(-A * Tb)
K = -3 * sp.log(T + Tb)
KT = sp.diff(K, x) / 2                      # dK/dT for a function of T + Tbar
KTTb = sp.Rational(3, 1) / (T + Tb) ** 2
DW = sp.diff(W0 * sp.exp(-A * sp.Symbol("t")), sp.Symbol("t")).subs(sp.Symbol("t"), T) + KT * W
DWb = sp.conjugate(DW).subs({sp.conjugate(x): x, sp.conjugate(y): y, sp.conjugate(A): A, sp.conjugate(Wc): Wc, sp.conjugate(W0): W0})
V = sp.exp(K) * (DW * DWb / KTTb - 3 * W * Wb)
Vang = sp.simplify(sp.expand(sp.simplify(V - V.subs(y, 0))))
amp = sp.simplify(sp.diff(V, y, 2).subs(y, 0) / (-A ** 2))   # coefficient of cos(A y) near y = 0
target = A * W0 * Wc * sp.exp(-A * x) / (2 * x ** 2)
print("angle-dependent amplitude (coefficient of cos A y):", sp.simplify(amp))
print("matches A W0 Wc e^{-Ax}/(2x^2):", sp.simplify(amp - target) == 0)
MP = 2.435e18; Vstar = 1.0668e-10; m = 2 * math.sqrt(Vstar); Ac = math.pi / 4; xk = 1.0
print(f"inflaton mass m = {m:.2e} M_P = {m * MP:.1e} GeV")
for ratio in (0.1, 1.0, 10.0):                 # W_0 / W_c
    for m32 in (1e11, 3e11, 1e12, 1e13):
        Wcv = (m32 / MP) * (2 * xk) ** 1.5
        amp_v = Ac * (ratio * Wcv) * Wcv * math.exp(-Ac * xk) / (2 * xk ** 2)
        print(f"W0/Wc {ratio:5.1f}  m_3/2 {m32:.0e} GeV -> delta_eff ~ {amp_v / (2 * m * m / 4):.1e}")
