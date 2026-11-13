"""D21: the mirrored model (sugra_mirror.py) with radiation from reheating. AI-assisted.
At the end of inflation a fraction f of the inflaton's kinetic energy becomes radiation at once (instant preheating);
the inflaton velocity is reduced to match. Then fields + radiation evolve together:
  3 H^2 = (H^2/2)|phi'|^2 + V + rho_r  ->  H^2 = (V + rho_r)/(3 - K),  K = |phi'|^2/2 (field-space norm)
  eps = K + (2/3) rho_r/H^2,  rho_r ∝ e^{-4 (N - N_end)}
  phi^a'' + Gamma^a_bc phi^b' phi^c' + (3 - eps) phi^a' + g^ab V_b / H^2 = 0.
Units: M_P = 1, energies in m^2 with m^2 = 4 V* (plateau V = 1/4 <-> V* = 1.07e-10 M_P^4 from TWIST-INFLATION).
Output: temperature T, angle speed r = sqrt(g_yy)|y'| (MATTER's r), angle energy share, radiation share."""
import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sugra_mirror as M
from scipy.integrate import solve_ivp
c = M.c; MP = 2.435e18; m2 = 4 * 1.0668e-10; gs = 106.75


def T_of(rho):                                        # rho in code units -> GeV
    return (30 * rho * m2 * MP ** 4 / (math.pi ** 2 * gs)) ** 0.25


def run(delta=0.1, f=0.9, Nafter=6.0, step=0.25, mu=1.0, a=1.0, n=10.0, m2c=100.0):
    V, G, Mm = M.make(mu, delta, a, n, m2c)
    def rhs_inf(N, z):
        p, y, dp, dy = z; g = 1.5 * math.exp(-2 * c * p); e = 0.5 * (dp * dp + g * dy * dy); gp, gy = G(p, y)
        return [dp, dy, -c * g * dy * dy - (3 - e) * (dp + gp), 2 * c * dp * dy - (3 - e) * (dy + gy / g)]
    end = lambda N, z: 0.5 * (z[2] ** 2 + 1.5 * math.exp(-2 * c * z[0]) * z[3] ** 2) - 1; end.terminal = True; end.direction = 1
    s = solve_ivp(rhs_inf, [0, 300], [-5.6, 0, 0, 0], events=end, rtol=1e-8, atol=1e-11, method="LSODA")
    Ne = s.t_events[0][0]; p, y, dp, dy = s.y_events[0][0]
    # energy at the end (code units): H^2 = V/(3 - K), rho_tot = 3 H^2
    K = 0.5 * (dp * dp + 1.5 * math.exp(-2 * c * p) * dy * dy); H2 = V(p, y) / (3 - K)
    kin_inflaton = 0.5 * H2 * dp * dp
    rho_r0 = f * kin_inflaton
    dp = dp * math.sqrt(1 - f)                        # inflaton loses that kinetic energy
    def rhs(N, z):
        p, y, dp, dy, lnr = z; g = 1.5 * math.exp(-2 * c * p); K = 0.5 * (dp * dp + g * dy * dy)
        v = V(p, y); rr = math.exp(lnr); H2 = (v + rr) / (3 - K); e = K + (2 / 3) * rr / H2
        gp, gy = G(p, y)                              # d ln V
        return [dp, dy, -c * g * dy * dy - (3 - e) * dp - gp * v / H2,
                2 * c * dp * dy - (3 - e) * dy - gy * v / (g * H2), -4.0]
    z = [p, y, dp, dy, math.log(rho_r0)]; N = Ne; rows = []
    def row(N, z):
        p, y, dp, dy, lnr = z; g = 1.5 * math.exp(-2 * c * p); K = 0.5 * (dp * dp + g * dy * dy)
        v = V(p, y); rr = math.exp(lnr); H2 = (v + rr) / (3 - K)
        return (N - Ne, T_of(rr), math.sqrt(g) * abs(dy), 0.5 * g * dy * dy / 3, rr / (3 * H2))
    rows.append(row(N, z))
    while N < Ne + Nafter - 1e-9:
        z = list(solve_ivp(rhs, [N, N + step], z, rtol=1e-7, atol=1e-10, method="LSODA").y[:, -1]); N += step
        rows.append(row(N, z))
    return rows


if __name__ == "__main__":
    for delta, f in ((0.1, 0.9), (0.1, 0.99), (0.03, 0.99), (0.3, 0.99)):
        rows = run(delta, f)
        print(f"\ndelta {delta}, reheating fraction f {f}")
        print("  N-N_end   T (GeV)    angle r    angle share   radiation share")
        for dN, T, r, sh, rs in rows:
            print(f"  {dN:5.2f}   {T:9.2e}   {r:9.3e}   {sh:9.2e}     {rs:7.3f}")
        print(f"  peak angle share {max(r[3] for r in rows):.2e}")
