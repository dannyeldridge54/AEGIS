"""NS-SPA (rule: field_tests/rules/PREREG_NS_SPA.md). PC, WSL env "aegis". AI-assisted.
    python ns_spa_fit.py gate | fit PURE_FREE|PURE_FIXED|LCDM_FIXED | score"""
import json, math, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); AEG = os.path.abspath(os.path.join(HERE, "..", ".."))
RULE = os.path.join(AEG, "field_tests", "rules", "PREREG_NS_SPA.md")
sys.path.insert(0, os.path.join(AEG, "cmb-fit", "axiclass")); sys.path.insert(0, os.path.join(AEG, "field_tests", "S8_WL", "joint"))
BASE = {"PURE": "ax_spa_spiraltwist_kappa0.8165_beta0_nlfix", "LCDM": "ax_spa_lcdm_halofit"}
START = {"PURE": "ax_spa_lcdm_halofit_s8y6", "LCDM": "ax_spa_lcdm_halofit_s8y6"}   # PURE has no stored SPA fit
NS_FIX = 0.964


def setup(model, fixed):
    assert os.path.exists(RULE + ".sha256"), "rule not locked"
    import early_late_spa as E, s8_joint_fit as J
    E._maybe_coupled(BASE[model]); info = E.make(BASE[model]); J.add_s8(info)
    if fixed:
        info["params"]["n_s"] = NS_FIX
    m = json.load(open(f"{E.OUT}/cmp_{START[model]}.json"))["minimum"]
    return E, info, m


def name(job):
    return f"ns_spa_{job.lower()}"


def gate():
    from cobaya.model import get_model
    E, info, m = setup("LCDM", False)
    info.pop("sampler", None); info.pop("output", None)
    model = get_model(info); names = list(model.parameterization.sampled_params())
    point = {p: float(m[p]) for p in names if p in m}
    missing = [p for p in names if p not in m]
    point.update(dict(zip(missing, map(float, [model.prior.reference()[names.index(p)] for p in missing]))))
    x2 = sum(-2 * float(v) for v in model.loglikes(point, as_dict=True)[0].values())
    ok = abs(x2 - m["chi2"]) <= 0.5
    print({"recomputed": x2, "stored": m["chi2"], "pass": ok}, flush=True)
    json.dump({"recomputed": x2, "stored": m["chi2"], "pass": ok}, open(os.path.join(E.OUT, "ns_spa_gate.json"), "w"))
    sys.exit(0 if ok else 1)


def fit(job):
    from cobaya.run import run as crun
    model, fixed = job.split("_")[0], job.endswith("FIXED")
    E, info, m = setup(model, fixed)
    for k, p in info["params"].items():
        if isinstance(p, dict) and "ref" in p and k in m:
            p["ref"]["loc"] = float(m[k])
    info["sampler"]["minimize"]["best_of"] = 4
    info["output"] = f"{E.OUT}/chains/cmp_{name(job)}"
    t = time.time(); crun(info); E.save(name(job), time.time() - t)


def score():
    res = os.environ.get("TWIST_RESULTS", os.path.join(AEG, "cmb-fit", "results"))
    ld = lambda n: json.load(open(os.path.join(res, f"cmp_{n}.json")))["minimum"]
    pf, px, lx, lf = ld(name("PURE_FREE")), ld(name("PURE_FIXED")), ld(name("LCDM_FIXED")), ld("ax_spa_lcdm_halofit_s8y6")
    C = px["chi2"] - pf["chi2"]
    reading = "CONSISTENT" if C <= 4 else "TENSION" if C <= 9 else "INCONSISTENT"
    out = {"rule": "PREREG_NS_SPA.md", "cost_PURE": round(C, 3), "cost_LCDM": round(lx["chi2"] - lf["chi2"], 3),
           "n_s_PURE_free": pf.get("n_s"), "n_s_LCDM_free": lf.get("n_s"), "PURE_free_minus_LCDM_free": round(pf["chi2"] - lf["chi2"], 3),
           "reading": reading, "chi2": {"PURE_free": pf["chi2"], "PURE_fixed": px["chi2"], "LCDM_free": lf["chi2"], "LCDM_fixed": lx["chi2"]}}
    json.dump(out, open(os.path.join(AEG, "field_tests", "results", "ns_spa.json"), "w"), indent=1); print(json.dumps(out, indent=1))


if __name__ == "__main__":
    a = sys.argv[1:]
    {"gate": gate, "score": score}.get(a[0], lambda: fit(a[1]))()
