"""AEGIS CMB fit — full Boltzmann-code test of the torsion-born EDE model.

The torsion field (canonical Barbero–Immirzi pseudoscalar, V = Lambda^4 [1 - cos(phi/F)]^n) has the
same Lagrangian as CAMB's built-in EarlyQuintessence model, V = m^2 f^2 [1 - cos(phi/f)]^n.
So the full CMB + BAO + SN test is run with CAMB (the code Planck uses) and Cobaya, both standard.

Steps (run in order; each writes to results/):
  python cmbfit.py validate   reproduce CAMB's documented example (H0 = 73.2113); proves the install
  python cmbfit.py point      one full-likelihood evaluation at the paper's n=3 point (timing check)
  python cmbfit.py minimize   best fits: LCDM vs torsion EDE, without and with SH0ES (the decisive test)
  python cmbfit.py mcmc       posterior chains for the torsion EDE model (long; optional)
  python cmbfit.py report     summary table from whatever has finished

Data: Planck 2018 (low-l TT, low-l EE, high-l TTTEEE plik-lite, lensing), DESI DR2 BAO, Pantheon+,
optionally SH0ES via the Pantheon+SH0ES calibrated likelihood.
"""
import copy, json, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PACKAGES = os.path.join(HERE, "packages")
RESULTS = os.path.join(HERE, "results")
os.makedirs(RESULTS, exist_ok=True)

def lower_priority():
    try:
        if os.name == "nt":
            import ctypes
            ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x4000)
        else:
            os.nice(10)
    except Exception:
        pass

# ----------------------------------------------------------------------------- model blocks
CAMB_COMMON = dict(
    halofit_version="mead", bbn_predictor="PArthENoPE_880.2_standard.dat",
    lens_potential_accuracy=1, num_massive_neutrinos=1, nnu=3.044, theta_H0_range=[20, 100],
)
EDE_EXTRA = dict(dark_energy_model="EarlyQuintessence", n=3, use_zc=True)

BASE_PARAMS = {
    "logA": {"prior": {"min": 1.61, "max": 3.91}, "ref": {"dist": "norm", "loc": 3.05, "scale": 0.001},
             "proposal": 0.001, "latex": r"\log(10^{10} A_\mathrm{s})", "drop": True},
    "As": {"value": "lambda logA: 1e-10*np.exp(logA)", "latex": "A_\\mathrm{s}"},
    "ns": {"prior": {"min": 0.8, "max": 1.2}, "ref": {"dist": "norm", "loc": 0.965, "scale": 0.004},
           "proposal": 0.002, "latex": "n_\\mathrm{s}"},
    "theta_s_100": {"prior": {"min": 0.5, "max": 10}, "ref": {"dist": "norm", "loc": 1.0411, "scale": 0.0004},
                    "proposal": 0.0002, "latex": r"100\theta_\ast", "drop": True},
    "thetastar": {"value": "lambda theta_s_100: 1.e-2*theta_s_100", "derived": False},
    "H0": {"latex": "H_0"},
    "ombh2": {"prior": {"min": 0.005, "max": 0.1}, "ref": {"dist": "norm", "loc": 0.0224, "scale": 0.0001},
              "proposal": 0.0001, "latex": r"\Omega_\mathrm{b} h^2"},
    "omch2": {"prior": {"min": 0.001, "max": 0.99}, "ref": {"dist": "norm", "loc": 0.12, "scale": 0.001},
              "proposal": 0.0005, "latex": r"\Omega_\mathrm{c} h^2"},
    "tau": {"prior": {"min": 0.01, "max": 0.8}, "ref": {"dist": "norm", "loc": 0.055, "scale": 0.006},
            "proposal": 0.003, "latex": r"\tau_\mathrm{reio}"},
    "mnu": 0.06,
    "omegam": {"latex": r"\Omega_\mathrm{m}"},
    "sigma8": {"latex": r"\sigma_8"},
    "rdrag": {"latex": r"r_\mathrm{drag}"},
}
EDE_PARAMS = {
    "fde_zc": {"prior": {"min": 0.001, "max": 0.3}, "ref": {"dist": "norm", "loc": 0.08, "scale": 0.01},
               "proposal": 0.01, "latex": r"f_\mathrm{EDE}(z_c)"},
    "log10_zc": {"prior": {"min": 3.0, "max": 4.3}, "ref": {"dist": "norm", "loc": 3.55, "scale": 0.05},
                 "proposal": 0.05, "latex": r"\log_{10} z_c", "drop": True},
    "zc": {"value": "lambda log10_zc: 10**log10_zc", "latex": "z_c"},
    "theta_i": {"prior": {"min": 0.1, "max": 3.1}, "ref": {"dist": "norm", "loc": 2.8, "scale": 0.05},
                "proposal": 0.1, "latex": r"\theta_i"},
}

