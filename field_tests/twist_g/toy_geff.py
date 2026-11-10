"""EXPLORATORY feasibility (not pre-registered, not a verdict): can a dilaton coupled to gravity raise H0?
Toy background-only model. G_eff(z)/G0 = 1 + A (phi(z) - phi0)^2, with phi(z) the flagship's own field history
(../dilaton_me/phi_of_z.npz) and a quadratic (Damour-Nordtvedt-type) coupling about today's value. So G_eff = G0 today, and
to first order the solar-system (Cassini) and lunar-ranging (Gdot/G) limits are met.
H^2(z) = G_eff(z) (100)^2 [w_m (1+z)^3 + w_r (1+z)^4 + w_L]. Fitted: h, w_b, w_c, A (A = 0 is the reference).
Data: DESI DR2 BAO (all), Pantheon+ (uncalibrated, M marginalised), and Planck 2018 distance priors (R, l_A, w_b; Chen,
Huang & Wang 2019) as the CMB stand-in. LIMITS OF THE TOY: no perturbations, so no growth/S8 and no full CMB; z* and z_d from
fitting formulas; the priors were derived for standard gravity. A positive outcome only justifies the real build (hi_class),
it does not stand as a result. Also reports G_eff at z = 2, recombination and BBN against rough bounds (|dG/G| at BBN
< ~10%, at recombination < ~5%)."""
import json, os
import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__)); AEG = os.path.abspath(os.path.join(HERE, "..", ".."))
P = np.load(os.path.join(AEG, "field_tests", "dilaton_me", "phi_of_z.npz")); zp, pp = P["z"], P["phi"]
lzp = np.log1p(zp); PHI0 = float(np.interp(0, zp, pp))
f = lambda z: (np.interp(np.log1p(z), lzp, pp) - PHI0) ** 2
C = 299792.458; TCMB = 2.7255
w_g = 2.473e-5 * (TCMB / 2.7255) ** 4; w_r = w_g * (1 + 0.2271 * 3.046)

D = os.path.join(AEG, "cmb-fit", "packages", "data")
bm = np.loadtxt(os.path.join(D, "bao_data", "desi_bao_dr2", "desi_gaussian_bao_ALL_GCcomb_mean.txt"), dtype=str)
bz, bv, bq = bm[:, 0].astype(float), bm[:, 1].astype(float), bm[:, 2]
bCi = np.linalg.inv(np.loadtxt(os.path.join(D, "bao_data", "desi_bao_dr2", "desi_gaussian_bao_ALL_GCcomb_cov.txt")))
SD = os.path.join(D, "sn_data", "PantheonPlus")
sn = np.genfromtxt(os.path.join(SD, "Pantheon+SH0ES.dat"), names=True, dtype=None, encoding=None)
sC = np.loadtxt(os.path.join(SD, "Pantheon+SH0ES_STAT+SYS.cov"))[1:].reshape(len(sn), len(sn))
m = (sn["zHD"] > 0.01) & (sn["IS_CALIBRATOR"] == 0)
sn, sCi = sn[m], np.linalg.inv(sC[np.ix_(m, m)]); one = np.ones(len(sn))
cmb_mu = np.array([1.7502, 301.471, 0.02236]); cmb_s = np.array([0.0046, 0.090, 0.00015])
cmb_r = np.array([[1, 0.46, -0.66], [0.46, 1, -0.33], [-0.66, -0.33, 1]])
cmbCi = np.linalg.inv(cmb_r * np.outer(cmb_s, cmb_s))
zg = np.concatenate([np.linspace(0, 3, 600), np.logspace(np.log10(3.01), 5, 1500)])


