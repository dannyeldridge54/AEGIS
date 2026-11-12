"""BETA(z) (rule: field_tests/rules/PREREG_BETAZ.md): FLAG-1 with a piecewise-constant coupling, compressed likelihood.
    python betaz_fit.py fit <label>    label in LABELS; writes missing_piece/betaz/<label>.json (resumable per label)
    python betaz_fit.py score          -> field_tests/results/betaz.json
AI-assisted."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import betaz_build as B                     # must come before anything that imports classy
from scipy.optimize import minimize
from scipy.stats import chi2 as C2

AEG = B.AEG; E = B.E; classy = B.classy; spiral_guess = B.spiral_guess
RULE = os.path.join(AEG, "field_tests", "rules", "PREREG_BETAZ.md")
OUTD = os.path.join(HERE, "betaz"); os.makedirs(OUTD, exist_ok=True)
D = os.path.join(AEG, "cmb-fit", "packages", "data"); C = 299792.458
BAOF = {"dr2": ("desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_mean.txt", "desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_cov.txt"),
        "dr1": ("desi_2024_gaussian_bao_ALL_GCcomb_mean.txt", "desi_2024_gaussian_bao_ALL_GCcomb_cov.txt")}
SD = os.path.join(D, "sn_data", "PantheonPlus")
SN = np.genfromtxt(os.path.join(SD, "Pantheon+SH0ES.dat"), names=True, dtype=None, encoding=None)
SC = np.loadtxt(os.path.join(SD, "Pantheon+SH0ES_STAT+SYS.cov"))[1:].reshape(len(SN), len(SN))
msk = (SN["zHD"] > 0.01) & (SN["IS_CALIBRATOR"] == 0); SN = SN[msk]; SCi = np.linalg.inv(SC[np.ix_(msk, msk)])
ONE = np.ones(len(SN)); MU_OBS = SN["m_b_corr"].astype(float); CMB_S = np.array([0.00030, 0.00015, 0.0011])
LCDM = {k: v for k, v in E.BASE_ARGS.items() if k not in ("l_max_scalars", "non_linear")}
TAU = 0.0636
TR = json.load(open(os.path.join(E.OUT, "cmp_ax_spa_lcdm_halofit_s8y6.json")))["minimum"]
M1_FULL = os.path.join(HERE, "m1", "full.json")
HOLD_Z = 0.706
LABELS = ["const_dr2", "bz_dr2", "const_dr1", "bz_dr1", "const_dr2_ho", "bz_dr2_ho"]
BMAX = 0.15


def bao_data(rel):
    m = np.loadtxt(os.path.join(D, "bao_data", BAOF[rel][0]), dtype=str)
    return m[:, 0].astype(float), m[:, 1].astype(float), m[:, 2], np.loadtxt(os.path.join(D, "bao_data", BAOF[rel][1]))


def run_class(h, wb, wc, beta=None, bins=None):
    if beta is None:
        a = dict(LCDM, h=h, omega_b=wb, omega_cdm=wc, tau_reio=TAU, output="")
    else:
        g = spiral_guess.mu1_guess(1.0, beta, wb, wc, h=h)
        a = dict(B.SPIRAL, h=h, omega_b=wb, omega_cdm=wc, tau_reio=TAU, output="", scf_coupling_beta=beta,
                 scf_parameters=f"1.0, 0.0, {g}, 0.0, 0.0, 0.0")
        if bins is not None:
            a.update(scf_beta1=bins[0], scf_beta2=bins[1], scf_beta3=bins[2])
    c = classy.Class(); c.set(a); c.compute()
    return c


def observables(c, BZ, BQ, coupled):
    rd = c.rs_drag(); bg = c.get_background()
    zz = bg["z"][::-1]; dc = bg["comov. dist."][::-1]; hz = bg["H [1/Mpc]"][::-1]
    DC = lambda z: np.interp(z, zz, dc)
    dm = DC(BZ); dh = 1 / np.interp(BZ, zz, hz)
    vals = {"DM_over_rs": dm / rd, "DH_over_rs": dh / rd, "DV_over_rs": (BZ * dm * dm * dh) ** (1 / 3) / rd}
    bao = np.array([vals[q][i] for i, q in enumerate(BQ)])
    mu = 5 * np.log10(DC(SN["zHD"]) * (1 + SN["zHEL"])) + 25
    th = c.get_current_derived_parameters(["100*theta_star"])["100*theta_star"]
    if coupled:
        rc = bg["(.)rho_cdm"][::-1]; wce = float(np.interp(1090, zz, rc)) / 1091 ** 3 / (100 / C) ** 2
    else:
        wce = None
    return bao, mu, th, wce


def cmb_target():
    """The compressed-CMB vector of the M1/V1 anchor: the LCDM partner's (theta*, w_b, w_b + w_c)."""
    c = run_class(TR["H0"] / 100, TR["omega_b"], TR["omega_cdm"])
    th = c.get_current_derived_parameters(["100*theta_star"])["100*theta_star"]; c.struct_cleanup(); c.empty()
    return np.array([th, TR["omega_b"], TR["omega_b"] + TR["omega_cdm"]])


