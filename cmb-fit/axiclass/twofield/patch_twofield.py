"""Two-field engine, route 1 (TWOFIELD_ENGINE_STATUS.md): a SECOND full scalar field "dil" in AxiCLASS, so that the
native scf can be the early n = 3 axion field (AxiCLASS's own EDE machinery, KG + fluid switch, shooting) while the
flagship's late dilaton becomes "dil". Applies to a COPY of AxiCLASS_coupled_nlfix (untouched original).

dil (exactly the flagship's scf dilaton, same units/conventions as CLASS scf; rho = (phi'^2/2a^2 + V)/3):
  V = dil_mu4 * exp(-dil_kappa phi)          (= the flagship's double_exp with lambda2 = mu2 = 0)
  phi(ini) = dil_phi_ini (default 1), phi'(ini) = 0
  CDM coupling dil_beta:  rho_cdm a^3 ~ exp(beta (phi - phi_ini));  phi'' += -3 a^2 beta rho_cdm   (as patch_coupling)
  synchronous:  dphi'' = -2 aH dphi' - (h'/2) phi' - (k^2 + a^2 V'') dphi - 3 a^2 beta rho_cdm delta_cdm
                delta_cdm' += -theta_cdm + beta dphi';  theta_cdm' = -(aH + beta phi') theta_cdm + beta k^2 dphi
  Closure: input leaves Omega_Lambda as the closure; background_init moves that budget to dil (Omega_Lambda -> 0) and
  background_solve iterates dil_mu4 until rho_tot(today) = H0^2 + K (rel. 1e-9). Synchronous gauge only.
dilaton = yes switches it on; default off leaves every code path unchanged (gate G-2F0: bitwise-equal C_l).
Usage: python patch_twofield.py <path to a COPY of AxiCLASS_coupled_nlfix>"""
import sys

ROOT = sys.argv[1]


def edit(path, old, new, count=1):
    p = f"{ROOT}/{path}"
    s = open(p).read()
    n = s.count(old)
    assert n == count, f"{path}: anchor found {n} times, expected {count}:\n{old[:160]}"
    open(p, "w").write(s.replace(old, new))
    print(f"ok  {path}: {old.strip().splitlines()[0][:70]}")


# ---------------- halofit (external/Halofit/halofit.c): the flagship build's nl-scf-fix treats its scf dilaton as dark
# energy (not rho-3p matter) in HALOFIT's Omega_m, Omega_v, w and f_nu. The dilaton now lives in "dil", so it gets the
# same treatment (G-TF-PC diagnosis, 10 Nov 2026: without this HALOFIT counts the dilaton as matter -> lensing at high l).
HF = "external/Halofit/halofit.c"
DILHF = ("    if (pba->has_dil == _TRUE_) { /* two-field: the dilaton is dark energy for HALOFIT, as the flagship's scf */\n"
         "      Omega_m -= (pvecback[pba->index_bg_rho_dil]-3.*pvecback[pba->index_bg_p_dil])/pvecback[pba->index_bg_rho_crit];\n"
         "      Omega_v = 1.-Omega_m-pvecback[pba->index_bg_Omega_r]+3.*pvecback[pba->index_bg_p_dil]/pvecback[pba->index_bg_rho_crit]\n"
         "        + ((pba->has_scf == _TRUE_) ? 3.*pvecback[pba->index_bg_p_scf]/pvecback[pba->index_bg_rho_crit] : 0.);\n"
         "    }\n")


