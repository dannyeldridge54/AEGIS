"""EXPLORATORY (not a locked rule): V7's look-elsewhere statistic applied to the flagship FLAG-1.
PREREG_V7_LOOK_ELSEWHERE.md (locked 8 Nov) evaluated only the Spiral and S8-L; FLAG-1 came later. This uses V7's
statistic unchanged (Wilks local p, Sidak global, two-sided Gaussian sigma) with FLAG-1's stored Delta chi2 vs
LCDM+S8 (field_tests/results/flagship_score.json), k = 1 (beta free; kappa fixed at 1).
N is counted with V7's own counting rule on today's inventory, and also with a broadened glob (every cmp_*.json
late/early-field hypothesis, whatever its prefix), which is the more conservative of the two.
    python v7_flag1_exploratory.py  -> ../results/v7_flag1_exploratory.json"""
import glob, json, os, re, sys
from scipy import stats
HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.environ.get("TWIST_RESULTS", os.path.join(HERE, "..", "..", "cmb-fit", "results"))
sys.argv = [sys.argv[0]]
src = open(os.path.join(HERE, "v7_look_elsewhere.py")).read()
core_src = src[src.index("DATA_SUF"):src.index("names =")]
ns = {"re": re}; exec(core_src, ns); core = ns["core"]
REF = ("ax_spa_lcdm", "ax_spa_w0wa", "lcdm", "w0wa")

def count(paths):
    names = [os.path.basename(p)[4:-5] for p in paths]
    return sorted({core(n) for n in names if not core(n).startswith(REF)})

v7_glob = glob.glob(os.path.join(RES, "cmp_ax_spa_*.json")) + glob.glob(os.path.join(RES, "cmp_spiralL*.json"))
hyp_v7 = count(v7_glob)
hyp_all = count(glob.glob(os.path.join(RES, "cmp_*.json")))
sig = lambda p: float(stats.norm.isf(p / 2))
d = json.load(open(os.path.join(HERE, "..", "results", "flagship_score.json")))["vs_LCDM_S8"]
out = {"status": "EXPLORATORY (V7 statistic applied to FLAG-1; not a locked rule)", "k": 1,
       "N_v7_lock": 64, "N_v7_rule_today": len(hyp_v7), "N_broad_today": len(hyp_all),
       "hypotheses_broad": hyp_all, "rows": {}}
for sn in ("P+", "Dovekie", "Union3"):
    pl = float(stats.chi2.sf(-d[sn], 1))
    row = {"delta_chi2": d[sn], "p_local": pl, "sigma_local": round(sig(pl), 2)}
    for lab, N in (("N64", 64), ("N_v7_rule_today", len(hyp_v7)), ("N_broad_today", len(hyp_all))):
        pg = 1 - (1 - pl) ** N
        row["sigma_global_" + lab] = round(sig(pg), 2) if pg < 1 else 0.0
    out["rows"][sn] = row
json.dump(out, open(os.path.join(HERE, "..", "results", "v7_flag1_exploratory.json"), "w"), indent=1)
print({k: out[k] for k in ("N_v7_lock", "N_v7_rule_today", "N_broad_today")})
for k, v in out["rows"].items(): print(k, v)
