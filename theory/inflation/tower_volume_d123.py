"""D123: which lambda? If T behaves like a volume-type modulus (K = -3 ln(T + Tbar)), the light tower is Kaluza-Klein modes,
m_KK ~ M_P / x for x > 1 (lambda = sqrt(2/3), six-dimensional decompactification), and, by T-duality, winding modes m_w ~ M_P x for
x < 1. Tower mass min(x, 1/x) M_P (O(1) factors dropped) along the Twist trajectory vs the Hubble rate (inflation) and the bath
temperature (after). AI-assisted, estimate; the identification of T with a volume modulus is an assumption."""
import math
import numpy as np
from scipy.integrate import solve_ivp
import cliff_v2 as C
lnV, _ = C.version("exp", 4 / math.pi); c = C.c; MP = 2.435e18; TRH = 4e14
inf = C.inflation(lnV); ps, pe = inf["pstar"], inf["pend"]
H_inf = 1.5e13
tower = lambda x: MP * min(x, 1 / x)
print("during inflation (H ~ 1.5e13 GeV):")
for N in (60, 55, 40, 20, 0):
    from scipy.optimize import brentq
    from scipy.integrate import quad
    p = pe if N == 0 else brentq(lambda q: quad(lambda r: -1 / C.DL(r), q, pe, limit=200)[0] - N, -40, pe - 1e-6)
    x = math.exp(c * p); print(f"  {N:>2} e-folds before the end: x {x:.2e}, tower {tower(x):.1e} GeV, tower/H {tower(x)/H_inf:.0f}")
V = lambda p: math.exp(lnV(p)) if lnV(p) > -700 else 0.0
def rhs(t, z):
    p, dp = z; K = 0.5 * dp * dp; return [dp, -(3 - K) * dp - V(p) * C.DL(p) / (V(p) / (3 - K))]
end = lambda t, z: 0.5 * z[1] ** 2 - 1; end.terminal = True; end.direction = 1
s = solve_ivp(rhs, [0, 4000], [-13.0, 0], events=end, rtol=1e-8, atol=1e-12, method="LSODA")
p, dp = s.y_events[0][0]; H2 = V(p) / (3 - 0.5 * dp * dp); f = 0.008; lnr = math.log(f * 0.5 * H2 * dp * dp); dp *= math.sqrt(1 - f)
def rhs2(t, z):
    p, dp, lnr = z; rr = math.exp(lnr); K = 0.5 * dp * dp; Vp = V(p); H2 = (Vp + rr) / (3 - K); e = K + (2 / 3) * rr / H2
    return [dp, -(3 - e) * dp - Vp * C.DL(p) / H2, -4.0]
s2 = solve_ivp(rhs2, [0, 40], [p, dp, lnr], rtol=1e-8, atol=1e-12, dense_output=True, method="LSODA")
print("after inflation (bath T ~ T_RH e^-N):")
worst = 1e99
for N in np.linspace(0, 40, 401):
    x = math.exp(c * s2.sol(N)[0]); r = tower(x) / (TRH * math.exp(-N)); worst = min(worst, r)
    if abs(N - round(N)) < 1e-9 and int(round(N)) in (0, 1, 2, 3, 5, 10, 40):
        print(f"  N {N:4.0f}: x {x:9.3g}, tower {tower(x):.1e} GeV, T {TRH*math.exp(-N):.1e}, tower/T {r:.1e}")
print(f"  smallest tower/T after inflation: {worst:.1e}; today x ~ {x:.0f}: tower {tower(x):.1e} GeV")
