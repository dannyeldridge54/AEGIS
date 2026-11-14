# Twist-2: a self-modulating design (draft, 14 Nov 2026, 13:20 CT). AI-assisted.

**Status: design note, not a result.** Nothing here is scored. Each computation listed in §5 gets its own locked rule before it is run.
End view kept: one complex no-scale field T = x + i y drives inflation (Re T) and sets dark energy (the cliff scale and, here, the angle),
with matter genesis and dark matter tied to its scales, and every claim pre-registered.

## 1. What the data point to now (searched 14 Nov 2026)

| Item | Current status | Source |
|---|---|---|
| n_s | CMB alone: ACT 0.9666 ± 0.0076; CMB-SPA 0.9684 ± 0.0030. With DESI BAO in ΛCDM: 0.973–0.977 (P-ACT-LB 0.9741 ± 0.0033). The upward shift is tied to the BAO–CMB tension; nobody has shown whether it survives when that tension is absorbed by late-time physics. | 2507.12459, 2609.19296, 2511.14673 |
| Plateau ceiling | Monomial T-models (α-attractors) cannot exceed n_s = 0.9682 even with stiff reheating. Pole order p gives n_s = 1 − p/((p−1)N); p = 3 gives 0.974 at N ≈ 57. | 2511.14673; 1412.3797 eq. 2.10 |
| Dark energy | Dynamical DE preferred at 2.3σ (PantheonPlus) to 3.9–4.2σ (DESY5); CPL fits prefer a phantom past (Quintom-B), partly a parametrisation effect; DESY5 systematics debated. | 2511.22512 |
| Axion quintessence | Fits DESI+CMB+SNe better than ΛCDM (>2σ); prefers m/H₀ ≳ 1 and F_A ≲ M_P (weakly). With a photon coupling c_γ ~ O(1–20) it reproduces the birefringence angle at ~1σ for DESY5. | 2504.17638 |
| Birefringence | Planck 0.342 ± 0.093°, ACT 0.20 ± 0.08°; naive combination 0.261 ± 0.061°. Absolute calibration still unverified (D330, D386). | 2504.17638, D353 |
| Moduli quintessence | Exponential (two-field) quintessence fits DESI with slopes λ ~ 1; but a rolling Kähler modulus shifts gauge couplings at one loop (our D323), so it fails varying-α bounds unless shielded. | 2510.21627, D323 |

## 2. Design rule: every sector is an attractor or protected by a symmetry

"Self-modulating" here means: each sector's output is fixed by its own dynamics (an attractor, Hubble friction, or a symmetry), not by
an initial condition we tune. Each sector has one dial, fixed by one dataset and tested on a different one. If one sector's bet fails,
it reverts to a nested fallback instead of breaking the others.

## 3. The sectors

**I. Inflation (unchanged end view).** Re T with K = −3 ln(T + T̄): the α = 1 attractor, n_s = 1 − 2/N*, r = 12/N*². N* is set by the
Twist's own post-inflation kination. Without the σ sector (see IV) the shift is +1.48–1.53, so N* = 57.2, n_s = 0.9651, r = 0.0036
(locked D391). The bet: the BAO–CMB tension is resolved by late-time physics (which sector II supplies), so n_s stays near its
CMB-only value. Distances now: ACT alone 0.2σ, CMB-SPA 1.1σ, CMB-SPA+DESI 2.9σ, P-ACT-LB 2.7σ.
Recorded hedge, NOT adopted: a pole of order p ≈ 3 gives 0.974, but needs a non-logarithmic Kähler potential, which gives up the
no-scale structure. Adopt only if the Simons Observatory finds n_s ≥ 0.972 from the CMB alone.

**II. Dark energy + birefringence (new).** A shift-symmetric axion θ thaws by itself: Hubble friction holds it until H ≈ m, then it
rolls. Its photon coupling c_γ θ FF̃ rotates CMB polarisation: β = 0.42° (c_γ/2π) Δθ.
- Protected: a CP-odd coupling cannot change α at linear order, and the shift symmetry forbids a long-range fifth force. This is the
  sector that fixes the D323 failure by symmetry rather than tuning.
