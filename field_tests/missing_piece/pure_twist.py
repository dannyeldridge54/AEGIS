"""PURE-TWIST (rule: field_tests/rules/PREREG_PURE_TWIST.md, locked 12 Nov 2026 20:37 CT).
K816B0 = the TOURNAMENT SPIRAL code path with kappa = sqrt(2/3) = 0.81650 and beta = 0 fixed (k = 0); LCDM starts.
    python pure_twist.py fit <FULL|NOBAO|SDSS>    -> pure_twist/K816B0_<C>.json (resumable per start)
    python pure_twist.py score                     -> field_tests/results/pure_twist.json
AI-assisted."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import tournament as T
from scipy.optimize import minimize
KAP = 0.81650
RULE = os.path.join(T.AEG, "field_tests", "rules", "PREREG_PURE_TWIST.md")
OUTD = os.path.join(HERE, "pure_twist"); os.makedirs(OUTD, exist_ok=True)
SETS = {"FULL": T.bao_desi, "NOBAO": lambda: [], "SDSS": T.bao_sdss}
full = lambda p: list(p[:3]) + [0.0, KAP]


def fit(config):
    assert os.path.exists(RULE + ".sha256"), "rule not locked"
    f = os.path.join(OUTD, f"K816B0_{config}.json")
    if os.path.exists(f):
        return
    sets = SETS[config](); runs = []
    for i, x0 in enumerate(T.starts("LCDM")):
        sf = os.path.join(OUTD, f"K816B0_{config}_s{i}.json")
        if os.path.exists(sf):
            r = json.load(open(sf)); runs.append((r["chi2"], r["params"])); continue
        r = minimize(lambda q: T.chi2("SPIRAL", full(q), sets), x0, method="Nelder-Mead",
                     options={"xatol": 1e-6, "fatol": 1e-3, "maxiter": 1500, "maxfev": 1500})
        res = (float(r.fun), [float(v) for v in r.x]); runs.append(res)
        json.dump({"chi2": res[0], "params": res[1]}, open(sf, "w")); print("K816B0", config, "start", i, round(res[0], 3), flush=True)
    best = min(runs)
    out = {"config": config, "chi2": best[0], "params": best[1], "kappa": KAP, "beta": 0.0, "starts": [r[0] for r in runs]}
    if config == "NOBAO":
        c = T.model("SPIRAL", full(best[1]))
        out["pred_DESI"] = T.bao_chi2(c, T.bao_desi()); out["pred_SDSS"] = T.bao_chi2(c, T.bao_sdss()); c.struct_cleanup(); c.empty()
    json.dump(out, open(f, "w"), indent=1); print("K816B0", config, round(best[0], 3), flush=True)


def score():
    load = lambda d, n: {c: json.load(open(os.path.join(d, f"{n}_{c}.json"))) for c in SETS}
    P = load(OUTD, "K816B0"); L = load(T.OUTD, "LCDM"); S0 = load(T.OUTD, "SPIRAL0")
    K = load(os.path.join(HERE, "kappa_alpha1"), "K816")
    g = T.chi2("LCDM", L["FULL"]["params"], T.bao_desi()); gate = abs(g - L["FULL"]["chi2"]) <= 0.05
    d = lambda R, Q: {"dchi2_FULL": round(R["FULL"]["chi2"] - Q["FULL"]["chi2"], 3),
                      "dP_DESI": round(R["NOBAO"]["pred_DESI"] - Q["NOBAO"]["pred_DESI"], 3),
                      "dP_SDSS": round(R["NOBAO"]["pred_SDSS"] - Q["NOBAO"]["pred_SDSS"], 3),
                      "d_SDSS": round(R["SDSS"]["chi2"] - Q["SDSS"]["chi2"], 3)}
    vL = d(P, L)
    pred = vL["dP_DESI"] <= 0 and vL["dP_SDSS"] <= 0 and vL["d_SDSS"] <= 1
    reading = ("NO VERDICT (gate failed)" if not gate else
               ("PREFERRED" if pred and vL["dchi2_FULL"] < 0 else "PREDICTS" if pred else "NOT PREDICTIVE"))
    out = {"rule": "PREREG_PURE_TWIST.md", "gate": {"LCDM_FULL_recomputed": g, "stored": L["FULL"]["chi2"], "pass": gate},
           "vs_LCDM": vL, "vs_SPIRAL0": d(P, S0), "vs_K816": d(P, K),
           "params": {c: [round(v, 5) for v in P[c]["params"]] for c in SETS}, "reading": reading}
    json.dump(out, open(os.path.join(T.AEG, "field_tests", "results", "pure_twist.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    a = sys.argv[1:]
    fit(a[1]) if a[0] == "fit" else score()
