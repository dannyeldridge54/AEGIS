# FP (Fingerprint) deviations, 7 November 2026 (append-only)

Rule: `PREREGISTRATION_SINH.md`, locked 26 Oct 2026 16:10 CDT. **The rule is unchanged.** What changed and why:

1. **Code re-implemented.** The original `axion_sinh_x0` AxiCLASS option was never committed. `patch_sinh.py` re-adds
   it from the rule's own formula (V, dV, ddV for g(d) = s[sinh(d/s + x₀) − sinh x₀]/cosh x₀, s = √(3/2),
   x₀ = 2.1445), on the pinned base build (PoulinV/AxiCLASS ae9609e). The rule's regression requirement is enforced by
   `regress_sinh.py`: with the option off the build must match the base to every printed digit, or no fit runs.
2. **Same-engine reference.** The rule compares with "the plain-cosine torsion fit (χ²_eff 2427.80)". That fit is the
   26 Oct AxiCLASS polish run (H₀ 70.60, f_EDE 0.078), which was later found unconverged and withdrawn (MODEL_v2.md,
   28 Oct). Comparing a new converged fit with it would not be fair, so `fp_fit.py` refits the plain cosine with the
   identical driver, data, priors and best-of-4 (`fp_cosine`) and the verdict uses that difference. The difference to
   the locked number 2427.80 is reported beside it.
3. **Meaning since 7 Nov.** With the Nieh–Yan coupling adopted (`theory/COUPLING_CHOICE_NIEH_YAN.md`), the plain
   cosine is the Twist's prediction and the Fingerprint is the Holst alternative. The locked thresholds (±2) are used
   as written; the coupling reading is reported, not a new rule.
