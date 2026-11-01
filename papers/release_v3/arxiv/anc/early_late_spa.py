# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights.
"""ROUTE.md A3: early AND late together, on Planck + ACT + SPT-3G + DESI DR2 + Pantheon+, all in AxiCLASS
(CubeMind PREREGISTRATION_EARLY_LATE.md). CAMB cannot run its early-quintessence field and a w0-wa fluid at once;
AxiCLASS (CLASS) can: the twist field is the scalar field, late dark energy is a w0-wa fluid (PPF).

Four models, same engine, same settings (bobyqa, best of 4), so engine offsets cancel:
    ax_spa_lcdm, ax_spa_w0wa, ax_spa_edelock, ax_spa_edelock_w0wa
Runs inside WSL (micromamba env 'aegis'):
    python .../axiclass/early_late_spa.py <name>        -> results/cmp_<name>.json
    python .../axiclass/early_late_spa.py smoke         -> builds all four, prints finite/not only
"""
import json
import math
import os
import re
import sys
import time

ROOT = "/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit"
PACKAGES = ROOT + "/packages"
OUT = ROOT + "/results"

LOCK = "lambda omega_b, omega_cdm: np.log10(2.4728e-5 * (1 + 0.22711 * 3.044) / (omega_b + omega_cdm))"
BASE_ARGS = {"N_ncdm": 1, "m_ncdm": 0.06, "N_ur": 2.0328, "non_linear": "hmcode", "l_max_scalars": 9000}
EDE_ARGS = {"do_shooting": "yes", "do_shooting_scf": "yes", "scf_potential": "axion", "n_axion": 3,
            "security_small_Omega_scf": 0.001, "n_axion_security": 2.09, "use_big_theta_scf": "yes",
            "scf_has_perturbations": "yes", "attractor_ic_scf": "no", "scf_tuning_index": 0}


def _theory_class():
    """This AxiCLASS build ignores scf_theta_ini_cobaya; it only takes the starting angle as the text
    'scf_parameters = theta, 0.'. Cobaya samples theta_i_scf; this wrapper turns it into that text each step."""
    from cobaya.theories.classy import classy as _classy

    class ClassyTwist(_classy):
        def set(self, params_values_dict):
            p = dict(params_values_dict)
            if "theta_i_scf" in p:
                self.extra_args["scf_parameters"] = f"{p.pop('theta_i_scf')}, 0."
            super().set(p)
    return ClassyTwist


def P(lo, hi, loc, scale, latex=None):
    d = {"prior": {"min": lo, "max": hi}, "ref": {"dist": "norm", "loc": loc, "scale": scale}, "proposal": scale}
    if latex:
        d["latex"] = latex
    return d


CAMB2CLASS = {"logA": "logA", "ns": "n_s", "theta_s_100": "theta_s_1e2", "ombh2": "omega_b", "omch2": "omega_cdm",
              "tau": "tau_reio", "A_act": "A_act", "P_act": "P_act", "Tcal": "Tcal", "Ecal": "Ecal",
              "fde_zc": "fraction_axion_ac", "theta_i": "theta_i_scf", "w": "w0_fld", "wa": "wa_fld"}


def _start_from_camb(params, early, late):
    """Start each restart near the CAMB best point of the same model on the same data (spa_*), to cut AxiCLASS run
    time (~16 s per evaluation). Only the 'ref' centre moves; priors are unchanged. The early+late model takes the
    early parameters from spa_edelock and w0, wa from spa_w0wa."""
    srcs = (["spa_edelock"] if early else ["spa_lcdm"]) + (["spa_w0wa"] if late else [])
    for s in srcs:
        m = json.load(open(f"{OUT}/cmp_{s}.json"))["minimum"]
        for ck, xk in CAMB2CLASS.items():
            if s == "spa_w0wa" and early and ck not in ("w", "wa"):
                continue
            if ck in m and xk in params and "ref" in params[xk]:
                params[xk]["ref"]["loc"] = float(m[ck])


