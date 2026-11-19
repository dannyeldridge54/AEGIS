<!-- AEGIS-FP LRBPAWUDBMOHFPNX · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License) -->
# Postulates (Jl loop, L4). Each: assumptions, form, falsifier, status (open / tested / retired). Budget: at most 2 open (balance β3).

## P1 — CP violation at ρ comes from the couplings, not from τ (status: open — reopened D773; flux-relation sources P2/P4 retired; P1 is again the working assumption)
Assumptions: SERAPIS-E's flavour sector does NOT impose generalised CP. The 2⊕1 heavy-ν couplings (c, and the Dirac Yukawas) are complex with independent O(1) phases, uniformly distributed (a "no-preference" prior). τ sits at ρ on the CP-conserving line Re τ = ½ (1905.11970 §4.3), so τ adds no phase.
Form: the effective leptogenesis phase δ is uniform on [0, 2π); the asymmetry is ε = ε_DI·|sin δ|.
Falsifier: (i) a UV completion that imposes gCP (then ε = 0 at ρ and the branch needs another baryogenesis); (ii) a measured low-energy Dirac phase δ_CP pointing at CP conservation (δ_CP ≈ 0 or π at > 3σ, DUNE/Hyper-K), which would disfavour (but not exclude) P1.
- P1 update (D763): P1 is needed on BOTH branches (τ = i also sits on a CP-conserving locus). Falsifier (ii) is refined: δ_CP ≈ 0/π only weakly disfavours P1 (≈6% prior mass at |sin δ| < 0.1), while discovered leptonic CP violation excludes the gCP alternative.

## P2 — the heavy-ν couplings depend on a second complex-structure modulus U₂, tied to U₁ by the flux relation U₁U₂ = b₃/a⁰ (status: retired D772 — the published flux model also fixes τ₃ = S, leaving no free inflaton)
Source of the mechanism: literature (2405.18813). Postulated part: SERAPIS's heavy-ν sector (the Dirac Yukawas or N₃) lives on, or couples to, the second torus, so its couplings are modular forms of U₂.
Form: U₂ = −(b₃/a⁰)/ρ. CP is violated unless b₃/a⁰ or a⁰/b₃ is an integer (D764). The CP-odd size is s_CP = |sin arg j(U₂)|, with median 0.77 over small fluxes.
Falsifiers:
- the SERAPIS tadpole budget (5/5/5 + 1, D698) leaves no room for the a⁰, b₃ fluxes;
- the flux relation spoils inflation: U₂ tracks U₁ during the roll (forward check, D765);
- leptonic CP conservation established (δ ∈ {0, π}), which would favour integer flux ratios.
- P2 update (D765): the strong form (U₁ = inflaton in the flux relation) CONFLICTS with the frozen SERAPIS-E bands (r ≈ 6.5–7.5e-4). P2 is restricted to the relation on non-inflaton moduli (U₂U₃ = b₃/a⁰), to be tested by the next reverse tick.
- P2 update (D766): restricted form = U₂ = ω with U₂U₃ = b₃/a⁰, heavy-ν couplings ∝ forms of U₃. U₂ = i never violates CP. The tadpole then forces 3/3/3 + 1 stuck D3s (n_flux = 12 saturates 32). New falsifier: the exotic O3′ planes needed for odd b₃ are inconsistent with the stuck-brane torsion model.

## P3 — the SERAPIS-E plateau comes from the anti-D3 (nilpotent goldstino X) sector: K_XX̄(τ) is set so that V_inf = V0[1 − E(ρ,2)/E(τ,2)] (status: open)
Mechanism source: literature framework. In "geometric inflation" with a nilpotent X (the anti-D3 goldstino), W = W0 + F·X and V = |F|²K^{XX̄}(τ) − 3|W0|², so any non-negative V(τ) is realised by choosing K^{XX̄} = (V(τ) + 3|W0|²)/|F|². SL(2,Z)-invariant attractors with minimum at ρ are built exactly this way in 2408.05203 §9 (refs [16, 17] there).
Postulated part: the anti-D3 metric's τ-dependence is the Epstein ratio 1/E(τ,2), the same function as the BHK tilt. Not derived from a warped-throat computation.
Form: K^{XX̄} ∝ 1 − E(ρ,2)/E(τ,2) + 3|W0|²/V0. It is positive on the whole fundamental domain since V ≥ 0, and modular invariant.
Falsifiers:
- r outside 4.55–5.12e-4 (LiteBIRD era);
- n_s outside 0.970–0.975 (SO + SPHEREx ~2030);
- isocurvature or f_NL from the light axion Re τ (forward check D769);
- a warped-throat computation showing anti-D3 metrics depend on U only through e^{4A} warp factors with ln-type, not 1/E-type, dependence.
- P3 update (D769–D770): falsifier 3 (the light axion) CLEARED. ζ_axion ≤ 1e-7, and every start settles at a ρ image. P3 stays open (its origin is still postulated).
- P3 update (D797): no literature source. Tree-level anti-D3 has no torus-τ dependence (1707.07059). Standard one-loop routes give E(τ,2) ADDITIVELY in K_XX̄ (a hilltop at ρ, or a negative metric) or as a Casimir term (unbounded below), never the needed K^{XX̄} = a − b/E. New falsifier: an explicit T⁶/(Z₂×Z₂) anti-D3 annulus giving only additive k₁E. Still open.
- P3 update (D799): the gaugino-condensate placement is closed too. Weight −3 forces W ∝ η⁻⁶·P(j), which grows ≳ e^{πy} at the cusp (2212.03876), so condensate terms cannot give a plateau. Remaining route: inverse-metric (K^{XX̄}) placement only. Candidate plateau function: DKL Δ (D798, minimum at ρ).
- P2 update (D771): one allowed configuration only: n_flux = 12 (a⁰ = 2, b₃ = −3), 8 exotic O3′ spread evenly (two per inflaton fixed point), stuck D3s 2/2/2 + 0, N_eff = 2. New falsifiers: exotic-plane placement rules for this flux; stuck D3s at O3′-carrying fixed points.

