"""DESI-MOCK (rule: field_tests/rules/PREREG_DESI_MOCK.md). Asimov mock of DESI DR2 BAO + Pantheon+ + compressed CMB
from the FLAG-1 Pantheon+ best fit, then LCDM and w0waCDM (uncoupled CDM, plain CLASS) fitted to it.
    python desi_mock.py truth   (coupled flagship build; writes truth.json)
    python desi_mock.py fit     (plain AxiCLASS build on PYTHONPATH; writes desi_mock_result.json)"""
import json, os, sys, types
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); AEG = os.path.abspath(os.path.join(HERE, "..", ".."))
D = os.path.join(AEG, "cmb-fit", "packages", "data")
RULE = os.path.join(AEG, "field_tests", "rules", "PREREG_DESI_MOCK.md")
C = 299792.458
bm = np.loadtxt(os.path.join(D, "bao_data", "desi_bao_dr2", "desi_gaussian_bao_ALL_GCcomb_mean.txt"), dtype=str)
BZ, BQ = bm[:, 0].astype(float), bm[:, 2]
BCi = np.linalg.inv(np.loadtxt(os.path.join(D, "bao_data", "desi_bao_dr2", "desi_gaussian_bao_ALL_GCcomb_cov.txt")))
SD = os.path.join(D, "sn_data", "PantheonPlus")
SN = np.genfromtxt(os.path.join(SD, "Pantheon+SH0ES.dat"), names=True, dtype=None, encoding=None)
SC = np.loadtxt(os.path.join(SD, "Pantheon+SH0ES_STAT+SYS.cov"))[1:].reshape(len(SN), len(SN))
m = (SN["zHD"] > 0.01) & (SN["IS_CALIBRATOR"] == 0); SN, SCi = SN[m], np.linalg.inv(SC[np.ix_(m, m)]); ONE = np.ones(len(SN))
CMB_S = np.array([0.00030, 0.00015, 0.0011])


def observables(c, wbc_early=None):
    rd = c.rs_drag(); h = c.h()
    bao = []
    for z, q in zip(BZ, BQ):
        dm = c.angular_distance(z) * (1 + z); dh = C / (c.Hubble(z) * C)
        bao.append({"DM_over_rs": dm / rd, "DH_over_rs": dh / rd, "DV_over_rs": (z * dm * dm * dh) ** (1 / 3) / rd}[q])
    mu = np.array([5 * np.log10(c.angular_distance(zh) * (1 + zh) * (1 + zl)) + 25 for zh, zl in zip(SN["zHD"], SN["zHEL"])])
    th = c.get_current_derived_parameters(["100*theta_star"])["100*theta_star"]
    return np.array(bao), mu, th, rd, h


def truth():
    for n in ("candl", "candl.interface", "spt_candl_data"):
        sys.modules.setdefault(n, types.SimpleNamespace(CandlCobayaLikelihood=None, SPT3G_D1_TnE=None, interface=None))
    sys.modules["candl"].interface = sys.modules["candl.interface"]
    sys.path.insert(0, os.path.join(AEG, "cmb-fit", "axiclass"))
    import early_late_spa as E, spiral_guess
    run = "ax_spa_spiraltwist_kappa1_nlfix"; E._maybe_coupled(run); import classy
    info = E.make(run); st = json.load(open(f"{E.OUT}/cmp_{run}_s8y6.json"))["minimum"]
    a = dict(info["theory"]["classytwist"]["extra_args"])
    a.update({"A_s": 1e-10 * np.exp(st["logA"]), "n_s": st["n_s"], "100*theta_s": st["theta_s_1e2"], "omega_b": st["omega_b"],
              "omega_cdm": st["omega_cdm"], "tau_reio": st["tau_reio"], "output": "mPk"})
    for k in ("lensing", "l_max_scalars", "non_linear"): a.pop(k, None)
    b = st["scf_coupling_beta"]; a["scf_coupling_beta"] = b
    a["scf_parameters"] = f"1.0, 0.0, {spiral_guess.mu1_guess(1.0, b, st['omega_b'], st['omega_cdm'])}, 0.0, 0.0, 0.0"
    c = classy.Class(); c.set(a); c.compute()
    bao, mu, th, rd, h = observables(c)
    bg = c.get_background(); zz = bg["z"][::-1]; rc = bg["(.)rho_cdm"][::-1]
    wc_early = float(np.interp(1090, zz, rc)) / 1091 ** 3 / (100 / C) ** 2
    out = {"run": run, "h": h, "omega_b": st["omega_b"], "omega_cdm_today": st["omega_cdm"], "omega_c_early": wc_early,
           "theta_star_100": th, "rd": rd, "bao": bao.tolist(), "mu": mu.tolist(),
           "cmb": [th, st["omega_b"], st["omega_b"] + wc_early]}
    json.dump(out, open(os.path.join(HERE, "truth.json"), "w"), indent=1)
    print({k: v for k, v in out.items() if k not in ("bao", "mu")})


