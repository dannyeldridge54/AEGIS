# Theory audit of the Spiral Twist note, 7 November 2026

AI-assisted (Claude), at the author's request. **Not pre-registered and changes no locked file.** Every finding below
has a script that reproduces it. Tier: checks of existing algebra and code; nothing here is new evidence.

## Verified (re-derived by hand and against the source papers)

| Item | Result |
|---|---|
| Kähler metric from Gates–Ketov–Yunes Ω, K (arXiv:0906.4978 eqs 5.36–5.37) | K_ΦΦ̄ = 3/(Φ+Φ̄)², as in the note |
| BI field = the supergravity **axion** (imaginary part) | Confirmed in GKY's own text |
| λ = −2√(2/3), field-space curvature −2/3 (α = 1) | Correct |
| W = const potential, extrema at φ = −1/2 and −2/3 | Correct; −1/2 is a local **maximum**, −2/3 a local minimum, both at V < 0 |
| α_DEF = (2/√3)(\|φ\| − 1/2) and the Cassini window \|Δχ\| < 0.0072 | Correct in Damour–Esposito-Farèse normalisation |
| Matter-like angle: d ln m/dχ = −λ/2 = 0.816 | Correct |
| Babu–Amendola convention (arXiv:2610.23497) | m_c ∝ e^(−βκφ), κ = 1/M_Pl: **same** convention as the note, so f ≲ 0.073/0.816 ≈ 9% stands |
| Toomey et al. (arXiv:2511.23463) λ posterior | −1.3 (+1.3/−1.5) on Planck + DESI, prior (−3, 0): as quoted |
| "Weak mixing" | Ramos-Hamud writes W = e^(−ξφ/M_p) and needs log₁₀ξ ≳ 2.5. Whether ξ = 0.82 or 1.63 here depends on a factor-2 convention; either way it is 200–400× short. Conclusion robust |
| n_s = 0.9667, r = 0.0033 at N = 60; 2.4σ from ACT DR6 | Correct |

## Findings

**1. F is absorbed by the dilaton (Spiral model).** With matter blind to the dilaton, shifting the dilaton's starting
value is an exact symmetry once F, θᵢ, m and V₀ are rescaled. `f_dilaton_degeneracy.py` reproduces H² and w to
≤ 1.2 × 10⁻⁹ for four cases. So "F = (4/π)√(3/2) M_Pl, fixed" constrains nothing in the Spiral fits until something
physical fixes where the dilaton sits. If the dilaton were pinned at the Jordan-frame GR point (|φ| = 1/2), the
Nieh–Yan F would correspond to F = 3.12 in the note's convention, not 1.56. **λ is not affected.** In the single-field
late Twist (no dilaton), F is physical and the TF-P test is meaningful. *Correction, same day:* |φ| = 1 is not
arbitrary. There the GKY kinetic metric 3/(4φ²) equals the Einstein–Cartan coefficient 3/4 of Calcagni–Mercuri, which
is what `nieh_yan_period.py` uses. So F = 1.559 is the value when the dilaton sits at the Einstein–Cartan matching
point; the degeneracy means the Spiral must state that the dilaton is there (as `spiral_w.py` assumes at the start),
and F drifts as it rolls.

**2. ~~The F derivation is not in the repository.~~ Corrected: it is in the release repository.**
`the-twist-torsion-cosmology` has `code/analysis/nieh_yan_period.py`, `results_notes/NIEH_YAN_PERIOD.md` and both
pre-registrations (TF locked 2 Nov 14:51:28, TF-P 14:55:36); CubeMind has copies. They were just not in AEGIS. The
derivation: Mercuri–Taveras coupling (1/2κ)β N; Chandía–Zanelli ∫N = 4π²ℓ²ν; period Δβ = κ/(πℓ²) = 8 at ℓ = √G;
linear Nieh–Yan map φ = √(3/2)β; F = √(3/2)/(2π²ℓ²) = (4/π)√(3/2) M_Pl. Re-checked here: correct, with the four
assumptions it states itself (coupling normalisation, ν_min = 1, true periodicity, ℓ = √G). **The TF-P runs never
ran**: no `_fF0.1930` result exists in any repository. See the TF-P section below.

