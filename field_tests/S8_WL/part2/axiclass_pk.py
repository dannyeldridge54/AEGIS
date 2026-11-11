"""S8-WL Part 2, Spiral pairs: write the matter power spectrum, distances and growth of a stored AxiCLASS best fit
(coupled-dark-matter build for the Spiral) to a file that load_pk.py feeds to the DES Y3 pipeline. Runs in WSL on the PC
(the coupled AxiCLASS build lives there), with the SAME settings as the stored fit (early_late_spa.make):
    python axiclass_pk.py ax_spa_spiraltwist_nlfix ax_spa_lcdm_halofit [...]   -> ../results/pk_<run>.npz
Grids (z, k/h) are those of the CAMB runs (pk_grids.npz), so both kinds of model enter the pipeline identically."""
import copy
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
AX = os.path.join(HERE, "..", "..", "..", "cmb-fit", "axiclass")
sys.path.insert(0, AX)
try:                                       # the SPT likelihood package is only referenced by make(); the likelihoods
    import candl.interface  # noqa: F401   # are replaced below, so a stand-in is enough where it is not installed
    import spt_candl_data  # noqa: F401
except ImportError:
    import types
    for _n in ("candl", "candl.interface", "spt_candl_data"):
        sys.modules[_n] = types.SimpleNamespace(CandlCobayaLikelihood=None, SPT3G_D1_TnE=None, interface=None)
    sys.modules["candl"].interface = sys.modules["candl.interface"]
import early_late_spa as E  # noqa: E402

G = np.load(os.path.join(HERE, "pk_grids.npz"))
C_KMS = 299792.458


def one(name):
    """Same theory settings as the stored fit (early_late_spa.make, incl. the ClassyTwist parameter translation); CLASS is
    asked for P(k, z) up to z_max_pk (a z_pk list string is rejected by this build), then read directly.
    S8-J runs "<SF run>_s8y6" use their SF run's settings (the S8 term changes no theory setting); S8-L runs "spiralL*"
    use spiral_l_fit.make (ULA build, dark-matter split, log10_a_c from the stored point)."""
    ula = name.startswith(("spiralL", "S8A"))
    s8a = name.startswith("S8A")
    if s8a:                                    # S8-A (PREREG_LATE_BASE.md): angle-coupled build, angle in delta_m
        sys.path.insert(0, os.path.join(AX, "angle"))
        import angle_fit
        info, _ = angle_fit.make(name.split("__js")[0])      # JOINT-SHEAR design points: theory of the base run
    elif ula:
        sys.path.insert(0, os.path.join(AX, "ula"))
        import spiral_l_fit
        info, _ = spiral_l_fit.make(name)
    else:
        make_name = name.split("__js")[0].replace("_s8y6_more", "").replace("_s8y6", "")
        E._maybe_coupled(make_name)             # puts the run's own AxiCLASS build first on sys.path
        info = E.make(make_name)
    import classy
    zpk, zbg, zgr, kh = G["z_pk"], G["z_bg"], G["z_growth"], G["k_h"]
    best = json.load(open(os.path.join(E.OUT, f"cmp_{name}.json")))["minimum"]
    args = dict(info["theory"]["classytwist"]["extra_args"])
    # the stored point, translated exactly as Cobaya + ClassyTwist did during the fit
    args.update({"A_s": 1e-10 * np.exp(best["logA"]), "n_s": best["n_s"], "100*theta_s": best["theta_s_1e2"],
                 "omega_b": best["omega_b"], "omega_cdm": best["omega_cdm"], "tau_reio": best["tau_reio"]})
    if "scf_coupling_beta" in best:
        args["scf_coupling_beta"] = best["scf_coupling_beta"]
    if s8a:
        args["scf_coupling_beta"] = 0.0                       # CDM uncoupled; the angle coupling is in extra_args
    if ula:                                        # S8-L: omega_cdm, omega_fld, log10_a_c as stored (derived split)
        args.update({"omega_cdm": best["omega_cdm"], "omega_fld": best["omega_fld"], "log10_a_c": best["log10_a_c"]})
    kfix = info.get("params", {}).get("spiral_kappa")              # FLAG-1: kappa fixed (not in "minimum")
    kfix = kfix.get("value") if isinstance(kfix, dict) else kfix
    if "spiral_kappa" in best or isinstance(kfix, (int, float)):
        import spiral_guess
        k = best.get("spiral_kappa", kfix)
        mu = spiral_guess.mu1_guess(k, best.get("scf_coupling_beta", best.get("beta_eff", 0.0)), best["omega_b"],
                                    best["omega_cdm"])
        args["scf_parameters"] = f"{k}, 0.0, {mu}, 0.0, 0.0, 0.0"
    args.pop("l_max_scalars", None)                # CMB-only setting; unread without CMB output
    args.update({"output": "mPk", "z_max_pk": float(zpk.max()) + 0.05, "P_k_max_1/Mpc": 60.0})
    c = classy.Class()
    c.set(args)
    c.compute()
    h = c.h()
    kmax = 50.0                                                   # 1/Mpc, computed range; beyond: log-log extrapolation
    out = {"h0": h, "omega_m": (best["omega_b"] + best["omega_cdm"] + best.get("omega_fld", 0.0) + 0.06 / 93.14) / h ** 2}
    kM = kh * h

    def pk_row(fun, z):
        inside = kM <= kmax
        v = np.array([fun(k, z) for k in kM[inside]])
        lk, lv = np.log(kM[inside]), np.log(v)
        slope = (lv[-1] - lv[-6]) / (lk[-1] - lk[-6])
        ext = lv[-1] + slope * (np.log(kM[~inside]) - lk[-1])
        return np.exp(np.concatenate([lv, ext])) * h ** 3            # (Mpc/h)^3
    out["p_k_lin"] = np.array([pk_row(c.pk_lin, z) for z in zpk])
    out["p_k_nl"] = np.array([pk_row(c.pk, z) for z in zpk])
    out["d_m"] = np.array([c.angular_distance(z) * (1 + z) for z in zbg])
    out["h"] = np.array([c.Hubble(z) for z in zbg])               # 1/Mpc
    out["sigma_8"] = np.array([c.sigma(8 / h, z) for z in zgr])
    out["d_z"] = np.array([c.scale_independent_growth_factor(z) for z in zgr])
    out["d_z"] = out["d_z"] / out["d_z"][0]
    out["f_z"] = np.array([c.scale_independent_growth_factor_f(z) for z in zgr])
    np.savez(os.path.join(HERE, "..", "results", f"pk_{name}.npz"), z_pk=zpk, k_h=kh, z_bg=zbg, z_growth=zgr, **out)
    print("wrote", name, "sigma8", out["sigma_8"][0], "stored", best.get("sigma8"), "omega_m", out["omega_m"], flush=True)


if __name__ == "__main__":
    for n in sys.argv[1:]:
        one(n)
