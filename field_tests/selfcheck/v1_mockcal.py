"""SELFCHECK V1 (field_tests/rules/PREREG_SELFCHECK.md): fake-universe calibration of FLAG-1's local significance.
Compressed likelihood (DESI DR2 BAO + Pantheon+ with M marginalised + compressed CMB), background only, coupled build
for both models (LCDM through its Lambda settings).
    python v1_mockcal.py real                 -> v1/real.json  (real-data anchor)
    python v1_mockcal.py mocks <worker> <W>   -> v1/mock_<seed>.json for seeds = worker+1, worker+1+W, ... <= 200
    python v1_mockcal.py score                -> ../results/selfcheck_v1.json
Deviation D1 (logged in SELFCHECK_DEVIATIONS.md before any run): the compressed-CMB data vector for the real-data
anchor is the LCDM+S8 Pantheon+ full fit's (100 theta*, omega_b, omega_b + omega_c), the same vector as the mock truth."""
import json, os, sys, types
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); AEG = os.path.abspath(os.path.join(HERE, "..", ".."))
RULE = os.path.join(AEG, "field_tests", "rules", "PREREG_SELFCHECK.md")
OUTD = os.path.join(HERE, "v1"); os.makedirs(OUTD, exist_ok=True)
assert os.path.exists(RULE + ".sha256"), "rule not locked"
for n in ("candl", "candl.interface", "spt_candl_data"):
    sys.modules.setdefault(n, types.SimpleNamespace(CandlCobayaLikelihood=None, SPT3G_D1_TnE=None, interface=None))
sys.modules["candl"].interface = sys.modules["candl.interface"]
sys.path.insert(0, os.path.join(AEG, "cmb-fit", "axiclass"))
import early_late_spa as E, spiral_guess
RUN = "ax_spa_spiraltwist_kappa1_nlfix"; E._maybe_coupled(RUN)
import classy
from scipy.optimize import minimize
D = os.path.join(AEG, "cmb-fit", "packages", "data"); C = 299792.458
bm = np.loadtxt(os.path.join(D, "bao_data", "desi_bao_dr2", "desi_gaussian_bao_ALL_GCcomb_mean.txt"), dtype=str)
BZ, BV, BQ = bm[:, 0].astype(float), bm[:, 1].astype(float), bm[:, 2]
BCOV = np.loadtxt(os.path.join(D, "bao_data", "desi_bao_dr2", "desi_gaussian_bao_ALL_GCcomb_cov.txt")); BCi = np.linalg.inv(BCOV)
SD = os.path.join(D, "sn_data", "PantheonPlus")
SN = np.genfromtxt(os.path.join(SD, "Pantheon+SH0ES.dat"), names=True, dtype=None, encoding=None)
SC = np.loadtxt(os.path.join(SD, "Pantheon+SH0ES_STAT+SYS.cov"))[1:].reshape(len(SN), len(SN))
msk = (SN["zHD"] > 0.01) & (SN["IS_CALIBRATOR"] == 0); SN = SN[msk]; SCOV = SC[np.ix_(msk, msk)]; SCi = np.linalg.inv(SCOV)
ONE = np.ones(len(SN)); CMB_S = np.array([0.00030, 0.00015, 0.0011])
info = E.make(RUN)
SPIRAL = {k: v for k, v in info["theory"]["classytwist"]["extra_args"].items() if k not in ("lensing", "l_max_scalars", "non_linear")}
LCDM = {k: v for k, v in E.BASE_ARGS.items() if k not in ("l_max_scalars", "non_linear")}
TAU = 0.0636
TR = json.load(open(os.path.join(E.OUT, "cmp_ax_spa_lcdm_halofit_s8y6.json")))["minimum"]


def model(h, wb, wc, beta=None):
    if beta is None:
        a = dict(LCDM, h=h, omega_b=wb, omega_cdm=wc, tau_reio=TAU, output="")
    else:
        g = spiral_guess.mu1_guess(1.0, beta, wb, wc, h=h)
        a = dict(SPIRAL, h=h, omega_b=wb, omega_cdm=wc, tau_reio=TAU, output="", scf_coupling_beta=beta,
                 scf_parameters=f"1.0, 0.0, {g}, 0.0, 0.0, 0.0")
    c = classy.Class(); c.set(a); c.compute()
    rd = c.rs_drag(); bg = c.get_background()
    zz = bg["z"][::-1]; dc = bg["comov. dist."][::-1]; hz = bg["H [1/Mpc]"][::-1]
    DC = lambda z: np.interp(z, zz, dc)
    dm_b = DC(BZ); dh_b = 1 / np.interp(BZ, zz, hz)
    vals = {"DM_over_rs": dm_b / rd, "DH_over_rs": dh_b / rd, "DV_over_rs": (BZ * dm_b * dm_b * dh_b) ** (1 / 3) / rd}
    bao = [vals[q][i] for i, q in enumerate(BQ)]
    mu = 5 * np.log10(DC(SN["zHD"]) * (1 + SN["zHEL"])) + 25
    th = c.get_current_derived_parameters(["100*theta_star"])["100*theta_star"]
    rc = bg["(.)rho_cdm"][::-1]
    wce = float(np.interp(1090, zz, rc)) / 1091 ** 3 / (100 / C) ** 2 if beta is not None else wc
    c.struct_cleanup(); c.empty()
    return np.array(bao), mu, np.array([th, wb, wb + wce])


