"""DEVIATION D1 (UB1_DEVIATIONS.md): identical to the locked unify_hyperbolic_bg.py except the integrator (DOP853, not LSODA).
UB step 1: can the coupled BI axion-dilaton (hyperbolic field space, lambda fixed) do BOTH dark-energy jobs?
Rule: field_tests/rules/PREREG_UNIFY_BG.md (locked before this was run).
    python unify_hyperbolic_bg_v2.py         -> unify_hyperbolic_bg_v2.json
    python unify_hyperbolic_bg.py --smoke    -> timing only, prints no requirement results

Background only (no perturbations, no data). Units M_Pl = 1, densities in units of 3 H_fid^2.
Fields: canonical dilaton chi (|phi| = exp(S chi), S = sqrt(2/3)) and BI angle th with kinetic metric
    G = diag(1, F(chi)^2),  F(chi) = F_P exp(lam chi / 2),  lam = -2 sqrt(2/3),  F_P = (4/pi) sqrt(3/2)
so F = F_P/|phi| (Nieh-Yan, F = F_P at |phi| = 1). Potential V = A U(chi) + L (1 - cos th)^3 (n = 3, fixed).
    variant A (derived): U = (p - 1) exp(6 p) / p^2, p = |phi|   (GKY Kahler, constant W; no cosmological constant)
    variant B (Spiral form): U = exp(kappa chi), kappa in [-3, 3]   (one extra slope, as in the late Spiral)
No cosmological constant anywhere: today's dark energy must come from the field.
Equations in N = ln a (' = d/dN), eps = -dlnH/dN:
    chi'' = -(3 - eps) chi' + (lam/2) F^2 th'^2 - V_chi / H^2
    th''  = -(3 - eps) th'  - lam chi' th'      - V_th / (F^2 H^2)
    H^2 = (rho_r + rho_m + V) / (3 - K),  K = (chi'^2 + F^2 th'^2)/2,  eps = K + (rho_m + 4 rho_r/3)/(2 H^2)
"""
import json
import math
import sys
import time

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize

np.seterr(all="ignore")
S = math.sqrt(2 / 3)
LAM = -2 * S
FP = 4 / math.pi * math.sqrt(1.5)
OM, OR = 0.31, 9.0e-5
N0 = math.log(1e-8)
SEED, NSAMP, NPOLISH = 20261107, 20000, 40
ZPK = (2000.0, 6000.0)        # R2 peak window
FPK = (0.03, 0.15)            # R2 peak size
R3 = 0.5                      # R3: f(z=1090) <= R3 * f_peak
R4 = 0.02                     # R4: max f over 20 <= z <= 500
W0 = (-1.0, -0.7)             # R5 w0 window
OMW = (0.29, 0.33)            # R5 Omega_m today window


def F(c):
    return FP * math.exp(LAM * c / 2)


def U(c, var, k):
    if var == "A":
        p = math.exp(S * c)
        return (p - 1) * math.exp(6 * p) / p ** 2, ((math.exp(6 * p) / p ** 2) + (p - 1) * (6 - 2 / p) * math.exp(6 * p) / p ** 2) * S * p
    e = math.exp(k * c)
    return e, k * e


def solve(par, var):
    """par = (lnA, lnL, th_i, phi_i[, kappa]). Returns dict of diagnostics or None if the integration failed."""
    lnA, lnL, thi, phii = par[:4]
    k = par[4] if var == "B" else 0.0
    if not (0.01 < thi < math.pi - 0.01 and 1.05 < phii < 80 and -3 <= k <= 3):
        return None
    A, L = math.exp(lnA), math.exp(lnL)
    c0 = math.log(phii) / S

    def parts(N, y):
        c, th, cp, tp = y
        a = math.exp(N)
        rr, rm = 3 * OR / a ** 4, 3 * OM / a ** 3
        u, du = U(c, var, k)
        f2 = F(c) ** 2
        V = A * u + L * (1 - math.cos(th)) ** 3
        K = (cp * cp + f2 * tp * tp) / 2
        H2 = (rr + rm + V) / (3 - K)
        if not (H2 > 0 and math.isfinite(H2) and K < 3):
            raise ValueError("H^2 <= 0 or kinetic domination")
        return rr, rm, V, K, H2, du, f2

    def rhs(N, y):
        c, th, cp, tp = y
        rr, rm, V, K, H2, du, f2 = parts(N, y)
        eps = K + (rm + 4 * rr / 3) / (2 * H2)
        Vth = L * 3 * (1 - math.cos(th)) ** 2 * math.sin(th)
        return [cp, tp, -(3 - eps) * cp + LAM / 2 * f2 * tp * tp - A * du / H2,
                -(3 - eps) * tp - LAM * cp * tp - Vth / (f2 * H2)]

    try:
        sol = solve_ivp(rhs, (N0, 0.0), [c0, thi, 0.0, 0.0], method="DOP853", rtol=1e-7, atol=1e-10,
                        dense_output=True)
    except (OverflowError, ValueError, ZeroDivisionError):
        return None
    if sol.status != 0:
        return None

    def at(z):
        N = -math.log(1 + z)
        y = sol.sol(N)
        rr, rm, V, K, H2, du, f2 = parts(N, y)
        rf = K * H2 + V
        return rf / (rf + rr + rm), (K * H2 - V) / (K * H2 + V) if rf > 0 else float("nan"), H2, rm

    zs = np.concatenate([np.geomspace(1e5, 6000, 40), np.geomspace(6000, 2000, 60), np.geomspace(2000, 500, 40),
                         np.geomspace(500, 20, 50), np.geomspace(20, 1e-6, 40)])
    try:
        fz = np.array([at(z)[0] for z in zs])
        f0, w0, h2, rm0 = at(0.0)
        f1090 = at(1090.0)[0]
    except (OverflowError, ValueError):
        return None
    if not (np.all(np.isfinite(fz)) and all(map(math.isfinite, (f0, w0, h2, f1090)))):
        return None
    win = (zs >= ZPK[0]) & (zs <= ZPK[1])
    mid = (zs >= 20) & (zs <= 500)
    early = zs >= 1500
    ipk = int(np.argmax(np.where(early, fz, -1)))
    return {"f_peak": float(fz[ipk]), "z_peak": float(zs[ipk]), "peak_in_window": bool(win[ipk]),
            "f_1090": float(f1090), "f_max_20_500": float(fz[mid].max()), "w0": float(w0),
            "Om0": float(rm0 / (3 * h2)), "phi_today": float(math.exp(S * sol.sol(0.0)[0])),
            "F_today": float(F(sol.sol(0.0)[0])),
            "F_at_peak": float(F(sol.sol(-math.log(1 + zs[ipk]))[0]))}