def make(name):
    import candl.interface
    import spt_candl_data
    # CubeMind PREREGISTRATION_ROBUSTNESS.md suffixes: _b4 = best of 4 restarts (R1), _desy5 = DES Y5 SNe (R2).
    best_of = 4 if name.endswith("_b4") else 2
    desy5 = "_desy5" in name
    dovekie = "_dovekie" in name                    # CubeMind PREREGISTRATION_DOVEKIE.md (corrected DES sample)
    base = name.replace("_b4", "").replace("_desy5", "").replace("_dovekie", "")
    early = "edelock" in base
    late = "w0wa" in base
    latetwist = "latetwist" in base                 # CubeMind PREREGISTRATION_LATE_TWIST.md
    # CubeMind PREREGISTRATION_COUPLED_TWIST.md: the Late Twist plus a CDM coupling beta (needs the coupled build,
    # see run()). "_beta<x>" fixes beta (C5 and the beta profile); otherwise beta is free in [-0.15, 0.15].
    coupled = "coupledtwist" in base
    fixed_beta = re.search(r"_beta(-?[0-9.]+)", base)
    # (F, m) profile grid (deviation 08:58): "_gF<log10 F>m<log10 m>" fixes F and m; only the standard parameters
    # (and beta, if free) are minimised.
    grid = re.search(r"_gF(-?[0-9.]+)m(-?[0-9.]+)", base)
    latetwist = latetwist or coupled
    extra = dict(BASE_ARGS)
    if latetwist or base.endswith("_halofit"):
        # HMcode in this AxiCLASS refuses a scalar field present today ("not yet coded"), so the Late Twist and its
        # reference runs (ax_spa_lcdm_halofit, ax_spa_w0wa_halofit) all use halofit (PREREGISTRATION_LATE_TWIST deviation).
        extra["non_linear"] = "halofit"
    params = {
        "logA": dict(P(2.5, 3.5, 3.055, 0.003), drop=True),
        "A_s": {"value": "lambda logA: 1e-10*np.exp(logA)"},
        "n_s": P(0.85, 1.1, 0.975 if early else 0.968, 0.003),
        "theta_s_1e2": dict(P(1.03, 1.05, 1.0412, 0.0002), drop=True),
        "100*theta_s": {"value": "lambda theta_s_1e2: theta_s_1e2", "derived": False},
        "omega_b": P(0.019, 0.026, 0.0225, 0.00008),
        "omega_cdm": P(0.09, 0.16, 0.124 if early else 0.118, 0.0008),
        "tau_reio": P(0.02, 0.12, 0.057, 0.004),
        "A_act": P(0.5, 1.5, 1.0, 0.003), "P_act": P(0.9, 1.1, 1.0, 0.01),
        "Tcal": P(0.8, 1.2, 1.0, 0.003), "Ecal": P(0.8, 1.2, 1.0, 0.005),
        "H0": {"latex": "H_0"}, "sigma8": {"latex": r"\sigma_8"}, "Omega_m": {"latex": r"\Omega_m"},
    }
    if early:
        extra.update(EDE_ARGS)
        params["fraction_axion_ac"] = P(0.001, 0.3, 0.07, 0.006)
        params["log10_axion_ac"] = {"value": LOCK, "derived": False}       # the lock: peak at equality
        params["theta_i_scf"] = P(0.1, 3.1, 2.75, 0.04, r"\theta_i")
    prior = {"cal_dip_prior": "lambda A_act: stats.norm.logpdf(A_act, loc=1.0, scale=0.003)",
             "gaussian_Tcal": "lambda Tcal: stats.norm.logpdf(Tcal, loc=1.0, scale=0.0036)"}
    if late:
        extra.update({"Omega_Lambda": 0.0, "use_ppf": "yes",              # w0-wa fluid takes the closure;
                      "fluid_equation_of_state": "CLP"})                    # this build reads w0/wa only with CLP
        params["w0_fld"] = P(-3.0, 1.0, -0.84, 0.05)
        params["wa_fld"] = P(-3.0, 2.0, -0.6, 0.1)
        prior["w0wa_bound"] = "lambda w0_fld, wa_fld: 0.0 if w0_fld + wa_fld < 0 else -np.inf"
    if latetwist:
        # Late Twist: n = 1 cosine, all the dark energy (no Lambda); the starting angle is tuned for closure.
        extra.update({"scf_potential": "axion", "n_axion": 1, "scf_has_perturbations": "yes",
                      "attractor_ic_scf": "no", "scf_evolve_as_fluid": "no", "do_shooting": "yes",
                      "do_shooting_scf": "yes", "Omega_Lambda": 0, "Omega_fld": 0, "Omega_scf": -1,
                      "scf_tuning_index": 0, "scf_parameters": "1.5, 0."})
        if grid:
            extra["f_axion"] = 10 ** float(grid.group(1))
            extra["m_axion"] = 10 ** float(grid.group(2))
        else:
            params["log10_F"] = dict(P(-1.3, 0.5, 0.0, 0.05, r"\log_{10} F/M_{\rm Pl}"), drop=True)
            params["log10_m"] = dict(P(-0.5, 1.5, 0.3, 0.05, r"\log_{10} m/H_0"), drop=True)
            params["f_axion"] = {"value": "lambda log10_F: 10**log10_F", "derived": False}
            params["m_axion"] = {"value": "lambda log10_m: 10**log10_m", "derived": False}
    if coupled:
        if fixed_beta:
            extra["scf_coupling_beta"] = float(fixed_beta.group(1))
        else:
            params["scf_coupling_beta"] = P(-0.15, 0.15, 0.0, 0.02, r"\beta")
    likes = {
        "planck_2018_lowl.TT": None, "planck_2018_lowl.EE": None,
        "act_dr6_cmbonly.PlanckActCut": None, "act_dr6_cmbonly.ACTDR6CMBonly": None,
        "act_dr6_lenslike.ACTDR6LensLike": {"variant": "actplanck_baseline", "lens_only": False, "lmax": 4000},
        "spt3g_d1_tne_lite": {"external": candl.interface.CandlCobayaLikelihood,
                              "data_set_file": spt_candl_data.SPT3G_D1_TnE, "variant": "lite",
                              "clear_internal_priors": True, "additional_args": {}, "wrapper": None,
                              "feedback": False},
        "bao.desi_dr2.desi_bao_all": None,
        ("sn.desy5" if desy5 else "sn.desdovekie" if dovekie else "sn.pantheonplus"): None,
    }
    _start_from_camb(params, early, late)
    if latetwist:
        # Rerun deviation (PREREGISTRATION_SPT3G_DEVIATIONS.md): start from the AxiCLASS LCDM halofit best fit, not the
        # CAMB one (CAMB's theta is a different quantity); F, m references and all priors unchanged; best of 4.
        best_of = 2 if grid else 4          # grid points minimise only smooth standard parameters
        m = json.load(open(f"{OUT}/cmp_ax_spa_lcdm_halofit.json"))["minimum"]
        for k, p in params.items():
            if k in m and isinstance(p, dict) and "ref" in p:
                p["ref"]["loc"] = float(m[k])
    return {"theory": {"classytwist": {"external": _theory_class(), "extra_args": extra, "ignore_obsolete": True}},
            "likelihood": likes,
            "params": params, "prior": prior, "packages_path": PACKAGES,
            "sampler": {"minimize": {"method": "bobyqa", "best_of": best_of}},  # 2 for all A3 / Late Twist models
            "output": f"{OUT}/chains/cmp_{name}", "resume": False, "force": True}


