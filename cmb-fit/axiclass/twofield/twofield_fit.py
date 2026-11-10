"""Two-field Twist fit (rule: field_tests/rules/PREREG_TWOFIELD.md; refuses to fit before it is locked).
Model = FLAG-1 exactly (PREREG_FLAGSHIP.md: S8-J setup, kappa = 1, beta_eff free, DES Y6 S8 term, same data) on the
AxiCLASS_twofield build, with the dilaton carried by the new "dil" field (same equations; Lambda's input closure handed
to it) PLUS the early n = 3 axion field on AxiCLASS's own scalar field (KG + fluid switch), three new parameters:
  fraction_axion_ac [0.001, 0.3], log10_axion_ac [-4.3, -3.0], theta_i_scf [0.1, 3.1]
(the Locked Twist's ranges for f_EDE, log10 z_c, theta_i; AxiCLASS's targets agree with the exact f_EDE and z_c to
~1e-4 at the Locked Twist point, tf_gates_ede.json; exact values are reported after the fit).
    python twofield_fit.py gate_pc            # G-TF-PC: early field off, at the FLAG-1 best fits: chi2 = stored FLAG-1 within 0.15
    python twofield_fit.py TF[_dovekie|_union3]
"""
import glob
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
AX = os.path.dirname(HERE)
AEGIS = os.path.abspath(os.path.join(AX, "..", ".."))
sys.path.insert(0, AX)
sys.path.insert(0, os.path.join(AEGIS, "field_tests", "S8_WL", "joint"))
RULE = os.path.join(AEGIS, "field_tests", "rules", "PREREG_TWOFIELD.md")
FLAG = {"TF": "ax_spa_spiraltwist_kappa1_nlfix", "TF_dovekie": "ax_spa_spiraltwist_kappa1_dovekie_nlfix",
        "TF_union3": "ax_spa_spiraltwist_kappa1_union3_nlfix"}
DILATON_SCF_KEYS = ("scf_potential", "scf_has_perturbations", "attractor_ic_scf", "scf_evolve_as_fluid", "do_shooting_scf",
                    "Omega_Lambda", "Omega_scf", "scf_tuning_index", "scf_parameters")
EDE_ARGS = {"scf_potential": "axion", "n_axion": 3, "security_small_Omega_scf": 0.001, "n_axion_security": 2.09,
            "use_big_theta_scf": "yes", "scf_has_perturbations": "yes", "attractor_ic_scf": "no", "scf_tuning_index": 0,
            "do_shooting": "yes", "do_shooting_scf": "yes"}
EARLY = {"fraction_axion_ac": (0.001, 0.3, 0.08, 0.01, r"f_{\rm EDE}"),
         "log10_axion_ac": (-4.3, -3.0, -3.55, 0.05, r"\log_{10} a_c"),
         "theta_i_scf": (0.1, 3.1, 2.8, 0.05, r"\theta_i")}


def _theory_class(early):
    from cobaya.theories.classy import classy as _classy

    class ClassyTwoField(_classy):
        def set(self, params_values_dict):
            p = dict(params_values_dict)
            k = p.pop("spiral_kappa")
            beta = p.pop("scf_coupling_beta")
            # the flagship's dilaton, moved to "dil": V = mu^4 e^(-kappa phi), phi_ini = kappa (that build's convention)
            self.extra_args.update({"dilaton": "yes", "dil_kappa": k, "dil_phi_ini": k, "dil_beta": beta})
            if early:
                self.extra_args["scf_parameters"] = f"{p.pop('theta_i_scf')}, 0."
            super().set(p)
    return ClassyTwoField


def make(name, early=True):
    import early_late_spa as E
    import s8_joint_fit as J
    E.COUPLED_NLFIX_BUILD = os.path.join(E._BUILDS, "AxiCLASS_twofield/python/build")
    base = FLAG[name]
    E._maybe_coupled(base)
    import classy
    assert "AxiCLASS_twofield" in classy.__file__, classy.__file__
    info = E.make(base)
    J.add_s8(info)
    th = info["theory"].pop("classytwist")
    extra = {k: v for k, v in th["extra_args"].items() if k not in DILATON_SCF_KEYS}
    extra["Omega_fld"] = 0
    if early:
        extra.update(EDE_ARGS)
    info["theory"]["classytwotf"] = {"external": _theory_class(early), "extra_args": extra, "ignore_obsolete": True}
    p = info["params"]
    flag = json.load(open(f"{E.OUT}/cmp_{base}_s8y6.json"))["minimum"]     # start at the FLAG-1 best fit
    for k, v in p.items():
        if isinstance(v, dict) and "ref" in v and k in flag:
            v["ref"]["loc"] = float(flag[k])
    if early:
        for k, (lo, hi, loc, sc, lx) in EARLY.items():
            p[k] = E.P(lo, hi, loc, sc, lx)
    info["sampler"] = {"minimize": dict(info["sampler"]["minimize"], best_of=4)}
    info["output"] = f"{E.OUT}/chains/cmp_{name}"
    return info, E


def gate_pc():
    from cobaya.model import get_model
    out = {}
    for name, base in FLAG.items():
        info, E = make(name, early=False)
        info.pop("sampler", None); info.pop("output", None)
        m = get_model(info)
        st = json.load(open(f"{E.OUT}/cmp_{base}_s8y6.json"))["minimum"]
        point = {k: st[k] for k in m.parameterization.sampled_params()}
        chi2 = -2 * sum(m.loglikes(point, as_dict=True)[0].values())
        out[name] = {"chi2": round(chi2, 3), "stored_FLAG1": round(st["chi2"], 3), "diff": round(chi2 - st["chi2"], 3),
                     "pass": bool(abs(chi2 - st["chi2"]) <= 0.15)}
        print(name, out[name], flush=True)
    out["all_pass"] = all(v["pass"] for v in out.values() if isinstance(v, dict))
    json.dump(out, open(os.path.join(E.OUT, "tf_gate_pc.json"), "w"), indent=1)
    return out["all_pass"]


def run(name):
    assert name in FLAG, f"unknown run {name}"
    assert os.path.exists(RULE + ".sha256"), "PREREG_TWOFIELD.md is not locked; no fit runs before the lock"
    from cobaya.run import run as crun
    t = time.time()
    info, E = make(name)
    crun(info)
    E.save(name, time.time() - t)


if __name__ == "__main__":
    if sys.argv[1] == "gate_pc":
        sys.exit(0 if gate_pc() else 1)
    run(sys.argv[1])
