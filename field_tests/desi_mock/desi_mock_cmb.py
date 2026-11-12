"""DESI-MOCK-CMB (field_tests/rules/PREREG_DESI_MOCK_CMB.md): the DESI-MOCK test with the full CMB likelihoods. PC.

    python desi_mock_cmb.py truth            -> mock_cmb_truth.npz   (FLAG-1 build; theory vectors at the truth)
    python desi_mock_cmb.py gate             -> mock_cmb_gate.json   (G-MC: every mocked data term chi2 <= 0.01)
    python desi_mock_cmb.py fit <LCDM|W0WA> <SN|noSN>  -> mock_cmb_part_<model>_<combo>.json
    python desi_mock_cmb.py score            -> mock_cmb_result.json

Each likelihood's data vector is replaced by its own theory vector at the truth (Asimov). Low-l Planck TT/EE are
replaced by tau ~ N(tau_truth, 0.0086) in the fits (no data vector exists to replace). Covariances unchanged.
Delta chi2 uses chi2 (all likelihoods) + 2 x the named Gaussian priors (calibrations, tau); their constants cancel.
"""
import json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); AEG = os.path.abspath(os.path.join(HERE, "..", ".."))
AX = os.path.join(AEG, "cmb-fit", "axiclass")
sys.path.insert(0, AX)
RULE = os.path.join(AEG, "field_tests", "rules", "PREREG_DESI_MOCK_CMB.md")
TRUTH_RUN = "ax_spa_spiraltwist_kappa1_nlfix"
TRUTH_NPZ = os.path.join(HERE, "mock_cmb_truth.npz")
TAU_SIGMA = 0.0086
LOWL = ("planck_2018_lowl.TT", "planck_2018_lowl.EE")
MOCKED = ("act_dr6_cmbonly.PlanckActCut", "act_dr6_cmbonly.ACTDR6CMBonly", "act_dr6_lenslike.ACTDR6LensLike",
          "spt3g_d1_tne_lite", "bao.desi_dr2.desi_bao_all", "sn.pantheonplus")
CAP = {}            # name -> theory vector captured at the truth
MOCK = {}           # name -> mock data vector to install


def _stub_free_imports():
    import candl.interface  # noqa: F401  (real likelihoods: this test needs them)
    import spt_candl_data   # noqa: F401


def _act_theory(self, cl, A_act, P_act):
    """Same arithmetic as ACTDR6CMBonly.chi_square, returning the binned theory vector."""
    ps = np.zeros_like(self.data_vec)
    for m in self.spec_meta:
        win = m["window"].weight.T; ls = m["window"].values; pol = m["pol"]
        dat = cl[pol][ls] / (A_act * A_act)
        if pol[0] == "e":
            dat = dat / P_act
        if pol[1] == "e":
            dat = dat / P_act
        ps[m["idx"]] = win @ dat
    return ps


def install_hooks(mode):
    """mode 'capture': record each likelihood's theory vector at the next evaluation; 'mock': swap in MOCK data."""
    from act_dr6_cmbonly.act_dr6_cmbonly import ACTDR6CMBonly
    from act_dr6_cmbonly.PlanckActCut import PlanckActCut
    import act_dr6_lenslike.act_dr6_lenslike as LL
    from candl.interface import CandlCobayaLikelihood
    from cobaya.likelihoods.base_classes import BAO
    from cobaya.likelihoods.sn.pantheonplus import PantheonPlus

    def after(cls, fn):
        orig = cls.initialize

        def init(self):
            orig(self); fn(self)
        cls.initialize = init

    # ACT DR6 CMB-only
    def act(self):
        n = self.get_name()
        if mode == "mock":
            self.data_vec = np.array(MOCK[n], dtype=float)
        else:
            orig = self.chi_square

            def chi_square(cl, A_act, P_act):
                CAP[n] = _act_theory(self, cl, A_act, P_act); return orig(cl, A_act, P_act)
            self.chi_square = chi_square
    after(ACTDR6CMBonly, act)

    # Planck cut (plik-lite): theory = X_data - diff
    def plik(self):
        n = self.get_name()
        if mode == "mock":
            self.X_data = np.array(MOCK[n], dtype=float)
        else:
            orig = self._fast_chi_squared

            def fast(invcov, diff):
                CAP[n] = np.array(self.X_data - diff); return orig(invcov, diff)
            self._fast_chi_squared = fast
    after(PlanckActCut, plik)

    # ACT DR6 lensing: module-level generic_lnlike returns the binned theory on request
    if mode == "mock":
        def lens(self):
            self.data["data_binned_clkk"] = np.array(MOCK[self.get_name()], dtype=float)
        after(LL.ACTDR6LensLike, lens)
    else:
        orig_g = LL.generic_lnlike

        def generic_lnlike(*a, **k):
            k["return_theory"] = True
            lnl, th = orig_g(*a, **k); CAP["act_dr6_lenslike.ACTDR6LensLike"] = np.array(th); return lnl
        LL.generic_lnlike = generic_lnlike

    # SPT-3G D1 lite (candl)
    def spt(self):
        n = self.get_name(); L = self.candl_like
        if mode == "mock":
            L._data_bandpowers = np.array(MOCK[n], dtype=float)
            L.data_bandpowers = L._data_bandpowers
        else:
            orig = L.log_like

            def log_like(pars):
                CAP[n] = np.array(L.bin_model_specs(L.get_model_specs(pars))); return orig(pars)
            L.log_like = log_like
    after(CandlCobayaLikelihood, spt)

    # DESI DR2 BAO: logpdf(theory vector in data order)
    def bao(self):
        n = self.get_name()
        if mode == "mock":
            self.data["value"] = np.array(MOCK[n], dtype=float)
        else:
            orig = self.logpdf

            def logpdf(x):
                CAP[n] = np.array(x, dtype=float); return orig(x)
            self.logpdf = logpdf
    after(BAO, bao)

    # Pantheon+ (M marginalised in invcov): mag -> lumdists at the truth
    def sn(self):
        n = self.get_name()
        if mode == "mock":
            self.mag = np.array(MOCK[n], dtype=float)
        else:
            orig = self.alpha_beta_logp

            def abl(lumdists, *a, **k):
                CAP[n] = np.array(lumdists, dtype=float); return orig(lumdists, *a, **k)
            self.alpha_beta_logp = abl
    after(PantheonPlus, sn)