## P4 — CP violation from a pure-NS flux relation on the non-inflaton tori (status: retired D773 — no SUSY Minkowski vacuum with Im S > 0; no τ₁-free flux vacuum exists at all)
Assumptions: F₃ = 0 and H₃ has an odd quantum, so W = S·(a·U₂U₃ + b). At W = 0 this enforces U₂U₃ = −b/a with U₂ at ω, leaving U₁ (the inflaton) free. S is stabilised separately (racetrack, D586). The heavy-ν couplings depend on U₃. Exotic NS O3 planes are spread evenly over the inflaton torus.
Form: U₃ = −(b/a)/ω, CP-violating unless b/a or a/b is an integer (D764 j-test).
Falsifiers:
- no exotic-plane pattern fits both the odd-cycle parity rule and even spreading;
- W = 0 conflicts with the covariant completion's W₀ ≠ 0 (f² = 3|W₀|²) or with the dilaton racetrack;
- leptonic CP conservation established.

## P5 — a Z₃-charged colour-triplet diquark scalar X lighter than the heavy pair (status: retired D792 — not needed: the self-diluted ρ history makes baryons without it)
Assumptions: X (colour triplet, Z₃ charge fixed by the couplings) has renormalisable couplings y₁·N·u^c·X* and y₂·X·d^c·d^c allowed by Z₃ (baryon triality on the SM, D787) and by matter parity. M_X < M_pair (≈ 4e11–1e12 GeV).
Form: N → u X* is a 2-body renormalisable decay (fast), then X → d d. The CP asymmetry from X-loop interference is ε ~ y²/(8π)·(phase) [estimate]; y ≳ 0.02–0.17 for ε_req.
Consequences: the pair decays promptly, so there is NO late matter phase and T_R returns to the D725 value (3e8–3e9). The frozen ρ band is restored without the Λ condition (D781–D783 become moot). Baryogenesis is B-violating from N decays, and the proton is still protected by baryon triality.
Falsifiers: a coloured scalar with these couplings in conflict with gauge-coupling unification or flavour data; the requirement that X's Z₃ charge also allows a proton-decay path (to check); no string origin for a light colour triplet (doublet–triplet-type issue).
- P3 update (D828–D832, P3 deep project): the anti-D3 one-loop amplitude for our configuration was set up and computed. It is additive in V (K_XX̄ unchanged), its only stable placement is a stuck anti-D3 at an empty O3 point with D3 stacks (5, 2), and its T²-shape term is a rising wall ∝ +(4π/3)κy. P3 has NO one-loop origin. Kept as a postulate, downgraded. Remaining routes: warped throat, non-perturbative, or a different origin.
- P3 update (D833–D836, κ project): if the plateau's anti-D3 is present, its one-loop interaction (κ/V0 = g_s/8πv₄) shifts n_s unless v₄ ≳ 2e4·g_s [estimate]. So P3 now carries a geometric requirement: large small tori. It also makes the τ = i vacuum unstable along x (D834).
- P3 update (D837–D839, warped-throat project): a warped throat couples to U only multiplicatively and can give only an exponentially approached plateau; SERAPIS-E's E-ratio is a power law. With the one-loop and holomorphic routes closed, P3's E-ratio has NO identified string origin. Kept as a postulate.
- P1 update (D843): in string completions CP is a symmetry of the effective theory (outer automorphism; 2010.10782, 1901.03251), so the couplings' phases are not free and CP must be broken spontaneously by an axion vev. Toroidal flux vacua do not break it. P1 is not falsified but must be reformulated with a named breaking modulus (Kähler axion or brane modulus; C.2).
- P1 update (D844): the specified configuration (T⁶/(Z₂×Z₂), equal stuck D3 stacks, BHK, flux-fixed S, U₂, U₃, flat Kähler axions) has NO spontaneous CP source. P1 needs a named extension: a non-toroidal sector, a CP-odd racetrack vacuum for a Kähler axion, or a hidden-sector source.
- P1 → P1′ (D846): CP is broken spontaneously by a Kähler-axion vev fixed in a CP-odd minimum of a real-coefficient racetrack (D845); the heavy-ν couplings depend on that modulus. δ is vacuum-dependent, not uniform. Status: open (P1′). Falsifiers: no racetrack possible on the relevant 4-cycle, or no heavy-ν coupling to it; δ_CP ≈ 0/π stays a weak test.
- P1′ update (D851–D853): final form: CP broken by a Kähler axion in a CP-odd racetrack minimum (deepest in 41% of racetracks); heavy-ν masses from ≥ 2 D-instanton sectors of different charge; phase Δ = 2πΔn⟨Re T⟩, |sin Δ| > 0.1 in 80% of CP-odd vacua. ρ-leptogenesis pass probability given a CP-odd vacuum: median 0.84 (P1: 0.95); unconditional ≈ 0.34 (estimate).
- P1′ update (D854): at τ = i the resonant doublet shares one charge and hence one instanton phase; on a single cycle class singlet mixing adds no relative phase, so ε = 0. τ = i leptogenesis under P1′ needs CP-odd axions on two cycle classes.
- P1′ update (D855, D853a): P1′ is needed only for the τ = i branch (resonant leptogenesis), where it requires CP-odd axions on two cycle classes. The ρ branch's frozen band has no baryogenesis mechanism and its post-hoc AD history needs no phase; D853's ρ numbers are withdrawn.
- P1′/P3 update (D860, D861): in our configuration P1′'s racetrack and P3's anti-D3 (with BHK) cannot hold together; without the anti-D3 a consistent point exists only with string-size small tori (benchmark g_s = 0.232, A = (40.8, 1, 1)). τ = i (which needs P1′) therefore also needs its nilpotent sector not to be a natural-size anti-D3.
- P3 update (D867–D870): the anti-D3 on the inflaton torus is excluded for SERAPIS-E (D867). P3 now reads: the plateau sits in the UPLIFT sector, realised by a sequestered throat anti-D3 (D869, nilpotent X kept) or a T-brane D-term on the T⁴ cycle (D868, no X); both need ingredients beyond T⁶/(Z₂×Z₂). Its E-ratio form still has no identified origin (D839).