def chi2(p, data, coupled):
    h, wb, wc = p[:3]; beta = p[3] if coupled else None
    if coupled and not (0.0 <= beta <= 0.12):
        return 1e10
    try:
        bao, mu, cmb = model(h, wb, wc, beta)
    except Exception:
        return 1e10
    rb = data["bao"] - bao; y = data["mu"] - mu
    rs = y - (ONE @ SCi @ y) / (ONE @ SCi @ ONE)
    return float(rb @ BCi @ rb + rs @ SCi @ rs + np.sum(((cmb - data["cmb"]) / CMB_S) ** 2))


def fitpair(data):
    t = [TR["H0"] / 100, TR["omega_b"], TR["omega_cdm"]]
    starts = [t, [t[0] - 0.01, t[1] + 0.0002, t[2] + 0.002], [t[0] + 0.01, t[1] - 0.0002, t[2] - 0.002]]
    out = {}
    for coupled, betas in ((False, [None] * 3), (True, [0.01, 0.04, 0.08])):
        runs = []
        for s, b in zip(starts, betas):
            x0 = s + ([b] if coupled else [])
            r = minimize(lambda q: chi2(q, data, coupled), x0, method="Nelder-Mead",
                         options={"xatol": 1e-6, "fatol": 1e-3, "maxiter": 1500, "maxfev": 1500,
                                  "initial_simplex": None})
            runs.append((float(r.fun), [float(v) for v in r.x]))
        out["FLAG1" if coupled else "LCDM"] = min(runs)
    out["delta"] = out["FLAG1"][0] - out["LCDM"][0]
    return out


def truth_vectors():
    bao, mu, cmb = model(TR["H0"] / 100, TR["omega_b"], TR["omega_cdm"])
    return bao, mu, cmb


if __name__ == "__main__":
    mode = sys.argv[1]
    TB, TMU, TC = truth_vectors()
    if mode == "real":
        data = {"bao": BV, "mu": SN["m_b_corr"].astype(float), "cmb": TC}
        r = fitpair(data); json.dump(r, open(os.path.join(OUTD, "real.json"), "w"), indent=1); print(r)
    elif mode == "mocks":
        w, W = int(sys.argv[2]), int(sys.argv[3])
        LB, LS = np.linalg.cholesky(BCOV), np.linalg.cholesky(SCOV)
        for seed in range(w + 1, 201, W):
            f = os.path.join(OUTD, f"mock_{seed:03d}.json")
            if os.path.exists(f):
                continue
            rng = np.random.default_rng(seed)
            data = {"bao": TB + LB @ rng.standard_normal(len(TB)), "mu": TMU + LS @ rng.standard_normal(len(TMU)),
                    "cmb": TC + CMB_S * rng.standard_normal(3)}
            r = fitpair(data); r["seed"] = seed
            json.dump(r, open(f, "w")); print(seed, round(r["delta"], 3), r["FLAG1"][1][3], flush=True)
    elif mode == "score":
        from scipy import stats
        real = json.load(open(os.path.join(OUTD, "real.json"))); dr = real["delta"]
        ms = [json.load(open(os.path.join(OUTD, f))) for f in sorted(os.listdir(OUTD)) if f.startswith("mock_")]
        d = np.array([m["delta"] for m in ms]); n = len(d); k = int(np.sum(d <= dr))
        pe = k / n; lo, hi = stats.beta.ppf([0.16, 0.84], k + 0.5, n - k + 0.5)
        pw = float(stats.chi2.sf(-dr, 1)) if dr < 0 else 1.0
        sig = lambda p: float(stats.norm.isf(p / 2)) if 0 < p < 1 else (0.0 if p >= 1 else float("inf"))
        reading = ("NO READING (fewer than 100 mocks)" if n < 100 else "WILKS ADEQUATE" if pw / 2 <= pe <= 2 * pw
                   else "WILKS OVERSTATES" if pe > 2 * pw else "WILKS UNDERSTATES")
        pg = 1 - (1 - max(pe, 0.5 / n)) ** 66
        out = {"rule": "PREREG_SELFCHECK.md V1", "n_mock": n, "delta_real_compressed": dr, "k_le_real": k,
               "p_emp": pe, "p_emp_68": [float(lo), float(hi)], "p_wilks": pw, "sigma_emp": sig(max(pe, 0.5 / n)),
               "sigma_wilks": sig(pw), "sigma_global_emp_N66": sig(pg),
               "beta_at_boundary_share": float(np.mean([m["FLAG1"][1][3] < 1e-3 for m in ms])),
               "delta_quantiles": {q: float(np.quantile(d, q)) for q in (0.01, 0.05, 0.16, 0.5, 0.84)},
               "reading": reading}
        json.dump(out, open(os.path.join(AEG, "field_tests", "results", "selfcheck_v1.json"), "w"), indent=1); print(out)
