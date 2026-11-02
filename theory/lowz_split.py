"""LZ part of PREREGISTRATION_SOLAR_LOWZ.md (locked 2026-11-02 15:17:31): split the DES Y5 supernova chi2 at z = 0.1.
Runs in WSL, micromamba env 'aegis', one model per process (the two models use different AxiCLASS builds):
    python lowz_split.py eval ax_spa_latetwist_gF0m0.102_desy5_nlfix   -> lowz_<name>.npz
    python lowz_split.py eval ax_spa_lcdm_halofit_desy5                 -> lowz_<name>.npz
    python lowz_split.py score                                          -> lowz_split.json
Each model is rebuilt with early_late_spa.make(name) and evaluated at its stored minimum (no refit)."""
import json
import os
import sys

import numpy as np

AXI = os.environ.get("TWIST_AXI", "/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass")
HERE = os.path.dirname(os.path.abspath(__file__))
TWIST, LCDM = "ax_spa_latetwist_gF0m0.102_desy5_nlfix", "ax_spa_lcdm_halofit_desy5"
ZCUT = 0.1


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
    point = {p: stored[p] for p in model.parameterization.sampled_params()}
    res = model.logposterior(point)
    lik = model.likelihood["sn.desy5"]
    da = lik.provider.get_angular_diameter_distance(lik.zcmb)
    lumdists = 5 * np.log10((1 + lik.zhel) * (1 + lik.zcmb) * da)
    chi2_own = -2 * float(lik.logp())
    np.savez(os.path.join(HERE, f"lowz_{name}.npz"), zcmb=lik.zcmb, mag=lik.mag, lumdists=lumdists,
             cov=lik.covs["mag"], pre_vars=np.broadcast_to(lik.pre_vars, lik.zcmb.shape), invcov=lik.invcov,
             chi2_own=chi2_own, chi2_stored=stored.get("chi2__sn.desy5", np.nan),
             logpost=res.logpost, logpost_stored=-stored["minuslogpost"])
    print(name, "own chi2", chi2_own, "stored", stored.get("chi2__sn.desy5"), "logpost", res.logpost,
          "stored", -stored["minuslogpost"])


def chi2_marg(d, C):
    """chi2 with the absolute magnitude marginalised exactly as the likelihood does (projection, no log term)."""
    ic = np.linalg.inv(C)
    u = ic.sum(axis=1)
    P = ic - np.outer(u, u) / u.sum()
    return float(d @ P @ d)


def score():
    out, parts = {}, {}
    for key, name in (("twist", TWIST), ("lcdm", LCDM)):
        f = np.load(os.path.join(HERE, f"lowz_{name}.npz"))
        d = f["mag"] - f["lumdists"]
        C = f["cov"] + np.diag(f["pre_vars"])
        full_mine = float(d @ f["invcov"] @ d)
        lo, hi = f["zcmb"] <= ZCUT, f["zcmb"] > ZCUT
        parts[key] = {"full_recomputed": full_mine, "full_own_logp": float(f["chi2_own"]),
                      "full_stored": float(f["chi2_stored"]), "full_from_cov": chi2_marg(d, C),
                      "low": chi2_marg(d[lo], C[np.ix_(lo, lo)]), "high": chi2_marg(d[hi], C[np.ix_(hi, hi)]),
                      "n_low": int(lo.sum()), "n_high": int(hi.sum()),
                      "logpost": float(f["logpost"]), "logpost_stored": float(f["logpost_stored"])}
    mirror = all(abs(parts[k]["full_recomputed"] - parts[k]["full_stored"]) <= 0.05 for k in parts)
    d_full = parts["twist"]["full_recomputed"] - parts["lcdm"]["full_recomputed"]
    d_high = parts["twist"]["high"] - parts["lcdm"]["high"]
    d_low = parts["twist"]["low"] - parts["lcdm"]["low"]
    r = d_high / d_full
    if not mirror:
        verdict = "NO VERDICT (mirror failed)"
    elif r < 0.5:
        verdict = "CALIBRATION-SENSITIVE"
    elif r < 0.8:
        verdict = "MIXED"
    else:
        verdict = "ROBUST TO LOW-Z"
    out = {"zcut": ZCUT, "parts": parts, "mirror_pass": mirror, "delta_full": d_full, "delta_high": d_high,
           "delta_low": d_low, "r": r, "verdict": verdict}
    json.dump(out, open(os.path.join(HERE, "lowz_split.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


def context(name):
    """Post-hoc context (no rule, no verdict): the same split for another model against LCDM, e.g. w0-wa."""
    vals = {}
    for key, n in (("model", name), ("lcdm", LCDM)):
        f = np.load(os.path.join(HERE, f"lowz_{n}.npz"))
        d = f["mag"] - f["lumdists"]
        C = f["cov"] + np.diag(f["pre_vars"])
        lo, hi = f["zcmb"] <= ZCUT, f["zcmb"] > ZCUT
        vals[key] = (float(d @ f["invcov"] @ d), chi2_marg(d[lo], C[np.ix_(lo, lo)]), chi2_marg(d[hi], C[np.ix_(hi, hi)]))
    out = {"model": name, "delta_full": vals["model"][0] - vals["lcdm"][0],
           "delta_low": vals["model"][1] - vals["lcdm"][1], "delta_high": vals["model"][2] - vals["lcdm"][2]}
    out["r"] = out["delta_high"] / out["delta_full"]
    json.dump(out, open(os.path.join(HERE, f"lowz_context_{name}.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    {"eval": lambda: evaluate(sys.argv[2]), "context": lambda: context(sys.argv[2])}.get(sys.argv[1], score)()
