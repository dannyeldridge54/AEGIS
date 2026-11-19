# PREREG HELIX — the two lens strands as a double helix: does the base-pairing rule s ↔ 2s − 1 hold on every rung?

Locked 2026-11-19 (10:48 CT) before computing. Danny 10:38 "cosmic DNA … singular waveform"; 10:41 "Mirror it like the DNA helix".
Strands (derived before computing):
  Strand G (gradient / 10D-type): V₀ = (y∂_y ln E_s / s)²  ≈ 1 − D_s·y^{1−2s},  D_s = 2(2s−1)/s · b_s/a_s,
     a_s = 2ζ(2s), b_s = 2√π Γ(s−½)ζ(2s−1)/Γ(s) (E_s = a_s y^s + b_s y^{1−s} + …). The plateau IS the mirror ratio y^{1−s}/y^s of the
     functional-equation pair s ↔ 1 − s.
  Strand R (ratio / 8D-type): V₀ = e/(e + 1), e = λ(E_{s'} − E_{s'}(ρ)) ≈ 1 − y^{−s'}/(2ζ(2s')λ).
  Base pair: s' = 2s − 1 with λ_{s'} = 1/(D_s·2ζ(2s')). Computed now: rung 1 (3/2 ↔ 2): D = 7.2983, λ = 0.063298 (= D1552 ✓);
  rung 2 (5/2 ↔ 4): D = 4.4535, λ = 0.111816; rung 3 (7/2 ↔ 6): D = 3.6898, λ = 0.135477.
Runs (engine F, untilted, T_R 8.94e8, D1 start rule): rung 2 G(5/2) vs R(4); rung 3 G(7/2) vs R(6). (Rung 1 = D1552.)
Rule ("pair holds"): per rung |Δn_s| ≤ 1e-3 and |Δr|/r ≤ 5 % between the two strands.
Expectation stated now: pairs hold on rungs 2 and 3 as on rung 1 (same asymptotics ⇒ same observables); r falls rung by rung
(k = 2, 4, 6 ⇒ r ≈ 4.0e-4, 1.0e-4, ~4.5e-5) — only rung 1 sits in the observed band.
No reruns to chase results; fixes only via PREREG_HELIX_DEVIATIONS.md written first.
