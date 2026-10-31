"""Stability check of the Locked Twist field WITH expansion (ROADMAP_MATH.md step 3.5, second pass).

Units: phi in F, time in 1/m with m^2 = Lambda^4/F^2, scale factor a = 1 at the switch-on (matter-radiation
equality, the lock). Width F = sqrt(3/2) M_Pl / 9, so (M_Pl/F)^2 = 54.

  background  H(a) = Hc sqrt((a^-4 + a^-3) / 2)        radiation + matter, equal at a = 1 (field neglected in H)
              phi'' + 3 H phi' + V'(phi) = 0,  V = (1 - cos phi)^3
  energy share f(a) = rho_phi / (3 (M_Pl/F)^2 H^2)
  ripples     d'' + 3 H d' + (k^2/a^2 + V''(phi)) d = 0       (comoving k in units of m; metric perturbations
                                                              neglected, so this is a first, field-only estimate)

Hc is tuned so that f(a) peaks at a = 1, as the lock requires. Each ripple's growth is measured against the same
ripple evolved with V'' = 0 (pure expansion): G_k = late-time amplitude / free amplitude. ln G of about 11.5 (a 10^5
boost) would turn 10^-5 primordial ripples non-linear, i.e. fragmentation.

Run: python floquet_expanding.py
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

MPL_OVER_F_SQ = (9 / np.sqrt(1.5)) ** 2         # = 54
LNA0, LNA1 = np.log(0.02), np.log(40.0)


def dV(x):
    return 3 * (1 - np.cos(x)) ** 2 * np.sin(x)


def d2V(x):
    return 6 * (1 - np.cos(x)) * np.sin(x) ** 2 + 3 * (1 - np.cos(x)) ** 2 * np.cos(x)


def V(x):
    return (1 - np.cos(x)) ** 3


def H(lna, Hc):
    a = np.exp(lna)
    return Hc * np.sqrt((a ** -4 + a ** -3) / 2)


def background(theta, Hc, dense=False):
    def rhs(lna, y):
        h = H(lna, Hc)
        return [y[1] / h, (-3 * h * y[1] - dV(y[0])) / h]
    return solve_ivp(rhs, (LNA0, LNA1), [theta, 0.0], rtol=1e-9, atol=1e-11, dense_output=dense, max_step=0.01)


def share_peak(theta, Hc):
    s = background(theta, Hc)
    h = H(s.t, Hc)
    f = (0.5 * s.y[1] ** 2 + V(s.y[0])) / (3 * MPL_OVER_F_SQ * h ** 2)
    i = int(np.argmax(f))
    return s.t[i], f[i]


def tune_Hc(theta):
    """Hc such that the energy share peaks at a = 1 (ln a = 0)."""
    return np.exp(brentq(lambda lh: share_peak(theta, np.exp(lh))[0], np.log(0.02), np.log(50.0), xtol=1e-4))


def growth(theta, Hc, ks):
    nk = len(ks)

    def rhs(lna, y):
        h, a = H(lna, Hc), np.exp(lna)
        phi, pi = y[0], y[1]
        d, dd, fr, dfr = y[2:2 + nk], y[2 + nk:2 + 2 * nk], y[2 + 2 * nk:2 + 3 * nk], y[2 + 3 * nk:]
        k2 = (ks / a) ** 2
        return np.concatenate([[pi / h, (-3 * h * pi - dV(phi)) / h],
                               dd / h, (-3 * h * dd - (k2 + d2V(phi)) * d) / h,
                               dfr / h, (-3 * h * dfr - k2 * fr) / h])

    y0 = np.concatenate([[theta, 0.0], np.ones(nk), np.zeros(nk), np.ones(nk), np.zeros(nk)])
    s = solve_ivp(rhs, (LNA0, LNA1), y0, rtol=1e-8, atol=1e-12, max_step=0.005, dense_output=False)
    late = s.t > LNA1 - 1.0                          # last e-fold: compare envelopes
    d = np.abs(s.y[2:2 + nk, late]).max(1)
    fr = np.abs(s.y[2 + 2 * nk:2 + 3 * nk, late]).max(1)
    return np.log(d / fr)


if __name__ == "__main__":
    ks = np.linspace(0.05, 6.0, 60)
    print("theta_i   Hc      peak share f   max ln G (k)      G = growth factor vs pure expansion")
    for theta in (1.0, 2.0, 2.41421, 2.6, 2.7887, 2.9, 3.0):
        Hc = tune_Hc(theta)
        _, fpk = share_peak(theta, Hc)
        lnG = growth(theta, Hc, ks)
        i = int(np.argmax(lnG))
        verdict = "FRAGMENTS (>10^5)" if lnG[i] > 11.5 else ("strong" if lnG[i] > 5 else "mild")
        print(f"{theta:7.4f}  {Hc:6.3f}   {fpk:9.4f}     {lnG[i]:7.2f} ({ks[i]:.2f})   G = {np.exp(lnG[i]):.3g}  {verdict}")
