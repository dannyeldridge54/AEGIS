# REVERSE WEAVE — notes (side loop, 21 Nov 2026; D1850 upward)

Scope: carry today's unification results (D1786–D1803) over to the reverse thread (dark energy,
V = V_L(1 − A e^{−βφ}), A = 7.30, published doi:10.5281/zenodo.24380387). Labels: [derived], [computed],
[estimate], [literature], [conjecture]. AI-assisted. Nothing here is published.

## D1850 (RW1, derivation, no lock) — with axion dark energy excluded (D1795), the saxion-type plateau thread is the Weave's only dark-energy carrier left
- [derived, from D1795] An axion with potential height ρ_Λ = 7.1e-121 M_P⁴ and decay constant f has
  m = √ρ_Λ / f. Staying frozen today (m ≲ 3 H₀) needs f ≳ 1.4 M_P/3 ≈ 0.5 M_P; the stricter m ≈ H₀ needs
  f ≈ 1.42 M_P. The dark-cycle axion has f = √3/(2·38.6) M_P = 0.022 M_P ⇒ m = 64 H₀: it oscillates since
  z ~ 15 and is matter, not dark energy. Any axion with f < M_P (the weak-gravity/axion-WGC range, and every
  f = √3/(2σ) with σ > 1) fails the same way. So axion quintessence at sub-Planckian f is excluded for the Weave.
- [derived] What remains: (i) a pure constant Λ (input, D1795), or (ii) a SAXION-type (real, non-periodic)
  field on a plateau, i.e. the reverse thread. Only (ii) gives w ≠ −1, and only (ii) carries the D1692 fit
  (Δχ² ≈ −7 on DESI DR2 BAO + DES-SN5YR with one parameter). The thread is therefore the Weave's dark-energy
  carrier by elimination, not by derivation: its potential height V_L is still an input (I8), as for Λ.
- [derived] Consequences that the next cycles must face:
  1. A saxion is a modulus-like scalar. Unlike an axion it has no shift symmetry, so its couplings to the
     visible gauge kinetic function are not forbidden. The α-drift / equivalence-principle bound
     (ζ < 1.66e-6, D819 MICROSCOPE; 5.9e-8 with the Martins et al. combined bound) therefore applies in full
     (RW2).
  2. It must be light: thawing needs m² = |V''| ≲ few H₀². The dark-cycle saxion of D1793 must be checked
     against this (RW3).
  3. Its plateau shape 1 − A e^{−βφ} needs a microscopic origin with β of order √2 … 2√2 (D1627: all three
     tilts pass DESI DR2) (RW3).
- Status: reverse_thread stays a postulate; this note only removes the alternative.

## D1851 (RW2, locked PREREG_RW2_SEQUESTER + DEVIATIONS D1–D2) — a thread on the dark D7 cycle is NOT sequestered: the one-loop Kähler leak gives ζ ≈ 4e-4, 237× the MICROSCOPE bound (FAIL)
- DEVIATIONS (both written and pushed before any result): D1, finite-difference roundoff in K_dd caught by the
  tool self-test; D2, a factor ½ in D1's formula text. No RW2 number came from the bad code.
- [derived] Tree level is clean (f_vis = T_vis + 9S has no T_dark). But at one loop the visible coupling
  depends on the Kähler potential itself (Kaplunovsky–Louis; with local matter metrics Z ∝ e^{K/3} the
  coefficient is 16π² δ(1/g_a²) = (b_a/3) δK, which reproduces the in-repo D400 coefficient). With
  K = −2 ln 𝒱 and 𝒱 = τ_b^{3/2} − τ_vis^{3/2} − τ_d^{3/2}, moving τ_d moves 𝒱, so δK ≠ 0.
- [computed] At 𝒱 = 1e5, τ_d = 38.6: δK/δφ = 0.169 (≈ √(12 τ_d^{3/2}/𝒱)). |d ln α_em/dK| = 2.32e-3 (KL+Z),
  2.52e-3 (+ soft thresholds m_soft ∝ e^{K/2}), 4.45e-3 (no Z dependence). ⇒ **ζ = 3.9e-4 – 7.5e-4**.
  Adiabatic heavy-moduli shift (C4) 4.9e-97, kinetic mixing (C5) 8.2e-97. Largest (lower end) / bound
  = **237** (6.7e3 against the combined 5.9e-8 bound). Verdict by the lock: **FAIL**.
