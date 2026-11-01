# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights.
"""Post-hoc diagnostic for the Late Twist L1 result (chi2 above LCDM): can the field reach the LCDM-like limit
(large F, small m) inside its pre-registered prior? Evaluates chi2 at a few (F, m) points with the cosmological and
nuisance parameters held at the AxiCLASS LCDM (halofit) best fit, and at the Late Twist best fit itself. No fit."""
import copy
import json
import sys

sys.path.insert(0, "/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass")
from early_late_spa import make, OUT
from cobaya.model import get_model

info = copy.deepcopy(make("ax_spa_latetwist"))
for k in ("sampler", "output", "resume", "force"):
    info.pop(k, None)
model = get_model(info)
sp = list(model.parameterization.sampled_params())
lcdm = json.load(open(f"{OUT}/cmp_ax_spa_lcdm_halofit.json"))["minimum"]
lt = json.load(open(f"{OUT}/cmp_ax_spa_latetwist.json"))["minimum"]
print(f"LCDM halofit chi2 {lcdm['chi2']:.2f} | Late Twist best chi2 {lt['chi2']:.2f} "
      f"(log10F {lt['log10_F']:.3f}, log10m {lt['log10_m']:.3f})", flush=True)
for lf, lm in ((0.5, -0.5), (0.5, -0.3), (0.3, -0.5), (0.5, 0.0), (lt["log10_F"], lt["log10_m"])):
    pt = {p: lcdm.get(p, lt[p]) for p in sp}
    pt["log10_F"], pt["log10_m"] = lf, lm
    r = model.logposterior(pt)
    chi2 = -2 * sum(r.loglikes) if r.loglikes is not None else float("nan")
    print(f"log10F {lf:+.2f} log10m {lm:+.2f} (F {10**lf:.2f}, m {10**lm:.2f})  chi2 {chi2:.2f}  "
          f"delta vs LCDM {chi2 - lcdm['chi2']:+.2f}", flush=True)
