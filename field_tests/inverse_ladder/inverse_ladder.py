"""Inverse distance ladder inside our own fits (EXPLORATORY, not pre-registered). For a stored best fit (CMB + BAO + SN,
its D_L(z) from dl_at_fit.py), the SN absolute magnitude M it implies = GLS fit of m_b_corr - 5 log10 D_L - 25 over the
Pantheon+ Hubble-flow SNe (z > 0.0233, non-calibrators; STAT+SYS covariance). SH0ES's M = GLS over the Cepheid-host
calibrators (m_b_corr - CEPH_DIST). The H0 tension inside the model is then one number: Delta M (mag), and the H0 the
model would need to agree with SH0ES: H0 * 10^(-Delta M / 5).
Errors: SN covariance only for M_model (the fit's own parameter error, ~0.4% in H0 -> ~0.009 mag, is added in quadrature);
the small cross-covariance between the two SN subsets is ignored."""
import json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "..", "..", "cmb-fit", "packages", "data", "sn_data", "PantheonPlus")
d = np.genfromtxt(os.path.join(D, "Pantheon+SH0ES.dat"), names=True, dtype=None, encoding=None)
C = np.loadtxt(os.path.join(D, "Pantheon+SH0ES_STAT+SYS.cov"))[1:].reshape(len(d), len(d))


def gls_mean(y, idx):
    Ci = np.linalg.inv(C[np.ix_(idx, idx)]); one = np.ones(idx.sum())
    v = 1 / (one @ Ci @ one); return float(v * one @ Ci @ y[idx]), float(np.sqrt(v))


cal = d["IS_CALIBRATOR"] == 1
hf = (~cal) & (d["zHD"] > 0.0233)
M_sh, e_sh = gls_mean(d["m_b_corr"] - d["CEPH_DIST"], cal)
out = {"note": "EXPLORATORY, not pre-registered", "M_SH0ES": [round(M_sh, 4), round(e_sh, 4)], "models": {}}
for run, H0 in (("ax_spa_spiraltwist_kappa1_nlfix_s8y6", 67.1585), ("ax_spa_lcdm_halofit_s8y6", 68.2461)):
    dl = np.load(os.path.join(HERE, f"dl_{run}.npy"))
    M, e = gls_mean(d["m_b_corr"] - 5 * np.log10(dl) - 25, hf)
    e = float(np.hypot(e, 0.009))
    dM = M - M_sh
    out["models"][run] = {"H0": H0, "M_implied": [round(M, 4), round(e, 4)], "Delta_M": round(dM, 4),
                          "sigma": round(dM / np.hypot(e, e_sh), 2), "H0_needed_for_SH0ES_M": round(H0 * 10 ** (-dM / 5), 2)}
json.dump(out, open(os.path.join(HERE, "inverse_ladder.json"), "w"), indent=1)
print(json.dumps(out, indent=1))

# JWST/CCHP calibration (Freedman et al. 2025, arXiv 2408.06153v3: TRGB HST+JWST H0 = 70.39 +- 1.22 stat +- 1.33 sys
# +- 0.70 sigma_SN). Its M on the Pantheon+ scale: the SH0ES M shifted by the H0 ratio, using the Pantheon+ Hubble-flow
# H0 that the SH0ES M gives here (73.82, ../local_void/void_shells.json fit A); error from the quoted H0 error.
H0_sh_hf, H0_j, eH0_j = 73.82, 70.39, float(np.sqrt(1.22 ** 2 + 1.33 ** 2 + 0.70 ** 2))
M_j = M_sh + 5 * np.log10(H0_j / H0_sh_hf); e_j = 5 / np.log(10) * eH0_j / H0_j
out["M_JWST_TRGB_approx"] = [round(float(M_j), 4), round(float(e_j), 4)]
for run, r in out["models"].items():
    M, e = r["M_implied"]
    r["vs_JWST_TRGB"] = {"Delta_M": round(M - M_j, 4), "sigma": round((M - M_j) / np.hypot(e, e_j), 2)}
json.dump(out, open(os.path.join(HERE, "inverse_ladder.json"), "w"), indent=1)
print("JWST", out["M_JWST_TRGB_approx"], {k: v["vs_JWST_TRGB"] for k, v in out["models"].items()})
