"""MISSING-PIECE M1 (field_tests/rules/PREREG_MISSING_PIECE.md): DESI DR2 bin jackknife on V1's real-data anchor.
    python m1_jackknife.py run <worker> <n_workers>   -> missing_piece/m1/<label>.json
    python m1_jackknife.py score                      -> field_tests/results/missing_piece_m1.json
AI-assisted."""
import json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); AEG = os.path.abspath(os.path.join(HERE, "..", ".."))
RULE = os.path.join(AEG, "field_tests", "rules", "PREREG_MISSING_PIECE.md")
assert os.path.exists(RULE + ".sha256"), "rule not locked"
sys.path.insert(0, os.path.join(AEG, "field_tests", "selfcheck"))
import v1_mockcal as V                       # same likelihood, model, starts and optimiser as V1
from scipy.optimize import minimize

OUTD = os.path.join(HERE, "m1"); os.makedirs(OUTD, exist_ok=True)
ZB = [0.295, 0.51, 0.706, 0.934, 1.321, 1.484, 2.33]
LABELS = ["full"] + [f"drop_z{z}" for z in ZB] + ["drop_all_desi"]


def keep_mask(label):
    if label == "full":
        return np.ones(len(V.BZ), bool)
    if label == "drop_all_desi":
        return np.zeros(len(V.BZ), bool)
    z = float(label.split("_z")[1])
    return ~np.isclose(V.BZ, z)


def chi2(p, data, coupled, keep, Ci):
    h, wb, wc = p[:3]; beta = p[3] if coupled else None
    if coupled and not (0.0 <= beta <= 0.12):
        return 1e10
    try:
        bao, mu, cmb = V.model(h, wb, wc, beta)
    except Exception:
        return 1e10
    y = data["mu"] - mu
    rs = y - (V.ONE @ V.SCi @ y) / (V.ONE @ V.SCi @ V.ONE)
    out = float(rs @ V.SCi @ rs + np.sum(((cmb - data["cmb"]) / V.CMB_S) ** 2))
    if keep.any():
        rb = (data["bao"] - bao)[keep]; out += float(rb @ Ci @ rb)
    return out


def fitpair(data, keep):
    Ci = np.linalg.inv(V.BCOV[np.ix_(keep, keep)]) if keep.any() else None
    t = [V.TR["H0"] / 100, V.TR["omega_b"], V.TR["omega_cdm"]]
    starts = [t, [t[0] - 0.01, t[1] + 0.0002, t[2] + 0.002], [t[0] + 0.01, t[1] - 0.0002, t[2] - 0.002]]
    out = {}
    for coupled, betas in ((False, [None] * 3), (True, [0.01, 0.04, 0.08])):
        runs = []
        for s, b in zip(starts, betas):
            x0 = s + ([b] if coupled else [])
            r = minimize(lambda q: chi2(q, data, coupled, keep, Ci), x0, method="Nelder-Mead",
                         options={"xatol": 1e-6, "fatol": 1e-3, "maxiter": 1500, "maxfev": 1500, "initial_simplex": None})
            runs.append((float(r.fun), [float(v) for v in r.x]))
        out["FLAG1" if coupled else "LCDM"] = min(runs)
    out["delta"] = out["FLAG1"][0] - out["LCDM"][0]
    return out


def run(w, W):
    TB, TMU, TC = V.truth_vectors()
    data = {"bao": V.BV, "mu": V.SN["m_b_corr"].astype(float), "cmb": TC}
    for lab in LABELS[w::W]:
        f = os.path.join(OUTD, f"{lab}.json")
        if os.path.exists(f):
            continue
        r = fitpair(data, keep_mask(lab)); r["label"] = lab
        json.dump(r, open(f, "w"), indent=1); print(lab, round(r["delta"], 3), round(r["FLAG1"][1][3], 4), flush=True)


def score():
    R = {l: json.load(open(os.path.join(OUTD, f"{l}.json"))) for l in LABELS}
    full = R["full"]["delta"]; gate = abs(full - (-5.323424186139846)) <= 0.05
    drops = {l: R[l]["delta"] for l in LABELS if l.startswith("drop_z")}
    if not gate:
        reading = "NO VERDICT (gate failed)"
    elif max(drops.values()) > -2:
        reading = "ONE BIN CARRIES IT"
    elif all(d <= -4 for d in drops.values()):
        reading = "SPREAD"
    else:
        reading = "PARTLY CONCENTRATED"
    out = {"rule": "PREREG_MISSING_PIECE.md M1", "gate": {"full_delta": full, "v1_anchor": -5.3234, "pass": gate},
           "bins": {l: {"delta": round(d, 3), "share": round(d - full, 3), "beta": round(R[l]["FLAG1"][1][3], 4)}
                    for l, d in drops.items()},
           "drop_all_desi": {"delta": round(R["drop_all_desi"]["delta"], 3), "beta": round(R["drop_all_desi"]["FLAG1"][1][3], 4)},
           "reading": reading}
    json.dump(out, open(os.path.join(AEG, "field_tests", "results", "missing_piece_m1.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    run(int(sys.argv[2]), int(sys.argv[3])) if sys.argv[1] == "run" else score()
