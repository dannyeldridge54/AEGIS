# THE WEAVE — the unified field equation (v3.1 — simplification 1 added; v3, 21 Nov 2026, after unify loops 1–2: D1753–D1766)
Builds on WEAVE_FULL_EQUATION.md (v2, 19 Nov). New in v3: the visible forces on magnetised D7 (the gauge-coupling repair), the dark side on unfluxed D7, the superpartner spectrum, the flux superpotential, the photon-axion, and the reheating chain re-derived. Tags: **[der]** derived and checked · **[lit]** literature · **[P]** principle · **[C]** conjecture with a mechanism · **[E]** estimate · **[F]** fitted · **[A]** hosted/imported · **[OPEN]**.

## 1. The fields (one string compactification, type IIB on an orientifold with D3/D7-branes)
| field | what it is | where it ends | role |
|---|---|---|---|
| S = C₀ + i/g_s | axio-dilaton = the inflaton (Malina) | the knot ρ = e^{iπ/3} (g_s = 2/√3) | inflation; reheating; part of the visible coupling |
| T_vis | Kähler volume of the 4-cycle under the visible magnetised D7 stack | Re T_vis = α⁻¹ − 9 Re S ≈ 16.5–32 | strength of the forces |
| T_dark | Kähler volume of the unfluxed dark D7 cycle | — | dark gauge force (dark photon); the dark thread (Arthur field) [C] |
| T_ℓ | a cycle wrapped only by lepton/U(1) branes | Re T_ℓ ≈ 20–22 | the photon-only axion (cosmic birefringence) [C] |
| τ_ℓ | complex structure of the lepton torus | ρ (residual Z₃) | Koide |
| τ_ν | complex structure of the neutrino torus | ≈ i (offset 1.0685i, C-off) | TM1 mixing |
| τ_q | the quark modulus (third thread) | generic point; SUGRA slip-ladder minima | quark hierarchies, CKM phase |
| X, A′ | dark baryon (sarion) and dark photon (cassion) | — | dark matter |
| N₁₋₃ | heavy neutrinos (waaqino) | — | seesaw + leptogenesis |
| superpartners | split spectrum | — | wino dark-matter component; Higgs mass |

## 2. The equation (4D N = 1 supergravity form)
    L/√−g = ½ M_P² R − K_{ij̄} ∂Φⁱ ∂Φ̄ʲ − V
            − ¼ Σ_a Re f_a F_a² + ¼ Σ_a Im f_a F_a F̃_a                          (gauge sectors a = SU(3), SU(2), U(1), dark U(1))
            + matter kinetic terms + Yukawa terms + seesaw                          (flavour)

**Kähler potential** [lit form; Weave choices P]
    K = −ln(−i(S − S̄)) − 2 ln 𝒱(T_vis, T_dark, T_ℓ, …) − Σ_{τ = τ_ℓ, τ_ν, τ_q} ln(−i(τ − τ̄)) + Σ_matter K_α(τ, S, T) |Φ_α|²

**Gauge kinetic functions** (D1758, Lüst–Reffert–Stieberger hep-th/0410074 eqs. 2.25/3.13)
    f_vis = T_vis + g² S,  g = 3 (the flux quantum that gives three generations)        [lit + C-magD7, E normalisation]
    f_dark = T_dark (no flux ⇒ no S)                                                     [C, keeps the dark side cold]
    the photon-axion: Im T_ℓ couples to F_em F̃_em only                                   [C-photon-axion]

**Superpotential**
    W = W₀ + Σ_mod-forms Y_{αβγ}(τ) Φ_α Φ_β Φ_γ + ½ M_N N N + W_np(T)
    |W₀| ≈ 2e-9 – 1e-7 (from 𝒱 and m₃/₂, D1764)                                         [E, C-smallW0]
    Yukawas: lepton circulant at ρ (Z₃), neutrinos S₄/TM1 at i, quarks modular forms of τ_q with anomaly-free weights (A = 0 ⇒ θ̄ = 0)

**The potential** (the SERAPIS core, unchanged)
    V(S) = V∞ ( ⅔ y∂_y ln E(S, 3/2) )² [1 + C (E − E_ρ)],  E(S,3/2) = 2ζ(3)y^{3/2} + 4ζ(2)y^{−1/2} + …   (Zhinü principle P; tilt C F)
    + V_thread = V_L (1 − 7.30 e^{−β φ}),  φ ⊂ T_dark (sequestered by ≳ 3e3 from the visible gauge sector)  (reverse thread; V_L OPEN)
    + V_ladder(τ_q) (SUGRA (m,0) classes: |ε_m| = 0.0251/(m + 1/16) at arg 50°)
    + V_soft (split SUSY: m₃/₂ = 2.5–7e5 GeV; winos by anomaly mediation)