def fit(only=None):
    assert os.path.exists(RULE + ".sha256"), "rule not locked"
    import classy
    from scipy.optimize import minimize
    T = json.load(open(os.path.join(HERE, "truth.json"))); TB, TMU, TC = np.array(T["bao"]), np.array(T["mu"]), np.array(T["cmb"])
    base = {"N_ur": 2.0328, "N_ncdm": 1, "m_ncdm": 0.06, "tau_reio": 0.06, "output": ""}

    def chi2(p, w0wa, parts=False, use_sn=True):
        h, wb, wc = p[:3]
        a = dict(base, h=h, omega_b=wb, omega_cdm=wc)
        if w0wa:
            a.update({"Omega_Lambda": 0, "fluid_equation_of_state": "CLP", "w0_fld": p[3], "wa_fld": p[4], "use_ppf": "yes", "cs2_fld": 1})
            if not (-3 < p[3] < 1 and -3 < p[4] < 2):
                return 1e10
        try:
            c = classy.Class(); c.set(a); c.compute()
            bao, mu, th, rd, _ = observables(c); c.struct_cleanup()
        except Exception:
            return 1e10
        rb = TB - bao; cb = rb @ BCi @ rb
        y = TMU - mu; Mh = (ONE @ SCi @ y) / (ONE @ SCi @ ONE); rs = y - Mh; cs = rs @ SCi @ rs if use_sn else 0.0
        cc = float(np.sum(((np.array([th, wb, wb + wc]) - TC) / CMB_S) ** 2))
        return (cb, cs, cc) if parts else cb + cs + cc

    res = {}
    for use_sn in ((True, False) if only is None else (only == "SN",)):
        tag = "BAO+CMB+SN" if use_sn else "BAO+CMB"
        best = {}
        for w0wa, starts in ((False, [[T["h"], T["omega_b"], T["omega_c_early"]], [0.68, 0.0224, 0.12], [0.66, 0.0226, 0.125]]),
                             (True, [[T["h"], T["omega_b"], T["omega_c_early"], -0.85, -0.3], [0.67, 0.0224, 0.12, -1.0, 0.0], [0.66, 0.0225, 0.121, -0.6, -1.2]])):
            runs = []
            for s in starts:
                r = minimize(lambda q: chi2(q, w0wa, use_sn=use_sn), s, method="Nelder-Mead",
                             options={"xatol": 1e-6, "fatol": 1e-4, "maxiter": 3000, "maxfev": 3000})
                r = minimize(lambda q: chi2(q, w0wa, use_sn=use_sn), r.x, method="Nelder-Mead",
                             options={"xatol": 1e-7, "fatol": 1e-5, "maxiter": 1500, "maxfev": 1500})
                runs.append((float(r.fun), r.x.tolist()))
                print(tag, "w0wa" if w0wa else "LCDM", runs[-1], flush=True)
            b = min(runs); best["w0wa" if w0wa else "LCDM"] = {"chi2": b[0], "params": b[1], "all_starts": runs}
        d = best["LCDM"]["chi2"] - best["w0wa"]["chi2"]
        from scipy.stats import chi2 as C2, norm
        sig = float(norm.isf(C2.sf(max(d, 0), 2) / 2))
        w0, wa = best["w0wa"]["params"][3:5]
        res[tag] = {"fits": best, "delta_chi2": d, "sigma_2dof": sig, "w0": w0, "wa": wa}
    if only is not None:
        json.dump(res, open(os.path.join(HERE, f"desi_mock_part_{only}.json"), "w"), indent=1)
        return
    score(res)


def score(res=None):
    if res is None:
        res = {}
        for part in ("SN", "noSN"):
            res.update(json.load(open(os.path.join(HERE, f"desi_mock_part_{part}.json"))))
    r = res["BAO+CMB+SN"]
    if r["sigma_2dof"] >= 2 and r["wa"] < 0 and r["w0"] > -1:
        reading = "REPRODUCES DESI'S SIGNAL"
    elif r["sigma_2dof"] >= 1 and r["wa"] < 0 and r["w0"] > -1:
        reading = "PARTIAL"
    else:
        reading = "DOES NOT"
    res["reading"] = reading
    res["vs_DESI_DR2_CMB_PantheonPlus"] = {"w0_sigma": (r["w0"] + 0.838) / 0.055, "wa_sigma": (r["wa"] + 0.62) / 0.21}
    json.dump(res, open(os.path.join(HERE, "desi_mock_result.json"), "w"), indent=1)
    print(reading, {k: (v["delta_chi2"], v["sigma_2dof"], v["w0"], v["wa"]) for k, v in res.items() if isinstance(v, dict) and "w0" in v})


if __name__ == "__main__":
    if sys.argv[1] == "fit" and len(sys.argv) > 2:
        fit(sys.argv[2])
    else:
        {"truth": truth, "fit": fit, "score": score}[sys.argv[1]]()
