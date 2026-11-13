"""TWIST-INFLATION (rule: field_tests/rules/PREREG_TWIST_INFLATION.md, locked 12 Nov 2026 18:14 CT).
E-model alpha = 1: V = V0 (1 - exp(-sqrt(2/3) phi))^2 (reduced Planck units). Exact slow-roll parameters along the
trajectory (first order in slow roll, all orders in 1/N); phi_end from eps = 1; V0 from A_s = V/(24 pi^2 eps) = 2.1e-9.
N* for instantaneous reheating (Planck 2018 X, Eq. 47 form, w_int irrelevant):
    N* = 66.89 - ln(k*/(a0 H0)) + (1/4) ln(V*^2 / rho_end) - (1/12) ln(g_reh),  k* = 0.05/Mpc, rho_end = 1.5 V_end,
solved self-consistently. -> field_tests/results/twist_inflation.json. AI-assisted."""
import json, math, os
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); AEG = os.path.abspath(os.path.join(HERE, "..", ".."))
assert os.path.exists(os.path.join(AEG, "field_tests", "rules", "PREREG_TWIST_INFLATION.md.sha256")), "rule not locked"
c = math.sqrt(2 / 3); AS = 2.1e-9; G = 106.75; H0c = 67.4 / 299792.458; KSTAR = 0.05
f = lambda p: 1 - math.exp(-c * p)
eps = lambda p: 0.5 * (2 * c * math.exp(-c * p) / f(p)) ** 2
eta = lambda p: 2 * c * c * math.exp(-c * p) * (2 * math.exp(-c * p) - 1) / f(p) ** 2
pend = brentq(lambda p: eps(p) - 1, 0.01, 5)
Nof = lambda p: quad(lambda x: 1 / math.sqrt(2 * eps(x)), pend, p)[0]
phi_of_N = lambda N: brentq(lambda p: Nof(p) - N, pend + 1e-6, 30)


def obs(N):
    p = phi_of_N(N); e, h = eps(p), eta(p)
    V0 = AS * 24 * math.pi ** 2 * e / f(p) ** 2
    return {"N": N, "n_s": 1 - 6 * e + 2 * h, "r": 16 * e, "V*": V0 * f(p) ** 2, "rho_end": 1.5 * V0 * f(pend) ** 2}


N = 55.0
for _ in range(50):
    o = obs(N)
    Nn = 66.89 - math.log(KSTAR / H0c) + 0.25 * math.log(o["V*"] ** 2 / o["rho_end"]) - math.log(G) / 12
    if abs(Nn - N) < 1e-6:
        break
    N = Nn
o = obs(N)
MP = 2.435e18
o["H_inf_GeV"] = math.sqrt(o["V*"] / 3) * MP
o["T_reh_instant_GeV"] = (30 * o["rho_end"] / (math.pi ** 2 * G)) ** 0.25 * MP
NS = {"Planck 2018": (0.9649, 0.0042), "Planck+ACT+SPT": (0.9684, 0.0030), "Planck+ACT+DESI": (0.9743, 0.0034)}
o["NS_NOW_pulls"] = {k: round((o["n_s"] - m) / s, 2) for k, (m, s) in NS.items()}
o["band_check"] = {"n_s in 0.9636-0.9649": 0.9636 <= o["n_s"] <= 0.9649, "r in 0.0037-0.0040": 0.0037 <= o["r"] <= 0.0040}
o["R_FUTURE"] = "PENDING (no r measurement with sigma(r) <= 0.002 yet)"
o["rule"] = "PREREG_TWIST_INFLATION.md"
json.dump(o, open(os.path.join(AEG, "field_tests", "results", "twist_inflation.json"), "w"), indent=1, default=float)
print(json.dumps(o, indent=1, default=float))
