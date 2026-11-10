"""EXPLORATORY (not pre-registered): where the flagship's dark energy lands in DESI's (w0, wa) plane.
DESI fits assume uncoupled CDM ~ a^-3. So the "dark energy" a DESI-style analysis would infer from the flagship is
rho_DE,eff(a) = rho_tot - rho_b - rho_rad - rho_ncdm - rho_cdm(today) a^-3  (the coupling's transfer is absorbed into DE),
and w_eff = -1 - (1/3) dln rho_DE,eff / dln a. Fit w0 + wa (1 - a) to w_eff over z in [0, 2] (where BAO + SN constrain it),
weighted by rho_DE,eff (DE only matters where it is large). Also the bare field's own w_scf.
    python flagship_w0wa.py   -> flagship_w0wa.json"""
import sys, os, json, types
import numpy as np
for n in ("candl", "candl.interface", "spt_candl_data"):
    sys.modules.setdefault(n, types.SimpleNamespace(CandlCobayaLikelihood=None, SPT3G_D1_TnE=None, interface=None))
sys.modules["candl"].interface = sys.modules["candl.interface"]
HERE = os.path.dirname(os.path.abspath(__file__)); AEGIS = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(AEGIS, "cmb-fit", "axiclass"))
import early_late_spa as E, spiral_guess

RUNS = ["ax_spa_spiraltwist_kappa1_nlfix", "ax_spa_spiraltwist_kappa1_dovekie_nlfix", "ax_spa_spiraltwist_kappa1_union3_nlfix"]
E._maybe_coupled(RUNS[0])
import classy
out = {"note": "EXPLORATORY, not pre-registered", "runs": {}}
for run in RUNS:
    info = E.make(run)
    st = json.load(open(f"{E.OUT}/cmp_{run}_s8y6.json"))["minimum"]
    a = dict(info["theory"]["classytwist"]["extra_args"])
    a.update({"A_s": 1e-10 * np.exp(st["logA"]), "n_s": st["n_s"], "100*theta_s": st["theta_s_1e2"], "omega_b": st["omega_b"],
              "omega_cdm": st["omega_cdm"], "tau_reio": st["tau_reio"]})
    for k in ("output", "lensing", "l_max_scalars", "non_linear", "P_k_max_1/Mpc"):
        a.pop(k, None)
    k, b = st.get("spiral_kappa", 1.0), st["scf_coupling_beta"]
    a["scf_coupling_beta"] = b
    a["scf_parameters"] = f"{k}, 0.0, {spiral_guess.mu1_guess(k, b, st['omega_b'], st['omega_cdm'])}, 0.0, 0.0, 0.0"
    c = classy.Class(); c.set(a); c.compute()
    bg = c.get_background()
    z = bg["z"]; sel = z <= 3.0; z = z[sel]; aa = 1 / (1 + z)
    g = lambda key: bg[key][sel] if key in bg else 0 * z
    rad_etc = g("(.)rho_b") + g("(.)rho_g") + g("(.)rho_ur") + g("(.)rho_ncdm[0]")
    cdm0 = bg["(.)rho_cdm"][-1]
    de_eff = g("(.)rho_tot") - rad_etc - cdm0 * aa ** -3
    lna = np.log(aa)
    o = np.argsort(lna); lna, de_eff, z, aa = lna[o], de_eff[o], z[o], aa[o]
    w_eff = -1 - np.gradient(np.log(de_eff), lna) / 3
    w_scf = (g("(.)p_scf") / g("(.)rho_scf"))[o]
    m = z <= 2.0
    X = np.vstack([np.ones(m.sum()), 1 - aa[m]]).T; W = de_eff[m] / de_eff[m].max()
    w0, wa = np.linalg.lstsq(X * np.sqrt(W)[:, None], w_eff[m] * np.sqrt(W), rcond=None)[0]
    zi = lambda arr, zz: float(np.interp(zz, z[::-1], arr[::-1]))   # z descends after the sort
    out["runs"][run] = {"beta_eff": b, "H0": st.get("H0"), "w0_eff": round(float(w0), 3), "wa_eff": round(float(wa), 3),
                        "w_eff(z=0,0.5,1,2)": [round(zi(w_eff, q), 3) for q in (0, 0.5, 1, 2)],
                        "w_scf(z=0,0.5,1,2)": [round(zi(w_scf, q), 3) for q in (0, 0.5, 1, 2)]}
    print(run, out["runs"][run], flush=True)
# DESI DR2 (arXiv 2503.14738) w0waCDM, DESI BAO + CMB + SN: means and 1-sigma (as published; quoted here)
out["DESI_DR2"] = {"+Pantheon+": [-0.838, 0.055, -0.62, 0.21], "+Union3": [-0.667, 0.088, -1.09, 0.29],
                   "+DESY5": [-0.752, 0.057, -0.86, 0.22], "CMB only": [-0.42, 0.21, -1.75, 0.58]}
json.dump(out, open(os.path.join(HERE, "flagship_w0wa.json"), "w"), indent=1)