def halofit():
    # f_nu: only builds whose nl-scf-fix also moved the scf out of f_nu (patch_nlfix.py after B0) get the dil there too;
    # an older flagship build (the PC's: plain Omega0_m, as the git patch 0001-nl-scf-fix) is matched by leaving it alone.
    src = open(f"{ROOT}/{HF}").read()
    if "    fnu = pba->Omega0_ncdm_tot/Omega_m;\n" not in src:
        assert src.count("    fnu = pba->Omega0_ncdm_tot/pba->Omega0_m;\n") == 1, "halofit.c: unknown f_nu line"
        print("ok  external/Halofit/halofit.c: f_nu uses Omega0_m in this build (as the flagship build): unchanged")
    else:
     edit(HF,
         "    fnu = pba->Omega0_ncdm_tot/Omega_m;\n",
         "    if (pba->has_dil == _TRUE_) {   /* two-field: present-day matter excludes the dilaton too */\n"
         "      class_call(background_at_tau(pba,pba->conformal_age,long_info,inter_normal,&last_index,pvecback),\n"
         "                 pba->error_message,pfo->error_message);\n"
         "      Omega_m -= (pvecback[pba->index_bg_rho_dil]-3.*pvecback[pba->index_bg_p_dil])/pvecback[pba->index_bg_rho_crit];\n"
         "    }\n"
         "    fnu = pba->Omega0_ncdm_tot/Omega_m;\n")
    edit(HF,
         "      Omega_v = 1.-Omega_m-(pvecback[pba->index_bg_Omega_r]-3.*pvecback[pba->index_bg_p_scf]/pvecback[pba->index_bg_rho_crit]);\n    }\n"
         "    /* until v2.9.3",
         "      Omega_v = 1.-Omega_m-(pvecback[pba->index_bg_Omega_r]-3.*pvecback[pba->index_bg_p_scf]/pvecback[pba->index_bg_rho_crit]);\n    }\n"
         + DILHF + "    /* until v2.9.3")
    edit(HF,
         "    if (pba->has_scf == _TRUE_ && pba->has_fld == _FALSE_) { /* nl-scf-fix: effective w of field + Lambda */\n"
         "      double rho_de = pvecback[pba->index_bg_rho_scf], p_de = pvecback[pba->index_bg_p_scf];\n",
         "    if ((pba->has_scf == _TRUE_ || pba->has_dil == _TRUE_) && pba->has_fld == _FALSE_) { /* nl-scf-fix: effective w of fields + Lambda */\n"
         "      double rho_de = 0., p_de = 0.;\n"
         "      if (pba->has_scf == _TRUE_) { rho_de += pvecback[pba->index_bg_rho_scf]; p_de += pvecback[pba->index_bg_p_scf]; }\n"
         "      if (pba->has_dil == _TRUE_) { rho_de += pvecback[pba->index_bg_rho_dil]; p_de += pvecback[pba->index_bg_p_dil]; }\n")
    edit(HF,
         "    Omega_v = 1.-Omega_m-(pvecback[pba->index_bg_Omega_r]-3.*pvecback[pba->index_bg_p_scf]/pvecback[pba->index_bg_rho_crit]);\n  }\n\n"
         "  // for debugging:",
         "    Omega_v = 1.-Omega_m-(pvecback[pba->index_bg_Omega_r]-3.*pvecback[pba->index_bg_p_scf]/pvecback[pba->index_bg_rho_crit]);\n  }\n"
         + DILHF.replace("\n    ", "\n  ").replace("    if (pba->has_dil", "  if (pba->has_dil", 1) + "\n  // for debugging:")


if len(sys.argv) > 2 and sys.argv[2] == "--halofit-only":   # an already-patched build that predates this fix
    halofit()
    sys.exit()


DILON = "(pba->has_dil == _TRUE_ && pba->dil_beta != 0.)"

# ---------------- background.h
edit("include/background.h",
     "  double scf_coupling_beta; /**< Coupled Twist: m_cdm ~ exp(beta phi/M_Pl); 0 = uncoupled */",
     "  double scf_coupling_beta; /**< Coupled Twist: m_cdm ~ exp(beta phi/M_Pl); 0 = uncoupled */\n"
     "  short has_dil;            /**< two-field: second scalar field (late dilaton) */\n"
     "  double dil_kappa, dil_beta, dil_phi_ini, dil_mu4; /**< V = mu4 exp(-kappa phi); CDM coupling beta */\n"
     "  int dil_closure_iterations;")
