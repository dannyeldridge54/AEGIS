"""KAPPA-ALPHA1 (rule: field_tests/rules/PREREG_KAPPA_ALPHA1.md, locked 12 Nov 2026 18:14 CT).
K816 = the TOURNAMENT SPIRAL code path with kappa fixed at sqrt(2/3) = 0.81650 (k = 1: beta only); FLAG1 starts.
    python kappa_alpha1.py fit <FULL|NOBAO|SDSS>     -> kappa_alpha1/K816_<C>.json (resumable per start)
    python kappa_alpha1.py score                      -> field_tests/results/kappa_alpha1.json
AI-assisted."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import tournament as T
from scipy.optimize import minimize
KAP = 0.81650
RULE = os.path.join(T.AEG, "field_tests", "rules", "PREREG_KAPPA_ALPHA1.md")
OUTD = os.path.join(HERE, "kappa_alpha1"); os.makedirs(OUTD, exist_ok=True)
SETS = {"FULL": T.bao_desi, "NOBAO": lambda: [], "SDSS": T.bao_sdss}


def full(p):
    return list(p) + [KAP]


def fit(config):
    assert os.path.exists(RULE + ".sha256"), "rule not locked"
    f = os.path.join(OUTD, f"K816_{config}.json")
    if os.path.exists(f):
        return
    sets = SETS[config](); runs = []
    for i, x0 in enumerate(T.starts("FLAG1")):
        sf = os.path.join(OUTD, f"K816_{config}_s{i}.json")
        if os.path.exists(sf):
            r = json.load(open(sf)); runs.append((r["chi2"], r["params"])); continue
        r = minimize(lambda q: T.chi2("SPIRAL", full(q), sets), x0, method="Nelder-Mead",
                     options={"xatol": 1e-6, "fatol": 1e-3, "maxiter": 1500, "maxfev": 1500})
        res = (float(r.fun), [float(v) for v in r.x]); runs.append(res)
        json.dump({"chi2": res[0], "params": res[1]}, open(sf, "w")); print("K816", config, "start", i, round(res[0], 3), flush=True)
    best = min(runs)
    out = {"config": config, "chi2": best[0], "params": best[1], "kappa": KAP, "starts": [r[0] for r in runs]}
    if config == "NOBAO":
        c = T.model("SPIRAL", full(best[1]))
        out["pred_DESI"] = T.bao_chi2(c, T.bao_desi()); out["pred_SDSS"] = T.bao_chi2(c, T.bao_sdss()); c.struct_cleanup(); c.empty()
    json.dump(out, open(f, "w"), indent=1); print("K816", config, round(best[0], 3), flush=True)


def score():
    K = {c: json.load(open(os.path.join(OUTD, f"K816_{c}.json"))) for c in SETS}
    L = {c: json.load(open(os.path.join(T.OUTD, f"LCDM_{c}.json"))) for c in SETS}
    F = {c: json.load(open(os.path.join(T.OUTD, f"FLAG1_{c}.json"))) for c in SETS}
    g = T.chi2("LCDM", L["FULL"]["params"], T.bao_desi())
    gate = abs(g - L["FULL"]["chi2"]) <= 0.05
    d = lambda R: {"dAIC_FULL": round(R["FULL"]["chi2"] - L["FULL"]["chi2"] + (2 if R is not L else 0), 3),
                   "dP_DESI": round(R["NOBAO"]["pred_DESI"] - L["NOBAO"]["pred_DESI"], 3),
                   "dP_SDSS": round(R["NOBAO"]["pred_SDSS"] - L["NOBAO"]["pred_SDSS"], 3),
                   "d_SDSS": round(R["SDSS"]["chi2"] - L["SDSS"]["chi2"], 3)}
    k = d(K); f1 = d(F)
    pred = k["dP_DESI"] <= 0 and k["dP_SDSS"] <= 0 and k["d_SDSS"] <= 1
    reading = ("NO VERDICT (gate failed)" if not gate else
               ("PREFERRED" if pred and k["dAIC_FULL"] < 0 else "PREDICTS" if pred else "NOT PREDICTIVE"))
    out = {"rule": "PREREG_KAPPA_ALPHA1.md", "gate": {"LCDM_FULL_recomputed": g, "stored": L["FULL"]["chi2"], "pass": gate},
           "K816": k, "FLAG1": f1, "K_VS_FLAG1": {x: round(k[x] - f1[x], 3) for x in k},
           "params": {c: [round(v, 5) for v in K[c]["params"]] for c in SETS}, "reading": reading}
    json.dump(out, open(os.path.join(T.AEG, "field_tests", "results", "kappa_alpha1.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    a = sys.argv[1:]
    fit(a[1]) if a[0] == "fit" else score()
