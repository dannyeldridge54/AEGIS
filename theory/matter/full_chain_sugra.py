"""D27: the full chain with the DERIVED supergravity angle potential (Development 26), no stand-in kick term. AI-assisted.
V/m^2 = |F0(T)|^2/(4x^2)                                  inflaton (mirrored plateau -> cliff -> tail, no kick)
      + eps * exp(-A x_o) cos(A y_o + gamma) / (2 x_o^2)  angle: instanton x constant-W interference (eq. 5), base frame
with T = x + i y, T_o = 1/T (x_o = x/|T|^2, y_o = -y/|T|^2), A = pi/4 (Nieh-Yan period), F0 = T/sqrt(1+T/mu) e^{-nT/(T+m2)},
eps = A W0 Wc / m^2 = A (W0/Wc) (m_3/2/M_P)^2 (2 x_o)^3 / m^2 evaluated with x_o = 1 -> eps = 8 A (W0/Wc) (m_3/2 / m)^2
(m = inflaton mass, 2 sqrt(V*) = 2.07e-5 M_P). Radiation from instant preheating (fraction f); MATTER rate equation.
Output: the gravitino mass that gives the observed n_B/s, for W0/Wc = 1.
RESULT (12 Nov, 21:20 CT): does not run as written. The derived angle term has a 1/x_o^2 (e^K) factor that is unsuppressed
at one end of the field range: in the base frame it exceeds the inflaton potential by 1e7-1e25 below the cliff and on the
tail; written in the mirrored frame it exceeds the plateau by 2e3. So it cannot simply be added to the plateau-cliff-tail
model (Development 27). Kept as the record; the next model multiplies the angle term by the cliff factor."""
import cmath, math, os, sys
from scipy.integrate import solve_ivp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import chain_d22 as C
c = math.sqrt(2 / 3); A = math.pi / 4; MP = 2.435e18; m2u = 4 * 1.0668e-10; m_inf = math.sqrt(m2u); gs = 106.75
MU, N, M2 = 1e4, 10.0, 1.0


def make(eps, gamma):
    def V(p, y):
        x = math.exp(c * p); T = complex(x, y)
        F0 = T / cmath.sqrt(1 + T / MU) * cmath.exp(-N * T / (T + M2))
        To = 1 / T; xo, yo = To.real, To.imag
        return abs(F0) ** 2 / (4 * x * x) + eps * math.exp(-A * xo) * math.cos(A * yo + gamma) / (2 * xo * xo)
    def G(p, y, h=1e-6):
        v = V(p, y)
        return (V(p + h, y) - V(p - h, y)) / (2 * h) / v, (V(p, y + h) - V(p, y - h)) / (2 * h) / v
    return V, G


def T_of(rho):
    return (30 * rho * m2u * MP ** 4 / (math.pi ** 2 * gs)) ** 0.25


def run(eps, gamma=math.pi / 2, f=0.99, p0=-10.0, Nafter=6.0, step=0.05):
    V, G = make(eps, gamma)
    def rhs_inf(N_, z):
        p, y, dp, dy = z; g = 1.5 * math.exp(-2 * c * p); e = 0.5 * (dp * dp + g * dy * dy); gp, gy = G(p, y)
        return [dp, dy, -c * g * dy * dy - (3 - e) * (dp + gp), 2 * c * dp * dy - (3 - e) * (dy + gy / g)]
    end = lambda N_, z: 0.5 * (z[2] ** 2 + 1.5 * math.exp(-2 * c * z[0]) * z[3] ** 2) - 1; end.terminal = True; end.direction = 1
    s = solve_ivp(rhs_inf, [0, 400], [p0, 0, 0, 0], events=end, rtol=1e-8, atol=1e-11, method="LSODA", dense_output=True)
    Ne = s.t_events[0][0]; p, y, dp, dy = s.y_events[0][0]
    epsH = lambda N_: (lambda z: 0.5 * (z[2] ** 2 + 1.5 * math.exp(-2 * c * z[0]) * z[3] ** 2))(s.sol(N_))
    e0 = epsH(Ne - 55.6); ns = 1 - 2 * e0 - (math.log(epsH(Ne - 55.6 + 0.01)) - math.log(e0)) / 0.01
    K = 0.5 * (dp * dp + 1.5 * math.exp(-2 * c * p) * dy * dy); H2 = V(p, y) / (3 - K)
    lnr0 = math.log(f * 0.5 * H2 * dp * dp); dp *= math.sqrt(1 - f)
    def rhs(N_, z):
        p, y, dp, dy, lnr = z; g = 1.5 * math.exp(-2 * c * p); K = 0.5 * (dp * dp + g * dy * dy)
        v = V(p, y); rr = math.exp(lnr); H2 = (v + rr) / (3 - K); e = K + (2 / 3) * rr / H2; gp, gy = G(p, y)
        return [dp, dy, -c * g * dy * dy - (3 - e) * dp - gp * v / H2, 2 * c * dp * dy - (3 - e) * dy - gy * v / (g * H2), -4.0]
    z = [p, y, dp, dy, lnr0]; Nn = Ne; Y = 0.0; prev = None; peak = 0.0
    while Nn < Ne + Nafter - 1e-9:
        z = list(solve_ivp(rhs, [Nn, Nn + step], z, rtol=1e-7, atol=1e-10, method="LSODA").y[:, -1]); Nn += step
        p, y, dp, dy, lnr = z; g = 1.5 * math.exp(-2 * c * p); K = 0.5 * (dp * dp + g * dy * dy)
        v = V(p, y); rr = math.exp(lnr); H2 = (v + rr) / (3 - K)
        T = T_of(rr); r = math.sqrt(g) * dy; H = math.sqrt(H2 * m2u) * MP; peak = max(peak, 0.5 * g * dy * dy / 3)
        if prev is not None:
            k = C.GW(T) / H; Yeq = -C.KEQ * C.cA * r * H / T; Y = Yeq + (Y - Yeq) * math.exp(-k * step)
        prev = T
    return {"N_end": Ne, "n_s": ns, "r_t": 16 * e0, "nBs": (28 / 79) * abs(Y), "peak_angle_share": peak}


if __name__ == "__main__":
    for eps in (1e-5, 1e-4, 1e-3):
        o = run(eps)
        m32 = m_inf * MP * math.sqrt(eps / (8 * A))
        print(f"eps {eps:.0e} (m_3/2 ~ {m32:.1e} GeV for W0 = Wc): N_end {o['N_end']:.1f} n_s {o['n_s']:.4f} r {o['r_t']:.4f} | "
              f"n_B/s {o['nBs']:.2e} (x{o['nBs'] / C.TARGET:.2g}) | peak angle share {o['peak_angle_share']:.1e}", flush=True)
