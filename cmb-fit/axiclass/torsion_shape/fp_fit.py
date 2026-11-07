# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights.
"""FP fits (PREREGISTRATION_SINH.md, locked 26 Oct): the Fingerprint and the plain cosine, run identically.
    python fp_fit.py fp_cosine      plain cosine, free EDE (f_EDE, z_c, theta_i), option off
    python fp_fit.py fp_sinh        same, with axion_sinh_x0 = 2.1445 (x0 = arsinh(1/0.2375), fixed by the rule)
    python fp_fit.py score          applies the locked rule -> fp_score.json
Data as the rule states: Planck 2018 (low-l TT, EE, plik-lite TTTEEE, lensing) + DESI DR2 BAO + Pantheon+, no SH0ES.
Same free parameters for both shapes. Both run on the Fingerprint build (option off = original code, regress_sinh.py)
and only start if fp_regress.json passed. chi2_eff = chi2 + ((A_planck - 1)/0.0025)^2, as in the reference fits.
Deviation (FP_DEVIATIONS.md): the rule's number 2427.80 came from an unconverged, since-withdrawn run, so the plain
cosine is refitted on the same engine and settings; the locked reference is reported beside it."""
import glob
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
AXI = os.path.dirname(HERE)
sys.path.insert(0, AXI)
BLD = os.environ.get("TWIST_BUILDS", os.path.expanduser("~"))
RES = os.environ.get("TWIST_RESULTS", os.path.join(os.path.dirname(AXI), "results"))
X0 = 2.1445
LOCKED_REF = 2427.80
BEST_OF = 4


def info(name):
    import early_late_spa as E
    extra = dict(E.BASE_ARGS, **E.EDE_ARGS)
    if name == "fp_sinh":
        extra["axion_sinh_x0"] = X0
    P = E.P
    params = {
        "logA": dict(P(2.5, 3.5, 3.055, 0.003), drop=True),
        "A_s": {"value": "lambda logA: 1e-10*np.exp(logA)"},
        "n_s": P(0.85, 1.1, 0.975, 0.003),
        "theta_s_1e2": dict(P(1.03, 1.05, 1.0412, 0.0002), drop=True),
        "100*theta_s": {"value": "lambda theta_s_1e2: theta_s_1e2", "derived": False},
        "omega_b": P(0.019, 0.026, 0.0225, 0.00008),
        "omega_cdm": P(0.09, 0.16, 0.124, 0.0008),
        "tau_reio": P(0.02, 0.12, 0.057, 0.004),
        "fraction_axion_ac": P(0.001, 0.3, 0.07, 0.006),
        "log10_axion_ac": P(-4.3, -3.0, -3.55, 0.05, r"\log_{10} a_c"),
        "theta_i_scf": P(0.1, 3.1, 2.75, 0.04, r"\theta_i"),
        "H0": {"latex": "H_0"}, "sigma8": {"latex": r"\sigma_8"}, "Omega_m": {"latex": r"\Omega_m"},
    }
    likes = {"planck_2018_lowl.TT": None, "planck_2018_lowl.EE": None,
             "planck_2018_highl_plik.TTTEEE_lite_native": None, "planck_2018_lensing.native": None,
             "bao.desi_dr2.desi_bao_all": None, "sn.pantheonplus": None}
    return {"theory": {"classytwist": {"external": E._theory_class(), "extra_args": extra, "ignore_obsolete": True}},
            "likelihood": likes, "params": params, "packages_path": E.PACKAGES,
            "sampler": {"minimize": {"method": "bobyqa", "best_of": BEST_OF}},
            "output": f"{RES}/chains/cmp_{name}", "resume": False, "force": True}


def fit(name):
    gate = os.path.join(HERE, "fp_regress.json")
    if not (os.path.exists(gate) and json.load(open(gate)).get("pass")):
        sys.exit("FP gate not passed: run build_sinh.sh and regress_sinh.py first")
    build = os.path.join(BLD, "AxiCLASS_sinh/python/build")
    sys.path.insert(0, glob.glob(build + "/lib*")[0])
    import classy
    assert classy.__file__.startswith(build), classy.__file__
    from cobaya import run
    t = time.time()
    run(info(name))
    lines = open(f"{RES}/chains/cmp_{name}.minimum.txt").read().splitlines()
    row = {k: float(v) for k, v in zip(lines[0].lstrip("#").split(), lines[1].split())}
    json.dump({"run": name, "engine": "AxiCLASS (Fingerprint build)", "seconds": time.time() - t, "minimum": row},
              open(f"{RES}/cmp_{name}.json", "w"), indent=2)
    print("done", name, row.get("chi2"))


def chi2_eff(m):
    return m["chi2"] + ((m.get("A_planck", 1.0) - 1) / 0.0025) ** 2


def score():
    def load(n):
        p = f"{RES}/cmp_{n}.json"
        return json.load(open(p))["minimum"] if os.path.exists(p) else None
    s, c = load("fp_sinh"), load("fp_cosine")
    out = {"rule": "PREREGISTRATION_SINH.md (locked 2026-10-26 16:10)"}
    if s is None or c is None:
        out["verdict"] = "pending"
    else:
        d = chi2_eff(s) - chi2_eff(c)
        out.update({"chi2_eff_sinh": chi2_eff(s), "chi2_eff_cosine_same_engine": chi2_eff(c), "delta": d,
                    "verdict": ("data prefer the torsion-derived (sinh) shape" if d < -2 else
                                "data cannot tell the shapes apart yet" if d <= 2 else
                                "data disfavour the periodic-in-gamma shape"),
                    "coupling_reading (7 Nov)": ("favours Holst over Nieh-Yan" if d < -2 else
                                                 "no preference between couplings" if d <= 2 else
                                                 "favours Nieh-Yan (plain cosine)"),
                    "locked_reference_2427.80_delta": chi2_eff(s) - LOCKED_REF,
                    "note": "The 2427.80 reference is from a withdrawn, unconverged run; the same-engine delta decides."})
    json.dump(out, open(os.path.join(HERE, "fp_score.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    (score if sys.argv[1] == "score" else lambda: fit(sys.argv[1]))()
