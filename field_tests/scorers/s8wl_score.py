"""Score S8-WL Part 1 (field_tests/rules/PREREG_S8_WL.md) exactly as written: DES Y6 S8 penalty at stored best fits.
    python s8wl_score.py       (results from $TWIST_RESULTS, plus $TWIST_RESULTS_EXTRA for fits stored elsewhere)"""
import json
import math
import os

OBS, UP, DN = 0.798, 0.014, 0.015
DIRS = [d for d in (os.environ.get("TWIST_RESULTS"), os.environ.get("TWIST_RESULTS_EXTRA"),
                    os.path.join(os.path.dirname(__file__), "..", "..", "cmb-fit", "results")) if d]
PAIRS = {"Locked Twist (Planck+DESI+Pantheon+)": ("edelockP", "lcdmP"),
         "Spiral, Pantheon+": ("ax_spa_spiraltwist_nlfix", "ax_spa_lcdm_halofit"),
         "Spiral, DES-Dovekie": ("ax_spa_spiraltwist_dovekie_nlfix", "ax_spa_lcdm_halofit_dovekie"),
         "Spiral, Union3": ("ax_spa_spiraltwist_union3_nlfix", "ax_spa_lcdm_halofit_union3")}


def load(n):
    for d in DIRS:
        p = os.path.join(d, f"cmp_{n}.json")
        if os.path.exists(p):
            return json.load(open(p))["minimum"]
    return None


OMEGA_NU = 0.06 / 93.14          # one massive neutrino, 0.06 eV, as in every fit


def s8(m):
    """S8 = sigma8 sqrt(Omega_m/0.3), with Omega_m = (omega_b + omega_cdm + omega_nu)/h^2 for every fit. AxiCLASS's own
    Omega_m output counts a dark-energy scalar field as matter (the B0 bug, nlfix/BUG_REPORT.md): 2.89 for the Spiral."""
    wb, wc = m.get("omega_b", m.get("ombh2")), m.get("omega_cdm", m.get("omch2"))
    h = m["H0"] / 100
    return m["sigma8"] * math.sqrt((wb + wc + OMEGA_NU) / h ** 2 / 0.3)


def pen(x):
    return ((x - OBS) / (UP if x > OBS else DN)) ** 2


out = {"rule": "PREREG_S8_WL.md Part 1", "data": "DES Y6 cosmic shear S8 = 0.798 +0.014/-0.015", "rows": {}}
for lab, (m, l) in PAIRS.items():
    a, b = load(m), load(l)
    if a is None or b is None:
        out["rows"][lab] = "pending (fit not found)"
        continue
    sa, sb = s8(a), s8(b)
    p = pen(sa) - pen(sb)
    out["rows"][lab] = {"S8_model": round(sa, 4), "S8_LCDM": round(sb, 4), "penalty": round(p, 2),
                        "reading": "PASSES" if p <= 2 else "OVER"}
print(json.dumps(out, indent=1))
