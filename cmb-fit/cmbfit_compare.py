# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under THE AEGIS PEOPLE'S LICENSE (see LICENSE in the AEGIS repository): free for people; no AI use; no military, surveillance or harmful use. AEGIS-ID: 88a710722a5e849d
"""Same-data model comparison (Planck 2018 + DESI DR2 + Pantheon+, no SH0ES), CAMB + Cobaya.

  python cmbfit_compare.py <lcdm|wcdm|ede|edelock>   one best fit (bobyqa), writes results/cmp_<name>.json
  python cmbfit_compare.py report                    table with chi2, dAIC, dBIC vs LCDM

edelock = Twist-2: switch-on locked to matter-radiation equality (PREREGISTRATION_ZEQ.md formula).
Written 28 Oct 2026 after seeing earlier fits, so the lock result is NOT blind.
"""
import copy, glob, json, os, sys, time
import numpy as np
import cmbfit as C

EXTRA_SETTINGS = {"lcdm": 0, "wcdm": 1, "ede": 3, "edelock": 2, "lcdm8": 0, "edelock8": 2, "ede8": 3,
                  "lcdmP": 0, "edelockP": 2, "edeP": 3}
PACT = {"pact_lcdm": 0, "pact_edelock": 2, "pact_ede": 3}     # blind test: same rule, new data (see make)
SPT = {"spt_lcdm": 0, "spt_edelock": 2, "spt_edelock_F9": 1, "spt_edelock_th2.41421_F9": 0,   # SPT-3G pre-registrations
       "spt_edelock_th2.78_F9": 0}                            # last one: contrast at the Planck angle, NOT a prediction
N_DATA = 1994  # approximate; see dossier

LOCK = ("lambda ombh2, omch2: np.log10((ombh2 + omch2) / (2.4728e-5 * (1 + 0.22711 * 3.044)) - 1)")

# Polish / profile / P-ACT starting points. CAMB at the AxiCLASS best EDE point scores better than CAMB's own
# bobyqa minima (engine_check.py), so every model is re-polished from its best known point, with the same settings.
START_LCDM = dict(logA=3.053158, ns=0.97051, theta_s_100=1.041361, ombh2=0.02253, omch2=0.117788, tau=0.060734)
START_EDE = dict(logA=3.05766, ns=0.98053, theta_s_100=1.040924, ombh2=0.0226097, omch2=0.1260421, tau=0.055346,
                 fde_zc=0.0783, log10_zc=3.5533, theta_i=2.7887)
SCALE = dict(logA=0.003, ns=0.003, theta_s_100=0.0002, ombh2=0.00008, omch2=0.0008, tau=0.004,
             fde_zc=0.006, log10_zc=0.02, theta_i=0.04, A_act=0.003, P_act=0.01, Tcal=0.003, Ecal=0.005)


def _start_near(info, start):
    for k, v in start.items():
        if k in info["params"] and isinstance(info["params"][k], dict) and "prior" in info["params"][k]:
            info["params"][k]["ref"] = {"dist": "norm", "loc": v, "scale": SCALE[k]}


def _pact(info):
    """P-ACT, ACT DR6's own baseline: Planck PR3 high-l cut at the ACT overlap (TT<1000, TE/EE<600) + ACT DR6
    CMB-only (l 600-6500) + Planck low-l + ACT DR6 x Planck PR4 lensing + DESI DR2 + Pantheon+."""
    L = info["likelihood"]
    for k in ("planck_2018_highl_plik.TTTEEE_lite_native", "planck_2018_lensing.native"):
        L.pop(k)
    L["act_dr6_cmbonly.PlanckActCut"] = None
    L["act_dr6_cmbonly.ACTDR6CMBonly"] = None
    L["act_dr6_lenslike.ACTDR6LensLike"] = {"variant": "actplanck_baseline", "lens_only": False, "lmax": 4000}
    info["theory"]["camb"]["extra_args"].update(lens_potential_accuracy=4, lAccuracyBoost=1.2,
                                                lSampleBoost=1.0, AccuracyBoost=1.0, kmax=10)
    info["prior"] = {"cal_dip_prior": "lambda A_act: stats.norm.logpdf(A_act, loc=1.0, scale=0.003)"}  # ACT's own
    for k, lo, hi in (("A_act", 0.5, 1.5), ("P_act", 0.9, 1.1)):
        info["params"][k] = {"prior": {"min": lo, "max": hi}, "ref": {"dist": "norm", "loc": 1.0, "scale": SCALE[k]},
                             "proposal": SCALE[k]}


