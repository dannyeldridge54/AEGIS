"""V6 (field_tests/rules/PREREG_V6_PR4.md): DATA-GEN fit C with Planck PR4 CamSpec high-l in place of PR3 plik-lite.
    python v6_pr4_fit.py gate FLAG1|LCDM    (setup evaluated at the stored fit-C minimum; all terms finite)
    python v6_pr4_fit.py fit FLAG1|LCDM     -> cmb-fit/results/cmp_<name>.json        (PC, WSL env "aegis")
    python v6_pr4_fit.py score              -> field_tests/results/selfcheck_v6.json
AI-assisted."""
import json, math, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); AEG = os.path.abspath(os.path.join(HERE, "..", ".."))
RULE = os.path.join(AEG, "field_tests", "rules", "PREREG_V6_PR4.md")
sys.path.insert(0, os.path.join(AEG, "cmb-fit", "axiclass")); sys.path.insert(0, os.path.join(AEG, "field_tests", "S8_WL", "joint"))
BASE = {"FLAG1": "ax_spa_spiraltwist_kappa1_nlfix", "LCDM": "ax_spa_lcdm_halofit"}
OLD, NEW = "planck_2018_highl_plik.TTTEEE_lite_native", "planck_NPIPE_highl_CamSpec.TTTEEE"


def engine(which):
    return BASE[which].replace("_nlfix", "") + "_planckfull" + ("_nlfix" if which == "FLAG1" else "")


def name(which):
    return f"{BASE[which]}_pr4_s8y6"


def setup(which):
    assert os.path.exists(RULE + ".sha256"), "rule not locked"
    import early_late_spa as E
    import s8_joint_fit as J
    E._maybe_coupled(engine(which))
    info = E.make(engine(which))
    assert OLD in info["likelihood"], sorted(info["likelihood"])
    info["likelihood"].pop(OLD); info["likelihood"][NEW] = None
    J.add_s8(info)
    m = json.load(open(f"{E.OUT}/cmp_{BASE[which]}_cmbplanck_s8y6.json"))["minimum"]
    return E, info, m


def gate(which):
    from cobaya.model import get_model
    E, info, m = setup(which)
    info.pop("sampler", None); info.pop("output", None)
    model = get_model(info)
    names = list(model.parameterization.sampled_params())
    point = dict(zip(names, map(float, model.prior.reference())))   # PR4 nuisance parameters: their own reference values
    point.update({p: float(m[p]) for p in names if p in m})          # everything else: the stored fit-C minimum
    parts = {k: -2 * float(v) for k, v in model.loglikes(point, as_dict=True)[0].items()}
    ok = all(math.isfinite(v) for v in parts.values())
    out = {"which": which, "parts": parts, "pass": ok}
    print(out, flush=True)
    json.dump(out, open(os.path.join(E.OUT, f"v6_gate_{which}.json"), "w"), indent=1)
    if not ok:
        sys.exit(1)


def fit(which):
    from cobaya.run import run as crun
    E, info, m = setup(which)
    for k, p in info["params"].items():
        if isinstance(p, dict) and "ref" in p and k in m:
            p["ref"]["loc"] = float(m[k])
    info["sampler"]["minimize"]["best_of"] = 4
    info["output"] = f"{E.OUT}/chains/cmp_{name(which)}"
    t = time.time(); crun(info); E.save(name(which), time.time() - t)


def score():
    res = os.environ.get("TWIST_RESULTS", os.path.join(AEG, "cmb-fit", "results"))
    f = {w: json.load(open(os.path.join(res, f"cmp_{name(w)}.json")))["minimum"] for w in BASE}
    d = f["FLAG1"]["chi2"] - f["LCDM"]["chi2"]; b = f["FLAG1"].get("scf_coupling_beta")
    reading = ("HOLDS ON PR4" if d <= -2 and b is not None and b > 0.01 else "WEAKENS" if d <= 0 else "REVERSES")
    keep = ("chi2", "H0", "sigma8", "Omega_m", "scf_coupling_beta")
    out = {"rule": "PREREG_V6_PR4.md", "delta_PR4": round(d, 3), "delta_fitC_PR3": -3.911, "reading": reading,
           "fits": {w: {k: v.get(k) for k in keep} | {"chi2_parts": {k: x for k, x in v.items() if k.startswith("chi2__")}}
                    for w, v in f.items()}}
    json.dump(out, open(os.path.join(AEG, "field_tests", "results", "selfcheck_v6.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    a = sys.argv[1:]
    {"gate": lambda: gate(a[1]), "fit": lambda: fit(a[1]), "score": score}[a[0]]()
