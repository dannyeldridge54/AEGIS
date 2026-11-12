"""Data for the redshift map (one shared z axis): model curves (FLAG-1 vs its LCDM partner, Pantheon+ s8y6 fits) and
data points (DESI DR2 + SDSS BAO, DESI DR1 full-shape f sigma_s8 from SELFCHECK V3, ACT DR6 x BOSS E_G). AI-assisted."""
import json, os, sys, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); MP = os.path.dirname(HERE); AEG = os.path.abspath(os.path.join(MP, "..", ".."))
sys.path.insert(0, MP)
import m3_map as M3                     # coupled build + BAO data/predictions (checked against the stored DESI chi2)
E = M3.E; classy = M3.classy; spiral_guess = M3.spiral_guess
def mk(base, name, mpk):
    st = json.load(open(f"{E.OUT}/cmp_{name}.json"))["minimum"]
    info = E.make(base); a = dict(info["theory"]["classytwist"]["extra_args"])
    for k in ("lensing", "l_max_scalars", "non_linear"): a.pop(k, None)
    a.update({"A_s": 1e-10*np.exp(st["logA"]), "n_s": st["n_s"], "100*theta_s": st["theta_s_1e2"], "omega_b": st["omega_b"],
              "omega_cdm": st["omega_cdm"], "tau_reio": st["tau_reio"], "output": "mPk", "P_k_max_1/Mpc": 1.0, "z_max_pk": 3.0})
    if "spiraltwist" in base:
        b = st["scf_coupling_beta"]; a["scf_coupling_beta"] = b
        a["scf_parameters"] = f"1.0, 0.0, {spiral_guess.mu1_guess(1.0, b, st['omega_b'], st['omega_cdm'])}, 0.0, 0.0, 0.0"
    c = classy.Class(); c.set(a); c.compute(); return c, st
Z = [round(x, 3) for x in np.arange(0.05, 2.501, 0.05)]
out = {"z": Z}
for lab, base, name in (("LCDM", "ax_spa_lcdm_halofit", "ax_spa_lcdm_halofit_s8y6"), ("FLAG1", M3.FLAG, "ax_spa_spiraltwist_kappa1_nlfix_s8y6")):
    c, st = mk(base, name, True); h = c.h(); rd = c.rs_drag()
    bg = c.get_background(); zz = bg["z"][::-1]; rm = bg["(.)rho_b"][::-1] + bg["(.)rho_cdm"][::-1]; H0 = c.Hubble(0)
    dm = [c.angular_distance(z)*(1+z)/rd for z in Z]; dh = [1/c.Hubble(z)/rd for z in Z]
    def f_of(z, dz=0.01):
        lnD = lambda q: 0.5*np.log(c.pk_cb_lin(0.02, q)); return -(1+z)*(lnD(z+dz)-lnD(z-dz))/(2*dz)
    fs8 = [f_of(z)*c.sigma_cb(8/h, z) for z in Z]
    eg = [float(np.interp(z, zz, rm))/(1+z)**3/H0**2/f_of(z) for z in Z]
    out[lab] = {"DM_rd": dm, "DH_rd": dh, "fs8": fs8, "EG": eg, "beta": st.get("scf_coupling_beta")}
    c.struct_cleanup(); c.empty()
S = M3.load(); L, F = out["LCDM"], out["FLAG1"]
out["ratio"] = {"DM": [f/l-1 for f, l in zip(F["DM_rd"], L["DM_rd"])], "DH": [f/l-1 for f, l in zip(F["DH_rd"], L["DH_rd"])],
                "fs8": [f/l-1 for f, l in zip(F["fs8"], L["fs8"])], "EG": [f/l-1 for f, l in zip(F["EG"], L["EG"])]}
# BAO points vs the LCDM partner
c, _ = mk("ax_spa_lcdm_halofit", "ax_spa_lcdm_halofit_s8y6", False); refs = M3.pred_all(c, S); c.struct_cleanup(); c.empty()
pts = []
for (n, zs, qs, v, cov), r in zip(S, refs):
    e = np.sqrt(np.diag(cov))
    for z, q, x, s, rr in zip(zs, qs, v, e, r):
        sign = -1 if q == "bao_Hz_rs" else 1          # SDSS DR12 gives H; DH residual = -H residual (first order)
        qq = "DH" if q in ("bao_Hz_rs", "DH_over_rs") else "DM" if q == "DM_over_rs" else "DV"
        pts.append({"survey": "DESI DR2" if n.startswith("DESI") else "SDSS", "set": n, "z": float(z), "q": qq,
                    "resid": sign*float(x/rr-1), "err": float(s/rr)})
out["bao_points"] = pts
v3 = json.load(open(os.path.join(AEG, "field_tests/results/selfcheck_v3.json")))["fits"]["Pantheon+"]
sys.path.insert(0, os.path.join(AEG, "field_tests/selfcheck")); import v3_desi_fs as V3
out["fs8_points"] = [{"tracer": t, "z": z, "val": d, "err": float(np.sqrt(var)),
                      "FLAG1": v3["FLAG-1"]["pred"]["nw"][i]["fs8"], "LCDM": v3["LCDM"]["pred"]["nw"][i]["fs8"]}
                     for i, (t, z, d, var) in enumerate(zip(V3.TRACERS, V3.ZEFF, V3.DATA, V3.VAR))]
out["EG_points"] = [{"label": "ACT DR6 x CMASS", "z": 0.555, "val": 0.31, "up": 0.06, "lo": 0.05},
                    {"label": "ACT DR6 x LOWZ", "z": 0.316, "val": 0.49, "up": 0.14, "lo": 0.11}]
out["sources"] = {"fits": "cmp_ax_spa_spiraltwist_kappa1_nlfix_s8y6 / cmp_ax_spa_lcdm_halofit_s8y6",
                  "bao": "DESI DR2 ALL; SDSS DR12 consensus (rs_fid 147.78), DR16 LRG, DR16 QSO",
                  "fs8": "DESI DR1 full-shape (SELFCHECK V3, Pantheon+ fits, EH98 no-wiggle)", "EG": "Wenzl et al. 2024 arXiv:2405.12795"}
json.dump(out, open(os.path.join(HERE, "zmap_data.json"), "w"), indent=1)
print("ok", len(pts), out["ratio"]["DM"][13], out["ratio"]["EG"][10])
