# Rolling moduli move α: a one-loop obstruction to Kähler-modulus quintessence from clocks and MICROSCOPE

**Danny Lee Eldridge** (independent researcher) · Version 2, 16 November 2026 (v1: 14 November 2026, "One-loop gauge-coupling drift rules out modulus quintessence at DESI-preferred dark energy") · AI-assisted (see Acknowledgements)

> **Status (v2).** The central result, a one-loop drift d ln α_em/d ln x = 7.0×10⁻³ (k/3) for a rolling Kähler modulus, stands. This version corrects the MICROSCOPE input (the final 2022 result strengthens the bound about fivefold), adds the combined quasar + clock + MICROSCOPE bound of Martins et al. (required suppression ~10⁵ in ζ), states the assumptions explicitly, reports excesses as ratios rather than σ, and replaces the unconditional "rules out" with a conditional statement. Changes are listed at the end.

## Abstract

DESI DR2 BAO combined with the CMB and type Ia supernovae prefers evolving dark energy (2.8–4.2σ, depending on the supernova sample [1]), with CPL fits w₀ ≈ −0.66 to −0.83. Many
string-motivated explanations use a rolling Kähler modulus and assume that it is minimally coupled to the visible sector. We point out
that, under stated assumptions (a visible MSSM-like sector in the same supergravity, X-independent holomorphic gauge kinetic functions and Yukawas), this assumption fails at one loop in 4d N = 1 supergravity. For a field X with K ⊃ −k ln(X + X̄), the Kaplunovsky–Louis formula
for the physical gauge couplings, together with matter metrics fixed by Yukawa locality, gives 16π² d(1/g_a²)/d ln x = −(k/3) b_a. For
MSSM content this is d ln α_em/d ln x = 7.0×10⁻³ (k/3). We show by linear algebra that no assignment of matter modular weights, with or
without a universal Green–Schwarz term, removes the drift of all three Standard Model couplings while keeping the Yukawa couplings and the
μ term field-independent. Using the field speed implied by the DESI-preferred fits (canonical field, w ≥ −1), the predicted variation is
Δα/α ≈ (3.5–10)×10⁻⁴ at z = 1.15, α̇/α ≈ (1.3–3.3)×10⁻¹³ yr⁻¹ today, and an equivalence-principle violation η ≈ (1–3)×10⁻⁸. These exceed the
1σ uncertainties of ESPRESSO, optical clocks and MICROSCOPE by factors of ~10²–10³, ~10⁶ and ~10⁷ respectively. In terms of the coupling ζ = d ln α/dφ,
the one-loop value must be suppressed by ≳ 2×10³ (MICROSCOPE alone) and by ~10⁵ using the combined bound of Martins et al. [19]. The clock relation also requires
1 + w₀ ≲ 10⁻¹² today for such a modulus, so the obstruction does not depend on the DESI preference itself.
The natural escapes are axionic dark energy, or a visible sector that does not feel the rolling field's Kähler potential at all. This
sharpens the qualitative argument of Choi (1999) into a quantitative statement for the DESI era.

## 1. Introduction

The DESI DR2 BAO measurements, combined with the CMB and supernovae, prefer a time-dependent dark-energy equation of state, at 2.8σ to
4.2σ depending on the supernova sample [1, 2]. A natural theoretical home for evolving dark energy is a slowly rolling scalar, and in
string compactifications the obvious candidates are moduli: volume, dilaton or complex-structure fields with logarithmic Kähler
potentials. Several recent analyses fit DESI with such fields, typically asserting that a minimally coupled field evades fifth-force and
varying-constant bounds [e.g. 3, 4].

It has long been known that this is delicate. Carroll [5] showed that generic couplings of quintessence to F² must be suppressed far
below gravitational strength, and Choi [6] argued that string moduli which set gauge couplings cannot be quintessence, proposing axions
instead. Acharya, Maharana and Muia [7] showed that sequestering of light moduli from the visible sector is never complete in string
theory. What has been missing is a sharp, quantitative statement at the level of the DESI fits: how large is the unavoidable one-loop
coupling, and by how much do current bounds exclude it?

