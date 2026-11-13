"""DESY5-SWAP (rule: field_tests/rules/PREREG_DESY5_SWAP.md). TOURNAMENT FULL likelihood with DES Y5 SNe. AI-assisted.
    python desy5_swap.py gate | fit <LCDM|W0WA|PURE|FLAG1> | score"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import tournament as T
from scipy.optimize import minimize
F = T.F
AEG = T.AEG; RULE = os.path.join(AEG, "field_tests", "rules", "PREREG_DESY5_SWAP.md")
OUTD = os.path.join(HERE, "desy5_swap"); os.makedirs(OUTD, exist_ok=True)
D = "/home/claude/cobaya_packages/data/sn_data/DESY5"
import pandas as pd
SN = pd.read_csv(os.path.join(D, "DES-SN5YR_HD.csv"))
cov = np.loadtxt(os.path.join(D, "covsys_000.txt"))
n = int(cov[0]); C = cov[1:].reshape(n, n) + np.diag(SN["MUERR_FINAL"].to_numpy(float) ** 2)
F.SN = {"zHD": SN["zHD"].to_numpy(float), "zHEL": SN["zHEL"].to_numpy(float)}
F.MU_OBS = SN["MU"].to_numpy(float); F.SCi = np.linalg.inv(C); F.ONE = np.ones(n)
VER = {"LCDM": "LCDM", "W0WA": "W0WA", "PURE": "SPIRAL", "FLAG1": "FLAG1"}
full = {"PURE": lambda q: list(q[:3]) + [0.0, 0.8165]}


def chi2(m, q, sets):
    return T.chi2(VER[m], full.get(m, list)(q), sets)


def gate():
    assert os.path.exists(RULE + ".sha256"), "rule not locked"
    print("N_SN", n, "LCDM chi2 at stored start", chi2("LCDM", T.starts("LCDM")[0], T.bao_desi()), flush=True)


def fit(m):
    assert os.path.exists(RULE + ".sha256"), "rule not locked"
    f = os.path.join(OUTD, f"{m}.json")
    if os.path.exists(f):
        return
    sets = T.bao_desi(); runs = []
    for i, x0 in enumerate(T.starts("LCDM" if m == "PURE" else VER[m])):
        sf = os.path.join(OUTD, f"{m}_s{i}.json")
        if os.path.exists(sf):
            r = json.load(open(sf)); runs.append((r["chi2"], r["params"])); continue
        r = minimize(lambda q: chi2(m, q, sets), x0, method="Nelder-Mead",
                     options={"xatol": 1e-6, "fatol": 1e-3, "maxiter": 1500, "maxfev": 1500})
        res = (float(r.fun), [float(v) for v in r.x]); runs.append(res)
        json.dump({"chi2": res[0], "params": res[1]}, open(sf, "w")); print(m, "start", i, round(res[0], 3), flush=True)
    best = min(runs)
    json.dump({"chi2": best[0], "params": best[1], "starts": [r[0] for r in runs]}, open(f, "w"), indent=1)
    print(m, "best", round(best[0], 3), best[1], flush=True)


def band(d, dw):
    return ("TWIST HOLDS ON DES Y5" if d <= -2 and d - dw <= 4 else "STRAINED" if d <= 0 else "FAILS ON DES Y5")


def score():
    r = {m: json.load(open(os.path.join(OUTD, f"{m}.json"))) for m in VER}
    d = {m: r[m]["chi2"] - r["LCDM"]["chi2"] for m in VER}
    wa = r["W0WA"]["params"][4]; gate_ok = n == 1829 and np.isfinite(r["LCDM"]["chi2"]) and wa < -0.40
    out = {"rule": "PREREG_DESY5_SWAP.md", "N_SN": n, "chi2": {m: r[m]["chi2"] for m in VER},
           "delta_vs_LCDM": {m: round(v, 3) for m, v in d.items()}, "W0WA_w0_wa": r["W0WA"]["params"][3:],
           "params": {m: r[m]["params"] for m in VER}, "gate": bool(gate_ok),
           "reading_PURE": band(d["PURE"], d["W0WA"]) if gate_ok else "NO VERDICT (gate failed)",
           "reading_FLAG1": band(d["FLAG1"], d["W0WA"]) if gate_ok else "NO VERDICT (gate failed)"}
    json.dump(out, open(os.path.join(AEG, "field_tests", "results", "desy5_swap.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    a = sys.argv[1:]
    {"gate": gate, "score": score}.get(a[0], lambda: fit(a[1]))()
