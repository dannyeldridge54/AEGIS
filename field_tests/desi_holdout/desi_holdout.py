"""DESI-HOLDOUT (rule: field_tests/rules/PREREG_DESI_HOLDOUT.md). AI-assisted.
    python desi_holdout.py fit FLAG1|LCDM        holdout fit (all bao. likelihoods removed) -> results/cmp_<name>.json
    python desi_holdout.py predict FLAG1|LCDM [stored]
                                                 DESI chi2 at the holdout minimum ("stored": at the DESI-included
                                                 minimum, the Test A gate) -> desi_holdout/predict_<w>[_stored].json
    python desi_holdout.py truth                 Test B truth from the holdout FLAG-1 minimum -> desi_holdout/truth.json
    python desi_holdout.py mock SN|noSN          Test B fits (DESI-MOCK code, plain build)
    python desi_holdout.py score                 -> field_tests/results/desi_holdout.json
One model per process: the coupled CLASS build cannot be switched after classy is imported."""
import json, os, sys, time, types

HERE = os.path.dirname(os.path.abspath(__file__)); AEG = os.path.abspath(os.path.join(HERE, "..", ".."))
RULE = os.path.join(AEG, "field_tests", "rules", "PREREG_DESI_HOLDOUT.md")
sys.path.insert(0, os.path.join(AEG, "cmb-fit", "axiclass")); sys.path.insert(0, os.path.join(AEG, "field_tests", "S8_WL", "joint"))
sys.path.insert(0, os.path.join(AEG, "field_tests", "desi_mock"))
RUNS = {"FLAG1": ("ax_spa_spiraltwist_kappa1_nlfix", "ax_spa_spiraltwist_kappa1_nlfix_nodesi_s8y6"),
        "LCDM": ("ax_spa_lcdm_halofit", "ax_spa_lcdm_halofit_nodesi_s8y6")}
DESI = "bao.desi_dr2.desi_bao_all"
GATE = {"FLAG1": 8.646, "LCDM": 12.733}


def locked():
    assert os.path.exists(RULE + ".sha256"), "rule not locked"


def fit(which):
    locked()
    import early_late_spa as E
    import s8_joint_fit as J
    from cobaya.run import run as crun
    base, name = RUNS[which]
    t = time.time()
    E._maybe_coupled(base)
    info = E.make(base)
    info["likelihood"] = {k: v for k, v in info["likelihood"].items() if not k.startswith("bao.")}
    J.add_s8(info)
    m = json.load(open(f"{E.OUT}/cmp_{base}_s8y6.json"))["minimum"]
    for k, p in info["params"].items():
        if isinstance(p, dict) and "ref" in p and k in m:
            p["ref"]["loc"] = float(m[k])
    info["sampler"]["minimize"]["best_of"] = 4
    info["output"] = f"{E.OUT}/chains/cmp_{name}"
    crun(info)
    E.save(name, time.time() - t)


def predict(which, stored=False):
    """Evaluate the full s8y6 setup (DESI included) at a minimum; report the DESI term. No refit."""
    import early_late_spa as E
    import s8_joint_fit as J
    from cobaya.model import get_model
    base, name = RUNS[which]
    E._maybe_coupled(base)
    info = E.make(base)
    assert DESI in info["likelihood"]
    J.add_s8(info)
    info.pop("sampler", None); info.pop("output", None)
    model = get_model(info)
    src = f"{E.OUT}/cmp_{base}_s8y6.json" if stored else f"{E.OUT}/cmp_{name}.json"
    m = json.load(open(src))["minimum"]
    point = {p: m[p] for p in model.parameterization.sampled_params()}
    parts = {k: -2 * float(v) for k, v in model.loglikes(point, as_dict=True)[0].items()}
    out = {"which": which, "minimum_from": os.path.basename(src), "chi2_DESI": parts[DESI], "parts": parts}
    if stored:
        out["expected"] = GATE[which]; out["pass"] = abs(parts[DESI] - GATE[which]) <= 0.01
    print(out, flush=True)
    json.dump(out, open(os.path.join(HERE, f"predict_{which}{'_stored' if stored else ''}.json"), "w"), indent=1)


