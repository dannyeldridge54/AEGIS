# V7 — Global significance (look-elsewhere / trials factor) across the whole programme

**Problem.** Many model variants and tests were run (powers n, widths F, starting angles, bracket candidates,
UB-1/1b/2, couplings, SN sets). Local preferences (Δχ² per test) overstate significance unless corrected for the number
of hypotheses tried.

**Already done.** Early Twist only: PREREGISTRATION_LOOK_ELSEWHERE.md → **1.2–1.4σ global** (CLAIMS_INDEX E6,
"WEAK HINT"). Must be stated wherever the early-field Δχ² is quoted.

**To do.**
1. Inventory every hypothesis compared to data since 26 Oct (from the ledger, `field_tests/ledger/ledger.json`, plus
   untracked exploratory fits in `cmb-fit/results/cmp_*`): count distinct model variants per headline claim.
2. For the headline late-time claim (Spiral vs ΛCDM, Δχ² −9 to −13 with 2 extra parameters): local p from the χ²
   distribution with k = 2 (Wilks; note boundary/degeneracy caveats), then global p by (a) Šidák/Bonferroni with the
   inventory count as an upper bound, (b) an effective trials factor from the correlation of the variants' Δχ² (the
   method used for E6).
3. Report local and global σ side by side; never quote local alone.

**Pre-registration.** The counting rule (what counts as a separate hypothesis) must be locked before computing.
**Cost.** Cloud, cheap. **Prep done (8 Nov).** Ledger built (72 verdicts, 50 locked files) as the inventory base.
