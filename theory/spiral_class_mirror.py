"""Mirror for the effective Spiral Twist in AxiCLASS (coupled B0-fixed build, pol_times_exp with alpha = 0) against the
independently validated solver in spiral_w.py (coupled_exp_w). Same cosmology, kappa = 1, beta in {0, 0.05}.
PASS if w_scf(z) agrees within 0.003 and H(z)/H0 within 0.1% on 0 <= z <= 3.
    WSL env 'aegis':  python spiral_class_mirror.py   -> spiral_class_mirror.json"""
import glob
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
build = os.path.expanduser("~/AxiCLASS_coupled_nlfix/python/build")
sys.path.insert(0, glob.glob(build + "/lib*")[0])
import classy  # noqa: E402

sys.path.insert(0, HERE)
import spiral_w as S  # noqa: E402
from mirror_background import prepare_background  # noqa: E402

ZS = np.linspace(0, 3, 31)
KAP = float(os.environ.get("KAP", "1.0"))
rows = {}
for beta in (0.0, 0.05):
    c = classy.Class()
    c.set({"h": 0.68, "omega_b": 0.0224, "omega_cdm": 0.12, "N_ur": 3.044, "N_ncdm": 0,
           "Omega_Lambda": 0, "Omega_fld": 0, "Omega_scf": -1, "scf_potential": "double_exp",
           # V = mu1^4 e^(-k phi); this build sets phi_ini = scf_parameters[0] = k and phi'_ini = scf_parameters[1] = 0,
           # so the second exponential (lambda2 = 0, mu2 = 0) vanishes; mu1 (index 2) is tuned for closure
           "scf_parameters": f"{KAP}, 0.0, {S.class_mu1_guess(KAP, beta, 0.0224 / 0.68**2, 0.12 / 0.68**2, 9.1e-5, 0.68)}, 0.0, 0.0, 0.0",
           "scf_tuning_index": 2,
           "attractor_ic_scf": "no",
           "scf_evolve_as_fluid": "no", "do_shooting": "yes", "do_shooting_scf": "yes", "scf_has_perturbations": "yes",
           "scf_coupling_beta": beta, "output": ""})
    c.compute()
    bg = c.get_background()
    # the tuned slope kappa: -dV/dphi / V at any time (pure exponential), from the background columns
    kap = None
    for key in ("V_scf", "(.)V_scf"):
        if key in bg:
            break
    keys_scf = [k for k in bg if "scf" in k]
    E_cl, w_cl, h, orad = prepare_background(bg, ZS)
    # the coupled build closes the universe on its ACTUAL H(z=0), which differs from the input h when beta != 0
    # (H(0)/H0_in = 0.998 at beta = 0.05): use the actual h for the solver's densities
    om_b, om_c = 0.0224 / h ** 2, 0.12 / h ** 2
    print("CLASS w0", w_cl[0], flush=True)
    kap = KAP           # no matching: the same kappa goes into both codes
    E_s, w_s = S.coupled_exp_w(kap, beta, om_b, om_c, orad, ZS)
    dw = float(np.max(np.abs(np.array(w_s) - w_cl)))
    dE = float(np.max(np.abs(np.array(E_s) / E_cl - 1)))
    rows[f"beta={beta}"] = {"kappa_matched": kap, "scf_columns": keys_scf, "max_dw": dw, "max_dE_rel": dE,
                            "w0_class": float(w_cl[0]), "w0_solver": float(w_s[0]),
                            "pass": dw < 0.003 and dE < 0.001}
    print(beta, rows[f"beta={beta}"], flush=True)
    c.struct_cleanup()
rows["MIRROR"] = "PASS" if all(v["pass"] for v in rows.values() if isinstance(v, dict)) else "FAIL"
json.dump(rows, open(os.path.join(HERE, "spiral_class_mirror.json"), "w"), indent=1)
print(rows["MIRROR"])
if rows["MIRROR"] != "PASS":
    raise SystemExit(1)
