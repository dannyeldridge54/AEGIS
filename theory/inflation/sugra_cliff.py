"""D19b: plateau -> cliff -> sqrt(2/3) tail in one no-scale model; tests T-ROLL with the end of inflation included.
D19 (sugra_tail.py) found that a plateau joined smoothly to a slope-sqrt(2/3) tail never ends inflation (eps -> 1/3).
Fix: a holomorphic cliff factor, F(T) = [T^{3/2}(T+mu)^{-1/2} + delta e^{i gamma} e^{-aT}] * exp(-n m2/(T + m2)).
Along y = 0 the factor is exp(-2 n m2/(x + m2)): 1 on the plateau, e^{-2n} past the cliff; the log-slope peaks at n c/2,
so for n > 2 sqrt(2)/c ~ 3.5 the cliff ends inflation (kination follows). n = 10 here (drop e^{-20}; the real drop to
today's dark energy, ~1e-110, needs n ~ 125 and is only steeper). AI-assisted.
Printed: the end of inflation, n_s, r, and from inflation into kination: eps, m_y/H (angle mass over expansion rate),
and the angle speed r = sqrt(g_yy)|y'| (= thetadot_can/(H M_P), MATTER's r)."""
import cmath, math
import numpy as np
from scipy.integrate import solve_ivp
c = math.sqrt(2 / 3); NSTAR = 55.6


def make(mu, delta, a, n, m2, gamma=math.pi / 2, scaled=False):
    d = delta * cmath.exp(1j * gamma)
    def V(p, y):
        x = math.exp(c * p); T = complex(x, y)
        kick = d * cmath.exp(-a * T) * (T ** 1.5 if scaled else 1)       # scaled: the kick shrinks with the rest below the plateau
        F = (T ** 1.5 / cmath.sqrt(T + mu) + kick) * cmath.exp(-n * m2 / (T + m2))
        return abs(F) ** 2 / (4 * x * x)
    def lnV_grad(p, y, h=1e-6):
        return ((math.log(V(p + h, y)) - math.log(V(p - h, y))) / (2 * h), (math.log(V(p, y + h)) - math.log(V(p, y - h))) / (2 * h))
    def m2_over_V(p, y, h=1e-4):
        return (V(p, y + h) - 2 * V(p, y) + V(p, y - h)) / h ** 2 / V(p, y)
    return V, lnV_grad, m2_over_V


def run(mu=1.0, delta=0.1, a=1.0, n=10.0, m2=1.0, p0=5.6, Nafter=4.0, scaled=False):
    V, G, M = make(mu, delta, a, n, m2, scaled=scaled)
    def rhs(N, z):
        p, y, dp, dy = z; g = 1.5 * math.exp(-2 * c * p); eps = 0.5 * (dp * dp + g * dy * dy); gp, gy = G(p, y)
        return [dp, dy, -c * g * dy * dy - (3 - eps) * (dp + gp), 2 * c * dp * dy - (3 - eps) * (dy + gy / g)]
    end = lambda N, z: 0.5 * (z[2] ** 2 + 1.5 * math.exp(-2 * c * z[0]) * z[3] ** 2) - 1; end.direction = 1; end.terminal = True
    s1 = solve_ivp(rhs, [0, 400], [p0, 0, 0, 0], events=end, rtol=1e-10, atol=1e-13, dense_output=True, method="LSODA")
    if not s1.t_events[0].size:
        return None
    Ne = s1.t_events[0][0]
    s2 = solve_ivp(rhs, [Ne, Ne + Nafter], s1.y_events[0][0], rtol=1e-10, atol=1e-13, dense_output=True, method="LSODA")
    def at(N):
        z = s1.sol(N) if N <= Ne else s2.sol(N); p, y, dp, dy = z
        g = 1.5 * math.exp(-2 * c * p); eps = 0.5 * (dp * dp + g * dy * dy)
        mH2 = 3 * M(p, y) / g / (3 - eps) * (3 - eps) / 3 * 3 / (3 - eps) if eps < 3 else float("nan")
        # m_y^2/H^2 = (V_yy/g) / (V/(3 - eps))
        mH2 = (M(p, y) / g) * (3 - eps)
        return eps, p, math.sqrt(max(mH2, 0)), math.sqrt(g) * abs(dy)
    e0 = at(Ne - NSTAR)[0]; e1 = at(Ne - NSTAR + 0.01)[0]
    return {"N_end": Ne, "n_s": 1 - 2 * e0 - (math.log(e1) - math.log(e0)) / 0.01, "r_t": 16 * e0, "at": at}


if __name__ == "__main__":
    for delta, n in ((0.0, 10.0), (0.1, 10.0), (0.3, 10.0), (0.1, 20.0)):
        o = run(delta=delta, n=n)
        if o is None:
            print(f"delta {delta}, n {n}: inflation does not end"); continue
        print(f"\ndelta {delta}, n {n}: inflation ends at N = {o['N_end']:.1f}; n_s {o['n_s']:.4f}; r_tensor {o['r_t']:.4f}")
        print("  N - N_end    eps     phi      m_y/H    angle speed r")
        for dN in (-NSTAR, -3, -1, 0, 0.5, 1, 2, 3, 4):
            e, p, mh, r = o["at"](o["N_end"] + dN)
            print(f"  {dN:+6.1f}   {e:6.3f}  {p:+7.3f}  {mh:9.3e}  {r:.3e}")
