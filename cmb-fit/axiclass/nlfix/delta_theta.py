# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights.
"""B4 input (CubeMind T2_PHOTON_COUPLING_LOG.md): how far the Late Twist field angle theta = phi/F moved between recombination
and today, at the corrected-code (NR) best fits. Evaluates each best-fit point once on the fixed build (no fitting) and
reads phi_scf(z) from AxiCLASS's background table. Prints theta(z_rec), theta(0) and delta_theta.
    python delta_theta.py <run> [<run> ...]       (run names ending in _nlfix)"""
import copy
import json
import sys

sys.path.insert(0, "/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass")
import early_late_spa as E                                      # noqa: E402

E._maybe_coupled(sys.argv[1])
from cobaya.model import get_model                              # noqa: E402
import numpy as np                                              # noqa: E402

out = {}
for run in sys.argv[1:]:
    best = json.load(open(f"{E.OUT}/cmp_{run}.json"))["minimum"]
    info = copy.deepcopy(E.make(run))
    for k in ("sampler", "output", "resume", "force"):
        info.pop(k, None)
    model = get_model(info)
    pt = {p: best[p] for p in model.parameterization.sampled_params()}
    model.logposterior(pt)
    th = model.theory[next(iter(model.theory))]
    cl = getattr(th, "classy", None) or getattr(th, "classy_module", None)
    bg = cl.get_background()
    keys = list(bg.keys())
    z = np.array(bg["z"])
    pk = [k for k in keys if "phi_scf" in k and "prime" not in k and "'" not in k]
    phi = np.array(bg[pk[0]])
    F = info["theory"][next(iter(info["theory"]))]["extra_args"]["f_axion"]
    zr = 1089.9
    i_r = int(np.argmin(abs(z - zr))); i_0 = int(np.argmin(abs(z)))
    th_r, th_0 = phi[i_r] / F, phi[i_0] / F
    out[run] = {"F": F, "phi_key": pk[0], "theta_rec": th_r, "theta_today": th_0, "delta_theta": th_0 - th_r,
                "phi_units_note": "AxiCLASS phi_scf and f_axion share units, so phi/F is unit-free"}
    print(f"{run}: F={F:.3f}  theta(z={z[i_r]:.0f})={th_r:.5f}  theta(0)={th_0:.5f}  delta_theta={th_0 - th_r:+.5f}"
          f"  [key {pk[0]}; available: {[k for k in keys if 'scf' in k]}]", flush=True)
json.dump(out, open(f"{E.OUT}/b4_delta_theta.json", "w"), indent=1)
