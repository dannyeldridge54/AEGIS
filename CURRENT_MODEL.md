# CURRENT MODEL: read this first (updated 7 Nov 2026)

**One page, the source of truth.** Anything elsewhere that disagrees with this page is older; older pages carry a
"SUPERSEDED" banner pointing here. Every number below is from a locked test (rule hashed before its data).

## The model: the UFE / Spiral Twist
The Barbero–Immirzi (BI) field in N = 1 supergravity is an **axion–dilaton pair** on a hyperbolic field space with
fixed curvature: kinetic mixing λ = −2√(2/3) (α = 1, not fitted). It couples through the **Nieh–Yan** term (decided
7 Nov; `theory/COUPLING_CHOICE_NIEH_YAN.md`), so its potential is the plain cosine and F = (4/π)√(3/2) M_Pl at a
Planck-length Nieh–Yan scale. Two roles:
- **Late (dark energy, the Spiral):** exponential dilaton (slope κ) + the BI angle as a small fraction f of the dark
  matter, β_eff = 0.816 f. Two dark-energy settings, like w0–wa.
- **Early (the Locked Twist):** n = 3 cosine early dark energy, onset locked to matter–radiation equality.
- Not unified yet: one field doing both roles fails with the derived potential (`theory/dilaton_running_F.py`).

Latest public record: Nov 3 "UFE/Spiral Twist update" (supplement to Zenodo v3 doi:10.5281/zenodo.23867116; theory note
doi:10.5281/zenodo.23899237).

## Locked results
| Test | Result | Verdict (rule labels; see field_tests/WORDING_STANDARD.md for definitions) |
|---|---|---|
| **SF** Spiral vs ΛCDM / w0–wa: Pantheon+, Dovekie, Union3 | −9.22 / +0.73; −11.44 / +1.80; −12.88 / +2.12 | **BEATS ΛCDM**, **COMPETITIVE** with w0–wa |
| SF implied angle share f | 5.2–5.9% (β_eff 0.042–0.049) | under the 9% bound |
| SR-B2 (is SF DESI-driven?) | Pantheon+, Dovekie DESI-driven; Union3 partly | reported |
| SR-R3 (cold restarts) | all three stable | reported |
| **TF-P** F = 1.559 fixed (Nieh–Yan) | DES Y5 D 0.00, G −7.42 | **SUPPORTED** (3-value look-elsewhere); Union3 DISFAVOURED, Pantheon+ CONSISTENT (information) |
| TF F = √(3/2), √6 | DES Y5 | both **DISFAVOURED** |
| Early field, fair Planck / blind P-ACT | −4.70 / −7.23 | pass |
| Early field, three SN sets | −4.55 / −5.08 / −4.91 | pass |
| Early field vs w0–wa (combined CMB) | −5.63 vs −10.89 | loses to w0–wa |
| Weak lensing S8 penalty | 2.87 (DES+KiDS-1000) / 0.75 (KiDS-Legacy) | **TIE** overall |
| **S8-WL Part 1**, DES Y6 shear (S8 0.798) | Locked Twist 2.86; Spiral 4.17 / 4.87 / 6.97 | **OVER** for all (limit 2); reported beside the verdict |
| **SF2** does the BI angle matter? (β = 0 vs free; Pantheon+ / Dovekie / Union3) | removing the angle costs Δχ² +8.53 / +8.73 / +11.70; β = 0 alone vs ΛCDM −0.70 / −2.72 / −1.19 | **ANGLE NEEDED** (7 Nov) |
| **FP** Fingerprint (Holst) vs cosine (Nieh–Yan), same engine | Δχ²_eff = +0.86 (sinh worse) | **cannot tell apart yet**; no coupling preference |
| **UB-1** can one coupled axion–dilaton do both jobs? (background, no data) | locked code: FAIL (A and B); D1 integrator fix: **B PASS** (κ = −0.145: bump 3.2% at z ≈ 5,800, quiet, w0 = −0.997, Ω_m 0.295), A FAIL | **PASS only with the extra slope κ (D1)**; the derived potential (A) fails; dilaton barely moves (|φ| 12.4 → 12.1) |
| **UB-1b** derived potential with W = W0 e^{bΦ} (b free), background only | closest point misses by 0.038 (peak at z = 1,930, just below 2,000; Ω_m = 0.330, just above 0.33), b = 2.80 | **FAIL** (D1b-1: same search run in parallel) |
| **UB-2** one field vs Planck 2018 + DESI + SN (variant B, 4 extra parameters, best of 4 restarts each) | Δχ² vs ΛCDM −0.69 / −5.96 / −1.93; vs w0–wa +8.42 / +5.87 / +13.09 (ΔAIC +12.4 / +9.9 / +17.1); stored Spiral pieces −9.22 / −11.44 / −12.88 | **vs ΛCDM MIXED; vs w0–wa NOT COMPETITIVE; DOES NOT UNIFY** (8 Nov) |
| **UB-P** does UB-2 land where UB-1 predicted? (locked 05:33 UTC, before any UB-2 result) | Pantheon+: 1 of 5 inside (peak at z ≈ 60,000, κ −0.58); Dovekie: 3 of 5 (w0, κ outside); Union3: 4 of 5 (f_peak 0.023 below 0.031) | **MIXED** (8 Nov) |
| Potential power n = 3 vs 2, 4 | n = 2: no better than ΛCDM; n = 4: tie | **n = 3 stays** |

