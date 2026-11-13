"""Backlog L (exploratory): where does the inflaton freeze on the real supergravity tail, and what slope does it see today?
Tail: V = m^2 |F0|^2/(4x^2) = m^2 exp(-2n x/(x+m2)) / (4 (1 + x/mu)), x = exp(c p). For x >> mu the slope is c = sqrt(2/3)
(PURE-TWIST); for x << mu it is c x/mu (almost a cosmological constant). Run: end of inflation -> kinetic energy with a
radiation share f (derived reheating, Development 42) -> follow p for 40 e-folds until it freezes. AI-assisted."""
import cmath, math
from scipy.integrate import solve_ivp
c = math.sqrt(2 / 3); m2u = 4 * 1.0668e-10


def run(mu, n=125.0, m2=1.0, f=0.0147, Nafter=40.0):
    def V(p):
        x = math.exp(c * p); return math.exp(-2 * n * x / (x + m2)) / (4 * (1 + x / mu))
    dV = lambda p, h=1e-6: (V(p + h) - V(p - h)) / (2 * h)
    def rhs(t, z):
        p, dp = z; K = 0.5 * dp * dp; H2 = V(p) / (3 - K); return [dp, -(3 - K) * dp - dV(p) / H2]
    end = lambda t, z: 0.5 * z[1] ** 2 - 1; end.terminal = True; end.direction = 1
    s = solve_ivp(rhs, [0, 400], [-13.0, 0], events=end, rtol=1e-8, atol=1e-12, method="LSODA")
    p, dp = s.y_events[0][0]; H2 = V(p) / (3 - 0.5 * dp * dp); lnr = math.log(f * 0.5 * H2 * dp * dp); dp *= math.sqrt(1 - f)
    def rhs2(t, z):
        p, dp, lnr = z; rr = math.exp(lnr); K = 0.5 * dp * dp; H2 = (V(p) + rr) / (3 - K); e = K + (2 / 3) * rr / H2
        return [dp, -(3 - e) * dp - dV(p) / H2, -4.0]
    s2 = solve_ivp(rhs2, [0, Nafter], [p, dp, lnr], rtol=1e-8, atol=1e-12, method="LSODA")
    pf = s2.y[0, -1]; xf = math.exp(c * pf)
    return xf, c * xf / (xf + mu), s2.y[1, -1]


if __name__ == "__main__":
    for f in (0.0015, 0.0147, 0.5):
        for mu in (1e4, 100.0, 1.0, 0.01):
            xf, kap, v = run(mu, f=f)
            print(f"f {f}, mu {mu:g}: frozen at x = {xf:.3g}, slope seen today kappa_eff = {kap:.4f} ({kap / c:.3f} of sqrt(2/3)), dp/dN left {v:.1e}", flush=True)
    n_de = 0.5 * math.log(m2u / (4 * 7.9e-121))
    print(f"Cliff depth that sets the dark-energy scale: exp(-2n) m^2/4 = rho_DE -> n = {n_de:.1f}")
