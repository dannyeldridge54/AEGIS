# THE WEAVE: the unified field equation (UFE v4, 21 Nov 2026, 16:45 CT)
Danny 16:21: "It's all about deriving the UFE."

v4 rebuilds v3.3 (written this morning) from the record D1806–D1933. Every term carries a status tag and its compass arrow.

**Status tags:**
- **[der]** derived and checked
- **[lit]** taken from the literature
- **[P]** principle
- **[C]** conjecture with a mechanism
- **[E]** estimate
- **[F]** fitted
- **[PHEN]** phenomenological (no geometric home yet)
- **[TRUST]** an explicit input
- **[OPEN]**
- **[WD]** withdrawn

**Compass arrows** (from field_tests/loom/compass_catalog.json, D1931):
- **●** on target
- **↑ / ↓** the value must move up / down to reach its target
- **!** failing now
- **○** no target yet

**Scoreboard (v4, D1924):** 12 PASS (3 of them PHEN), 2 FAIL (α_s, Δ₃).

## 0. The geometry the equation lives on
| element | value | tag | source |
|---|---|---|---|
| Compactification | type IIB on the **Z₆-II** orientifold, twist (1/6, 1/3, −1/2), χ = 48 on every lattice | [lit/der] | D1847, D1871 |
| Knots | ρ = e^{iπ/3} (order 3, the still point) and i (order 2, the hub) | [P] U22′ | D1818 |
| Tori 1, 2 | Z₃-twisted. U is **frozen at ρ**, so the modulus has no free complex structure | [lit] | D1922, D1923 |
| Torus 3 | Z₂ pyramid. U₃ is the **only free** complex structure (h²¹ = 1). U₃ = i is a choice | [lit/C] | D1907, D1922 |
| N = 2 planes | θ³ fixes the ρ torus and θ² fixes the i torus | [lit] | D1880 |

## 1. The fields
| field | what it is | where it ends | tag |
|---|---|---|---|
| S = C₀ + i/g_s | axio-dilaton and the inflaton | **ρ** (g_s = 2/√3, baseline). i is also a Minkowski vacuum but is disfavoured by the forces (D1926, D1929) | [der] vacuum; g_s control [C] |
| T_vis | 4-cycle under the visible magnetised D7 stack | x = 2πσ/N = 21.10 (σ_vis = 20.15, N = 6) | [der] |
| T_dark | the dark D7 cycle (SU(12) = 2 × 6) | σ_d = 40.3 | [der] / [C] |
| φ_thread | the dark-energy thread | non-Kähler class only (every Kähler thread is excluded: D1906a/b) | [OPEN] |
| U₃ | complex structure of the pyramid torus | i (neutrinos) | [C] |
| X, A′ | dark baryon and dark photon | — | [der]/[E] |
| N₁₋₃ | heavy neutrinos | M_N = 1.84e11 GeV | [CONS] |
| superpartners | split spectrum from anomaly mediation | — | [der] |

## 2. The equation (4D N = 1 supergravity)
    L/√−g = ½ M_P² R − K_{ij̄} ∂Φⁱ ∂Φ̄ʲ − V − ¼ Σ_a Re f_a F_a² + ¼ Σ_a Im f_a F_a F̃_a + matter kinetic + Yukawa + seesaw

**Kähler potential** [lit form]

    K = −ln(−i(S − S̄)) − 2 ln 𝒱(T_vis, T_dark, …) − ln(−i(U₃ − Ū₃)) + Σ_α K_α |Φ_α|²

- Tori 1 and 2 contribute no U-dependence, because U is frozen at ρ (D1922).

**Gauge kinetic functions**

    f_vis = T_vis + 9 S    (flux 9 = 3 families × 3; |M| = 9 on T²/Z₃ exists only at ρ)      [lit + der]
    f_dark = T_dark        (no flux, so the dark side stays cold)                            [C]

**Superpotential**

    W = W₀ + A e^{−2πT_vis/6} + (dark condensate) + Y_q(u) Q H q^c + Y_ℓ(ρ) L H e^c + Y_ν(i) L H N + ½ M_N N N

1. **W₀ and the visible condensate.** |W₀| = A e^{−x}(1 + 2x/3) = **5.6e-9** with A = 0.54, which selects N = 6 [der] (D1811, D1871).
2. **Quarks: one Froggatt–Nielsen spurion, |u| ∈ [0.02588, 0.02740]** [PHEN], converged to 7 nulls in D1932.
   - Charges q_Q = (3/2, 1, 0), q_u = (2, ½, 0), q_d = (½, 0, 0).
   - Natural: f7 = 22–23 %, fJ = 61–66 %.
   - The window is narrow (×1.059), with one fixed charge pattern. It contains 0.027 by construction, since the search started there (D1935); u_d = 0.02587 still fails by 0.05 %. **Compass: ○ (measurement).**
   - Its geometric home is OPEN. There is no modular-τ home (D1922, D1923). Candidates: twisted moduli, bulk-brane positions, recombination flavons, and U₃ near i.
   - Secondary window: U32, |u| = 0.063–0.148, with an assignment that varies across it (D1928).
