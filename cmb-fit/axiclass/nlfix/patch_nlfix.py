# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights.
"""B0 halofit fix (CubeMind PREREGISTRATION_SPT3G_DEVIATIONS.md, 14:34:07; LATE_TWIST_NULL_MIRROR.md).
background.c counts a scalar field as (rho - 3p) of matter and 3p of radiation. Halofit and HMcode read that Omega_m, so
a field acting as late dark energy (p = -rho) appears as +4 Omega_scf of matter. This patch takes the field back out of
Omega_m and Omega_r in the non-linear modules and gives halofit the effective w of the dark energy (field + Lambda).
Nothing else in CLASS changes. Exact-anchor edits; each must match once.
Usage: python patch_nlfix.py /home/syndyr/AxiCLASS_nlfix"""
import os
import sys

ROOT = sys.argv[1]

SCF_OUT = ("if (pba->has_scf == _TRUE_) {{ /* nl-scf-fix: treat the scalar field as dark energy, not rho-3p matter */\n"
           "{i}  Omega_m -= (pvecback[pba->index_bg_rho_scf]-3.*pvecback[pba->index_bg_p_scf])/pvecback[pba->index_bg_rho_crit];\n"
           "{i}  Omega_v = 1.-Omega_m-(pvecback[pba->index_bg_Omega_r]-3.*pvecback[pba->index_bg_p_scf]/pvecback[pba->index_bg_rho_crit]);\n"
           "{i}}}\n")
W_EFF = ("{i}if (pba->has_scf == _TRUE_ && pba->has_fld == _FALSE_) {{ /* nl-scf-fix: effective w of field + Lambda */\n"
         "{i}  double rho_de = pvecback[pba->index_bg_rho_scf], p_de = pvecback[pba->index_bg_p_scf];\n"
         "{i}  if (pba->has_lambda == _TRUE_) {{ rho_de += pvecback[pba->index_bg_rho_lambda]; p_de -= pvecback[pba->index_bg_rho_lambda]; }}\n"
         "{i}  if (rho_de > 0.) w = p_de/rho_de;\n"
         "{i}}}\n")

EDITS = [
    ("external/Halofit/halofit.c",
     "    Omega_v = 1.-pvecback[pba->index_bg_Omega_m]-pvecback[pba->index_bg_Omega_r];\n"
     "    /* until v2.9.3",
     "    Omega_v = 1.-pvecback[pba->index_bg_Omega_m]-pvecback[pba->index_bg_Omega_r];\n"
     "    " + SCF_OUT.format(i="    ") + "    /* until v2.9.3"),
    ("external/Halofit/halofit.c",
     "    class_call(background_w_fld(pba,pvecback[pba->index_bg_a],&w,&dw_over_da_fld,&integral_fld), pba->error_message, pfo->error_message);\n",
     "    class_call(background_w_fld(pba,pvecback[pba->index_bg_a],&w,&dw_over_da_fld,&integral_fld), pba->error_message, pfo->error_message);\n"
     + W_EFF.format(i="    ")),
    ("external/Halofit/halofit.c",
     "  Omega_v = 1.-pvecback[pba->index_bg_Omega_m]-pvecback[pba->index_bg_Omega_r];\n\n  // for debugging:",
     "  Omega_v = 1.-pvecback[pba->index_bg_Omega_m]-pvecback[pba->index_bg_Omega_r];\n"
     "  " + SCF_OUT.format(i="  ") + "\n  // for debugging:"),
    ("external/HMcode/hmcode.c",
     "  Omega_m = pvecback[pba->index_bg_Omega_m];//TBC",
     "  Omega_m = pvecback[pba->index_bg_Omega_m];\n"
     "  if (pba->has_scf == _TRUE_) /* nl-scf-fix: the scalar field is dark energy, not rho-3p matter */\n"
     "    Omega_m -= (pvecback[pba->index_bg_rho_scf]-3.*pvecback[pba->index_bg_p_scf])/pvecback[pba->index_bg_rho_crit];//TBC"),
    # Addendum 14:41:32: the real cause. n_axion = 1 forced the field into delta_m (right for axion dark matter, wrong for
    # axion dark energy). The user's include_scf_in_delta_m setting (default no) now decides.
    ("source/input.c",
     "         if(pba->n_axion==1){\n           ppt->include_scf_in_delta_m = _TRUE_;\n         }",
     "         /* nl-scf-fix: n_axion = 1 no longer forces include_scf_in_delta_m (axion dark energy must not dilute\n"
     "            delta_m); set include_scf_in_delta_m = yes for axion dark matter. */"),
]

for rel, old, new in EDITS:
    p = os.path.join(ROOT, rel)
    t = open(p, encoding="utf-8").read()
    if new in t:
        print("already patched", rel)
        continue
    n = t.count(old)
    assert n == 1, f"{rel}: anchor found {n} times:\n{old}"
    open(p, "w", encoding="utf-8").write(t.replace(old, new))
    print("patched", rel)
