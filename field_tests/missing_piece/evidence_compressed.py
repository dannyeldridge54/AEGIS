"""EVIDENCE-COMPRESSED (rule: field_tests/rules/PREREG_EVIDENCE_COMPRESSED.md). AI-assisted.
    python evidence_compressed.py run LCDM|PURE|K816|W0WA  |  score"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import tournament as T
AEG = T.AEG; RULE = os.path.join(AEG, "field_tests", "rules", "PREREG_EVIDENCE_COMPRESSED.md")
OUTD = os.path.join(HERE, "evidence"); os.makedirs(OUTD, exist_ok=True)
SH = [(0.60, 0.75), (0.0215, 0.0235), (0.105, 0.130)]
EXTRA = {"LCDM": [], "PURE": [], "K816": [(0.0, 0.10)], "W0WA": [(-1.5, -0.5), (-2.0, 1.0)]}
SETS = None


def full(m, q):
    if m == "LCDM":
        return "LCDM", list(q)
    if m == "PURE":
        return "SPIRAL", list(q) + [0.0, 0.8165]
    if m == "K816":
        return "SPIRAL", list(q) + [0.8165]
    return "W0WA", list(q)


def run(m):
    global SETS
    import dynesty
    assert os.path.exists(RULE + ".sha256"), "rule not locked"
    SETS = T.bao_desi(); B = SH + EXTRA[m]; lo = np.array([b[0] for b in B]); hi = np.array([b[1] for b in B])
    def pt(u):
        return lo + u * (hi - lo)
    def ll(q):
        if m == "W0WA" and q[3] + q[4] >= 0:
            return -1e100
        v, p = full(m, q); x = T.chi2(v, p, SETS)
        return -0.5 * x if x < 1e9 else -1e100
    s = dynesty.NestedSampler(ll, pt, len(B), nlive=300, sample="rwalk", rstate=np.random.default_rng(1))
    s.run_nested(dlogz=0.1, print_progress=False, checkpoint_file=os.path.join(OUTD, f"{m}.save"))
    r = s.results
    out = {"model": m, "logz": float(r.logz[-1]), "logzerr": float(r.logzerr[-1]), "ncall": int(sum(r.ncall)),
           "max_logl": float(np.max(r.logl))}
    json.dump(out, open(os.path.join(OUTD, f"{m}.json"), "w"), indent=1); print(out, flush=True)


def score():
    z = {m: json.load(open(os.path.join(OUTD, f"{m}.json"))) for m in EXTRA}
    lb = {m: round(z[m]["logz"] - z["LCDM"]["logz"], 3) for m in EXTRA}
    pk = round(z["PURE"]["logz"] - z["K816"]["logz"], 3)
    if lb["PURE"] >= 1 and pk >= 0:
        r = "PURE PREFERRED BY EVIDENCE"
    elif lb["K816"] >= 1 and pk < 0:
        r = "K816 PREFERRED BY EVIDENCE"
    elif lb["PURE"] < 1 and lb["K816"] < 1:
        r = "NO EVIDENCE FOR THE TWIST"
    else:
        r = "MIXED (see numbers)"
    out = {"rule": "PREREG_EVIDENCE_COMPRESSED.md", "lnB_vs_LCDM": lb, "lnB_PURE_vs_K816": pk,
           "errors": {m: z[m]["logzerr"] for m in EXTRA}, "reading": r}
    json.dump(out, open(os.path.join(AEG, "field_tests", "results", "evidence_compressed.json"), "w"), indent=1); print(out)


if __name__ == "__main__":
    a = sys.argv[1:]
    run(a[1]) if a[0] == "run" else score()
