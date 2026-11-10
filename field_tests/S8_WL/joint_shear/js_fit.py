"""JOINT-SHEAR fits (field_tests/rules/PREREG_JOINT_SHEAR.md), PC (WSL env "aegis").
Model = the stored fit's own setup (S8-A: angle_fit.make; LCDM: early_late_spa.make), best of 4, PLUS one likelihood:
the calibrated quadratic q(S8, Omega_m[, beta_eff]) for the full DES Y3 shear chi2_WL (js_calib.json "fit").
S8 and Omega_m are computed exactly as in the calibration (pk files): Omega_m = (omega_b + omega_dm + omega_nu)/h^2
(omega_dm = omega_cdm + omega_fld for S8-A; sampled inputs, not CLASS's present-day omega_cdm), S8 = sigma8 sqrt(Omega_m/0.3).
    python js_fit.py gate_pc            # G-JS-PC: at the two calibration centres, q(S8 from the fitter) = q(S8 from the table) within 0.05
    python js_fit.py <base>             # base in RUNS; writes results/cmp_<base>__jsfit.json
Refuses to run before the lock and unless the calibration gate G-JS passed for that model."""
import json
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
AEGIS = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(AEGIS, "cmb-fit", "axiclass"))
sys.path.insert(0, os.path.join(AEGIS, "cmb-fit", "axiclass", "angle"))
RULE = os.path.join(AEGIS, "field_tests", "rules", "PREREG_JOINT_SHEAR.md")
TABLE = os.path.join(HERE, "js_calib.json")
OMEGA_NU = 0.06 / 93.14
RUNS = {"S8A": "S8A", "S8A_dovekie": "S8A", "S8A_union3": "S8A",
        "ax_spa_lcdm_halofit": "LCDM", "ax_spa_lcdm_halofit_dovekie": "LCDM", "ax_spa_lcdm_halofit_union3": "LCDM"}


def coef(model):
    fit = json.load(open(TABLE))["fit"][model]
    assert fit["G-JS"] == "PASS", f"G-JS did not pass for {model}: no fits (rule)"
    return fit["coef"]


def q(c, S8, Om, beta=None):
    import itertools
    x = [S8, Om] + ([beta] if beta is not None else [])
    f = [1.0] + x + [a * b for a, b in itertools.combinations_with_replacement(x, 2)]
    return sum(a * b for a, b in zip(c, f))


def likelihood_class(model):
    from cobaya.likelihood import Likelihood
    c = coef(model)
    s8a = model == "S8A"

    class JSShear(Likelihood):
        params = {"jsin_omega_b": None, "jsin_omega_dm": None, **({"jsin_beta": None} if s8a else {})}

        def get_requirements(self):
            return {"sigma8": None, "H0": None}

        def logp(self, **p):
            g = self.provider.get_param
            Om = (p["jsin_omega_b"] + p["jsin_omega_dm"] + OMEGA_NU) / (g("H0") / 100) ** 2
            S8 = g("sigma8") * math.sqrt(Om / 0.3)
            return -0.5 * q(c, S8, Om, p["jsin_beta"] if s8a else None)

    return JSShear


def make(base):
    model = RUNS[base]
    if model == "S8A":
        import angle_fit
        info, E = angle_fit.make(base)
        dm, beta = "lambda omega_dm: omega_dm", {"jsin_beta": {"value": "lambda beta_eff: beta_eff", "derived": False}}
    else:
        import early_late_spa as E
        E._maybe_coupled(base)
        info = E.make(base)
        dm, beta = "lambda omega_cdm: omega_cdm", {}
    info["likelihood"]["js_shear"] = {"external": likelihood_class(model)}
    info["params"]["jsin_omega_b"] = {"value": "lambda omega_b: omega_b", "derived": False}
    info["params"]["jsin_omega_dm"] = {"value": dm, "derived": False}
    info["params"].update(beta)
    info["sampler"] = {"minimize": dict(info["sampler"]["minimize"], best_of=4)}
    return info, E


def gate_pc():
    from cobaya.model import get_model
    tab = json.load(open(TABLE))
    out = {}
    for base, model in (("S8A", "S8A"), ("ax_spa_lcdm_halofit", "LCDM")):
        info, E = make(base)
        info.pop("sampler", None); info.pop("output", None)
        m = get_model(info)
        st = json.load(open(f"{E.OUT}/cmp_{base}.json"))["minimum"]
        point = {k: st[k] for k in m.parameterization.sampled_params()}
        parts = m.loglikes(point, as_dict=True)[0]
        got = -2 * float(parts["js_shear"])
        row = tab["points"][f"{base}__jsc"]
        want = q(coef(model), row["S8"], row["Omega_m"], row["beta_eff"] if model == "S8A" else None)
        out[base] = {"q_fitter": round(got, 3), "q_table": round(want, 3), "pass": bool(abs(got - want) <= 0.05)}
        print(base, out[base], flush=True)
    out["all_pass"] = all(v["pass"] for v in out.values() if isinstance(v, dict))
    json.dump(out, open(os.path.join(E.OUT, "js_gate_pc.json"), "w"), indent=1)
    return out["all_pass"]


def run(base):
    assert base in RUNS, f"unknown run {base}"
    assert os.path.exists(RULE + ".sha256"), "PREREG_JOINT_SHEAR.md is not locked"
    from cobaya.run import run as crun
    name = f"{base}__jsfit"
    t = time.time()
    info, E = make(base)
    info["output"] = f"{E.OUT}/chains/cmp_{name}"
    crun(info)
    E.save(name, time.time() - t)


if __name__ == "__main__":
    if sys.argv[1] == "gate_pc":
        sys.exit(0 if gate_pc() else 1)
    run(sys.argv[1])
