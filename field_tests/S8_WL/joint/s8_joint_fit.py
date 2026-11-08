"""S8-J: the Spiral (and its LCDM reference) refit with DES Y6 cosmic-shear S8 inside the fit.

Rule: field_tests/rules/PREREG_S8_JOINT.md (refuses to fit until PREREG_S8_JOINT.md.sha256 exists).
Engine: exactly the SF fit (cmb-fit/axiclass/early_late_spa.make), unchanged, plus ONE extra likelihood:
    -2 ln L = ((S8 - 0.798) / sigma)^2,  sigma = 0.014 above, 0.015 below   (DES Y6, as S8-WL Part 1)
    S8 = sigma8 sqrt((omega_b + omega_cdm + omega_nu) / h^2 / 0.3)          (as field_tests/scorers/s8wl_score.py)
Runs (best of 4, starting points as SF):  <SF run name>_s8y6, e.g. ax_spa_spiraltwist_dovekie_nlfix_s8y6.

    python s8_joint_fit.py gate              # expected joint chi2 at the stored SF best fits (cloud, no engine)
    python s8_joint_fit.py gate_pc <run>     # G-J for one run through the full fitter (PC, evaluation only)
    python s8_joint_fit.py gate_sum          # combine the six into results/s8j_gate_pc.json
    python s8_joint_fit.py <run>_s8y6        # one fit (PC, WSL env "aegis")
"""
import json
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
AEGIS = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(AEGIS, "cmb-fit", "axiclass"))
RULE = os.path.join(AEGIS, "field_tests", "rules", "PREREG_S8_JOINT.md")

OBS, UP, DN = 0.798, 0.014, 0.015
OMEGA_NU = 0.06 / 93.14
RUNS = ["ax_spa_spiraltwist_nlfix", "ax_spa_spiraltwist_dovekie_nlfix", "ax_spa_spiraltwist_union3_nlfix",
        "ax_spa_lcdm_halofit", "ax_spa_lcdm_halofit_dovekie", "ax_spa_lcdm_halofit_union3"]


def s8(sigma8, omega_b, omega_cdm, H0):
    return sigma8 * math.sqrt((omega_b + omega_cdm + OMEGA_NU) / (H0 / 100) ** 2 / 0.3)


def chi2_s8(x):
    return ((x - OBS) / (UP if x > OBS else DN)) ** 2


def likelihood_class():
    from cobaya.likelihood import Likelihood

    class DESY6S8(Likelihood):
        # Deviation S8J-D1 (S8J_DEVIATIONS.md): omega_b and omega_cdm are the SAMPLED inputs (aliases below), as the rule
        # and s8wl_score.py use. Asking the theory for "omega_cdm" returned the coupled build's present-day value.
        params = {"s8in_omega_b": None, "s8in_omega_cdm": None}

        def get_requirements(self):
            return {"sigma8": None, "H0": None}

        def logp(self, **params_values):
            g = self.provider.get_param
            return -0.5 * chi2_s8(s8(g("sigma8"), params_values["s8in_omega_b"], params_values["s8in_omega_cdm"],
                                     g("H0")))

    return DESY6S8


def gate():
    """G-J: at each stored SF best fit, the added term must equal the S8-WL Part 1 penalty input (no fitting)."""
    res = os.environ.get("TWIST_RESULTS", os.path.join(AEGIS, "cmb-fit", "results"))
    out = {}
    for r in RUNS:
        m = json.load(open(f"{res}/cmp_{r}.json"))["minimum"]
        x = s8(m["sigma8"], m["omega_b"], m["omega_cdm"], m["H0"])
        out[r] = {"S8": round(x, 4), "chi2_S8": round(chi2_s8(x), 3), "chi2_stored": round(m["chi2"], 3),
                  "chi2_joint_expected": round(m["chi2"] + chi2_s8(x), 3)}
    json.dump(out, open(os.path.join(HERE, "s8j_gate.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


def add_s8(info):
    info["likelihood"]["s8_desy6"] = {"external": likelihood_class()}
    info["params"]["s8in_omega_b"] = {"value": "lambda omega_b: omega_b", "derived": False}
    info["params"]["s8in_omega_cdm"] = {"value": "lambda omega_cdm: omega_cdm", "derived": False}


def gate_pc(r):
    """G-J for ONE run (one process per run, so no CLASS build or likelihood state carries over): through the full
    fitter (SF engine + the S8 term), at the stored SF best fit, total chi2 must equal stored chi2 + chi2_S8 within 0.05.
    Writes results/s8j_gate_<run>.json; `gate_sum` combines them into results/s8j_gate_pc.json. Evaluation only."""
    import early_late_spa as E
    from cobaya.model import get_model
    exp = json.load(open(os.path.join(HERE, "s8j_gate.json")))
    E._maybe_coupled(r)
    info = E.make(r)
    add_s8(info)
    info.pop("sampler", None); info.pop("output", None)
    model = get_model(info)
    m = json.load(open(f"{E.OUT}/cmp_{r}.json"))["minimum"]
    point = {p: m[p] for p in model.parameterization.sampled_params()}
    parts = {k: round(-2 * float(v), 3) for k, v in model.loglikes(point, as_dict=True)[0].items()}
    chi2 = sum(parts.values())
    out = {"chi2": round(chi2, 3), "expected": exp[r]["chi2_joint_expected"], "parts": parts,
           "pass": bool(abs(chi2 - exp[r]["chi2_joint_expected"]) <= 0.05)}
    print(r, out, flush=True)
    json.dump(out, open(os.path.join(E.OUT, f"s8j_gate_{r}.json"), "w"), indent=1)


def gate_sum():
    res = os.environ.get("TWIST_RESULTS", os.path.join(AEGIS, "cmb-fit", "results"))
    out = {}
    for r in RUNS:
        p = os.path.join(res, f"s8j_gate_{r}.json")
        out[r] = json.load(open(p)) if os.path.exists(p) else {"pass": False, "missing": True}
    out["all_pass"] = all(v["pass"] for v in out.values())
    json.dump(out, open(os.path.join(res, "s8j_gate_pc.json"), "w"), indent=1)
    print("all_pass", out["all_pass"])


def run(name):
    assert name.endswith("_s8y6") and name[:-5] in RUNS, f"unknown run {name}"
    assert os.path.exists(RULE + ".sha256"), "PREREG_S8_JOINT.md is not locked; no fit runs before the lock"
    import early_late_spa as E
    from cobaya.run import run as crun
    base = name[:-5]
    t = time.time()
    E._maybe_coupled(base)
    info = E.make(base)                                  # the SF fit, unchanged
    add_s8(info)
    info["output"] = f"{E.OUT}/chains/cmp_{name}"
    crun(info)
    E.save(name, time.time() - t)


if __name__ == "__main__":
    if sys.argv[1] == "gate":
        gate()
    elif sys.argv[1] == "gate_pc":
        gate_pc(sys.argv[2])
    elif sys.argv[1] == "gate_sum":
        gate_sum()
    else:
        run(sys.argv[1])
