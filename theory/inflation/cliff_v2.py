"""Development 79 (exploratory): a reshaped cliff whose leftover slope dies off fast (option 1 after TAIL-F). AI-assisted.
Old cliff factor: exp(-n T/(T + m2))          leftover tail slope ~ c * 2n m2 / x       (dies like 1/x)
New cliff factor: exp(-n T^2/(T^2 + m2^2))    leftover tail slope ~ c * 4n m2^2 / x^2   (dies like 1/x^2)
Both: F = T / sqrt(1 + T/mu) * cliff, mu = 1, n = 125, V = m^2 |F|^2/(4x^2), K = -3 ln(T + Tbar - S Sbar + ...).
For each version: (1) inflation n_s, r, N* (instant-reheating N* as kahler_correction_ns.py; same method for old and new,
so the comparison is like for like); (2) where the field freezes after the cliff for heat share f (as tail_freeze.py:
start at eps = 1, radiation share f, follow 40 e-folds); (3) w0, wa thawing on the full tail (as tail_full_thaw.py);
(4) mass of the angle y on the plateau and today (as plateau_checks.py)."""
import math, sys
import numpy as np
import mpmath as mp
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq
c = math.sqrt(2 / 3); MU, NN = 1.0, 125.0
AS, G, H0c, KSTAR = 2.1e-9, 106.75, 67.4 / 299792.458, 0.05
Om, Or = 0.31, 9.1e-5; ODE = 1 - Om - Or


def version(kind, m2):
    if kind == "old":
        ex = lambda T: -NN * T / (T + m2); dex = lambda x: -NN * m2 / (x + m2) ** 2
    elif kind == "exp":                     # exp(-n (1 - e^{-T/m2})): linear at small x like the old one, leftover dies like e^{-x/m2}
        ex = lambda T: -NN * (1 - (mp.exp(-T / m2) if isinstance(T, (mp.mpc, mp.mpf)) else math.exp(-T / m2)))
        dex = lambda x: -NN * math.exp(-x / m2) / m2
    else:
        ex = lambda T: -NN * T * T / (T * T + m2 * m2); dex = lambda x: -2 * NN * x * m2 * m2 / (x * x + m2 * m2) ** 2
    lnV = lambda p: (lambda x: 2 * ex(x) - math.log(4 * (1 + x / MU)))(math.exp(c * p))   # ln(|F|^2/(4x^2)), real T
    Fc = lambda T: T / mp.sqrt(1 + T / MU) * mp.exp(ex(T))
    global DL
    DL = lambda p: (lambda x: c * x * (2 * dex(x) - 1 / (MU + x)))(math.exp(c * p))     # analytic d lnV / d phi
    return lnV, Fc


DL = None


def d(f, p, h=1e-5):
    return DL(p)                       # analytic slope of lnV for the current version (f kept for call shape)


def d2(f, p, h=1e-4):
    return (f(p + h) - 2 * f(p) + f(p - h)) / (h * h)


def inflation(lnV):
    eps = lambda p: 0.5 * d(lnV, p) ** 2
    eta = lambda p: (DL(p + 1e-5) - DL(p - 1e-5)) / 2e-5 + DL(p) ** 2
    ps = np.linspace(-25, 2, 4000); e = [eps(p) for p in ps]
    i = next(k for k in range(len(ps)) if e[k] >= 1); pend = brentq(lambda p: eps(p) - 1, ps[i - 1], ps[i])
    Nof = lambda p: quad(lambda q: -1 / d(lnV, q), p, pend, limit=200)[0]
    N = 55.0
    for _ in range(50):
        p = brentq(lambda q: Nof(q) - N, -25, pend - 1e-6)
        V0 = AS * 24 * math.pi ** 2 * eps(p) / math.exp(lnV(p))                      # m^2 from A_s
        Nn = 66.89 - math.log(KSTAR / H0c) + 0.25 * math.log((V0 * math.exp(lnV(p))) ** 2 / (1.5 * V0 * math.exp(lnV(pend)))) - math.log(G) / 12
        if abs(Nn - N) < 1e-6:
            break
        N = Nn
    p = brentq(lambda q: Nof(q) - N, -25, pend - 1e-6)
    return dict(N=N, ns=1 - 6 * eps(p) + 2 * eta(p), r=16 * eps(p), pstar=p, pend=pend)