**Failed and dropped (kept on record):** N = 9 width on SPT-3G; silver-ratio angle; pure torsion width F = √(3/2) M_Pl
for the early field; torsion-natural coupling β = 0.816 (all dark matter); minimal-field birefringence; running-F
unification with constant W.

## Open (in progress)
| Test | State |
|---|---|
| **S8-J** Spiral and ΛCDM refit with DES Y6 S8 (NLA, 0.798) in the likelihood; best of 4 (ΛCDM best of 2+2, D3) | Δχ² vs ΛCDM −7.32 / −8.14 / −8.23 (P+ / Dovekie / Union3); lensing cost +0.28 / +0.88 / +1.64; S8 0.822 / 0.826 / 0.827 vs ΛCDM 0.814–0.816; β_eff 0.037–0.042 (SF 0.042–0.049) | **SURVIVES LENSING** (Δχ² ≤ −4 on 3 of 3; 8 Nov; deviations D1–D3) |
| **S8-L** light angle (option 4): the angle share f = β_eff/0.816 as an ultralight field, +1 parameter (mass) | engine built and code-checked (σ8 equal to 2×10⁻⁸); no-data check: S8 −0.003 at a_c = 10⁻⁵, −0.035 at 10⁻⁴·⁵; **rule locked 8 Nov**; PC: build, gate G-L, then 3 fits |
| BR bracket (early-field variants) | 2 of 6 done: θ 2.414 F8 χ² 2432.00 (score 2430.00), F9 2432.72 (2430.72), vs locked fit 2428.83, so both lose so far. The other 4 (θ 2.414 F10, θ 2.777 F8/F9/F10) stopped part-way at about 04:40–05:00 UTC 8 Nov when their windows were closed. The rule says failed jobs are not re-run; whether a closed window counts as failed is Danny's call |
| **S8WL Part 2** full DES Y3 shear likelihood | rule locked 7 Nov; run in the cloud. Locked Twist Δ_WL = +1.14 **PASSES** (limit +2); Spiral +2.57 / +3.47 / +3.99 **OVER**; UB-2 joined field −0.37 / 0.00 / +0.14 **PASSES** (equal effort, all pairs done 8 Nov) |
| **S8-J Part 2** S8-J joint Spiral on the full DES Y3 shear likelihood (same locked Part 2 rule, equal effort: 7 tries each side) | Δ_WL +0.79 / +2.01 / +1.38 (P+ / Dovekie / Union3; limit +2) | **MIXED: PASSES 2 of 3, Dovekie OVER by 0.01** (8 Nov; minimiser spread between tries ~1 unit, reported as is) |
| Stage-3 P-ACT bracket | after BR |

## Where things are
- Run and score every test: `field_tests/` (`STATUS.md`, `score.py`, `run_pc.sh`). PC results merged 7 Nov (PR #13).
- Locked rules: `field_tests/rules/` and `cmb-fit/PREREG*`; theory checks: `theory/` (audit `THEORY_AUDIT_2026-11-07.md`).
- Cloud refits and tournament: `aegis-Kronos-syndyr/research/refit/`.

## Superseded (do not use these numbers)
f_EDE = 0.078 / H₀ = 70.6 (withdrawn, unconverged engine); the N = 9 "width module" as a working model;
`MODEL_v2.md`, `ufe-v2/UFE_MODEL.md`, the Oct 30 FINISH_PLAN / MATH_SHEET on the Desktop; "TF-P never ran" (it ran
3 Nov; results were only on the PC until 7 Nov).
