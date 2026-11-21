# PREREG D1941 — the pulsing Loom over every tension point (Danny 17:12; locked 21 Nov 2026 before running; repo at 1e788d9a)
Script: tools/loom/pulse.py.
**Tension points (log margins):**
- P1: the wino bound.
- P2: the gravitino → wino overclosure box (Ω ∝ T_R M₂^p, three readings of p).
- P3: non-thermal leptogenesis through inflaton → NN. This needs m_φ > 2M_N and Br(φ → NN) ≤ 1 at the Davidson–Ibarra ε; three readings of m_φ.
- P4: the α_s seam through split stacks, A₃/A₂ ∈ [1/3, 3].
**Knobs:** ln m₃/₂ and ln T_R. T_R used as a knob is a postulate; its derived value is 3.7e8.
**Pulse:** all four tension points are evaluated together. A coordinate 3-point triangulation maximises the minimum margin. The run stops after 7 null pulses in a row (state change < 1e-4 and min-margin change < 1e-4). This is a deterministic search and is reported as such.
**PASS:** all four margins > 0 at the final state, with m_φ > 2M_N. Otherwise FAIL, and the failing point is named.