This note gives that statement for the most common case, a field that enters the Kähler potential as K ⊃ −k ln(X + X̄). We assume that the holomorphic gauge kinetic functions and Yukawa couplings do not depend on X (a shift symmetry of Im X forbids
non-linear dependence; a linear dependence is a tree-level coupling, which is far more tightly constrained). The point is
not a tree-level coupling, but the one-loop dependence of the physical gauge couplings on the Kähler potential
itself, which is fixed by anomalies [8, 9].

## 2. The one-loop coupling

**Formula.** In 4d N = 1 supergravity, the physical (canonical) gauge couplings at scale μ obey [8, 10]

16π²/g_a²(μ) = 16π² Re f_a + b_a ln(M_P²/μ²) + c_a K − 2 Σ_r T_a(r) ln det Z_r + 2 T(G_a) ln(1/g_a²) + …,

with b_a = Σ_r T_a(r) − 3T(G_a) and c_a = Σ_r T_a(r) − T(G_a). The c_a K term and the matter-metric term come from the Kähler and
sigma-model anomalies, and their coefficients are fixed (rescaling anomalies, [9]). They cannot be tuned by choosing f_a.

**Locality fixes the matter metrics.** Let K ⊃ −k ln(X + X̄) and Z_r ∝ (X + X̄)^(−n_r). The physical Yukawa coupling is
y = e^(K/2) W_ijk /(Z_i Z_j Z_k)^(1/2) ∝ x^((n_i + n_j + n_k − k)/2), and similarly for μ. Requiring field-independent Yukawas and μ (no drift of
fermion masses or of the electroweak scale) with universal weights gives n_r = k/3. For k ≠ 3 this is imposed by the requirement, not derived
from a string locality argument; for the volume case (k = 3) it agrees with locality (cross-check below). The x-dependent part then combines to

16π² d(1/g_a²)/d ln x = −k c_a + (2k/3) Σ_r T_a(r) = −(k/3) b_a.

For MSSM content, b_a = (33/5, 1, −3) in GUT normalisation, so d(1/α_em)/d ln x = −(k/3)(1 + 11)/(4π) = −0.955 (k/3), and

**d ln α_em / d ln x = 6.97×10⁻³ × (k/3).**

**Cross-check.** Applied to the overall volume of a local D3 model (K̂ = −2 ln 𝒱, locality Z ∝ 𝒱^(−2/3)), the same rule gives
16π² d(1/g_a²)/d ln 𝒱 = −(2/3) b_a, i.e. exactly the b_a ln M_X² with M_X ∝ 𝒱^(−1/3) found by Conlon and Palti [10] from the same formula.
The T(G_a) ln(1/g_a²) term only feeds back the shift at higher order and is dropped.

The shift is a constant offset of 1/α at the matching scale, so it is carried unchanged to low energies by ordinary running. (The
gluon coupling, and hence Λ_QCD and m_p/m_e, also drift; we use α_em only, which is conservative.)

**No escape through weights or a universal Green–Schwarz term.** Allow arbitrary weights n_Q, n_u, n_d, n_L, n_e, n_Hu, n_Hd and a
universal GS shift δ of 16π²/g_a². Requiring zero drift for all three gauge factors, three field-independent Yukawas (up, down, lepton)
and a field-independent μ gives seven unknowns plus δ and seven equations. The system has no solution (exact rational linear algebra,
code in [11]). Dropping the μ condition admits solutions, but all of them have n_Hu + n_Hd = 12, so the physical μ ∝ x^4.5: the
electroweak scale drifts instead. A GS term per gauge factor, with coefficients tuned ∝ b_a, would cancel the drift, but this is a
separate tuning for each factor rather than a mechanism, and the known orientifold examples do not provide it [12].

