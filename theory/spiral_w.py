"""Spiral Twist background (exploratory feasibility, NOT a pre-registered test): what w0-wa would a CPL analysis see?
    python spiral_w.py validate   -> checks: LCDM limit, single-field limit, energy conservation
    python spiral_w.py scan       -> spiral_w_scan.json + summary
Model (Einstein frame, Reading B: matter blind to the dilaton; reduced Planck units, H in units of H0):
    L = -1/2 (d chi)^2 - 1/2 e^(lam chi) (d theta)^2 - V,   V = V0 e^(-kap chi) + m^2 F^2 (1 - cos(theta/F))
    lam = -2 sqrt(2/3) (alpha = 1, bi_kahler_lambda.py); F = (4/pi) sqrt(3/2) (Nieh-Yan period, nieh_yan_period.py).
Free: kap (dilaton steepness), m (angle mass, units H0), theta_i (starting angle); V0 is tuned for closure (H(0) = 1).
The 'CPL illusion' fits (Om_eff, w0, wa) to the model's H(z) on 0 < z < 2.5, assuming matter dilutes as a^-3."""
import json
import math
import os
import sys

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, least_squares

LAM = -2 * math.sqrt(2 / 3)
FDEC = 4 / math.pi * math.sqrt(1.5)
OM, ORAD = 0.30, 9.0e-5            # true matter and radiation today (matter blind to the fields)
N0 = -math.log(1 + 1e5)
ZFIT = np.linspace(0.0, 2.5, 120)


def solve(V0, kap, m, th0, lam=LAM, F=FDEC, chi0=0.0, dense=True, tp0=0.0, N1=0.0, cp0=0.0):
    def V(c, t):
        return V0 * math.exp(-kap * c) + m * m * F * F * (1 - math.cos(t / F))

    def rhs(N, y):
        c, cp, t, tp = y
        e = math.exp(lam * c)
        rm, rr = 3 * OM * math.exp(-3 * N), 3 * ORAD * math.exp(-4 * N)
        kin = 0.5 * cp * cp + 0.5 * e * tp * tp
        if kin >= 3:
            return [0, 0, 0, 0]
        H2 = (rm + rr + V(c, t)) / (3 - kin)
        eps = (rm + 4 * rr / 3 + H2 * (cp * cp + e * tp * tp)) / (2 * H2)
        Vc = -kap * V0 * math.exp(-kap * c)
        Vt = m * m * F * math.sin(t / F)
        cpp = -(3 - eps) * cp + 0.5 * lam * e * tp * tp - Vc / H2
        tpp = -(3 - eps) * tp - lam * cp * tp - Vt / (e * H2)
        return [cp, cpp, tp, tpp]

    sol = solve_ivp(rhs, (N0, N1), [chi0, cp0, th0, tp0], method="LSODA", rtol=1e-9, atol=1e-11,
                    dense_output=dense)
    return sol, V


def H2_of(sol, V, N, lam=LAM):
    c, cp, t, tp = sol.sol(N)
    e = math.exp(lam * c)
    rm, rr = 3 * OM * math.exp(-3 * N), 3 * ORAD * math.exp(-4 * N)
    kin = 0.5 * cp * cp + 0.5 * e * tp * tp
    H2 = (rm + rr + V(c, t)) / (3 - kin)
    rho_de = H2 * kin + V(c, t)
    p_de = H2 * kin - V(c, t)
    return H2, rho_de, p_de


def closed(kap, m, th0, **kw):
    """Tune V0 so that H(z=0) = 1."""
    def f(V0):
        sol, V = solve(V0, kap, m, th0, dense=True, **kw)
        return H2_of(sol, V, 0.0, kw.get("lam", LAM))[0] - 1 if sol.success else 1e3
    lo, hi = 0.0, 10.0
    if f(lo) > 0:
        raise ValueError("overclosed: the angle alone exceeds the dark-energy budget")
    while f(hi) < 0:
        hi *= 10
        if hi > 1e6:
            raise ValueError("cannot close: the dilaton runs away too fast to supply the dark energy")
    V0 = brentq(f, lo, hi, xtol=1e-10)
    sol, V = solve(V0, kap, m, th0, **kw)
    return V0, sol, V


