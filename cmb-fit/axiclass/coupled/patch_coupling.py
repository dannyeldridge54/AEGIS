# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights.
"""Add a conformal scalar-field -> CDM coupling to a COPY of AxiCLASS (CubeMind PREREGISTRATION_COUPLED_TWIST.md).

    m_cdm(phi) = m0 exp(beta phi / M_Pl)          (phi in reduced Planck units, as CLASS uses)
    background:  rho_cdm = rho_cdm,early a^-3 exp(beta (phi - phi_ini))
                 phi'' + 2 aH phi' + a^2 dV = -3 a^2 beta rho_cdm        (CLASS units, H^2 = sum rho)
    synchronous: delta_c' = -theta_c - h'/2 + beta dphi'
                 theta_c' = -(aH + beta phi') theta_c + beta k^2 dphi    (theta_cdm now evolved in this gauge)
                 dphi''  += -3 a^2 beta rho_cdm delta_c
Every edit is an exact-anchor replacement that must match once. beta = 0 (the default) leaves the code path unchanged.
Usage: python patch_coupling.py /home/syndyr/AxiCLASS_coupled
"""
import sys

ROOT = sys.argv[1]


def edit(path, old, new, count=1):
    p = f"{ROOT}/{path}"
    s = open(p).read()
    n = s.count(old)
    assert n == count, f"{path}: anchor found {n} times, expected {count}:\n{old[:120]}"
    open(p, "w").write(s.replace(old, new))
    print(f"ok  {path}: {old.strip().splitlines()[0][:70]}")


# --- parameter -------------------------------------------------------------------------------------------------
edit("include/background.h",
     "  double phi_ini_scf;       /**< \\f$ \\phi(t_0) \\f$: scalar field initial value */",
     "  double phi_ini_scf;       /**< \\f$ \\phi(t_0) \\f$: scalar field initial value */\n"
     "  double scf_coupling_beta; /**< Coupled Twist: m_cdm ~ exp(beta phi/M_Pl); 0 = uncoupled */")
edit("source/input.c",
     "  pba->phi_ini_scf = 1;",
     "  pba->phi_ini_scf = 1;\n  pba->scf_coupling_beta = 0.;")
edit("source/input.c",
     "    class_read_double(\"m_axion\",pba->m_scf);",
     "    class_read_double(\"m_axion\",pba->m_scf);\n    class_read_double(\"scf_coupling_beta\",pba->scf_coupling_beta);")

# --- background: CDM density follows the field ------------------------------------------------------------------
edit("source/background.c",
     "    pvecback[pba->index_bg_rho_cdm] = pba->Omega0_cdm * pow(pba->H0,2) / pow(a,3);\n    rho_tot += pvecback[pba->index_bg_rho_cdm];",
     "    pvecback[pba->index_bg_rho_cdm] = pba->Omega0_cdm * pow(pba->H0,2) / pow(a,3);\n"
     "    if (pba->has_scf == _TRUE_ && pba->scf_coupling_beta != 0.)   /* Coupled Twist: rho_c a^3 ~ m_c(phi) */\n"
     "      pvecback[pba->index_bg_rho_cdm] *= exp(pba->scf_coupling_beta*(pvecback_B[pba->index_bi_phi_scf]-pba->phi_ini_scf));\n"
     "    rho_tot += pvecback[pba->index_bg_rho_cdm];")
# --- background: Klein-Gordon source ---------------------------------------------------------------------------
edit("source/background.c",
     "    dy[pba->index_bi_phi_prime_scf] = - 2*y[pba->index_bi_phi_prime_scf] - a*dV_scf(pba,y[pba->index_bi_phi_scf])/H ;",
     "    dy[pba->index_bi_phi_prime_scf] = - 2*y[pba->index_bi_phi_prime_scf] - a*dV_scf(pba,y[pba->index_bi_phi_scf])/H ;\n"
     "    if (pba->has_cdm == _TRUE_ && pba->scf_coupling_beta != 0.)   /* Coupled Twist: -3 a^2 beta rho_cdm, per dlna */\n"
     "      dy[pba->index_bi_phi_prime_scf] -= a*3.*pba->scf_coupling_beta*pvecback[pba->index_bg_rho_cdm]/H;")

