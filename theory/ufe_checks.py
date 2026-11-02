"""UFE checks (PREREGISTRATION_UFE_CHECKS.md, locked 2026-11-02 15:50:03): ER early role, LQ LQG value, IN inflation.
    python ufe_checks.py er                 -> ufe_er.json (local; numpy/scipy)
    python ufe_checks.py in                 -> ufe_in.json (local)
    python ufe_checks.py lq_eval <run>      -> ufe_lq_<run>.json (WSL env 'aegis'; reads CLASS phi_scf at z = 0)
    python ufe_checks.py lq                 -> ufe_lq.json (local; scores the two Late Twist fits)
Reduced Planck units. Reading A: ln A = |phi| - (1/2) ln|phi| + const, |phi| = exp(sqrt(2/3) chi), GR point |phi| = 1/2."""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.environ.get("TWIST_RESULTS", r"C:\Users\Danny\.copilot\repos\AEGIS\cmb-fit\results")
S23 = math.sqrt(2 / 3)
LT_FITS = ("ax_spa_latetwist_gF0.4m-0.3_nlfix", "ax_spa_latetwist_gF0m0.102_desy5_nlfix")


def lnA(chi):
    p = math.exp(S23 * chi)
    return p - 0.5 * math.log(p)


def beta(chi):
    return S23 * (math.exp(S23 * chi) - 0.5)


def er():
    from scipy.integrate import solve_ivp
    m = json.load(open(os.path.join(RES, "cmp_ax_spa_lcdm_halofit.json")))["minimum"]
    h = m["H0"] / 100
    om = m["Omega_m"]
    orad = 2.473e-5 * (1 + 0.22711 * 3.044) / h ** 2
    ol = 1 - om - orad
    chi_gr = math.log(0.5) / S23
    N0, N1 = -math.log(1 + 1e8), 0.0

    def rhs(N, y):
        chi, x = y
        rm = 3 * om * math.exp(-3 * N) * math.exp(lnA(chi) - lnA(chi_gr))
        rr = 3 * orad * math.exp(-4 * N)
        rl = 3 * ol
        H2 = (rm + rr + rl) / (3 * (1 - x * x / 6))
        eps = (rm + 4 * rr / 3 + H2 * x * x) / (2 * H2)
        return [x, -(3 - eps) * x - beta(chi) * rm / H2]

    zq = {"3500": 3500.0, "500": 500.0, "0": 0.0}
    rows = []
    for p0 in np.logspace(math.log10(0.05), math.log10(5), 100):
        chi0 = math.log(p0) / S23
        Nq = sorted(-math.log(1 + z) for z in zq.values())
        sol = solve_ivp(rhs, (N0, N1), [chi0, 0.0], method="LSODA", rtol=1e-9, atol=1e-12, dense_output=True)
        if not sol.success:
            rows.append({"phi_i": p0, "ok": False})
            continue
        Ngrid = np.linspace(N0, N1, 4000)
        xs = sol.sol(Ngrid)[1]
        om_chi = xs ** 2 / 6
        at = {k: float(sol.sol(-math.log(1 + z))[1] ** 2 / 6) for k, z in zq.items()}
        chi_today = float(sol.sol(0.0)[0])
        g_bbn = math.exp(2 * (lnA(chi0) - lnA(chi_today))) - 1
        ipk = int(np.argmax(om_chi))
        rows.append({"phi_i": float(p0), "ok": True, "Om_chi_3500": at["3500"], "Om_chi_500": at["500"],
                     "Om_chi_peak": float(om_chi[ipk]), "z_peak": float(math.exp(-Ngrid[ipk]) - 1),
                     "dchi_today": abs(chi_today - chi_gr), "dG_BBN": g_bbn})
    ok = [r for r in rows if r["ok"]]
    reach = [r for r in ok if 0.03 <= r["Om_chi_3500"] <= 0.12]
    viable = [r for r in reach if r["Om_chi_500"] <= 0.01 and r["dchi_today"] < 0.0072 and abs(r["dG_BBN"]) < 0.10]
    verdict = "VIABLE" if viable else "WRONG SHAPE" if reach else "TOO SMALL"
    best = max(ok, key=lambda r: r["Om_chi_3500"])
    out = {"verdict": verdict, "n_reach": len(reach), "n_viable": len(viable), "best_Om_chi_3500": best,
           "reach_examples": reach[:3], "cosmo": {"h": h, "Omega_m": om, "Omega_r": orad}, "rows": rows}
    json.dump(out, open(os.path.join(HERE, "ufe_er.json"), "w"), indent=1)
    print("ER:", verdict, "| reach", len(reach), "| viable", len(viable))
    print(" max Om_chi(3500) =", round(best["Om_chi_3500"], 5), "at phi_i =", round(best["phi_i"], 3),
          "| its Om_chi(500) =", round(best["Om_chi_500"], 5), "dchi_today =", best["dchi_today"],
          "dG_BBN =", round(best["dG_BBN"], 4))
    for r in reach[:3]:
        print(" reach:", {k: (round(v, 5) if isinstance(v, float) else v) for k, v in r.items()})