edit("include/background.h",
     "  int index_bg_ddw_scf;",
     "  int index_bg_ddw_scf;\n  int index_bg_phi_dil, index_bg_phi_prime_dil, index_bg_V_dil, index_bg_dV_dil, index_bg_ddV_dil,"
     " index_bg_rho_dil, index_bg_p_dil;")
edit("include/background.h",
     "  int index_bi_phi_prime_scf;",
     "  int index_bi_phi_prime_scf;\n  int index_bi_phi_dil, index_bi_phi_prime_dil;")

# ---------------- input.c
edit("source/input.c",
     "  pba->scf_coupling_beta = 0.;",
     "  pba->scf_coupling_beta = 0.;\n  pba->has_dil = _FALSE_;\n  pba->dil_kappa = 1.;\n  pba->dil_beta = 0.;\n"
     "  pba->dil_phi_ini = 1.;\n  pba->dil_mu4 = 0.;")
edit("source/input.c",
     "    class_read_double(\"scf_coupling_beta\",pba->scf_coupling_beta);",
     "    class_read_double(\"scf_coupling_beta\",pba->scf_coupling_beta);\n"
     "    { char dil_str[_ARGUMENT_LENGTH_MAX_]; int dil_flag;                       /* two-field: dilaton = yes */\n"
     "      class_call(parser_read_string(pfc,\"dilaton\",&dil_str,&dil_flag,errmsg),errmsg,errmsg);\n"
     "      if (dil_flag == _TRUE_ && (strstr(dil_str,\"y\") != NULL || strstr(dil_str,\"Y\") != NULL)) pba->has_dil = _TRUE_; }\n"
     "    class_read_double(\"dil_kappa\",pba->dil_kappa);\n    class_read_double(\"dil_beta\",pba->dil_beta);\n"
     "    class_read_double(\"dil_phi_ini\",pba->dil_phi_ini);")

# ---------------- background.c: densities
edit("source/background.c",
     "      pvecback[pba->index_bg_rho_cdm] *= exp(pba->scf_coupling_beta*(pvecback_B[pba->index_bi_phi_scf]-pba->phi_ini_scf));\n",
     "      pvecback[pba->index_bg_rho_cdm] *= exp(pba->scf_coupling_beta*(pvecback_B[pba->index_bi_phi_scf]-pba->phi_ini_scf));\n"
     f"    if {DILON}   /* two-field: CDM mass runs with the dilaton */\n"
     "      pvecback[pba->index_bg_rho_cdm] *= exp(pba->dil_beta*(pvecback_B[pba->index_bi_phi_dil]-pba->dil_phi_ini));\n")
edit("source/background.c",
     "  /* idm */\n  if (pba->has_idm == _TRUE_) {",
     "  /* two-field dilaton (same formulas and bookkeeping as the scf block) */\n"
     "  if (pba->has_dil == _TRUE_) {\n"
     "    double pd = pvecback_B[pba->index_bi_phi_dil], pdp = pvecback_B[pba->index_bi_phi_prime_dil];\n"
     "    double Vd = pba->dil_mu4*exp(-pba->dil_kappa*pd);\n"
     "    pvecback[pba->index_bg_phi_dil] = pd;\n    pvecback[pba->index_bg_phi_prime_dil] = pdp;\n"
     "    pvecback[pba->index_bg_V_dil] = Vd;\n    pvecback[pba->index_bg_dV_dil] = -pba->dil_kappa*Vd;\n"
     "    pvecback[pba->index_bg_ddV_dil] = pba->dil_kappa*pba->dil_kappa*Vd;\n"
     "    pvecback[pba->index_bg_rho_dil] = (pdp*pdp/(2*a*a) + Vd)/3.;\n"
     "    pvecback[pba->index_bg_p_dil] = (pdp*pdp/(2*a*a) - Vd)/3.;\n"
     "    rho_tot += pvecback[pba->index_bg_rho_dil];\n    p_tot += pvecback[pba->index_bg_p_dil];\n"
     "    rho_r += 3.*pvecback[pba->index_bg_p_dil];\n"
     "    rho_m += pvecback[pba->index_bg_rho_dil] - 3.*pvecback[pba->index_bg_p_dil];\n  }\n\n"
     "  /* idm */\n  if (pba->has_idm == _TRUE_) {")
