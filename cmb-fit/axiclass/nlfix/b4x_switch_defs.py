# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights.
"""Ratio replication S3 (CubeMind PREREGISTRATION_RATIO_REPLICATION.md, locked 2026-11-02 12:01:34): H(z_on)/H0 at the NR
best fits for switch definitions f = 5, 10, 20, 50% of the field's move since recombination.
    python b4x_switch_defs.py <run> [<run> ...]"""
import copy
import json
import sys

sys.path.insert(0, "/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass")
import early_late_spa as E                                      # noqa: E402

E._maybe_coupled(sys.argv[1])
from cobaya.model import get_model                              # noqa: E402
import numpy as np                                              # noqa: E402

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
    z = np.array(bg["z"]); phi = np.array(bg["phi_scf"]); H = np.array(bg["H [1/Mpc]"])
    o = np.argsort(z); z, phi, H = z[o], phi[o], H[o]
    p0, prec = np.interp(0, z, phi), np.interp(1089.9, z, phi)
    frac = (phi - prec) / (p0 - prec)
    hi = z <= 1089.9
    zz, ff = z[hi][::-1], frac[hi][::-1]
    out[run] = {}
    for f in (0.05, 0.10, 0.20, 0.50):
        i = int(np.argmax(ff >= f))
        zon = float(np.interp(f, [ff[i - 1], ff[i]], [zz[i - 1], zz[i]]))
        out[run][f"{int(f * 100)}%"] = {"z_on": zon, "H_over_H0": float(np.interp(zon, z, H) / np.interp(0, z, H))}
    print(run, json.dumps(out[run]), flush=True)
json.dump(out, open(f"{E.OUT}/ratio_s3_switch_defs.json", "w"), indent=1)