def cpl_fit(sol, V, lam=LAM):
    E2 = np.array([H2_of(sol, V, -math.log(1 + z), lam)[0] for z in ZFIT])

    def model(p):
        om, w0, wa = p
        a = 1 / (1 + ZFIT)
        de = (1 - om - ORAD) * a ** (-3 * (1 + w0 + wa)) * np.exp(-3 * wa * (1 - a))
        return om * (1 + ZFIT) ** 3 + ORAD * (1 + ZFIT) ** 4 + de

    r = least_squares(lambda p: (model(p) - E2) / E2, [0.3, -0.9, -0.2],
                      bounds=([0.1, -3, -5], [0.6, 1, 3]))
    resid = float(np.max(np.abs((model(r.x) - E2) / E2)))
    return {"Om_eff": float(r.x[0]), "w0": float(r.x[1]), "wa": float(r.x[2]), "max_rel_resid": resid}


def w_true(sol, V, lam=LAM):
    out = {}
    for z in (0.0, 0.5, 1.0, 2.0):
        H2, rho, p = H2_of(sol, V, -math.log(1 + z), lam)
        out[str(z)] = p / rho
    return out


def validate():
    # 1) LCDM limit: kap = 0, m = 0 -> V = V0 constant; CPL fit must give w0 = -1, wa = 0, Om_eff = OM
    V0, sol, V = closed(0.0, 0.0, 1.0)
    f1 = cpl_fit(sol, V)
    # 2) single-field limit: lam = 0 and kap large (dilaton frozen at a tiny V0 contribution) is not clean; instead
    #    lam = 0 and kap = 0: the angle is an ordinary thawing cosine on top of Lambda -> w0 > -1, wa < 0, never < -1
    V0b, solb, Vb = closed(0.0, 1.0, 1.5, lam=0.0)
    f2 = cpl_fit(solb, Vb, lam=0.0)
    wt2 = w_true(solb, Vb, lam=0.0)
    # 3) energy: w_true of the full spiral never below -1 (null energy condition)
    V0c, solc, Vc = closed(1.0, 10.0, 0.15)
    wt3 = [p / r for r, p in (H2_of(solc, Vc, N)[1:] for N in np.linspace(-math.log(3.5), 0, 200))]
    out = {"LCDM_limit": f1, "single_field_limit": {"cpl": f2, "w_true": wt2},
           "spiral_min_w_true": float(min(wt3))}
    print(json.dumps(out, indent=1))
    ok = (abs(f1["w0"] + 1) < 1e-3 and abs(f1["wa"]) < 1e-3 and abs(f1["Om_eff"] - OM) < 1e-3
          and min(wt2.values()) >= -1 - 1e-9 and out["spiral_min_w_true"] >= -1 - 1e-9)
    print("VALIDATION", "PASS" if ok else "FAIL")
    return ok


def scan():
    rows = []
    for kap in (0.0, 1.0, 3.0, 5.0, 7.0):
        for m in (1.0, 3.0, 10.0, 30.0):
            for th0 in (0.05, 0.15, 0.5, 1.5):
                try:
                    V0, sol, V = closed(kap, m, th0)
                except Exception as ex:
                    rows.append({"kap": kap, "m": m, "theta_i": th0, "error": str(ex)[:80]})
                    continue
                f = cpl_fit(sol, V)
                rows.append({"kap": kap, "m": m, "theta_i": th0, "V0": V0, **f,
                             "w_true": w_true(sol, V), "chi_today": float(sol.sol(0.0)[0])})
                r = rows[-1]
                print(f"kap {kap:3.0f} m {m:5.1f} th {th0:3.1f} | Om_eff {r['Om_eff']:.3f} w0 {r['w0']:+.3f} "
                      f"wa {r['wa']:+.3f} resid {r['max_rel_resid']:.1e} | w(0) {r['w_true']['0.0']:+.3f}", flush=True)
    good = [r for r in rows if "w0" in r]
    desi_like = [r for r in good if -0.9 <= r["w0"] <= -0.7 and r["wa"] <= -0.4 and r["max_rel_resid"] < 0.01]
    illusion = [r for r in good if r["w0"] + r["wa"] < -1 and r["max_rel_resid"] < 0.01]
    json.dump({"rows": rows, "n_desi_like": len(desi_like), "n_phantom_illusion": len(illusion),
               "desi_like": desi_like, "fixed": {"lambda": LAM, "F": FDEC, "Om_true": OM}},
              open("spiral_w_scan.json", "w"), indent=1)
    print(f"\n{len(good)} solved | apparent crossing (w0 + wa < -1): {len(illusion)} | DESI-like "
          f"(-0.9 <= w0 <= -0.7, wa <= -0.4): {len(desi_like)}")


