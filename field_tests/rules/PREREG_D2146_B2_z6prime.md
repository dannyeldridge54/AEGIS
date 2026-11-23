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