def smoke():
    import copy
    from cobaya.model import get_model
    for n in (sys.argv[2:] or ("ax_spa_lcdm", "ax_spa_w0wa", "ax_spa_edelock", "ax_spa_edelock_w0wa")):
        _maybe_coupled(n)
        info = copy.deepcopy(make(n))
        for k in ("sampler", "output", "resume", "force"):
            info.pop(k, None)
        t = time.time()
        try:
            m = get_model(info)
            sp = m.parameterization.sampled_params()
            ok = math.isfinite(m.logposterior(dict(zip(sp, m.prior.reference(random_state=1)))).logpost)
        except Exception as e:
            ok = f"ERROR {type(e).__name__}: {str(e)[:160]}"
        print(f"{n:22s} finite: {ok}   ({time.time() - t:.0f} s incl. setup)", flush=True)


def save(name, seconds=None):
    """Write results/cmp_<name>.json from Cobaya's own chains/cmp_<name>.minimum.txt (header row, value row).
    (The minimizer's products() returns a OnePoint object without keys(), which crashed the first A3 save.)"""
    lines = open(f"{OUT}/chains/cmp_{name}.minimum.txt").read().splitlines()
    row = {k: float(v) for k, v in zip(lines[0].lstrip("#").split(), lines[1].split())}
    # Cobaya's own total "chi2" (sum of all likelihoods, priors excluded) is kept as reported.
    json.dump({"run": name, "engine": "AxiCLASS", "seconds": seconds, "minimum": row},
              open(f"{OUT}/cmp_{name}.json", "w"), indent=2)
    print("done", name, row.get("H0"), row.get("chi2"), flush=True)


