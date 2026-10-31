"""Run AxiCLASS directly at the pact_edelock CAMB best point and print CLASS's own error message."""
import json
import math

from classy import Class, CosmoComputationError, CosmoSevereError

m = json.load(open("/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/results/cmp_pact_edelock.json"))["minimum"]
p = {"A_s": m["As"], "n_s": m["ns"], "H0": m["H0"], "omega_b": m["ombh2"], "omega_cdm": m["omch2"],
     "tau_reio": m["tau"], "N_ncdm": 1, "m_ncdm": 0.06, "N_ur": 2.0328, "output": "tCl,pCl,lCl", "lensing": "yes",
     "do_shooting": "yes", "do_shooting_scf": "yes", "scf_potential": "axion", "n_axion": 3,
     "security_small_Omega_scf": 0.001, "n_axion_security": 2.09, "use_big_theta_scf": "yes",
     "scf_has_perturbations": "yes", "attractor_ic_scf": "no", "scf_tuning_index": 0,
     "precision_newton_method_F": 1e-3, "precision_newton_method_x": 1e-3,
     "fraction_axion_ac": m["fde_zc"], "log10_axion_ac": math.log10(1 / (1 + m["zc"])),
     "scf_parameters": f"{m['theta_i']}, 0."}
for extra in ({}, {"Omega_Lambda": 0.0}, {"use_big_theta_scf": "no"}, {"do_shooting_scf": "no"}):
    c = Class()
    try:
        c.set({**p, **extra})
        c.compute()
        print("OK with", extra, "H0 =", c.h() * 100, "f_ede:", c.get_current_derived_parameters(["f_ede"]))
        c.struct_cleanup()
        break
    except (CosmoComputationError, CosmoSevereError) as e:
        print("FAILED with", extra, "->", str(e).strip().splitlines()[-3:])
    c.struct_cleanup()
