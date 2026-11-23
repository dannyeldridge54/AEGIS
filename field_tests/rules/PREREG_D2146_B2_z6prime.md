# PREREG D2146: B2, families from intersections on IIA T⁶/Z₆′ (= the Weave's Z6-II); plan lock after ping-pong round 1
Locked before any build. Referee items R-B2-1…5 are folded in.

## Facts settled in round 1
- **Twist.** Z₆′ = (1, 2, −3)/6 = (1/6, 1/3, −1/2) is the Weave's Z6-II (referee confirmed).
- **Tori.** T₁ and T₂ are SU(3) lattices with fixed complex structure, so the Weave's "frozen at ρ" is automatic. T₃ has only a Z₂ action.
- **No discrete torsion.** A single Z₆′ has none.

## Plan
1. **New builder, tools/seed/z6p.py.** It is written from the Gmeiner–Honecker / Honecker–Ott Z₆′ formulas:
   - the bulk 3-cycle lattice;
   - the θ³ Z₂ sector with fixed points on T₁ × T₃;
   - the lattice orientations (A/B);
   - the O6 planes;
   - bulk and exceptional tadpoles;
   - intersection numbers.

   Only the generic parts of z2z6p.py are reused (R-B2-1). **The transcription rules are locked before any run** (readings and sign conventions), as in D2110. A z₀-type ambiguity is expected and will be resolved by the control.
2. **Positive control.** Reproduce one published MSSM-like or PS model from 0708.2285 / 0806.3039: tadpoles = 0 and the published chiral spectrum. No scan runs until the control passes.
3. **Scan for B2 candidates.** Every candidate is reported against all of these filters:
   - 3 families from I_ab (no flux);
   - tadpoles and K-theory probes (as D2117);
   - massless U(1)s and the Green–Schwarz rank (hypercharge must stay massless);
   - no chiral exotics;
   - **the hidden massless-state count**: ΔN_eff ≤ 0.14, at most 2 light hidden Weyl fermions (N1).
4. **N4-seq is OPEN.** The classified D6 models carry no SUSY-breaking sector (R-B2-4). The only reading reported is the geometric separation of τ_q's cycle from the hidden stacks, labelled "necessary, not sufficient".

## Cost clause (R-B2-2), pre-registered
A B2 model is a **different brane content** from UFE v4's |M| = 9 flux model. These scored items were derived with the flux model, so they **must be re-derived in any B2 model and may move**: Koide, TM1/δ_CP, the quark ladder fit, the proton lifetime, and n_s and r if the moduli assignments change. Any item that moves is reported as **moved**, never silently kept.

## Verdict rules
- **N16 CLOSED** only if a model passes step 3 in full.
- **"B2 viable, cost pending"** if it passes the tadpoles but the scored items have not yet been re-derived.
- **NULL** if no model passes.

## ADDENDUM 1: transcription rules, locked before the builder runs (2026-11-22 ~21:25 CT)
**Source.** arXiv e-print 0708.2285 (TeX source `z6prime.tex`). Downloaded with Danny's OK through his browser. The tar's SHA-256 is 631a85bb…3666. The 0806.3039 source is also held (SHA-256 911c323e…72b0).

**Rules taken from the paper:**
- **Fractional cycle.** Π = ½(P ρ₁ + Q ρ₂ + U ρ₃ + V ρ₄) + ½ Σᵢ (dᵢ δᵢ + eᵢ δ̃ᵢ).
- **Bulk intersections.** ρ₁∘ρ₂ = ρ₃∘ρ₄ = 0, ρ₂∘ρ₃ = ρ₁∘ρ₄ = 2, ρ₁∘ρ₃ = ρ₂∘ρ₄ = 4, antisymmetric.
- **Exceptional intersections.** δᵢ∘δ̃ⱼ = −2δᵢⱼ, all others 0.
- **ΩR images** for the lattice of the control, ABa (b = 0):
  - bulk: ρ₁ → ρ₂, ρ₂ → ρ₁, ρ₃ → −ρ₄, ρ₄ → −ρ₃;
  - exceptional (Table 5): δᵢ → −δ̃ᵢ and δ̃ᵢ → −δᵢ.
