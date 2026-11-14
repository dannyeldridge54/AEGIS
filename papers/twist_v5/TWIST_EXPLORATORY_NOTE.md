# The Twist — exploratory companion note: matter, dark matter, reheating, string embedding and post-data variants

Danny Lee Eldridge (independent researcher) · 13 November 2026 · companion to "The Twist: a no-scale supergravity field for inflation and a thawing dark-energy tail" (version 5)

This note holds the parts of the work that are not settled. Some of its numbers are still changing, and several rest on choices made after data were seen. Nothing here is claimed as a prediction unless a locked rule is named. Symbols and parameter values follow Section 2 of the main paper. Notes labelled D… are in theory/pending_docs/D72_D75_weak_spots.md in the archived repository.

## 1. Matter genesis (exploratory)

### 1.1 The chain

If the angle rolls, it acts as an axial chemical potential μ₅ = c_A v_θ H, using the coupling in Eq. (2) of the main paper. Gauge, Yukawa and strong-sphaleron processes, all fast above 10¹² GeV, pass it to leptons with μ_ℓ/μ₅ = 0.5227. The Weinberg operator, Γ_W = 3T³ Σm_ν²/(4π³v⁴), relaxes lepton number toward

Y_eq = −(45/2π²g*)(μ_ℓ/μ₅)(μ₅/T).

Electroweak sphalerons then convert 28/79 of it into baryons. This is lepto-axiogenesis [1]. Neutrino masses are taken from oscillation data (normal ordering, lightest mass zero). The process freezes out near 2×10¹³ GeV.

**Locked check (MATTER):** a freely rolling angle needs v_θ = 0.022 at T_RH = 10¹³ GeV and 0.0035 at 10¹⁴ GeV. The locked reading is VIABLE.

### 1.2 What sets the angle rolling

A kick from the inflaton's own non-perturbative sector fails. Inflation and today sit at opposite ends of the field range, and the factor e^K ∝ x⁻³ either swamps one end or is far too weak at the cliff. A thermal kick is short by ~10¹⁶⁴.

What works is a separate hidden axion σ. It shares a cosine with the angle at the Nieh–Yan period, with strength ∝ exp(−(π/4) Re T), as from gaugino condensation of a hidden SU(8) with gauge kinetic function f = T [2]. The phase ϑ_k of that cosine sets the sign of the asymmetry, which is therefore not predicted.

**Caveat (D266):** with f = T the hidden coupling is strong at Re T ≲ 1, which is where the kick acts. The condensate formula is therefore used outside calculational control. This is the same problem that removed the hidden-gauge construction of the cliff from the main model.

### 1.3 Numbers and their status

| Quantity | Current value | Status |
|---|---|---|
| Hidden axion mass m_σ for the observed n_B/s = 8.7×10⁻¹¹ | ≈ 6×10¹⁰ GeV | refit after a locked prediction missed: D124 predicted 2–3× observed at m_σ = 6×10⁹ GeV and found 7.53×. A confirmation run is pending |
| Yield scaling | ∝ m_σ^−0.89 | computed (n = 125 cliff) |
| Heat share f_heat | 0.65–0.8% | derived from the reheating field's decay |
| σ's own peak energy share | ~5%, removed by a decay coupling y = 0.1 (entropy dilution 1.2–1.5) | computed |
| Frame | yield computed in the frame the base theory selects; it drops 400× in the other frame | choice |
| Angle-speed normalisation | canonical (main paper, Eq. 2); coupling to ∂(y/x) not computed | choice |

The matter yield is a fit: the one free input m_σ is set by the observed asymmetry. It is not a prediction. Under the adopted construction (TWIST-K) the yield is being recomputed (D160).

### 1.4 Isocurvature (one estimate, unverified)

The hidden axion is light during inflation. Its fluctuations give a baryon isocurvature S_B ≈ 6×10⁻⁶ for a yield sensitivity |d ln Y/d ln σ₀| ≈ 0.64. That is about 8× below the Planck bound (estimate). The angle itself contributes ~10⁻¹⁰.

