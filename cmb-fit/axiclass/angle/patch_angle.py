"""S8-A engine patch (theory/DM_COUPLING_PICTURE.md, picture B): put the dilaton coupling on the ultralight angle
(AxiCLASS pheno_axion fluid) instead of on the cold dark matter. Applies to a COPY of AxiCLASS_coupled_nlfix_ula.

The angle's mass runs as m_eff = m exp(beta_a phi/M_Pl), beta_a = sqrt(2/3) (= -lambda/2, derived). For a field with
V ~ m_eff^2, dV/dphi = 2 beta_a V and 2V = rho (1 - w) for any w (frozen: w = -1, 2V = 2 rho; oscillating, averaged:
w = 0, <2V> = rho). So with B = beta_a (1 - w):
  background   rho_fld'  = -3 aH (1+w) rho_fld + B phi' rho_fld                   (conformal time)
               phi''     += -3 a^2 B rho_fld                                        (CLASS units)
  synchronous  delta_fld' += B dphi'
               theta_fld' += -B phi' theta_fld + B k^2 dphi / (1+w)   (only while 1+w > 1e-3: a frozen field has no flow)
               dphi''    += -3 a^2 B rho_fld delta_fld                              (delta w neglected)
w = 0 recovers the coupled-CDM equations of patch_coupling.py with beta -> beta_a (gate G-A1).
beta_a = 0 (default) leaves the code path unchanged (gate G-A0).
Supported only with use_delta_fld_over_1plusw = no and use_big_theta_fld = no (the S8-L settings; checked at run time).
Usage: python patch_angle.py <path to a COPY of AxiCLASS_coupled_nlfix_ula>"""
import sys

ROOT = sys.argv[1]


def edit(path, old, new, count=1):
    p = f"{ROOT}/{path}"
    s = open(p).read()
    n = s.count(old)
    assert n == count, f"{path}: anchor found {n} times, expected {count}:\n{old[:120]}"
    open(p, "w").write(s.replace(old, new))
    print(f"ok  {path}: {old.strip().splitlines()[0][:70]}")


edit("include/background.h",
     "  double scf_coupling_beta; /**< Coupled Twist: m_cdm ~ exp(beta phi/M_Pl); 0 = uncoupled */",
     "  double scf_coupling_beta; /**< Coupled Twist: m_cdm ~ exp(beta phi/M_Pl); 0 = uncoupled */\n"
     "  double fld_coupling_beta; /**< S8-A: m_angle ~ exp(beta_a phi/M_Pl) on the pheno_axion fluid; 0 = uncoupled */")
edit("source/input.c",
     "  pba->scf_coupling_beta = 0.;",
     "  pba->scf_coupling_beta = 0.;\n  pba->fld_coupling_beta = 0.;")
edit("source/input.c",
     "    class_read_double(\"scf_coupling_beta\",pba->scf_coupling_beta);",
     "    class_read_double(\"scf_coupling_beta\",pba->scf_coupling_beta);\n"
     "    class_read_double(\"fld_coupling_beta\",pba->fld_coupling_beta);")

# background: fluid density and Klein-Gordon source (per dln a)
edit("source/background.c",
     "    dy[pba->index_bi_rho_fld] = -3.*(1.+pvecback[pba->index_bg_w_fld])*y[pba->index_bi_rho_fld];\n  }",
     "    dy[pba->index_bi_rho_fld] = -3.*(1.+pvecback[pba->index_bg_w_fld])*y[pba->index_bi_rho_fld];\n"
     "    if (pba->has_scf == _TRUE_ && pba->fld_coupling_beta != 0.)   /* S8-A: B dphi/dlna rho_fld */\n"
     "      dy[pba->index_bi_rho_fld] += pba->fld_coupling_beta*(1.-pvecback[pba->index_bg_w_fld])\n"
     "        *y[pba->index_bi_phi_prime_scf]/a/H*y[pba->index_bi_rho_fld];\n  }")
edit("source/background.c",
     "      dy[pba->index_bi_phi_prime_scf] -= a*3.*pba->scf_coupling_beta*pvecback[pba->index_bg_rho_cdm]/H;\n",
     "      dy[pba->index_bi_phi_prime_scf] -= a*3.*pba->scf_coupling_beta*pvecback[pba->index_bg_rho_cdm]/H;\n"
     "    if (pba->has_fld == _TRUE_ && pba->fld_coupling_beta != 0.)   /* S8-A: -3 a^2 B rho_fld, per dlna */\n"
     "      dy[pba->index_bi_phi_prime_scf] -= a*3.*pba->fld_coupling_beta*(1.-pvecback[pba->index_bg_w_fld])\n"
     "        *pvecback[pba->index_bg_rho_fld]/H;\n")

