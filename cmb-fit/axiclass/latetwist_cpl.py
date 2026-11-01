# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights.
"""Late Twist "reported beside the verdicts" (CubeMind PREREGISTRATION_LATE_TWIST.md): from a best fit, the field's w today
and the CPL-equivalent (w0, wa), a least-squares fit of w(a) = w0 + wa (1 - a) over z < 2 from the CLASS background.
    python latetwist_cpl.py <run name>      -> results/cpl_<run name>.json
    python latetwist_cpl.py test            -> same at the reference point (log10 F = 0, log10 m = 0.2), no file
"""
import copy
import json
import sys

import numpy as np

sys.path.insert(0, "/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass")
from early_late_spa import make, OUT
from cobaya.model import get_model

name = sys.argv[1]
info = copy.deepcopy(make(name if "_gF" in name else "ax_spa_latetwist" + ("_desy5" if "desy5" in name else "")))
for k in ("sampler", "output", "resume", "force"):
    info.pop(k, None)
model = get_model(info)
sp = list(model.parameterization.sampled_params())
if name == "test":
    point = dict(zip(sp, model.prior.reference(random_state=1)))
    point["log10_F"], point["log10_m"] = 0.0, 0.2
else:
    best = json.load(open(f"{OUT}/cmp_{name}.json"))["minimum"]
    point = {p: best[p] for p in sp}
r = model.logposterior(point)
bg = model.theory["classytwist"].classy.get_background()
z = np.asarray(bg["z"])
w = np.asarray(bg["(.)p_scf"]) / np.asarray(bg["(.)rho_scf"])
sel = z < 2
a = 1 / (1 + z[sel])
A = np.c_[np.ones(sel.sum()), 1 - a]
(w0, wa), *_ = np.linalg.lstsq(A, w[sel], rcond=None)
res = {"run": name, "logpost": float(r.logpost), "w_today": float(w[np.argmin(z)]), "cpl_w0": float(w0),
       "cpl_wa": float(wa), "max_abs_resid": float(np.max(np.abs(A @ [w0, wa] - w[sel])))}
print(json.dumps(res, indent=2))
if name != "test":
    json.dump(res, open(f"{OUT}/cpl_{name}.json", "w"), indent=2)
