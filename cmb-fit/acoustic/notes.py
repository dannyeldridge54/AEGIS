# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under THE AEGIS PEOPLE'S LICENSE (see LICENSE in the AEGIS repository): free for people; no AI use; no military, surveillance or harmful use. AEGIS-ID: 273ace4d128c1bfc
"""The universe's sound waves (acoustic peaks) for the standard model and the Twist best fits.
Outputs acoustic/notes.json: TT/EE spectra (lensed), peak and trough multipoles, 100*theta_s, r_s, z_*, and
the 'spacing' between peaks. Uses the same AxiCLASS build and settings as the fits."""
import json, os, sys, numpy as np
sys.path.insert(0, "/home/claude/cmbwork/AxiCLASS/python"); sys.path.insert(0, "/home/claude/cmbwork")
from classy import Class
import cmb_cloud as C

def run(ckpt, ede):
    b = json.load(open(ckpt))["best_params"]
    p = {"A_s": 1e-10 * np.exp(b["logA"]), "n_s": b["n_s"], "H0": b["H0"], "omega_b": b["omega_b"],
         "omega_cdm": b["omega_cdm"], "tau_reio": b["tau_reio"], "m_ncdm": 0.06,
         "output": "tCl,pCl,lCl", "lensing": "yes", "l_max_scalars": 3000}
    p.update(C.EDE_ARGS if ede else C.LCDM_ARGS)
    if ede:
        lz = b.get("log10_axion_ac")
        if lz is None:  # locked: equality
            lz = np.log10(2.4728e-5 * (1 + 0.22711 * 3.044) / (b["omega_b"] + b["omega_cdm"]))
        p.update(fraction_axion_ac=b["f_axion_ac"], log10_axion_ac=lz, scf_parameters=f"{b['scf_param_1']}, 0.")
    M = Class(); M.set(p); M.compute()
    cl = M.lensed_cl(2500); ell = cl["ell"][2:]; T = 2.7255e6
    D = ell * (ell + 1) / (2 * np.pi) * T**2
    tt, ee = D * cl["tt"][2:], D * cl["ee"][2:]
    der = M.get_current_derived_parameters(["100*theta_s", "rs_rec", "z_rec", "ra_rec", "rs_d"]) if hasattr(M, "get_current_derived_parameters") else {}
    def peaks(y, sign=1, lo=100):
        s = sign * y; out = []
        for i in range(lo, len(s) - 30):
            if s[i] == max(s[max(0, i - 30):i + 31]): out.append(int(ell[i]))
        return out
    res = {"ell": ell.tolist(), "tt": tt.tolist(), "ee": ee.tolist(), "derived": der,
           "tt_peaks": peaks(tt)[:7], "tt_troughs": peaks(tt, -1)[:7], "H0": b["H0"]}
    M.struct_cleanup(); return res

out = {"lcdm": run("results/lcdm_noshoes_polish.ckpt.json", False),
       "ede": run("results/ede_noshoes_polish.ckpt.json", True)}
z = "results/ede_noshoes_zeq.ckpt.json"
if os.path.exists(z): out["zeq"] = run(z, True)
json.dump(out, open("acoustic/notes.json", "w"))
for k, v in out.items():
    print(k, v["derived"], "peaks", v["tt_peaks"], "troughs", v["tt_troughs"])
