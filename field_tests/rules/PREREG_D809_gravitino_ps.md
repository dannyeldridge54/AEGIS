# PREREG D809: gravitino → wino with the full Pradler–Steffen yield (accuracy queue item 3; Jl tick 48)
Locked before computing, 2026-11-16.
Replaces the one-term fit Y₃/₂ = 1.9e-12 (T/1e10 GeV) used in D732/D784 with the Pradler–Steffen thermal yield [literature: hep-ph/0612291]:
Y = Σᵢ yᵢ gᵢ²(T)(1 + Mᵢ²/(3m₃/₂²)) ln(kᵢ/gᵢ(T)) (T/1e10 GeV), with y = (0.653, 1.604, 4.276)e-12 and k = (1.266, 1.312, 1.271).
Couplings: one-loop MSSM running from M_Z (α⁻¹ = 59.0, 29.6, 8.5 in GUT normalisation; b = 33/5, 1, −3) [estimate: MSSM running all the way from M_Z, threshold effects ignored].
Gaugino masses from anomaly mediation, M₂ = 0.67–1.85 TeV, gluino 4.7–13 TeV, m₃/₂ = (2.5–7)e5 GeV.
Cases:
(A) τ = i covariant: T_R = 1e6, 3e6.
(B) SERAPIS-E frozen: early T_R = 3e8, 3e9, diluted by T₂/T_R with T₂ = 1e5, 1e6.
(C) SERAPIS-E self-diluted: same early T_R, T₂ = 140, 1100.
(D) K4: Y at 1e10 GeV against the old fit 1.9e-12.
Output: Y₃/₂, Ω_wino^nonth = 2.74e8·M₂·Y (one wino per gravitino; gravitino decays after wino freeze-out, as in D732), and its ratio to the old fit.
Expectation: Y(1e10) within a factor 1.5 of 1.9e-12; Ω_nonth ≪ 0.01 in A, B and C, so the D784 window is unchanged.
Verdict: window unchanged if Ω_nonth < 0.01 everywhere. Any fix goes in DEVIATIONS first.
