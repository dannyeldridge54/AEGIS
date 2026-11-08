"""Score V7 exactly as field_tests/rules/PREREG_V7_LOOK_ELSEWHERE.md says.
    python v7_look_elsewhere.py   (reads cmb-fit/results; $TWIST_RESULTS overrides) -> ../results/v7_look_elsewhere.json"""
import glob
import json
import os
import re

from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.environ.get("TWIST_RESULTS", os.path.join(HERE, "..", "..", "cmb-fit", "results"))
DATA_SUF = r"_(dovekie|union3|desy5)"
TAIL = r"(_(s8y6_more|s8y6|nobao|cmbonly|planckfull_snjla|planckfull_snpantheon|planckfull|nlfix|r4|more|b4))+$"


def core(name):
    n = re.sub(r"\.stalled\d*$", "", name)
    n = re.sub(DATA_SUF, "", n)
    n = re.sub(r"_(nobao|cmbonly|planckfull_snjla|planckfull_snpantheon|planckfull)(?=_|$)", "", n)
    n = re.sub(TAIL, "", n)
    return n


names = [os.path.basename(p)[4:-5] for p in glob.glob(os.path.join(RES, "cmp_ax_spa_*.json")) +
         glob.glob(os.path.join(RES, "cmp_spiralL*.json"))]
hyp = sorted({core(n) for n in names if not core(n).startswith(("ax_spa_lcdm", "ax_spa_w0wa"))})
N = len(hyp)


def chi2(n):
    return json.load(open(os.path.join(RES, f"cmp_{n}.json")))["minimum"]["chi2"]


def sig(p):
    return float(stats.norm.isf(p / 2))


CLAIMS = {"Spiral": ("ax_spa_spiraltwist{s}_nlfix", 2), "S8-L": ("spiralL{s}", 3)}
out = {"rule": "PREREG_V7_LOOK_ELSEWHERE.md", "N": N, "hypotheses": hyp, "claims": {}}
for claim, (pat, k) in CLAIMS.items():
    rows = {}
    for sn, s in (("Pantheon+", ""), ("DES-Dovekie", "_dovekie"), ("Union3", "_union3")):
        d = chi2(pat.format(s=s)) - chi2(f"ax_spa_lcdm_halofit{s}")
        pl = float(stats.chi2.sf(-d, k)) if d < 0 else 1.0
        pg = 1 - (1 - pl) ** N
        rows[sn] = {"delta_chi2": round(d, 2), "k": k, "p_local": pl, "sigma_local": round(sig(pl), 2),
                    "p_global": pg, "sigma_global": round(sig(pg), 2) if pg < 1 else 0.0}
    g = rows["Pantheon+"]["sigma_global"]
    rows["reading"] = ("SIGNIFICANT AFTER LOOK-ELSEWHERE" if g >= 3 else "SUGGESTIVE" if g >= 2 else
                       "NOT SIGNIFICANT AFTER LOOK-ELSEWHERE")
    out["claims"][claim] = rows
os.makedirs(os.path.join(HERE, "..", "results"), exist_ok=True)
json.dump(out, open(os.path.join(HERE, "..", "results", "v7_look_elsewhere.json"), "w"), indent=1)
print("N =", N)
for c, r in out["claims"].items():
    print(c, r["reading"], {k: (v["delta_chi2"], v["sigma_local"], v["sigma_global"]) for k, v in r.items() if k != "reading"})
