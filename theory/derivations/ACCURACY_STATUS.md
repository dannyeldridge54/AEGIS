# SERAPIS accuracy status (16 Nov 2026, after the accuracy track D807–D827)
Published: SERAPIS v3.1, 10.5281/zenodo.24281771. Changes queued for v3.2: papers/v3/V32_TODO.md.

## Derived (computed from stated inputs; exact MS where spectra are involved)
- The Janus closed form and the consistency relation (bias 11–13%, D635); caps (D674–D677); the (n_s, r) strip (D678–D681); β_s (D666).
- SERAPIS-E: plateau, ρ vacuum and tilt from E(τ,2) and the one-loop BHK correction, at a natural size (D689–D696). The frozen band uses exact MS (D692).
- ρ selected by lattice sums (Rankin, Montgomery) for supersymmetric (positive, completely monotone) sums; a Scherk–Schwarz breaking reduces the group (D801, D803, D804). SERAPIS-E needs the full SL(2,Z) and equal brane numbers.
- Z₃ structure at ρ: isotropy, cubic term, orbit charge |η| = (1.7–2.1)|Δx| (D796, D810).
- The τ = i vacuum is stable against BHK terms for any C (D802, D811).
- Gravitino → wino is negligible (Ω ≤ 3e-4, D809). The wino window is 0.67–1.85 TeV (thermal; D784).
- Exactness: every flagged paper number was recomputed with MS (D813–D817). The slow-roll bias is uniform: n_s +0.0003, r −1.3%.

## Fitted (chosen to match data; stated as such)
- ε at τ = i (and the ρ L-variant's tilt), which also supplies the τ = i vacuum mass. No derived source comes within 10¹¹ (D826). A loop-sized BHK factor can tilt τ = i, but it changes α_s and r and leaves the vacuum massless (D823).
- C for SERAPIS-E: natural size, but its value is chosen to hit the n_s band.

## Postulated (open)
- P3: the plateau sits in the anti-D3 (nilpotent) metric with the E(τ,2) placement. The deep project (D828–D832) computed the anti-D3 one-loop term for our configuration: additive, a rising wall in y, so P3 has no one-loop origin. P3 stays a postulate (downgraded); the frozen predictions do not depend on its origin. Tadpole with an anti-D3 needs D3 stacks (5, 2), not (5, 1). The κ project (D833–D836): the anti-D3 term is harmless for the band only if the small tori are large (v₄ ≳ 2e4·g_s, estimate); at natural size it shifts n_s by +0.02 (exact MS). At τ = i it is a saddle, so it is not the τ = i mass source; at band-allowed size it does not destabilise τ = i (D834a). ρ is safe. Warped-throat project (D837–D839): a throat gives only exponentially approached plateaus, not the power-law E-ratio, and our torus has no conifold. P3's E-ratio has no identified string origin; it stays a postulate.
- P1: CP phases in the heavy-ν couplings (leptogenesis). Testable only (DUNE/Hyper-K).

## Conditional (the bands hold only if)
- τ = i band: under the corrected reheating, only ε ≈ 1.40–1.45e-4 stays in band (D815).
- SERAPIS-E band: the late Z₃ decay at T₂ ≳ 1e5 GeV; otherwise the post-hoc self-diluted band 0.966–0.970 applies (D781, D813).

## Error budget (D821)
Band edges: ±0.0005–0.0006 in n_s, ±1.5–2% in r (numerical). This is well below the data σ (0.0025).

## Tests in reach
- n_s: SO + DESI. The frozen band sits at −1.5 to +0.5σ of CMB-SPA+DESI; the post-hoc ρ history is at −3.1 to −1.5σ (D805, D813).
- Σm_ν: alive by 0.0005 eV. This is a class test (NO + ΛCDM), not SERAPIS-specific (D824).
- r: NOT detectable by LiteBIRD (δr = 1e-3); exclusion only (D820).
- α_s: ~1σ by 2030s forecasts; the Janus enhancement needs ~5× better (D806).
- Wino: HL-LHC reaches ~1 TeV; gamma-ray lines.
- τ = i variant status (D841, rule committed first): KEPT AS A CONDITIONAL VARIANT. No frozen prediction fails and the vacuum is stable; conditions: ε has no derived source, and a 2⊕1 heavy-ν structure is needed only at τ = i.
- P1 (D843–D846): CP is a symmetry of the string effective theory, and our specified configuration has no CP source. P1 is replaced by P1′: spontaneous CP violation by a Kähler-axion racetrack minimum (CP-odd minima exist in 90% of a scan, often metastable). No frozen prediction changes.
- P1′ follow-up (D851–D855): CP-odd racetrack vacua are the deepest in 41% of cases; heavy-ν instanton masses need two charge sectors. P1′ is needed only at τ = i, where it requires CP-odd axions on two cycle classes (D854). The ρ re-weighting of D853 is withdrawn (D853a): ρ's frozen band has no baryogenesis mechanism and its AD history needs no phase.
- τ = i under P1′ (D854): single-modulus P1′ gives the resonant doublet no CP phase (ε = 0); τ = i leptogenesis then needs two CP-odd Kähler axions on different cycle classes, a fourth condition on the conditional τ = i variant.
- Moduli consistency (D857–D861): with an anti-D3, no moduli point satisfies the BHK tilt, the anti-D3 bound and P1′'s CP-odd racetrack together; without it, only with string-size small tori (benchmark g_s = 0.232, A = (40.8, 1, 1), C = 1.25e-6, M ≈ 1e11 GeV). τ = i stays a conditional variant (rule D841: R2 not met) with the added condition; ρ unaffected.
- α′ control (D862): at the benchmark the BBHL correction is 0.3% and worldsheet-instanton-type terms are sub-percent; but with small tori ≥ 2 string units only one grid-edge point survives (none at ≥ 3), so the consistent P1′ region is a thin sliver; the one-loop Kähler correction to the racetrack modulus is tiny (c′ ≈ 0.008) and leaves the CP-odd minima unchanged even at 100× (D863).
- Correction (D866, D857a): BHK's tilt modulus is the 4-cycle transverse to the inflaton torus, not the inflaton torus's area. The moduli scans and benchmark of D857–D865 are superseded; a corrected scan follows. Racetrack on that same cycle is excluded; on the other two cycles it is reopened.
- Corrected scan (D867): an anti-D3 uplift is incompatible with SERAPIS-E's BHK tilt at any perturbative coupling (its interaction would shift n_s by ≈ +0.005 to +0.06), so SERAPIS-E's uplift/nilpotent sector cannot be an anti-D3 on this torus. The earlier 'P1′ vs anti-D3' conflict mixed branches (BHK is ρ's, P1′ is τ = i's); D861's extra τ = i condition is withdrawn (D861a).
- Uplift sector (D868–D870): with the on-torus anti-D3 excluded, P3's plateau sits in the uplift sector: a distant warped-throat anti-D3 is sequestered enough (κ/V0 ≲ 1e-8), or a T-brane uplift on the T⁴ cycle; both need more than the toroidal orbifold.
