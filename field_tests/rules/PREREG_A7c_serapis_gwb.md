# PREREG A7c (track X, AEGIS application; manual Djl 17 Nov 05:35 CT): SERAPIS inflationary GW background through each branch's reheating history (written before running)
Code: tools/janus_astro/gwb.py as committed with this lock (never run before it).
Histories (from the notes): τ = i (D727, D730): inflation → octic oscillation w = 3/5 (ρ_x/ρ_end = 3.4e-6 / 4.5e-6) → matter (w = 0) from ρ_x = 3 M_P² H_x² (H_x = 8.4e9 / 1.0e10 GeV) to T_R = 1e6 / 3e6 GeV → radiation; r = 4.63e-4 / 5.12e-4 (ε = 1.3 / 1.6e-4). SERAPIS-E at ρ (D725): matter from ρ_end = V*/2.27 (V* = (3π²/2) A_s r M_P⁴, D979 ratio) to T_R = 3.2e8 / 3.0e9 GeV; r = 4.70e-4 / 4.61e-4. g* = 106.75 at entry; A_s = 2.1e-9; n_t = −r/8.
Validation tests (route A = piecewise power law, route B = numerical mode evolution):
C1 radiation plateau (route B, pure radiation history), 5 modes k/k_R ∈ [1e-3, 1e-1]: T² = 1 within 1e-3.
C2 slopes (route B): local d ln T²/d ln k at the logarithmic centre of each band, at least one decade from both knees: matter band −2 ± 0.05; octic band 4/7 ± 0.05.
C3 route A vs route B at those band centres: |log10 T²_A − log10 T²_B| ≤ 0.5 (route A ignores the O(1) knee coefficients; stated).
C4 f_R(T_R = 1e8 GeV, g* = 106.75) vs the standard ≈ 2.65 Hz: relative ≤ 3e-2.
Pass C1–C4 → A7c VALIDATED.
Application [computed, then compared]: Ω_GW h² at f = 1e-9, 1e-3, 1e-1, 1, 10, 100, 1e3 Hz for each case (route B), the plateau value, f_R, the end frequency, and the stiff-phase peak if any. Comparison with detectors is reported against order-of-magnitude power-law sensitivities (LISA ~1e-13, BBO/DECIGO ~1e-17–1e-16, ET ~1e-12; D710 used the same orders), not scored.
Caveats stated now: the ρ branch's later heavy-N matter era (D780–D783, T₂ ≳ 1e5–1e6 GeV) is not included (it would add suppression above f(T₂)); g* steps (QCD, e⁺e⁻) are not modelled; first-order tensor spectrum only.
Script theory/janus_astro/a7c_check.py; output field_tests/results/janus_astro_a7c.txt. No reruns to chase; DEVIATIONS first.
