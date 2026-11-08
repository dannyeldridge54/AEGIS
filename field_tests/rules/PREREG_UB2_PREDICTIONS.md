# PRE-REGISTRATION UB-P: what the joined field predicts for UB-2 (from the UB-1 map)

Written 7 Nov 2026, 22:26 CT with AI assistance at Danny's request ("prep"); ranges filled from
`theory/ub1_map_region.json` (background only, no data) and locked 8 Nov **before any UB-2 fit result existed**
(checked on the PC: no `cmp_ub2B*.json`; the three UB-2 fits were on their first restarts; no UB-2 log was read). UB-2's own verdicts (`PREREG_UNIFY_DATA.md`) are
unchanged; this is an additional, sharper test.

## Why
UB-1 found one setting of the joined field (variant B) that does both jobs. If the field is real, the CMB/BAO/SN fit
(UB-2) should land inside the region UB-1 found **without being told to**: the data were never used to draw it.

## Predictions (from the UB-1 passing region; ranges cover both families the map found)
The map (random walk of 3,000 steps from the UB-1 point, acceptance 21%, plus 60 fresh starts) found a **main family**
(θ_i ≈ 2.4–2.9, |φ|_i ≈ 9–14; 5–95% ranges below) and a second **hilltop family** (θ_i ≈ 3.0, near the top of the
cosine, |φ|_i ≈ 25–27; 2 points, F ≈ 0.06). The locked ranges are the union, so neither family is favoured after the fact.

| Quantity at the UB-2 best fit | Predicted range |
|---|---|
| F during the early boost (angle width, M_Pl) | 0.057 to 0.177 |
| redshift of the boost peak z_peak | 2500 to 6000 |
| boost size f_peak | 0.031 to 0.125 |
| w0 today | -1.000 to -0.974 |
| dilaton slope κ | -0.42 to 0.15 |

Notes: the z_peak upper end (6000) and f_peak lower end (0.03) are UB-1 requirement edges, so those two are partly
built in; F, w0 and κ are not, and are the real predictions. The main family alone gives F 0.115–0.177 (median 0.139),
which matches the width range the earlier CMB fits preferred (0.12–0.17) without being fitted to it — reported here,
not scored.

## Rule (per supernova set; scored from each UB-2 best fit by re-solving its background with UB-1's code)
- **PREDICTION HOLDS** on a set if all five quantities lie inside their ranges; **PARTLY** if 3–4 do; **FAILS** if ≤ 2.
- Overall: HOLDS if it holds on at least 2 of 3 sets; FAILS if it fails on at least 2 of 3; otherwise MIXED.
- A UB-2 fit that is NO VERDICT is NO VERDICT here too. Reported at full size whatever the outcome.
