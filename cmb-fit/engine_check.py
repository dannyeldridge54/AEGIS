# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under THE AEGIS PEOPLE'S LICENSE (see LICENSE in the AEGIS repository): free for people; no AI use; no military, surveillance or harmful use. AEGIS-ID: 68edd77ee503adc8
"""Engine check: evaluate CAMB at the exact AxiCLASS best-fit points (ΛCDM and free EDE), same data, H0 fixed
instead of theta_*. If CAMB gives the same chi2 there, the engines agree and the gap is in the optimizers;
if not, the gap is in the physics/precision of the two EDE codes.

  python engine_check.py        writes results/engine_check.json and prints the per-likelihood table
"""
import copy, json, os
import cmbfit as C
import numpy as np
from cmbfit_compare import LOCK

AX = os.path.join(C.HERE, "axiclass", "results_live", "results")
MAP = {"logA": "logA", "n_s": "ns", "H0": "H0", "omega_b": "ombh2", "omega_cdm": "omch2", "tau_reio": "tau",
       "A_planck": "A_planck", "f_axion_ac": "fde_zc", "scf_param_1": "theta_i"}


def camb_at(ax_file, model, lock=False):
    from cobaya.model import get_model
    ax = json.load(open(os.path.join(AX, ax_file)))
    info = C.make_info(model)
    P = info["params"]
    for k in ("theta_s_100", "thetastar"):
        P.pop(k, None)
    P["H0"] = {"prior": {"min": 40, "max": 100}}
    P["thetastar"] = {"derived": True}
    point = {MAP[k]: v for k, v in ax["best_params"].items() if k in MAP}
    if model == "ede":
        point["log10_zc"] = ax["derived"]["log10_z_c"]      # AxiCLASS samples a_c; z_c is the same switch-on
    if lock:
        point["log10_zc"] = eval(LOCK)(point["ombh2"], point["omch2"])
    m = get_model(info)
    ll = m.loglikes(point, as_dict=True, return_derived=True)
    likes, der = ll
    chi = {k: -2 * v for k, v in likes.items()}
    dnames = list(m.parameterization.derived_params())
    dd = dict(zip(dnames, der)) if not isinstance(der, dict) else der
    return dict(point=point, camb_chi2=chi, camb_total=sum(chi.values()), ax_chi2=ax["chi2"],
                ax_total=ax["chi2_total"], camb_derived={k: dd.get(k) for k in ("rdrag", "sigma8", "omegam", "thetastar")},
                ax_derived={k: ax["derived"].get(k) for k in ("rs_drag", "sigma8", "Omega_m")})


if __name__ == "__main__":
    C.lower_priority()
    out = {"lcdm": camb_at("lcdm_noshoes_polish.ckpt.json", "lcdm"),
           "ede": camb_at("ede_noshoes_polish.ckpt.json", "ede"),
           "edelock": camb_at("ede_noshoes_polish.ckpt.json", "ede", lock=True)}
    json.dump(out, open(os.path.join(C.RESULTS, "engine_check.json"), "w"), indent=1, default=float)
    for n, r in out.items():
        print(f"\n{n}: CAMB total {r['camb_total']:.2f}  vs AxiCLASS {r['ax_total']:.2f}")
        for k, v in r["camb_chi2"].items():
            print(f"  {k:48s} CAMB {v:9.2f}  AxiCLASS {r['ax_chi2'].get(k, float('nan')):9.2f}")
        print("  derived CAMB", r["camb_derived"], " AxiCLASS", r["ax_derived"])
    print("\nΔχ² EDE−ΛCDM at the AxiCLASS points: CAMB "
          f"{out['ede']['camb_total'] - out['lcdm']['camb_total']:+.2f}, AxiCLASS {out['ede']['ax_total'] - out['lcdm']['ax_total']:+.2f}")
    best = {n: json.load(open(os.path.join(C.RESULTS, f"cmp_{n}.json")))["minimum"]["chi2"] for n in ("lcdm8", "ede8", "edelock8")}
    print(f"CAMB at the AxiCLASS EDE point vs CAMB's own best-of-8 ΛCDM: free {out['ede']['camb_total'] - best['lcdm8']:+.2f}, "
          f"locked {out['edelock']['camb_total'] - best['lcdm8']:+.2f} (CAMB's own minimizer found {best['ede8'] - best['lcdm8']:+.2f} / "
          f"{best['edelock8'] - best['lcdm8']:+.2f})")
