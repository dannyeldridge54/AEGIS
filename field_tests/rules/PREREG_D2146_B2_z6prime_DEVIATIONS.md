# D2146 DEVIATIONS
## DEV-1 (2026-11-22 ~19:55 CT). Control 2 first run: a, b PASS; c, d, e mismatched. Written before the rerun
- **c: the exceptional part matches up to one global sign.** The bulk is correct. This is a representative-orientation ambiguity: flipping (n₂, m₂) → −(n₂, m₂) together with (n₃, m₃) → −(n₃, m₃) leaves the bulk unchanged and flips the exceptional part, which is equivalent to τ₀ → τ₀ + 1.
  - **Resolution:** the generator treats τ₀ as defined for the **published representative's orientation**. If the paper's (n₂, m₂) and ours differ by that flip, the sign is absorbed into τ₀.
  - **Test:** c must match with τ₀ → 1 − τ₀ and nothing else changed.
- **d and e: the bulk mismatches.** Appendix D.1 lists (1, −1; 1, −2; 0, 1), which gives (P, Q, U, V) = (0, 0, −1, −1). Table 13 gives (0, 0, 3, −3).
  - **Hypothesis:** an m₁ sign typo in Appendix D.1. The wrapping (1, 1; 1, −2; 0, 1) gives exactly (0, 0, 3, −3), as worked by hand.
  - **Test:** with that wrapping and the published σ and τ, d and e must reproduce Table 13 in full (bulk and exceptional), and both must be SUSY at ϱ = 1/2.
  - **If either fails, STOP.**
- **No other change.** Tables 1 and 2 and the sign ordering stay as locked.
