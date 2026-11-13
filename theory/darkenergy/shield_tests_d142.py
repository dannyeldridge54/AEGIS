"""D142: the "isometry shield" constructed explicitly and run against every precision test. AI-assisted, order of magnitude.
Construction: the SM is neutral under both isometries of the T-disk (scaling T -> lambda T and shift T -> T + i c). Then a SM constant
(alpha, the proton mass via Lambda_QCD, ...) can depend on the tail only through the breaking:
   d ln(constant) = eps(x),  eps(x) = c_q * Re q(x)  +  c_p / x^p,     q = e^{-pi T/4}  (the cliff's own instanton)
Here: c_q = 1 (natural size), and the perturbative order p with coefficient c_p is what each test bounds.
x(z) along the late universe from the full thawing solution (reshaped cliff, heat 0.8%; frozen x = 72.7, today 88.9).
Tests (current limits, approximate): quasar spectra |d alpha/alpha| < 1e-6 (z = 1-3); Oklo |d alpha/alpha| < 1e-8 (z = 0.14);
atomic clocks |alpha_dot/alpha| < 1e-18 /yr (today); BBN |d alpha/alpha| < 1e-2 (z ~ 1e9); MICROSCOPE beta < 1.2e-6; Cassini 3.4e-3."""
import math, sys, numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
sys.path.insert(0, "/home/claude/aegis/theory/inflation"); import cliff_v2 as C
lnV, _ = C.version("exp", 4 / math.pi); c = C.c
pf = C.freeze(lnV, 0.008); Om, Or = C.Om, C.Or
Vf = lambda V0, p: V0 * math.exp(lnV(p) - lnV(pf))
def go(V0, N0=math.log(1e-9)):
    def rhs(N, y):
        p, v = y; a = math.exp(N); V = Vf(V0, p); H2 = (Om * a ** -3 + Or * a ** -4 + V / 3) / (1 - v * v / 6)
        eps = (1.5 * Om * a ** -3 + 2 * Or * a ** -4 + 0.5 * v * v * H2) / H2; return [v, -(3 - eps) * v - V * C.DL(p) / H2]
    return solve_ivp(rhs, [N0, 0], [pf, 0], rtol=1e-10, atol=1e-13, dense_output=True)
def ode(V0):
    s = go(V0); p, v = s.y[:, -1]; V = Vf(V0, p); H2 = (Om + Or + V / 3) / (1 - v * v / 6); return (v * v * H2 / 6 + V / 3) / H2 - C.ODE
V0 = brentq(ode, 1e-2, 1e4); S = go(V0)
x_of = lambda z: math.exp(c * S.sol(-math.log(1 + z))[0])
H0_per_yr = 67.4 / 3.0857e19 * 3.156e7
p0, v0 = S.sol(0.0); xdot_over_x = c * v0 * H0_per_yr          # d ln x / dt today (per year), v = dphi/dN
print(f"tail: x(z=1e9) {x_of(1e9):.2f}, x(3) {x_of(3):.2f}, x(1) {x_of(1):.2f}, x(0.14) {x_of(0.14):.2f}, today {x_of(0):.2f}; "
      f"d ln x/dt today {xdot_over_x:.2e} /yr")
qre = lambda x: math.exp(-math.pi * x / 4)
x0 = x_of(0)
print("\n(a) instanton part, c_q = 1:")
for lab, z, lim in (("quasars z=3", 3, 1e-6), ("quasars z=1", 1, 1e-6), ("Oklo z=0.14", 0.14, 1e-8), ("BBN", 1e9, 1e-2)):
    d = qre(x_of(z)) - qre(x0); print(f"   {lab}: d alpha/alpha {d:.1e} (limit {lim:.0e}) PASS by 10^{math.log10(lim/abs(d)):.0f}")
rate = abs(-math.pi / 4 * x0 * qre(x0) * xdot_over_x); print(f"   clocks: |alpha_dot/alpha| {rate:.1e} /yr (limit 1e-18) PASS by 10^{math.log10(1e-18/rate):.0f}")
print("\n(c) perturbative part c_p/x^p: largest coefficient c_p each test allows")
rows = []
for p in (1.0, 1.5, 2.0, 3.0, 4.0):
    lims = {}
    for lab, z, lim in (("quasar z=3", 3, 1e-6), ("Oklo", 0.14, 1e-8), ("BBN", 1e9, 1e-2)):
        d = abs(x_of(z) ** -p - x0 ** -p); lims[lab] = lim / d
    lims["clocks"] = 1e-18 / abs(p * x0 ** -p * xdot_over_x)
    lims["MICROSCOPE"] = 1.2e-6 / (p * x0 ** -p * c)
    lims["Cassini"] = 3.4e-3 / (p * x0 ** -p * c)
    tight = min(lims, key=lims.get)
    print(f"   p = {p}: " + ", ".join(f"{k} {v:.1e}" for k, v in lims.items()) + f"  -> tightest: {tight} (c_p < {lims[tight]:.1e})")
