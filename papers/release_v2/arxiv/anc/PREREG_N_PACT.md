# The module test on new data: is the field width 1/9 of the torsion value on ACT? (written 2026-10-29 16:03 CT, before looking)

Builds on PREREGISTRATION_N.md (unchanged) and the temple map's lesson: resonances close only when every length is a
whole number of one module (0.54 m in the temple; there, closure is exact). For the Twist the candidate module is the
torsion width F_torsion = √(3/2) M_Pl = 1.2247 M_Pl, and the field width would be F = F_torsion / N.

## Prediction fixed now
N = 9, taken from the Planck free fit (8.97, AxiCLASS; disclosed in PREREGISTRATION_N.md). So the width predicted
for data that never shaped it is **F = 1.2247 / 9 = 0.1361 M_Pl**.

## Tests (the ACT-based P-ACT fits were finished at 06:49 and 09:3x; their F has NOT been computed or looked at)
**T1, width on new data.** Compute F from the saved best fits by re-running CAMB at each minimum and reading the
solved decay constant f: `pact_ede` (free) and `pact_edelock` (locked). Implied N = 1.2247 / F.
- **Pass:** N within 9 ± 0.5 for pact_ede.
- **Fail:** N outside 8.0–10.0.
- **In between:** "not decisive".
- Also report the Planck CAMB values (edeP, edelockP) for consistency with the AxiCLASS 8.97.

**T2, the one-setting Twist on new data (only if CAMB exposes F so it can be fixed).** Locked Twist with F fixed at
0.1361 M_Pl (1% constraint, its own χ² removed), on P-ACT. With N fixed from other data and z_c locked, only θ_i is
free: **one** extra setting.
- **Pass:** Δχ² < −2 vs pact_lcdm (ΔAIC < 0), the PREREGISTRATION_ZEQ Twist-1 bar.

## Honest limits
- On Planck, N = 7.7–10.1 all fit within Δχ² = 1, so a T1 pass alone is weak. A clear miss (N ≈ 6 or 12) would be informative.
- N = 9 is not derived from physics. Even a T2 pass shows that "width = torsion / 9" costs nothing on new data; it
  does not explain why 9. That remains Great Work II (instanton charge, crystal symmetry and so on), to be fixed before
  the next data set.
