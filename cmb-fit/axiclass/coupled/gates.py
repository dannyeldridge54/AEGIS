# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights.
"""Validation gates V1-V4 for the Coupled Twist build (CubeMind PREREGISTRATION_COUPLED_TWIST.md).

    python gates.py chi2 original|coupled [beta]  -> total chi2 at a fixed Late Twist point (V1 compares the two)
    python gates.py background [beta]             -> V2 energy exchange, V3 phi-MDE, V4 sign, from the coupled build

The coupled build is loaded from its own build folder; the installed classy is never touched.
"""
import copy
import glob
import json
import sys

import numpy as np

COUPLED = "/home/syndyr/AxiCLASS_coupled"
OUT = "/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/results"
POINT = {"log10_F": 0.0, "log10_m": 0.2}           # a viable Late Twist point (probe_latetwist.py)


def use_coupled():
    sys.path.insert(0, glob.glob(f"{COUPLED}/python/build/lib*")[0])
    import classy
    assert classy.__file__.startswith(COUPLED), classy.__file__
    return classy


def chi2(which, beta):
    if which == "coupled":
        use_coupled()
    sys.path.insert(1, "/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass")
    from early_late_spa import make
    from cobaya.model import get_model
    import classy
    info = copy.deepcopy(make("ax_spa_latetwist"))
    for k in ("sampler", "output", "resume", "force"):
        info.pop(k, None)
    if which == "coupled":
        info["theory"]["classytwist"]["extra_args"]["scf_coupling_beta"] = beta
    model = get_model(info)
    best = json.load(open(f"{OUT}/cmp_ax_spa_lcdm_halofit.json"))["minimum"]
    sp = list(model.parameterization.sampled_params())
    pt = {p: best.get(p, model.prior.reference(random_state=1)[sp.index(p)]) for p in sp}
    pt.update(POINT)
    r = model.logposterior(pt)
    c = -2 * sum(r.loglikes)
    print(json.dumps({"which": which, "beta": beta, "classy": classy.__file__, "chi2": c}))


def background(beta, no_baryons=False):
    classy = use_coupled()
    sys.path.insert(1, "/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass")
    from early_late_spa import make
    extra = dict(make("ax_spa_latetwist")["theory"]["classytwist"]["extra_args"])
    best = json.load(open(f"{OUT}/cmp_ax_spa_lcdm_halofit.json"))["minimum"]
    pars = {**extra, "omega_b": best["omega_b"], "omega_cdm": best["omega_cdm"], "100*theta_s": best["theta_s_1e2"],
            "A_s": best["A_s"], "n_s": best["n_s"], "tau_reio": best["tau_reio"],
            "f_axion": 10 ** POINT["log10_F"], "m_axion": 10 ** POINT["log10_m"], "scf_coupling_beta": beta,
            "output": "", "background_verbose": 0}
    for k in ("non_linear", "l_max_scalars"):
        pars.pop(k, None)
    if no_baryons:            # V3 exactly as written: all matter coupled, so the target is 2 beta^2/3
        pars["omega_cdm"] += pars["omega_b"] - 1e-5
        pars["omega_b"] = 1e-5
        pars["h"] = 0.68
        pars.pop("100*theta_s")
    c = classy.Class()
    c.set(pars)
    c.compute(["background"])
    bg = c.get_background()
    z = np.asarray(bg["z"]); a = 1 / (1 + z); lna = np.log(a)
    o = np.argsort(lna); lna, a = lna[o], a[o]
    rc = np.asarray(bg["(.)rho_cdm"])[o]
    rs = np.asarray(bg["(.)rho_scf"])[o]
    ps = np.asarray(bg["(.)p_scf"])[o]
    phi = np.asarray(bg["phi_scf"])[o]
    rtot = np.asarray(bg["(.)rho_tot"])[o] if "(.)rho_tot" in bg else None
    d = lambda y: np.gradient(y, lna)
    sel = (a > 1e-4) & (a < 0.99)
    res = {"beta": beta, "keys_ok": True}
    # V2: scalar-field energy equation with the exchange term, d rho_s/dlna = -3(rho_s+p_s) - beta dphi/dlna rho_c
    lhs = d(rs)[sel]
    rhs = (-3 * (rs + ps) - beta * d(phi) * rc)[sel]
    scale = np.maximum(np.abs(rhs), 1e-3 * np.abs(beta * d(phi) * rc)[sel].max() + 1e-300)
    res["V2_max_rel_resid"] = float(np.max(np.abs(lhs - rhs) / np.maximum(np.abs(rs[sel]) * 3, scale)))
    # V4: d ln(rho_c a^3)/dlna = beta dphi/dlna (sign and size)
    lhs4 = d(np.log(rc * a ** 3))[sel]; rhs4 = (beta * d(phi))[sel]
    res["V4_max_abs_resid"] = float(np.max(np.abs(lhs4 - rhs4)))
    res["V4_sign_ok"] = bool(np.all(np.sign(lhs4[np.abs(rhs4) > 1e-8]) == np.sign(rhs4[np.abs(rhs4) > 1e-8])))
    # V3: phi-MDE, Omega_phi -> 2 beta^2/3 in the matter era (V negligible)
    H2 = np.asarray(bg["H [1/Mpc]"])[o] ** 2
    om = rs / H2
    xk2 = (rs + ps) / 2 / H2               # kinetic part x^2: the phi-MDE quantity ("field kinetic, V negligible")
    for amid in (0.005, 0.01, 0.02, 0.05, 0.1):
        res[f"V3_Omega_phi_at_a={amid}"] = float(np.interp(np.log(amid), lna, om))
        res[f"V3_kinetic_x2_at_a={amid}"] = float(np.interp(np.log(amid), lna, xk2))
    res["V3_target_2b2over3"] = 2 * beta ** 2 / 3
    fc = pars["omega_cdm"] / (pars["omega_cdm"] + pars["omega_b"])
    res["cdm_fraction_fc"] = fc
    res["V3_target_2b2fc2over3"] = 2 * beta ** 2 * fc ** 2 / 3
    res["phi_today_minus_ini"] = float(phi[-1] - phi[0])
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    if sys.argv[1] == "chi2":
        chi2(sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 0.0)
    else:
        background(float(sys.argv[2]) if len(sys.argv) > 2 else 0.1, "nobaryons" in sys.argv)
