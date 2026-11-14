"""D367 (locked, PREREG_D367_OMEGAKIN): instrumented copy of hidden_kick_decay_v2 (matter_refit_check settings). AI-assisted."""
import sys; sys.path.insert(0, "/home/claude/aegis/theory/matter")

import cmath, math, os, sys
from scipy.integrate import solve_ivp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import chain_d22 as C
c = math.sqrt(2 / 3); A = math.pi / 4; MP = 2.435e18; m2u = 4 * 1.0668e-10; m_inf = math.sqrt(m2u) * MP; gs = 106.75
MU, N, M2 = 1.0, 125.0, 4 / math.pi
CLIFF = "exp"


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
    import pickle, time as _t, os as _os
    _ck = _os.environ.get('D367_CKPT'); _t0 = _t.time()
    if _ck and _os.path.exists(_ck):
        z, Nn, Y, peak_hid, dil = pickle.load(open(_ck, 'rb')); print('resumed at N-Ne', round(Nn - Ne, 3), flush=True)
    while Nn < Ne + Nafter - 1e-9:
        z = list(solve_ivp(rhs, [Nn, Nn + step], z, rtol=1e-7, atol=1e-11, method="LSODA").y[:, -1]); Nn += step
        p, y, s, dp, dy, ds, lnr = z; g = 1.5 * math.exp(-2 * c * p); K = 0.5 * (dp * dp + g * dy * dy + ds * ds)
        rr = math.exp(lnr); v = V(p, y, s); H2 = (v + rr) / (3 - K); Hc = math.sqrt(H2)
        T = T_of(rr); r = math.sqrt(g) * dy; H = Hc * math.sqrt(m2u) * MP
        hid = (0.5 * ds * ds * H2 + 0.5 * mus ** 2 * s * s + L4x(p) * (1 - math.cos(A * y - s / fdec))) / (3 * H2)
        peak_hid = max(peak_hid, hid)
        k = C.GW(T) / H; Yeq = -C.KEQ * C.cA * r * H / T; Y = Yeq + (Y - Yeq) * math.exp(-k * step)
        f_dil = math.exp(-0.75 * Gam * Hc * ds * ds / rr * step); Y *= f_dil; dil *= f_dil
        if _ck and _t.time() - _t0 > float(_os.environ.get('D367_TLIM', '150')):
            pickle.dump((z, Nn, Y, peak_hid, dil), open(_ck, 'wb')); print('checkpoint at N-Ne', round(Nn - Ne, 3), flush=True); raise SystemExit(3)
        if abs(((Nn - Ne) / 0.5) - round((Nn - Ne) / 0.5)) < 1e-6 or abs(Nn - Ne - 11.0) < 1e-6:
            print(f"N-Ne {Nn-Ne:5.2f} T {T:.3e} Omega_kin_x {(dp*dp+g*dy*dy)/6:.3e} Omega_V {v/(3*H2):.3e} Omega_sigma {hid:.3e} x {math.exp(c*p):.3f} dp {dp:.3e} nBs {(28/79)*abs(Y):.4e}", flush=True)
    return {"N_end": Ne, "nBs": (28 / 79) * abs(Y), "peak_hidden_share": peak_hid, "hidden_share_end": hid,
            "T_end": T, "entropy_dilution": 1 / dil, "Gamma_GeV": Gam * m_inf, "x_end": math.exp(c * p), "y_end": y}


if __name__ == "__main__":
    o = run(5.8e10, 0.1, f_rh=0.008, Nafter=16.0)
    print("final", o, flush=True)