def inflation():
    ns_obs, sig, rmax = 0.974, 0.003, 0.036
    rows = {N: {"ns": 1 - 2 / N, "r": 12 / N ** 2, "pull": (ns_obs - (1 - 2 / N)) / sig} for N in (50, 55, 60)}
    p60 = rows[60]["pull"]
    verdict = ("CONSISTENT" if p60 <= 2 and rows[60]["r"] < rmax else "TENSION" if p60 <= 3 else "DISFAVOURED")
    n_for_2sigma = 2 / (1 - (ns_obs - 2 * sig))
    out = {"verdict": verdict, "by_N": rows, "N_for_pull_2": n_for_2sigma, "data": "n_s 0.974 +- 0.003; r < 0.036"}
    json.dump(out, open(os.path.join(HERE, "ufe_in.json"), "w"), indent=1)
    print("IN:", verdict, json.dumps(rows), "N for pull 2:", round(n_for_2sigma, 1))


def lq_eval(name):
    axi = os.environ.get("TWIST_AXI", "/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass")
    sys.path.insert(0, axi)
    import early_late_spa as E
    from cobaya.model import get_model
    E._maybe_coupled(name)
    info = E.make(name)
    for k in ("sampler", "output", "resume", "force"):
        info.pop(k, None)
    model = get_model(info)
    stored = json.load(open(f"{E.OUT}/cmp_{name}.json"))["minimum"]
    res = model.logposterior({p: stored[p] for p in model.parameterization.sampled_params()})
    bg = model.theory["classytwist"].classy.get_background()
    z = np.array(bg["z"])
    phi = np.array(bg["phi_scf"])
    i0 = int(np.argmin(z))
    out = {"name": name, "phi_today": float(phi[i0]), "phi_early": float(phi[int(np.argmax(z))]),
           "logpost": float(res.logpost), "logpost_stored": -float(stored["minuslogpost"]),
           "f_axion": None}
    json.dump(out, open(os.path.join(HERE, f"ufe_lq_{name}.json"), "w"), indent=1)
    print(out)


def lq():
    vals = (0.2375, 0.2740)
    rows = {}
    for n in LT_FITS:
        g = json.load(open(os.path.join(HERE, f"ufe_lq_{n}.json")))
        phi = abs(g["phi_today"])
        gam = math.sqrt(6) / (2 * phi) if phi > 0 else float("inf")
        rows[n] = {"phi_today": g["phi_today"], "gamma_today": gam,
                   "within10": [abs(gam / v - 1) <= 0.10 for v in vals],
                   "mirror": abs(g["logpost"] - g["logpost_stored"]) <= 0.05}
    both = [rows[LT_FITS[0]]["within10"][k] and rows[LT_FITS[1]]["within10"][k] for k in range(2)]
    anyone = any(any(r["within10"]) for r in rows.values())
    verdict = "MATCH" if any(both) else "PARTIAL" if anyone else "NO MATCH"
    if not all(r["mirror"] for r in rows.values()):
        verdict = "NO VERDICT (mirror)"
    out = {"verdict": verdict, "lqg_values": vals, "rows": rows}
    json.dump(out, open(os.path.join(HERE, "ufe_lq.json"), "w"), indent=1)
    print("LQ:", verdict, json.dumps(rows, indent=1))


if __name__ == "__main__":
    {"er": er, "in": inflation, "lq": lq, "lq_eval": lambda: lq_eval(sys.argv[2])}[sys.argv[1]]()