## 3. How far does a DESI-fitting modulus roll?

For a canonical field φ (M_P = 1) with K ⊃ −k ln(X + X̄), d ln x/dφ = √(2/k). Its speed follows from the equation of state:
(dφ/dN)² = 3 Ω_DE(z)(1 + w(z)), N = ln a. A canonical field cannot cross w = −1, so we clip the CPL fits at w = −1; this
underestimates the excursion relative to the fits. With Ω_m = 0.31:

| CPL fit (CMB + DESI + SNe, [2]) | w₀ | w_a | Δφ since z = 1.15 | today's φ̇ / H₀ |
|---|---|---|---|---|
| PantheonPlus | −0.833 | −0.65 | 0.107 | 0.59 |
| DESY5 | −0.749 | −0.88 | 0.147 | 0.72 |
| Union3 | −0.664 | −1.10 | 0.184 | 0.83 |

Hence ζ ≡ d ln α_em/dφ = 6.97×10⁻³ (k/3) √(2/k) = 3.3×10⁻³ (k = 1), 4.6×10⁻³ (k = 2), 5.7×10⁻³ (k = 3).

## 4. Comparison with bounds

We use three bounds: the ESPRESSO measurement Δα/α = (1.3 ± 1.3_stat ± 0.4_sys) ppm at z = 1.15 [13]; the optical-clock bound
α̇/α = (1.8 ± 2.5)×10⁻¹⁹ yr⁻¹ [14, 15]; and the final MICROSCOPE equivalence-principle result η(Ti, Pt) = (−1.5 ± 2.3_stat ± 1.5_syst)×10⁻¹⁵ [16], converted with
η ≈ 10⁻³ ζ² [17]. (Version 1 used the 2017 first result, (−0.1 ± 1.3)×10⁻¹⁴, under the label of the 2022 paper; the pre-registered run D400 used that
value, and the MICROSCOPE column below is recomputed with the final value as a recorded deviation.) Entries give the predicted value divided by the
1σ uncertainty of each measurement.

| Fit | k | Δα/α (z = 1.15) | ÷ ESPRESSO σ | α̇/α today [yr⁻¹] | ÷ clock σ | η | ÷ MICROSCOPE σ |
|---|---|---|---|---|---|---|---|
| PantheonPlus | 1 | 3.5×10⁻⁴ | 250 | 1.3×10⁻¹³ | 5×10⁵ | 1.1×10⁻⁸ | 4×10⁶ |
| PantheonPlus | 3 | 6.1×10⁻⁴ | 430 | 2.3×10⁻¹³ | 9×10⁵ | 3.2×10⁻⁸ | 1.2×10⁷ |
| DESY5 | 3 | 8.4×10⁻⁴ | 600 | 2.8×10⁻¹³ | 1.1×10⁶ | 3.2×10⁻⁸ | 1.2×10⁷ |
| Union3 | 3 | 1.0×10⁻³ | 750 | 3.3×10⁻¹³ | 1.3×10⁶ | 3.2×10⁻⁸ | 1.2×10⁷ |

(ESPRESSO σ = 1.4 ppm, statistical and systematic in quadrature; MICROSCOPE σ = 2.7×10⁻¹⁵.)

(All nine fit/k combinations are in [11]; every one exceeds every bound.) To be compatible with MICROSCOPE at 1σ requires
ζ ≲ 1.7×10⁻⁶, a suppression of the one-loop coupling by (2.0–3.4)×10³. The combined quasar + clock + MICROSCOPE analysis of
Martins et al. [19] gives ζ = (−3.6 ± 5.9)×10⁻⁸, so the one-loop value ζ = (3.3–5.7)×10⁻³ must be suppressed by (0.6–1.0)×10⁵. The clock bound requires ζ φ̇ ≲ 2.5×10⁻¹⁹ yr⁻¹, i.e. a suppression of ~10⁶ at
the DESI-preferred field speed.

