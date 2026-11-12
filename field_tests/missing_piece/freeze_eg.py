"""Frozen E_G predictions for FLAG-1 and its LCDM partners (rule: field_tests/rules/PREREG_EG_FORECAST_FLAG1.md).
    python freeze_eg.py   -> field_tests/missing_piece/eg_frozen.json      (coupled build; AI-assisted)
Same method as MISSING-PIECE M2 (m2_eg.py): E_G = Omega_m,eff(z)/f(z), f from the linear cb power at k = 0.02/Mpc."""
import hashlib, json, os, sys, types
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); AEG = os.path.abspath(os.path.join(HERE, "..", ".."))
for n in ("candl", "candl.interface", "spt_candl_data"):
    sys.modules.setdefault(n, types.SimpleNamespace(CandlCobayaLikelihood=None, SPT3G_D1_TnE=None, interface=None))
sys.modules["candl"].interface = sys.modules["candl.interface"]
sys.path.insert(0, os.path.join(AEG, "cmb-fit", "axiclass"))
import early_late_spa as E, spiral_guess
FLAG = "ax_spa_spiraltwist_kappa1_nlfix"; E._maybe_coupled(FLAG)
import classy

ZS = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.5]
K, DZ = 0.02, 0.01
PAIRS = {"Pantheon+": ("ax_spa_spiraltwist_kappa1_nlfix_s8y6", "ax_spa_lcdm_halofit_s8y6"),
         "Dovekie": ("ax_spa_spiraltwist_kappa1_dovekie_nlfix_s8y6", "ax_spa_lcdm_halofit_dovekie_s8y6_more"),
         "Union3": ("ax_spa_spiraltwist_kappa1_union3_nlfix_s8y6", "ax_spa_lcdm_halofit_union3_s8y6_more")}


def cls(base, st):
    info = E.make(base)
    a = dict(info["theory"]["classytwist"]["extra_args"])
    for k in ("lensing", "l_max_scalars", "non_linear"): a.pop(k, None)
    a.update({"A_s": 1e-10 * np.exp(st["logA"]), "n_s": st["n_s"], "100*theta_s": st["theta_s_1e2"],
              "omega_b": st["omega_b"], "omega_cdm": st["omega_cdm"], "tau_reio": st["tau_reio"],
              "output": "mPk", "P_k_max_1/Mpc": 1.0, "z_max_pk": 2.0})
    if "spiraltwist" in base:
        b = st["scf_coupling_beta"]; a["scf_coupling_beta"] = b
        a["scf_parameters"] = f"1.0, 0.0, {spiral_guess.mu1_guess(1.0, b, st['omega_b'], st['omega_cdm'])}, 0.0, 0.0, 0.0"
    c = classy.Class(); c.set(a); c.compute()
    return c


def eg(c, z):
    bg = c.get_background(); zz = bg["z"][::-1]; rm = bg["(.)rho_b"][::-1] + bg["(.)rho_cdm"][::-1]
    om = float(np.interp(z, zz, rm)) / (1 + z) ** 3 / c.Hubble(0) ** 2
    lnD = lambda q: 0.5 * np.log(c.pk_cb_lin(K, q))
    f = -(1 + z) * (lnD(z + DZ) - lnD(z - DZ)) / (2 * DZ)
    return om / f


out = {"method": "E_G = Omega_m,eff(z)/f(z); f from linear cb P(k=0.02/Mpc); galaxies taken to move with the dark matter",
       "z": ZS, "sets": {}}
for sn, (fl, lc) in PAIRS.items():
    row = {}
    for lab, name, base in (("FLAG-1", fl, FLAG), ("LCDM", lc, "ax_spa_lcdm_halofit")):
        p = f"{E.OUT}/cmp_{name}.json"
        st = json.load(open(p))["minimum"]; c = cls(base, st)
        row[lab] = {"fit": name, "sha256_16": hashlib.sha256(open(p, "rb").read()).hexdigest()[:16],
                    "E_G": [round(eg(c, z), 4) for z in ZS]}
        c.struct_cleanup(); c.empty()
    row["ratio_minus_1"] = [round(a / b - 1, 4) for a, b in zip(row["FLAG-1"]["E_G"], row["LCDM"]["E_G"])]
    out["sets"][sn] = row
    print(sn, row["FLAG-1"]["E_G"], row["LCDM"]["E_G"], row["ratio_minus_1"], flush=True)
json.dump(out, open(os.path.join(HERE, "eg_frozen.json"), "w"), indent=1)