LIKES_BASE = {
    "planck_2018_lowl.TT": None,
    "planck_2018_lowl.EE": None,
    "planck_2018_highl_plik.TTTEEE_lite_native": None,
    "planck_2018_lensing.native": None,
    "bao.desi_dr2.desi_bao_all": None,
}
SN_NO_SHOES = {"sn.pantheonplus": None}
SN_WITH_SHOES = {"sn.pantheonplusshoes": None}

def make_info(model="ede", shoes=False, sampler=None, output=None):
    extra = dict(CAMB_COMMON); params = copy.deepcopy(BASE_PARAMS)
    if model == "ede":
        extra.update(EDE_EXTRA); params.update(copy.deepcopy(EDE_PARAMS))
    likes = dict(LIKES_BASE); likes.update(SN_WITH_SHOES if shoes else SN_NO_SHOES)
    info = {"theory": {"camb": {"extra_args": extra, "stop_at_error": False}},
            "likelihood": likes, "params": params, "packages_path": PACKAGES}
    if sampler: info["sampler"] = sampler
    if output: info["output"] = output
    return info

RUNS = [("lcdm", False), ("ede", False), ("lcdm", True), ("ede", True)]
def run_name(model, shoes):
    return f"{model}_{'shoes' if shoes else 'noshoes'}"

# ----------------------------------------------------------------------------- steps
def validate():
    """Reproduce the EarlyQuintessence example in CAMB's own documentation (CAMBdemo)."""
    import camb
    thetastar, n = 0.01044341764253, 3
    lcdm = camb.get_results(camb.set_params(ombh2=0.022, omch2=0.122, thetastar=thetastar))
    pars = camb.set_params(ombh2=0.022, omch2=0.122, m=8e-53, f=0.05, n=n, theta_i=3.1, use_zc=True,
                           zc=1e4, fde_zc=0.1, dark_energy_model="EarlyQuintessence", thetastar=thetastar)
    t0 = time.time(); ede = camb.get_results(pars); dt = time.time() - t0
    out = dict(camb_version=camb.__version__, H0_LCDM=lcdm.Params.H0, H0_EDE=ede.Params.H0,
               expected_H0_EDE=73.21133477061629, seconds=dt,
               m=ede.Params.DarkEnergy.m, f=ede.Params.DarkEnergy.f)
    out["pass"] = abs(out["H0_EDE"] - out["expected_H0_EDE"]) < 0.05
    json.dump(out, open(os.path.join(RESULTS, "validate.json"), "w"), indent=2)
    print(json.dumps(out, indent=2))
    print("VALIDATION", "PASSED" if out["pass"] else "FAILED (H0 differs from CAMB's documented value)")
    return out

def point():
    """One full-likelihood evaluation at the paper's n=3 torsion point (checks data + timing)."""
    from cobaya.model import get_model
    info = make_info("ede", shoes=False)
    model = get_model(info)
    names = list(model.parameterization.sampled_params())
    p = dict(zip(names, model.prior.reference()))              # reference values for every sampled parameter
    p.update(dict(logA=3.05, ns=0.97, theta_s_100=1.0411, ombh2=0.0224, omch2=0.13, tau=0.055,
                  fde_zc=0.10, log10_zc=3.55, theta_i=2.8))     # the paper's n=3 torsion point
    t0 = time.time(); lp = model.logposterior(p, as_dict=True); dt = time.time() - t0
    out = dict(seconds=dt, loglikes=lp.get("loglikes"), derived=lp.get("derived"))
    json.dump(out, open(os.path.join(RESULTS, "point.json"), "w"), indent=2, default=float)
    print(json.dumps(out, indent=2, default=float))