## P6 — lattice-disk plateau: one Poincaré disk per complex dimension of a weave lattice, 3α = d/2 (status: side model — D1352; not part of the SERAPIS chain, scored only on future r data)
Mechanism source: literature 3α = 1…7 disk family (Ferrara–Kallosh 2016; Kallosh–Linde–Wrase–Yamada 2017). Postulated part: the lattice → disk-count rule.
Form: V = V0 tanh²(φ/√(6α)), 3α = d/2 (A2 1, D4 2, E6 3, E8 4, BW16 8, Leech 12).
Falsifiers: r < 1e-3 at 95% CL kills every config; a detected r picks one lattice (A2 ≈ 1.4e-3 … Leech ≈ 1.5e-2).
- P3 update (D1361–D1385, D1364 locked, 2026-11-18): status → "derived (candidate)" by the D1364 lock — the plateau survives with the leading-order s = 1 shape alone (w = 0: n_s 0.96984, r 5.26e-4, in band). Candidate origin: the universal one-loop threshold in the dilaton Kähler potential, K = −log(Im S + Y/16π²), Y ⊃ (90/π³)E(U,2)/T₂ (KKPR hep-th/9608034; D1366, D1375, D1383), which supplies exactly the K^{XX̄}-type 1/(a + bE) structure D797 asked for. SUGRA embedding: Kallosh–Linde streamlined construction (D1353). Still open: explicit model (Z₄ host, condenser b′ ≈ 0, D1384–D1385), control at T₂ ≳ 16 (D1378), uplift.
- P3 update (D1397–D1398, 2026-11-18): the universal-threshold origin (KKPR K = −log(Im S + Y/16π²)) is KILLED for the SERAPIS point: in the E(U,2) regime horizon exit violates the chamber (y* ≥ 37T₂, D1397); with the full Y the plateau is the α = 1/3 attractor (n_s 0.960, r 1.6e-3, D1398). P3's origin is a postulate again; D1364 (shape robust to expansion order) and D1353 (exact SUGRA embedding) stand.
