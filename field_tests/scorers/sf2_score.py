"""Score SF2 (field_tests/rules/PREREG_SF2_ANGLE.md) exactly as written. Reads stored fits; no fitting.
    python sf2_score.py      (results from $TWIST_RESULTS)"""
import json
import os

RES = os.environ.get("TWIST_RESULTS", os.path.join(os.path.dirname(__file__), "..", "..", "cmb-fit", "results"))
S = {"Union3": "_union3", "Pantheon+": "", "DES-Dovekie": "_dovekie"}


def chi2(n):
    p = os.path.join(RES, f"cmp_{n}.json")
    if not os.path.exists(p):
        return None
    v = json.load(open(p))["minimum"].get("chi2")
    return v if v == v else None


rows, D = {}, []
for lab, s in S.items():
    b0, bf = chi2(f"ax_spa_spiraltwist_beta0{s}_nlfix"), chi2(f"ax_spa_spiraltwist{s}_nlfix")
    lc, ww = chi2(f"ax_spa_lcdm_halofit{s}"), chi2(f"ax_spa_w0wa_halofit{s}")
    if b0 is None or bf is None:
        rows[lab] = "pending or NO VERDICT"
        continue
    d = b0 - bf
    D.append(d)
    rows[lab] = {"D (beta0 - beta free)": round(d, 2),
                 "beta0 - LCDM (reported)": None if lc is None else round(b0 - lc, 2),
                 "beta0 - w0wa (reported)": None if ww is None else round(b0 - ww, 2)}
out = {"rule": "PREREG_SF2_ANGLE.md", "rows": rows}
if len(D) == 3:
    out["verdict"] = ("ANGLE NEEDED" if sum(d >= 4 for d in D) >= 2 else
                      "ANGLE NOT NEEDED" if sum(d < 1 for d in D) >= 2 else "WEAK")
else:
    out["verdict"] = "pending"
print(json.dumps(out, indent=1))
