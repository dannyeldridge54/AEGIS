"""TAIL-F (rule: field_tests/rules/PREREG_TAIL_F.md). python tail_f.py run FIXED|RANGE | score. AI-assisted."""
import json, math, os, sys
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import tournament as T
AEG = T.AEG; RULE = os.path.join(AEG, "field_tests", "rules", "PREREG_TAIL_F.md")
TAB = json.load(open(os.path.join(AEG, "field_tests", "results", "tail_curve_table.json")))
LF = np.log([r["f"] for r in TAB]); W0 = np.array([r["w0"] for r in TAB]); WA = np.array([r["wa"] for r in TAB])
OUTD = os.path.join(HERE, "tail_f"); os.makedirs(OUTD, exist_ok=True)
LCDM, W0WA = 1401.176, 1394.971


def w(f):
    return float(np.interp(math.log(f), LF, W0)), float(np.interp(math.log(f), LF, WA))


def run(m):
    assert os.path.exists(RULE + ".sha256"), "rule not locked"
    sets = T.bao_desi(); runs = []
    for i, x0 in enumerate(T.starts("LCDM")):
        if m == "FIXED":
            fun = lambda q: T.chi2("W0WA", list(q) + list(w(1.3e-3)), sets); x = x0
        else:
            def fun(q):
                f = math.exp(q[3])
                return 1e10 if not 1e-4 <= f <= 2.5e-3 else T.chi2("W0WA", list(q[:3]) + list(w(f)), sets)
            x = x0 + [math.log(1.3e-3)]
        r = minimize(fun, x, method="Nelder-Mead", options={"xatol": 1e-6, "fatol": 1e-3, "maxiter": 1500, "maxfev": 1500})
        runs.append((float(r.fun), [float(v) for v in r.x])); print(m, "start", i, round(r.fun, 3), flush=True)
    best = min(runs); out = {"fit": m, "chi2": best[0], "params": best[1], "starts": [r[0] for r in runs]}
    if m == "RANGE":
        out["best_f"] = math.exp(best[1][3]); out["w0wa_at_best"] = w(out["best_f"])
    json.dump(out, open(os.path.join(OUTD, f"{m}.json"), "w"), indent=1); print(out, flush=True)


def score():
    a = json.load(open(os.path.join(OUTD, "FIXED.json"))); b = json.load(open(os.path.join(OUTD, "RANGE.json")))
    d = a["chi2"] - LCDM
    ra = "FULL TAIL HOLDS" if d <= -2 else ("FULL TAIL DISFAVOURED" if d >= 2 else "FULL TAIL NEUTRAL")
    rb = "HEAT SHARE CONSISTENT" if b["best_f"] >= 4e-4 else "DATA WANT LESS HEAT THAN COMPUTED"
    out = {"rule": "PREREG_TAIL_F.md", "FIXED": {"dchi2_vs_LCDM": round(d, 3), "w0wa": w(1.3e-3), "reading": ra},
           "RANGE": {"dchi2_vs_LCDM": round(b["chi2"] - LCDM, 3), "best_f_percent": round(b["best_f"] * 100, 4),
                     "w0wa": b["w0wa_at_best"], "minus_w0wa_chi2": round(b["chi2"] - W0WA, 3), "reading": rb}}
    json.dump(out, open(os.path.join(AEG, "field_tests", "results", "tail_f.json"), "w"), indent=1); print(json.dumps(out, indent=1))


if __name__ == "__main__":
    a = sys.argv[1:]; run(a[1]) if a[0] == "run" else score()