The estimate assumes the yield is not very sensitive to the starting values. The angle's end point is known to swing widely, so the sensitivity is being measured in a locked run (D137), with a locked limit of 5. Until that run reports, the isocurvature status is **unverified**.

## 2. Reheating

Instant preheating through a reheating field χ, with coupling g ≈ 0.1, gives f_heat ≈ 0.15–1.5% from the model's own inflaton speed (H_end = 5.2×10¹² GeV). The decay chain then gives 0.65–0.8%, so T_RH ≈ 5.5–5.8×10¹⁴ GeV.

Requirements on χ:
- **χ must decay.** That needs χ → −χ to be broken at the Planck scale.
- **Its inflaton-dependent mass must saturate**, W ⊃ (h/2)(1 − e^{−2π(T − T₀)})χ², with h ≈ 0.2–1 and x₀ ≈ 0.02–0.1. Otherwise the field-dependent vacuum energy is 10⁵²–10¹⁰⁸ times today's dark energy. With saturation it falls to ≤ 10⁻⁸⁹ ρ_DE. This needs a single instanton, or an SU(2) condensate with Standard Model loops cut off below ~10¹⁶ GeV.
- With the saturating mass, the loop shift of n_s is negligible.

## 3. Dark matter (conditional)

Dark matter is not the gravitino, not the angle and not σ. The data prefer it uncoupled from the field (β_DM = 0).

A minimally coupled light scalar would be overproduced by inflation by a factor 10²²–10²⁵, so the candidate is a gravity-only fermion. Two sources add:
- freeze-in through graviton exchange [3, 4];
- graviton bremsstrahlung in the decays of χ's fermion partner χ̃ [5].

Bremsstrahlung dominates (≥ 99%) and gives m_DM ≈ 100–500 TeV, provided χ̃ decays to Standard Model fermions. The earlier values (1.4–6.6×10⁶ GeV from freeze-in alone, and 1–6×10⁸ GeV from a kination-only estimate) are superseded. The prediction is null results in direct detection.

## 4. Where the Twist could live in string theory (search result: none found)

The Twist needs three things at once:
- **(A)** the rung-3 Kähler potential;
- **(B)** a source for the cliff;
- **(C)** Standard Model constants independent of T today.

The cases examined (D150–D211, D231–D233):

| Setting | Outcome |
|---|---|
| Type IIB, T = volume | gives A and B, fails C: the volume sets M_s/M_P, so even sequestered D3 matter has β_m ≈ 0.61; a warped throat still gives ≈ 0.4 |
| Type IIB, complex-structure modulus | neutral at tree level; a one-loop Kaluza–Klein leak gives β_m ≈ 0.1–16 |
| Weakly coupled heterotic, Z₃-type orbifold (with a Γ₀(9) duality group, a degree-9 hauptmodul cliff and a BGW-stabilised dilaton with a pure hidden E₈) | gives A and C at weak coupling, but every computed history ends today at strong coupling: g_s ≥ 3 even with 100% reheating, and a matter-neutral volume direction forces g_s ∝ x^{3/2}. The degree-9 version (TWIST-M9, locked) also lowers n_s to 0.957–0.965 |
| Heterotic M-theory | its matter-neutral direction is rung 4 and moves the Standard Model coupling (d ln α_em/dφ ≈ 0.71); TWIST-4 is locked but is not a home |
| Instanton sums for n | the convergent degree-9 genus-0 sum on the quintic gives ~2×10⁻⁴ of the 250 needed; n stays chosen |

**Conclusion.** No setting examined keeps matter neutral at today's field value. The long excursion (~16 M_P) makes some tower light or some coupling strong, which is the distance conjecture at work. The shield remains an effective-theory assumption.

Version 4's TWIST-K statements, that worldsheet instantons "remove the conflict" and give "a precise route to deriving n", are withdrawn.

Structural observation: an integer-power superpotential W = c S Tᵖ gives a plateau only for p = (3α − 1)/2, so only odd rungs work. The Twist's √3 m S T is rung 3.

## 5. Variants built after seeing the n_s data (locked; scored only on future data)