def make_chi2(rel, hold):
    BZ, BV, BQ, BC = bao_data(rel)
    keep = ~np.isclose(BZ, HOLD_Z) if hold else np.ones(len(BZ), bool)
    Ci = np.linalg.inv(BC[np.ix_(keep, keep)]); TC = cmb_target()

    def chi2(p, binned):
        h, wb, wc, be = p[:4]; bins = p[4:7] if binned else None
        if binned:
            if any(abs(x) > BMAX for x in p[3:7]):
                return 1e10
        elif not (0.0 <= be <= 0.12):
            return 1e10
        try:
            c = run_class(h, wb, wc, be, bins); bao, mu, th, wce = observables(c, BZ, BQ, True); c.struct_cleanup(); c.empty()
        except Exception:
            return 1e10
        rb = (BV - bao)[keep]; y = MU_OBS - mu
        rs = y - (ONE @ SCi @ y) / (ONE @ SCi @ ONE)
        cmb = np.array([th, wb, wb + wce])
        return float(rb @ Ci @ rb + rs @ SCi @ rs + np.sum(((cmb - TC) / CMB_S) ** 2))
    return chi2, (BZ, BV, BQ, BC, keep)


def nm(f, x0, maxfev):
    r = minimize(f, x0, method="Nelder-Mead", options={"xatol": 1e-6, "fatol": 1e-3, "maxiter": maxfev, "maxfev": maxfev})
    return float(r.fun), [float(v) for v in r.x]


def hessian_errors(f, x, steps):
    n = len(x); H = np.zeros((n, n)); f0 = f(x)
    for i in range(n):
        for j in range(i, n):
            def fx(si, sj):
                y = np.array(x, float); y[i] += si * steps[i]; y[j] += sj * steps[j]; return f(y)
            if i == j:
                H[i, i] = (fx(1, 0) - 2 * f0 + fx(-1, 0)) / steps[i] ** 2
            else:
                H[i, j] = H[j, i] = (fx(1, 1) - fx(1, -1) - fx(-1, 1) + fx(-1, -1)) / (4 * steps[i] * steps[j])
    cov = np.linalg.inv(H / 2)
    return [float(np.sqrt(cov[i, i])) if cov[i, i] > 0 else None for i in range(n)]


def fit(label):
    assert os.path.exists(RULE + ".sha256"), "rule not locked"
    f = os.path.join(OUTD, f"{label}.json")
    if os.path.exists(f):
        return
    kind, rel = label.split("_")[0], label.split("_")[1]; hold = label.endswith("_ho")
    chi2, _ = make_chi2(rel, hold)
    t = [TR["H0"] / 100, TR["omega_b"], TR["omega_cdm"]]
    if kind == "const":
        starts = [t + [0.01], [t[0] - 0.01, t[1] + 0.0002, t[2] + 0.002, 0.04], [t[0] + 0.01, t[1] - 0.0002, t[2] - 0.002, 0.08]]
        runs = [nm(lambda q: chi2(q, False), s, 1500) for s in starts]
        best = min(runs); out = {"label": label, "chi2": best[0], "params": best[1], "names": ["h", "omega_b", "omega_c", "beta"]}
    else:
        cf = os.path.join(OUTD, f"const_{label[3:]}.json")
        cp = json.load(open(cf))["params"]; b = cp[3]
        starts = [cp[:3] + [b, b, b, b], cp[:3] + [b, b - 0.03, b, b + 0.03], cp[:3] + [b, b + 0.03, b, b - 0.03]]
        runs = [nm(lambda q: chi2(q, True), s, 4000) for s in starts]
        best = min(runs)
        out = {"label": label, "chi2": best[0], "params": best[1],
               "names": ["h", "omega_b", "omega_c", "beta_early", "beta1_z<0.5", "beta2_z0.5-1", "beta3_z1-2"],
               "all_starts": [r[0] for r in runs]}
        if not hold:
            out["errors"] = hessian_errors(lambda q: chi2(q, True), best[1], [1e-4, 1e-4, 1e-4, 0.005, 0.005, 0.005, 0.005])
    json.dump(out, open(f, "w"), indent=1); print(label, round(out["chi2"], 3), [round(v, 4) for v in out["params"]], flush=True)


