"""D140: CONSTRUCT a protection against the fifth force and TEST it. AI-assisted, order of magnitude.

Construction ("scaling shield"):
  K = -3 ln(T + Tbar) is invariant (up to a Kahler transformation) under the scaling T -> lambda T (the no-scale symmetry; in string
  language, rescaling the size of the extra dimensions). Put the Standard Model in sequestered / Einstein-frame minimally coupled form,
  so that tree-level SM couplings respect the scaling. Then a coupling of the tail field phi = sqrt(3/2) ln x to the SM can only come
  from things that BREAK the scaling:
   (a) non-perturbative effects ~ q^k = e^{-k pi T/4}  (the SAME instantons that make the cliff; k = 1 is the cliff's own SU(8) factor)
   (b) the single-instanton factor of D118, e^{-2 pi T}
   (c) perturbative corrections ~ c_p / x^p  (string-theory alpha'/loop corrections to no-scale, e.g. p = 3/2 for alpha'^3)
   (d) the superpotential's own breaking (the dark-energy slope) reaches the SM only through gravity: ~ V_tail / M_P^4
  chi (the reheating field) carries no scaling charge, so its Planck-suppressed links to the SM stay allowed (D110) — the asymmetry D135
  asked for now follows from a named symmetry instead of a bare assumption.
Coupling: if a SM mass scale depends on x as m(x) = m0 (1 + eps(x)), then beta = |d ln m / d phi| = |d eps/dx| * x * sqrt(2/3).
Tests: Cassini (universal): beta < 3.4e-3. MICROSCOPE (composition, eta < ~3e-15; for a QCD-scale coupling the material difference is
~1e-3, eta ~ 2 beta^2 1e-3): beta < ~1.2e-6."""
import math
c = math.sqrt(2 / 3); CASS, MICRO = 3.4e-3, 1.2e-6
def beta(deps_dx, x): return abs(deps_dx) * x * c
print(f"tests: Cassini beta < {CASS:.1e}; MICROSCOPE beta < {MICRO:.1e}\n")
for x, lab in ((73.0, "field frozen (late universe)"), (88.9, "today")):
    print(f"x = {x} ({lab}):")
    for k in (1, 2):
        b = beta(-k * math.pi / 4 * math.exp(-k * math.pi * x / 4), x)
        print(f"  (a) instanton breaking q^{k}: beta {b:.1e}  -> {'PASS' if b < MICRO else 'FAIL'} (margin 10^{math.log10(MICRO/b):.0f})")
    b = beta(-2 * math.pi * math.exp(-2 * math.pi * x), x); print(f"  (b) single instanton e^(-2 pi T): beta {b:.1e} -> PASS (margin 10^{math.log10(MICRO/b):.0f})")
    for p in (0.5, 1.0, 1.5, 2.0, 3.0):
        b = beta(-p / x ** (p + 1), x)          # c_p = 1
        cmax_c, cmax_m = CASS / b, MICRO / b
        print(f"  (c) perturbative 1/x^{p} (coefficient 1): beta {b:.1e} -> Cassini {'PASS' if b < CASS else 'FAIL'}, MICROSCOPE "
              f"{'PASS' if b < MICRO else 'FAIL'}; coefficient must be < {cmax_m:.1e} for MICROSCOPE")
    rho, MP = 2.5e-47, 2.435e18
    print(f"  (d) superpotential breaking via gravity: beta ~ V_tail/M_P^4 ~ {rho/MP**4:.0e} -> PASS\n")
