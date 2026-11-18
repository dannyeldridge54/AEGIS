# AEGIS-FP P5GQKKTRGBSXV3AI · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Janus calculator: closed-form running alpha_s and running-of-running beta_s from (n_s, r).

For V ~ 1 - A e^{-p phi} + delta e^{q phi} with kappa = q/p (AEGIS D669, D671; paper Sec. V):
  rho   = p sqrt(r/2) / (1 - n_s)
  x     = (rho - 1) / (1 + kappa rho)
  alpha = -1/2 (1-n_s)^2 (1+x)(1+kappa^2 x) / (1 - kappa x)^2
  beta  = -1/4 (1-n_s)^3 (1+x) [(1-kappa x)(1+kappa^2 x) + (1+x)(1-kappa^3 x)] / (1 - kappa x)^3
x = 0 (no tilt) gives the attractor values alpha = -(1-n_s)^2/2, beta = -(1-n_s)^3/2.
Offset-corrected SERAPIS tau = i form (D640; c = ln1728 / 2pi, u = 1/I*):
  1-n_s = 8u^2[(2-x)+cu(5-x)], r = 64u^4(1+x)^2(1+2cu), alpha = -32u^4(1+x)[(4+x)+cu(23+2x)]
"""
from __future__ import annotations
import math
from dataclasses import dataclass

C_J = math.log(1728) / (2 * math.pi)

@dataclass
class JanusResult:
    x: float
    alpha_s: float
    beta_s: float

def janus(ns: float, r: float, p: float, kappa: float) -> JanusResult:
    if not (0 < 1 - ns and r > 0 and p > 0):
        raise ValueError("need n_s < 1, r > 0, p > 0")
    e = 1 - ns
    rho = p * math.sqrt(r / 2) / e
    x = (rho - 1) / (1 + kappa * rho)
    if 1 - kappa * x <= 0:
        raise ValueError("outside the relation's domain (1 - kappa x <= 0)")
    a = -0.5 * e**2 * (1 + x) * (1 + kappa**2 * x) / (1 - kappa * x) ** 2
    b = -0.25 * e**3 * (1 + x) * ((1 - kappa * x) * (1 + kappa**2 * x) + (1 + x) * (1 - kappa**3 * x)) / (1 - kappa * x) ** 3
    return JanusResult(x, a, b)

def janus_offset_serapis(ns: float, r: float, c: float = C_J) -> JanusResult:
    """Invert the D640 offset-corrected relations for (u, x), then predict alpha_s (beta_s from D666 leading form)."""
    from scipy.optimize import fsolve
    def eqs(v):
        u, x = v
        return [8*u*u*((2-x)+c*u*(5-x)) - (1-ns), 64*u**4*(1+x)**2*(1+2*c*u) - r]
    u0 = math.sqrt((1 - ns) / 16)
    u, x = fsolve(eqs, [u0, 0.3], xtol=1e-14)
    a = -32*u**4*(1+x)*((4+x)+c*u*(23+2*x))
    b = 128*u**6*(1+x)*(2*x*x - 5*x - 16)
    return JanusResult(x, a, b)

MODEL_CLASSES = {
    # name: (p, kappa, note)
    "alpha-attractor (no tilt)": (math.sqrt(2/3), 0.0, "p = sqrt(2/(3 alpha)); here alpha = 1"),
    "SERAPIS tau=i / rho (eps I1 or eps L tilt)": (2*math.sqrt(2), 0.5, "kappa = 1/n for an I^n plateau, n = 2 (D672)"),
    "SERAPIS-E (Epstein E(tau,2))": (2*math.sqrt(2), 1.0, "plateau 1 - a/E, tilt C E: p = q = 2 sqrt 2 (D692)"),
}