def _truth_point():
    return json.load(open(os.path.join(AEG, "cmb-fit", "results", f"cmp_{TRUTH_RUN}_s8y6.json")))["minimum"]


def _truth_model():
    import early_late_spa as E
    info = E.make(TRUTH_RUN)
    for k in LOWL:
        info["likelihood"].pop(k)
    for k in ("sampler", "output", "resume", "force"):
        info.pop(k, None)
    from cobaya.model import get_model
    m = get_model(info)
    st = _truth_point()
    pt = {p: st[p] for p in m.parameterization.sampled_params()}
    return m, pt


def _build_first(run):
    """Load the right classy build before any likelihood import pulls in another one."""
    import early_late_spa as E
    E._maybe_coupled(run)


def truth():
    _build_first(TRUTH_RUN)
    install_hooks("capture")
    m, pt = _truth_model()
    ll = m.loglikes(pt, as_dict=True)[0]
    real = {k: -2 * float(v) for k, v in ll.items()}
    missing = [n for n in MOCKED if n not in CAP]
    assert not missing, f"no theory captured for {missing}"
    np.savez(TRUTH_NPZ, **{n: CAP[n] for n in MOCKED}, tau=_truth_point()["tau_reio"])
    json.dump({"real_chi2_at_truth": real, "point": pt}, open(os.path.join(HERE, "mock_cmb_truth.json"), "w"), indent=1)
    print("truth saved", real, flush=True)


def _load_mock():
    z = np.load(TRUTH_NPZ)
    MOCK.update({n: z[n] for n in MOCKED})
    return float(z["tau"])


def gate():
    assert os.path.exists(RULE + ".sha256"), "rule not locked"
    _build_first(TRUTH_RUN)
    _load_mock(); install_hooks("mock")
    m, pt = _truth_model()
    ll = m.loglikes(pt, as_dict=True)[0]
    mock = {k: -2 * float(v) for k, v in ll.items()}
    real = json.load(open(os.path.join(HERE, "mock_cmb_truth.json")))["real_chi2_at_truth"]
    rows = {n: {"mock_chi2": mock[n], "real_chi2": real[n], "pass": abs(mock[n]) <= 0.01 and abs(real[n]) > 0.01}
            for n in MOCKED}
    ok = all(r["pass"] for r in rows.values())
    json.dump({"rows": rows, "all_pass": ok}, open(os.path.join(HERE, "mock_cmb_gate.json"), "w"), indent=1)
    print("G-MC", "PASSED" if ok else "FAILED", rows, flush=True)
    sys.exit(0 if ok else 1)


