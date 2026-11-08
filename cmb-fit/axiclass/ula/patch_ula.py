"""Spiral-L engine patch: let the AxiCLASS pheno_axion fluid (n = 1, w -> 0) act as an ultralight dark-matter share
beside the coupled dilaton. Two edits, neither touching the physics equations:
  1. HALOFIT: when the fluid is the pheno_axion (matter-like) share, the dark-energy w HALOFIT uses still comes from the
     scalar field (+ Lambda), as in the nl-scf-fix.
  2. input.c closure check: with Omega_scf < 0 (the field takes the closure), an EDE-mode fluid given by 'omega_fld'
     counts as specified (CLASS only accepted 'Omega_fld', which needs h before the theta_s shooting knows it). The fluid's linear
physics (w(a), k-dependent sound speed c_s^2 = k^2/(k^2 + 4 a^2 m^2)) is AxiCLASS's own, unchanged.
Usage: python patch_ula.py <path to a COPY of AxiCLASS_coupled_nlfix>"""
import sys
ROOT = sys.argv[1]
p = f"{ROOT}/external/Halofit/halofit.c"
s = open(p).read()
old = "if (pba->has_scf == _TRUE_ && pba->has_fld == _FALSE_) { /* nl-scf-fix: effective w of field + Lambda */"
new = ("if (pba->has_scf == _TRUE_ && (pba->has_fld == _FALSE_ || pba->ede_parametrization == pheno_axion)) {"
       " /* nl-scf-fix (+ Spiral-L: the pheno_axion fluid is matter, not dark energy) */")
n = s.count(old)
assert n == 1, f"anchor found {n} times"
open(p, "w").write(s.replace(old, new))
print("ok  external/Halofit/halofit.c: HALOFIT w from the scalar field when the fluid is the matter-like axion")

p = f"{ROOT}/source/input.c"
s = open(p).read()
old = ("       /* Test */\n"
       "       class_test((flag1 == _TRUE_) && (flag2 == _TRUE_) && (((flag3 == _FALSE_) && (flag4 == _FALSE_))|| (param3 >= 0.)),")
new = ("       /* Test */\n"
       "       if (flag2 == _FALSE_ && pba->fluid_equation_of_state == EDE && pba->Omega0_fld > 0.) flag2 = _TRUE_; /* Spiral-L: omega_fld given */\n"
       "       class_test((flag1 == _TRUE_) && (flag2 == _TRUE_) && (((flag3 == _FALSE_) && (flag4 == _FALSE_))|| (param3 >= 0.)),")
n = s.count(old)
assert n == 1, f"input.c anchor found {n} times"
open(p, "w").write(s.replace(old, new))
print("ok  source/input.c: omega_fld counts as a specified fluid density for the Omega_scf < 0 closure")
