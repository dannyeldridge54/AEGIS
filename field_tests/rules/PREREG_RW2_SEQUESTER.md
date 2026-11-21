# PREREG_RW2_SEQUESTER — is a reverse thread living on the dark D7 cycle sequestered from α drift?
Locked 21 Nov 2026 before computing. AI-assisted. Script: theory/tests/rw2_sequester.py (uses tools/weave_cm/weave_reverse.py).
Result file: field_tests/results/rw2_sequester.json.

## Hypothesis under test
H-RW2: the thread φ is the saxion Re T_dark of the unfluxed dark D7 cycle (f_dark = T_dark), while
f_vis = T_vis + 9S contains no T_dark at tree level ⇒ "structurally sequestered".
Bound: ζ ≡ |d ln α_em / dφ| (φ canonical, M_P = 1) < 1.66e-6 (MICROSCOPE, D819). Also reported against the
combined Martins et al. bound 5.9e-8 (report only, not the verdict).

## Inputs (fixed now)
𝒱 = 1.0e5, Re T_vis = 20.15, σ_d ≡ Re T_dark = 38.6 (D1793), α_em = 1/137.036, MSSM content above m_soft,
SM below. Swiss-cheese Kähler potential K = −2 ln(τ_b^{3/2} − τ_vis^{3/2} − τ_d^{3/2}) (dark and visible are
diagonal, non-intersecting local cycles), τ_b set by 𝒱. m₃/₂ = 2.5e5 GeV, H₀ = 1.44e-42 GeV.

## Channels (each computed; leading one decides)
- C1 tree: ∂f_vis/∂T_dark = 0 ⇒ 0.
- C2 one-loop Kaplunovsky–Louis + local matter metrics Z ∝ e^{K/3}: 16π² δ(1/g_a²) = (b_a/3) δK
  (reproduces the in-repo D400 coefficient d ln α_em/d ln x = 6.97e-3 for K = −3 ln x, i.e.
  |d ln α_em/dK| = α_em·b_em/(12π), b_em = 12). δK/δφ for moving τ_d alone (τ_b, τ_vis held, KKLT-style):
  δK/δφ = K_d / √(K_dd/2) from the swiss-cheese K.
- C3 soft thresholds m_soft ∝ m₃/₂ ∝ e^{K/2}: d(α_em⁻¹)/dK = −Δb_em/(4π), Δb_em = 25/3. Reported as a variant
  (C2+C3 combined, and C2 with Z moduli-independent, c_em = 16), giving a range for |d ln α/dK|.
- C4 adiabatic shift of heavy visible moduli (τ_vis, S) driven by the thread's own potential:
  ζ_C4 ~ α_em·|∂α⁻¹/∂τ_vis|·(ρ_Λ/(m_heavy² M_P²)), m_heavy = m₃/₂ (order of magnitude).
- C5 kinetic mixing T_vis–T_dark: admixture of τ_vis in the light eigenvector ~ (m_φ²/m_heavy²)·G_vd/G_vv,
  with m_φ = H₀ (order of magnitude).
- C6 N=2 annulus thresholds between visible and dark stacks: zero if intersection numbers vanish
  (non-intersecting), else O(b_ab/4π) per unit δ ln t. Recorded as a literature condition, not computed.
- C7 (report only) the fixed-𝒱 direction: δK = 0 along the light direction if the heavy potential fixes 𝒱.
- Also report: the 𝒱 that would make C2 pass at σ_d = 38.6, and the K = −3 ln (single-modulus) value
  δK/δφ = √6 for comparison with D1793's convention.
- Consistency side-check (report only): the uplifted KKLT vacuum V ⊃ −e^K|W₀|²(…) gives τ_d a slope
  ~ m₃/₂²·|δK/δφ|; report its ratio to the thread's own slope ~ ρ_Λ·β (β = 2√2).

## Verdict rule (primary = H-RW2 as stated: thread = τ_d, KKLT-style, C1–C5 at the inputs above)
- PASS if the largest of C1–C5 (using the LOWER end of the C2/C3 range) is < 1.66e-6.
- TENSION if it is between 1.66e-6 and 1.66e-5 (within ×10).
- FAIL if it is ≥ 1.66e-5.
C6/C7 do not change the verdict; they are reported as the conditions for a sequestered alternative.
No threshold will be loosened; a script bug needs a DEVIATIONS file before any rerun.
