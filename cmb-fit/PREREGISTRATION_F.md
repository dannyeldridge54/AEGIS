# Pre-registered test: is the field range F fixed by the torsion physics? (written before running, 2026-10-26 15:25 CDT)

Hypothesis. The canonical torsion field is phi = sqrt(3/2) M_Pl arsinh(1/gamma) (paper Eq. canonical). If the
non-perturbative potential is periodic in the natural torsion variable arsinh(1/gamma) with period 2 pi, then
F = sqrt(3/2) M_Pl = 1.2247 M_Pl (reduced Planck mass). This is a hypothesis for the potential's origin, not a derivation.

Test. Planck 2018 + DESI DR2 + Pantheon+ (no SH0ES), torsion EDE with F held at 1.2247 M_Pl (tight constraint on the
derived F), all else free. Compare chi2_eff with LCDM and with free-F EDE.

Decision rule (fixed now):
* If chi2_eff(F fixed) <= chi2_eff(free F) + 2, the theory-fixed version is as good as the free one and has one fewer
  free parameter: report Delta AIC with 2 extra parameters instead of 3.
* If it is worse by more than 2 but still better than LCDM, report it as allowed but disfavoured relative to free F.
* If it is worse than LCDM, the hypothesis F = sqrt(3/2) M_Pl is rejected by the data; report that plainly.
For reference, the free fit gives F = 0.137 M_Pl, so the data may well reject this hypothesis.