edit("source/background.c",
     "    pvecback[pba->index_bg_p_tot_prime] += pvecback[pba->index_bg_p_prime_scf];\n  }\n",
     "    pvecback[pba->index_bg_p_tot_prime] += pvecback[pba->index_bg_p_prime_scf];\n  }\n"
     "  if (pba->has_dil == _TRUE_)   /* as for scf */\n"
     "    pvecback[pba->index_bg_p_tot_prime] += pvecback[pba->index_bg_phi_prime_dil]*\n"
     "      (-pvecback[pba->index_bg_phi_prime_dil]*pvecback[pba->index_bg_H]/a-2./3.*pvecback[pba->index_bg_dV_dil]);\n")
# indices
edit("source/background.c",
     "  class_define_index(pba->index_bg_ddw_scf,pba->has_scf,index_bg,1);",
     "  class_define_index(pba->index_bg_ddw_scf,pba->has_scf,index_bg,1);\n"
     + "".join(f"  class_define_index(pba->index_bg_{n}_dil,pba->has_dil,index_bg,1);\n"
               for n in ("phi", "phi_prime", "V", "dV", "ddV", "rho", "p")))
edit("source/background.c",
     "  class_define_index(pba->index_bi_rho_scf,pba->has_scf,index_bi,1);",
     "  class_define_index(pba->index_bi_rho_scf,pba->has_scf,index_bi,1);\n"
     "  class_define_index(pba->index_bi_phi_dil,pba->has_dil,index_bi,1);\n"
     "  class_define_index(pba->index_bi_phi_prime_dil,pba->has_dil,index_bi,1);")
# initial conditions
edit("source/background.c",
     "  if (pba->has_scf == _TRUE_) {\n    if (pba->attractor_ic_scf == _TRUE_) {",
     "  if (pba->has_dil == _TRUE_) {\n    pvecback_integration[pba->index_bi_phi_dil] = pba->dil_phi_ini;\n"
     "    pvecback_integration[pba->index_bi_phi_prime_dil] = 0.;\n  }\n"
     "  if (pba->has_scf == _TRUE_) {\n    if (pba->attractor_ic_scf == _TRUE_) {")
# derivatives (per dlna, as the scf)
edit("source/background.c",
     "  if (pba->has_scf == _TRUE_){\n    /*<VP: Main modifications to SCF in AxiCLASS",
     "  if (pba->has_dil == _TRUE_) {\n"
     "    dy[pba->index_bi_phi_dil] = y[pba->index_bi_phi_prime_dil]/a/H;\n"
     "    dy[pba->index_bi_phi_prime_dil] = - 2*y[pba->index_bi_phi_prime_dil]\n"
     "      + a*pba->dil_kappa*pba->dil_mu4*exp(-pba->dil_kappa*y[pba->index_bi_phi_dil])/H;\n"
     f"    if (pba->has_cdm == _TRUE_ && {DILON})\n"
     "      dy[pba->index_bi_phi_prime_dil] -= a*3.*pba->dil_beta*pvecback[pba->index_bg_rho_cdm]/H;\n  }\n\n"
     "  if (pba->has_scf == _TRUE_){\n    /*<VP: Main modifications to SCF in AxiCLASS")
# closure: Lambda's budget goes to dil, then iterate mu4
edit("source/background.c",
     "  class_call(background_solve(ppr,pba),",
     "  if (pba->has_dil == _TRUE_) {   /* two-field: the dilaton takes the closure input gave to Lambda */\n"
     "    class_test(pba->has_lambda == _FALSE_, pba->error_message,\n"
     "               \"dilaton = yes needs Omega_Lambda as the input closure (leave Omega_Lambda unset, Omega_fld = 0)\");\n"
     "    if (pba->dil_mu4 <= 0.)\n"
     "      pba->dil_mu4 = 3.*pba->Omega0_lambda*pba->H0*pba->H0*exp(pba->dil_kappa*pba->dil_phi_ini);\n"
     "    pba->Omega0_lambda = 0.;\n    pba->dil_closure_iterations = 0;\n  }\n"
     "  class_call(background_solve(ppr,pba),")
