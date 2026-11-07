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
| Test | Result | Verdict |
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
| Potential power n = 3 vs 2, 4 | n = 2: no better than ΛCDM; n = 4: tie | **n = 3 stays** |

**Failed and dropped (kept on record):** N = 9 width on SPT-3G; silver-ratio angle; pure torsion width F = √(3/2) M_Pl
for the early field; torsion-natural coupling β = 0.816 (all dark matter); minimal-field birefringence; running-F
unification with constant W.

## Open (in progress)
| Test | State |
|---|---|
| **SF2** does the BI angle matter? (β = 0 vs free) | running on the PC (`field_tests`, rule locked 7 Nov) |
| **FP** Fingerprint (Holst) vs cosine (Nieh–Yan) | running on the PC (gate passed) |
| **UB-1** can the coupled axion–dilaton do both jobs? (background only) | rule locked 7 Nov 23:45 UTC; runs on the PC right after SF2/FP, before the bracket |
| BR bracket (early-field variants) | 2 of 6 done; the other 4 start on the PC after UB-1 |
| **S8WL Part 2** full DES Y3 shear likelihood | rule locked 7 Nov; PC, needs CosmoSIS |
| Stage-3 P-ACT bracket | after BR |

## Where things are
- Run and score every test: `field_tests/` (`STATUS.md`, `score.py`, `run_pc.sh`). PC results merged 7 Nov (PR #13).
- Locked rules: `field_tests/rules/` and `cmb-fit/PREREG*`; theory checks: `theory/` (audit `THEORY_AUDIT_2026-11-07.md`).
- Cloud refits and tournament: `aegis-Kronos-syndyr/research/refit/`.

## Superseded (do not use these numbers)
f_EDE = 0.078 / H₀ = 70.6 (withdrawn, unconverged engine); the N = 9 "width module" as a working model;
`MODEL_v2.md`, `ufe-v2/UFE_MODEL.md`, the Oct 30 FINISH_PLAN / MATH_SHEET on the Desktop; "TF-P never ran" (it ran
3 Nov; results were only on the PC until 7 Nov).