3. **Charged leptons at ρ.** One stack, three whole rungs (τ 0, μ 1, e 2) [der, modest]. Koide δ = 2/9 and c_e = 0.106 are [TRUST]. **Compass: ○.**
4. **Neutrinos at i.** Flux (4, 4, 8). The ratio is natural (1.3 %) [der]. **Compass: ↑**, with only 0.12 dex of headroom.
   - θ-step n = 3: y₃ = g e^{−9π/8} = 0.0196, giving M_N = 1.84e11 GeV [CONS].

**Potential**

    V(S) = V∞ · G^{SS̄} |∂_S ln E(S, 3/2)|²      E(S, 3/2) = 2ζ(3)y^{3/2} + 4ζ(2)y^{−1/2} + 16π√y Σ N σ₋₂(N) K₁(2πNy) cos 2πNx
         + V_thread(φ) + V_soft

- **Plateau** (P3-S, D1523) [der]. Minkowski vacua sit at **both** ρ and i, with V = 0 to round-off (D1926).
  - Canonical m²/V∞ = 0.5625 × 2 at ρ (isotropic) and (0.193, 3.76) at i.
  - The non-zero-mode coefficient is 16π, corrected in the D1926 DEVIATIONS.
- **V_thread** [OPEN]. It must leave the volume unchanged and needs a slope λ ≈ 0.95 for DESI. Five locked must-tests apply: α_DEF, BBN, MICROSCOPE, D1853, and λ from a named source.
- **V_soft**: split SUSY from anomaly mediation, m₃/₂ = 2.58e5 GeV.

## 3. The derived chain (one number feeds the next), with compass arrows
| step | value | tag | compass |
|---|---|---|---|
| ρ ⇒ g_s | 2/√3 = 1.155 | [der] | g_s > 1: control CONDITIONAL |
| x = 2πσ/N | 21.10 | [der] | — |
| W₀ | 5.58e-9 | [der] | — |
| m₃/₂ = √(g_s/2) W₀ M_P / 𝒱 (𝒱 = 4.0e4) | 2.58e5 GeV | [der] | **TENSION**: the wino wants ↑, α_s wants ↓ |
| wino | 0.687 TeV (bar 0.66) | [der] | ↑ (0.02 dex of headroom, the thinnest) |
| gluino | 4.93 TeV | [der] | ● |
| unification M₁₂, α⁻¹ | 1.07e16 GeV, 28.0 | [der] | — |
| **α_s(M_Z)** | **0.1142** (−4.2 σ; gluino 4.93 TeV, D1929; the scoreboard JSON still carries 0.1147) | [der] | **↑!**; it must come from Δ₃, since m₃/₂ would need ×0.27 |
| **Δ₃** after Higgs pair + gauge term | **−0.094** (bar −0.05) | [der] | **↑!** |
| proton lifetime | 1.6e35 yr | [der] | ● |
| n_s | 0.9706 (data 0.9728 ± 0.0027) | [der] | ● (soft pull: N*, T_R ↑) |
| r | 5.4e-4 | [der] | ● |
| **T_R** = x-chain | **3.7e8 GeV** | [E] | **BOXED** (D1931a): gravitino → wino caps T_R at ≲ 3e9 (Ω ∝ T_R, D732). The "strongest pointing" was withdrawn by referee D1935. N* = 50.3 vs T_R still to be cross-checked |
| leptogenesis | non-thermal (T_R ≪ M_N) | [OPEN] | ↑ |
| m_X = (Ω_DM/Ω_b) m_p · 28/11 | 12.8 GeV | [der] | ○ (prediction) |
| ΔN_eff | 0 | [der] | ● |
| thread α drift ζ | 3.8e-10 (bound 1.66e-6) | [E] | ● (3.6 dex of headroom) |
| knot-charge theorem | integer steps per weight | [lit] | ● |