def w_chi_eff_fit(sol, V0, kap, lam):
    """Toomey et al. eq. 11: w_chi,eff = (chi'^2 - 2V(chi) + (f-1) phi'^2) / (chi'^2 + 2V(chi) + (f-1) phi'^2), with
    V(chi) = V0 e^(-kap chi) and dots = H d/dN; the angle is counted with matter. Fit w0 + wa (1 - a) on 0 < z < 2.5."""
    zs = np.linspace(0.0, 2.5, 100)
    ws = []
    for z in zs:
        N = -math.log(1 + z)
        c, cp, t, tp = sol.sol(N)
        e = math.exp(lam * c)
        rm, rr = 3 * OM * math.exp(-3 * N), 3 * ORAD * math.exp(-4 * N)
        # H^2 from the full Friedmann equation needs the angle's potential too; reuse the closure-consistent form
        Vt = 0.0
        H2 = None
        ws.append((c, cp, tp, e, N))
    out = []
    for (c, cp, tp, e, N), z in zip(ws, zs):
        H2 = H2_cache(sol, N, V0, kap, lam)
        cd2, td2 = H2 * cp * cp, H2 * tp * tp
        Vc = V0 * math.exp(-kap * c)
        out.append((cd2 - 2 * Vc + (e - 1) * td2) / (cd2 + 2 * Vc + (e - 1) * td2))
    a = 1 / (1 + zs)
    A = np.vstack([np.ones_like(a), 1 - a]).T
    (w0, wa), *_ = np.linalg.lstsq(A, np.array(out), rcond=None)
    return {"w0_eff": float(w0), "wa_eff": float(wa), "w_eff_z0": float(out[0]), "w_eff_z1": float(out[40])}


_H2C = {}


def H2_cache(sol, N, V0, kap, lam):
    return H2_of(sol, _H2C["V"], N, lam)[0]


def benchmark():
    """Mirror against Toomey et al. (arXiv:2511.23463) Fig. 1 benchmark: lambda = -1.25, alpha (our kap) = 1.7,
    log10 m/eV = -31.8, log10 f/eV = 26.3, theta_i = 3.12 (theta/f). H0 = 1.44e-33 eV (h = 0.68), reduced M_Pl
    = 2.435e27 eV. Then the same with our lambda = -2 sqrt(2/3). Their chi_i is tiny (we use 0)."""
    m = 10 ** -31.8 / 1.44e-33
    f = 10 ** 26.3 / 2.435e27
    out = {}
    for label, lam in (("toomey_benchmark", -1.25), ("our_lambda", LAM)):
        for kap in (1.7, 5.3):
            try:
                V0, sol, V = closed(kap, m, 3.12 * f, lam=lam, F=f, chi0=1e-4)
                fit = cpl_fit(sol, V, lam)
                _H2C["V"] = V
                out[f"{label}_kap{kap}"] = {**fit, **w_chi_eff_fit(sol, V0, kap, lam),
                                            "w_true": w_true(sol, V, lam), "V0": V0}
            except Exception as ex:
                out[f"{label}_kap{kap}"] = {"error": str(ex)[:100]}
    out["inputs"] = {"m_over_H0": m, "f_over_MPl": f}
    json.dump(out, open("spiral_w_benchmark.json", "w"), indent=1)
    print(json.dumps(out, indent=1))


def mirror_scan():
    """Q2: scan the inputs Toomey et al. do not state (angle mass m, starting angle, dilaton steepness kap, lambda)
    for their reported effective behaviour: w_chi,eff above -1 today and below -1 in the past, with
    (w0_eff, wa_eff) inside their CMB+DESI 1-sigma box (-0.50 +- 0.21, -1.51 +- 0.60). f fixed at their 0.082 M_Pl."""
    f = 10 ** 26.3 / 2.435e27
    rows = []
    for lam in (-1.25, LAM):
        for kap in (1.0, 1.7, 3.0):
            for m in (3.0, 5.0, 11.0, 30.0, 100.0):
                for th in (2.5, 3.0, 3.12, 3.14):
                    try:
                        V0, sol, V = closed(kap, m, th * f, lam=lam, F=f, chi0=1e-4)
                    except Exception:
                        continue
                    _H2C["V"] = V
                    e = w_chi_eff_fit(sol, V0, kap, lam)
                    hit = (abs(e["w0_eff"] + 0.50) <= 0.21 and abs(e["wa_eff"] + 1.51) <= 0.60
                           and e["w_eff_z0"] > -1 and e["w_eff_z1"] < -1)
                    rows.append({"lam": lam, "kap": kap, "m": m, "theta_over_f": th, **e, "match": hit})
                    print(f"lam {lam:+.3f} kap {kap} m {m:5.1f} th {th} | w0_eff {e['w0_eff']:+.3f} "
                          f"wa_eff {e['wa_eff']:+.3f} w(0) {e['w_eff_z0']:+.3f} w(1) {e['w_eff_z1']:+.3f} "
                          f"{'MATCH' if hit else ''}", flush=True)
    json.dump({"rows": rows, "n_match": sum(r["match"] for r in rows)}, open("spiral_mirror_scan.json", "w"), indent=1)
    print("matches:", sum(r["match"] for r in rows), "of", len(rows))


