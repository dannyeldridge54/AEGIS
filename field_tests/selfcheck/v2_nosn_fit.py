"""SELFCHECK V2 (field_tests/rules/PREREG_SELFCHECK.md): FLAG-1 and LCDM refit with every supernova likelihood
removed; otherwise exactly the stored s8y6 fits (same CMB, DESI DR2 BAO, DES Y6 S8 term, priors, build), best of 4,
each starting from its own stored Pantheon+ s8y6 minimum.
    python v2_nosn_fit.py FLAG1 | LCDM     (PC, WSL env "aegis")  -> cmb-fit/results/cmp_<name>.json
    python v2_nosn_fit.py score                                   -> field_tests/results/selfcheck_v2.json"""
import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); AEG = os.path.abspath(os.path.join(HERE, "..", ".."))
RULE = os.path.join(AEG, "field_tests", "rules", "PREREG_SELFCHECK.md")
sys.path.insert(0, os.path.join(AEG, "cmb-fit", "axiclass")); sys.path.insert(0, os.path.join(AEG, "field_tests", "S8_WL", "joint"))
RUNS = {"FLAG1": ("ax_spa_spiraltwist_kappa1_nlfix", "ax_spa_spiraltwist_kappa1_nlfix_nosn_s8y6"),
        "LCDM": ("ax_spa_lcdm_halofit", "ax_spa_lcdm_halofit_nosn_s8y6")}


def fit(which):
    assert os.path.exists(RULE + ".sha256"), "rule not locked"
    import early_late_spa as E
    import s8_joint_fit as J
    from cobaya.run import run as crun
    base, name = RUNS[which]
    t = time.time()
    E._maybe_coupled(base)
    info = E.make(base)
    info["likelihood"] = {k: v for k, v in info["likelihood"].items() if not k.startswith("sn.")}
    J.add_s8(info)
    m = json.load(open(f"{E.OUT}/cmp_{base}_s8y6.json"))["minimum"]
    for k, p in info["params"].items():
        if isinstance(p, dict) and "ref" in p and k in m:
            p["ref"]["loc"] = float(m[k])
    info["sampler"]["minimize"]["best_of"] = 4
    info["output"] = f"{E.OUT}/chains/cmp_{name}"
    crun(info)
    E.save(name, time.time() - t)


def score():
    res = os.environ.get("TWIST_RESULTS", os.path.join(AEG, "cmb-fit", "results"))
    f = {w: json.load(open(os.path.join(res, f"cmp_{n}.json"))) for w, (_, n) in RUNS.items()}
    d = f["FLAG1"]["minimum"]["chi2"] - f["LCDM"]["minimum"]["chi2"]
    reading = ("PREFERENCE SURVIVES WITHOUT SNe" if d <= -4 else "SN-DRIVEN" if d > -2 else "WEAK")
    keep = ("chi2", "H0", "sigma8", "Omega_m", "scf_coupling_beta")
    out = {"rule": "PREREG_SELFCHECK.md V2", "delta_noSN": round(d, 3), "reading": reading,
           "fits": {w: {k: v["minimum"].get(k) for k in keep} | {"chi2_parts": {k: v2 for k, v2 in v["minimum"].items() if k.startswith("chi2__")}}
                    for w, v in f.items()}}
    json.dump(out, open(os.path.join(AEG, "field_tests", "results", "selfcheck_v2.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    score() if sys.argv[1] == "score" else fit(sys.argv[1])
