"""D20: the mirrored model. Same no-scale field space (K = -3 ln(T+Tbar), symmetric under T -> 1/T), but the plateau
is at small x and the tail at large x, so the inflaton rolls toward +phi after inflation. The angle's metric
g_yy = 1.5 e^{-2 c phi} then shrinks, and the curved space pumps the angle's speed instead of draining it. AI-assisted.
F(T) = [ T (1 + T/mu)^{-1/2}                                  plateau (F ~ T, V -> 1/4) at small x; tail F ~ sqrt(mu T),
                                                              V ~ mu/(4x) = slope sqrt(2/3) at large x
        + delta e^{i gamma} T e^{-a mu/T} / (1 + T/mu) ]     kick: off on the plateau (e^{-a mu/T} -> 0), subdominant on the tail
       * exp(-n T/(T + m2))                                   cliff at x ~ m2 (after inflation), drop e^{-2n}
V = |F|^2/(4 x^2), x = e^{c phi}, g_yy = 3/(2 x^2) = 1.5 e^{-2 c phi}."""
import cmath, math
from scipy.integrate import solve_ivp
c = math.sqrt(2 / 3); NSTAR = 55.6


def make(mu, delta, a, n, m2, gamma=math.pi / 2, mk=None):
    d = delta * cmath.exp(1j * gamma); mk = mu if mk is None else mk     # mk: where the kick switches on
    def V(p, y):
        x = math.exp(c * p); T = complex(x, y)
        F = (T / cmath.sqrt(1 + T / mu) + d * T * cmath.exp(-a * mk / T) / (1 + T / mu)) * cmath.exp(-n * T / (T + m2))
        return abs(F) ** 2 / (4 * x * x)
    def G(p, y, h=1e-6):
        return ((math.log(V(p + h, y)) - math.log(V(p - h, y))) / (2 * h), (math.log(V(p, y + h)) - math.log(V(p, y - h))) / (2 * h))
    def M(p, y, h=1e-4):
        return (V(p, y + h) - 2 * V(p, y) + V(p, y - h)) / h ** 2 / V(p, y)
    return V, G, M


def run(mu=1.0, delta=0.1, a=1.0, n=10.0, m2=100.0, p0=-5.6, Nafter=4.0, step=0.25, mk=None):
    V, G, M = make(mu, delta, a, n, m2, mk=mk)
    def rhs(N, z):
        p, y, dp, dy = z; g = 1.5 * math.exp(-2 * c * p); e = 0.5 * (dp * dp + g * dy * dy); gp, gy = G(p, y)
        return [dp, dy, -c * g * dy * dy - (3 - e) * (dp + gp), 2 * c * dp * dy - (3 - e) * (dy + gy / g)]
    end = lambda N, z: 0.5 * (z[2] ** 2 + 1.5 * math.exp(-2 * c * z[0]) * z[3] ** 2) - 1; end.terminal = True; end.direction = 1
    s = solve_ivp(rhs, [0, 300], [p0, 0, 0, 0], events=end, rtol=1e-8, atol=1e-11, method="LSODA", dense_output=True)
    if not s.t_events[0].size:
        return None
    Ne = s.t_events[0][0]
    eps = lambda z: 0.5 * (z[2] ** 2 + 1.5 * math.exp(-2 * c * z[0]) * z[3] ** 2)
    e0 = eps(s.sol(Ne - NSTAR)); e1 = eps(s.sol(Ne - NSTAR + 0.01))
    rows = []; z = s.y_events[0][0]; N = Ne
    def row(N, z):
        p, y, dp, dy = z; g = 1.5 * math.exp(-2 * c * p); e = eps(z)
        ang = 0.5 * g * dy * dy / 3                                   # angle's share of the total energy (rho_kin_angle / rho)
        return (N - Ne, e, p, math.sqrt(max(M(p, y) / g * (3 - e), 0)), math.sqrt(g) * abs(dy), ang)
    rows.append(row(N, z))
    while N < Ne + Nafter - 1e-9:
        z = solve_ivp(rhs, [N, N + step], z, rtol=1e-7, atol=1e-10, method="LSODA").y[:, -1]; N += step
        rows.append(row(N, z))
    return {"N_end": Ne, "n_s": 1 - 2 * e0 - (math.log(e1) - math.log(e0)) / 0.01, "r_t": 16 * e0, "rows": rows}


if __name__ == "__main__":
    for delta in (0.0, 0.1, 0.3):
        o = run(delta=delta)
        if o is None:
            print(f"delta {delta}: inflation does not end"); continue
        print(f"\ndelta {delta}: N_end {o['N_end']:.1f}  n_s {o['n_s']:.4f}  r_t {o['r_t']:.4f}")
        print("  N-N_end   eps     phi     m_y/H      angle r   angle energy share")
        for dN, e, p, mh, r, sh in o["rows"]:
            print(f"  {dN:5.2f}  {e:5.3f}  {p:+7.3f}  {mh:9.2e}  {r:9.3e}  {sh:8.2e}")