def miss(d):
    """Sum of fractional misses of R2-R5 (0 = all met)."""
    if d is None:
        return 1e3
    m = 0.0
    m += max(0, math.log(ZPK[0] / d["z_peak"]), math.log(d["z_peak"] / ZPK[1]))
    m += max(0, (FPK[0] - d["f_peak"]) / FPK[0], (d["f_peak"] - FPK[1]) / FPK[1])
    m += max(0, d["f_1090"] / max(d["f_peak"], 1e-12) - R3)
    m += max(0, d["f_max_20_500"] - R4) / R4
    w = d["w0"] if d["w0"] == d["w0"] else 1.0
    m += max(0, W0[0] - w, w - W0[1]) / 0.3
    m += max(0, OMW[0] - d["Om0"], d["Om0"] - OMW[1]) / 0.02
    return m


def met(d):
    if d is None:
        return {}
    return {"R2_peak": d["peak_in_window"] and FPK[0] <= d["f_peak"] <= FPK[1],
            "R3_fades": d["f_1090"] <= R3 * d["f_peak"],
            "R4_quiet": d["f_max_20_500"] <= R4,
            "R5_late": W0[0] <= d["w0"] <= W0[1] and OMW[0] <= d["Om0"] <= OMW[1]}


def box(var):
    lo = [-400.0 if var == "A" else -60.0, 0.0, 0.1, 1.1] + ([-3.0] if var == "B" else [])
    hi = [5.0, 40.0, 3.0, 60.0] + ([3.0] if var == "B" else [])
    return np.array(lo), np.array(hi)


def search(var, nsamp=NSAMP, npol=NPOLISH, rng=None):
    lo, hi = box(var)
    pts = lo + (hi - lo) * rng.random((nsamp, len(lo)))
    scored = []
    for p in pts:
        scored.append((miss(solve(p, var)), p))
    scored.sort(key=lambda t: t[0])
    best = None
    for m0, p0 in scored[:npol]:
        r = minimize(lambda p: miss(solve(p, var)), p0, method="Nelder-Mead",
                     options={"maxfev": 400, "xatol": 1e-3, "fatol": 1e-4})
        if best is None or r.fun < best[0]:
            best = (r.fun, r.x)
        if r.fun == 0:
            break
    d = solve(best[1], var)
    return {"variant": var, "samples": nsamp, "polished": npol, "best_miss": round(float(best[0]), 4),
            "best_params(lnA, lnL, th_i, phi_i[, kappa])": [round(float(x), 4) for x in best[1]],
            "best_point": {k: (round(v, 5) if isinstance(v, float) else v) for k, v in (d or {}).items()},
            "requirements": met(d), "ALL_MET": best[0] == 0 and all(met(d).values())}


def main():
    rng = np.random.default_rng(SEED)
    if "--smoke" in sys.argv:
        t = time.time()
        n = sum(solve(p, "A") is not None for p in (box("A")[0] + (box("A")[1] - box("A")[0]) * rng.random((5, 4))))
        print(f"smoke: {n}/5 integrations ok, {time.time() - t:.1f}s")
        return
    rows = [search("A", rng=rng), search("B", rng=rng)]
    verdict = "PASS" if any(r["ALL_MET"] for r in rows) else "FAIL"
    out = {"rule": "field_tests/rules/PREREG_UNIFY_BG.md", "verdict": verdict, "rows": rows,
           "reading": ("PASS: some setting of the free scales and starting values meets R2-R5 -> write and lock the "
                       "step-2 data test. FAIL: none found in the locked search box; this does not prove impossibility, "
                       "and the closest point and its missed requirements are reported. Neither is evidence about data.")}
    json.dump(out, open("unify_hyperbolic_bg_v2.json", "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
