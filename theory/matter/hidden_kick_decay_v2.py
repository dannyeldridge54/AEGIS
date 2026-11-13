"""D36: Development 35 with the hidden field's DECAY and the entropy it releases. Realistic cliff n = 125, natural hidden
cosine strength suppressed by exp(-A Re T) (holomorphy), MATTER rate equation. AI-assisted.
Decay: sigma loses energy at rate Gamma = y^2 m_sigma / (8 pi) into radiation:
    sigma'' += -(Gamma/H) sigma'            (friction on the hidden field)
    d rho_r/dN = -4 rho_r + Gamma H sigma'^2  (its energy becomes radiation)
    Y (= n_{B-L}/s) is diluted by the entropy injected: d ln Y/dN -= (3/4) Gamma H sigma'^2 / rho_r.
Units M_P = 1, energies in m^2 (m = inflaton mass)."""
import cmath, math, os, sys
from scipy.integrate import solve_ivp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import chain_d22 as C
c = math.sqrt(2 / 3); A = math.pi / 4; MP = 2.435e18; m2u = 4 * 1.0668e-10; m_inf = math.sqrt(m2u) * MP; gs = 106.75
MU, N, M2 = 1e4, 125.0, 1.0
CLIFF = "old"


def T_of(rho):
    return (30 * rho * m2u * MP ** 4 / (math.pi ** 2 * gs)) ** 0.25


def run(m_sigma, ycoup, Omega0=0.05, fdec=0.1, f_rh=0.99, p0=-13.0, Nafter=11.0, step=0.02, s0=None):
    mus = m_sigma / m_inf; s0 = fdec if s0 is None else s0; Gam = ycoup ** 2 * m_sigma / (8 * math.pi) / m_inf
    L4x = lambda p: Omega0 * 3 * mus ** 2 * math.exp(-A * math.exp(c * p))
    def Vinf(p, y):
        x = math.exp(c * p); T = complex(x, y)
        return abs(T / cmath.sqrt(1 + T / MU) * (cmath.exp(-N * (1 - cmath.exp(-T / M2))) if CLIFF == "exp" else cmath.exp(-N * T / (T + M2)))) ** 2 / (4 * x * x)
    def V(p, y, s):
        return Vinf(p, y) + 0.5 * mus ** 2 * s * s + L4x(p) * (1 - math.cos(A * y - s / fdec))
    def dV(p, y, s, h=1e-6):
        cs = 1 - math.cos(A * y - s / fdec); sn = math.sin(A * y - s / fdec)
        vp = (Vinf(p + h, y) - Vinf(p - h, y)) / (2 * h) + (L4x(p + h) - L4x(p - h)) / (2 * h) * cs
        vy = (Vinf(p, y + h) - Vinf(p, y - h)) / (2 * h) + L4x(p) * A * sn
        vs = mus ** 2 * s - L4x(p) / fdec * sn
        return vp, vy, vs
    def rhs_inf(N_, z):
        p, y, s, dp, dy, ds = z; g = 1.5 * math.exp(-2 * c * p); K = 0.5 * (dp * dp + g * dy * dy + ds * ds)
        H2 = V(p, y, s) / (3 - K); vp, vy, vs = dV(p, y, s)
        return [dp, dy, ds, -c * g * dy * dy - (3 - K) * dp - vp / H2, 2 * c * dp * dy - (3 - K) * dy - vy / (g * H2), -(3 - K) * ds - vs / H2]
    end = lambda N_, z: 0.5 * (z[3] ** 2 + 1.5 * math.exp(-2 * c * z[0]) * z[4] ** 2 + z[5] ** 2) - 1; end.terminal = True; end.direction = 1
    s1 = solve_ivp(rhs_inf, [0, 400], [p0, 0, s0, 0, 0, 0], events=end, rtol=1e-8, atol=1e-12, method="LSODA")
    Ne = s1.t_events[0][0]; p, y, s, dp, dy, ds = s1.y_events[0][0]
    K = 0.5 * (dp * dp + 1.5 * math.exp(-2 * c * p) * dy * dy + ds * ds); H2 = V(p, y, s) / (3 - K)
    lnr = math.log(f_rh * 0.5 * H2 * dp * dp); dp *= math.sqrt(1 - f_rh)
    def rhs(N_, z):
        p, y, s, dp, dy, ds, lnr = z; g = 1.5 * math.exp(-2 * c * p); K = 0.5 * (dp * dp + g * dy * dy + ds * ds)
        rr = math.exp(lnr); v = V(p, y, s); H2 = (v + rr) / (3 - K); H = math.sqrt(H2)
        e = K + (2 / 3) * rr / H2; vp, vy, vs = dV(p, y, s); src = Gam * H * ds * ds
        return [dp, dy, ds, -c * g * dy * dy - (3 - e) * dp - vp / H2, 2 * c * dp * dy - (3 - e) * dy - vy / (g * H2),
                -(3 - e) * ds - vs / H2 - (Gam / H) * ds, -4.0 + src / rr]
    z = [p, y, s, dp, dy, ds, lnr]; Nn = Ne; Y = 0.0; peak_hid = 0.0; dil = 1.0
    while Nn < Ne + Nafter - 1e-9:
        z = list(solve_ivp(rhs, [Nn, Nn + step], z, rtol=1e-7, atol=1e-11, method="LSODA").y[:, -1]); Nn += step
        p, y, s, dp, dy, ds, lnr = z; g = 1.5 * math.exp(-2 * c * p); K = 0.5 * (dp * dp + g * dy * dy + ds * ds)
        rr = math.exp(lnr); v = V(p, y, s); H2 = (v + rr) / (3 - K); Hc = math.sqrt(H2)
        T = T_of(rr); r = math.sqrt(g) * dy; H = Hc * math.sqrt(m2u) * MP
        hid = (0.5 * ds * ds * H2 + 0.5 * mus ** 2 * s * s + L4x(p) * (1 - math.cos(A * y - s / fdec))) / (3 * H2)
        peak_hid = max(peak_hid, hid)
        k = C.GW(T) / H; Yeq = -C.KEQ * C.cA * r * H / T; Y = Yeq + (Y - Yeq) * math.exp(-k * step)
        f_dil = math.exp(-0.75 * Gam * Hc * ds * ds / rr * step); Y *= f_dil; dil *= f_dil
    return {"N_end": Ne, "nBs": (28 / 79) * abs(Y), "peak_hidden_share": peak_hid, "hidden_share_end": hid,
            "T_end": T, "entropy_dilution": 1 / dil, "Gamma_GeV": Gam * m_inf}


if __name__ == "__main__":
    for m in (6e9, 1e10):
        for yc in (0.0, 0.03, 0.1, 0.3):
            o = run(m, yc)
            print(f"m_sigma {m:.0e} GeV, y {yc}: n_B/s {o['nBs']:.2e} (x{o['nBs'] / C.TARGET:.2g}); peak hidden share {o['peak_hidden_share']:.2f}, "
                  f"at end {o['hidden_share_end']:.2e} (T {o['T_end']:.1e} GeV); entropy dilution x{o['entropy_dilution']:.2f}", flush=True)
