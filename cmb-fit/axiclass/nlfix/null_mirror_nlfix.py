# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights.
"""B0 validation (CubeMind PREREGISTRATION_SPT3G_DEVIATIONS.md, 14:34:07): the null mirror with halofit ON on the fixed
build. Pass if |chi2(frozen field) - chi2(true Lambda)| < 0.15. Same fixed LCDM halofit best fit as null_mirror.py; no fit.
The edge-like point is reported too (expected near the non-linear-off value, -0.9)."""
import copy
import glob
import json
import math
import sys

BUILD = glob.glob("/home/syndyr/AxiCLASS_nlfix/python/build/lib*")[0]
sys.path.insert(0, BUILD)
import classy                                                  # noqa: E402
assert classy.__file__.startswith(BUILD), classy.__file__
sys.path.insert(1, "/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass")
from early_late_spa import make, OUT                           # noqa: E402
from cobaya.model import get_model                             # noqa: E402

lcdm = json.load(open(f"{OUT}/cmp_ax_spa_lcdm_halofit.json"))["minimum"]


def chi2(name):
    info = copy.deepcopy(make(name))
    for k in ("sampler", "output", "resume", "force"):
        info.pop(k, None)
    model = get_model(info)
    sp = list(model.parameterization.sampled_params())
    r = model.logposterior({p: lcdm[p] for p in sp})
    return -2 * sum(r.loglikes)


ref = chi2("ax_spa_lcdm_halofit")
rows = []
for F, m in ((100.0, 0.015), (3.16, 0.5)):
    c = chi2(f"ax_spa_latetwist_gF{math.log10(F):.3f}m{math.log10(m):.3f}")
    rows.append({"F": F, "m": m, "chi2_lcdm": ref, "chi2_lt": c, "diff": c - ref})
    print(f"fixed build, halofit on: F={F:6.2f} m={m:5.3f}  LT-LCDM {c - ref:+.3f}", flush=True)
frozen = rows[0]["diff"]
verdict = "PASS" if abs(frozen) < 0.15 else "FAIL"
print(f"B0 validation (|frozen| < 0.15): {verdict}  [classy from {classy.__file__}]")
json.dump({"build": BUILD, "lcdm_chi2_fixed_build": ref, "rows": rows, "verdict": verdict},
          open(f"{OUT}/null_mirror_nlfix.json", "w"), indent=1)
