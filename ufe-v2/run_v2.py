"""AEGIS UFE v2 — fit LCDM, the v1 legacy-beta model, and the v2 torsion-born EDE model to
CMB theta* + DESI DR2 BAO + Pantheon+ (full covariance), with and without the SH0ES H0 prior."""
import json, sys, time
import numpy as np
from scipy.optimize import minimize
from aegis.cosmo_v2 import LCDM, LegacyBeta, TorsionField
from aegis.likelihood_v2 import Likelihood

PANTHEON = sys.argv[1] if len(sys.argv) > 1 else "data/pantheon/pantheon_binned_fullcov.json"

MODELS = {
    "LCDM":       (lambda p: LCDM(p[0], p[1]),                     [(0.6, 0.8), (0.10, 0.17)], ["h", "omega_c"]),
    "LegacyBeta": (lambda p: LegacyBeta(p[0], p[1], p[2], p[3]),    [(0.6, 0.8), (0.10, 0.17), (-0.3, 0.3), (-1.0, 1.0)],
                   ["h", "omega_c", "beta0", "beta1"]),
    "TorsionField": (lambda p: TorsionField(p[0], p[1], p[2], p[3]), [(0.6, 0.8), (0.10, 0.18), (7.0, 10.5), (0.03, 0.45)],
                   ["h", "omega_c", "log10_v0", "F"]),
}

def fit(L, key, starts, rng):
    build, bounds, names = MODELS[key]
    lo, hi = np.array(bounds).T
    def obj(x):
        if np.any(x < lo) or np.any(x > hi):
            return 1e12
        return L.chi2(build(x))
    best = None
    for s in starts:
        r = minimize(obj, s, method="Nelder-Mead",
                     options=dict(xatol=1e-6, fatol=1e-4, maxiter=6000, maxfev=6000))
        if best is None or r.fun < best.fun:
            best = r
    # polish
    best = minimize(obj, best.x, method="Nelder-Mead", options=dict(xatol=1e-7, fatol=1e-5, maxiter=6000))
    parts = L.parts(build(best.x)); d = parts["derived"]
    return dict(model=key, params=dict(zip(names, map(float, best.x))), chi2=float(best.fun),
                chi2_parts={k: float(parts[k]) for k in ("cmb", "bao", "sn", "h0")},
                H0=d["H0"], Om=d["Om"], rs=d["rs"], rd=d["rd"], rdh=d["rdh"], M_B=float(parts["M_B"]),
                n_params=len(names),
                **({"f_peak": build(best.x).f, "z_c": build(best.x).zc} if key == "TorsionField" else {}))

def starts_for(key, rng, n=6):
    _, bounds, _ = MODELS[key]
    lo, hi = np.array(bounds).T
    base = {"LCDM": [0.68, 0.12], "LegacyBeta": [0.68, 0.12, 0.0, 0.0],
            "TorsionField": [0.70, 0.135, 8.7, 0.16]}[key]
    pts = [np.array(base)]
    for _ in range(n - 1):
        pts.append(lo + (hi - lo) * (0.2 + 0.6 * rng.random(len(lo))))
    return pts

if __name__ == "__main__":
    rng = np.random.default_rng(2026)
    out = {}
    for label, kw in [("no_SH0ES", dict(use_shoes=False)), ("with_SH0ES", dict(use_shoes=True))]:
        L = Likelihood(PANTHEON, **kw)
        out[label] = {}
        for key in MODELS:
            t = time.time()
            r = fit(L, key, starts_for(key, rng), rng)
            out[label][key] = r
            print(f"[{label}] {key:11s} chi2={r['chi2']:8.2f}  H0={r['H0']:6.2f}  Om={r['Om']:.4f}  "
                  f"rs={r['rs']:6.2f}  rd*h={r['rdh']:6.2f}  params={ {k: round(v, 4) for k, v in r['params'].items()} }  "
                  f"parts={ {k: round(v, 2) for k, v in r['chi2_parts'].items()} }  ({time.time()-t:.0f}s)", flush=True)
    json.dump(out, open("results_v2.json", "w"), indent=2)