def fit(model, combo):
    assert os.path.exists(RULE + ".sha256"), "rule not locked"
    g = json.load(open(os.path.join(HERE, "mock_cmb_gate.json")))
    assert g["all_pass"], "G-MC failed: no fits"
    tau_t = _load_mock(); install_hooks("mock")
    import early_late_spa as E
    from cobaya.run import run
    name = {"LCDM": "ax_spa_lcdm_halofit", "W0WA": "ax_spa_w0wa_halofit"}[model]
    E._maybe_coupled(name)
    info = E.make(name)
    for k in LOWL:
        info["likelihood"].pop(k)
    if combo == "noSN":
        info["likelihood"].pop("sn.pantheonplus")
    info["prior"]["tau_mock"] = f"lambda tau_reio: stats.norm.logpdf(tau_reio, loc={tau_t!r}, scale={TAU_SIGMA})"
    st = _truth_point()
    for k, p in info["params"].items():
        if isinstance(p, dict) and "ref" in p:
            if k in st:
                p["ref"]["loc"] = float(st[k])
            elif k == "w0_fld":
                p["ref"]["loc"] = -1.0
            elif k == "wa_fld":
                p["ref"]["loc"] = 0.0
    info["sampler"] = {"minimize": {"method": "bobyqa", "best_of": 4}}
    info["output"] = os.path.join(AEG, "cmb-fit", "results", "chains", f"mockcmb_{model}_{combo}")
    info["force"] = True; info["resume"] = False
    _, sampler = run(info)
    try:
        mn = sampler.products()["minimum"]
        row = {k: float(mn[k]) for k in mn.data.columns if k != "weight"}
    except Exception:   # fall back to Cobaya's own text output
        f = info["output"] + ".minimum.txt"
        head = open(f).readline().lstrip("#").split()
        vals = np.loadtxt(f, ndmin=2)[0]
        row = {k: float(v) for k, v in zip(head, vals) if k != "weight"}
    named = sum(v for k, v in row.items() if k.startswith("minuslogprior__") and k != "minuslogprior__0")
    out = {"model": model, "combo": combo, "chi2": row["chi2"], "chi2_eff": row["chi2"] + 2 * named, "minimum": row}
    json.dump(out, open(os.path.join(HERE, f"mock_cmb_part_{model}_{combo}.json"), "w"), indent=1)
    print(out["chi2_eff"], flush=True)


def score():
    from scipy.stats import chi2 as C2, norm
    res = {}
    for combo, tag in (("SN", "CMB+BAO+SN"), ("noSN", "CMB+BAO")):
        try:
            L = json.load(open(os.path.join(HERE, f"mock_cmb_part_LCDM_{combo}.json")))
            W = json.load(open(os.path.join(HERE, f"mock_cmb_part_W0WA_{combo}.json")))
        except FileNotFoundError:
            res[tag] = "NO VERDICT (fit missing)"; continue
        d = L["chi2_eff"] - W["chi2_eff"]
        res[tag] = {"delta_chi2": d, "sigma_2dof": float(norm.isf(C2.sf(max(d, 0), 2) / 2)),
                    "w0": W["minimum"]["w0_fld"], "wa": W["minimum"]["wa_fld"],
                    "H0_LCDM": L["minimum"].get("H0"), "H0_W0WA": W["minimum"].get("H0")}
    r = res["CMB+BAO+SN"]
    if not isinstance(r, dict):
        reading = "NO VERDICT"
    elif r["sigma_2dof"] >= 2 and r["wa"] < 0 and r["w0"] > -1:
        reading = "REPRODUCES DESI'S SIGNAL"
    elif r["sigma_2dof"] >= 1 and r["wa"] < 0 and r["w0"] > -1:
        reading = "PARTIAL"
    else:
        reading = "DOES NOT"
    res["reading"] = reading
    if isinstance(r, dict):
        res["vs_DESI_DR2_CMB_PantheonPlus"] = {"w0_sigma": (r["w0"] + 0.838) / 0.055, "wa_sigma": (r["wa"] + 0.62) / 0.21}
        cp = os.path.join(HERE, "desi_mock_result.json")   # side comparison only; see DESI_MOCK_CMB_DEVIATIONS.md D1
        if os.path.exists(cp):
            comp = json.load(open(cp))["BAO+CMB+SN"]
            res["compressed_DESI_MOCK"] = {k: comp[k] for k in ("delta_chi2", "sigma_2dof", "w0", "wa")}
        else:
            res["compressed_DESI_MOCK"] = "not available (desi_mock_result.json missing); reading unaffected"
    json.dump(res, open(os.path.join(HERE, "mock_cmb_result.json"), "w"), indent=1)
    print(reading, json.dumps(res, indent=1))


if __name__ == "__main__":
    {"truth": truth, "gate": gate, "score": score,
     "fit": lambda: fit(sys.argv[2], sys.argv[3])}[sys.argv[1]]()
