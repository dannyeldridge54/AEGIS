"""Spiral-L engine check (no data): at a stored Spiral best fit, compare sigma8 from the SF build and the ULA build.
  (a) ULA share ~ 0 must reproduce the SF build (code check);
  (b) ULA share f = beta_eff/0.816 of the dark matter at several masses: sigma8, S8 and the mass in eV.
    python ula_check.py [run]   -> ula_check_<run>.json"""
import json, math, os, sys, importlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "field_tests", "S8_WL", "part2"))
import axiclass_pk as AP   # noqa: E402  (candl stub + early_late_spa)
E = AP.E
BLD = os.environ.get("TWIST_BUILDS", os.path.expanduser("~"))
HBAR_H0 = 2.1332e-33   # eV per (100 km/s/Mpc)

def args_for(name):
    info = E.make(name)
    best = json.load(open(os.path.join(E.OUT, f"cmp_{name}.json")))["minimum"]
    a = dict(info["theory"]["classytwist"]["extra_args"])
    a.update({"A_s": 1e-10 * np.exp(best["logA"]), "n_s": best["n_s"], "100*theta_s": best["theta_s_1e2"],
              "omega_b": best["omega_b"], "omega_cdm": best["omega_cdm"], "tau_reio": best["tau_reio"],
              "scf_coupling_beta": best["scf_coupling_beta"]})
    import spiral_guess
    k = best["spiral_kappa"]
    mu = spiral_guess.mu1_guess(k, best["scf_coupling_beta"], best["omega_b"], best["omega_cdm"])
    a["scf_parameters"] = f"{k}, 0.0, {mu}, 0.0, 0.0, 0.0"
    a.pop("l_max_scalars", None)
    a.update({"output": "mPk", "P_k_max_1/Mpc": 5.0})
    return a, best

def run(build, a):
    sys.path.insert(0, build)
    for m in [m for m in sys.modules if m.startswith("classy")]:
        del sys.modules[m]
    import classy
    c = classy.Class(); c.set(a); c.compute()
    h = c.h(); s8 = c.sigma(8 / h, 0.0)
    om = (a["omega_b"] + a["omega_cdm"] + a.get("omega_fld", 0) + 0.06 / 93.14) / h ** 2
    out = {"sigma8": s8, "S8": s8 * math.sqrt(om / 0.3), "H0": 100 * h}
    try:
        out["m_eV"] = c.get_background()["H [1/Mpc]"][-1] and None
    except Exception:
        pass
    c.struct_cleanup(); sys.path.remove(build)
    return out

def main(name):
    a, best = args_for(name)
    res = {"run": name, "beta_eff": best["scf_coupling_beta"]}
    sf = os.path.join(BLD, "AxiCLASS_coupled_nlfix/python/build"); ul = os.path.join(BLD, "AxiCLASS_coupled_nlfix_ula/python/build")
    sf = [os.path.join(sf, d) for d in os.listdir(sf) if d.startswith("lib")][0]
    ul = [os.path.join(ul, d) for d in os.listdir(ul) if d.startswith("lib")][0]
    res["SF_build"] = run(sf, a)
    f = best["scf_coupling_beta"] / 0.816
    res["f"] = f
    def ula(fr, lac):
        b = dict(a); b.pop("Omega_fld", None)
        b.update({"omega_cdm": a["omega_cdm"] * (1 - fr), "omega_fld": a["omega_cdm"] * fr, "use_ppf": "no",
                  "fluid_equation_of_state": "EDE", "ede_parametrization": "pheno_axion", "n_pheno_axion": 1, "Theta_initial_fld": 0.1,
                  "log10_a_c": lac, "background_verbose": 2})
        return run(ul, b)
    res["ULA_tiny"] = ula(1e-7, -5.0)
    res["ULA_tiny"]["rel_sigma8_vs_SF"] = res["ULA_tiny"]["sigma8"] / res["SF_build"]["sigma8"] - 1
    res["scan"] = {}
    for lac in (-6.0, -5.0, -4.5, -4.0, -3.7, -3.4):
        r = ula(f, lac); r["dS8_vs_SF"] = r["S8"] - res["SF_build"]["S8"]; res["scan"][lac] = r
        print(lac, r, flush=True)
    json.dump(res, open(os.path.join(HERE, f"ula_check_{name}.json"), "w"), indent=1, default=float)
    print(json.dumps({k: v for k, v in res.items() if k != "scan"}, indent=1, default=float))

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "ax_spa_spiraltwist_nlfix")