def matter_angle():
    """Matter-like-angle route: the angle oscillates (m >> H0) and acts as a fraction f of the matter; through e^(lam chi)
    its effective mass depends on the dilaton (coupled dark matter, d ln m_eff/d chi = -lam/2 = 0.816). True baryon+CDM
    density is lowered so that total matter stays 0.30. A CPL fit (free Om, w0, wa) then shows what a w0-wa analysis
    would read. Exploratory, not a pre-registered test."""
    global OM
    rows = []
    grid = json.loads(os.environ.get("MA_GRID", "null")) or [[0.5, 1.0, 1.5], [100.0, 300.0], [0.003, 0.01, 0.03, 0.06, 0.1]]
    out_name = os.environ.get("MA_OUT", "spiral_matter_angle.json")
    for kap in grid[0]:
        for m in grid[1]:
            for th in grid[2]:
                OM = 0.30
                try:
                    for _ in range(3):           # iterate so that true matter + angle (matter-like) = 0.30 today
                        V0, sol, V = closed(kap, m, th, F=FDEC)
                        c, cp, t, tp = sol.sol(0.0)
                        H2 = H2_of(sol, V, 0.0)[0]
                        rho_ang = 0.5 * math.exp(LAM * c) * H2 * tp * tp + m * m * FDEC ** 2 * (1 - math.cos(t / FDEC))
                        f = rho_ang / (rho_ang + 3 * OM)
                        OM = 0.30 * (1 - f)
                    fit = cpl_fit(sol, V)
                except Exception as ex:
                    rows.append({"kap": kap, "m": m, "theta_i": th, "error": str(ex)[:80]})
                    OM = 0.30
                    continue
                r = {"kap": kap, "m": m, "theta_i": th, "angle_fraction_of_matter": f, "Om_true": OM, **fit,
                     "beta_eff": f * (-LAM / 2)}
                rows.append(r)
                print(f"kap {kap} m {m:5.0f} th {th:5.3f} | angle {f:6.3f} of matter, beta_eff {r['beta_eff']:.3f} | "
                      f"Om_eff {fit['Om_eff']:.3f} w0 {fit['w0']:+.3f} wa {fit['wa']:+.3f} resid {fit['max_rel_resid']:.1e}",
                      flush=True)
    OM = 0.30
    good = [r for r in rows if "w0" in r and r["max_rel_resid"] < 0.01]
    desi = [r for r in good if -0.9 <= r["w0"] <= -0.7 and r["wa"] <= -0.4]
    allowed = [r for r in desi if r["beta_eff"] <= 0.073]
    json.dump({"rows": rows, "n_desi_like": len(desi), "n_desi_like_and_coupling_allowed": len(allowed)},
              open(out_name, "w"), indent=1)
    print(f"\nclean fits {len(good)} | DESI-like {len(desi)} | DESI-like with beta_eff <= 0.073 {len(allowed)}")


def coupled_exp_w(kap, beta, om_b, om_c, orad, zs):
    """Exponential dilaton (V0 e^(-kap chi)) + CDM coupled as in the AxiCLASS coupled build:
    rho_cdm = rho_c,unc a^-3 e^(beta (chi - chi_i)); force on chi = -beta rho_cdm. V0 tuned so H(0) = 1 (units H0).
    Returns w_scf(z) and E(z) = H/H0 on zs (for the CLASS mirror)."""
    from scipy.integrate import solve_ivp as ivp

    def run(V0):
        def rhs(N, y):
            c, cp = y
            rb, rc = 3 * om_b * math.exp(-3 * N), 3 * om_c * math.exp(-3 * N) * math.exp(beta * c)
            rr = 3 * orad * math.exp(-4 * N)
            V = V0 * math.exp(-kap * c)
            H2 = (rb + rc + rr + V) / (3 - 0.5 * cp * cp)
            eps = (rb + rc + 4 * rr / 3 + H2 * cp * cp) / (2 * H2)
            return [cp, -(3 - eps) * cp + (kap * V - beta * rc) / H2]
        return ivp(rhs, (N0, 0.0), [0.0, 0.0], method="LSODA", rtol=1e-10, atol=1e-12, dense_output=True), rhs

    def h2(sol, N, V0):
        c, cp = sol.sol(N)
        rb, rc = 3 * om_b * math.exp(-3 * N), 3 * om_c * math.exp(-3 * N) * math.exp(beta * c)
        rr = 3 * orad * math.exp(-4 * N)
        V = V0 * math.exp(-kap * c)
        H2 = (rb + rc + rr + V) / (3 - 0.5 * cp * cp)
        return H2, (0.5 * H2 * cp * cp - V) / (0.5 * H2 * cp * cp + V)

    V0 = brentq(lambda v: h2(run(v)[0], 0.0, v)[0] - 1, 1e-4, 50, xtol=1e-12)
    sol, _ = run(V0)
    out = [h2(sol, -math.log(1 + z), V0) for z in zs]
    coupled_exp_w.last_V0 = V0
    return [math.sqrt(o[0]) for o in out], [o[1] for o in out]


