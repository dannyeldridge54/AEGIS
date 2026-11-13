"""D18: the angle kick from an explicit no-scale supergravity model (Development 17 made concrete). AI-assisted.
K = -3 ln(T + Tbar - S Sbar), W = sqrt(3) m S F(T), stabiliser S = 0  ->  V = m^2 |F(T)|^2 / (T + Tbar)^2   (units m = 1).
T = x + i y, x = e^{c phi}, c = sqrt(2/3): metric dphi^2 + (3/2) e^{-2 c phi} dy^2  (the Twist's field space, lambda = -2c).
F(T) = (T - 1/2) + delta e^{i gamma} e^{-a T}:
  delta = 0  -> V = (1/4)(1 - e^{-c phi}/2)^2, the alpha = 1 E-model; y = 0 is the angle's minimum.
  the e^{-aT} term is ~e^{-a x}: negligible on the plateau (x ~ 100), switched on near the end (x ~ 1); its phase gamma
  breaks y -> -y, so the angle's minimum moves as phi falls: the kick. gamma also fixes the kick's sign (matter vs antimatter).
Output: angle canonical speed r = sqrt(g_yy) |y'| at the end of inflation; N, n_s (single-field estimate at N* = 55.6)."""
import cmath, math
import numpy as np
from scipy.integrate import solve_ivp
c = math.sqrt(2 / 3); NSTAR = 55.6


def model(delta, a, gamma=math.pi / 2):
    d = delta * cmath.exp(1j * gamma)
    def V(p, y):
        x = math.exp(c * p); T = complex(x, y)
        return abs((T - 0.5) + d * cmath.exp(-a * T)) ** 2 / (4 * x * x)
    def grad(p, y, h=1e-6):
        return ((V(p + h, y) - V(p - h, y)) / (2 * h), (V(p, y + h) - V(p, y - h)) / (2 * h))
    return V, grad


def run(delta, a, gamma=math.pi / 2, p0=5.6):
    V, grad = model(delta, a, gamma)
    def rhs(N, z):
        p, y, dp, dy = z; g = 1.5 * math.exp(-2 * c * p); eps = 0.5 * (dp * dp + g * dy * dy)
        v = V(p, y); vp, vy = grad(p, y)
        return [dp, dy, -c * g * dy * dy - (3 - eps) * (dp + vp / v), 2 * c * dp * dy - (3 - eps) * (dy + vy / (g * v))]
    end = lambda N, z: 0.5 * (z[2] ** 2 + 1.5 * math.exp(-2 * c * z[0]) * z[3] ** 2) - 1
    end.terminal = True; end.direction = 1
    sol = solve_ivp(rhs, [0, 400], [p0, 0, 0, 0], events=end, rtol=1e-10, atol=1e-13, dense_output=True, method="LSODA")
    if not sol.t_events[0].size:
        return None
    Ne = sol.t_events[0][0]; p, y, dp, dy = sol.y_events[0][0]
    def epsH(N):
        z = sol.sol(N); return 0.5 * (z[2] ** 2 + 1.5 * math.exp(-2 * c * z[0]) * z[3] ** 2)
    N0 = Ne - NSTAR; e0 = epsH(N0); eta = (math.log(epsH(N0 + 0.01)) - math.log(e0)) / 0.01
    return {"N": Ne, "phi_end": p, "y_end": y, "r_end": math.sqrt(1.5) * math.exp(-c * p) * abs(dy), "n_s": 1 - 2 * e0 - eta, "r_t": 16 * e0}


if __name__ == "__main__":
    b = run(0.0, 1.0)
    print(f"no extra term: N {b['N']:.1f}  n_s {b['n_s']:.4f}  r_tensor {b['r_t']:.4f}  angle speed {b['r_end']:.1e}")
    print("  delta     a     N     n_s    r_tensor   y_end    angle speed r")
    for a in (0.5, 1.0, 2.0, 4.0):
        for delta in (0.01, 0.1, 0.3, 1.0):
            o = run(delta, a)
            print(f"{delta:6.2f} {a:5.1f}", "  inflation broken" if o is None else
                  f"{o['N']:6.1f} {o['n_s']:7.4f} {o['r_t']:8.4f} {o['y_end']:+8.4f} {o['r_end']:10.2e}")
