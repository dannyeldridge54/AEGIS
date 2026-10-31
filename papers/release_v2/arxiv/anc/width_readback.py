# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights.
"""Read the field width back out of a finished best fit: implied N = sqrt(3/2) M_Pl / F.

    python width_readback.py NAME [NAME ...]      e.g. spt_edelock  (needs results/cmp_NAME.json)

Rebuilds the model exactly as cmbfit_compare.make(NAME) did, evaluates it once at the saved minimum, and reads CAMB's
solved decay constant f (= F / M_Pl) from Params.DarkEnergy.f. Used for the width checks in PREREG_N_PACT.md (T1) and
the CubeMind SPT-3G pre-registration. Prints and saves results/width_NAME.json.
"""
import json
import math
import os
import sys

import cmbfit as C
import cmbfit_compare as M

F_TORSION = math.sqrt(1.5)


def readback(name):
    from cobaya.model import get_model
    m = json.load(open(os.path.join(C.RESULTS, f"cmp_{name}.json")))["minimum"]
    info = M.make(name)
    info.pop("sampler", None)
    info.pop("output", None)
    model = get_model(info)
    model.add_requirements({"CAMBdata": None})       # free-width fits do not request it themselves
    point = {p: m[p] for p in model.parameterization.sampled_params() if p in m}
    missing = [p for p in model.parameterization.sampled_params() if p not in m]
    if missing:
        raise ValueError(f"minimum of {name} lacks sampled parameters {missing}")
    model.logposterior(point)
    f = model.provider.get_CAMBdata().Params.DarkEnergy.f
    out = dict(run=name, f_over_MPl=f, implied_N=F_TORSION / f, theta_i=m.get("theta_i"), fde_zc=m.get("fde_zc"),
               H0=m.get("H0"))
    json.dump(out, open(os.path.join(C.RESULTS, f"width_{name}.json"), "w"), indent=2)
    print(f"{name}: F = {f:.5f} M_Pl  ->  implied N = {F_TORSION / f:.3f}", flush=True)
    return out


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        readback(arg)
