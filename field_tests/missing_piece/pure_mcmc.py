"""PURE-MCMC (rule: field_tests/rules/PREREG_PURE_MCMC.md). AI-assisted.
    python pure_mcmc.py run PURE|LCDM   -> pure_mcmc/<M>.h5 (resumable) and pure_mcmc/<M>_status.json
    python pure_mcmc.py score            -> field_tests/results/pure_mcmc.json"""
import json, os, sys
import numpy as np
import emcee
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import tournament as T
AEG = T.AEG; RULE = os.path.join(AEG, "field_tests", "rules", "PREREG_PURE_MCMC.md")
OUTD = os.path.join(HERE, "pure_mcmc"); os.makedirs(OUTD, exist_ok=True)
P = json.load(open(os.path.join(AEG, "field_tests", "results", "pure_twist_predictions.json")))
BEST = {"PURE": P["pure_twist_params"], "LCDM": P["lcdm_params"]}
LO, HI = np.array([0.55, 0.018, 0.09]), np.array([0.80, 0.026, 0.15])
SETS = None; NW, MAXS, CHK = 12, 6000, 500


def chi2(m, q):
    full = list(q) + [0.0, 0.8165] if m == "PURE" else list(q)
    return T.chi2("SPIRAL" if m == "PURE" else "LCDM", full, SETS)


def logp(q, m):
    if np.any(q < LO) or np.any(q > HI):
        return -np.inf, 1e10
    x = chi2(m, q)
    return (-0.5 * x if x < 1e9 else -np.inf), x


def split_rhat(ch):                      # ch: (steps, walkers, ndim), kept half
    n = ch.shape[0] // 2; halves = np.concatenate([ch[:n], ch[n:2 * n]], axis=1)
    W = halves.var(axis=0, ddof=1).mean(axis=0); mean = halves.mean(axis=0)
    B = n * mean.var(axis=0, ddof=1); var = (n - 1) / n * W + B / n
    return np.sqrt(var / W)


def run(m):
    global SETS
    assert os.path.exists(RULE + ".sha256"), "rule not locked"
    SETS = T.bao_desi()
    be = emcee.backends.HDFBackend(os.path.join(OUTD, f"{m}.h5"))
    s = emcee.EnsembleSampler(NW, 3, logp, args=(m,), backend=be, blobs_dtype=float)
    start = None if be.iteration > 0 else np.array(BEST[m]) * (1 + 1e-3 * np.random.default_rng(1).standard_normal((NW, 3)))
    while be.iteration < MAXS:
        s.run_mcmc(start, CHK - be.iteration % CHK, progress=False); start = None
        it = be.iteration; ch = be.get_chain()[it // 2:]
        rh = split_rhat(ch) - 1
        try:
            tau = float(np.max(be.get_autocorr_time(discard=it // 2, quiet=True)))
        except Exception:
            tau = float("nan")
        conv = bool(np.all(rh < 0.02) and (it // 2) > 30 * tau)
        json.dump({"steps": it, "R_minus_1": rh.tolist(), "tau": tau, "converged": conv},
                  open(os.path.join(OUTD, f"{m}_status.json"), "w"))
        print(m, it, "R-1", np.round(rh, 4).tolist(), "tau", round(tau, 1), "converged", conv, flush=True)
        if conv:
            break


def summary(m):
    be = emcee.backends.HDFBackend(os.path.join(OUTD, f"{m}.h5"), read_only=True); it = be.iteration
    ch = be.get_chain(discard=it // 2, flat=True); x2 = be.get_blobs(discard=it // 2, flat=True)
    allx2 = be.get_blobs(flat=True)
    h, wb, wc = ch.T; d = {"H0": 100 * h, "Omega_m": (wb + wc) / h ** 2, "omega_b": wb, "omega_cdm": wc}
    q = lambda v: [float(np.percentile(v, p)) for p in (16, 50, 84)]
    st = json.load(open(os.path.join(OUTD, f"{m}_status.json")))
    return {"steps": it, "status": st, **{k: q(v) for k, v in d.items()}, "chi2_min_chain": float(np.min(allx2)),
            "chi2_mean_posterior": float(np.mean(x2))}


def score():
    pt = json.load(open(os.path.join(AEG, "field_tests", "results", "pure_twist.json")))
    out = {"rule": "PREREG_PURE_MCMC.md", "PURE": summary("PURE"), "LCDM": summary("LCDM")}
    out["delta_chi2_min"] = out["PURE"]["chi2_min_chain"] - out["LCDM"]["chi2_min_chain"]
    out["stored_best"] = {"note": "from pure_twist.json FULL fits", "raw": pt.get("FULL", pt)}
    conv = out["PURE"]["status"]["converged"] and out["LCDM"]["status"]["converged"]
    out["reading_inputs"] = {"converged": conv}
    json.dump(out, open(os.path.join(AEG, "field_tests", "results", "pure_mcmc.json"), "w"), indent=1, default=float)
    print(json.dumps(out, indent=1, default=float)[:3000])


if __name__ == "__main__":
    a = sys.argv[1:]
    run(a[1]) if a[0] == "run" else score()
