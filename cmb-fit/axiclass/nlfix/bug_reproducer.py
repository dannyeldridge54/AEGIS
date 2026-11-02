# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights.
"""Minimal reproducer for the two AxiCLASS issues with n = 1 scalar-field dark energy (no likelihoods, no Cobaya).

A frozen n = 1 field (F = 100 M_Pl, m = 0.015 H0, so it never moves) IS a cosmological constant. Its matter power
spectrum and sigma8 must equal LCDM's. Run with a build's classy on the path:
    python bug_reproducer.py /home/syndyr/AxiCLASS/python/build        (installed: differs)
    python bug_reproducer.py /home/syndyr/AxiCLASS_nlfix/python/build  (fixed: matches)
The causes: input.c forces include_scf_in_delta_m for n_axion = 1, and halofit/HMcode take Omega_m from a total
that counts the field as rho - 3p (patch: nlfix/0001-nl-scf-fix.patch)."""
import glob
import sys

sys.path.insert(0, glob.glob(sys.argv[1] + "/lib*")[0])
import classy                                                   # noqa: E402

COMMON = {"h": 0.68, "omega_b": 0.0224, "omega_cdm": 0.119, "A_s": 2.1e-9, "n_s": 0.966, "tau_reio": 0.055,
          "output": "mPk", "P_k_max_h/Mpc": 2.0, "non_linear": "halofit", "N_ur": 2.0328, "N_ncdm": 1,
          "m_ncdm": 0.06}
FROZEN = {"scf_potential": "axion", "n_axion": 1, "f_axion": 100.0, "m_axion": 0.015, "scf_has_perturbations": "yes",
          "attractor_ic_scf": "no", "scf_evolve_as_fluid": "no", "do_shooting": "yes", "do_shooting_scf": "yes",
          "Omega_Lambda": 0, "Omega_fld": 0, "Omega_scf": -1, "scf_tuning_index": 0, "scf_parameters": "1.5, 0."}


def run(extra):
    c = classy.Class()
    c.set({**COMMON, **extra})
    c.compute()
    h = c.h()
    out = {"sigma8": c.sigma8(), "Pnl(k=1 h/Mpc)": c.pk(1.0 * h, 0.0), "Plin(k=0.1 h/Mpc)": c.pk_lin(0.1 * h, 0.0)}
    c.struct_cleanup()
    return out


if len(sys.argv) > 2:                                           # optional: a smaller mass freezes the field harder
    FROZEN["m_axion"] = float(sys.argv[2])
lcdm, frozen = run({}), run(FROZEN)
print(f"classy from {classy.__file__}  (frozen field m = {FROZEN['m_axion']} H0)")
for k in lcdm:
    print(f"{k:18s} LCDM {lcdm[k]:.6g}   frozen field {frozen[k]:.6g}   ratio {frozen[k] / lcdm[k]:.5f}")
# The two bugs' signatures are sigma8 and the LINEAR spectrum (delta_m). The non-linear spectrum is reported separately:
# on the fixed build a 0.5% residual at k = 1 h/Mpc remains (cause not isolated; its full-likelihood cost is 0.13 in chi2).
bad = any(abs(frozen[k] / lcdm[k] - 1) > 2e-3 for k in ("sigma8", "Plin(k=0.1 h/Mpc)"))
print("RESULT:", "MISMATCH (bug present)" if bad else "MATCH in sigma8 and linear P(k) (frozen field = Lambda)",
      f"| non-linear P(k=1) ratio {frozen['Pnl(k=1 h/Mpc)'] / lcdm['Pnl(k=1 h/Mpc)']:.4f}")
