# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights.
"""B4-X (CubeMind PREREGISTRATION_B4X_PHOTON_COUPLING.md, locked 2026-11-02 11:54:34): the switch numbers at the NR
best fits. Evaluates each best fit once on the fixed build and reads the background table:
  R    = [phi(0) - phi(z_re)] / [phi(0) - phi(z_rec)]        (z_re = 7.7, z_rec = 1089.9)
  z_on = redshift where the field has covered 10% of its move since recombination
  b0   = (sqrt6/4) phi_dot(today) / M_Pl, in GeV (phi' is d phi/d tau in M_Pl/Mpc; a = 1 today)
    python b4x_switch.py <run> [<run> ...]"""
import copy
import json
import math
import sys

sys.path.insert(0, "/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass")
import early_late_spa as E                                      # noqa: E402

E._maybe_coupled(sys.argv[1])
from cobaya.model import get_model                              # noqa: E402
import numpy as np                                              # noqa: E402

MPC_GEV = 1.973269804e-16 / 3.0856775814913673e22               # hbar c / Mpc in GeV
out = {}
for run in sys.argv[1:]:
    best = json.load(open(f"{E.OUT}/cmp_{run}.json"))["minimum"]
    info = copy.deepcopy(E.make(run))
    for k in ("sampler", "output", "resume", "force"):
        info.pop(k, None)
    model = get_model(info)
    model.logposterior({p: best[p] for p in model.parameterization.sampled_params()})
    th = model.theory[next(iter(model.theory))]
    bg = (getattr(th, "classy", None) or getattr(th, "classy_module", None)).get_background()
    z = np.array(bg["z"]); phi = np.array(bg["phi_scf"]); dphi = np.array(bg["phi'_scf"])
    H = np.array(bg["H [1/Mpc]"])
    o = np.argsort(z); z, phi, dphi, H = z[o], phi[o], dphi[o], H[o]
    at = lambda zz, arr: float(np.interp(zz, z, arr))
    p0, pre, prec = at(0, phi), at(7.7, phi), at(1089.9, phi)
    frac = (phi - prec) / (p0 - prec)
    hi = z <= 1089.9
    zz, ff = z[hi][::-1], frac[hi][::-1]                        # high z -> low z
    i = int(np.argmax(ff >= 0.10))
    z_on = float(np.interp(0.10, [ff[i - 1], ff[i]], [zz[i - 1], zz[i]]))
    b0 = math.sqrt(6) / 4 * at(0, dphi) * MPC_GEV
    m_over_H0 = None
    out[run] = {"R": (p0 - pre) / (p0 - prec), "z_on": z_on, "b0_GeV": b0, "phi0": p0, "phi_re": pre, "phi_rec": prec,
                "dphi_dtau_today_MPl_per_Mpc": at(0, dphi), "H0_per_Mpc": at(0, H), "H_at_z_on_over_H0": at(z_on, H) / at(0, H)}
    print(run, json.dumps(out[run]), flush=True)
json.dump(out, open(f"{E.OUT}/b4x_switch.json", "w"), indent=1)
