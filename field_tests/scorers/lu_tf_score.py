"""Score LU (PREREGISTRATION_LATE_UNION3.md, locked 14:23:26), TF (PREREGISTRATION_TORSION_F.md, 14:51:28) and TF-P
(PREREGISTRATION_TORSION_F_PLANCK.md, 14:55:36) exactly as written. Missing runs print as pending. Written before any
of their results existed. Writes lu_tf_score.json.
    python lu_tf_score.py"""
import glob
import json
import os
import re

RES = os.environ.get("TWIST_RESULTS") or r"C:\Users\Danny\.copilot\repos\AEGIS\cmb-fit\results"  # field_tests: env override only
if not os.path.isdir(RES):
    RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "fit_results")


def chi2(n):
    p = os.path.join(RES, f"cmp_{n}.json")
    return json.load(open(p))["minimum"]["chi2"] if os.path.exists(p) else None


out = {}
# ---- LU -------------------------------------------------------------------------------------------------------------
lt, ref, w = (chi2(n) for n in ("ax_spa_latetwist_gF0m0.102_union3_nlfix", "ax_spa_lcdm_halofit_union3",
                                "ax_spa_w0wa_halofit_union3"))
if lt is not None and ref is not None:
    du = lt - ref
    v = "CONFIRMED" if du <= -4 else "WEAKENED" if du <= -1 else "NOT CONFIRMED"
    out["LU"] = {"delta_U": du, "verdict": v, "w0wa_vs_LCDM (context)": None if w is None else w - ref}
    print(f"LU: delta_U = {du:+.2f} -> {v}" + ("" if w is None else f"   (w0-wa on Union3: {w - ref:+.2f})"))
else:
    print("LU: pending")

# ---- TF / TF-P ------------------------------------------------------------------------------------------------------
SAMPLES = {"DES Y5": ("_desy5", "ax_spa_lcdm_halofit_desy5"), "Pantheon+": ("", "ax_spa_lcdm_halofit"),
           "Union3": ("_union3", "ax_spa_lcdm_halofit_union3")}
FVALS = {"F1 = sqrt(3/2)": "0.0880", "F2 = sqrt6": "0.3891", "F_P = (4/pi) sqrt(3/2)": "0.1930"}


def best_free(suffix):
    """Lowest chi2 on that sample among grid + edge points, the LU point and every F-fixed run (the rule's 'best free fit')."""
    pats = [f"cmp_ax_spa_latetwist_gF*m*{suffix}_nlfix.json", f"cmp_ax_spa_latetwist_fF*{suffix}_nlfix.json"]
    vals = []
    for pat in pats:
        for p in glob.glob(os.path.join(RES, pat)):
            name = os.path.basename(p)[4:-5]
            body = name.replace("ax_spa_latetwist_", "").replace("_nlfix", "")
            # keep only runs on exactly this SN sample (no other sample tag, no nobao/r4/dovekie)
            tags = re.sub(r"^(gF-?[0-9.]+m-?[0-9.]+|fF-?[0-9.]+)", "", body)
            if tags != suffix:
                continue
            vals.append(json.load(open(p))["minimum"]["chi2"])
    return min(vals) if vals else None


for lab, (suf, refname) in SAMPLES.items():
    r, b = chi2(refname), best_free(suf)
    for flab, lf in FVALS.items():
        c = chi2(f"ax_spa_latetwist_fF{lf}{suf}_nlfix")
        key = f"{flab} | {lab}"
        if c is None or r is None or b is None:
            print(f"{key}: pending")
            continue
        D, G = c - b, c - r
        v = ("SUPPORTED" if G <= -4 else "CONSISTENT") if D <= 1 else "DISFAVOURED" if D <= 4 else "EXCLUDED"
        out[key] = {"D_F": D, "G_F": G, "verdict (rule applies to DES Y5)": v}
        print(f"{key}: D_F = {D:+.2f}, G_F = {G:+.2f} -> {v}" + ("" if lab == "DES Y5" else "  (information)"))
print("Look-elsewhere: 3 F values declared in total (F1, F2, F_P).")
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lu_tf_score.json"), "w"), indent=1)
