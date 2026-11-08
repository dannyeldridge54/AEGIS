"""S8-LNL (field_tests/rules/PREREG_S8L_NONLINEAR.md): replace the halofit nonlinear power in a stored Part 2 P(k) file
with axionHMcode (patched for HMcode-2020 BAO damping), same flags on both sides.
    TWIST_BUILDS=... TWIST_RESULTS=... AXHM=<axionHMcode_dw> python axhm_pk.py <run> [--gate]
Reads  ../results/pk_<run>.npz (linear power, grids, background: unchanged)
Writes ../results/pk_<run>_axhm.npz (same file, p_k_nl replaced) and axhm_<run>.json (gate G2, timings, settings).
<run> is spiralL{,_dovekie,_union3} (ULA share from the stored fit) or ax_spa_lcdm_halofit{,...} (no ULA)."""
import json
import math
import os
import sys
import time

import numpy as np
if not hasattr(np, "trapz"):
    np.trapz = np.trapezoid            # numpy 2 rename (execution only)

HERE = os.path.dirname(os.path.abspath(__file__))
RESD = os.path.join(HERE, "..", "results")
sys.path.insert(0, os.environ.get("AXHM", "/home/claude/builds/ext/axionHMcode_dw"))
sys.path.insert(0, HERE)
from axionCAMB_and_lin_PS import load_cosmology          # noqa: E402
from halo_model import HMcode_params, PS_nonlin_cold, PS_nonlin_axion   # noqa: E402
from axion_functions import axion_params                  # noqa: E402
from dewiggle import dewiggle_ratio                       # noqa: E402

FLAGS = dict(alpha=True, eta_given=True, one_halo_damping=True, two_halo_damping=True, concentration_param=True,
             full_2h=False)
NZ = 31                                    # rule: z grid 0-3, at least 30 points
H100_EV = 2.1332e-33
OGR, ONU = 4.18e-5, 0.06 / 93.14


def mass_ev(m):                            # as spiral_l_score.py
    a = 10 ** m["log10_a_c"]
    wm = m["omega_b"] + m["omega_cdm"] + m.get("omega_fld", 0.0) + ONU
    return 3 * H100_EV * math.sqrt(OGR / a ** 4 + wm / a ** 3)


def class_ratios(run, best, zs, kh):
    """ULA run: per-z transfer weights (d_i / d_tot)^2 from AxiCLASS at the stored point (same settings as Part 2)."""
    sys.path.insert(0, os.path.join(HERE, "..", "part2"))
    import axiclass_pk as AP
    E = AP.E
    sys.path.insert(0, os.path.join(AP.AX, "ula"))
    import spiral_l_fit
    info, _ = spiral_l_fit.make(run)
    import classy
    a = dict(info["theory"]["classytwist"]["extra_args"])
    a.update({"A_s": 1e-10 * np.exp(best["logA"]), "n_s": best["n_s"], "100*theta_s": best["theta_s_1e2"],
              "omega_b": best["omega_b"], "omega_cdm": best["omega_cdm"], "tau_reio": best["tau_reio"],
              "scf_coupling_beta": best["scf_coupling_beta"], "omega_fld": best["omega_fld"],
              "log10_a_c": best["log10_a_c"]})
    import spiral_guess
    k = best["spiral_kappa"]
    mu = spiral_guess.mu1_guess(k, best["scf_coupling_beta"], best["omega_b"], best["omega_cdm"])
    a["scf_parameters"] = f"{k}, 0.0, {mu}, 0.0, 0.0, 0.0"
    a.pop("l_max_scalars", None)
    a.update({"output": "mPk,mTk", "z_max_pk": float(max(zs)) + 0.05, "P_k_max_1/Mpc": 60.0})
    c = classy.Class(); c.set(a); c.compute()
    out, g2 = {}, 0.0
    wc, wb, wa, wn = best["omega_cdm"], best["omega_b"], best["omega_fld"], ONU
    h = c.h()
    for z in zs:
        t = c.get_transfer(z)
        kt = np.array(t["k (h/Mpc)"])
        dc, db, da, dn = (np.array(t[n]) for n in ("d_cdm", "d_b", "d_fld", "d_ncdm[0]"))
        # CLASS's matter P(k) in this build counts CDM + baryons + massive neutrinos, not the ULA (a "fluid"): see D2
        dcl = (wc * dc + wb * db + wn * dn) / (wc + wb + wn)
        dm = (wc * dc + wb * db + wa * da + wn * dn) / (wc + wb + wa + wn)      # true total matter, ULA included
        # G2: component sum x primordial spectrum vs CLASS's own linear matter power (= the stored file)
        sel = (kt >= 1e-3) & (kt <= 10)
        kM = kt[sel] * h
        pprim = best_As(best) * (kM / 0.05) ** (best["n_s"] - 1) * 2 * np.pi ** 2 / kM ** 3
        precon = pprim * dcl[sel] ** 2 * h ** 3
        pclass = np.array([c.pk_lin(x, z) for x in kM]) * h ** 3
        g2 = max(g2, float(np.max(np.abs(precon / pclass - 1))))
        cold = (wc * dc + wb * db) / (wc + wb)
        out[z] = {n: np.interp(np.log(kh), np.log(kt), (v / dcl) ** 2, left=(v / dcl)[0] ** 2, right=(v / dcl)[-1] ** 2)
                  for n, v in (("CDM", dc), ("baryon", db), ("cold", cold), ("axion", da), ("total", dm))}
    c.struct_cleanup()
    return out, g2


