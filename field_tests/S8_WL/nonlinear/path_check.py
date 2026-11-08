import os, sys, json, numpy as np
sys.path.insert(0, os.getcwd())
import axhm_pk as A   # (run once with version = "basic" in a copy for the second check)
best = json.load(open(os.environ["TWIST_RESULTS"] + "/cmp_ax_spa_lcdm_halofit.json"))["minimum"]
src = np.load("../results/pk_ax_spa_lcdm_halofit.npz"); kh = src["k_h"]; h = float(src["h0"])
M = np.logspace(7, 18, 100)
for fax in (0.001, 0.06):
  for zi, z in ((0, 0.0), (50, float(src["z_pk"][50]))):
    pz = src["p_k_lin"][zi]
    b2 = dict(best); b2["omega_fld"] = best["omega_cdm"] * fax; b2["omega_cdm"] = best["omega_cdm"] * (1 - fax)
    c = A.cosmo(b2, h, z, fax, 1.41e-25)
    psd = {"k": kh, "power_total": pz, "power_CDM": pz, "power_baryon": pz, "power_cold": pz, "power_axion": pz}
    hp = A.HMcode_params.HMCode_param_dic(c, kh, pz)
    hp["dw"] = A.dewiggle_ratio(kh, pz, h, best["omega_b"] + best["omega_cdm"], best["omega_b"], best["n_s"])
    ap = A.axion_params.func_axion_param_dic(M, c, psd, hp, concentration_param=True)
    nl_ax = A.PS_nonlin_axion.func_full_halo_model_ax(M, psd, c, hp, ap, **A.FLAGS)[0]
    c0 = A.cosmo(best, h, z, 0.0, 1e-25)
    hp0 = A.HMcode_params.HMCode_param_dic(c0, kh, pz)
    hp0["dw"] = hp["dw"]
    nl0 = A.PS_nonlin_cold.func_non_lin_PS_matter(M, kh, pz, c0, hp0, c0["Omega_m_0"], **A.FLAGS)[0]
    out = " ".join("%.2f:%.3f" % (kh[j], nl_ax[j] / nl0[j]) for j in [abs(kh - k).argmin() for k in (0.05, 0.1, 0.2, 0.5, 1, 3, 10)])
    print("fax %.3f z %.2f  ULA path / cold path (same linear power): %s" % (fax, z, out), flush=True)
