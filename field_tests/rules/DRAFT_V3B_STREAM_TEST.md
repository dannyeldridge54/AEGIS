# V3-B: dark matter falls differently from stars, test design for both coupling pictures (DRAFT, not locked)

**Status: DRAFT** (9 Nov 2026, V3 check-in). Nothing measured or scored. Companion to the locked
`PREREG_V3_STREAMS.md`, which stays as written. Theory: `theory/DM_COUPLING_PICTURE.md`.

## Predictions (one per picture; DM force = (1 + β_KK²) × gravity, stars feel gravity only)

| Model | Picture | Galaxy streams (Milky Way, Sgr) | Clusters |
|---|---|---|---|
| Spiral, S8-J (all dark matter coupled, as fitted) | A | β_KK = √2 β = 0.053–0.069; extra DM–DM pull 0.27–0.48% | same 2β² |
| S8-L, as the action reads it (angle = ultralight share, coupled at 0.816) | B | **β_KK ≈ 0** (angle smooth on < 400 kpc at 1.3–1.5 × 10⁻²⁵ eV) | small; only the angle share that clusters, angle–angle pull ×2.33 |
| Any model, B with a heavy (clustering) angle | B | mean β_KK as A, plus a ~7% extra pull on the 5–6% angle share inside each satellite | as A |

So the stream test separates the plain Spiral (signal ~0.06) from S8-L read as the action (null). The locked V3 rule
scores only the picture-A numbers.

## Published limits (searched 9 Nov; conversions to β_KK to be written down per paper before scoring)

| Paper | System | Reported | β_KK (our conversion, to check) | Reaches 0.053–0.075? |
|---|---|---|---|---|
| Kesden & Kamionkowski 2006 (astro-ph/0608095), Kesden 2009 (arXiv:0903.4458) | Sgr stream symmetry | forces > 10% of gravity excluded (would erase the leading tail) | β_KK² < 0.1, β_KK ≲ 0.3 | no |
| Carroll, Mantry, Ramsey-Musolf & Stubbs (arXiv:0807.4363) | Sgr, as used in the locked rule | β < 0.2 | 0.2 | no |
| Keselman, Nusser & Peebles 2009 (arXiv:0902.3452) | Sgr, strong forces | stream can stay symmetric for force ~ gravity if stars leave the halo | caveat, not a bound | no |
| Zamlung & Nusser 2025 (arXiv:2509.01713) | Fornax, N-body | β ≳ 0.6 destroys Fornax; ≲ 0.2 consistent (no confidence level) | F₅ = βF: β_KK² = β, β_KK ≲ 0.45–0.6 | no |

The best current limit is ~4–6× above the picture-A signal in β_KK (~20–35× in force). No Gaia-era stream paper
with a dark-matter-only force limit was found; Gaia DR3 stream papers constrain the halo shape, not this force.

## What to measure (if we ever run our own analysis; the locked rule relies on published ones)

1. **Leading/trailing asymmetry of the Sgr stream.** Observable: ratio of star counts and the mean orbital-energy
   offset of leading vs trailing debris, from Gaia DR3/DR4 proper motions plus spectroscopic velocities (H3, S5,
   DESI MWS). Signal under A: the satellite's halo is pulled ~0.3–0.5% harder than its stars; stars drift to the
   trailing side; the energy offset scales with β_KK² × (host mass/satellite mass) and must be computed in
   N-body models (Kesden-type), not guessed.
2. **Thin streams from globular clusters (GD-1, Pal 5, Jhelum).** No dark matter of their own, so they test the host
   only through orbits: under A they feel exactly gravity, the same as under ΛCDM. A null control: any "signal" here
   is a modelling error.
3. **Dwarf-galaxy streams with dark matter (Sgr, Orphan–Chenab, Tucana III).** Each gives an independent β_KK; the
   test needs at least two to beat Milky Way potential systematics (the LMC's pull on Orphan–Chenab must be in the
   model).
4. **Clusters (picture B only):** galaxy–dark-matter centroid offsets in merging clusters; only meaningful if the
   angle share clusters at cluster scales. Not designed further here.

## Reach (rough, stated as such)

A Kesden-type bound scales with how well the energy offset between the tails is measured. Going from β_KK ≈ 0.2–0.3
to 0.05 needs ~16–36× smaller force errors. Gaia DR4 proper-motion errors improve ~2× over DR3 and number counts
grow, so the statistical part may improve several-fold; the Milky Way potential and LMC modelling are the limit.
Our judgment: DR4 alone is unlikely to reach 0.05 in Sgr; a joint analysis of several dwarf streams might reach
~0.1. So the realistic near-term outcome for picture A is CANNOT TELL, and picture B predicts a null that cannot be
told apart from A until a bound below ~0.05 exists.

## Before any lock

- Write the per-paper β_KK conversions (above) out in full from each paper's definitions.
- Decide whether S8-L's stream prediction follows the code (A-like) or the action (null); the theory note says the
  action. If the action, S8-L needs a build with the coupling on the ultralight share before its numbers are used.
- Cost: literature only (cheap). An own N-body test would be days of PC time and is not proposed.
