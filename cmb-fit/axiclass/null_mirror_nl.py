# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights.
"""Null-mirror diagnosis (CubeMind LATE_TWIST_NULL_MIRROR.md). AxiCLASS adds a scalar field to rho_m as rho - 3p and to
rho_r as 3p, so a frozen field (p = -rho) enters Omega_m(z) as +4 Omega_scf. Halofit reads that Omega_m. If the +1.35
offset comes from halofit, it should vanish when both LCDM and the frozen Late Twist are evaluated with non_linear = none.
Same fixed LCDM halofit best-fit parameters as null_mirror.py. No fit."""
import copy
import json
import math
import sys

sys.path.insert(0, "/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass")
from early_late_spa import make, OUT
from cobaya.model import get_model

lcdm = json.load(open(f"{OUT}/cmp_ax_spa_lcdm_halofit.json"))["minimum"]


def chi2(name, nl):
    info = copy.deepcopy(make(name))
    for k in ("sampler", "output", "resume", "force"):
        info.pop(k, None)
    th = info["theory"]
    cl = th["classy"] if "classy" in th else next(iter(th.values()))
    cl.setdefault("extra_args", {})["non_linear"] = nl
    model = get_model(info)
    sp = list(model.parameterization.sampled_params())
    r = model.logposterior({p: lcdm[p] for p in sp})
    om = model.provider.get_param("Omega_m") if "Omega_m" in model.provider.params else float("nan")
    return -2 * sum(r.loglikes), om


rows = []
for nl in ("halofit", "none"):
    c_l, om_l = chi2("ax_spa_lcdm_halofit", nl)
    for F, m in ((100.0, 0.015), (3.16, 0.5)):
        c_t, om_t = chi2(f"ax_spa_latetwist_gF{math.log10(F):.3f}m{math.log10(m):.3f}", nl)
        rows.append({"non_linear": nl, "F": F, "m": m, "chi2_lcdm": c_l, "chi2_lt": c_t, "diff": c_t - c_l,
                     "Omega_m_lcdm": om_l, "Omega_m_lt": om_t})
        print(f"{nl:8s} F={F:6.2f} m={m:5.3f}  LT-LCDM {c_t - c_l:+.3f}  Omega_m lcdm {om_l:.4f} lt {om_t:.4f}", flush=True)
json.dump(rows, open(f"{OUT}/null_mirror_nl.json", "w"), indent=1)