**3. The two locked α = 1 inflation statements pull against each other.** `alpha1_inflation_squeeze.py`: matching ACT's
n_s within 1σ needs N = 69–87 e-folds, which gives r = 0.0016–0.0025, straddling the locked kill line r < 0.002. The
locked r range (0.0033–0.0048) assumes N = 50–60, which is the range in 2.4–4.7σ tension. Not a change to the lock;
it should be stated in the next version.

**4. Sign of the matter-like coupling: still to check.** Babu–Amendola find a bimodal posterior (β ≈ ±0.05) and only the
negative mode gives apparent phantom crossing. Here m ∝ e^(+0.816χ), so β_BA = −0.816f, and the direction of the bend
also depends on the sign of χ̇. The note's table shows the bend toward DESI, which suggests the signs line up, but the
mapping should be written out explicitly.

## New literature to cite or answer

- M. Ramos-Hamud, *Spiralling into Dark Energy: Axio-Dilaton Attractors in Light of Current Data*, arXiv:2610.34380
  (25 Oct 2026). Same "spiral" non-geodesic attractor; needs λ ≳ 7–9 and log₁₀ξ ≳ 2.5. Directly relevant.
- Gao et al., arXiv:2608.09487 and 2608.19392: a dynamical BI field through the **Holst** term gives GW amplitude
  damping (Ξ₀), not velocity birefringence. The Twist's locked GW prediction uses the **Nieh–Yan** coupling, so no
  conflict, but it is a second GW channel to test. Their papers contain arithmetic slips (a 90% interval that does not
  follow from their stated method; a forecast bound quoted two ways).
- DESI DR3 BAO is **not** out (as of 7 Nov 2026). arXiv:2610.37664 is a Lyman-α reconstruction methods paper,
  mislabelled "DR3" by a third-party bot.

## Tests still needed (drafts; the author writes and locks the rules)

| # | Test | Where | Status |
|---|---|---|---|
| A | What fixes the dilaton's value? | `dilaton_pinning.py` | **Done**, see below |
| B | Run the three locked TF-P fits (rules and derivation exist in the release repository) | PC | Open: Union3 is the blind one |
| C | Coupled-angle fit (fraction f, 2 DE parameters), "running under a locked rule" | PC (AxiCLASS) | Open |
| D | n = 2 refit restart (`edelockP_n2_deep` failed: flat start, all 19 evaluations equal) | PC | Open |
| E | GW friction and birefringence for the Nieh–Yan coupling | Literature | **Done**, see below |
| F | Sign map to Babu–Amendola's phantom mode | Solver + algebra | **Done**, see below |
| G | Holst or Nieh–Yan: the model uses both (new, from E) | Theory | **Decided: Nieh–Yan** (`COUPLING_CHOICE_NIEH_YAN.md`) |

## Follow-up, same day: tests A, E, F and the new item G

**A. What fixes the dilaton** (`dilaton_pinning.py`). The canonical axion is a_c = √(3/2) a/|φ|, so a period P in a
gives F = √(3/2) P/(2π|φ|). The note's value implies P = 8 at |φ| = 1, and F depends on where the dilaton sits:

| Pin | \|φ\| | F (M_Pl) | `_fF` value | Extremum of V (W = const)? | α_DEF | Light dilaton passes Cassini? |
|---|---|---|---|---|---|---|
| Einstein–Cartan matching (note's choice) | 1 | 1.559 | 0.193 | no | 0.58 | no |
| GR point | 1/2 | 3.119 = (4/π)√6 | 0.494 | yes, a **maximum** | 0 | yes |
| W = const minimum | 2/3 | 2.339 | 0.369 | yes, a minimum | 0.19 | no: must be heavy (≳ 5 meV) |

Reading: (1) |φ| = 1 is where GKY matches Einstein–Cartan (kinetic coefficient 3/4), but it is not an extremum of V, so something must hold the dilaton there. (2) A pinned dilaton cannot also roll as dark
energy, so **a fixed F and the rolling Spiral exclude each other**: either the dilaton rolls and F is free (+1 parameter),
or it is pinned and the late field is the axion alone with one of the discrete F values above. (3) With W = const the
GR point is a maximum, so a light dilaton cannot rest where Cassini needs it; a different W, or a heavy dilaton at
|φ| = 2/3, is needed. (4) The single-field late Twist can test the two physical values directly: run names
`_fF0.4940` (GR point) and `_fF0.3690` (W = const minimum), beside TF-P's `_fF0.1930`. These are new hypotheses and
need a locked rule before they run.

**E. Gravitational waves.** In Einstein–Cartan gravity, solving for torsion with a Nieh–Yan-coupled BI field gives
torsion-free GR plus a free scalar (Calcagni & Mercuri, arXiv:0902.0957, eq. 27): no parity-violating term remains,
so at tree level there is no GW velocity birefringence and no extra friction (Ξ₀ = 1). The velocity birefringence in
locked Q6 comes from Li, Rao & Zhao (arXiv:2007.08038), which is **teleparallel** gravity (zero curvature), a different
framework. Q6's null-result clause is unaffected (a null is consistent either way), but its quoted 10⁻⁴³–10⁻⁴² GeV
scale has no source in the Einstein–Cartan framework the paper uses. Gao et al.'s Ξ₀ friction (Holst) likewise needs
a step beyond tree-level Einstein–Cartan; their mapping is model-dependent by their own account.

**F. Sign.** In `spiral_w.py` the dilaton rolls toward larger χ at all late times (dχ/dN > 0 for κ = 0.5, 1.2, 2.0), so
the BI angle's mass m ∝ e^(0.816χ) grows with time. A growing dark-matter mass is what produces apparent phantom
crossing, i.e. Babu–Amendola's negative-β mode (m ∝ e^(−βκφ), β < 0). The bend toward DESI in the note's table is
therefore the right direction. Caveat: this assumes Babu–Amendola's field also increases, as in thawing from a hilltop.

**G. Holst or Nieh–Yan (new).** Calcagni & Mercuri: the Holst coupling gives the canonical field φ = √(3/2) arsinh β,
while the Nieh–Yan coupling gives a **linear** map φ = √(3/2) β. The model's field map and Fingerprint (sinh/arsinh)
are the Holst result, while the decay constant F and Q6 are argued from the Nieh–Yan term. One theory has to pick one
coupling (or state how both appear) before the torsion-specific numbers are consistent.

Scripts: `f_dilaton_degeneracy.py`, `alpha1_inflation_squeeze.py`, `dilaton_pinning.py` (outputs `.json` beside them).

## TF-P read from the existing grid (indicative, not the locked test)

The TF-P pre-registration itself notes that the grid already holds log₁₀F = 0.2, 0.007 dex from F_P. Profiling the
stored `cmp_ax_spa_latetwist_gF*m*` fits over the grid's m values (an upper bound on χ²: freeing m can only lower it),
with TF's D_F and G_F:

| log₁₀F | F (M_Pl) | DES Y5 G_F | DES Y5 D_F | TF rule would read | Pantheon+ G_F |
|---|---|---|---|---|---|
| 0.0 | 1.00 | −6.23 | 0 | (grid best) | −0.19 |
| **0.2** | **1.58 ≈ F_P** | **−5.49** | **+0.74** | **SUPPORTED** | −0.41 |
| 0.4 | 2.51 ≈ W = const minimum (2.34) | −4.67 | +1.56 | DISFAVOURED | −0.02 |
| 0.5 | 3.16 ≈ GR point (3.12) | −4.41 | +1.82 | DISFAVOURED | −0.10 |

Reading: the Einstein–Cartan / Nieh–Yan value F_P sits where the data are best; the two dilaton-pinned values I
proposed in test A do worse. **Caveats:** (i) this is a grid read, not the locked runs; (ii) the DES Y5 preference is
itself a low/high-redshift calibration effect (split at z = 0.1), so "SUPPORTED on DES Y5" is weak; (iii) the TF-P
look-elsewhere count is three F values; (iv) **Union3 is the blind sample and must still be run.** Next step on the
PC: the three locked `ax_spa_latetwist_fF0.1930*_nlfix` runs.