edit("source/background.c",
     "       }else{\n         //no axion or no loop required so we ignore the loop.\n         is_axion_converged = _TRUE_;\n"
     "       }\n  }\n  /** - recover some quantities today */",
     "       }else{\n         //no axion or no loop required so we ignore the loop.\n         is_axion_converged = _TRUE_;\n"
     "       }\n"
     "  if (is_axion_converged == _TRUE_ && pba->has_dil == _TRUE_) {   /* two-field closure on the dilaton height */\n"
     "    double * pvb_dil; double rho_now, rho_dil_now, target;\n"
     "    class_alloc(pvb_dil,pba->bg_size*sizeof(double),pba->error_message);\n"
     "    class_call(background_functions(pba,1.,pvecback_integration,long_info,pvb_dil),pba->error_message,pba->error_message);\n"
     "    rho_now = pvb_dil[pba->index_bg_rho_tot]; rho_dil_now = pvb_dil[pba->index_bg_rho_dil];\n"
     "    free(pvb_dil);\n"
     "    target = pba->H0*pba->H0 + pba->K - (rho_now - rho_dil_now);\n"
     "    class_test(target <= 0., pba->error_message, \"two-field closure: no room left for the dilaton today\");\n"
     "    if (fabs(rho_now/(pba->H0*pba->H0 + pba->K) - 1.) > 1.e-9) {\n"
     "      pba->dil_closure_iterations++;\n"
     "      class_test(pba->dil_closure_iterations > 60, pba->error_message, \"two-field closure did not converge\");\n"
     "      pba->dil_mu4 *= target/rho_dil_now;\n"
     "      is_axion_converged = _FALSE_;\n"
     "      free(pvecback_integration);\n      free(pba->loga_table);\n      free(used_in_output);\n"
     "    }\n  }\n"
     "  }\n  /** - recover some quantities today */")

# ---------------- perturbations.c
PERT = "source/perturbations.c"
edit(PERT, "(pba->scf_coupling_beta != 0.))",
     f"(pba->scf_coupling_beta != 0.) || {DILON})", count=4)
edit(PERT,
     "    /* scalar field */\n    // CO 22.01.18 - delta and theta need to be initialised if we intend to use the fluid eqs",
     "    /* two-field dilaton (KG only) */\n"
     "    class_define_index(ppv->index_pt_phi_dil,pba->has_dil,index_pt,1);\n"
     "    class_define_index(ppv->index_pt_phi_prime_dil,pba->has_dil,index_pt,1);\n\n"
     "    /* scalar field */\n    // CO 22.01.18 - delta and theta need to be initialised if we intend to use the fluid eqs")
edit(PERT,
     "      if (pba->has_scf == _TRUE_&& pba->scf_has_perturbations == _TRUE_) {\n        if (scf_kg_variables == _TRUE_\n",
     "      if (pba->has_dil == _TRUE_) {\n"
     "        ppv->y[ppv->index_pt_phi_dil] = ppw->pv->y[ppw->pv->index_pt_phi_dil];\n"
     "        ppv->y[ppv->index_pt_phi_prime_dil] = ppw->pv->y[ppw->pv->index_pt_phi_prime_dil];\n      }\n\n"
     "      if (pba->has_scf == _TRUE_&& pba->scf_has_perturbations == _TRUE_) {\n        if (scf_kg_variables == _TRUE_\n")