| Model (rule) | Change | n_s | r | Notes |
|---|---|---|---|---|
| TWIST-P (PREREG_TWISTP, _L, D1) | Kähler term b_P/(T + T̄) | 0.965–0.971 | 0.0036–0.011 | rise together |
| TWIST-L (PREREG_TWISTL) | logarithmic factor in S's metric | 0.965–0.979 | 0.0036–0.014 | lower r than TWIST-P at the same n_s |
| TWIST-G− (PREREG_TWISTGN; TWISTG D1 records a sign error) | W = √3 m S T^{1+ε}, ε ≈ −0.0085 | 0.974 | ≈ 0.0068 | loop-sized; full supergravity check passes; a loop whose masses track the inflaton gives such a tilt at first order (literature analogue), but the Twist-specific calculation is not done |
| TWIST-C (PREREG_TWISTC) | W = √3 m S (T + c), c ≈ 3.5×10⁻⁷ | ≈ 0.974 | ≈ 0.005 | c sharply tuned |
| TWIST-M9 (PREREG_TWISTM9) | Γ₀(9) degree-9 cliff | 0.957–0.965 | 0.0038–0.0058 | does not reach the ACT value |

These give distinct (n_s, r) curves that LiteBIRD and CMB-S4 can separate. Their agreement with today's data is not counted as evidence.

## 6. If birefringence is confirmed: TWIST+ALP (PREREG_TWIST_ALP)

The minimal extension adds a spectator axion coupled to photons, with mass 10⁻³²–10⁻²⁸ eV. A coupling times initial angle ≈ 4.5 reproduces β_CMB ≈ 0.3° while carrying ~6×10⁻⁵ of the dark energy.

The ratio of reionization-era to recombination-era rotation is a LiteBIRD signature. It falls from ≈ 1 below 2×10⁻³² eV to ≈ 0 above 10⁻³¹ eV.

The extension sits below a suggested magnetic weak-gravity floor on the axion mass. A domain-wall alternative, with photon coupling ≈ 5, avoids that floor.

## 7. Other costs

| Issue | Status |
|---|---|
| Strong CP | not solved: the angle would overproduce axion dark matter by ~4×10⁵. A separate post-inflation axion of 40–600 μeV would be needed |
| Neutrino masses | assumed; the seesaw scale (6×10¹²–6×10¹⁴ GeV) falls within the model's own scales |
| Quantum stability of the tail | requires T-independent masses above ~6 meV (assumed) |

## References

[1] R. T. Co, N. Fernandez, A. Ghalsasi, L. J. Hall, K. Harigaya, "Lepto-axiogenesis", JHEP 03 (2021) 017, arXiv:2006.05687; R. T. Co, K. Harigaya, "Axiogenesis", Phys. Rev. Lett. 124, 111602 (2020), arXiv:1910.02080; A. G. Cohen, D. B. Kaplan, "Spontaneous baryogenesis", Nucl. Phys. B 308 (1988) 913.
[2] T. Li, Z. Li, D. V. Nanopoulos, arXiv:1407.1819.
[3] M. Garny, M. Sandora, M. S. Sloth, "Planckian interacting massive particles as dark matter", Phys. Rev. Lett. 116, 101302 (2016), arXiv:1511.03278.
[4] S. Cléry, Y. Mambrini, K. A. Olive, S. Verner, arXiv:2112.15214.
[5] Y. Mambrini, K. A. Olive, J. Zheng, "Post-inflationary dark matter bremsstrahlung", JCAP 10 (2022) 055, arXiv:2208.05859.
[6] R. T. Co et al., "Gravitational wave and CMB probes of axion kination", arXiv:2108.09299; C. Chen, S. J. Das, K. Dimopoulos, A. Ghoshal, "Flipped rotating axion non-minimally coupled to gravity: baryogenesis and dark matter", arXiv:2502.08720.
[7] P. Binétruy, M. K. Gaillard, Y.-Y. Wu, "Dilaton stabilization in the context of dynamical supersymmetry breaking through gaugino condensation", Nucl. Phys. B 481 (1996) 109, arXiv:hep-th/9605170.
[8] G. N. Felder, L. Kofman, A. Linde, "Instant preheating", Phys. Rev. D 59, 123523 (1999).
