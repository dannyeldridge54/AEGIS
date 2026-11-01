# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights.
"""Shared-F test input: the early field's decay constant F (in M_Pl) and mass, which AxiCLASS solves for by shooting
from (f_EDE, z_c, theta_i). Recomputes the given best fit once and prints what classy exposes.
    python early_F.py ax_spa_edelock_w0wa   -> results/earlyF_<name>.json
"""
import copy
import json
import sys

sys.path.insert(0, "/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass")
from early_late_spa import make, OUT
from cobaya.model import get_model

name = sys.argv[1]
info = copy.deepcopy(make(name))
for k in ("sampler", "output", "resume", "force"):
    info.pop(k, None)
model = get_model(info)
best = json.load(open(f"{OUT}/cmp_{name}.json"))["minimum"]
model.logposterior({p: best[p] for p in model.parameterization.sampled_params()})
cl = model.theory["classytwist"].classy
keys = ["f_axion", "m_axion", "log10_f_axion", "log10_m_axion", "fraction_axion_ac", "log10_axion_ac", "a_c", "z_c"]
got = {}
for k in keys:
    try:
        got[k] = float(cl.get_current_derived_parameters([k])[k])
    except Exception as e:
        got[k] = f"n/a ({type(e).__name__})"
print(json.dumps(got, indent=2))
json.dump({"run": name, **got}, open(f"{OUT}/earlyF_{name}.json", "w"), indent=2)