- **Π_O6** for ABa = (ρ₁ + ρ₂) + 3(ρ₃ − ρ₄). This is the sum of both O6 orbits from Table 4, with multiplicity 1 − b = 1.
- **Tadpoles.** Σ N(Π + Π′) = 4 Π_O6, bulk and exceptional.
- **Chirality** (Table 6):
  - Anti = ½(Π∘Π′ + Π∘Π_O6);
  - Sym = ½(Π∘Π′ − Π∘Π_O6);
  - (N_a, N̄_b) = Π_a∘Π_b;
  - (N_a, N_b) = Π_a∘Π_b′.

**Control.** The SM example (Table 13, ABa, ϱ = 1/2; stacks a…e with N = 3, 2, 1, 1, 1) must give:
- tadpoles = 0;
- the published chiral table: a: (Anti, Sym, ·b, ·c, ·d, ·e, ·b′, ·c′, ·d′, ·e′) = (0, 0, 0, −3, 0, 0, 3, −3, 0, 0); b: ·c = −9, ·d = 6, ·c′ = −9, ·d′ = 3; c: ·d = −3, ·d′ = 3; all other entries 0.

**Sign rule.** A mismatch that is only a global sign of the bulk-vs-exceptional term (the paper's footnote) may be resolved ONCE and recorded here. Any other mismatch is a STOP.

## ADDENDUM 2 (referee R-B2-6…9), written before any scan
- **R-B2-6: filter order.**
  1. Tadpoles + SUSY + K-theory.
  2. The GS rank: Y must stay massless, and every hidden U(1) is classified as massive or massless.
  3. Zero chiral exotics.

  **ΔN_eff is a reported dial, not a filter.** It has three readings:
  - (i) everything massless and thermal;
  - (ii) non-chiral pairs and singlets lifted;
  - (iii) τ_q-diluted, which needs Br(τ_q → hidden).

  Both bounds are used: free-streaming 0.14, and the fluid bound per R36-1. A model is rejected on ΔN_eff only under reading (ii) with no dilution.
- **R-B2-7: the Z₃ sector.** 0708.2285 §2.2.3 says it works on the sublattice of bulk plus Z₂-exceptional cycles, because only those "have a known interpretation in terms of partition functions" [bbkl02]. That is a **stated assumption inherited from the paper, not a proof** that Z₃-twisted tadpoles vanish. It is kept as an assumption and flagged. A Z₃-sector tadpole check is added as an open lock item.
- **R-B2-8: scope.**
  - The lattice is fixed at ABa and ϱ at the published value.
  - Candidates come from our own generator. The 1.3e7 count is a statistic, not a list.
  - Our statistics are reported against theirs as a second control.
- **R-B2-9: dials reported for every surviving model:**
  - the Yukawa texture (which three-point couplings exist);
  - the hidden-gauge β-coefficients (a possible gaugino condensate, relevant to N4-seq);
  - the overlap between the hidden cycle and τ_q's cycle;
  - the discrete Z_n remnants that govern proton safety.
- **Generator rule (from §2.2.3 and Tables 1 and 2):**
  - **Fixed points.** The bulk representative is chosen with (n₁, m₁) = (odd, odd); θ rotates any cycle there. The four fixed points come from Table 2 given σ and the parities of (n₃, m₃), listed as d_{i₁j₁}, d_{i₁j₂}, d_{i₂j₁}, d_{i₂j₂}. Point 1 on T₁ is θ-invariant and drops out of the orbit.
  - **Exceptional cycle.** Π^Z₂ = (−1)^τ₀ [d_{i₁j₁} + (−1)^τ₁ d_{i₂j₁} + (−1)^τ₃ d_{i₁j₂} + (−1)^{τ₁+τ₃} d_{i₂j₂}] ⊗ (n₂π₃ + m₂π₄), with the orbits from Table 1.
  - **Hand checks (pre-run):** branes a and b of the published example reproduce their (d, e).
  - **Control 2:** all 5 published branes must regenerate their (P, Q, U, V, d, e) from the Appendix D.1 wrapping numbers plus their σ and τ, and satisfy SUSY at ϱ = 1/2: (P − Q)/(2ϱ) = U + V, with Re Z > 0.
