"""Step B (exploratory): reheating derived, not put in by hand. AI-assisted.
Instant preheating (Felder, Kofman & Linde, hep-ph/9812289): a field chi with coupling g^2 phi^2 chi^2 / 2, massless
where the inflaton crosses phi0 (placed at the end of inflation, as the task asks). Crossing at speed phidot creates
    n_chi = (g |phidot|)^{3/2} / (8 pi^3),
each chi then weighs g |phi - phi0|; once the inflaton has moved dphi further (chi decays to radiation there), the
energy moved out of the kinetic energy is rho_chi = n_chi g dphi, so the efficiency is
    f = rho_chi / (phidot^2 / 2) = g^{5/2} dphi / (4 pi^3 sqrt(phidot)),   capped at 1 (backreaction).
phidot at the end of inflation from the model itself (n = 125, mu = 1e4, m2 = 1, p0 = -13): kinetic share 1 at the end
(eps = 1 by the end condition), phidot = sqrt(2) H_end M_P. Units: M_P = 1 unless GeV stated."""
import cmath, math
from scipy.integrate import solve_ivp

c = math.sqrt(2 / 3); MP = 2.435e18; m2u = 4 * 1.0668e-10; gs = 106.75
MU, N, M2 = 1e4, 125.0, 1.0


def end_state():
    def V(p):
        x = math.exp(c * p); T = complex(x, 0)
        return abs(T / cmath.sqrt(1 + T / MU) * cmath.exp(-N * T / (T + M2))) ** 2 / (4 * x * x)
    dV = lambda p, h=1e-6: (V(p + h) - V(p - h)) / (2 * h)
    def rhs(t, z):
        p, dp = z; K = 0.5 * dp * dp; H2 = V(p) / (3 - K); return [dp, -(3 - K) * dp - dV(p) / H2]
    end = lambda t, z: 0.5 * z[1] ** 2 - 1; end.terminal = True; end.direction = 1
    s = solve_ivp(rhs, [0, 400], [-13.0, 0], events=end, rtol=1e-8, atol=1e-12, method="LSODA")
    p, dp = s.y_events[0][0]; H2 = V(p) / (3 - 0.5 * dp * dp)
    return math.sqrt(H2 * m2u), dp          # H in M_P units, dphi/dN


def T_of(f, H, dp):
    rho = f * 0.5 * (H * dp) ** 2 * MP ** 4                  # GeV^4
    return (30 * rho / (math.pi ** 2 * gs)) ** 0.25


if __name__ == "__main__":
    H, dp = end_state(); phidot = H * dp
    print(f"End of inflation: H = {H * MP:.2e} GeV, phidot = {phidot:.2e} M_P^2 (sqrt = {math.sqrt(phidot) * MP:.2e} GeV)")
    for dphi in (0.1, 1.0):
        for g in (0.01, 0.03, 0.1, 0.3, 1.0):
            f = min(1.0, g ** 2.5 * dphi / (4 * math.pi ** 3 * math.sqrt(phidot)))
            print(f"  dphi {dphi} M_P, g {g}: efficiency f = {f:.2e}, T_RH = {T_of(max(f, 1e-30), H, dp):.2e} GeV", flush=True)
