"""EXPLORATORY (not pre-registered): growth rate f*sigma8 of the stored best fits vs the SDSS/BOSS/eBOSS DR16 consensus
BAO+RSD fsigma8 (sdss4.org final table: MGS 0.15, BOSS 0.38/0.51, eBOSS LRG 0.70, ELG 0.85, QSO 1.48). Diagonal errors only
(the published BAO-fsigma8 correlations and the small BOSS bin overlap are ignored: an approximate chi2). No fitting.
    python fs8_check.py <run> [<run> ...]   (each run with its own build; prints one JSON line per run)"""
import sys, os, json, types
import numpy as np
DATA = [(0.15, 0.53, 0.16), (0.38, 0.497, 0.045), (0.51, 0.459, 0.038), (0.70, 0.473, 0.041), (0.85, 0.315, 0.095), (1.48, 0.462, 0.045)]
for n in ("candl", "candl.interface", "spt_candl_data"):
    sys.modules.setdefault(n, types.SimpleNamespace(CandlCobayaLikelihood=None, SPT3G_D1_TnE=None, interface=None))
sys.modules["candl"].interface = sys.modules["candl.interface"]
HERE = os.path.dirname(os.path.abspath(__file__)); AEG = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(AEG, "cmb-fit", "axiclass"))
import early_late_spa as E
run = sys.argv[1]
base = run.replace("_s8y6_more", "").replace("_s8y6", "")
E._maybe_coupled(base)
import classy
info = E.make(base); st = json.load(open(f"{E.OUT}/cmp_{run}.json"))["minimum"]
a = dict(info["theory"]["classytwist"]["extra_args"])
a.update({"A_s": 1e-10 * np.exp(st["logA"]), "n_s": st["n_s"], "100*theta_s": st["theta_s_1e2"], "omega_b": st["omega_b"],
          "omega_cdm": st["omega_cdm"], "tau_reio": st["tau_reio"], "output": "mPk", "z_max_pk": 2.0, "P_k_max_1/Mpc": 2.0})
for k in ("lensing", "l_max_scalars", "non_linear"): a.pop(k, None)
if "scf_coupling_beta" in st:
    import spiral_guess
    k = st.get("spiral_kappa", 1.0); b = st["scf_coupling_beta"]; a["scf_coupling_beta"] = b
    a["scf_parameters"] = f"{k}, 0.0, {spiral_guess.mu1_guess(k, b, st['omega_b'], st['omega_cdm'])}, 0.0, 0.0, 0.0"
c = classy.Class(); c.set(a); c.compute(); h = c.h()
th = [c.scale_independent_growth_factor_f(z) * c.sigma(8 / h, z) for z, _, _ in DATA]
chi2 = sum(((t - v) / e) ** 2 for t, (z, v, e) in zip(th, DATA))
print(json.dumps({"run": run, "fsigma8": [round(float(t), 4) for t in th], "chi2_diag": round(float(chi2), 3), "n": len(DATA)}))
