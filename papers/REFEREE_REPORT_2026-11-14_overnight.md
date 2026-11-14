# Referee report on the overnight work (D313–D322 and G2_HOME_PROPOSAL.md), 14 Nov 2026, 06:10 CT

Scope: the G₂ home proposal and its addenda, and D317–D322. The v5 paper itself was refereed on 13 Nov.

## Major

**M1. The shield fails at one loop in the G₂ block split (affects D312, D322, the proposal's §2 and "What is not shown").**
The proposal makes the tree-level coupling x-independent: f_SM has no T₂ component. But the overall volume V_X contains T₂, so M₁₁/M_P ∝ V_X^{−1/2}
slides with x (d ln M₁₁/d ln x = −1/2). The SM is matched at the local scale ∝ M₁₁, and its low-energy couplings run from there. Meanwhile
D292 makes the SUSY-breaking (soft) scale x-independent in Planck units. The ratio M₁₁/m_soft therefore moves, and
d(1/α_em)/d ln x = (b_em/2π)(1/2) ≈ 0.95 for MSSM b_em = 12, i.e. **d ln α_em/d ln x ≈ 7×10⁻³** (estimate). That is the same size as the
soft-drift effect D289 found to be ~4×10⁵ times over the clock bound. Equivalently, in the Kaplunovsky–Louis formula the Kähler-anomaly and
matter-metric terms do not cancel: with Z = κ/V_X and K ⊃ −3 ln V_X, the coefficient is (ΣT_r/3 − 3T_G)K, which works out to −b_a ln t₂ per gauge factor (corrected in D324; an earlier draft said −7K).
- D322's statement "the SM coupling gets no x-dependence from thresholds at one loop" is wrong. The Ray–Singer torsion is only the local part
  of the threshold.
- The bullet "Varying M₁₁/M_P affects only heavy states" is wrong. Heavy thresholds feed into light couplings logarithmically.
- Making soft masses scale with M₁₁ instead does not help: then every SM mass scales as M_P x^{−1/2}, which is the type IIB β_m problem
  again (G m_p² ∝ x^{−1}).
**Required:** state that the block split removes the tree-level problem but not the one-loop one. Gap 2 stays HIGH, with no candidate
mechanism. Question 12 should ask how the one-loop volume dependence is removed, not only whether the couplings are independent at tree level.

**M2. The two directions orthogonal to T₂ inside the rolling block are not stabilised.** A three-modulus block with Σa = 1 reduces to one
field T₂ only along its diagonal. The ABKKV condensates sit on T₁-only cycles, so the two non-diagonal directions inside the rolling block are
flat. Either they are light (a new fifth force, plus isocurvature), or something stabilises them, which then risks coupling to T₂.

**M3. A W = 0 supersymmetric Minkowski minimum for the fixed block is a tuning.** Two condensates can give W = ∂W = 0 only for tuned
prefactors (the Kallosh–Linde racetrack). It should be listed as a tuning in the proposal and as an assumption, alongside the cosmological
constant.

## Minor

- m1 (D317): the LHAASO number quoted (6.3×10²⁸ s) is at 10⁷ GeV. Limits at 10⁵ GeV are weaker, so "only ~100 TeV survives" may be too strong.
  D242's anchor (10²⁴ s at 10⁶ GeV for ξ ~ 1) was itself a reading of plots. Label D317 an order-of-magnitude estimate, with the 10⁵ GeV limit
  to be read off properly.
- m2 (D319/D322): "n becomes a finite computable set" holds only if the hidden groups sit on lens-space cycles with known Wilson lines. Say so.
- m3 (D320): the lock and its stated m_σ limitation are fine. The result must be scored exactly as locked.
- m4 (D321): fine. The point that smooth TCS manifolds lack ADE loci is correct and important.
- m5 (D318): fine. Consider adding that a gauged Z₂ is the default expectation in string constructions, which makes "stable DM" the default.

## Verdict
The overnight dark-matter and n notes are sound with small labelling fixes. The G₂ proposal's central claim is overstated: it solves the
shield only at tree level, and the one-loop sliding of M₁₁/M_P reproduces the D289-sized drift. Gap 9 stays "proposal", and gap 2 goes back
to "HIGH, no candidate mechanism" until M1 is answered.
