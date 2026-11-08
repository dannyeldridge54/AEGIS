"""Frozen forward predictions for the CURRENT model (Spiral, S8-J and S8-L fits), computed in the cloud with CLASS
called directly (same settings as each stored fit, as field_tests/S8_WL/part2/axiclass_pk.py). No data are compared.
Prep for validation step 1 (DESI DR3) and step 2 (Euclid/Rubin). Extends theory/forward_predictions.py, which needs the
PC likelihood packages.
    python forward_predictions_cloud.py <run> [<run> ...]   -> theory/fpc_<run>.json
Per run: BAO D_M/r_d, D_H/r_d, D_V/r_d on the DESI DR2 effective redshifts + a grid; r_d; H0; w(z) of the scalar field
on 0-3 and a CPL (w0, wa) fit on 0-2.5; min w; f*sigma8(z); sigma8 and S8 (s8wl_score convention); for coupled runs
the dark-matter coupling beta and the sign of the dark-matter mass change (from the scalar field's roll today)."""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "field_tests", "S8_WL", "part2"))
import axiclass_pk as AP  # noqa: E402  (candl stub, early_late_spa as AP.E, results path)

E = AP.E
ZB = [0.295, 0.51, 0.706, 0.934, 1.321, 1.484, 2.33, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.6, 2.0, 2.6, 3.0]
C_KMS = 299792.458


def args_for(name):
    ula = name.startswith("spiralL")
    if ula:
        sys.path.insert(0, os.path.join(AP.AX, "ula"))
        import spiral_l_fit
        info, _ = spiral_l_fit.make(name)
    else:
        make_name = name[:-5] if name.endswith("_s8y6") else name
        E._maybe_coupled(make_name)
        info = E.make(make_name)
    best = json.load(open(os.path.join(E.OUT, f"cmp_{name}.json")))["minimum"]
    a = dict(info["theory"]["classytwist"]["extra_args"])
    a.update({"A_s": 1e-10 * np.exp(best["logA"]), "n_s": best["n_s"], "100*theta_s": best["theta_s_1e2"],
              "omega_b": best["omega_b"], "omega_cdm": best["omega_cdm"], "tau_reio": best["tau_reio"]})
    for k in ("scf_coupling_beta", "omega_fld", "log10_a_c"):
        if k in best:
            a[k] = best[k]
    if "spiral_kappa" in best:
        import spiral_guess
        k = best["spiral_kappa"]
        mu = spiral_guess.mu1_guess(k, best.get("scf_coupling_beta", 0.0), best["omega_b"], best["omega_cdm"])
        a["scf_parameters"] = f"{k}, 0.0, {mu}, 0.0, 0.0, 0.0"
    a.pop("l_max_scalars", None)
    a.update({"output": "mPk", "z_max_pk": 3.1, "P_k_max_1/Mpc": 5.0})
    return a, best


def run(name):
    a, best = args_for(name)
    import classy
    c = classy.Class(); c.set(a); c.compute()
    h, rd = c.h(), c.rs_drag()
    bao = {}
    for z in ZB:
        dm = c.angular_distance(z) * (1 + z)
        dh = 1 / c.Hubble(z)
        bao[f"{z:g}"] = {"DM_rd": dm / rd, "DH_rd": dh / rd, "DV_rd": (z * dm * dm * dh) ** (1 / 3) / rd}
    bg = c.get_background()
    zz = np.array(bg["z"]); sel = zz <= 3.0
    out = {"run": name, "H0": 100 * h, "r_d": rd, "BAO": bao}
    if "(.)rho_scf" in bg:
        w = np.array(bg["(.)p_scf"])[sel] / np.array(bg["(.)rho_scf"])[sel]
        z = zz[sel]
        m = z <= 2.5
        A = np.vstack([np.ones(m.sum()), 1 - 1 / (1 + z[m])]).T
        w0, wa = np.linalg.lstsq(A, w[m], rcond=None)[0]
        out.update({"w0_cpl": w0, "wa_cpl": wa, "min_w": float(w.min())})
        if "(.)phi_scf" in bg and "scf_coupling_beta" in best:
            phi = np.array(bg["(.)phi_scf"])[sel]
            dphi_dz0 = (phi[-1] - phi[-2]) / (z[-1] - z[-2]) if z[-1] < z[-2] else (phi[1] - phi[0]) / (z[1] - z[0])
            out["beta"] = best["scf_coupling_beta"]
            out["dark_matter_mass_change_today"] = "grows" if best["scf_coupling_beta"] * (-dphi_dz0) > 0 else "shrinks"
            out["note_sign"] = "m_c ~ exp(beta*phi); sign read from dphi/dz at z~0 in the coupled build's convention (check)"
    s8z = {f"{z:g}": c.sigma(8 / h, z) * c.scale_independent_growth_factor_f(z) for z in (0.0, 0.3, 0.5, 0.7, 1.0, 1.5)}
    out["fsigma8"] = s8z
    wm = best["omega_b"] + best["omega_cdm"] + best.get("omega_fld", 0.0) + 0.06 / 93.14
    s8 = c.sigma(8 / h, 0.0)
    out.update({"sigma8": s8, "S8": s8 * math.sqrt(wm / h ** 2 / 0.3)})
    c.struct_cleanup()
    json.dump(out, open(os.path.join(HERE, f"fpc_{name}.json"), "w"), indent=1, default=float)
    print(name, "H0 %.2f rd %.2f w0 %s wa %s S8 %.4f" % (out["H0"], rd, out.get("w0_cpl"), out.get("wa_cpl"), out["S8"]),
          flush=True)


if __name__ == "__main__":
    for n in sys.argv[1:]:
        run(n)