def best_As(best):
    return 1e-10 * math.exp(best["logA"])


def cosmo(best, h, z, fax, m_ax):
    f = os.path.join(HERE, f"_in_{os.getpid()}.txt")
    wd = best["omega_cdm"] + best.get("omega_fld", 0.0)
    open(f, "w").write("\n".join([f"omega_b_0 = {best['omega_b']}", f"omega_d_0 = {wd}", f"ax_fraction = {fax}",
                                  f"m_ax = {m_ax}", f"h = {h}", f"z = {z}", "M_min = 7", "M_max = 18",
                                  f"ns = {best['n_s']}", f"As = {1e-10 * math.exp(best['logA'])}", "k_piv = 0.05",
                                  "transfer_kmax = 100", "version = 'dome'"]) + "\n")
    c = load_cosmology.load_cosmology_input(f, LCDM=(fax == 0))
    os.remove(f)
    return c


def main(run, gate_only=False):
    t0 = time.time()
    best = json.load(open(os.path.join(os.environ["TWIST_RESULTS"], f"cmp_{run}.json")))["minimum"]
    src = dict(np.load(os.path.join(RESD, f"pk_{run}.npz")))
    kh, zp, plin = src["k_h"], src["z_pk"], src["p_k_lin"]
    h = float(src["h0"])
    ula = run.startswith("spiralL")
    fax = best["omega_fld"] / (best["omega_fld"] + best["omega_cdm"]) if ula else 0.0
    m_ax = mass_ev(best) if ula else 1e-25
    zs = list(np.linspace(0.0, float(zp.max()), NZ))
    ratios, g2 = class_ratios(run, best, zs, kh) if ula else ({}, 0.0)
    info = {"run": run, "rule": "PREREG_S8L_NONLINEAR.md", "flags": FLAGS, "ax_fraction": fax, "m_ax_eV": m_ax,
            "nz": NZ, "G2_max_dev_total_from_components": g2, "G2": "PASS" if g2 <= 0.005 else "FAIL"}
    print(run, "fax %.4f m %.3g G2 %.2e" % (fax, m_ax, g2), flush=True)
    if gate_only or info["G2"] == "FAIL":
        json.dump(info, open(os.path.join(HERE, f"axhm_{run}.json"), "w"), indent=1)
        return
    M = np.logspace(7, 18, 100)
    lnP = []
    for z in zs:
        pz = np.array([np.interp(z, zp, plin[:, j]) for j in range(len(kh))]) if z not in zp else plin[list(zp).index(z)]
        c = cosmo(best, h, z, fax, m_ax)
        if ula:
            r = ratios[z]
            psd = {"k": kh, "power_total": pz * r["total"], "power_CDM": pz * r["CDM"], "power_baryon": pz * r["baryon"],
                   "power_cold": pz * r["cold"], "power_axion": pz * r["axion"]}
            hp = HMcode_params.HMCode_param_dic(c, kh, psd["power_cold"])
            hp["dw"] = dewiggle_ratio(kh, psd["power_cold"], h, best["omega_b"] + best["omega_cdm"] + best["omega_fld"],
                                      best["omega_b"], best["n_s"])
            ap = axion_params.func_axion_param_dic(M, c, psd, hp, concentration_param=FLAGS["concentration_param"])
            nl = PS_nonlin_axion.func_full_halo_model_ax(M, psd, c, hp, ap, **FLAGS)[0]
        else:
            hp = HMcode_params.HMCode_param_dic(c, kh, pz)
            hp["dw"] = dewiggle_ratio(kh, pz, h, best["omega_b"] + best["omega_cdm"], best["omega_b"], best["n_s"])
            nl = PS_nonlin_cold.func_non_lin_PS_matter(M, kh, pz, c, hp, c["Omega_m_0"], **FLAGS)[0]
        lnP.append(np.log(nl))
        print(f"  z {z:.2f}  {time.time() - t0:.0f}s", flush=True)
    lnP = np.array(lnP)
    nlz = np.array([[np.interp(z, zs, lnP[:, j]) for j in range(len(kh))] for z in zp])
    src["p_k_nl"] = np.exp(nlz)
    np.savez(os.path.join(RESD, f"pk_{run}_axhm.npz"), **src)
    info["seconds"] = time.time() - t0
    json.dump(info, open(os.path.join(HERE, f"axhm_{run}.json"), "w"), indent=1, default=float)
    print("wrote", run, flush=True)


if __name__ == "__main__":
    main(sys.argv[1], "--gate" in sys.argv)
