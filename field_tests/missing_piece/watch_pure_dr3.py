"""WATCH-PURE-DR3 (rule: field_tests/rules/PREREG_WATCH_PURE_DR3.md, locked 12 Nov 2026 20:59 CT).
Both models frozen at their 12 Nov 2026 FULL best fits (no refit); scores new BAO data.
    python watch_pure_dr3.py dryrun                         pipeline check on DESI DR2 (NOT the test; DR2 was in the fit)
    python watch_pure_dr3.py score <values.dat> <cov.txt> [label]   the test, on a new release (same file format as DR2:
                                                            columns z, value, quantity; quantity in DM_over_rs|DH_over_rs|DV_over_rs)
AI-assisted."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import tournament as T
RULE = os.path.join(T.AEG, "field_tests", "rules", "PREREG_WATCH_PURE_DR3.md")
PRED = json.load(open(os.path.join(T.AEG, "field_tests", "results", "pure_twist_predictions.json")))
KAP = 0.81650


def models():
    P = PRED["pure_twist_params"]; L = PRED["lcdm_params"]
    return T.model("SPIRAL", list(P[:3]) + [0.0, KAP]), T.model("LCDM", L)


def chi2s(sets):
    cP, cL = models()
    xP, xL = T.bao_chi2(cP, sets), T.bao_chi2(cL, sets)
    sign = {}
    for (lab, zs, vals, qs, cov), pP, pL in zip(sets, T.bao_pred(cP, sets), T.bao_pred(cL, sets)):
        for z, v, q, a, b in zip(zs, vals, qs, pP, pL):
            if q == "DH_over_rs" and 0.5 <= z <= 1.3:
                sign[f"{z:.3f}"] = {"measured_below_LCDM": bool(v < b), "PURE_predicts_below": bool(a < b)}
    return xP, xL, sign


def run(sets, label, is_test):
    assert os.path.exists(RULE + ".sha256"), "rule not locked"
    xP, xL, sign = chi2s(sets); d = xP - xL
    reading = ("SUPPORTED" if d <= -2 else "DISFAVOURED" if d >= 2 else "UNDECIDED") if is_test else "DRY RUN (not a test)"
    out = {"rule": "PREREG_WATCH_PURE_DR3.md", "data": label, "chi2_PURE": xP, "chi2_LCDM": xL, "dchi2": d,
           "D_SIGN": sign, "reading": reading}
    print(json.dumps(out, indent=1))
    if is_test:
        json.dump(out, open(os.path.join(T.AEG, "field_tests", "results", f"watch_pure_{label}.json"), "w"), indent=1)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "dryrun":
        run(T.bao_desi(), "DR2", False)
    else:
        m = np.loadtxt(a[1], dtype=str); cov = np.loadtxt(a[2])
        run([("NEW", m[:, 0].astype(float), m[:, 1].astype(float), m[:, 2], cov)], a[3] if len(a) > 3 else "DR3", True)