def truth():
    """desi_mock.truth() with the holdout FLAG-1 minimum as the truth (everything else identical)."""
    import numpy as np
    for n in ("candl", "candl.interface", "spt_candl_data"):
        sys.modules.setdefault(n, types.SimpleNamespace(CandlCobayaLikelihood=None, SPT3G_D1_TnE=None, interface=None))
    sys.modules["candl"].interface = sys.modules["candl.interface"]
    import early_late_spa as E, spiral_guess
    base, name = RUNS["FLAG1"]; E._maybe_coupled(base); import classy
    import desi_mock as DM
    info = E.make(base); st = json.load(open(f"{E.OUT}/cmp_{name}.json"))["minimum"]
    a = dict(info["theory"]["classytwist"]["extra_args"])
    a.update({"A_s": 1e-10 * np.exp(st["logA"]), "n_s": st["n_s"], "100*theta_s": st["theta_s_1e2"], "omega_b": st["omega_b"],
              "omega_cdm": st["omega_cdm"], "tau_reio": st["tau_reio"], "output": "mPk"})
    for k in ("lensing", "l_max_scalars", "non_linear"): a.pop(k, None)
    b = st["scf_coupling_beta"]; a["scf_coupling_beta"] = b
    a["scf_parameters"] = f"1.0, 0.0, {spiral_guess.mu1_guess(1.0, b, st['omega_b'], st['omega_cdm'])}, 0.0, 0.0, 0.0"
    c = classy.Class(); c.set(a); c.compute()
    bao, mu, th, rd, h = DM.observables(c)
    bg = c.get_background(); zz = bg["z"][::-1]; rc = bg["(.)rho_cdm"][::-1]
    wc_early = float(np.interp(1090, zz, rc)) / 1091 ** 3 / (100 / DM.C) ** 2
    out = {"run": name, "h": h, "omega_b": st["omega_b"], "omega_cdm_today": st["omega_cdm"], "omega_c_early": wc_early,
           "theta_star_100": th, "rd": rd, "bao": bao.tolist(), "mu": mu.tolist(),
           "cmb": [th, st["omega_b"], st["omega_b"] + wc_early]}
    json.dump(out, open(os.path.join(HERE, "truth.json"), "w"), indent=1)
    print({k: v for k, v in out.items() if k not in ("bao", "mu")})


def mock(part):
    """The DESI-MOCK fits, unchanged, reading this folder's truth.json and writing here."""
    locked()
    import desi_mock as DM
    DM.HERE, DM.RULE = HERE, RULE
    DM.fit(part)
    if all(os.path.exists(os.path.join(HERE, f"desi_mock_part_{q}.json")) for q in ("SN", "noSN")):
        DM.score()


def score():
    res = os.environ.get("TWIST_RESULTS", os.path.join(AEG, "cmb-fit", "results"))
    J = lambda p: json.load(open(p))
    out = {"rule": "PREREG_DESI_HOLDOUT.md"}
    gate = {w: J(os.path.join(HERE, f"predict_{w}_stored.json")) for w in RUNS}
    out["gate"] = {w: {"chi2_DESI": round(g["chi2_DESI"], 3), "expected": g["expected"], "pass": g["pass"]} for w, g in gate.items()}
    fits = {w: J(os.path.join(res, f"cmp_{n}.json"))["minimum"] for w, (_, n) in RUNS.items()}
    keep = ("chi2", "H0", "sigma8", "Omega_m", "scf_coupling_beta")
    out["holdout_fits"] = {w: {k: m.get(k) for k in keep} for w, m in fits.items()}
    b = fits["FLAG1"]["scf_coupling_beta"]
    edge = b is None or abs(abs(b) - 0.15) < 1e-4
    pred = {w: J(os.path.join(HERE, f"predict_{w}.json"))["chi2_DESI"] for w in RUNS}
    dA = pred["FLAG1"] - pred["LCDM"]
    out["testA"] = {"chi2_DESI_FLAG1": round(pred["FLAG1"], 3), "chi2_DESI_LCDM": round(pred["LCDM"], 3),
                    "delta_A": round(dA, 3), "delta_A_DESI_included": round(GATE["FLAG1"] - GATE["LCDM"], 3)}
    if not all(g["pass"] for g in gate.values()) or edge:
        out["testA"]["reading"] = "NO VERDICT" + (" (gate failed)" if not all(g["pass"] for g in gate.values()) else " (beta at prior edge)")
    else:
        out["testA"]["reading"] = ("FLAG-1 PREDICTS DESI BETTER" if dA <= -4 else "LEANS FLAG-1" if dA <= -1 else
                                   "NO DIFFERENCE" if dA < 1 else "LEANS LCDM" if dA < 4 else "LCDM PREDICTS DESI BETTER")
    mr = os.path.join(HERE, "desi_mock_result.json")
    if os.path.exists(mr):
        r = J(mr)
        out["testB"] = {"reading": r["reading"], **{k: {q: r[k][q] for q in ("delta_chi2", "sigma_2dof", "w0", "wa")}
                                                     for k in ("BAO+CMB+SN", "BAO+CMB")}}
    else:
        out["testB"] = "not run yet"
    json.dump(out, open(os.path.join(AEG, "field_tests", "results", "desi_holdout.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    a = sys.argv[1:]
    {"fit": lambda: fit(a[1]), "predict": lambda: predict(a[1], len(a) > 2 and a[2] == "stored"),
     "truth": truth, "mock": lambda: mock(a[1]), "score": score}[a[0]]()
