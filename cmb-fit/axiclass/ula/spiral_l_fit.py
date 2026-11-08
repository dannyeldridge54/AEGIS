"""S8-L: the Spiral with its matter-like angle share as an ultralight field (the "light angle").

Rule: field_tests/rules/PREREG_SPIRAL_L.md (refuses to fit until PREREG_SPIRAL_L.md.sha256 exists).
Model = the SF Spiral (early_late_spa.make, unchanged) with ONE change: the angle share f = beta_eff/0.816 of the dark
matter is moved out of the coupled CDM into AxiCLASS's pheno_axion fluid with n = 1 (w -> 0, sound speed
c_s^2 = k^2/(k^2 + 4 a^2 m^2)), uncoupled. Its mass is set by the onset scale factor a_c: ONE new parameter, log10_a_c.
    omega_dm (sampled, = SF's omega_cdm prior);  omega_cdm = (1 - f) omega_dm;  omega_fld = f omega_dm
Fixed: n_pheno_axion = 1, Theta_initial_fld = 0.1 (harmonic regime), w before onset = -1 (frozen field).
Build: ula/build_ula.sh (AxiCLASS_coupled_nlfix + patch_ula.py: two non-physics edits).

    python spiral_l_fit.py gate_pc                    # G-L (PC, evaluation only, allowed before the lock)
    python spiral_l_fit.py spiralL[_dovekie|_union3]  # one fit (PC, after the lock)
"""
import glob
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
AXI = os.path.dirname(HERE)
AEGIS = os.path.abspath(os.path.join(AXI, "..", ".."))
sys.path.insert(0, AXI)
RULE = os.path.join(AEGIS, "field_tests", "rules", "PREREG_SPIRAL_L.md")
SF = {"spiralL": "ax_spa_spiraltwist_nlfix", "spiralL_dovekie": "ax_spa_spiraltwist_dovekie_nlfix",
      "spiralL_union3": "ax_spa_spiraltwist_union3_nlfix"}
F_OF_BETA = "scf_coupling_beta/0.816"
TINY = 1e-7          # gate G-L: light share forced to ~0, so the new build must reproduce the stored SF fit


def make(name, fixed_ac=None, share=None):
    import early_late_spa as E
    E.COUPLED_NLFIX_BUILD = os.path.join(E._BUILDS, "AxiCLASS_coupled_nlfix_ula/python/build")
    E._maybe_coupled(SF[name])
    import classy
    assert "AxiCLASS_coupled_nlfix_ula" in classy.__file__, classy.__file__
    info = E.make(SF[name])                                   # the SF fit, unchanged ...
    extra = info["theory"]["classytwist"]["extra_args"]
    extra.pop("Omega_fld", None)                              # ... except the dark-matter split below
    extra.update({"fluid_equation_of_state": "EDE", "ede_parametrization": "pheno_axion", "n_pheno_axion": 1,
                  "Theta_initial_fld": 0.1, "use_ppf": "no"})
    p = info["params"]
    p["omega_dm"] = dict(p.pop("omega_cdm"), drop=True, latex=r"\omega_{\rm dm}")
    f = F_OF_BETA if share is None else repr(share)
    p["omega_cdm"] = {"value": f"lambda omega_dm, scf_coupling_beta: omega_dm*(1-{f})"}
    p["omega_fld"] = {"value": f"lambda omega_dm, scf_coupling_beta: omega_dm*{f}"}
    if fixed_ac is None:
        p["log10_a_c"] = {"prior": {"min": -6.0, "max": -3.5}, "ref": {"dist": "norm", "loc": -5.0, "scale": 0.2},
                          "proposal": 0.1, "latex": r"\log_{10} a_c"}
    else:
        p["log10_a_c"] = fixed_ac
    info["output"] = f"{E.OUT}/chains/cmp_{name}"
    return info, E


def gate_pc():
    """G-L (code check): at each stored SF best fit, with the light share forced to 1e-7 (log10_a_c = -5), the total
    chi2 through the full fitter on the new build must equal the stored SF chi2 within 0.1. Evaluation only."""
    from cobaya.model import get_model
    out = {}
    for name, sf in SF.items():
        info, E = make(name, fixed_ac=-5.0, share=TINY)
        info.pop("sampler", None); info.pop("output", None)
        model = get_model(info)
        m = json.load(open(f"{E.OUT}/cmp_{sf}.json"))["minimum"]
        point = {k: (m["omega_cdm"] if k == "omega_dm" else m[k]) for k in model.parameterization.sampled_params()}
        chi2 = -2 * sum(model.loglikes(point, as_dict=True)[0].values())
        out[name] = {"chi2": round(chi2, 3), "stored_SF": round(m["chi2"], 3), "diff": round(chi2 - m["chi2"], 3),
                     "pass": bool(abs(chi2 - m["chi2"]) <= 0.1)}
        print(name, out[name], flush=True)
    out["all_pass"] = bool(all(v["pass"] for v in out.values() if isinstance(v, dict)))
    json.dump(out, open(os.path.join(E.OUT, "spiral_l_gate_pc.json"), "w"), indent=1)


def run(name):
    assert name in SF, f"unknown run {name}"
    assert os.path.exists(RULE + ".sha256"), "PREREG_SPIRAL_L.md is not locked; no fit runs before the lock"
    from cobaya.run import run as crun
    t = time.time()
    info, E = make(name)
    crun(info)
    E.save(name, time.time() - t)


if __name__ == "__main__":
    gate_pc() if sys.argv[1] == "gate_pc" else run(sys.argv[1])