def minimize(which=None):
    from cobaya import run
    for model, shoes in RUNS:
        name = run_name(model, shoes)
        if which and which != name:
            continue
        if os.path.exists(os.path.join(RESULTS, name + ".json")):
            print("already done:", name); continue
        print(f"\n=== minimize {name} ===", flush=True)
        info = make_info(model, shoes, sampler={"minimize": {"method": "bobyqa", "best_of": 2}},
                         output=os.path.join(RESULTS, "chains", name))
        info["resume"] = True
        t0 = time.time()
        upd, sampler = run(info)
        res = sampler.products()
        row = {k: float(v) for k, v in res["minimum"].data.iloc[0].items()
               if isinstance(v, (int, float, np.integer, np.floating))}
        out = dict(run=name, seconds=time.time() - t0, minimum=row)
        json.dump(out, open(os.path.join(RESULTS, name + ".json"), "w"), indent=2)
        print(f"done {name}: H0={row.get('H0')}, chi2 pieces: "
              f"{ {k: round(v, 2) for k, v in row.items() if k.startswith('chi2')} }", flush=True)

def mcmc(shoes=False):
    from cobaya import run
    name = "mcmc_" + run_name("ede", shoes)
    info = make_info("ede", shoes, output=os.path.join(RESULTS, "chains", name),
                     sampler={"mcmc": {"Rminus1_stop": 0.02, "max_tries": 10000, "drag": True,
                                       "oversample_power": 0.4, "proposal_scale": 1.9}})
    info["resume"] = True
    run(info)

def chi2_eff(m):
    """chi2 of all likelihoods + the Gaussian Planck calibration prior A_planck ~ N(1, 0.0025), as in the cloud fits
    (flat-prior constants excluded), so LCDM and EDE are compared fairly."""
    tot = m.get("chi2", sum(v for k, v in m.items() if k.startswith("chi2__")))
    return tot + ((m.get("A_planck", 1.0) - 1.0) / 0.0025) ** 2

def report():
    rows = {}
    for model, shoes in RUNS:
        f = os.path.join(RESULTS, run_name(model, shoes) + ".json")
        if os.path.exists(f):
            rows[run_name(model, shoes)] = json.load(open(f))
    lines = ["| Run | chi2_eff | Planck | DESI BAO | SNe | H0 | f_EDE | omch2 |", "|---|---|---|---|---|---|---|---|"]
    def pick(r, key):
        return sum(v for k, v in r["minimum"].items() if k.startswith("chi2__") and key in k)
    for name, r in rows.items():
        m = r["minimum"]; tot = chi2_eff(m)
        lines.append(f"| {name} | {tot:.2f} | {pick(r, 'planck'):.2f} | {pick(r, 'bao'):.2f} | {pick(r, 'sn.'):.2f} | "
                     f"{m.get('H0', float('nan')):.2f} | {m.get('fde_zc', 0):.3f} | {m.get('omch2', float('nan')):.4f} |")
    for shoes in (False, True):
        a, b = rows.get(run_name("lcdm", shoes)), rows.get(run_name("ede", shoes))
        if a and b:
            ca = chi2_eff(a["minimum"]); cb = chi2_eff(b["minimum"])
            if ca is not None and cb is not None:
                lines.append(f"\n{'With' if shoes else 'Without'} SH0ES: delta chi2 (EDE - LCDM) = {cb - ca:+.2f} "
                             f"with 3 extra parameters (delta AIC = {cb - ca + 6:+.2f})")
    text = "\n".join(lines)
    open(os.path.join(RESULTS, "REPORT.md"), "w").write("# CMB fit results\n\n" + text + "\n")
    print(text)

if __name__ == "__main__":
    lower_priority()
    step = sys.argv[1] if len(sys.argv) > 1 else "validate"
    {"validate": validate, "point": point, "report": report,
     "minimize": lambda: minimize(sys.argv[2] if len(sys.argv) > 2 else None),
     "mcmc": lambda: mcmc(shoes=len(sys.argv) > 2 and sys.argv[2] == "shoes")}[step]()