**A one-line null test.** The two arms of the comparison can be combined into a ratio from which the field's history cancels:
R ≡ (α̇/α) / [H₀ √(3 Ω_DE (1 + w₀))], which must equal ζ = 6.97×10⁻³ (k/3) √(2/k) for any rolling modulus of this kind. With the clock
bound and the PantheonPlus w₀, R = (4.4 ± 6.2)×10⁻⁹, against ζ = (3.3–5.7)×10⁻³, which exceeds R's 1σ range by a factor ~5×10⁵. Any future w₀ > −1 measurement can be
checked against clocks in the same way, without modelling the field. Read the other way, the clock bound with R = ζ requires
1 + w₀ ≲ (2–6)×10⁻¹³ today for k = 1–3 (Ω_DE = 0.69). The obstruction therefore does not depend on the DESI preference: any observable
thawing of such a modulus is excluded, under the assumptions of §2 and §6.

## 5. What survives

- **Axionic dark energy.** A pseudoscalar couples to F F̃, not F², so it does not shift α at linear order, and a shift symmetry forbids a
  long-range scalar force. This is Choi's proposal [6] and is consistent with DESI-era fits [18]. (Its photon coupling instead rotates CMB
  polarisation, a separate test.)
- **A visible sector that does not see the rolling field's e^K.** Our coefficient assumes that the rolling field enters the same Kähler
  potential that multiplies the visible sector. Constructions in which the visible sector is sequestered from that field beyond locality
  could evade it, but sequestering is generically incomplete [7], and the residual must be suppressed by ~10³ (MICROSCOPE) to ~10⁵ (combined bound) in ζ.
- **Per-factor Green–Schwarz couplings ∝ b_a.** Possible in principle, but a tuning for each gauge factor; not realised in the known
  Z₃/Z₇ orientifolds [12].
- **Non-canonical or screened fields.** Screening mechanisms need environmental masses far above H₀ and do not obviously apply to a
  cosmologically rolling modulus; not analysed here.

## 6. Scope and caveats

The result is one-loop, assumes the visible sector is a 4d N = 1 MSSM-like theory in the same supergravity as the rolling field, assumes
X-independent holomorphic gauge kinetic functions and Yukawas, uses universal matter metrics fixed by field-independent Yukawas, and uses α_em only. Threshold effects of heavy states are field-independent if their masses are
set in Planck units by the same locality argument; if they are not, they add further drift. The bounds are 1σ values from single
analyses, and the field excursion is a lower estimate. None of these changes the size of the discrepancy, which is a factor 10³–10⁵ in ζ.

## 7. Conclusion

Under the assumptions of §2 and §6, a modulus with a logarithmic Kähler potential cannot be the evolving dark energy that DESI prefers
unless its one-loop coupling to the visible sector is suppressed by ~10³–10⁵ (in ζ). The suppression is not available from modular weights or a universal Green–Schwarz
term. Evolving dark energy from string theory, if real, points to axions or to sectors that are genuinely sequestered from the visible
Kähler potential.

## Code and data

All numbers come from two short scripts, with their pre-registration (rule written and hashed before running):
theory/alpha_nogo/kl_coeff.py, theory/alpha_nogo/desi_alpha_d400.py, field_tests/rules/PREREG_D400_DESI_ALPHA.md, results in
field_tests/results/. Repository: github.com/dannyeldridge54/AEGIS (branch unify-bg); archived with the Twist project on Zenodo
(concept DOI 10.5281/zenodo.24202420).

## Acknowledgements

