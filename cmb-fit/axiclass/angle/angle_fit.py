"""S8-A: the S8-L model with the coupling where the action puts it (theory/DM_COUPLING_PICTURE.md, picture B).

Rule: field_tests/rules/PREREG_S8A_ANGLE.md (refuses to fit until its .sha256 exists).
Model = S8-L (ula/spiral_l_fit.py) with ONE change: the cold dark matter is uncoupled and the ultralight angle share
f = beta_eff/sqrt(2/3) carries the coupling, with strength fixed at sqrt(2/3) (derived, not fitted):
    scf_coupling_beta = 0 (CDM), fld_coupling_beta = sqrt(2/3) (angle), fld_in_delta_m = 1 (sigma8 counts the angle).
beta_eff keeps the S8-L prior [0, 0.12] and is sampled under the name beta_eff. Same data, priors, settings, best of 4.
Build: angle/build_angle.sh (AxiCLASS_coupled_nlfix_ula + patch_angle.py; gates angle_gates.py passed 9 Nov).

    python angle_fit.py gate_pc               # G-A-PC (evaluation only, allowed before the lock)
    python angle_fit.py S8A[_dovekie|_union3] # one fit (PC, after the lock)
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
AXI = os.path.dirname(HERE)
AEGIS = os.path.abspath(os.path.join(AXI, "..", ".."))
sys.path.insert(0, AXI)
sys.path.insert(0, os.path.join(AXI, "ula"))
RULE = os.path.join(AEGIS, "field_tests", "rules", "PREREG_S8A_ANGLE.md")
SL = {"S8A": "spiralL", "S8A_dovekie": "spiralL_dovekie", "S8A_union3": "spiralL_union3"}
BETA_A = (2 / 3) ** 0.5


def make(name, angle_coupled=True):
    import spiral_l_fit as L
    import early_late_spa as E
    E.COUPLED_NLFIX_BUILD = os.path.join(E._BUILDS, "AxiCLASS_coupled_nlfix_angle/python/build")
    info, E = _make_sl(L, name)
    p = info["params"]
    extra = info["theory"]["classytwist"]["extra_args"]
    if angle_coupled:
        p["beta_eff"] = dict(p.pop("scf_coupling_beta"), drop=True, latex=r"\beta_{\rm eff}")
        p["scf_coupling_beta"] = 0.0
        for k in ("omega_cdm", "omega_fld"):
            p[k] = {"value": p[k]["value"].replace("scf_coupling_beta", "beta_eff")}
        extra.update({"fld_coupling_beta": BETA_A, "fld_in_delta_m": 1})
    info["output"] = f"{E.OUT}/chains/cmp_{name}"
    return info, E


def _make_sl(L, name):
    """spiral_l_fit.make's model on the angle build (spiral_l_fit.make itself asserts the ULA build)."""
    import early_late_spa as E
    sl_name = SL[name]
    E._maybe_coupled(L.SF[sl_name])
    info = E.make(L.SF[sl_name])
    extra = info["theory"]["classytwist"]["extra_args"]
    extra.pop("Omega_fld", None)
    extra.update({"fluid_equation_of_state": "EDE", "ede_parametrization": "pheno_axion", "n_pheno_axion": 1,
                  "Theta_initial_fld": 0.1, "use_ppf": "no"})
    p = info["params"]
    p["omega_dm"] = dict(p.pop("omega_cdm"), drop=True, latex=r"\omega_{\rm dm}")
    f = L.F_OF_BETA
    p["omega_cdm"] = {"value": f"lambda omega_dm, scf_coupling_beta: omega_dm*(1-{f})"}
    p["omega_fld"] = {"value": f"lambda omega_dm, scf_coupling_beta: omega_dm*{f}"}
    p["log10_a_c"] = {"prior": {"min": -6.0, "max": -3.5}, "ref": {"dist": "norm", "loc": -5.0, "scale": 0.2},
                      "proposal": 0.1, "latex": r"\log_{10} a_c"}
    return info, E


def _check_build():
    import classy
    assert "AxiCLASS_coupled_nlfix_angle" in classy.__file__, classy.__file__


def gate_pc():
    """G-A-PC: with the angle coupling OFF (S8-L equations) the fitter on the angle build reproduces each stored S8-L
    chi2 within 0.1 at its stored best point. Evaluation only."""
    from cobaya.model import get_model
    out = {}
    for name, sl in SL.items():
        info, E = make(name, angle_coupled=False)
        _check_build()
        info.pop("sampler", None); info.pop("output", None)
        model = get_model(info)
        m = json.load(open(f"{E.OUT}/cmp_{sl}.json"))["minimum"]
        point = {k: m[k] for k in model.parameterization.sampled_params()}
        chi2 = -2 * sum(model.loglikes(point, as_dict=True)[0].values())
        out[name] = {"chi2": round(chi2, 3), "stored_S8L": round(m["chi2"], 3), "diff": round(chi2 - m["chi2"], 3),
                     "pass": bool(abs(chi2 - m["chi2"]) <= 0.1)}
        print(name, out[name], flush=True)
    out["all_pass"] = bool(all(v["pass"] for v in out.values() if isinstance(v, dict)))
    json.dump(out, open(os.path.join(E.OUT, "s8a_gate_pc.json"), "w"), indent=1)
    return out["all_pass"]


def run(name):
    assert name in SL, f"unknown run {name}"
    assert os.path.exists(RULE + ".sha256"), "PREREG_S8A_ANGLE.md is not locked; no fit runs before the lock"
    from cobaya.run import run as crun
    t = time.time()
    info, E = make(name)
    _check_build()
    crun(info)
    E.save(name, time.time() - t)


if __name__ == "__main__":
    if sys.argv[1] == "gate_pc":
        sys.exit(0 if gate_pc() else 1)
    run(sys.argv[1])
