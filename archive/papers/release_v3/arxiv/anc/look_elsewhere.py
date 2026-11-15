"""ROUTE.md A2: look-elsewhere calibration of the combined-data Twist preference (PREREGISTRATION_LOOK_ELSEWHERE.md),
following Gross & Vitells, Eur. Phys. J. C 70, 525 (2010), with 1 degree of freedom and the f >= 0 boundary.
Reads the fixed-angle runs from AEGIS results. Run: python look_elsewhere.py   -> table and LOOK_ELSEWHERE_RESULTS.json
"""
import json
import math
from pathlib import Path

from scipy.stats import chi2, norm

R = Path(r"C:\Users\Danny\.copilot\repos\AEGIS\cmb-fit\results")
THETAS = (0.5, 1.0, 1.5, 2.0, 2.4, 2.7, 2.9, 3.05)
CHI2_LCDM = 2402.40          # spa_lcdm (fixed in the pre-registration)


def p_local(u):
    return 0.5 * chi2.sf(u, 1)            # half chi^2_1: f >= 0 boundary


def z_of(p):
    return norm.isf(p) if p < 0.5 else 0.0


def upcrossings(xs, qs, u0):
    return sum(1 for a, b in zip(qs, qs[1:]) if a < u0 <= b)


def main():
    pts = []
    for th in THETAS:
        f = R / f"cmp_spa_edelock_th{th}.json"
        if not f.exists():
            print("missing", f.name)
            return
        m = json.load(open(f))["minimum"]
        pts.append((th, max(0.0, CHI2_LCDM - m["chi2"]), m.get("fde_zc"), m.get("H0")))
    free = json.load(open(R / "cmp_spa_edelock.json"))["minimum"]
    pts.append((free["theta_i"], max(0.0, CHI2_LCDM - free["chi2"]), free["fde_zc"], free["H0"]))
    pts.sort()
    print("theta_i   q = chi2(LCDM) - chi2(theta)   f_EDE    H0")
    for th, q, f, h in pts:
        print(f"{th:6.3f}   {q:8.2f}                      {f:.3f}   {h:.2f}")
    xs = [0.1] + [p[0] for p in pts] + [3.1]
    qs = [0.0] + [p[1] for p in pts] + [pts[-1][1]]       # q -> 0 at theta -> 0.1 (field barely moves)
    u = max(qs)
    pl = p_local(u)
    out = {"points": pts, "u": u, "p_local": pl, "Z_local": z_of(pl)}
    print(f"\nmax q = {u:.2f}: p_local = {pl:.4f}, Z_local = {z_of(pl):.2f}   (naive chi2_2: "
          f"{z_of(chi2.sf(u, 2)):.2f} sigma two-sided-equivalent shown in the paper)")
    for u0 in (0.5, 1.0):
        n0 = upcrossings(xs, qs, u0)
        pg = min(1.0, pl + n0 * math.exp(-(u - u0) / 2))
        out[f"u0={u0}"] = {"N0": n0, "p_global": pg, "Z_global": z_of(pg)}
        print(f"u0 = {u0}: upcrossings N0 = {n0}, p_global = {pg:.4f}, Z_global = {z_of(pg):.2f}")
    zc = min(out["u0=0.5"]["Z_global"], out["u0=1.0"]["Z_global"])
    verdict = ("mild evidence survives" if zc >= 2 else "a weak hint" if zc >= 1 else "consistent with noise")
    out["Z_global_conservative"] = zc
    out["verdict"] = verdict
    print(f"\nconservative Z_global = {zc:.2f} -> {verdict}")
    json.dump(out, open("LOOK_ELSEWHERE_RESULTS.json", "w"), indent=1)


if __name__ == "__main__":
    main()
