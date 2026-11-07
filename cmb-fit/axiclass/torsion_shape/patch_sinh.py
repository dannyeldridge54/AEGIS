# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights.
"""Fingerprint option for AxiCLASS (re-implementation, 7 Nov 2026; rule: PREREGISTRATION_SINH.md, locked 26 Oct).
The original axion_sinh_x0 build was never committed; this re-adds it exactly as the rule describes:
    V = m^2 F^2 [1 - cos(g(phi)/F)]^n,   g(phi) = s [sinh(phi/s + x0) - sinh(x0)] / cosh(x0),   s = sqrt(3/2) M_Pl,
with x0 = arsinh(1/gamma0) = 2.1445 passed as `axion_sinh_x0` (0 = off). g(0) = 0 and g'(0) = 1, so the minimum and the
small-field limit match the plain cosine. With the option off every code path is the original one (regression check:
regress_sinh.py). Exact-anchor edits; each must match once.
Usage: python patch_sinh.py <path to an AxiCLASS clone at ae9609e (or an nlfix copy)>"""
import os
import sys

ROOT = sys.argv[1]

SINH_FUNCS = r'''/* Fingerprint (PREREGISTRATION_SINH.md): potential periodic in 1/gamma, V = m^2 F^2 [1 - cos(g/F)]^n with
   g(phi) = s (sinh(phi/s + x0) - sinh(x0)) / cosh(x0), s = sqrt(3/2) (reduced Planck units). Used only if axion_sinh_x0 != 0. */
static double fp_g(struct background *pba, double phi, double *g1, double *g2){
  double s = sqrt(1.5), x0 = pba->axion_sinh_x0, c0 = cosh(x0);
  *g1 = cosh(phi/s + x0)/c0;
  *g2 = sinh(phi/s + x0)/(s*c0);
  return s*(sinh(phi/s + x0) - sinh(x0))/c0;
}
static double V_axion_sinh_scf(struct background *pba, double phi){
  double n = pba->n_axion, fa = pba->f_axion, m = pba->m_scf*pba->H0, g1, g2;
  double g = fp_g(pba, phi, &g1, &g2);
  return pow(m,2)*pow(fa,2)*pow(1 - cos(g/fa), n);
}
static double dV_axion_sinh_scf(struct background *pba, double phi){
  double n = pba->n_axion, fa = pba->f_axion, m = pba->m_scf*pba->H0, g1, g2;
  double g = fp_g(pba, phi, &g1, &g2), u = 1 - cos(g/fa);
  double un1 = (n == 1) ? 1. : pow(u, n-1);
  return n*pow(m,2)*fa*un1*sin(g/fa)*g1;
}
static double ddV_axion_sinh_scf(struct background *pba, double phi){
  double n = pba->n_axion, fa = pba->f_axion, m = pba->m_scf*pba->H0, g1, g2;
  double g = fp_g(pba, phi, &g1, &g2), u = 1 - cos(g/fa), sn = sin(g/fa), cs = cos(g/fa);
  double un1 = (n == 1) ? 1. : pow(u, n-1);
  double un2 = (n == 1) ? 0. : ((n == 2) ? 1. : pow(u, n-2));
  return n*pow(m,2)*((n-1)*un2*sn*sn*g1*g1 + un1*cs*g1*g1 + fa*un1*sn*g2);
}

'''

EDITS = [
    ("include/background.h",
     "  double n_axion;\n",
     "  double n_axion;\n  double axion_sinh_x0; /* Fingerprint: x0 = arsinh(1/gamma0); 0 = off (plain cosine) */\n"),
    ("source/input.c",
     "  pba->m_scf = 0.0;\n",
     "  pba->m_scf = 0.0;\n  pba->axion_sinh_x0 = 0.;\n"),
    ("source/input.c",
     "         pba->scf_potential = axion;\n",
     "         pba->scf_potential = axion;\n"
     "         class_call(parser_read_double(pfc,\"axion_sinh_x0\",&param1,&flag1,errmsg),errmsg,errmsg);\n"
     "         if (flag1 == _TRUE_) pba->axion_sinh_x0 = param1; /* Fingerprint option */\n"),
    ("source/background.c",
     "/** parameters and functions for the axion potential\n",
     SINH_FUNCS + "/** parameters and functions for the axion potential\n"),
    ("source/background.c",
     "double V_axion_scf(\n                  struct background *pba,\n                  double phi){\n",
     "double V_axion_scf(\n                  struct background *pba,\n                  double phi){\n"
     "    if (pba->axion_sinh_x0 != 0.) return V_axion_sinh_scf(pba, phi);\n"),
    ("source/background.c",
     "double dV_axion_scf(\n                  struct background *pba,\n                  double phi){\n",
     "double dV_axion_scf(\n                  struct background *pba,\n                  double phi){\n"
     "    if (pba->axion_sinh_x0 != 0.) return dV_axion_sinh_scf(pba, phi);\n"),
    ("source/background.c",
     "double ddV_axion_scf(\n                  struct background *pba,\n                  double phi){\n",
     "double ddV_axion_scf(\n                  struct background *pba,\n                  double phi){\n"
     "     if (pba->axion_sinh_x0 != 0.) return ddV_axion_sinh_scf(pba, phi);\n"),
]

for rel, old, new in EDITS:
    p = os.path.join(ROOT, rel)
    t = open(p, encoding="utf-8", errors="surrogateescape").read()
    if new in t:
        print(f"already patched: {rel}")
        continue
    k = t.count(old)
    if k != 1:
        sys.exit(f"anchor matched {k} times in {rel}; refusing to patch")
    open(p, "w", encoding="utf-8", errors="surrogateescape").write(t.replace(old, new))
    print(f"patched: {rel}")
print("Fingerprint option added: axion_sinh_x0 (0 = off). Rebuild, then run regress_sinh.py.")