## 4. Inputs (honest list)
| # | input | status |
|---|---|---|
| I1 | V∞^{1/4} = 4.9e15 GeV | [TRUST], the one outside knob |
| I2 | Koide δ = 2/9, c_e | [TRUST] |
| I3 | the quark spurion size \|u\| ≈ 0.0266 | [PHEN]; one size, but no home |
| I4 | neutrino fluxes (4, 4, 8) and the θ-step n = 3 | chosen to fit [F] |
| I5 | v/m_SUSY ≈ 2.7e-7 | [TRUST] (tuned) |
| I6 | the dark-thread potential | [OPEN] |
| I7 | g_s = 2/√3 > 1 | [C], outside perturbative control |
| I8 | the dark-cycle size σ_d = 40.3 | [C] |

## 5. Superseded from v3.3 (do not use)
| v3.3 item | status |
|---|---|
| N = 7, χ ≈ 50 / ≈ 120 | **WD**: the exact KKLT condition gives N = 6 (D1810, D1811); the fold is Z₆-II with χ = 48 (D1871) |
| N = 6, χ ≈ 90, 𝒱 7.5e4, W₀ 1.0e-8 | superseded by χ = 48, 𝒱 4.0e4, W₀ 5.6e-9 (D1871) |
| U15 twin cycles | **WD** (D1793) |
| LVS | **WD** (D1767a) |
| the shared-step "arrow" u* = 0.052 | **WD**: ε was confused with u (D1894b) |
| the U29 Δ₃ restoration | **WD** (D1907) |
| quark slip ladder, up rung 8 / down ½ (τ_q at a generic point) | superseded: no modular-τ home (D1922, D1923). Replaced by the single spurion (D1932) |
| I8 Λ from the twin cycle | **WD** (D1793–D1795); Λ is an input |
| the S-at-i branch | Minkowski, and inflation passes (D1926), but **α_s 0.1112 (−7.5 σ)** fails (D1929). Disfavoured |

## 6. What closes the UFE (the pulse, from the centre outwards)
- **Ring 0, the rung step:** measured (D1932, D1932a). The one-spurion window is ×1.059 wide with one assignment; its median match is by construction.
- **Ring 3, T_R:** boxed by gravitinos (≲ 3e9). Derive non-thermal leptogenesis within the box, and cross-check N*.
- **Ring 2, forces:** a brane-native Δ₃ path to −0.05. That is the only remaining route for α_s.
- **Ring 1, neutrinos and leptons:** thin margins (the neutrino ratio at 0.12 dex). Koide δ is [TRUST].
- **Ring 4, the reverse thread:** a non-Kähler slope source.
- **The quark spurion's home:** U₃ near i, or a twisted modulus, sized to |u| ≈ 0.0266.

Rule 6h applies to every ring: triangulate from 3 vectors and repeat to 7 nulls in a row. Each ring is locked first and fingerprinted into the compass (tools/project_docs/WEAVE_COMPASS.md).

## 7. Three fields in tandem (Danny 16:48)
The UFE splits into three field equations. They couple only through named interface terms, so any imbalance can be located on a specific interface.

| field | what it governs | its own equation | status alone |
|---|---|---|---|
| **S** (axio-dilaton) | time and cosmology: inflation, reheating, the S vacuum, g_s | V(S) = V∞ G\|∂ ln E(S, 3/2)\|² | balanced (n_s ●, r ●, ΔN_eff ●) |
| **T** (Kähler volumes) | forces and scales: σ_vis, N = 6, W₀, m₃/₂, the dark cycle | KKLT: \|W₀\| = A e^{−x}(1 + 2x/3) | balanced (proton ●, gluino ●) |
| **U** (matter / flavour) | quarks (the spurion), leptons at ρ, neutrinos at i | Yukawas Y(u), Y(ρ), Y(i) | balanced as a fit (PHEN); its home is open |

**Interfaces (the coupling terms):**
- **S–T:**
  - f_vis = T + 9S (the forces);
  - m₃/₂ = √(g_s/2) W₀ M_P/𝒱 (the spectrum);
  - inflaton decay to gravitinos (T_R).
- **T–U:** the matter Kähler metric K_α(T); which brane or twisted modulus hosts the spurion.
- **S–U:** the knot locations (ρ, i), and no perturbative S-dependence of D7 Yukawas (D1923).

**Where the current imbalances sit:** every open failure lies on the **S–T interface**.
- α_s/Δ₃: the threshold in f_vis.
- The wino/α_s tension through m₃/₂.
- T_R, boxed by the gravitino.

The S, T and U sectors are each balanced on their own.
- **Reading:** the missing piece is an S–T coupling term (for example D7 threshold states, or the inflaton's branching into the hidden sector), not a fourth field.
- **Use as a prediction:** the size of the imbalance fixes what the missing term must supply. Example: Δ₃ needs +0.044, which fixes the charges and masses of the threshold states. That is a testable prediction of new states, made from the residual.
