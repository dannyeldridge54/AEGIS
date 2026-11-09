"""V6 Laplace step (PREREG_V6_EVIDENCE.md cross-check; deviation V6-D1 in V6_DEVIATIONS.md).
    python v6_laplace.py <run> [workers]          (PC, WSL env "aegis")
Numerical Hessian of -ln(L x prior) at the STORED best fit, by central differences in the sampled parameters
(step h_i = 0.25 x the fit's own proposal width, shrunk to stay inside the prior). Gives
  - the Laplace evidence  ln Z = ln L* + ln prior* + (d/2) ln 2pi + (1/2) ln det C,  C = H^-1, and
  - C as the starting proposal covariance for the V6 chains (Cobaya covmat file).
Gate: the centre point must reproduce the stored -ln posterior within 0.05, else no number is reported."""
import json
import math
import os
import sys
from multiprocessing import Pool

import numpy as np

import v6_chains as V

_MODEL = None


def _init(run):
    global _MODEL
    from cobaya.model import get_model
    info, _ = V.make(run)
    for k in ("sampler", "output", "resume", "force"):
        info.pop(k, None)
    _MODEL = get_model(info)


def _mlp(point):
    lp = _MODEL.logposterior(point)
    return -float(lp.logpost) if np.isfinite(lp.logpost) else float("inf")


def main(run, workers=8):
    out_dir = os.path.join(V.AEGIS, "cmb-fit", "results", "chains", "v6")
    os.makedirs(out_dir, exist_ok=True)
    res_path = os.path.join(V.AEGIS, "field_tests", "results", f"v6_laplace_{run}.json")
    info, E = V.make(run)
    m = json.load(open(os.path.join(E.OUT, f"cmp_{run}.json")))["minimum"]
    params = {k: v for k, v in info["params"].items() if isinstance(v, dict) and "prior" in v}
    names = list(params)
    x0 = np.array([m[k] if k in m else m["omega_cdm"] for k in names])
    h = []
    for k, x in zip(names, x0):
        p = params[k]
        s = 0.25 * float(p.get("proposal") or p.get("ref", {}).get("scale", 1e-3 * max(abs(x), 1e-3)))
        pr = p["prior"]
        if "min" in pr:
            s = min(s, 0.45 * (x - pr["min"]), 0.45 * (pr["max"] - x))
        h.append(max(s, 1e-8))
    h = np.array(h)
    d = len(names)
    pts = [x0.copy()]
    idx = {}
    for i in range(d):
        for sgn in (1, -1):
            p = x0.copy(); p[i] += sgn * h[i]; idx[(i, sgn)] = len(pts); pts.append(p)
    for i in range(d):
        for j in range(i + 1, d):
            for si in (1, -1):
                for sj in (1, -1):
                    p = x0.copy(); p[i] += si * h[i]; p[j] += sj * h[j]; idx[(i, j, si, sj)] = len(pts); pts.append(p)
    print(f"{run}: d={d}, {len(pts)} evaluations, {workers} workers", flush=True)
    with Pool(workers, initializer=_init, initargs=(run,)) as pool:
        f = pool.map(_mlp, [dict(zip(names, p)) for p in pts], chunksize=1)
    f = np.array(f)
    f0 = f[0]
    gate = abs(f0 - m["minuslogpost"])
    H = np.zeros((d, d))
    for i in range(d):
        H[i, i] = (f[idx[(i, 1)]] - 2 * f0 + f[idx[(i, -1)]]) / h[i] ** 2
        for j in range(i + 1, d):
            v = (f[idx[(i, j, 1, 1)]] - f[idx[(i, j, 1, -1)]] - f[idx[(i, j, -1, 1)]] + f[idx[(i, j, -1, -1)]])
            H[i, j] = H[j, i] = v / (4 * h[i] * h[j])
    ev = np.linalg.eigvalsh(H)
    posdef = bool(ev.min() > 0)
    res = {"run": run, "params": names, "steps": h.tolist(), "minuslogpost_centre": f0,
           "minuslogpost_stored": m["minuslogpost"], "gate_abs_diff": gate, "gate_pass": gate <= 0.05,
           "hessian_eigen_min": float(ev.min()), "hessian_posdef": posdef, "n_evaluations": len(pts)}
    if posdef:
        C = np.linalg.inv(H)
        sign, logdet = np.linalg.slogdet(C)
        res["lnZ_laplace"] = -f0 + 0.5 * d * math.log(2 * math.pi) + 0.5 * logdet
        res["sigma"] = dict(zip(names, np.sqrt(np.diag(C)).tolist()))
        cov = os.path.join(out_dir, f"{run}.covmat")
        with open(cov, "w") as fh:
            fh.write("# " + " ".join(names) + "\n")
            np.savetxt(fh, C)
        res["covmat"] = cov
    else:   # chains then start with a diagonal proposal from the positive curvatures (reported)
        diag = np.where(np.diag(H) > 0, 1 / np.maximum(np.diag(H), 1e-300), (2 * h) ** 2)
        cov = os.path.join(out_dir, f"{run}.covmat")
        with open(cov, "w") as fh:
            fh.write("# " + " ".join(names) + "\n")
            np.savetxt(fh, np.diag(diag))
        res["covmat"] = cov
        res["lnZ_laplace"] = None
        res["note"] = "Hessian not positive definite: no Laplace evidence; diagonal proposal written"
    json.dump(res, open(res_path, "w"), indent=1)
    print(json.dumps({k: res[k] for k in ("run", "gate_abs_diff", "gate_pass", "hessian_posdef", "lnZ_laplace")}),
          flush=True)


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 8)