edit(PERT,
     "    if (pba->has_scf == _TRUE_&& pba->scf_has_perturbations == _TRUE_) {\n\n      if (ppt->perturbations_verbose>10)\n"
     "        fprintf(stdout,\"Inside scf if statement.",
     "    if (pba->has_dil == _TRUE_) {   /* two-field dilaton: synchronous gauge only */\n"
     "      class_test(ppt->gauge != synchronous, ppt->error_message, \"dilaton = yes supports the synchronous gauge only\");\n"
     "      ppw->delta_rho += 1./3.*(1./a2*ppw->pvecback[pba->index_bg_phi_prime_dil]*y[ppw->pv->index_pt_phi_prime_dil]\n"
     "                               + ppw->pvecback[pba->index_bg_dV_dil]*y[ppw->pv->index_pt_phi_dil]);\n"
     "      ppw->delta_p += 1./3.*(1./a2*ppw->pvecback[pba->index_bg_phi_prime_dil]*y[ppw->pv->index_pt_phi_prime_dil]\n"
     "                             - ppw->pvecback[pba->index_bg_dV_dil]*y[ppw->pv->index_pt_phi_dil]);\n"
     "      ppw->rho_plus_p_theta += 1./3.*k*k/a2*ppw->pvecback[pba->index_bg_phi_prime_dil]*y[ppw->pv->index_pt_phi_dil];\n"
     "    }\n\n"
     "    if (pba->has_scf == _TRUE_&& pba->scf_has_perturbations == _TRUE_) {\n\n      if (ppt->perturbations_verbose>10)\n"
     "        fprintf(stdout,\"Inside scf if statement.")
edit(PERT,
     "            + pba->scf_coupling_beta*k2*y[pv->index_pt_phi_scf];\n        }\n",
     "            + pba->scf_coupling_beta*k2*y[pv->index_pt_phi_scf];\n        }\n"
     f"        if {DILON} {{   /* two-field: fifth force from the dilaton on CDM */\n"
     "          if (pba->scf_coupling_beta == 0.) {\n"
     "            dy[pv->index_pt_delta_cdm] += -y[pv->index_pt_theta_cdm];\n"
     "            dy[pv->index_pt_theta_cdm] = -a_prime_over_a*y[pv->index_pt_theta_cdm];\n          }\n"
     "          dy[pv->index_pt_delta_cdm] += pba->dil_beta*y[pv->index_pt_phi_prime_dil];\n"
     "          dy[pv->index_pt_theta_cdm] += -pba->dil_beta*pvecback[pba->index_bg_phi_prime_dil]*y[pv->index_pt_theta_cdm]\n"
     "            + pba->dil_beta*k2*y[pv->index_pt_phi_dil];\n        }\n")
edit(PERT,
     "    /** - ---> scalar field (scf) */\n    if (pba->has_scf == _TRUE_ && pba->scf_has_perturbations == _TRUE_) {",
     "    /** - ---> two-field dilaton: Klein-Gordon (synchronous gauge) */\n"
     "    if (pba->has_dil == _TRUE_) {\n"
     "      dy[pv->index_pt_phi_dil] = y[pv->index_pt_phi_prime_dil];\n"
     "      dy[pv->index_pt_phi_prime_dil] = - 2.*a_prime_over_a*y[pv->index_pt_phi_prime_dil]\n"
     "        - metric_continuity*pvecback[pba->index_bg_phi_prime_dil]\n"
     "        - (k2 + a2*pvecback[pba->index_bg_ddV_dil])*y[pv->index_pt_phi_dil];\n"
     f"      if (pba->has_cdm == _TRUE_ && {DILON})\n"
     "        dy[pv->index_pt_phi_prime_dil] -= 3.*a2*pba->dil_beta*pvecback[pba->index_bg_rho_cdm]*y[pv->index_pt_delta_cdm];\n"
     "    }\n\n"
     "    /** - ---> scalar field (scf) */\n    if (pba->has_scf == _TRUE_ && pba->scf_has_perturbations == _TRUE_) {")
edit("include/perturbations.h",
     "  int index_pt_phi_scf;",
     "  int index_pt_phi_dil, index_pt_phi_prime_dil;  /**< two-field dilaton */\n  int index_pt_phi_scf;")
halofit()
print("patched", ROOT)
