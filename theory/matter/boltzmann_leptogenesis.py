"""MATTER full calculation (rule: field_tests/rules/PREREG_MATTER.md). Runs only once the rule is locked.
    python boltzmann_leptogenesis.py gate     equilibrium limit must reproduce chemical_balance.py: n_B/s = 3.96e-3 mu_A/T
    python boltzmann_leptogenesis.py run      -> field_tests/results/matter.json
Boltzmann equation for Y = n_(B-L)/s in x = ln(T_RH/T), radiation era:
    dY/dx = -(Gamma_W/H) (Y - Y_eq(T)),   Y_eq = -(45 / (2 pi^2 g*)) * (mu_l/mu_A) * (mu_A/T)
with the Weinberg-operator rate Gamma_W = 3 T^3 sum(m_i^2) / (4 pi^3 v^4), the derived source
mu_A/T = c_A phidot / (M_P T), c_A = sqrt(3/8), phidot = r H(T_RH) M_P (T/T_RH)^3 (free roll), and
n_B/s = (28/79) * |Y| after electroweak sphalerons. mu_l/mu_A = 0.5227 from chemical_balance.py (fast set at
T > 1e12 GeV). The sign (matter or antimatter) follows the roll direction and is not predicted. AI-assisted."""
import json, math, os, sys
import numpy as np
from scipy.integrate import solve_ivp
HERE = os.path.dirname(os.path.abspath(__file__)); AEG = os.path.abspath(os.path.join(HERE, "..", ".."))
RULE = os.path.join(AEG, "field_tests", "rules", "PREREG_MATTER.md")
MP, MPL, gs, v = 2.435e18, 1.221e19, 106.75, 174.0
cA = math.sqrt(3 / 8); RATIO = 0.5227; TARGET = 8.7e-11
MASSES = [0.0, 0.0086e-9, 0.0502e-9]          # GeV, normal ordering, lightest 0 (oscillation values)
H = lambda T: 1.66 * math.sqrt(gs) * T * T / MPL
GW = lambda T: 3 * T ** 3 * sum(m * m for m in MASSES) / (4 * math.pi ** 3 * v ** 4)
KEQ = 45 / (2 * math.pi ** 2 * gs) * RATIO
TRHS = [1e13, 3e13, 1e14, 1e15]


def locked():
    assert os.path.exists(RULE + ".sha256"), "PREREG_MATTER.md is not locked: not running"


def gate():
    locked()
    eq = (28 / 79) * KEQ
    ok = abs(eq - 3.96e-3) / 3.96e-3 < 0.005
    print({"n_B/s per mu_A/T (equilibrium)": eq, "expected": 3.96e-3, "pass": ok})
    return ok


def nb_over_s(TRH, r, T_end=1e11):
    def rhs(x, y):
        T = TRH * math.exp(-x)
        muA_T = cA * r * H(TRH) * MP * (T / TRH) ** 3 / (MP * T)
        return [-(GW(T) / H(T)) * (y[0] + KEQ * muA_T)]
    sol = solve_ivp(rhs, [0, math.log(TRH / T_end)], [0.0], rtol=1e-9, atol=1e-30, method="LSODA")
    return (28 / 79) * abs(sol.y[0, -1])


def run():
    assert gate(), "gate failed: NO VERDICT"
    rows = {}
    for TRH in TRHS:
        unit = nb_over_s(TRH, 1.0)                      # linear in r
        r_need = TARGET / unit if unit > 0 else math.inf
        rows[f"{TRH:.0e}"] = {"nB_s_per_unit_r": unit, "r_needed": r_need,
                              "angle_energy_share_at_TRH": r_need ** 2 / 6}
        print(TRH, rows[f"{TRH:.0e}"], flush=True)
    ok = [float(k) for k, v_ in rows.items() if v_["r_needed"] <= 0.3]
    tmin = min(ok) if ok else None
    out = {"rule": "PREREG_MATTER.md", "target_nB_s": TARGET, "c_A": cA, "mu_l_over_mu_A": RATIO, "rows": rows,
           "K_TEMP_min_TRH": tmin, "K_TEMP": ("VIABLE" if tmin is not None and tmin <= 1e15 else "NOT VIABLE"),
           "K_KIN_flag": {k: v_["angle_energy_share_at_TRH"] > 0.01 for k, v_ in rows.items()},
           "note": "K-GRAV: gravitino yield at the minimum T_RH from twist_baryogenesis_estimates.py (D3)"}
    json.dump(out, open(os.path.join(AEG, "field_tests", "results", "matter.json"), "w"), indent=1)
    print(out["K_TEMP"], tmin)


if __name__ == "__main__":
    {"gate": gate, "run": run}[sys.argv[1]]()