def model(h, wb, wc, A):
    wm = wb + wc + 0.06 / 93.14; wL = h * h - wm - w_r
    G = 1 + A * f(zg)
    H = 100 * np.sqrt(np.maximum(G * (wm * (1 + zg) ** 3 + w_r * (1 + zg) ** 4 + wL), 1e-30))
    chi = np.concatenate([[0], np.cumsum(0.5 * (1 / H[1:] + 1 / H[:-1]) * np.diff(zg))]) * C
    DM = lambda z: np.interp(z, zg, chi)
    Hz = lambda z: np.interp(z, zg, H)
    zs = 1048 * (1 + 0.00124 * wb ** -0.738) * (1 + (0.0783 * wb ** -0.238 / (1 + 39.5 * wb ** 0.763)) * wm ** (0.560 / (1 + 21.1 * wb ** 1.81)))
    b1 = 0.313 * wm ** -0.419 * (1 + 0.607 * wm ** 0.674); b2 = 0.238 * wm ** 0.223
    zd = 1291 * wm ** 0.251 / (1 + 0.659 * wm ** 0.828) * (1 + b1 * wb ** b2)

    def rs(z0):
        g = lambda z: C / np.sqrt(3 * (1 + 3 * wb / (4 * w_g * (1 + z)))) / (100 * np.sqrt((1 + A * f(z)) * (wm * (1 + z) ** 3 + w_r * (1 + z) ** 4 + wL)))
        return quad(g, z0, 1e7, limit=200)[0]
    rd = rs(zd)
    return DM, Hz, zs, rs(zs), rd, wm


def chi2(p, ret=False):
    h, wb, wc, A = p
    if not (0.5 < h < 0.9 and 0.015 < wb < 0.03 and 0.08 < wc < 0.16):
        return 1e10
    DM, Hz, zs, rss, rd, wm = model(h, wb, wc, A)
    th = []
    for z, q in zip(bz, bq):
        dm, dh = DM(z), C / Hz(z)
        th.append({"DM_over_rs": dm / rd, "DH_over_rs": dh / rd, "DV_over_rs": (z * dm * dm * dh) ** (1 / 3) / rd}[q])
    r = bv - np.array(th); cb = r @ bCi @ r
    dl = (1 + sn["zHEL"]) * DM(sn["zHD"]); y = sn["m_b_corr"] - 5 * np.log10(dl) - 25
    Mh = (one @ sCi @ y) / (one @ sCi @ one); rs_ = y - Mh; cs = rs_ @ sCi @ rs_
    R = np.sqrt(wm) * 100 * DM(zs) / C; lA = np.pi * DM(zs) / rss
    rc = np.array([R, lA, wb]) - cmb_mu; cc = rc @ cmbCi @ rc
    if ret:
        return {"chi2": cb + cs + cc, "bao": cb, "sn": cs, "cmb": cc, "rd": rd}
    return cb + cs + cc


out = {"note": "EXPLORATORY toy feasibility; background only; not a verdict", "phi0": PHI0,
       "f_at": {str(z): float(f(z)) for z in (0, 0.5, 1, 2, 3, 10, 1100, 1e5)}}
best = {}
for name, x0, fixA in (("A=0 (no gravity coupling)", [0.68, 0.0224, 0.119, 0.0], True), ("A free", [0.68, 0.0224, 0.119, 0.5], False)):
    fun = (lambda q: chi2([*q, 0.0])) if fixA else chi2
    st = x0[:3] if fixA else x0
    r = minimize(fun, st, method="Nelder-Mead", options={"xatol": 1e-6, "fatol": 1e-4, "maxiter": 6000, "maxfev": 12000})
    for _ in range(2):
        r = minimize(fun, r.x, method="Nelder-Mead", options={"xatol": 1e-7, "fatol": 1e-5, "maxiter": 6000, "maxfev": 12000})
    p = [*r.x, 0.0] if fixA else list(r.x)
    d = chi2(p, ret=True); A = p[3]
    best[name] = {"H0": round(100 * p[0], 3), "w_b": p[1], "w_c": p[2], "A": A, **{k: round(float(v), 3) for k, v in d.items()},
                  "dG_over_G": {"z=2": A * float(f(2)), "recombination": A * float(f(1100)), "BBN": A * float(f(1e8 if 1e8 < zp.max() else zp.max()))}}
    print(name, best[name], flush=True)
out["fits"] = best
out["delta_chi2"] = round(best["A free"]["chi2"] - best["A=0 (no gravity coupling)"]["chi2"], 3)
out["delta_H0"] = round(best["A free"]["H0"] - best["A=0 (no gravity coupling)"]["H0"], 3)
json.dump(out, open(os.path.join(HERE, "toy_geff.json"), "w"), indent=1)
print("dchi2", out["delta_chi2"], "dH0", out["delta_H0"])
