# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights.
"""Diagnose the ax_spa_latetwist minimiser crash (likelihood overflow): evaluate the Late Twist on a coarse (F, m) grid
with the other parameters at the AxiCLASS LCDM best fit, and print the log-posterior and each chi2. No fit, no result."""
import copy
import json
import math
import sys

sys.path.insert(0, "/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass")
from early_late_spa import make, OUT
from cobaya.model import get_model

info = copy.deepcopy(make("ax_spa_latetwist"))
for k in ("sampler", "output", "resume", "force"):
    info.pop(k, None)
model = get_model(info)
best = json.load(open(f"{OUT}/cmp_ax_spa_lcdm.json"))["minimum"]
sp = list(model.parameterization.sampled_params())
point = {p: best.get(p, model.prior.reference(random_state=1)[sp.index(p)]) for p in sp}
for lf in (-1.2, -0.6, 0.0, 0.4):
    for lm in (-0.4, 0.2, 0.8, 1.4):
        point["log10_F"], point["log10_m"] = lf, lm
        try:
            r = model.logposterior(point)
            chis = {k: round(-2 * v, 1) for k, v in zip(model.likelihood, r.loglikes)} if r.loglikes is not None else {}
            bad = [k for k, v in chis.items() if not math.isfinite(v) or abs(v) > 1e5]
            print(f"logF {lf:+.1f} logm {lm:+.1f}  logpost {r.logpost:.4g}  bad {bad}", flush=True)
        except Exception as e:
            print(f"logF {lf:+.1f} logm {lm:+.1f}  ERROR {type(e).__name__}: {str(e)[:120]}", flush=True)
