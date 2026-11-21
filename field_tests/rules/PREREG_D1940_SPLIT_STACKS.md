# PREREG D1940 — split stacks, the first candidate orthogonal to m₃/₂ (locked 21 Nov 2026 before running; repo at e396c332)
Model: SU(3) on its own 4-cycle T₃ and SU(2) × U(1) on T₂, with the same flux (9S) on both, so there are still 3 families. Each cycle is KKLT-stabilised by its own rank-6 condensate with a shared W₀.
Script: theory/tests/d1940_split_stacks.py.
- Three readings of the needed Re T₃ − Re T₂: bare at a 4.93 TeV gluino; at the wino bound (D1937); and with the post-selected Higgs pair (CONS).
- Convert each to the prefactor ratio A₃/A₂ = exp(2π ΔRe T/N).
**PASS (viable)** if all three ratios lie in [1/3, 3] (A ∈ [0.3, 3], D1811) and m₃/₂ is unchanged, so the wino bound holds. Otherwise FAIL.
**Honest label, fixed in advance:** even a PASS makes α_s a FIT (one ratio chosen) unless A₃/A₂ is derived. With split stacks, proton decay loses its G-branch prediction.