def _spt(info):
    """SPT-3G D1 TT/TE/EE as the only CMB data (PREREGISTRATION_SPT3G_N9.md / _SILVER.md in CubeMind): the 'lite'
    (foreground-marginalised) candl likelihood from spt_candl_data, with SPT's own template settings: Gaussian tau prior
    N(0.051, 0.006) standing in for Planck low-l EE, Tcal/Ecal calibrations, Tcal ~ N(1, 0.0036). + DESI DR2 + Pantheon+."""
    import candl.interface
    import spt_candl_data
    L = info["likelihood"]
    for k in ("planck_2018_lowl.TT", "planck_2018_lowl.EE", "planck_2018_highl_plik.TTTEEE_lite_native",
              "planck_2018_lensing.native"):
        L.pop(k)
    L["spt3g_d1_tne_lite"] = {"external": candl.interface.CandlCobayaLikelihood,
                              "data_set_file": spt_candl_data.SPT3G_D1_TnE, "variant": "lite",
                              "clear_internal_priors": True, "additional_args": {}, "wrapper": None, "feedback": False}
    # SPT's template also sets lens_margin=1250, which CAMB 2.0.5 does not accept; lens accuracy 4 as for P-ACT.
    info["theory"]["camb"]["extra_args"].update(lens_potential_accuracy=4, lAccuracyBoost=1.0,
                                                lSampleBoost=1.0, AccuracyBoost=1.0)
    info["params"]["tau"]["prior"] = {"dist": "norm", "loc": 0.051, "scale": 0.006}
    for k in ("Tcal", "Ecal"):
        info["params"][k] = {"prior": {"min": 0.8, "max": 1.2}, "ref": {"dist": "norm", "loc": 1.0, "scale": SCALE[k]},
                             "proposal": SCALE[k]}
    info["prior"] = {"gaussian_Tcal": "lambda Tcal: stats.norm.logpdf(Tcal, loc=1.0, scale=0.0036)"}


SN_SWAP = {"_desy5": "sn.desy5", "_dovekie": "sn.desdovekie", "_union3": "sn.union3"}   # robustness: other SN sets