# --- perturbations: evolve theta_cdm in synchronous gauge when coupled ------------------------------------------
edit("source/perturbations.c",
     "class_define_index(ppv->index_pt_theta_cdm,pba->has_cdm && (ppt->gauge == newtonian),index_pt,1);",
     "class_define_index(ppv->index_pt_theta_cdm,pba->has_cdm && ((ppt->gauge == newtonian) || (pba->scf_coupling_beta != 0.)),index_pt,1);")
edit("source/perturbations.c",
     "      if (ppt->gauge == synchronous) {\n        dy[pv->index_pt_delta_cdm] = -metric_continuity; /* cdm density */\n      }",
     "      if (ppt->gauge == synchronous) {\n        dy[pv->index_pt_delta_cdm] = -metric_continuity; /* cdm density */\n"
     "        if (pba->scf_coupling_beta != 0.) {   /* Coupled Twist: fifth force on CDM only */\n"
     "          dy[pv->index_pt_delta_cdm] += -y[pv->index_pt_theta_cdm] + pba->scf_coupling_beta*y[pv->index_pt_phi_prime_scf];\n"
     "          dy[pv->index_pt_theta_cdm] = -(a_prime_over_a + pba->scf_coupling_beta*pvecback[pba->index_bg_phi_prime_scf])*y[pv->index_pt_theta_cdm]\n"
     "            + pba->scf_coupling_beta*k2*y[pv->index_pt_phi_scf];\n"
     "        }\n      }")
edit("source/perturbations.c",
     "        - (k2 + a2*pvecback[pba->index_bg_ddV_scf])*y[pv->index_pt_phi_scf]; //checked",
     "        - (k2 + a2*pvecback[pba->index_bg_ddV_scf])*y[pv->index_pt_phi_scf]; //checked\n"
     "        if (pba->has_cdm == _TRUE_ && pba->scf_coupling_beta != 0.)   /* Coupled Twist */\n"
     "          dy[pv->index_pt_phi_prime_scf] -= 3.*a2*pba->scf_coupling_beta*pvecback[pba->index_bg_rho_cdm]*y[pv->index_pt_delta_cdm];")
# Approximation switches copy the old vector into the new one: carry theta_cdm across when it exists
edit("source/perturbations.c",
     "        if (ppt->gauge == newtonian) {\n          ppv->y[ppv->index_pt_theta_cdm] =",
     "        if ((ppt->gauge == newtonian) || (pba->scf_coupling_beta != 0.)) {\n          ppv->y[ppv->index_pt_theta_cdm] =")
# Einstein equations and matter sources: include the CDM momentum whenever theta_cdm exists
edit("source/perturbations.c",
     "      if (ppt->gauge == newtonian)\n        ppw->rho_plus_p_theta = ppw->rho_plus_p_theta + ppw->pvecback[pba->index_bg_rho_cdm]*y[ppw->pv->index_pt_theta_cdm];",
     "      if ((ppt->gauge == newtonian) || (pba->scf_coupling_beta != 0.))\n        ppw->rho_plus_p_theta = ppw->rho_plus_p_theta + ppw->pvecback[pba->index_bg_rho_cdm]*y[ppw->pv->index_pt_theta_cdm];")
edit("source/perturbations.c",
     "        if (ppt->gauge == newtonian)\n          rho_plus_p_theta_m += ppw->pvecback[pba->index_bg_rho_cdm]*y[ppw->pv->index_pt_theta_cdm];",
     "        if ((ppt->gauge == newtonian) || (pba->scf_coupling_beta != 0.))\n          rho_plus_p_theta_m += ppw->pvecback[pba->index_bg_rho_cdm]*y[ppw->pv->index_pt_theta_cdm];")
print("all edits applied")
