"""SN-SWAP (rule: field_tests/rules/PREREG_SN_SWAP.md). TOURNAMENT FULL likelihood with Union3 or DES-Dovekie SNe.
    SNSET=UNION3|DOVEKIE python sn_swap.py fit <LCDM|W0WA|PURE|FLAG1> | score      AI-assisted."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import tournament as T
from scipy.optimize import minimize
F = T.F
AEG = T.AEG; RULE = os.path.join(AEG, "field_tests", "rules", "PREREG_SN_SWAP.md"); SET = os.environ["SNSET"]
OUTD = os.path.join(HERE, "sn_swap_" + SET.lower()); os.makedirs(OUTD, exist_ok=True)
B0 = "/home/claude/cobaya_packages/data/sn_data"
import pandas as pd
if SET == "UNION3":
    U = np.genfromtxt(os.path.join(B0, "Union3", "lcparam_full.txt"), usecols=(1, 2, 4))
    zc, zh, mu = U[:, 0], U[:, 1], U[:, 2]
    cv = np.loadtxt(os.path.join(B0, "Union3", "mag_covmat.txt")); n = int(cv[0]); Ci = np.linalg.inv(cv[1:].reshape(n, n))
    zh = zc                                   # as Cobaya's union3.py (zhel = zcmb)
else:
    S = pd.read_csv(os.path.join(B0, "DES-Dovekie", "DES-Dovekie_HD.csv"))
    zc, zh, mu = S["zHD"].to_numpy(float), S["zHEL"].to_numpy(float), S["MU"].to_numpy(float)
    d = np.load(os.path.join(B0, "DES-Dovekie", "covtot_inv_000.npz")); n = int(d["nsn"][0])
    Ci = np.zeros((n, n)); Ci[np.triu_indices(n)] = d["cov"]; il = np.tril_indices(n, -1); Ci[il] = Ci.T[il]   # as Cobaya
C = None
F.SN = {"zHD": zc, "zHEL": zh}
F.MU_OBS = mu; F.SCi = Ci; F.ONE = np.ones(n)
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
    return ("TWIST HOLDS ON " + SET + "" if d <= -2 and d - dw <= 4 else "STRAINED" if d <= 0 else "FAILS ON " + SET)


def score():
    r = {m: json.load(open(os.path.join(OUTD, f"{m}.json"))) for m in VER}
    d = {m: r[m]["chi2"] - r["LCDM"]["chi2"] for m in VER}
    wa = r["W0WA"]["params"][4]; gate_ok = n == {"UNION3": 22, "DOVEKIE": 1820}[SET] and np.isfinite(r["LCDM"]["chi2"]) and wa < -0.40
    out = {"rule": "PREREG_SN_SWAP.md", "set": SET, "N_SN": n, "chi2": {m: r[m]["chi2"] for m in VER},
           "delta_vs_LCDM": {m: round(v, 3) for m, v in d.items()}, "W0WA_w0_wa": r["W0WA"]["params"][3:],
           "params": {m: r[m]["params"] for m in VER}, "gate": bool(gate_ok),
           "reading_PURE": band(d["PURE"], d["W0WA"]) if gate_ok else "NO VERDICT (gate failed)",
           "reading_FLAG1": band(d["FLAG1"], d["W0WA"]) if gate_ok else "NO VERDICT (gate failed)"}
    json.dump(out, open(os.path.join(AEG, "field_tests", "results", "sn_swap_" + SET.lower() + ".json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    a = sys.argv[1:]
    {"gate": gate, "score": score}.get(a[0], lambda: fit(a[1]))()