def make(name):
    zc_fixed = None
    full, sn, shoes = name, None, False
    fwidth = None
    mcmc_chain = None
    if "_mcmc" in name:                             # MCMC chain K (PREREG_PHASE1.md, step 1.1), e.g. pact_edelock_mcmc2
        name, k = name.split("_mcmc")
        mcmc_chain = int(k or 1)
    import re
    m_f = re.search(r"_F(\d+)$", name)
    if m_f:                                         # field width fixed to torsion/N (PREREG_N_PACT.md; PREREG_PHASE1.md 1.2)
        name, fwidth = name[:m_f.start()], int(m_f.group(1))
    theta_fixed = None
    m_th = re.search(r"_th(\d+(?:\.\d+)?)$", name)
    if m_th:                                        # starting angle fixed, e.g. pact_edelock_th2.41421_F9: lock + width +
        name, theta_fixed = name[:m_th.start()], float(m_th.group(1))   # angle = zero free settings (SPT3G_SILVER prereg)
    n_pow = 3
    m_n = re.search(r"_n(\d)$", name)
    if m_n:                                         # rival potential power, e.g. edelockP_n2_F9 (default n=3 unchanged)
        name, n_pow = name[:m_n.start()], int(m_n.group(1))
    s8 = None
    for suffix in ("_s8A", "_s8B"):                  # add a weak-lensing S8 likelihood (PREREG_S8.md)
        if name.endswith(suffix):
            name, s8 = name[:-len(suffix)], suffix[-1]
    for suffix, like in SN_SWAP.items():            # same fit with another supernova compilation instead of Pantheon+
        if name.endswith(suffix):
            name, sn = name[:-len(suffix)], like
    if name.endswith("_shoes"):                     # same fit with the SH0ES H0 calibration added
        name, shoes = name[:-6], True
    if name.startswith("zc"):                       # z_c profile point, e.g. zc3.45: free EDE with log10 z_c fixed
        zc_fixed, core = float(name[2:]), "edeP"
    elif name.startswith("th"):                     # hilltop test (PREREG_THETA.md): free EDE with theta_i fixed
        core = "edeP"
    elif name.startswith("spt_"):
        core = name[4:]
    else:
        core = name[5:] if name.startswith("pact_") else name
    base = "ede" if core.startswith(("ede", "edelock")) else "lcdm"
    best_of = 8 if core.endswith("8") else 4
    info = C.make_info(base, shoes=shoes,
                       sampler={"minimize": {"method": "bobyqa", "best_of": best_of}},
                       output=os.path.join(C.RESULTS, "chains", "cmp_" + full))
    if sn:
        info["likelihood"].pop("sn.pantheonplus", None)
        info["likelihood"][sn] = None
    if s8:
        import s8like
        info["likelihood"]["s8_" + s8] = {"external": getattr(s8like, "S8" + s8)}
    if fwidth:
        import fwidth as FW
        info["likelihood"][f"fwidth_{fwidth}"] = {"external": getattr(FW, f"FWidth{fwidth}")}
    info["resume"] = True
    extra = info["theory"]["camb"]["extra_args"]
    if n_pow != 3 and base == "ede":
        extra["n"] = n_pow
    if name == "wcdm":
        extra["dark_energy_model"] = "ppf"
        info["params"]["w"] = {"prior": {"min": -2.0, "max": -0.4},
                               "ref": {"dist": "norm", "loc": -1.0, "scale": 0.03},
                               "proposal": 0.03, "latex": "w"}
    if core.startswith("edelock"):
        info["params"]["log10_zc"] = {"value": LOCK, "derived": False}
    if zc_fixed is not None:
        info["params"]["log10_zc"] = {"value": zc_fixed, "drop": True}
    if name.startswith("th"):
        info["params"]["theta_i"] = {"value": float(name[2:])}
    if theta_fixed is not None:
        info["params"]["theta_i"] = {"value": theta_fixed}
    if core.endswith("P") or name.startswith(("pact_", "spt_")):
        _start_near(info, START_EDE if base == "ede" else START_LCDM)
    if name.startswith("pact_"):
        _pact(info)
    if name.startswith("spt_"):
        _spt(info)
    seed = os.environ.get("CMB_START_FROM")         # e.g. zc3.55: start this fit from another run's best point
    if seed:
        p = os.path.join(C.RESULTS, f"cmp_{seed}.json")
        if os.path.exists(p):
            m = json.load(open(p))["minimum"]
            _start_near(info, {k: m[k] for k in SCALE if k in m and k != "log10_zc"})
    if os.environ.get("CMB_BEST_OF"):               # more restarts for a re-check (never fewer than the default)
        info["sampler"]["minimize"]["best_of"] = max(best_of, int(os.environ["CMB_BEST_OF"]))
    if mcmc_chain is not None:                      # independent chain; convergence checked across chains afterwards
        info["sampler"] = {"mcmc": {"Rminus1_stop": 0.02, "Rminus1_cl_stop": 0.2, "learn_proposal": True,
                                    "max_tries": 10000, "seed": 1000 + mcmc_chain, "output_every": "60s"}}
    return info

def _archive_stale(name):
    """Cobaya's minimizer cannot resume: if an earlier attempt left files but no .minimum, move them aside
    (archived, never deleted) so the run starts clean instead of failing."""
    import shutil
    prefix = os.path.join(C.RESULTS, "chains", "cmp_" + name)
    left = glob.glob(prefix + ".*")
    if left and not os.path.exists(prefix + ".minimum"):
        dest = os.path.join(C.RESULTS, "chains", "_stale", time.strftime("%Y%m%d_%H%M%S") + "_" + name)
        os.makedirs(dest, exist_ok=True)
        for f in left:
            shutil.move(f, dest)
        print("archived stale files of", name, "to", dest, flush=True)


def run_one(name):
    from cobaya import run
    t0 = time.time()
    if "_mcmc" in name:                             # chains resume by themselves; never archive them
        upd, sampler = run(make(name))
        json.dump(dict(run=name, seconds=time.time() - t0, kind="mcmc",
                       chain=os.path.join(C.RESULTS, "chains", "cmp_" + name)),
                  open(os.path.join(C.RESULTS, f"cmp_{name}.json"), "w"), indent=2)
        print("done", name, flush=True)
        return
    _archive_stale(name)
    upd, sampler = run(make(name))
    row = {k: float(v) for k, v in sampler.products()["minimum"].data.iloc[0].items()
           if isinstance(v, (int, float, np.integer, np.floating))}
    json.dump(dict(run=name, seconds=time.time() - t0, minimum=row),
              open(os.path.join(C.RESULTS, f"cmp_{name}.json"), "w"), indent=2)
    print("done", name, row.get("H0"), row.get("chi2"), flush=True)

