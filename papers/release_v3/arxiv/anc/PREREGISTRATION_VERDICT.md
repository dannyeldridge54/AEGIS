# Verdict rule for the Twist fit question (written 2026-10-29 10:09 CT, BEFORE reading the remaining results)

## What was already known when this was written (disclosed)
- Blind P-ACT test: **passed** the PREREGISTRATION_ZEQ rule (Locked Twist Δχ² −7.23, ΔAIC −3.23).
- Fair Planck comparison: Locked Twist vs polished ΛCDM Δχ² −4.70 (ΔAIC −0.70).
- DES-Dovekie supernovae: Locked Twist Δχ² −5.08.
- The z_c profile has closed (best near log z_c 3.55–3.75, +0.38 at 4.05).
- **Not yet read:** the DES Y5 and Union3 swaps, the SH0ES runs, the S8 penalties (PREREG_S8.md) and the hilltop
  runs (PREREG_THETA.md). Their files may exist on disk but have not been opened.

## The rule (about the Locked Twist, `edelock`, 2 extra settings; each comparison is against the best ΛCDM on the same data)
**PREFERRED** (the phenomenology is favoured; this is not proof of torsion) if all of:
1. the blind P-ACT test passes the ZEQ rule (Δχ² < −4) — already met;
2. fair Planck Δχ² < −4 — already met;
3. Δχ² < −2 with **each** of the DES-Dovekie, DES Y5 and Union3 supernova sets;
4. S8 penalty (PREREG_S8.md) < 2 against **both** weak-lensing values A and B.

**TIE** if items 1–2 hold but 3 or 4 fails (the result depends on which supernovae or which lensing survey is right).

**NOISE** if the blind test or the fair Planck test had failed (not the case), or if Δχ² ≥ 0 with any supernova set.

## Reported beside the verdict, never part of it
- SH0ES runs: the pull of the local H0 (not independent evidence).
- The hilltop test (PREREG_THETA.md): it tests the `hold_release` hypothesis, not the fit verdict.
- The pattern-watch tally (lens tier).
- Significance for every Δχ²: p = chi2.sf(−Δχ², k), with σ as a two-sided normal equivalent.

## What any verdict does not change
The torsion-specific prediction (F = √(3/2) M_Pl) failed and stays failed. Even a PREFERRED verdict says only that
"early dark energy switching on at matter–radiation equality" fits better. It does not say that torsion is the
cause. That is Great Work II.
