# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under THE AEGIS PEOPLE'S LICENSE (see LICENSE in the AEGIS repository): free for people; no AI use; no military, surveillance or harmful use. AEGIS-ID: d097dd5fa73dce02
"""Predicted STACKED polarization around temperature hot spots (the radial/tangential ring pattern first seen by
WMAP, Komatsu et al. 2011, and confirmed by Planck), for the standard model and the Locked Twist best fits.
Q_r(theta) = - int l dl/(2 pi) W_l^2 C_l^TE J_2(l theta)   (unweighted-peak approximation, b_nu = 1, b_zeta = 0;
the ring positions are robust to that choice, the overall height is not). Beam: Gaussian FWHM 5 arcmin (Planck-like).
Q_r < 0 means polarization points radially (spokes); > 0 tangentially (rings)."""
import json, sys, numpy as np
from scipy.special import jv
sys.path.insert(0, "/home/claude/cmbwork/AxiCLASS/python"); sys.path.insert(0, "/home/claude/cmbwork")
from classy import Class
import cmb_cloud as C

def te(ckpt, ede):
    b = json.load(open(ckpt))["best_params"]
    p = {"A_s": 1e-10 * np.exp(b["logA"]), "n_s": b["n_s"], "H0": b["H0"], "omega_b": b["omega_b"],
         "omega_cdm": b["omega_cdm"], "tau_reio": b["tau_reio"], "m_ncdm": 0.06, "output": "tCl,pCl,lCl",
         "lensing": "yes", "l_max_scalars": 3000}
    p.update(C.EDE_ARGS if ede else C.LCDM_ARGS)
    if ede:
        lz = np.log10(2.4728e-5 * (1 + 0.22711 * 3.044) / (b["omega_b"] + b["omega_cdm"]))
        p.update(fraction_axion_ac=b["f_axion_ac"], log10_axion_ac=lz, scf_parameters=f"{b['scf_param_1']}, 0.")
    M = Class(); M.set(p); M.compute(); cl = M.lensed_cl(2500); M.struct_cleanup()
    return cl["ell"][2:], cl["te"][2:] * (2.7255e6) ** 2

th = np.radians(np.linspace(0.01, 3.0, 600))
sig = np.radians(5 / 60) / np.sqrt(8 * np.log(2))
out = {"theta_deg": np.degrees(th).tolist()}
for key, ck, ede in (("lcdm", "results/lcdm_noshoes_polish.ckpt.json", False), ("zeq", "results/ede_noshoes_zeq.ckpt.json", True)):
    l, cte = te(ck, ede)
    W2 = np.exp(-l * (l + 1) * sig ** 2)
    Q = np.array([-np.trapezoid(l / (2 * np.pi) * W2 * cte * jv(2, l * t), l) for t in th])
    zero = [float(np.degrees(th[i])) for i in range(len(th) - 1) if Q[i] * Q[i + 1] < 0]
    ext = [float(np.degrees(th[i])) for i in range(1, len(th) - 1) if abs(Q[i]) > abs(Q[i - 1]) and abs(Q[i]) > abs(Q[i + 1])]
    out[key] = {"Qr": Q.tolist(), "zero_crossings_deg": zero[:6], "extrema_deg": ext[:6]}
    print(key, "zero crossings (deg):", [round(z, 3) for z in zero[:6]], " extrema:", [round(e, 3) for e in ext[:6]], flush=True)
a, b = np.array(out["lcdm"]["Qr"]), np.array(out["zeq"]["Qr"])
print("largest difference (Twist - standard) as % of the biggest swing:", round(100 * np.max(abs(b - a)) / np.max(abs(a)), 2))
json.dump(out, open("/home/claude/cmbwork/acoustic/stack_predict.json", "w"))