- [computed, report] D1793's single-modulus convention K = −3 ln: δK/δφ = √6, ζ = 5.7e-3 – 1.1e-2 (worse).
  To pass with a small dark cycle at τ_d = 38.6 would need 𝒱 ≳ 5.6e9 – 2.1e10 (and ≳ 4e12 for the combined
  bound), versus the Weave's 1.0e5 (D1801).
- [computed, consistency] In KKLT the uplifted vacuum depends on τ_d through e^K: the resulting slope along
  τ_d is ~m₃/₂²|δK/δφ| ≈ 9e92 × the thread's own slope ρ_Λβ. So a τ_d that moves 𝒱 cannot be light at all;
  it is held at m ~ m₃/₂ scale. The same quantity δK/δφ makes it both heavy and α-leaking.
- [derived] What would be sequestered (C7): a light direction along which 𝒱, τ_vis and S stay fixed (δK = 0),
  e.g. a fibre-type modulus at fixed volume. Then only C4/C5-size leaks (~1e-96) remain, plus C6: N=2 annulus
  thresholds between the stacks, which vanish if visible and dark D7s have zero intersection numbers.
  [literature, partial read] Conlon–Palti, arXiv:0906.1920: for local models the bulk enters the visible
  gauge running through the KL/winding-scale term, and one-loop holomorphic couplings become non-universal
  through the local twisted (blow-up) moduli; the excerpt read does not address non-intersecting blow-ups,
  so C6 = 0 is an assumption here, not a quoted result.
- Reading: "thread on the dark D7 cycle ⇒ sequestered" is WRONG as a tree-level argument: Kähler mixing
  through the volume leaks. The thread has to be a volume-preserving direction (→ RW3), not τ_dark itself.

## D1850a (correction to D1850, 21 Nov 2026; from the referee of D1790–D1803, relayed by the main session)
- D1850 used the axion decay constant f = √3/(2σ) M_P (from D1793/D1795). For K = −3 ln(T+T̄) with an
  instanton e^{−2πT} the correct value is **f = √(3/2)/(2πσ) M_P**, 4.44× smaller. [computed] At σ = 38.6:
  f = 5.05e-3 M_P, m = **282 H₀** (281 H₀ at σ_Λ = 38.49, the two-loop value with W₀ = 1.4e-8, 𝒱 = 1.0e5).
  The f needed to stay frozen (≈ 1.42 M_P for m = H₀) is unchanged.
- The conclusion of D1850 is unchanged and stronger: an axion with f < M_P cannot be the dark energy, so the
  saxion-type plateau thread is the only dark-energy carrier left. D1850 is kept as written.
- Also noted (main session): the dark modulus at σ ≈ 38.6 is NOT stabilised by KKLT/LVS as used (label C).
  This agrees with D1851's consistency check (a τ_d that moves 𝒱 gets a slope ~9e92 × the thread's).
  D1851 and RW3 use σ_d = 38.6; with 38.49 the RW2 ζ changes by (38.49/38.6)^{3/4} − 1 = −0.2 %, verdict unchanged.

## D1853 (RW6, locked PREREG_RW6_Z2) — the Z₂ at τ = i kills the LINEAR α leak but the quadratic one is still 80× too big (FAIL)
(D1852 is reserved for RW3, still running when this was written.)
- [derived] Near i put u = (τ − i)/(τ + i). S: τ → −1/τ acts as u → −u, so any S-invariant real function of τ
  (the physical one-loop threshold, built from Im τ |η(τ)|⁴) is even in u and its gradient vanishes at i:
  ln α(φ) = ln α_i + (c/2)(φ − φ_i)² + …. This is the mirror of the forward knot SETTING g_s: here the knot
  removes the first-order coupling. The mechanism is real, and it works only AT the knot.
