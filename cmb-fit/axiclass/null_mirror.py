# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights.
"""Late Twist null mirror (CubeMind PREREGISTRATION_EDGE_SCAN.md): in its LCDM limit (a very light field, nearly frozen at
the hilltop), the Late Twist should reproduce LCDM's chi2. Evaluates chi2 with the cosmological and calibration
parameters fixed at the AxiCLASS LCDM (halofit) best fit, for fields from 'edge-like' to 'deeply frozen'. No fit.
A residual that tends to a constant as the field freezes is a numerical offset; one that tends to 0 means none."""
import copy
import json
import math
import sys

sys.path.insert(0, "/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass")
from early_late_spa import make, OUT
from cobaya.model import get_model

lcdm = json.load(open(f"{OUT}/cmp_ax_spa_lcdm_halofit.json"))["minimum"]
rows = []
for F, m in ((3.16, 0.5), (10.0, 0.15), (30.0, 0.05), (100.0, 0.015)):
    name = f"ax_spa_latetwist_gF{math.log10(F):.3f}m{math.log10(m):.3f}"
    info = copy.deepcopy(make(name))
    for k in ("sampler", "output", "resume", "force"):
        info.pop(k, None)
    model = get_model(info)
    sp = list(model.parameterization.sampled_params())
    r = model.logposterior({p: lcdm[p] for p in sp})
    chi2 = -2 * sum(r.loglikes) if r.loglikes is not None else float("nan")
    rows.append({"F": F, "m": m, "m2F2": m * m * F * F, "chi2": chi2, "minus_lcdm": chi2 - lcdm["chi2"]})
    print(f"F={F:7.2f} m={m:6.3f} m2F2={m*m*F*F:5.2f}  chi2 {chi2:.3f}  vs LCDM {chi2 - lcdm['chi2']:+.3f}", flush=True)
json.dump({"lcdm_halofit_chi2": lcdm["chi2"], "rows": rows}, open(f"{OUT}/null_mirror_latetwist.json", "w"), indent=1)
