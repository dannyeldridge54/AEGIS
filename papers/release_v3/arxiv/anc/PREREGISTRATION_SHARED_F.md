# Pre-registration: one decay constant for both roles (the shared-F test)

**Written:** 2026-11-01 07:34 CT (time from the clock). The Late Twist rerun was still in progress, and
`cmp_ax_spa_latetwist.json` did not exist.

**Locking:** SHA-256 hashed and committed when written; never edited afterwards.

## What is already known (disclosed)

- **Early F (input, already computed):** the early field's decay constant at the A3 early-plus-late best fit, as solved
  by AxiCLASS shooting (`axiclass/early_F.py` → `results/earlyF_ax_spa_edelock_w0wa.json`):
  **F_early = 0.1451 M_Pl** (m = 2.96 × 10⁵ H₀).
- **The Late Twist probe (not blind on F_late):** the diagnostic grid behind the minimiser-guard deviation
  (`axiclass/probe_latetwist.py`) showed finite likelihoods near log10 F = 0 to +0.4 and none at log10 F ≤ −0.6 for the
  masses tried. So I already expected F_late ≈ 1 M_Pl, about 7 × F_early, before writing this.
  - This test is therefore **not blind on F_late**. Its value is that the rule is fixed before the exact number exists,
    and that it is stated honestly.

## Idea

The Barbero–Immirzi construction gives the field a Planck-scale range. If one torsion-born field type plays both roles
(early energy, then late dark energy), the simplest torsion-specific statement is that **both potentials share one
decay constant F**: one "twist length", set by gravity. A generic two-axion model has no reason for that. The masses
must differ hugely (about 10⁵ H₀ against about 1 H₀), so this does not claim a single field does both jobs. It only
says the two share a decay constant.

## Rule

**R = log10(F_late / F_early):**
- F_late is the Late Twist best fit (`ax_spa_latetwist`, the official Pantheon+ run);
- F_early = 0.1451 M_Pl, as above.

| Outcome | Rule |
|---|---|
| **SHARED** | \|R\| ≤ 0.30 (within a factor of 2) |
| **DIFFERENT** | \|R\| > 0.48 (more than a factor of 3) |
| **UNCLEAR** | anything in between |

Also reported: the same ratio with the DES Y5 Late Twist run (R2), and with F_early from the early-only fit
(`ax_spa_edelock`) if it is computed.

**Only if the Late Twist passes L1:** a SHARED result would be the first evidence for something torsion-specific.
- Even then, it would be a hint for a joint fit with F tied across both roles, pre-registered separately, not a
  detection.
- A DIFFERENT result says the two roles need different scales. The torsion construction then fixes neither.

**Expectation, written in advance:** from the probe, **DIFFERENT** is the likely outcome (ratio about 7). This test is
reported whatever it shows.
