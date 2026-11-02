"""Shooting guess for the effective Spiral Twist in the coupled AxiCLASS build (CubeMind PREREGISTRATION_SPIRAL_FIT.md).
The build uses double_exp with V = mu1^4 e^(-kappa phi), phi_ini = kappa (this build reads phi_ini from
scf_parameters[0]) and the CDM coupling beta. AxiCLASS's default guess cannot bracket mu1 when beta != 0, so this solves
the same background (exponential field + coupled CDM, closure H(0) = 1) and returns mu1. Validated: CubeMind
spiral_class_mirror.py (CLASS vs this solver: w to 2e-5, H to 8e-5)."""
import math

from scipy.integrate import solve_ivp
from scipy.optimize import brentq

N0 = -math.log(1 + 1e5)


def mu1_guess(kappa, beta, omega_b, omega_cdm, h=0.68, omega_r=4.2e-5):
    om_b, om_c, orad = omega_b / h ** 2, omega_cdm / h ** 2, omega_r / h ** 2

    def run(V0):
        def rhs(N, y):
            c, cp = y
            rb, rc = 3 * om_b * math.exp(-3 * N), 3 * om_c * math.exp(-3 * N) * math.exp(beta * c)
            rr = 3 * orad * math.exp(-4 * N)
            V = V0 * math.exp(-kappa * c)
            H2 = (rb + rc + rr + V) / (3 - 0.5 * cp * cp)
            eps = (rb + rc + 4 * rr / 3 + H2 * cp * cp) / (2 * H2)
            return [cp, -(3 - eps) * cp + (kappa * V - beta * rc) / H2]
        s = solve_ivp(rhs, (N0, 0.0), [0.0, 0.0], method="LSODA", rtol=1e-8, atol=1e-10)
        c, cp = s.y[:, -1]
        rb, rc, rr = 3 * om_b, 3 * om_c * math.exp(beta * c), 3 * orad
        return (rb + rc + rr + V0 * math.exp(-kappa * c)) / (3 - 0.5 * cp * cp) - 1

    V0 = brentq(run, 1e-4, 50, xtol=1e-9)
    H0 = h / 2997.92458
    return (V0 * H0 * H0 * math.exp(kappa * kappa)) ** 0.25
