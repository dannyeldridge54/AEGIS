"""Frozen forward predictions from the stored best fits (for PREDICTIONS_LOCKED_2026-11-02.md). No data are compared.
    python forward_predictions.py eval <run>   -> fp_<run>.json   (WSL env 'aegis')
    python forward_predictions.py summary      -> forward_predictions.json
Per model: w(z) of the dark energy (scalar field, fluid or Lambda) on 0 <= z <= 3; a CPL fit w0 + wa (1 - a) to it on
0 <= z <= 2.5; BAO D_M/r_d and D_H/r_d on a redshift grid covering DESI; sigma8, Omega_m, H0 as stored."""
import json
import math
import os
import sys

import numpy as np

AXI = os.environ.get("TWIST_AXI", "/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass")
HERE = os.path.dirname(os.path.abspath(__file__))
ZB = [0.295, 0.51, 0.706, 0.934, 1.321, 1.484, 2.33, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.6, 2.0, 2.6, 3.0]
RUNS = {"Late Twist, Pantheon+": "ax_spa_latetwist_gF0.4m-0.3_nlfix",
        "Late Twist, DES Y5": "ax_spa_latetwist_gF0m0.102_desy5_nlfix",
        "Coupled Twist": "ax_spa_coupledtwist_gF0.4m-0.1_nlfix",
        "LCDM (halofit, Pantheon+)": "ax_spa_lcdm_halofit",
        "w0-wa (Pantheon+)": "ax_spa_w0wa_halofit"}
C_KMS = 299792.458


def evaluate(name):
    sys.path.insert(0, AXI)
    import early_late_spa as E
    from cobaya.model import get_model
    E._maybe_coupled(name)
    info = E.make(name)
    for k in ("sampler", "output", "resume", "force"):
        info.pop(k, None)
    model = get_model(info)
    stored = json.load(open(f"{E.OUT}/cmp_{name}.json"))["minimum"]
    res = model.logposterior({p: stored[p] for p in model.parameterization.sampled_params()})
    cl = model.theory["classytwist"].classy
    bg = cl.get_background()
    z = np.array(bg["z"])
    keys = list(bg.keys())
    if "(.)rho_scf" in bg:
        rho, p = np.array(bg["(.)rho_scf"]), np.array(bg["(.)p_scf"])
        w = p / rho
        kind = "scalar field"
    elif "(.)w_fld" in bg:
        w = np.array(bg["(.)w_fld"])
        kind = "fluid"
    else:
        w = -np.ones_like(z)
        kind = "Lambda"
    order = np.argsort(z)
    zg = np.linspace(0, 3, 61)
    wg = np.interp(zg, z[order], w[order])
    rd = cl.rs_drag()
    bao = {str(zz): {"DM_rd": cl.angular_distance(zz) * (1 + zz) / rd, "DH_rd": 1.0 / cl.Hubble(zz) / rd}   # classy Hubble is in 1/Mpc
           for zz in ZB}
    out = {"name": name, "kind": kind, "z": zg.tolist(), "w": wg.tolist(), "bao": bao, "rd": rd,
           "H0": stored.get("H0"), "sigma8": stored.get("sigma8"), "logpost": float(res.logpost),
           "logpost_stored": -float(stored["minuslogpost"]), "bg_keys_sample": keys[:40]}
    json.dump(out, open(os.path.join(HERE, f"fp_{name}.json"), "w"), indent=1)
    print(name, kind, "w(0)", wg[0], "rd", rd, "mirror", out["logpost"] - out["logpost_stored"])


def summary():
    rows = {}
    for label, n in RUNS.items():
        g = json.load(open(os.path.join(HERE, f"fp_{n}.json")))
        z, w = np.array(g["z"]), np.array(g["w"])
        sel = z <= 2.5
        a = 1 / (1 + z[sel])
        A = np.vstack([np.ones_like(a), 1 - a]).T
        (w0, wa), *_ = np.linalg.lstsq(A, w[sel], rcond=None)
        rows[label] = {"run": n, "kind": g["kind"], "w0_cpl": float(w0), "wa_cpl": float(wa),
                       "w_min": float(w.min()), "w_at": {str(zz): float(np.interp(zz, z, w)) for zz in (0, 0.5, 1, 2)},
                       "bao": g["bao"], "rd": g["rd"], "H0": g["H0"], "sigma8": g["sigma8"],
                       "mirror": abs(g["logpost"] - g["logpost_stored"])}
    json.dump(rows, open(os.path.join(HERE, "forward_predictions.json"), "w"), indent=1)
    for k, v in rows.items():
        print(f"{k:28s} {v['kind']:12s} w0 {v['w0_cpl']:+.3f} wa {v['wa_cpl']:+.3f} wmin {v['w_min']:+.3f} "
              f"rd {v['rd']:.2f} DM/rd(0.51) {v['bao']['0.51']['DM_rd']:.3f} DH/rd(0.51) {v['bao']['0.51']['DH_rd']:.3f} "
              f"mirror {v['mirror']:.3f}")


if __name__ == "__main__":
    evaluate(sys.argv[2]) if sys.argv[1] == "eval" else summary()