- Nested fallback: θ at the potential minimum (or m ≪ H₀) gives w = −1 exactly, i.e. TWIST-I. If DESI's signal fades, nothing breaks.
- Scale: the amplitude stays "Λ from the cliff", V ∝ e^{−2n}.
- **Obstacle found (estimate, in code):** the Twist's own angle y cannot be this axion. From K = −3 ln(T + T̄) its decay constant is
  f = √(3/2)/(a x₀) M_P. A potential of size ρ_Λ ≈ 7×10⁻¹²¹ M_P⁴ needs a x₀ ≈ 277, so f ≈ 0.004 M_P and m/H₀ ~ 1/f ~ 250–280.
  Thawing today would then need a hilltop start tuned to ~10⁻¹¹⁶. Fits want m/H₀ ~ 1–20, i.e. f ~ 0.05–1 M_P.
  Candidate fix (to be checked): alignment of y with a second axion (Kim–Nilles–Peloso type), which raises the effective f to
  ~0.1–1 M_P at the cost of one extra field. The coupling c_γ then comes from the gauge kinetic functions (discrete), giving a
  joint prediction of β from w₀, w_a.
- Limits: a single canonical thawing axion never crosses w = −1. Falsifier: a non-parametric DESI/Euclid reconstruction showing
  phantom crossing at high significance.

**III. Volume stabilisation (weakest piece).** After inflation Re T must stop. Options: TWIST-I capture (D363–D384; UV origin
open, D388, D390), or a heavy modulus (≳ 10⁵ GeV) that decays before BBN (decay temperature ~20 MeV at 10⁵ GeV) followed by
non-thermal production of matter. Both stay open; this is the sector most likely to need a new idea.

**IV. Matter genesis (simplified).** Drop the hidden σ sector; use non-thermal leptogenesis from inflaton decay into right-handed
neutrinos (T_RH ~ 5×10¹⁴ GeV is ample; M_R ~ 2×10¹⁴ GeV from D214). This ties n_B/s to the neutrino sector instead of to
m_σ and the heat share, and removes the matter-like phase that cost 0.5 e-fold of N*. Yield not yet computed.

**V. Dark matter (unchanged).** Gravity-only fermion at 100–200 TeV (D341, D389).

## 4. Dials and what fixes each

| Dial | Fixed by | Tested by |
|---|---|---|
| Cliff scale n | Ω_DE | — (sets scale only) |
| Heat share (narrow) | reheating | N*, n_s, r (SO) |
| f_eff, θ_i | DESI w₀, w_a | β (SO/LiteBIRD calibrated), with c_γ discrete |
| M_R, Yukawa | n_B/s | Σm_ν, 0νββ |
| m_DM | Ω_DM | high-energy ν/γ (IceCube, LHAASO) |

## 5. Computations, in order (each locked before running)

1. D391 N* without σ: done (N* 57.2, n_s 0.9651).
2. Aligned-axion thawing: for f_eff ∈ {0.1, 0.3, 1} M_P, solve θ_i for Ω_DE, output w₀, w_a, Δθ, and β for c_γ ∈ {1, 10, 20};
   compare with 2504.17638's ranges.
3. Leptogenesis yield from inflaton decay with D214 masses.
4. n_s fitted in a thawing-axion background (PC, cobaya): does the DESI-driven upward shift survive? This is the decisive test of
   sector I's bet.
5. Stabiliser (sector III): χ trapping until T_c (D390), or heavy-modulus decay history.

## 6. Kill conditions (stated now)

- SO CMB-only n_s ≥ 0.972 at 3σ → sector I's bet fails (switch to the p ≈ 3 hedge = end view changed).
- Calibrated β consistent with 0 at < 0.05° while DESI keeps w₀ > −0.9 → sector II's c_γ link fails.
- Varying-α or fifth-force signal correlated with dark energy → contradicts sector II's symmetry (good for us to know).
- No natural alignment giving f_eff ≳ 0.05 M_P in the no-scale setting → sector II reverts to Λ (TWIST-I).
