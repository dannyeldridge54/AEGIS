# PREREG D320: isocurvature sensitivity under the alternative coupling reading (locked before running)

Locked 14 Nov 2026, ~05:50 CT (cloud). Exploratory check; AI-assisted.

**Run:** theory/review/alt_isocurv_d320.py: the D268 one-pass script (both readings) at m_σ = 5.8×10¹⁰ GeV, decay coupling 0.1, heat 0.8%,
exp cliff 4/π, μ = 1, n = 125, with the hidden axion start s0 = 0.105 (σ₀ × 1.05). Baselines are fixed in advance:
canonical 1.0900×10⁻¹⁰ (D277), alternative 4.8209×10⁻¹¹ (D297).

**Reported:** S_alt ≡ ln(Y_alt(1.05)/4.8209e-11)/ln 1.05. Validation: the canonical number in the same run must reproduce D277's
1.3060×10⁻¹⁰ within 1%; otherwise the run is void.

**Rule (same limit as D137):** |S_alt| ≤ 5 → PASS. Isocurvature margin against S_b < 5.1×10⁻⁵ (D278) at δσ/σ₀ = 10⁻⁵ (f = 0.1 M_P):
margin = 5.1 / S_alt. Stated before running: margin ≥ 1 → isocurvature passes under the alternative reading; < 1 → it fails at f = 0.1 M_P.
The run is at m_σ = 5.8×10¹⁰, not at the alternative fit point 3.0×10¹⁰; this is a stated limitation, not to be fixed by rerunning.
No reruns to chase a result; any fix goes in PREREG_D320_ALT_ISOCURV_DEVIATIONS.md.