def freeze(lnV, f, Nafter=40.0, p0=-13.0):
    V = lambda p: math.exp(lnV(p)); dV = lambda p: V(p) * d(lnV, p)
    def rhs(t, z):
        p, dp = z; K = 0.5 * dp * dp; H2 = V(p) / (3 - K); return [dp, -(3 - K) * dp - dV(p) / H2]
    end = lambda t, z: 0.5 * z[1] ** 2 - 1; end.terminal = True; end.direction = 1
    s = solve_ivp(rhs, [0, 4000], [p0, 0], events=end, rtol=1e-8, atol=1e-12, method="LSODA")
    p, dp = s.y_events[0][0]; H2 = V(p) / (3 - 0.5 * dp * dp); lnr = math.log(f * 0.5 * H2 * dp * dp); dp *= math.sqrt(1 - f)
    def rhs2(t, z):
        p, dp, lnr = z; rr = math.exp(lnr); K = 0.5 * dp * dp
        Vp = math.exp(lnV(p)) if lnV(p) > -700 else 0.0
        H2 = (Vp + rr) / (3 - K); e = K + (2 / 3) * rr / H2
        return [dp, -(3 - e) * dp - Vp * d(lnV, p) / H2, -4.0]
    s2 = solve_ivp(rhs2, [0, Nafter], [p, dp, lnr], rtol=1e-8, atol=1e-12, method="LSODA")
    return s2.y[0, -1]


def thaw(lnV, pf):
    Vf = lambda V0, p: V0 * math.exp(lnV(p) - lnV(pf))
    def go(V0):
        def rhs(N, y):
            p, v = y; a = math.exp(N); V = Vf(V0, p)
            H2 = (Om * a ** -3 + Or * a ** -4 + V / 3) / (1 - v * v / 6)
            eps = (1.5 * Om * a ** -3 + 2 * Or * a ** -4 + 0.5 * v * v * H2) / H2
            return [v, -(3 - eps) * v - V * d(lnV, p) / H2]
        return solve_ivp(rhs, [math.log(1e-4), 0], [pf, 0], rtol=1e-9, atol=1e-12, dense_output=True)
    def ode(V0):
        s = go(V0); p, v = s.y[:, -1]; V = Vf(V0, p); H2 = (Om + Or + V / 3) / (1 - v * v / 6)
        return (v * v * H2 / 6 + V / 3) / H2 - ODE
    V0 = brentq(ode, 1e-2, 1e4); s = go(V0); a = np.linspace(1 / 3, 1, 300); w = []
    for N in np.log(a):
        p, v = s.sol(N); A = math.exp(N); V = Vf(V0, p)
        H2 = (Om * A ** -3 + Or * A ** -4 + V / 3) / (1 - v * v / 6); K = v * v * H2 / 6; w.append((K - V / 3) / (K + V / 3))
    w0, wa = np.linalg.lstsq(np.vstack([np.ones(300), 1 - a]).T, np.array(w), rcond=None)[0]
    return w0, wa, s.y[0, -1]


def my2(Fc, x):
    mp.mp.dps = 30; x = mp.mpf(x)
    V = lambda y: abs(Fc(mp.mpc(x, y))) ** 2 / (4 * x * x)
    return float(mp.diff(V, 0, 2) / (2 * 3 / (4 * x * x)) / (V(0) / 3))


if __name__ == "__main__":
    cases = [(a.split(":")[0], float(a.split(":")[1])) for a in sys.argv[1:]] or [("old", 1.0)]
    for kind, m2 in cases:
        lnV, Fc = version(kind, m2); I = inflation(lnV)
        xs, xe = math.exp(c * I["pstar"]), math.exp(c * I["pend"])
        print(f"\n{kind} cliff, m2 = {m2}: N* {I['N']:.1f}, n_s {I['ns']:.4f}, r {I['r']:.4f}; CMB point x {xs:.2e}, end x {xe:.2e}; "
              f"angle on plateau m_y^2/H^2 {my2(Fc, xs):+.2f}", flush=True)
        for f in (4e-4, 1.3e-3, 4e-3):
            pf = freeze(lnV, f, p0=I["pstar"] - 1.0); xf = math.exp(c * pf); sl = -d(lnV, pf) / c
            try:
                w0, wa, pt = thaw(lnV, pf); xt = math.exp(c * pt)
                txt = f"w0 {w0:.3f}, wa {wa:.3f}; angle today m_y^2/H^2 {my2(Fc, xt):+.2f}"
            except ValueError:
                txt = "too steep for dark energy"
            print(f"   heat {f * 100:.2f}%: frozen x {xf:.3g}, slope {sl:.3f} x sqrt(2/3); {txt}", flush=True)