def class_mu1_guess(kap, beta, om_b, om_c, orad, h):
    """Shooting guess for AxiCLASS double_exp (V = mu1^4 e^(-kap phi), phi_ini = kap): from this solver's closure V0
    (units H0^2, field starting at 0): mu1^4 e^(-kap^2) = V0 H0^2 with H0 = h/2997.92458 Mpc^-1."""
    coupled_exp_w(kap, beta, om_b, om_c, orad, [0.0])
    H0 = h / 2997.92458
    return (coupled_exp_w.last_V0 * H0 * H0 * math.exp(kap * kap)) ** 0.25


def mirror_ramos():
    """Q2 alternative mirror: Ramos-Hamud, Garcia-Arroyo, Quevedo & Vazquez (arXiv:2609.22539), EXP case (n = 0):
    metric dphi1^2 + W^2 dphi2^2 with W = e^(-xi phi1), V = V0 e^(-lam_p phi1), no axion potential. Their autonomous
    system (eqs. 15a-d, Omega_b -> 0 in the far future) has a late-time attractor fixed by (lam_p, xi) alone. Our solver
    with kap = lam_p, lam = -2 xi, m = 0, run far into the future, must land on the same attractor (w and Omega split)."""
    from scipy.integrate import solve_ivp as ivp
    out = {}
    for lam_p, xi in ((2.0, 10.0), (2.0, 100.0), (8.0, 20.0)):
        # their system, Omega_b = 0 (scalar-dominated future), alpha = lam_p constant
        def f(N, s):
            x1, x2, y = s
            Pi = 2 * x1 * x1 + 2 * x2 * x2 + 1.0 * (1 - x1 * x1 - x2 * x2 - y * y)   # gamma = 1 (matter)
            return [-3 * x1 + 1.5 * Pi * x1 + math.sqrt(1.5) * (lam_p * y * y - 2 * xi * x2 * x2),
                    -3 * x2 + 1.5 * Pi * x2 + math.sqrt(6) * xi * x1 * x2,
                    1.5 * Pi * y - math.sqrt(1.5) * lam_p * x1 * y]
        s = ivp(f, (0, 200), [1e-3, 1e-3, 0.1], rtol=1e-10, atol=1e-12).y[:, -1]
        x1, x2, y = s
        w_theirs = (x1 * x1 + x2 * x2 - y * y) / (x1 * x1 + x2 * x2 + y * y)
        # ours: start with a small axion velocity so the mixing is active; run to N = +40 (matter negligible)
        sol, V = solve(1.0, lam_p, 0.0, 0.0, lam=-2 * xi, F=1.0, dense=True, tp0=1e-3, N1=40.0)
        c, cp, t, tp = sol.sol(40.0)
        e = math.exp(-2 * xi * c)
        H2, rho, p = H2_of(sol, V, 40.0, lam=-2 * xi)
        kin1, kin2 = H2 * cp * cp / 2, H2 * e * tp * tp / 2
        w_ours = p / rho
        out[f"lam{lam_p}_xi{xi}"] = {"theirs": {"x1": x1, "x2": x2, "y": y, "w": w_theirs,
                                                "x2_share": x2 * x2 / (x1 * x1 + x2 * x2 + y * y)},
                                     "ours": {"w": w_ours, "x2_share": kin2 / rho, "x1_share": kin1 / rho},
                                     "dw": w_ours - w_theirs}
    ok = all(abs(v["dw"]) < 1e-3 and abs(v["ours"]["x2_share"] - v["theirs"]["x2_share"]) < 1e-3 for v in out.values())
    out["MIRROR"] = "PASS" if ok else "FAIL"
    json.dump(out, open("spiral_mirror_ramos.json", "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    {"validate": validate, "scan": scan, "benchmark": benchmark, "mirror": mirror_scan,
     "mirror_ramos": mirror_ramos, "matter_angle": matter_angle}[sys.argv[1]]()
