"""Score UB-2 exactly as field_tests/rules/PREREG_UNIFY_DATA.md says (variant B, Planck 2018 + DESI DR2 + one SN set).
    python ub2_score.py        (reads cmb-fit/results/cmp_*.json; $TWIST_RESULTS overrides the folder)"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.environ.get("TWIST_RESULTS", os.path.join(HERE, "..", "..", "cmb-fit", "results"))
SETS = (("Pantheon+", ""), ("DES-Dovekie", "_dovekie"), ("Union3", "_union3"))
K = {"ub2B": 4, "w0waP": 2, "edelockP": 2}           # free settings beyond LCDM (UB: lnL, theta_i, |phi|_i, kappa)
S8_OBS, S8_UP, S8_DN = 0.798, 0.014, 0.015            # DES Y6 cosmic shear, as S8-WL Part 1


def load(n):
    p = os.path.join(RES, f"cmp_{n}.json")
    return json.load(open(p))["minimum"] if os.path.exists(p) else None


def pen(m):
    s8 = m["sigma8"] * math.sqrt(m["omegam"] / 0.3)
    return s8, ((s8 - S8_OBS) / (S8_UP if s8 > S8_OBS else S8_DN)) ** 2


rows, dL, dW, unify = {}, [], [], []
for lab, suf in SETS:
    ub, lc, w, lt = load("ub2B" + suf), load("lcdmP" + suf), load("w0waP" + suf), load("edelockP" + suf)
    sp, spl = load("ax_spa_spiraltwist" + suf + "_nlfix"), load("ax_spa_lcdm_halofit" + suf)
    if ub is None or lc is None:
        rows[lab] = "NO VERDICT (fit missing)"
        continue
    r = {"chi2": round(ub["chi2"], 2), "dLCDM": round(ub["chi2"] - lc["chi2"], 2),
         "dAIC_vs_LCDM": round(ub["chi2"] - lc["chi2"] + 2 * K["ub2B"], 2)}
    dL.append(r["dLCDM"])
    if w:
        r["dW0WA"] = round(ub["chi2"] - w["chi2"], 2)
        r["dAIC_vs_W0WA"] = round(r["dW0WA"] + 2 * (K["ub2B"] - K["w0waP"]), 2)
        dW.append(r["dW0WA"])
    pieces = []
    if lt:
        pieces.append(("Locked Twist (same engine)", lt["chi2"] - lc["chi2"]))
    if sp and spl:
        pieces.append(("Spiral SF (AxiCLASS, own LCDM)", sp["chi2"] - spl["chi2"]))
    if pieces:
        best = min(pieces, key=lambda t: t[1])
        r["best_piece"] = {"name": best[0], "dLCDM": round(best[1], 2)}
        r["within_2_of_best_piece"] = r["dLCDM"] <= best[1] + 2
        unify.append(r["within_2_of_best_piece"])
    s8, p = pen(ub)
    s8l, pl = pen(lc)
    r["S8"] = round(s8, 4)
    r["S8_penalty_vs_LCDM"] = round(p - pl, 2)
    r["kappa"], r["H0"] = ub.get("ub_kappa"), round(ub["H0"], 2)
    rows[lab] = r
out = {"rule": "PREREG_UNIFY_DATA.md", "rows": rows}
if len(dL) == 3:
    out["vs_LCDM"] = ("BEATS LCDM" if sum(d <= -4 for d in dL) >= 2 else
                      "TIE" if not any(d <= -4 for d in dL) and not any(d >= 2 for d in dL) else "MIXED")
if len(dW) == 3:
    out["vs_w0wa"] = ("BEATS w0-wa" if sum(d <= -2 for d in dW) >= 2 else
                      "COMPETITIVE" if sum(d <= 2 for d in dW) >= 2 else "NOT COMPETITIVE")
if len(unify) == 3:
    out["unification"] = "UNIFIES" if sum(unify) >= 2 else "DOES NOT UNIFY"
print(json.dumps(out, indent=1))
