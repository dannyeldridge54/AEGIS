"""Development 57 (exploratory): the w(z) an observer infers if they assume ordinary (uncoupled) dark matter.
For each stored TOURNAMENT best fit, take the model's H(z) from CLASS; take the observer's matter as
rho_m,obs(a) = rho_m,0 a^-3 with rho_m,0 the model's present matter density (baryons + CDM today); then
rho_DE,eff = 3 H^2 M_P^2 - rho_r - rho_m,obs, w_eff = -1 - (1/3) dln rho_DE,eff / dln a; fit CPL w0 + wa (1-a)
over 0 < z < 2 (weighted evenly in a). AI-assisted."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import tournament as T
R = json.load(open(os.path.join(T.AEG, "field_tests", "results", "tournament.json")))["rows"]
P = json.load(open(os.path.join(T.AEG, "field_tests", "results", "pure_twist_predictions.json")))
CASES = {"PURE-TWIST (kappa sqrt(2/3), beta 0)": ("SPIRAL", list(P["pure_twist_params"]) + [0.0, 0.8165]),
         "FLAG-1 (kappa 1, beta 0.041)": ("FLAG1", R["FLAG1"]["params_FULL"]),
         "SPIRAL free (kappa 0.85, beta 0.035)": ("SPIRAL", R["SPIRAL"]["params_FULL"]),
         "W0WA fit (check)": ("W0WA", R["W0WA"]["params_FULL"])}
out = {}
for lab, (v, p) in CASES.items():
    c = T.model(v, p); bg = c.get_background()
    z = bg["z"][::-1]; H = bg["H [1/Mpc]"][::-1]; rcrit = bg["(.)rho_crit"][::-1]
    rm = bg["(.)rho_b"][::-1] + bg["(.)rho_cdm"][::-1]; rr = bg["(.)rho_g"][::-1] + bg.get("(.)rho_ur", np.zeros_like(z))[::-1]
    a = 1 / (1 + z); rm0 = float(np.interp(0, z, rm))
    rde = rcrit - rr - rm0 * a ** -3
    sel = (z <= 2.0)
    la, lr = np.log(a[sel]), np.log(rde[sel])
    w = -1 - np.gradient(lr, la) / 3
    A = np.vstack([np.ones(sel.sum()), 1 - a[sel]]).T
    grid = np.linspace(a[sel].min(), 1, 400); wg = np.interp(grid, a[sel][::-1], w[::-1]) if a[sel][0] > a[sel][-1] else np.interp(grid, a[sel], w)
    w0, wa = np.linalg.lstsq(np.vstack([np.ones(400), 1 - grid]).T, wg, rcond=None)[0]
    out[lab] = {"w0_eff": round(float(w0), 3), "wa_eff": round(float(wa), 3), "w_eff_z0": round(float(np.interp(0, z[sel], w)), 3),
                "w_eff_z1": round(float(np.interp(1, z[sel], w)), 3), "min_w_eff_z_lt2": round(float(w.min()), 3)}
    print(lab, out[lab], flush=True)
    c.struct_cleanup(); c.empty()
out["DESI DR2 + CMB + DESY5 (unified tracer, arXiv:2608.27830)"] = {"w0": -0.803, "wa": -0.73}
json.dump(out, open(os.path.join(T.AEG, "field_tests", "results", "effective_w.json"), "w"), indent=1)