- [computed] Natural c = the D1851 one-loop size per M_P, 3.9e-4 – 7.5e-4.
  - T1 (decides): even with the field exactly at i today (the plan's form, a lower bound since
    (d + Δφ)² − d² ≥ Δφ²), the drift since z* is |Δ ln α| ≥ c·(0.64)²/2 = **8.0e-5**, against ~1e-6:
    **80×** too big (O(1) band 2.4e-5 – 4.6e-4).
  - T2 [estimate]: the knot is still ahead (D1644: reached at a = 1.89). d ≈ √(3(1+w₀)Ω_DE)·ln 1.89 = 0.47 M_P
    ⇒ ζ today = 1.8e-4, **110×** the MICROSCOPE bound. Passing would need d < 4.2e-3 M_P.
  - T3 (report): α̇/α today ≈ 9e-15 /yr, ~9e3× the 1e-18 /yr clock level.
  - Verdict by the lock: **FAIL**.
- Reading: the Z₂ protection helps by a factor ~ Δφ/M_P ~ 0.5. Closing the D1851 gap (×237) needs ~10⁻² –
  10⁻³ more. A Z₂-even leak would fit only if c itself were ≲ 5e-6 per M_P², i.e. the thread's Kähler leak
  were already sequestered, so the knot does not rescue it alone. Row 5 of the mirror table stays ✗.

## D1854 (RW5, locked PREREG_RW5_ZETA5) — the ζ(5) flip: A′ = 4.45 is invisible to background data; the doubled tilt β′ = 4√2 ties with 2√2 (Δχ² = −0.21, TIE)
- [computed, check] A′ = (16/5)(4/3)ζ(4)/ζ(5) = 4.4535; A = (8/3)·2ζ(2)/ζ(3) = 7.2983 (both reproduced).
- R0 [derived + computed]: at leading order φ → φ + c maps A → A e^{−βc} and V_L is shot to H₀, so A and the
  (5/3)² height norm are absorbed. On the D1692 likelihood χ²(A = 4.45) − χ²(A = 7.30) = **−1.5e-8** at the
  same (Ω_m, amp) = (0.3049, 0.1739). Danny's pass rule for A is therefore **UNTESTABLE at leading order**
  (not a fail). A becomes physical only once the field's origin is pinned to the knot (exact curve, D1638),
  which for the ζ(5) copy is not built.
- R1 [computed]: sanity ✓ (β = 2√2 gives χ² = 1638.3155, D1692's value). β′ = 4√2: χ² = 1638.104,
  Ω_m = 0.306, amp = 0.078; Δ = χ²(4√2) − χ²(2√2) = **−0.21** ⇒ verdict **TIE**. Against ΛCDM: −7.22 (4√2)
  vs −7.01 (2√2). For comparison CPL (2 parameters) is −7.21 (D1692).
- Reading: the data cannot tell the forward copy from the ζ(5) flip. The steeper tilt is marginally
  better, but far inside noise, and this is post-data. Row 2 of the mirror table stays "≈ / ?". The decisive
  version needs (a) the exact ζ(5) curve with its knot-fixed origin, so that A′ enters, and (b) future data
  (DR3/Euclid). Both A′ = 4.45 and β′ = 4√2 are now on record before those data.

## D1855 (RW7, locked PREREG_RW7_UPLADDER) — the dark-dimension up-ladder is in HARD CONFLICT with the Weave's scales
- [computed] For R = 1 – 10 μm: m_KK = 0.20 – 0.020 eV and species scale Λ_sp = m_KK^{1/3}M_P^{2/3}
  = 1.05e9 – 4.9e8 GeV (5.7e8 – 2.7e8 GeV with the 2π variant).
  - H_inf/Λ_sp = 5.5e3 – 1.2e4 (C1 fails).
  - M_N(≥ 4.5e10)/Λ_sp = 43 – 92 (C2 fails): the leptogenesis neutrino would sit above the 5D cutoff.
  - T_R/Λ_sp = 0.35 – 0.76 (C3 passes, marginally).
  - Scalars and m₃/₂: ≲ 1e-3 Λ_sp (pass).
  - KK-graviton measure X = (T_R R)T_R/M_P = 2.9e8 – 2.9e9 (C6 fails: overproduction if open at reheating).
  - Verdict by the lock: **HARD CONFLICT** (C1, C2 and C6 each fail at every R).
- Reading: this sharpens D1625 with today's scales. A micron dark dimension can only open AFTER reheating
  and after leptogenesis, which D1625 found needs ≥ 28 e-folds of radion kination. Mirror row 3 stays
  "≈ (direction only)". The ζ(5) codon of D1854 does not need the dimension to be open: it is a D⁴R⁴
  coefficient in 10D, so D1854 is unaffected.
