# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under THE AEGIS PEOPLE'S LICENSE (see LICENSE in the AEGIS repository): free for people; no AI use; no military, surveillance or harmful use.
"""Cross-engine check on P-ACT (PREREG_PHASE1.md step 1.3, at the best points; not a re-minimisation).

Evaluates AxiCLASS (exact Klein-Gordon scalar field, classy) at the CAMB best points of pact_lcdm, pact_edelock and
pact_edelock_F9, with the same P-ACT + DESI DR2 + Pantheon+ likelihoods, and compares dchi2 (EDE - LCDM) between the
two engines, so engine offsets cancel as in engine_check.py. Runs inside WSL (micromamba env 'aegis'):

    python /mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass/cross_engine_pact.py

H0 is passed directly from CAMB's best point (rather than theta_*), so both engines describe the same cosmology.
"""
import json
import math
import os

from cobaya.model import get_model

ROOT = "/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit"
PACKAGES = ROOT + "/packages"

LIKES = {
    "planck_2018_lowl.TT": None,
    "planck_2018_lowl.EE": None,
    "act_dr6_cmbonly.PlanckActCut": None,
    "act_dr6_cmbonly.ACTDR6CMBonly": None,
    "act_dr6_lenslike.ACTDR6LensLike": {"variant": "actplanck_baseline", "lens_only": False, "lmax": 4000},
    "bao.desi_dr2.desi_bao_all": None,
    "sn.pantheonplus": None,
}
EDE_ARGS = {"do_shooting": "yes", "do_shooting_scf": "yes", "scf_potential": "axion", "n_axion": 3,
            "security_small_Omega_scf": 0.001, "n_axion_security": 2.09, "use_big_theta_scf": "yes",
            "scf_has_perturbations": "yes", "attractor_ic_scf": "no", "scf_tuning_index": 0}
# (AxiCLASS's old cobaya template also set precision_newton_method_F/x; the current AxiCLASS rejects them.)
BASE_ARGS = {"N_ncdm": 1, "m_ncdm": 0.06, "N_ur": 2.0328, "non_linear": "hmcode", "l_max_scalars": 9000}


def evaluate(name):
    m = json.load(open(f"{ROOT}/results/cmp_{name}.json"))["minimum"]
    ede = "edelock" in name
    params = {"A_s": m["As"], "n_s": m["ns"], "H0": m["H0"], "omega_b": m["ombh2"], "omega_cdm": m["omch2"],
              "tau_reio": m["tau"], "A_act": m["A_act"], "P_act": m["P_act"]}
    if "A_planck" in m:
        params["A_planck"] = m["A_planck"]
    extra = dict(BASE_ARGS)
    if ede:
        extra.update(EDE_ARGS)
        extra["scf_parameters"] = f"{m['theta_i']}, 0."      # starting angle, initial velocity
        params["fraction_axion_ac"] = m["fde_zc"]          # current AxiCLASS refuses the old log10_ input
        params["log10_axion_ac"] = math.log10(1.0 / (1.0 + m["zc"]))
    # AxiCLASS is a modified CLASS (reports v3.3.0), so Cobaya's minimum-version check is switched off, as it advises.
    info = {"theory": {"classy": {"extra_args": extra, "ignore_obsolete": True}}, "likelihood": LIKES,
            "packages_path": PACKAGES,
            "params": {k: {"value": v} for k, v in params.items()}}
    model = get_model(info)
    lp = model.loglikes({})[0]
    names = list(model.likelihood)
    chi2 = {n: float(-2 * v) for n, v in zip(names, lp)}
    camb_chi2 = {k[len("chi2__"):]: v for k, v in m.items() if k.startswith("chi2__") and "fwidth" not in k
                 and k[len("chi2__"):] in names}
    return chi2, camb_chi2


if __name__ == "__main__":
    res = {}
    for n in ("pact_lcdm", "pact_edelock", "pact_edelock_F9"):
        try:
            res[n] = evaluate(n)
            print(n, "AxiCLASS total %.2f  CAMB total %.2f" % (sum(res[n][0].values()), sum(res[n][1].values())),
                  flush=True)
        except Exception as e:
            print(n, "FAILED", repr(e), flush=True)
    if "pact_lcdm" in res:
        for n in ("pact_edelock", "pact_edelock_F9"):
            if n in res:
                da = sum(res[n][0].values()) - sum(res["pact_lcdm"][0].values())
                dc = sum(res[n][1].values()) - sum(res["pact_lcdm"][1].values())
                print(f"{n}: dchi2 vs LCDM  AxiCLASS {da:+.2f}  CAMB {dc:+.2f}  difference {da - dc:+.2f}"
                      f"  -> {'AGREE (<0.5)' if abs(da - dc) < 0.5 else 'DIFFER (>=0.5)'}", flush=True)
    json.dump({n: {"axiclass": r[0], "camb": r[1]} for n, r in res.items()},
              open(f"{ROOT}/results/cross_engine_pact.json", "w"), indent=2)