PENALTY = -1e5
COUPLED_BUILD = "/home/syndyr/AxiCLASS_coupled/python/build"   # coupled/build_coupled.sh


def _maybe_coupled(name):
    """Coupled Twist runs load the coupled AxiCLASS build (coupled/build_coupled.sh), never the installed one."""
    if "coupledtwist" not in name:
        return
    import glob
    sys.path.insert(0, glob.glob(COUPLED_BUILD + "/lib*")[0])
    import classy
    assert classy.__file__.startswith(COUPLED_BUILD), classy.__file__


def _guard_minimizer():
    """Late Twist only (PREREGISTRATION_SPT3G_DEVIATIONS.md, minimiser guard): inside the minimiser, a non-finite or
    absurd log-posterior (closure impossible, or the field overshoots) becomes a flat PENALTY, so bobyqa rejects the
    step instead of overflowing. Installed in run(), after Cobaya has already drawn finite starting points."""
    from cobaya.samplers.minimize.minimize import Minimize
    orig_run = Minimize.run

    def guarded_run(self):
        f = self.logp

        def logp(x):
            v = f(x)
            return v if math.isfinite(v) and v > PENALTY else PENALTY
        self.logp = logp
        return orig_run(self)
    Minimize.run = guarded_run


def run(name):
    from cobaya.run import run as crun
    t = time.time()
    _maybe_coupled(name)
    if "latetwist" in name or "coupledtwist" in name:
        _guard_minimizer()
    crun(make(name))
    save(name, time.time() - t)


if __name__ == "__main__":
    if sys.argv[1] == "smoke":
        smoke()
    elif sys.argv[1] == "save":                     # recover JSONs from finished runs: save <name> [<name> ...]
        for n in sys.argv[2:]:
            save(n)
    else:
        # Atomic claim so two queue workers never run the same fit (run_grid.sh + run_grid_helper.sh). Scheduling only.
        claim = f"{OUT}/lanes/{sys.argv[1]}.claim"
        try:
            fd = os.open(claim, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, f"{os.getpid()} {time.strftime('%F %T')}\n".encode()); os.close(fd)
        except FileExistsError:
            print(f"{sys.argv[1]} is claimed by another worker; skipping", flush=True)
            sys.exit(0)
        run(sys.argv[1])
