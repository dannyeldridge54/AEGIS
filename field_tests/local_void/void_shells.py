"""EXPLORATORY (not pre-registered): local-void test with Pantheon+SH0ES. If we sit in a large underdensity (KBC void),
the expansion rate measured from nearby SNe should exceed that from distant ones, dropping toward the global value
beyond the void edge (~z 0.1-0.15). Method: SH0ES-style joint fit, full STAT+SYS covariance. Cepheid-host calibrators
(mu = CEPH_DIST) fix M; Hubble-flow SNe get mu_model = 5 log10(D_L(z; H0_shell, Om)) + 25 with flat LCDM shape
(Om = 0.315 fixed; beyond z 0.15 the shell "H0" is just the distance-scale intercept there). Fits:
  (A) one H0 for all;  (B) one H0 per redshift shell;  (C) one H0 per sky hemisphere x near/far (direction check).
Expectation stated before running: little or no trend (SH0ES-range checks found no big step)."""
import json, os
import numpy as np
from scipy.integrate import quad

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "cmb-fit", "packages", "data", "sn_data", "PantheonPlus")
d = np.genfromtxt(os.path.join(D, "Pantheon+SH0ES.dat"), names=True, dtype=None, encoding=None)
C = np.loadtxt(os.path.join(D, "Pantheon+SH0ES_STAT+SYS.cov"))[1:].reshape(len(d), len(d))
OM, c = 0.315, 299792.458
cal = d["IS_CALIBRATOR"] == 1
hf = (~cal) & (d["zHD"] > 0.0233)          # SH0ES Hubble-flow cut (no upper cut; shells below)
use = cal | hf
d, C = d[use], C[np.ix_(use, use)]
cal, z = d["IS_CALIBRATOR"] == 1, d["zHD"]
Ci = np.linalg.inv(C)
E = lambda zz: 1 / np.sqrt(OM * (1 + zz) ** 3 + 1 - OM)
dlc = np.array([(1 + d["zHEL"][i]) * c * quad(E, 0, zz)[0] for i, zz in enumerate(z)])   # D_L * H0
mu0 = 5 * np.log10(np.where(dlc > 0, dlc, 1)) + 25                                      # mu at H0 = 1


def fit(groups, names):
    """Exact GLS (the model is linear in M and x_i = 5 log10 H0_i). groups: label per HF SN (-1 = calibrator)."""
    ng = len(names)
    X = np.zeros((len(d), 1 + ng)); X[:, 0] = 1
    for i in range(ng):
        X[groups == i, 1 + i] = -1.0                     # m = M + mu0 - x_i  ->  m - mu0 = M - x_i
    y = d["m_b_corr"] - np.where(cal, d["CEPH_DIST"], mu0)
    F = X.T @ Ci @ X; Cov = np.linalg.inv(F); p = Cov @ X.T @ Ci @ y
    r = y - X @ p
    H = 10 ** (p[1:] / 5); eH = H * np.log(10) / 5 * np.sqrt(np.diag(Cov)[1:])
    out = {"chi2": float(r @ Ci @ r), "M": float(p[0]),
           "H0": {n: [round(float(h), 2), round(float(e), 2), int((groups == i).sum())] for i, (n, h, e) in enumerate(zip(names, H, eH))}}
    if ng > 1:   # relative to the last group: ratio and error with the shared M calibration cancelled
        J = np.zeros((ng - 1, 1 + ng))
        for i in range(ng - 1):
            J[i, 1 + i], J[i, ng] = 1, -1
        dx = J @ p; edx = np.sqrt(np.diag(J @ Cov @ J.T))
        out["rel_to_" + names[-1] + "_pct"] = {n: [round(float((10 ** (a / 5) - 1) * 100), 2), round(float(np.log(10) / 5 * e * 100), 2)] for n, a, e in zip(names[:-1], dx, edx)}
    return out


out = {"note": "EXPLORATORY, not pre-registered; Pantheon+SH0ES STAT+SYS; Om 0.315 flat-LCDM shape"}
g = np.where(cal, -1, 0)
out["A_single"] = fit(g, ["all"])
edges = [0.0233, 0.05, 0.1, 0.15, 0.3, 0.6, 2.5]
g = np.where(cal, -1, np.digitize(z, edges) - 1)
out["B_shells"] = fit(g, [f"{a}-{b}" for a, b in zip(edges[:-1], edges[1:])])
out["B_vs_A"] = {"dchi2": round(out["B_shells"]["chi2"] - out["A_single"]["chi2"], 2), "extra_params": len(edges) - 2}
# direction: CMB-dipole-ish split by galactic... use simple equatorial hemispheres (DEC>0 / DEC<0) x (z<0.1 / z>=0.1)
north, near = d["DEC"] > 0, z < 0.1
g = np.where(cal, -1, 2 * (~north) + (~near))
out["C_hemi"] = fit(g, ["north_near", "north_far", "south_near", "south_far"])
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "void_shells.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
