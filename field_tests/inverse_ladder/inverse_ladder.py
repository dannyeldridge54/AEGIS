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
