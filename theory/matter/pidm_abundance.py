"""D38 (exploratory): gravity-only dark matter (Planckian-interacting, PIDM) with the Twist's hot reheating. AI-assisted.
Only gravity connects dark matter to ordinary matter: SM SM -> graviton -> X X in the hot plasma after reheating.
Rate (massless limit), Clery, Mambrini, Olive & Verner, arXiv:2112.15214:  R = beta_j T^8 / M_P^4 (reduced M_P),
    beta_0 = 3997 pi^3 / 41472000 (scalar),  beta_1/2 = 11351 pi^3 / 20736000 (Dirac fermion).
Mass threshold: assumption of this script (not from the paper) — the T^8 rate is the Gondolo-Gelmini integral with
reduced cross section ~ s^2, so for a mass m we cut it at s > 4 m^2 with the kinematic factor sqrt(1-4m^2/s):
    F(z) = int_{2z} x^6 K1(x) sqrt(1-4z^2/x^2) dx / int_0 x^6 K1(x) dx,   z = m/T.
Yield Y = n/s from T_RH down (instant reheating, radiation after, g = 106.75):  dY/dT = -R/(s H T).
Omega h^2 = 2.745e8 (m/GeV) Y  (s0 = 2891 cm^-3, rho_c/h^2 = 1.054e-5 GeV cm^-3).
Garny, Sandora & Sloth, arXiv:1511.03278: T_rh = 0.25 gamma sqrt(M_P H_i); viable masses 1e-10 - 1e-2 M_P for gamma = 1."""
import math
from scipy.integrate import quad
from scipy.special import k1
from scipy.optimize import brentq

MP = 2.435e18; g = 106.75
BETA = {"scalar": 3997 * math.pi ** 3 / 41472000, "fermion": 11351 * math.pi ** 3 / 20736000}
NORM = quad(lambda x: x ** 6 * k1(x), 0, 200)[0]


def F(z):
    if z < 1e-3:
        return 1.0
    lo = 2 * z
    return quad(lambda x: x ** 6 * k1(x) * math.sqrt(max(0.0, 1 - 4 * z * z / (x * x))), lo, lo + 200, limit=200)[0] / NORM


def yield_Y(m, T_RH, spin="scalar"):
    c = (2 * math.pi ** 2 / 45) * g * math.sqrt(math.pi ** 2 * g / 90)
    f = lambda lnT: BETA[spin] * math.exp(lnT) ** 3 / (c * MP ** 3) * F(m / math.exp(lnT))
    lo = math.log(max(T_RH * 1e-6, m / 60))
    if lo >= math.log(T_RH):
        return 0.0
    return quad(f, lo, math.log(T_RH), limit=200)[0]


def omega(m, T_RH, spin="scalar"):
    return 2.745e8 * m * yield_Y(m, T_RH, spin)


def mass_for_dm(T_RH, spin="scalar", target=0.12):
    """Light branch (m << T_RH) and heavy branch (m >~ T_RH, Boltzmann-suppressed) masses giving Omega h^2 = target."""
    out = []
    grid = [10 ** (k / 8) for k in range(-16, 153)]
    grid = [x for x in grid if 1e-2 < x < 1e19]
    vals = [omega(x, T_RH, spin) - target for x in grid]
    for a, b, va, vb in zip(grid, grid[1:], vals, vals[1:]):
        if va * vb < 0:
            out.append(brentq(lambda x: omega(x, T_RH, spin) - target, a, b, rtol=1e-4))
    return out


if __name__ == "__main__":
    print("Gravity-only dark matter: mass(es) giving Omega h^2 = 0.12, by reheating temperature (GeV)")
    for T in (1e13, 3e13, 1e14, 3e14, 1e15):
        for spin in ("scalar", "fermion"):
            ms = mass_for_dm(T, spin)
            print(f"T_RH {T:.0e}  {spin:7s}: " + (", ".join(f"m = {x:.2e} GeV ({x / MP:.1e} M_P)" for x in ms) or "no solution"), flush=True)
