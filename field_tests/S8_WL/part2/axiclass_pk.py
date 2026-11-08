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
import early_late_spa as E  # noqa: E402

G = np.load(os.path.join(HERE, "pk_grids.npz"))
C_KMS = 299792.458


def one(name):
    from cobaya.likelihood import Likelihood
    from cobaya.model import get_model
    E._maybe_coupled(name)
    info = copy.deepcopy(E.make(name))
    for k in ("sampler", "output", "resume", "force"):
        info.pop(k, None)
    zpk, zbg = G["z_pk"], G["z_bg"]
    kmax = float(G["k_h"].max())

    class Need(Likelihood):
        def get_requirements(self):
            return {"Pk_grid": {"z": list(zpk), "k_max": 50.0, "nonlinear": (False, True)},
                    "comoving_radial_distance": {"z": list(zbg)}, "Hubble": {"z": list(zbg)},
                    "fsigma8": {"z": list(G["z_growth"])}, "sigma8_z": {"z": list(G["z_growth"])}}

        def logp(self, **kw):
            return 0.0

    info["likelihood"] = {"need": {"external": Need}}
    m = get_model(info)
    best = json.load(open(os.path.join(E.OUT, f"cmp_{name}.json")))["minimum"]
    sp = m.parameterization.sampled_params()
    m.logposterior({k: best[k] for k in sp})
    pv = m.provider
    h = best["H0"] / 100
    out = {"h0": h, "omega_m": (best["omega_b"] + best["omega_cdm"] + 0.06 / 93.14) / h ** 2}
    for nl, tag in ((False, "lin"), (True, "nl")):
        k, z, P = pv.get_Pk_grid(nonlinear=nl)                       # k in 1/Mpc, P in Mpc^3, P[z, k]
        logP = np.array([np.interp(np.log(G["k_h"] * h), np.log(k), np.log(P[i])) for i in range(len(z))])
        out[f"p_k_{tag}"] = np.array([np.interp(zpk, z, logP[:, j]) for j in range(logP.shape[1])]).T
        out[f"p_k_{tag}"] = np.exp(out[f"p_k_{tag}"]) * h ** 3              # (Mpc/h)^3 on (z_pk, k_h)
    out["d_m"] = np.asarray(pv.get_comoving_radial_distance(zbg))
    out["h"] = np.asarray(pv.get_Hubble(zbg)) / C_KMS                     # 1/Mpc
    s8 = np.asarray(pv.get_sigma8_z(G["z_growth"]))
    out["sigma_8"] = s8
    out["f_z"] = np.asarray(pv.get_fsigma8(G["z_growth"])) / s8
    out["d_z"] = s8 / s8[0]
    np.savez(os.path.join(HERE, "..", "results", f"pk_{name}.npz"), z_pk=zpk, k_h=G["k_h"], z_bg=zbg,
             z_growth=G["z_growth"], **out)
    print("wrote", name, "sigma8", s8[0], "omega_m", out["omega_m"], flush=True)


if __name__ == "__main__":
    for n in sys.argv[1:]:
        one(n)
