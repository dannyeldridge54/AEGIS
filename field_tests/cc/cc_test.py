"""CC: cosmic-chronometer H(z) vs the stored FLAG-1 and LCDM fits (rule: field_tests/rules/PREREG_CC.md). AI-assisted.
    python cc_test.py      -> field_tests/results/cc.json      (coupled build, both models)"""
import json, os, sys, types
import numpy as np
from scipy.stats import chi2 as C2

HERE = os.path.dirname(os.path.abspath(__file__)); AEG = os.path.abspath(os.path.join(HERE, "..", ".."))
RULE = os.path.join(AEG, "field_tests", "rules", "PREREG_CC.md")
assert os.path.exists(RULE + ".sha256"), "rule not locked"
for n in ("candl", "candl.interface", "spt_candl_data"):
    sys.modules.setdefault(n, types.SimpleNamespace(CandlCobayaLikelihood=None, SPT3G_D1_TnE=None, interface=None))
sys.modules["candl"].interface = sys.modules["candl.interface"]
sys.path.insert(0, os.path.join(AEG, "cmb-fit", "axiclass"))
import early_late_spa as E, spiral_guess
FLAG = "ax_spa_spiraltwist_kappa1_nlfix"; E._maybe_coupled(FLAG)
import classy

C = 299792.458
D = np.genfromtxt(os.path.join(HERE, "cc_data.csv"), delimiter=",", names=True, dtype=None, encoding=None)
Z, H, S = D["z"].astype(float), D["H"].astype(float), D["sigma"].astype(float)
WIN = (Z >= 0.4) & (Z <= 0.8)
PAIRS = {"Pantheon+": ("ax_spa_spiraltwist_kappa1_nlfix_s8y6", "ax_spa_lcdm_halofit_s8y6"),
         "Dovekie": ("ax_spa_spiraltwist_kappa1_dovekie_nlfix_s8y6", "ax_spa_lcdm_halofit_dovekie_s8y6_more"),
         "Union3": ("ax_spa_spiraltwist_kappa1_union3_nlfix_s8y6", "ax_spa_lcdm_halofit_union3_s8y6_more")}


def hz(base, name):
    st = json.load(open(f"{E.OUT}/cmp_{name}.json"))["minimum"]
    info = E.make(base); a = dict(info["theory"]["classytwist"]["extra_args"])
    for k in ("lensing", "l_max_scalars", "non_linear"): a.pop(k, None)
    a.update({"A_s": 1e-10 * np.exp(st["logA"]), "n_s": st["n_s"], "100*theta_s": st["theta_s_1e2"],
              "omega_b": st["omega_b"], "omega_cdm": st["omega_cdm"], "tau_reio": st["tau_reio"], "output": ""})
    if "spiraltwist" in base:
        b = st["scf_coupling_beta"]; a["scf_coupling_beta"] = b
        a["scf_parameters"] = f"1.0, 0.0, {spiral_guess.mu1_guess(1.0, b, st['omega_b'], st['omega_cdm'])}, 0.0, 0.0, 0.0"
    c = classy.Class(); c.set(a); c.compute()
    out = np.array([c.Hubble(z) * C for z in Z]); c.struct_cleanup(); c.empty()
    return out


def wmean(frac, err):
    w = 1 / err ** 2; return float(np.sum(w * frac) / np.sum(w)), float(1 / np.sqrt(np.sum(w)))


out = {"rule": "PREREG_CC.md", "n_points": int(len(Z)), "sets": {}}
for sn, (fl, lc) in PAIRS.items():
    hf, hl = hz(FLAG, fl), hz("ax_spa_lcdm_halofit", lc)
    cf, cl = float(np.sum(((H - hf) / S) ** 2)), float(np.sum(((H - hl) / S) ** 2))
    m, sw = wmean((H / hl - 1)[WIN], (S / hl)[WIN])
    mf, _ = wmean((hf / hl - 1)[WIN], (S / hl)[WIN])
    out["sets"][sn] = {"chi2_FLAG1": round(cf, 3), "p_FLAG1": float(C2.sf(cf, len(Z))), "chi2_LCDM": round(cl, 3),
                       "p_LCDM": float(C2.sf(cl, len(Z))), "delta": round(cf - cl, 3),
                       "window": {"cc_mean_frac": round(m, 4), "sigma_w": round(sw, 4), "flag1_mean_frac": round(mf, 4),
                                  "needed_sigma_2sig": round(abs(mf) / 2, 4)}}
    print(sn, out["sets"][sn], flush=True)
P = out["sets"]["Pantheon+"]
d = P["delta"]; m, sw = P["window"]["cc_mean_frac"], P["window"]["sigma_w"]
out["CC1"] = "FLAG-1 FAVOURED" if d <= -2 else "LCDM FAVOURED" if d >= 2 else "NO DISCRIMINATION"
out["CC2"] = "FAST, AS BAO SUGGESTS" if m >= 2 * sw else "SLOW" if m <= -2 * sw else "NOT RESOLVED"
json.dump(out, open(os.path.join(AEG, "field_tests", "results", "cc.json"), "w"), indent=1)
print(out["CC1"], out["CC2"])