# perturbations: fluid continuity and Euler (default variables), perturbed Klein-Gordon
edit("source/perturbations.c",
     "            -(1+w_fld)*(y[pv->index_pt_theta_fld]+metric_continuity)\n"
     "            -9.*(1+w_fld)*(cs2-ca2)*a_prime_over_a*a_prime_over_a*y[pv->index_pt_theta_fld]/k2;\n",
     "            -(1+w_fld)*(y[pv->index_pt_theta_fld]+metric_continuity)\n"
     "            -9.*(1+w_fld)*(cs2-ca2)*a_prime_over_a*a_prime_over_a*y[pv->index_pt_theta_fld]/k2;\n"
     "            if (pba->has_scf == _TRUE_ && pba->fld_coupling_beta != 0.)   /* S8-A: + B dphi' */\n"
     "              dy[pv->index_pt_delta_fld] += pba->fld_coupling_beta*(1.-w_fld)*y[pv->index_pt_phi_prime_scf];\n")
edit("source/perturbations.c",
     "            if((1+w_fld)!=0.0) dy[pv->index_pt_theta_fld] += cs2*k2/(1.+w_fld)*y[pv->index_pt_delta_fld];\n",
     "            if((1+w_fld)!=0.0) dy[pv->index_pt_theta_fld] += cs2*k2/(1.+w_fld)*y[pv->index_pt_delta_fld];\n"
     "            if (pba->has_scf == _TRUE_ && pba->fld_coupling_beta != 0. && (1.+w_fld) > 1.e-3) {   /* S8-A */\n"
     "              dy[pv->index_pt_theta_fld] += -pba->fld_coupling_beta*(1.-w_fld)*pvecback[pba->index_bg_phi_prime_scf]\n"
     "                *y[pv->index_pt_theta_fld] + pba->fld_coupling_beta*(1.-w_fld)/(1.+w_fld)*k2*y[pv->index_pt_phi_scf];\n"
     "            }\n")
edit("source/perturbations.c",
     "          dy[pv->index_pt_phi_prime_scf] -= 3.*a2*pba->scf_coupling_beta*pvecback[pba->index_bg_rho_cdm]*y[pv->index_pt_delta_cdm];\n",
     "          dy[pv->index_pt_phi_prime_scf] -= 3.*a2*pba->scf_coupling_beta*pvecback[pba->index_bg_rho_cdm]*y[pv->index_pt_delta_cdm];\n"
     "        if (pba->has_fld == _TRUE_ && pba->fld_coupling_beta != 0.)   /* S8-A */\n"
     "          dy[pv->index_pt_phi_prime_scf] -= 3.*a2*pba->fld_coupling_beta*(1.-pvecback[pba->index_bg_w_fld])\n"
     "            *pvecback[pba->index_bg_rho_fld]*y[pv->index_pt_delta_fld];\n")
# (the default-variables restriction is enforced by the fitter, angle_fit.py)

# delta_m option (S8-A): count the pheno_axion fluid as matter in delta_m / theta_m, so sigma8, S8, f sigma8 and P_m
# include the angle (CLASS leaves it out by default: the S8-LNL D2 caveat). Off by default: unchanged code path.
edit("include/background.h",
     "  double fld_coupling_beta; /**< S8-A: m_angle ~ exp(beta_a phi/M_Pl) on the pheno_axion fluid; 0 = uncoupled */",
     "  double fld_coupling_beta; /**< S8-A: m_angle ~ exp(beta_a phi/M_Pl) on the pheno_axion fluid; 0 = uncoupled */\n"
     "  int fld_in_delta_m;       /**< S8-A: 1 = count the pheno_axion fluid as matter in delta_m (sigma8, P_m) */")
edit("source/input.c",
     "  pba->fld_coupling_beta = 0.;",
     "  pba->fld_coupling_beta = 0.;\n  pba->fld_in_delta_m = 0;")
edit("source/input.c",
     "    class_read_double(\"fld_coupling_beta\",pba->fld_coupling_beta);",
     "    class_read_double(\"fld_coupling_beta\",pba->fld_coupling_beta);\n"
     "    class_read_int(\"fld_in_delta_m\",pba->fld_in_delta_m);")
edit("source/perturbations.c",
     "    if (ppt->has_source_delta_m == _TRUE_)\n      ppw->delta_m = delta_rho_m/rho_m;\n",
     "    if (pba->has_fld == _TRUE_ && pba->fld_in_delta_m == 1 && pba->use_ppf == _FALSE_) {   /* S8-A */\n"
     "      delta_rho_m += ppw->delta_rho_fld;\n"
     "      rho_m += ppw->pvecback[pba->index_bg_rho_fld];\n"
     "      rho_plus_p_theta_m += ppw->rho_plus_p_theta_fld;\n"
     "      rho_plus_p_m += (1.+ppw->pvecback[pba->index_bg_w_fld])*ppw->pvecback[pba->index_bg_rho_fld];\n"
     "    }\n"
     "    if (ppt->has_source_delta_m == _TRUE_)\n      ppw->delta_m = delta_rho_m/rho_m;\n")
print("patched; build with build_angle.sh")
