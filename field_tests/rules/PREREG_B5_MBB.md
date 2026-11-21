# PREREG B5 — neutrinoless double-beta decay: the Weave's m_ββ (test plan B5; Danny 21 Nov "start implementing and testing")
Locked BEFORE computing.
## Inputs (all earlier Weave choices, none new)
- Normal ordering, m₁ = 0 (register node mnu; Σm_ν = 0.0587 eV, D1234).
- Δm²₂₁ = 7.49e-5 eV², Δm²₃₁ = 2.513e-3 eV² (NuFIT 6.0 NO, arXiv:2410.05380) ⇒ m₂ = √Δm²₂₁, m₃ = √Δm²₃₁.
- sin²θ₁₃ = 0.02195 (as in the engine). sin²θ₁₂: the Weave's TM1 value (1−3s₁₃)/(3(1−s₁₃)) = 0.3184 (P), and the measured 0.307 for comparison.
- Majorana neutrinos (seesaw, E15). With m₁ = 0 only ONE relative Majorana phase φ matters; it is free (not predicted) ⇒ the prediction is a band.
## Formula (standard)
m_ββ(φ) = | m₂ s₁₂² c₁₃² + m₃ s₁₃² e^{iφ} |, φ ∈ [0, 2π) ⇒ band [ |m₂s₁₂²c₁₃² − m₃s₁₃²| , m₂s₁₂²c₁₃² + m₃s₁₃² ].
## Prediction and pass/fail (decided now)
- The Weave predicts m_ββ inside the band (expected ≈ 1.4–3.8 meV; the code's numbers are reported as they come).
- Experiments: LEGEND-1000 (3σ discovery reach ≈ 9–21 meV), nEXO (≈ 5–20 meV), KamLAND-Zen (current limit 28–122 meV).
- PASS (for the Weave) = no 0νββ signal in these experiments; FAIL = a confirmed signal implying m_ββ > 2 × (band top), i.e. above ≈ 8 meV, at any NME choice.
- Not counted as strict evidence until a post-lock data release (LEGEND-1000 / nEXO results).
## Code
theory/tests/b5_mbb.py; tool weave_mbb for CubeMind. One run, no reruns.
