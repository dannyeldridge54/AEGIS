# PREREG D1972 — layered resonance, centre outwards, 9 layers, 3 sweeps (Danny 17:58; locked 21 Nov 2026 before running; repo at 1ec453e0)
Engine: tools/loom/resonance.py.
**Layers:**
1. torus (rung step);
2. pyramid (neutrinos at i);
3. turnover (leptons at ρ; TRUST);
4. cube (agreement of the three rung readings);
5. fold (wino, against 700 GeV);
6. dilaton (n_s through N*(T_R));
7. forces (α_s single stack, σ = 0.0011 strict; or split stacks as a FIT);
8. cosmology (the gravitino box; leptogenesis at natural p = 2);
9. late universe (TRUST).

**Procedure.** At each layer, all knobs of layers 1..k are re-balanced together by a maximin coordinate search, stopping after 7 null passes (deterministic search, reported as such).
- **LOCK** = all of the layer's margins ≥ 0 in 3 consecutive solver passes.
- **TRUST** layers cannot lock (G-T5).
- Three full sweeps; each sweep starts from the previous one's knobs.

**Reported:** the lock state per layer per sweep, the margins, the knob values, and the **FITS SPENT** (any knob more than 1 % from its derived value, or split stacks switched on; G-T3).

**Labels.** This is a consistency map and is not evidence. A layer that locks only by spending fits is reported as **LOCKED-BY-FIT**.
