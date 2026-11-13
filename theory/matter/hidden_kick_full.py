"""D31: the hidden-axion kick in the full model (dilaton + angle + hidden field + radiation), with MATTER on top.
Mirrored plateau -> cliff -> tail inflaton (sugra_mirror.py, mu = 1e4, m2 = 1, n = 10, no stand-in kick), plus a sequestered
hidden field s (flat metric, no exp(K) factor):
    V/m^2 = |F0|^2/(4x^2) + (mu_s^2/2) s^2 + L4 [1 - cos(A y - s/f)],   A = pi/4 (Nieh-Yan period 8 in the angle coordinate y;
    assumption: the period is applied in the model's own angle frame), mu_s = m_sigma/m.
L4 = Omega_h * 3 mu_s^2 (the hidden cosine's energy share when H = m_sigma); s starts at s0 = f (as the toy run).
Radiation from instant preheating (f_rh). Units M_P = 1, energies in m^2, m = inflaton mass. AI-assisted."""
import cmath, math, os, sys
from scipy.integrate import solve_ivp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import chain_d22 as C
c = math.sqrt(2 / 3); A = math.pi / 4; MP = 2.435e18; m2u = 4 * 1.0668e-10; m_inf = math.sqrt(m2u) * MP; gs = 106.75
MU, N, M2 = 1e4, 10.0, 1.0


def T_of(rho):
    return (30 * rho * m2u * MP ** 4 / (math.pi ** 2 * gs)) ** 0.25


def run(Omega_h, m_sigma=1.4e8, fdec=0.1, f_rh=0.99, p0=-10.0, Nafter=10.0, step=0.02):
    mus = m_sigma / m_inf; L4 = Omega_h * 3 * mus ** 2; s0 = fdec
    def Vinf(p, y):
        x = math.exp(c * p); T = complex(x, y)
        return abs(T / cmath.sqrt(1 + T / MU) * cmath.exp(-N * T / (T + M2))) ** 2 / (4 * x * x)
    def V(p, y, s):
        return Vinf(p, y) + 0.5 * mus ** 2 * s * s + L4 * (1 - math.cos(A * y - s / fdec))
    def dV(p, y, s, h=1e-6):
        vp = (Vinf(p + h, y) - Vinf(p - h, y)) / (2 * h)
        vy = (Vinf(p, y + h) - Vinf(p, y - h)) / (2 * h) + L4 * A * math.sin(A * y - s / fdec)
        vs = mus ** 2 * s - L4 / fdec * math.sin(A * y - s / fdec)
        return vp, vy, vs
    def rhs_inf(N_, z):
        p, y, s, dp, dy, ds = z; g = 1.5 * math.exp(-2 * c * p); K = 0.5 * (dp * dp + g * dy * dy + ds * ds)
        v = V(p, y, s); H2 = v / (3 - K); vp, vy, vs = dV(p, y, s)
        return [dp, dy, ds, -c * g * dy * dy - (3 - K) * dp - vp / H2, 2 * c * dp * dy - (3 - K) * dy - vy / (g * H2), -(3 - K) * ds - vs / H2]
    end = lambda N_, z: 0.5 * (z[3] ** 2 + 1.5 * math.exp(-2 * c * z[0]) * z[4] ** 2 + z[5] ** 2) - 1; end.terminal = True; end.direction = 1
    s1 = solve_ivp(rhs_inf, [0, 400], [p0, 0, s0, 0, 0, 0], events=end, rtol=1e-8, atol=1e-12, method="LSODA")
    Ne = s1.t_events[0][0]; p, y, s, dp, dy, ds = s1.y_events[0][0]
    K = 0.5 * (dp * dp + 1.5 * math.exp(-2 * c * p) * dy * dy + ds * ds); H2 = V(p, y, s) / (3 - K)
    lnr = math.log(f_rh * 0.5 * H2 * dp * dp); dp *= math.sqrt(1 - f_rh)
    def rhs(N_, z):
        p, y, s, dp, dy, ds, lnr = z; g = 1.5 * math.exp(-2 * c * p); K = 0.5 * (dp * dp + g * dy * dy + ds * ds)
        v = V(p, y, s); rr = math.exp(lnr); H2 = (v + rr) / (3 - K); e = K + (2 / 3) * rr / H2; vp, vy, vs = dV(p, y, s)
        return [dp, dy, ds, -c * g * dy * dy - (3 - e) * dp - vp / H2, 2 * c * dp * dy - (3 - e) * dy - vy / (g * H2),
                -(3 - e) * ds - vs / H2, -4.0]
    z = [p, y, s, dp, dy, ds, lnr]; Nn = Ne; Y = 0.0; first = True
    peak_ang = peak_hid = 0.0; r_at = {}
    while Nn < Ne + Nafter - 1e-9:
        z = list(solve_ivp(rhs, [Nn, Nn + step], z, rtol=1e-7, atol=1e-11, method="LSODA").y[:, -1]); Nn += step
        p, y, s, dp, dy, ds, lnr = z; g = 1.5 * math.exp(-2 * c * p); K = 0.5 * (dp * dp + g * dy * dy + ds * ds)
        v = V(p, y, s); rr = math.exp(lnr); H2 = (v + rr) / (3 - K)
        T = T_of(rr); r = math.sqrt(g) * dy; H = math.sqrt(H2 * m2u) * MP
        peak_ang = max(peak_ang, 0.5 * g * dy * dy / 3)
        peak_hid = max(peak_hid, (0.5 * ds * ds * H2 + 0.5 * mus ** 2 * s * s + L4 * (1 - math.cos(A * y - s / fdec))) / (3 * H2))
        for Tm in (1e14, 3e13, 1e13, 3e12):
            if Tm not in r_at and T <= Tm:
                r_at[Tm] = r
        if not first:
            k = C.GW(T) / H; Yeq = -C.KEQ * C.cA * r * H / T; Y = Yeq + (Y - Yeq) * math.exp(-k * step)
        first = False
    H_inf = math.sqrt(Vinf(-10.0, 0) * m2u / 3) * MP
    iso = (H_inf / (2 * math.pi)) / (s0 * MP)                       # delta sigma / sigma0 -> baryon isocurvature
    return {"N_end": Ne, "nBs": (28 / 79) * abs(Y), "T_last": T, "r_at": r_at, "peak_angle_share": peak_ang,
            "peak_hidden_share": peak_hid, "iso_dsig_over_sig": iso}


if __name__ == "__main__":
    for Om in (0.003, 0.01, 0.03):
        o = run(Om)
        print(f"Omega_h {Om}: N_end {o['N_end']:.1f}; n_B/s {o['nBs']:.2e} (x{o['nBs'] / C.TARGET:.2g} of observed); "
              f"angle r at T: {{{', '.join(f'{k:.0e}: {v:+.3f}' for k, v in o['r_at'].items())}}}; "
              f"peak shares angle {o['peak_angle_share']:.1e}, hidden {o['peak_hidden_share']:.1e}; "
              f"T at end of run {o['T_last']:.1e} GeV; isocurvature d(sigma)/sigma ~ {o['iso_dsig_over_sig']:.1e}", flush=True)
