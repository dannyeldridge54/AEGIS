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
