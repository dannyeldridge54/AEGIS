"""MISSING-PIECE M2 (field_tests/rules/PREREG_MISSING_PIECE.md): E_G of FLAG-1 and LCDM vs ACT DR6 x BOSS.
    python m2_eg.py      -> field_tests/results/missing_piece_m2.json      (coupled build, both models; AI-assisted)"""
import json, os, sys, types
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); AEG = os.path.abspath(os.path.join(HERE, "..", ".."))
RULE = os.path.join(AEG, "field_tests", "rules", "PREREG_MISSING_PIECE.md")
assert os.path.exists(RULE + ".sha256"), "rule not locked"
for n in ("candl", "candl.interface", "spt_candl_data"):
    sys.modules.setdefault(n, types.SimpleNamespace(CandlCobayaLikelihood=None, SPT3G_D1_TnE=None, interface=None))
sys.modules["candl"].interface = sys.modules["candl.interface"]
sys.path.insert(0, os.path.join(AEG, "cmb-fit", "axiclass"))
import early_late_spa as E, spiral_guess
FLAG = "ax_spa_spiraltwist_kappa1_nlfix"; E._maybe_coupled(FLAG)
import classy

# Wenzl et al. 2024 (arXiv:2405.12795), ACT-only rows: z, E_G, +err, -err, systematic fraction
DATA = [(0.555, 0.31, 0.06, 0.05, 0.03), (0.316, 0.49, 0.14, 0.11, 0.04)]
K = 0.02; DZ = 0.01
SETS = {"Pantheon+": "", "Dovekie": "_dovekie", "Union3": "_union3"}


def cls(base, st):
    info = E.make(base)
    a = dict(info["theory"]["classytwist"]["extra_args"])
    for k in ("lensing", "l_max_scalars", "non_linear"): a.pop(k, None)
    a.update({"A_s": 1e-10 * np.exp(st["logA"]), "n_s": st["n_s"], "100*theta_s": st["theta_s_1e2"],
              "omega_b": st["omega_b"], "omega_cdm": st["omega_cdm"], "tau_reio": st["tau_reio"],
              "output": "mPk", "P_k_max_1/Mpc": 1.0, "z_max_pk": 1.0})
    if "spiraltwist" in base:
        b = st["scf_coupling_beta"]; a["scf_coupling_beta"] = b
        a["scf_parameters"] = f"1.0, 0.0, {spiral_guess.mu1_guess(1.0, b, st['omega_b'], st['omega_cdm'])}, 0.0, 0.0, 0.0"
    c = classy.Class(); c.set(a); c.compute()
    return c


def eg(c, z):
    bg = c.get_background(); zz = bg["z"][::-1]
    rm = bg["(.)rho_b"][::-1] + bg["(.)rho_cdm"][::-1]
    H0 = c.Hubble(0)
    om_eff = float(np.interp(z, zz, rm)) / (1 + z) ** 3 / H0 ** 2
    pk = lambda zq: c.pk_cb_lin(K, zq)
    lnD = lambda zq: 0.5 * np.log(pk(zq))
    f = -(1 + z) * (lnD(z + DZ) - lnD(z - DZ)) / (2 * DZ)
    return om_eff / f, om_eff, f


def chi2(vals):
    t = 0.0
    for (z, obs, up, lo, sysf), v in zip(DATA, vals):
        s = np.hypot(up if v > obs else lo, sysf * obs); t += ((v - obs) / s) ** 2
    return t


out = {"rule": "PREREG_MISSING_PIECE.md M2", "data": "Wenzl et al. 2024 arXiv:2405.12795, ACT-only rows", "sets": {}}
gate_ok = True
for sn, suf in SETS.items():
    row = {}
    for lab, base, name in (("FLAG-1", FLAG, f"{FLAG.replace('_nlfix', '')}{suf}_nlfix_s8y6"),
                            ("LCDM", "ax_spa_lcdm_halofit", f"ax_spa_lcdm_halofit{suf}_s8y6")):
        st = json.load(open(f"{E.OUT}/cmp_{name}.json"))["minimum"]
        c = cls(base, st)
        vals, det = [], {}
        for z, *_ in DATA:
            e, om, f = eg(c, z); vals.append(e)
            det[f"z{z}"] = {"E_G": round(e, 5), "Omega_m_eff": round(om, 5), "f": round(f, 5)}
            if lab == "LCDM":
                fc = c.scale_independent_growth_factor_f(z); det[f"z{z}"]["f_class"] = round(fc, 5)
                gate_ok &= abs(f / fc - 1) <= 0.01
        row[lab] = {"fit": name, "E_G": det, "chi2_EG": round(chi2(vals), 4), "vals": vals}
        c.struct_cleanup(); c.empty()
    d = row["FLAG-1"]["chi2_EG"] - row["LCDM"]["chi2_EG"]
    row["delta_EG"] = round(d, 4)
    row["frac_diff"] = {f"z{z}": round(row["FLAG-1"]["vals"][i] / row["LCDM"]["vals"][i] - 1, 5) for i, (z, *_) in enumerate(DATA)}
    row["sigma_needed_2sig_frac"] = {k: round(abs(v) / 2, 5) for k, v in row["frac_diff"].items()}
    for lab in ("FLAG-1", "LCDM"): row[lab].pop("vals")
    out["sets"][sn] = row
    print(sn, row["FLAG-1"]["chi2_EG"], row["LCDM"]["chi2_EG"], row["frac_diff"], flush=True)
d = out["sets"]["Pantheon+"]["delta_EG"]
out["gate_f_vs_class_1pct"] = bool(gate_ok)
out["reading"] = ("NO VERDICT (gate failed)" if not gate_ok else "FLAG-1 FAVOURED" if d <= -1 else
                  "LCDM FAVOURED" if d >= 1 else "NO DISCRIMINATION")
json.dump(out, open(os.path.join(AEG, "field_tests", "results", "missing_piece_m2.json"), "w"), indent=1)
print(out["reading"], d)
