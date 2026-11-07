"""Score SF (PREREGISTRATION_SPIRAL_FIT.md, locked 2026-11-02 17:01:01). Reads the stored fits; no fitting.
    python spiral_score.py   -> spiral_score.json"""
import json
import os

RES = os.environ.get("TWIST_RESULTS", r"C:\Users\Danny\.copilot\repos\AEGIS\cmb-fit\results")
SAMPLES = {"Pantheon+": ("ax_spa_spiraltwist_nlfix", "ax_spa_lcdm_halofit", "ax_spa_w0wa_halofit"),
           "DES-Dovekie": ("ax_spa_spiraltwist_dovekie_nlfix", "ax_spa_lcdm_halofit_dovekie", "ax_spa_w0wa_halofit_dovekie"),
           "Union3": ("ax_spa_spiraltwist_union3_nlfix", "ax_spa_lcdm_halofit_union3", "ax_spa_w0wa_halofit_union3")}


def load(n):
    p = os.path.join(RES, f"cmp_{n}.json")
    return json.load(open(p))["minimum"] if os.path.exists(p) else None


rows, dl, dw = {}, [], []
for s, (sp, lc, ww) in SAMPLES.items():
    a, b, c = load(sp), load(lc), load(ww)
    if a is None or b is None or c is None or not all(map(lambda x: x == x, [a["chi2"]])):
        rows[s] = {"status": "pending or NO VERDICT"}
        continue
    beta = a.get("scf_coupling_beta")
    r = {"dLCDM": a["chi2"] - b["chi2"], "dW0WA": a["chi2"] - c["chi2"], "kappa": a.get("spiral_kappa"),
         "beta_eff": beta, "f_implied": (beta / 0.816) if beta is not None else None, "sigma8": a.get("sigma8"),
         "H0_label": a.get("H0")}
    rows[s] = r
    dl.append(r["dLCDM"]); dw.append(r["dW0WA"])
out = {"rows": rows}
if len(dl) == 3:
    out["vs_LCDM"] = ("BEATS LCDM" if sum(x <= -4 for x in dl) >= 2 else
                      "TIE" if all(x > -4 for x in dl) and all(x < 2 for x in dl) else "MIXED")
    out["vs_w0wa"] = ("BEATS w0-wa" if sum(x <= -2 for x in dw) >= 2 else
                      "COMPETITIVE" if sum(x <= 2 for x in dw) >= 2 else "NOT COMPETITIVE")
else:
    out["vs_LCDM"] = out["vs_w0wa"] = "pending"
json.dump(out, open("spiral_score.json", "w"), indent=1)
print(json.dumps(out, indent=1))