def predict_holdout(label):
    """chi2 of the held-out z = 0.706 bin (DM, DH) at a holdout fit's minimum, with its 2x2 covariance."""
    r = json.load(open(os.path.join(OUTD, f"{label}.json"))); p = r["params"]
    BZ, BV, BQ, BC = bao_data("dr2"); m = np.isclose(BZ, HOLD_Z)
    bins = p[4:7] if label.startswith("bz") else None
    c = run_class(p[0], p[1], p[2], p[3], bins); bao, *_ = observables(c, BZ, BQ, True); c.struct_cleanup(); c.empty()
    d = (BV - bao)[m]; return float(d @ np.linalg.inv(BC[np.ix_(m, m)]) @ d)


def score():
    R = {l: json.load(open(os.path.join(OUTD, f"{l}.json"))) for l in LABELS}
    m1 = json.load(open(M1_FULL))["FLAG1"][0]
    gate = abs(R["const_dr2"]["chi2"] - m1) <= 0.05
    out = {"rule": "PREREG_BETAZ.md", "gate": {"const_dr2_chi2": R["const_dr2"]["chi2"], "m1_full_flag1_chi2": m1, "pass": gate}}
    d1 = R["const_dr2"]["chi2"] - R["bz_dr2"]["chi2"]
    shape = {n: {"value": round(v, 4), "err": (round(e, 4) if e else None)}
             for n, v, e in zip(R["bz_dr2"]["names"][3:], R["bz_dr2"]["params"][3:], R["bz_dr2"]["errors"][3:])}
    vals = R["bz_dr2"]["params"][3:7]
    out["B1"] = {"delta": round(d1, 3), "p_chi2_3": float(C2.sf(max(d1, 0), 3)), "beta_shape_dr2": shape,
                 "sign_change": bool(min(vals) < 0 < max(vals)),
                 "reading": "NO VERDICT" if not gate else ("TIME VARIATION NEEDED" if d1 >= 7.81 else "NOT NEEDED")}
    s1, s2 = R["bz_dr1"], R["bz_dr2"]
    shifts = {s2["names"][i]: (abs(s2["params"][i] - s1["params"][i]) / s1["errors"][i] if s1["errors"][i] else None) for i in (4, 5, 6)}
    ok = [v for v in shifts.values() if v is not None]
    rb2 = ("NO VERDICT" if not gate or len(ok) < 3 else "STABLE" if max(ok) < 1 else "WANDERS" if max(ok) > 2 else "UNCLEAR")
    out["B2"] = {"shift_in_dr1_sigma": {k: (round(v, 2) if v is not None else None) for k, v in shifts.items()},
                 "beta_dr1": dict(zip(s1["names"][3:], [round(v, 4) for v in s1["params"][3:]])), "reading": rb2,
                 "note": "DR2 contains DR1; correlated, a consistency check"}
    pb, pc = predict_holdout("bz_dr2_ho"), predict_holdout("const_dr2_ho"); d3 = pb - pc
    out["B3"] = {"chi2_pred_betaz": round(pb, 3), "chi2_pred_const": round(pc, 3), "delta": round(d3, 3),
                 "reading": "NO VERDICT" if not gate else ("BETA(z) PREDICTS BETTER" if d3 <= -1 else "WORSE" if d3 >= 1 else "SAME")}
    out["fits"] = {l: {"chi2": round(r["chi2"], 3), "params": [round(v, 5) for v in r["params"]]} for l, r in R.items()}
    json.dump(out, open(os.path.join(AEG, "field_tests", "results", "betaz.json"), "w"), indent=1)
    print(json.dumps({k: out[k] for k in ("gate", "B1", "B2", "B3")}, indent=1))


if __name__ == "__main__":
    fit(sys.argv[2]) if sys.argv[1] == "fit" else score()