## 3. The derived chain (one number feeds the next)
    ρ (self-dual knot)  ──► g_s = 2/√3 = 1.155  ──► flux part of the visible coupling 9·Re S = 7.79                       [der]
    α⁻¹ at the string scale (24–40, measured/run)  ──► Re T_vis = 16.5–32   ──► x = 7.79/α⁻¹ = 0.19–0.32                [der/E]
    x  ──► reheating T_R = x·1.34e9 = 2.6–4.3e8 GeV                                                                  [E]
      ├─► leptogenesis: ε = 3.8–6.2e-6, M_N ∈ [3.8–6.3e10, 2.5e12] GeV  (viable)                                    [E]
      ├─► gravitinos ∝ T_R ──► wino window 0.67–1.02 TeV (α⁻¹ 40) / none for a cuspy Galaxy (α⁻¹ 24)                 [E]
      └─► τ_q dilution D ∝ T_R ──► N* shift cancels exactly: r = 5.72e-4 whenever τ_q dilutes (D1766)                [der]
    plateau shape ──► n_s 0.9706 (F) and r 5.41e-4 (10D) / 1.07e-3 (6D)  ·  α_s −9.7e-4                             [der]
    𝒱 (from the tilt) + m₃/₂ (from the winos) ──► |W₀| ≈ 1e-9 – 1e-7  ──► M_P/m₃/₂ explained                         [E]
    m₃/₂ ──► split spectrum: winos 0.67–1.0 TeV, scalars 0.25–0.7 PeV, gluino ≳ 4.8 TeV ──► m_h = 125 needs tan β ≈ 1–4  [E]
    Z₃ at ρ ──► Koide Q = 2/3 (P-F1)                                                                                [der given P]
    knots ρ & i under S₄ ──► TM1: sin²θ₁₂ = 0.3184, δ_CP 262–286°  ──► m_ββ = 1.59–3.80 meV (NO, m₁ = 0)               [der/P]
    one asymmetry ──► m_X = 12.8 GeV (n_X/n_B = 11/28) ──► dark photon 0.3–12.8 GeV; σ/m ≤ 1e-4 cm²/g (α_D ≲ 5e-3)      [der/E]
    anomaly-free quark weights ──► θ̄ = 0 exactly                                                                    [lit]
    slip ladder ──► down quarks rung 1, up quarks rung ~8 (mass ratios) vs 2–5 (mixing, B6 running)                  [A]

## 3b. Simplification 1 — the master relation (D1772, v3.1)
    M₂(wino) = [√(g_s/2) M_P/375] · [4(2π)³ C/(wχ)] · exp[−(2π/N)(α⁻¹ − 9/g_s)],  g_s = 2/√3
Tilt (n_s), gauge running (α⁻¹ ≈ 28.9) and the wino/gravitino mass are ONE relation through two integers of the compactification: a hidden SU(N) condensate on the visible cycle and the Euler number χ. Consistent point: **N = 7, χ ≈ 50** (𝒱 = 4.2e4, |W₀| = 5.9e-9, m₃/₂ = 2.6e5 GeV, M₂ ≈ 0.70 TeV). (Consistency selection; KKLT-type, leading log; LVS excluded by the χ > 0 tilt, D1767a.)

## 4. What is still put in by hand (the honest input list)
| # | input | where it enters | could be derived from |
|---|---|---|---|
| I1 | V∞ (sets A_s) | inflation height | species count / volume [OPEN] |
| I2 | tilt C (sets n_s) | inflation | now tied to χ and 𝒱 by the master relation (D1772): with N = 7, χ ≈ 50 it is no longer independent of m₃/₂ |
| I3 | α⁻¹ at the string scale ⇔ Re T_vis | forces | FIXED BY DATA (D1767): α⁻¹ = 28.9 at 7e15 GeV (split-SUSY running) ⇒ Re T_vis = 21.1, T_R = 3.6e8 GeV, M_N ≥ 4.5e10 GeV, wino 0.67–0.71 TeV; theory (LVS SU(N) condensate) gives 26.0–26.7 (N = 4) / 30.6–31.4 (N = 5): not selected |
| I4 | m₃/₂ (or the wino mass) | SUSY, dark matter | DERIVED from (C, α⁻¹, N, χ) by the master relation (D1772); (N, χ) = (7, ≈50) |
| I5 | Koide scale (one lepton mass) and δ = 2/9 | leptons | δ: no derivation exists in the literature; not the thawing axion (would drift m_e/m_μ); Berry phase C-δ only (D1768) |
| I6 | neutrino masses (Σm_ν, m₁ = 0) | neutrinos | seesaw M_N and Yukawas [OPEN] |
| I7 | quark O(1) couplings (12) and τ_q's class | quarks | [A] |
| I8 | V_L (the size of Λ) and the thread's start | dark energy | [OPEN — the cosmological-constant problem] |
| I9 | m_A′, ε (dark force) | dark matter | α_D DERIVED = 0.035 at 12.8 GeV from a twin dark cycle (D1769, C); m_A′ and ε still free |
| I10 | g = 3 (M = 4) flux | generations | [A] |
| I11 | v = 246 GeV given m₃/₂ (tuning ~4e6) | Higgs | [OPEN — the last factor of the hierarchy] |
Compare: the Standard Model + ΛCDM have ~25–30 free numbers. The Weave fixes or ties: n_s/r/α_s relation, Q = 2/3, TM1 angles and δ_CP branch, θ̄ = 0, m_X, ΔN_eff ≈ 0, the reheating chain, the r-invariance, and W₀ from two others; it still hosts the quark couplings and the neutrino and dark-force scales.

## 5. What would unify it completely (the remaining derivations)
0. (done, D1767) the data fix α⁻¹ ≈ 29 and with it the whole reheating chain; the visible-cycle size 21.1 equals the birefringence cycle size 20–22 (U15, C-twin-cycles).
1. Stabilise T_vis (and T_dark, T_ℓ) inside the same species/flux structure ⇒ α⁻¹ predicted (I3), and with it T_R, the wino window and the genesis window become predictions.
2. δ = 2/9 from a Berry phase on Re τ_ℓ (C-δ) ⇒ all three lepton masses from one scale (I5).
3. What selects τ_q's class and the up-quark rung (B6 decides the data side) ⇒ quark couplings reduced (I7).
4. The size of Λ (I8) and the last hierarchy factor (I11): no Weave-native route found yet.
5. Dark-force numbers from the dark D7 (I9).

## 6. Tests
Full list: WEAVE_TEST_PLAN.md (on hold while the equation is finished; Danny 08:56). CubeMind's blind-derivation queue holds the loop-2 calculations.
