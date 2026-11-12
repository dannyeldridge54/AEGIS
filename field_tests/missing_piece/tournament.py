"""TOURNAMENT (rule: field_tests/rules/PREREG_TOURNAMENT.md): late-time Twist versions on one compressed likelihood.
    python tournament.py fit <VERSION> <CONFIG>    VERSION in VERSIONS, CONFIG in FULL|NOBAO|SDSS -> tournament/<V>_<C>.json
    python tournament.py score                      -> field_tests/results/tournament.json
Resumable: each start is saved. AI-assisted."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import betaz_build as B                     # beta(z) build, loaded before classy
import betaz_fit as F                       # shared SN, CMB target, observables, Nelder-Mead
from scipy.optimize import minimize
AEG = B.AEG; E = B.E; classy = B.classy; spiral_guess = B.spiral_guess
RULE = os.path.join(AEG, "field_tests", "rules", "PREREG_TOURNAMENT.md")
OUTD = os.path.join(HERE, "tournament"); os.makedirs(OUTD, exist_ok=True)
D = os.path.join(AEG, "cmb-fit", "packages", "data", "bao_data"); C = 299792.458
VERSIONS = {"LCDM": 0, "W0WA": 2, "SPIRAL0": 0, "FLAG1": 1, "SPIRAL": 2, "ON2": 1, "ON1": 1, "ON05": 1}
TWIST = ["SPIRAL0", "FLAG1", "SPIRAL", "ON2", "ON1", "ON05"]
ON_EARLY = 0.001     # D1: the closure solver fails at exactly 0 with late bins on; 0.001 (2*beta^2 = 2e-6) stands in for 0
ON_BINS = {"ON2": (1, 1, 1), "ON1": (1, 1, 0), "ON05": (1, 0, 0)}     # which late bins (z<0.5, 0.5-1, 1-2) carry beta


def bao_desi():
    BZ, BV, BQ, BC = F.bao_data("dr2")
    return [("DESI", BZ, BV, BQ, BC)]


def bao_sdss():
    m = np.loadtxt(os.path.join(D, "sdss_DR12Consensus_bao.dat"), dtype=str)
    c = np.loadtxt(os.path.join(D, "BAO_consensus_covtot_dM_Hz.txt"))
    keep = m[:, 0].astype(float) < 0.55                                   # z = 0.38 and 0.51 only
    out = [("DR12", m[keep, 0].astype(float), m[keep, 1].astype(float), m[keep, 2], c[np.ix_(keep, keep)])]
    for fn, cf, lab in (("sdss_DR16_LRG_BAO_DMDH.dat", "sdss_DR16_LRG_BAO_DMDH_covtot.txt", "DR16LRG"),
                        ("sdss_DR16_QSO_BAO_DMDH.txt", "sdss_DR16_QSO_BAO_DMDH_covtot.txt", "DR16QSO")):
        m = np.loadtxt(os.path.join(D, fn), dtype=str)
        out.append((lab, m[:, 0].astype(float), m[:, 1].astype(float), m[:, 2], np.loadtxt(os.path.join(D, cf))))
    return out


def model(version, p):
    """Return a computed CLASS object for parameter vector p (h, wb, wc, ...)."""
    h, wb, wc = p[:3]
    if version == "LCDM":
        a = dict(F.LCDM, h=h, omega_b=wb, omega_cdm=wc, tau_reio=F.TAU, output="")
    elif version == "W0WA":
        a = dict(F.LCDM, h=h, omega_b=wb, omega_cdm=wc, tau_reio=F.TAU, output="", Omega_Lambda=0.0, use_ppf="yes", fluid_equation_of_state="CLP",
                 w0_fld=p[3], wa_fld=p[4])
    else:
        kappa = p[4] if version == "SPIRAL" else 1.0
        beta = 0.0 if version == "SPIRAL0" else p[3]
        early = ON_EARLY if version in ON_BINS else beta     # TOURNAMENT_DEVIATIONS.md D1
        g = spiral_guess.mu1_guess(kappa, beta, wb, wc, h=h)   # closure guess from the late coupling (shooting refines it)
        a = dict(B.SPIRAL, h=h, omega_b=wb, omega_cdm=wc, tau_reio=F.TAU, output="", scf_coupling_beta=early,
                 scf_parameters=f"{kappa}, 0.0, {g}, 0.0, 0.0, 0.0")
        if version in ON_BINS:
            on = ON_BINS[version]; a.update(scf_beta1=beta * on[0], scf_beta2=beta * on[1], scf_beta3=beta * on[2])
    c = classy.Class(); c.set(a); c.compute()
    return c


def in_bounds(version, p):
    if version == "W0WA":
        return p[3] + p[4] < 0 and -3 <= p[3] <= 1 and -3 <= p[4] <= 2
    if version in ("FLAG1", "SPIRAL") or version in ON_BINS:
        if not 0.0 <= p[3] <= 0.15:
            return False
    if version == "SPIRAL":
        return 0.1 <= p[4] <= 2.0
    return True


def bao_pred(c, sets):
    rd = c.rs_drag(); out = []
    for lab, zs, vals, qs, cov in sets:
        pr = []
        for z, q in zip(zs, qs):
            dm = c.angular_distance(z) * (1 + z); hz = c.Hubble(z); dh = 1 / hz
            pr.append({"DM_over_rs": dm / rd * (147.78 if lab == "DR12" else 1), "DH_over_rs": dh / rd,
                       "DV_over_rs": (z * dm * dm * dh) ** (1 / 3) / rd, "bao_Hz_rs": hz * C * rd / 147.78}[q])
        out.append(np.array(pr))
    return out


def bao_chi2(c, sets):
    return float(sum((v - p) @ np.linalg.inv(cov) @ (v - p) for (_, _, v, _, cov), p in zip(sets, bao_pred(c, sets))))


TC = None


def chi2(version, p, sets):
    global TC
    if TC is None:
        TC = F.cmb_target()
    if not in_bounds(version, p):
        return 1e10
    try:
        c = model(version, p)
        bg = c.get_background(); zz = bg["z"][::-1]; dc = bg["comov. dist."][::-1]
        mu = 5 * np.log10(np.interp(F.SN["zHD"], zz, dc) * (1 + F.SN["zHEL"])) + 25
        th = c.get_current_derived_parameters(["100*theta_star"])["100*theta_star"]
        wce = float(np.interp(1090, zz, bg["(.)rho_cdm"][::-1])) / 1091 ** 3 / (100 / C) ** 2
        x = bao_chi2(c, sets) if sets else 0.0
        c.struct_cleanup(); c.empty()
    except Exception:
        return 1e10
    y = F.MU_OBS - mu; rs = y - (F.ONE @ F.SCi @ y) / (F.ONE @ F.SCi @ F.ONE)
    cmb = np.array([th, p[1], p[1] + wce])
    return float(x + rs @ F.SCi @ rs + np.sum(((cmb - TC) / F.CMB_S) ** 2))


def starts(version):
    t = [F.TR["H0"] / 100, F.TR["omega_b"], F.TR["omega_cdm"]]
    if version in ("LCDM", "SPIRAL0"):
        return [t, [t[0] + 0.005, t[1], t[2] - 0.001]]
    if version == "W0WA":
        return [t + [-0.9, -0.3], t + [-0.75, -0.8]]
    if version == "SPIRAL":
        return [t + [0.01, 1.0], t + [0.06, 1.0]]
    return [t + [0.01], t + [0.06]]


def fit(version, config):
    assert os.path.exists(RULE + ".sha256"), "rule not locked"
    f = os.path.join(OUTD, f"{version}_{config}.json")
    if os.path.exists(f):
        return
    sets = {"FULL": bao_desi(), "NOBAO": [], "SDSS": bao_sdss()}[config]
    runs = []
    for i, x0 in enumerate(starts(version)):
        sf = os.path.join(OUTD, f"{version}_{config}_s{i}.json")
        if os.path.exists(sf):
            r = json.load(open(sf)); runs.append((r["chi2"], r["params"])); continue
        r = minimize(lambda q: chi2(version, q, sets), x0, method="Nelder-Mead",
                     options={"xatol": 1e-6, "fatol": 1e-3, "maxiter": 1500, "maxfev": 1500})
        res = (float(r.fun), [float(v) for v in r.x]); runs.append(res)
        json.dump({"chi2": res[0], "params": res[1]}, open(sf, "w")); print(version, config, "start", i, round(res[0], 3), flush=True)
    best = min(runs)
    out = {"version": version, "config": config, "chi2": best[0], "params": best[1], "starts": [r[0] for r in runs]}
    if config == "NOBAO":
        c = model(version, best[1])
        out["pred_DESI"] = bao_chi2(c, bao_desi()); out["pred_SDSS"] = bao_chi2(c, bao_sdss()); c.struct_cleanup(); c.empty()
    json.dump(out, open(f, "w"), indent=1); print(version, config, round(best[0], 3), flush=True)


def score():
    R = {(v, c): json.load(open(os.path.join(OUTD, f"{v}_{c}.json"))) for v in VERSIONS for c in ("FULL", "NOBAO", "SDSS")}
    m1 = json.load(open(os.path.join(HERE, "m1", "full.json")))
    gate = abs(R[("LCDM", "FULL")]["chi2"] - m1["LCDM"][0]) <= 0.05 and abs(R[("FLAG1", "FULL")]["chi2"] - m1["FLAG1"][0]) <= 0.05
    L = {c: R[("LCDM", c)] for c in ("FULL", "NOBAO", "SDSS")}
    rows = {}
    for v, k in VERSIONS.items():
        d_full = R[(v, "FULL")]["chi2"] - L["FULL"]["chi2"]
        row = {"k": k, "dchi2_FULL": round(d_full, 3), "dAIC_FULL": round(d_full + 2 * k, 3),
               "dP_DESI": round(R[(v, "NOBAO")]["pred_DESI"] - L["NOBAO"]["pred_DESI"], 3),
               "dP_SDSS": round(R[(v, "NOBAO")]["pred_SDSS"] - L["NOBAO"]["pred_SDSS"], 3),
               "d_SDSS": round(R[(v, "SDSS")]["chi2"] - L["SDSS"]["chi2"], 3),
               "params_FULL": [round(x, 5) for x in R[(v, "FULL")]["params"]],
               "params_NOBAO": [round(x, 5) for x in R[(v, "NOBAO")]["params"]]}
        row["predicts"] = row["dP_DESI"] <= 0 and row["dP_SDSS"] <= 0 and row["d_SDSS"] <= 1
        rows[v] = row
    pred = [v for v in TWIST if rows[v]["predicts"]]
    if not gate:
        reading, best = "NO VERDICT (gate failed)", None
    elif not pred:
        best = min(TWIST, key=lambda v: rows[v]["dAIC_FULL"]); reading = f"NO VERSION PREDICTS (best fit only: {best})"
    else:
        best = min(pred, key=lambda v: rows[v]["dAIC_FULL"])
        reading = (f"BEST STANDARD VERSION: {best}" if rows[best]["dAIC_FULL"] < 0 else f"PREDICTS BUT NOT PREFERRED ({best})")
    out = {"rule": "PREREG_TOURNAMENT.md", "gate": {"LCDM_FULL": R[("LCDM", "FULL")]["chi2"], "FLAG1_FULL": R[("FLAG1", "FULL")]["chi2"],
           "m1_LCDM": m1["LCDM"][0], "m1_FLAG1": m1["FLAG1"][0], "pass": gate}, "rows": rows, "reading": reading}
    json.dump(out, open(os.path.join(AEG, "field_tests", "results", "tournament.json"), "w"), indent=1)
    print(json.dumps({"gate": out["gate"], "reading": reading,
                      "table": {v: {k: r[k] for k in ("dAIC_FULL", "dP_DESI", "dP_SDSS", "d_SDSS", "predicts")} for v, r in rows.items()}}, indent=1))


if __name__ == "__main__":
    a = sys.argv[1:]
    fit(a[1], a[2]) if a[0] == "fit" else score()
