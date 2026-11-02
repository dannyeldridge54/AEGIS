# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights.
"""Validate the "_nlfix" switch end to end (CubeMind PREREGISTRATION_NLFIX_REPLICATION.md, gate N0): through
early_late_spa's own make() and _maybe_coupled(), the frozen field (F 100, m 0.015) at the LCDM halofit best fit must give
|chi2 - chi2_LCDM| < 0.15, for the Late Twist (fixed build) and for the Coupled Twist at beta = 0 (fixed coupled build).
Run once per process (each loads one classy build):  python validate_nlfix_builds.py latetwist|coupled"""
import os as _os
_AXI = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_RESULTS = _os.environ.get("TWIST_RESULTS", _os.path.join(_os.path.dirname(_AXI), "results"))
_BUILDS = _os.environ.get("TWIST_BUILDS", _os.path.expanduser("~"))
import copy
import json
import sys

sys.path.insert(0, _AXI)
import early_late_spa as E                                     # noqa: E402

kind = sys.argv[1]
name = {"latetwist": "ax_spa_latetwist_gF2m-1.824_nlfix",
        "coupled": "ax_spa_coupledtwist_beta0_gF2m-1.824_nlfix"}[kind]
E._maybe_coupled(name)
import classy                                                  # noqa: E402
from cobaya.model import get_model                             # noqa: E402

lcdm = json.load(open(f"{E.OUT}/cmp_ax_spa_lcdm_halofit.json"))["minimum"]
info = copy.deepcopy(E.make(name))
for k in ("sampler", "output", "resume", "force"):
    info.pop(k, None)
model = get_model(info)
pt = {p: lcdm.get(p, 0.0) for p in model.parameterization.sampled_params()}
r = model.logposterior(pt)
d = -2 * sum(r.loglikes) - lcdm["chi2"]
v = "PASS" if abs(d) < 0.15 else "FAIL"
print(f"N0 {kind}: frozen field - LCDM = {d:+.3f} -> {v}   [classy {classy.__file__}]")
json.dump({"gate": "N0", "kind": kind, "run": name, "diff": d, "verdict": v, "classy": classy.__file__},
          open(f"{E.OUT}/nlfix_gate_N0_{kind}.json", "w"), indent=1)
