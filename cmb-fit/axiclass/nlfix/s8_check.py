# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights.
"""S8 on the corrected code (CubeMind PREREGISTRATION_S8_FIXED_CODE.md, locked 2026-11-02 12:10:03). Evaluates each best
fit once on the build chosen by the first run name and prints sigma8, the true Omega_m (cdm + b + ncdm, never the
field) and S8 = sigma8 sqrt(Omega_m / 0.3). Appends to results/s8_fixed_code.json.
    python s8_check.py <run> [<run> ...]"""
import copy
import json
import math
import os
import sys

sys.path.insert(0, "/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass")
import early_late_spa as E                                      # noqa: E402

E._maybe_coupled(sys.argv[1])
from cobaya.model import get_model                              # noqa: E402
import numpy as np                                              # noqa: E402

path = f"{E.OUT}/s8_fixed_code.json"
out = json.load(open(path)) if os.path.exists(path) else {}
for run in sys.argv[1:]:
    best = json.load(open(f"{E.OUT}/cmp_{run}.json"))["minimum"]
    info = copy.deepcopy(E.make(run))
    for k in ("sampler", "output", "resume", "force"):
        info.pop(k, None)
    model = get_model(info)
    model.logposterior({p: best[p] for p in model.parameterization.sampled_params()})
    th = model.theory[next(iter(model.theory))]
    cl = getattr(th, "classy", None) or getattr(th, "classy_module", None)
    bg = cl.get_background()
    i0 = int(np.argmin(np.abs(np.array(bg["z"]))))
    rho = lambda k: float(np.array(bg[k])[i0]) if k in bg else 0.0
    om = (rho("(.)rho_cdm") + rho("(.)rho_b") + sum(rho(k) for k in bg if k.startswith("(.)rho_ncdm"))) / rho("(.)rho_crit")
    s8 = cl.sigma8()
    out[run] = {"sigma8": s8, "Omega_m_true": om, "S8": s8 * math.sqrt(om / 0.3), "build_from": sys.argv[1],
                "Omega_m_class": cl.Omega_m()}
    print(run, json.dumps(out[run]), flush=True)
json.dump(out, open(path, "w"), indent=1)
