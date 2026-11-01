# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights.
"""Coupled Twist test C4 and reported quantities, from a best fit (CubeMind PREREGISTRATION_COUPLED_TWIST.md).

C4: an observer assuming ordinary (uncoupled) dark matter infers rho_DE,eff = rho_phi + rho_c - rho_c0 a^-3, with
w_eff = -1 - (1/3) dln(rho_DE,eff)/dlna. CROSSES if w_eff < -1 anywhere in 0.3 < z < 2 at the best fit.
Also reports today's true Omega_m and S8 (with the coupling, the solver's own Omega_m is the early-time value).
    python coupled_weff.py ax_spa_coupledtwist     -> results/weff_<name>.json
"""
import copy
import json
import sys

import numpy as np

sys.path.insert(0, "/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass")
from early_late_spa import make, OUT, _maybe_coupled

name = sys.argv[1]
_maybe_coupled(name)
from cobaya.model import get_model

info = copy.deepcopy(make(name))
for k in ("sampler", "output", "resume", "force"):
    info.pop(k, None)
model = get_model(info)
best = json.load(open(f"{OUT}/cmp_{name}.json"))["minimum"]
model.logposterior({p: best[p] for p in model.parameterization.sampled_params()})
cl = model.theory["classytwist"].classy
bg = cl.get_background()
z = np.asarray(bg["z"]); o = np.argsort(z); z = z[o]; a = 1 / (1 + z)
rc = np.asarray(bg["(.)rho_cdm"])[o]; rs = np.asarray(bg["(.)rho_scf"])[o]
rc0 = rc[0]                                            # z sorted ascending: index 0 is today
rde = rs + rc - rc0 / a ** 3
lna = np.log(a)
weff = -1 - np.gradient(np.log(np.abs(rde)), lna) / 3
sel = (z > 0.3) & (z < 2)
H0 = np.asarray(bg["H [1/Mpc]"])[o][0]
rho_m0 = rc0 + np.asarray(bg["(.)rho_b"])[o][0] + sum(np.asarray(bg[k])[o][0] for k in bg if k.startswith("(.)rho_ncdm"))
Om0 = float(rho_m0 / H0 ** 2)
s8 = float(cl.sigma8() * np.sqrt(Om0 / 0.3))
res = {"run": name, "beta": best.get("scf_coupling_beta", info["theory"]["classytwist"]["extra_args"].get("scf_coupling_beta")),
       "C4": "CROSSES" if bool(np.any(weff[sel] < -1)) else "DOES NOT",
       "w_eff_min_0.3<z<2": float(weff[sel].min()), "z_at_min": float(z[sel][np.argmin(weff[sel])]),
       "w_eff_today": float(weff[0]), "rde_positive_all_z<2": bool(np.all(rde[z < 2] > 0)),
       "Omega_m_today_true": Om0, "sigma8": float(cl.sigma8()), "S8_true": s8,
       "w_eff_samples": {f"{zz:.2f}": float(np.interp(zz, z, weff)) for zz in (0.0, 0.3, 0.5, 1.0, 1.5, 2.0)}}
print(json.dumps(res, indent=1))
json.dump(res, open(f"{OUT}/weff_{name}.json", "w"), indent=2)
