"""SN-K816 (rule: field_tests/rules/PREREG_SN_K816.md). SNSET=UNION3|DOVEKIE python sn_k816.py. AI-assisted."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sn_swap as D
from scipy.optimize import minimize
T = D.T; RULE = os.path.join(D.AEG, "field_tests", "rules", "PREREG_SN_K816.md")
assert os.path.exists(RULE + ".sha256"), "rule not locked"
sets = T.bao_desi(); runs = []
f = lambda q: T.chi2("SPIRAL", list(q[:4]) + [0.8165], sets)
for i, x0 in enumerate(T.starts("FLAG1")):
    sf = os.path.join(D.OUTD, f"K816_s{i}.json")
    if os.path.exists(sf):
        r = json.load(open(sf)); runs.append((r["chi2"], r["params"])); continue
    r = minimize(f, x0, method="Nelder-Mead", options={"xatol": 1e-6, "fatol": 1e-3, "maxiter": 1500, "maxfev": 1500})
    res = (float(r.fun), [float(v) for v in r.x]); runs.append(res); json.dump({"chi2": res[0], "params": res[1]}, open(sf, "w"))
    print(D.SET, "K816 start", i, round(res[0], 3), flush=True)
best = min(runs); S = json.load(open(os.path.join(D.AEG, "field_tests", "results", f"sn_swap_{D.SET.lower()}.json")))
d = best[0] - S["chi2"]["LCDM"]; dw = S["delta_vs_LCDM"]["W0WA"]
out = {"rule": "PREREG_SN_K816.md", "set": D.SET, "chi2": best[0], "params": best[1], "delta_vs_LCDM": round(d, 3),
       "delta_vs_W0WA": round(d - dw, 3), "reading": D.band(d, dw)}
json.dump(out, open(os.path.join(D.AEG, "field_tests", "results", f"sn_k816_{D.SET.lower()}.json"), "w"), indent=1); print(out)