This work was carried out with AI assistance (Anthropic's Claude) for literature search, algebra checks, code and drafting; the author is
responsible for its content. It arose while testing an earlier model of the author's; the result does not depend on that model.

## References

[1] DESI Collaboration, DESI DR2 results II: BAO and cosmological constraints, arXiv:2503.14738.
[2] "Robust evidence for dynamical dark energy in light of DESI DR2 and joint ACT, SPT, and Planck data", arXiv:2511.22512.
[3] arXiv:2511.23463 (string-motivated kinetically mixed dark energy; assumes minimal coupling).
[4] Alestas, Caldarola, Ocampo, Nesseris, Tsujikawa, "DESI constraints on two-field quintessence with exponential potentials", arXiv:2510.21627.
[5] S. M. Carroll, "Quintessence and the rest of the world", Phys. Rev. Lett. 81, 3067 (1998), astro-ph/9806099.
[6] K. Choi, "String or M theory axion as a quintessence", Phys. Rev. D 62, 043509 (2000), hep-ph/9902292.
[7] B. S. Acharya, A. Maharana, F. Muia, "Hidden sectors in string theory: kinetic mixings, fifth forces and quintessence", arXiv:1811.10633.
[8] V. Kaplunovsky, J. Louis, "Field dependent gauge couplings in locally supersymmetric effective quantum field theories", Nucl. Phys. B 422, 57 (1994), hep-th/9402005.
[9] N. Arkani-Hamed, H. Murayama, "Holomorphy, rescaling anomalies and exact beta functions in supersymmetric gauge theories", hep-th/9707133.
[10] J. P. Conlon, E. Palti, "Gauge threshold corrections for local string models", arXiv:0901.4350.
[11] This work, code and pre-registration (see Code and data).
[12] Z. Lalak, S. Lavignac, H. P. Nilles, "Target-space duality in heterotic and type I effective Lagrangians", hep-th/9912206.
[13] M. T. Murphy et al., "Fundamental physics with ESPRESSO: precise limit on variations in the fine-structure constant towards the bright quasar HE 0515−4414", A&A 658, A123 (2022).
[14] R. Lange et al., Phys. Rev. Lett. 126, 011102 (2021); N. Filzinger et al., Phys. Rev. Lett. 130, 253001 (2023).
[15] K. A. Bronnikov et al., "The fine structure constant: a review of measurement results and possible space-time variations", arXiv:2506.18328.
[16] P. Touboul et al. (MICROSCOPE), "MICROSCOPE mission: final results of the test of the equivalence principle", Phys. Rev. Lett. 129, 121102 (2022), arXiv:2209.15487.
[17] C. J. A. P. Martins et al., "Fundamental physics with ESPRESSO: constraining a simple parametrisation for varying α", arXiv:2204.02930.
[18] "Testing quintessence axion dark energy with recent cosmological results", arXiv:2504.17638.
[19] C. J. A. P. Martins et al., combined quasar, atomic-clock and MICROSCOPE constraints on the coupling of a varying α, arXiv:2105.09746.
[20] K. Choi, "String or M theory axion as a quintessence" (see [6]); see also moduli quintessence and varying α, hep-ph/0402075.

## Changes from version 1
1. Title: "rules out" replaced by a conditional statement of the obstruction.
2. MICROSCOPE: the final 2022 value replaces the 2017 value, which v1 had quoted under the 2022 citation. The bound on ζ tightens from 3.6×10⁻⁶ to 1.7×10⁻⁶, and the η column is recomputed. The pre-registered run (D400) used the 2017 value; the change is recorded as a deviation (D819).
3. Added the combined bound of [19]: the required suppression rises to ~10⁵.
4. Excesses are reported as ratios to 1σ uncertainties, not as "σ" pulls of 10⁵–10⁷.
5. Assumptions made explicit: X-independent f_a and Yukawas; for k ≠ 3, n_r = k/3 is imposed.
6. Added: the clock relation requires 1 + w₀ ≲ 10⁻¹² today, independent of DESI's preference.
7. DESI DR2 significance quoted as 2.8–4.2σ, from its own abstract.
8. References: added [19] and hep-ph/0402075; the MICROSCOPE reference now gives title and arXiv number.