def _table(models, ref_names, title):
    rows = {}
    for n in models:
        p = os.path.join(C.RESULTS, f"cmp_{n}.json")
        if os.path.exists(p):
            m = json.load(open(p))["minimum"]
            rows[n] = (m.get("chi2", float("nan")), C.chi2_eff(m), m.get("H0", float("nan")))
    out = [f"### {title}", "", "| Model | extra | chi2 | dchi2 | dAIC | dBIC | dchi2_eff | dAIC_eff | H0 |",
           "|---|---|---|---|---|---|---|---|---|"]
    refs = [n for n in ref_names if n in rows]
    ref = min(refs, key=lambda n: rows[n][0]) if refs else None
    for n, (c, ce, h) in rows.items():
        k = models[n]
        d = c - rows[ref][0] if ref else float("nan")
        de = ce - rows[ref][1] if ref else float("nan")
        out.append(f"| {n} | {k} | {c:.2f} | {d:+.2f} | {d + 2 * k:+.2f} | {d + k * np.log(N_DATA):+.2f} | "
                   f"{de:+.2f} | {de + 2 * k:+.2f} | {h:.2f} |")
    return out, (rows[ref][0] if ref else None)


def report():
    """Both scores the pre-registration asks for: likelihood-only chi2, and chi2_eff (adds the Planck calibration
    prior A_planck ~ N(1, 0.0025)). dAIC/dBIC use chi2; the _eff columns repeat dchi2/dAIC with chi2_eff.
    Each table is measured against the best ΛCDM on the same data (any number of restarts)."""
    out, ref = _table(EXTRA_SETTINGS, ("lcdm", "lcdm8", "lcdmP"), "Planck 2018 + DESI DR2 + Pantheon+")
    t2, _ = _table(PACT, ("pact_lcdm",), "P-ACT (Planck cut + ACT DR6 + ACT×PR4 lensing) + DESI DR2 + Pantheon+: blind test")
    out += [""] + t2
    if any(os.path.exists(os.path.join(C.RESULTS, f"cmp_{n}.json")) for n in SPT):
        t4, _ = _table(SPT, ("spt_lcdm",), "SPT-3G D1 TT/TE/EE (lite) + tau prior + DESI DR2 + Pantheon+: "
                                            "pre-registered tests (CubeMind PREREGISTRATION_SPT3G_N9.md, _SILVER.md)")
        out += [""] + t4
    for suffix, title in (("_desy5", "Planck 2018 + DESI DR2 + DES Y5 supernovae (instead of Pantheon+)"),
                          ("_dovekie", "Planck 2018 + DESI DR2 + DES-Dovekie supernovae (instead of Pantheon+)"),
                          ("_union3", "Planck 2018 + DESI DR2 + Union3 supernovae (instead of Pantheon+)"),
                          ("_shoes", "Planck 2018 + DESI DR2 + Pantheon+ with SH0ES (uses the local H0)"),
                          ("_s8A", "Planck 2018 + DESI DR2 + Pantheon+ + weak-lensing S8 (A: DES Y3+KiDS-1000)"),
                          ("_s8B", "Planck 2018 + DESI DR2 + Pantheon+ + weak-lensing S8 (B: KiDS-Legacy)")):
        group = {n + suffix: k for n, k in EXTRA_SETTINGS.items()}
        if any(os.path.exists(os.path.join(C.RESULTS, f"cmp_{n}.json")) for n in group):
            t3, _ = _table(group, tuple(n + suffix for n in ("lcdm", "lcdm8", "lcdmP")), title)
            out += [""] + t3
    prof = []
    for p in glob.glob(os.path.join(C.RESULTS, "cmp_zc*.json")):
        m = json.load(open(p))["minimum"]
        prof.append((float(os.path.basename(p)[6:-5]), m["chi2"], m.get("fde_zc"), m.get("H0")))
    if prof:
        out += ["", "### z_c profile (free EDE, log10 z_c fixed; Δχ² vs best ΛCDM above)", "",
                "| log10 z_c | z_c | chi2 | dchi2 | f_EDE | H0 |", "|---|---|---|---|---|---|"]
        for z, c, f, h in sorted(prof):
            out.append(f"| {z:.2f} | {10 ** z:.0f} | {c:.2f} | {c - ref:+.2f} | {f:.3f} | {h:.2f} |")
    txt = "\n".join(out)
    open(os.path.join(C.RESULTS, "COMPARE.md"), "w", encoding="utf-8").write(txt)
    print(txt)

if __name__ == "__main__":
    C.lower_priority()
    for arg in sys.argv[1:]:
        try:
            report() if arg == "report" else run_one(arg)
        except Exception as e:                       # one failed fit must not stop an overnight queue
            print("FAILED", arg, repr(e), flush=True)
