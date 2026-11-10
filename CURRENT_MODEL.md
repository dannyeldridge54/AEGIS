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
| **S8-L** light angle (option 4): the angle share f = β_eff/0.816 as an ultralight field, +1 parameter (mass); rule locked 8 Nov, scored by spiral_l_score.py | Δχ² vs ΛCDM −12.74 / −13.68 / −14.61 (P+ / Dovekie / Union3); S8 0.817 / 0.817 / 0.819 (ΛCDM 0.816–0.818, SF 0.833–0.840); DES Y6 penalty vs ΛCDM −0.10 / +0.12 / +0.45 (limit +2); vs SF Δχ² −3.52 / −2.24 / −1.73, ΔAIC −1.52 / −0.24 / +0.27; mass ≈ 1.3–1.5×10⁻²⁵ eV (approx.); f 0.062–0.065 | **BEATS ΛCDM; LENSING FIXED** (DES Y6 S8 test, 8 Nov). Part 2 (full DES Y3 shear, reported): Δ_WL +15.74 / +15.45 / +14.47, **OVER** (equal effort, 7 tries each). Caveat, measured: halofit gives S8-L ~15% more nonlinear power than the Spiral at k ≈ 0.1 h/Mpc where the linear power agrees to 0.3% (s8l_nonlinear_check.txt); halofit is not calibrated for an ultralight share, so this lensing number is not reliable either way |
| **S8-LNL** S8-L on the full DES Y3 shear with axionHMcode (built for ultralight fields) on both sides (PREREG_S8L_NONLINEAR.md, locked 8 Nov; deviations D1–D4 logged before any shear χ², D4 approved by Danny) | Δ_WL +2.65 / +3.21 / +2.57 (P+ / Dovekie / Union3; limit +2; 7 tries each side). The halofit run (+15.74 / +15.45 / +14.47) was an artifact of the wrong nonlinear model; it stays on record | **NOT FIXED** (0 of 3 pass). Close to the plain Spiral's +2.6 to +4.0 (that one used halofit) |
| **S8-A** coupling on the light angle, as the action says (PREREG_S8A_ANGLE.md, locked 9 Nov; G-A-PC passed 0.04–0.056) | Δχ² vs ΛCDM −10.35 / −13.94 / −15.05; DES Y6 S8 penalty +0.77 / −0.88 / −0.72 (S8 0.821 / 0.811 / 0.813, angle counted); vs S8-L +2.39 / −0.26 / −0.43 (same parameter count); angle share f 5.4–7.0%, mass ≈ 1.2–3.7 × 10⁻²⁵ eV, H0 67.7 / 67.5 / 66.8, κ 0.80 / 0.92 / 1.09 | **BEATS; LENSING FIXED** on the compressed DES Y6 S8 test (3 of 3). Caveat: this is the same S8-number test S8-L passed before failing the full-shear tests; the DES Y3 and KiDS-Legacy full-shear reruns are the real check and are not yet run |
| **LATE-BASE** S8-A full shear + base choice (PREREG_LATE_BASE.md, locked 9 Nov) | DES Y3 Δ_WL +1.76 / +2.32 / +2.76 (1 of 3 passes); KiDS-Legacy Δ +2.96 / +10.11 / +11.30 (0 of 3) | **OVER on both surveys: LENSING NOT FIXED** by the full shear. **The flagship (FLAG-1) stays the late base.** JOINT-SHEAR: see next row |
| **JOINT-SHEAR** S8-A vs ΛCDM refit with DES Y3 shear inside (PREREG_JOINT_SHEAR.md, locked 9 Nov) | Gate G-JS failed twice: the shear-χ² stand-in missed held-out points by up to 3.8 (S8-A) / 2.2 (ΛCDM) with 32 points, and up to 1.8 / 2.0 after the allowed 8 more per model (limit 0.5) | **NO FITS, NO VERDICT** (as locked). Per the agreed plan, no third lensing round: **lensing is written up as an OPEN PROBLEM** |
| **TWOFIELD** early n = 3 field + flagship dilaton (PREREG_TWOFIELD.md, locked 9 Nov; D1 HALOFIT fix before the gate rerun) | Δ vs FLAG-1 −1.06 / −1.00 / +0.62; vs ΛCDM+S8 −5.68 / −6.89 / −7.04; H0 67.76 / 67.48 / 67.63 (FLAG-1 67.16 / 67.36 / 67.02); f (fraction_axion_ac) 0.037 / 0.025 / 0.040; S8 0.828 / 0.822 / 0.825 | **EARLY FIELD NOT WORTH IT** (3 of 3: Δ_F > −2). Still **SURVIVES** vs ΛCDM+S8 (3 of 3), only because the flagship part does. **H0 does NOT rise** (+0.6 / +0.1 / +0.6, need ≥ 1.0). The data push the early field small; the flagship stays the model |
| **TWIST-ME** flagship + early electron mass (PREREG_TWIST_ME.md, locked 10 Nov) | Δ vs FLAG-1 −0.55 / −0.33 / −0.15; vs ΛCDM+S8 −5.25 / −6.34 / −7.84; m_e/m_e0 1.009 / 0.998 / 1.002; H0 67.88 / 67.14 / 67.18 (FLAG-1 67.16 / 67.36 / 67.02) | **NOT WORTH IT** (3 of 3). Still **SURVIVES** vs ΛCDM+S8 (flagship part). **H0 does NOT rise.** With the dilaton already in, the data do not ask for a heavier early electron (where m_e rose, β_eff fell, 0.041 → 0.028). The m_e + α draft is dropped as that rule says |
| **TWIST-DR** flagship + dark radiation ΔN_eff + running α_s (PREREG_TWIST_DR.md, locked 10 Nov) | Pantheon+ fit died (NO VERDICT); Dovekie / Union3: Δ vs FLAG-1 −1.04 / −0.47; vs ΛCDM+S8 −7.05 / −8.16; ΔN_eff 0.000 / 0.000 (at the prior edge); α_s 0.0040 / 0.0040; H0 67.24 / 67.10 | **NOT WORTH IT** (2 of 3). **H0 does NOT rise**; the data push dark radiation to zero. Still SURVIVES vs ΛCDM+S8 (flagship part) |
| **FLAG-1 flagship**: Spiral Twist with κ fixed at 1, fitted with the DES Y6 S8 term (PREREG_FLAGSHIP.md, locked 9 Nov; not blind, stated) | Δχ²_min vs ΛCDM+S8 −4.71 / −6.01 / −7.69 (P+ / Dovekie / Union3); vs S8-J raw χ² +2.62 / +2.13 / +0.55, score (χ² − 2 each) sum 6039.24 vs S8-J 6039.95; β_eff 0.041 / 0.045 / 0.038, H0 67.2 / 67.4 / 67.0, S8 0.825 / 0.828 / 0.825, w0 −0.87, wa −0.20 | **SURVIVES (Δ ≤ −4 on 3 of 3)**; **FLAGSHIP KEPT** (one fewer parameter pays for its χ² cost by 0.71). This is the model carried forward; predictions frozen in theory/fpc_*kappa1*_s8y6.json. Lensing reruns (KiDS, DES Y3) at these best fits not yet run |
| **SIMPLIFY-L** can the Spiral's slope κ be fixed? (PREREG_SIMPLIFY_LATE.md, locked 8 Nov; 2 candidates; score χ² − 2 per fit) | K1 κ = 0.8165: χ² −0.40 / −0.39 / +1.87 vs free; K2 κ = 1: −0.13 / +0.09 / +0.44 (P+ / Dovekie / Union3). Summed scores: free 6025.52, K1 6020.60, K2 6019.91 | **WINNER K2: κ = 1** (beats free κ by 5.60 ≥ 2; K1 by 0.69 only; two candidates tried). Flag (rule's check): fixed-κ χ² below free by 0.13–0.40 on P+ and Dovekie, so the stored free-κ fits are not fully converged; reported, nothing rerun. Note: the rule text quotes free κ 0.86 / 0.97 / 1.17; the stored fits it scores have 0.83 / 0.87 / 1.05 (text error in the rule, left as locked) |
| **V7 look-elsewhere** (PREREG_V7_LOOK_ELSEWHERE.md, locked 8 Nov; N = 64 late/early-field variants tried on the same data; Šidák, conservative) | Spiral local 2.6 / 2.9 / 3.2σ → global 0.7 / 1.3 / 1.7σ; S8-L local 2.8 / 2.9 / 3.1σ → global 1.1 / 1.3 / 1.5σ (P+ / Dovekie / Union3) | **NOT SIGNIFICANT AFTER LOOK-ELSEWHERE** (both). Quote local and global together from now on |
| BR bracket (early-field variants), round 1 (PREREG_BRACKET.md; score = deep χ² − 2) | all 6 done (4 restarted from scratch 8 Nov, Danny's call): θ 2.414 F8 2430.00, F9 2430.72, F10 2431.34; θ 2.777 F8 2426.77, F9 2426.72, F10 2427.06; locked fit 2428.48 (edelockP_deep, as bracket.py reads it; 2428.83 was the non-deep fit) | **Round 1: θ 2.777 F9, F8, F10 advance** (the 3 lowest; bracket.py stage 2). Round 2 (DES Y5 + Dovekie + Union3, 9 fits): START_BRACKET_R2.bat ready on the PC, 8 Nov; a winner must beat the locked fit's summed value by ≥ 2 |
| BR bracket, round 2 (DES Y5 + Dovekie + Union3; score = χ² − 2 per set) | sums: θ 2.777 F9 6376.32, F8 6376.41, F10 6376.96; locked fit 6382.01 (per set 2672.82 / 2658.01 / 1051.18; F9 2670.79 / 2656.20 / 1049.32) | **WINNER θ 2.777, F9** (beats the locked fit by 5.69 ≥ 2). Honest reading: the margin is the AIC credit for fixing θ (−2 × 3); raw χ² is +0.31 worse in sum, so fixing θ at the fitted value and the width at torsion/9 costs nothing in fit. Six candidates were tried; the locked result stands beside it. Round 3 (P-ACT, S8 A/B; reported only) started 8 Nov 17:06 CT |
| **S8WL Part 2** full DES Y3 shear likelihood | rule locked 7 Nov; run in the cloud. Locked Twist Δ_WL = +1.14 **PASSES** (limit +2); Spiral +2.57 / +3.47 / +3.99 **OVER**; UB-2 joined field −0.37 / 0.00 / +0.14 **PASSES** (equal effort, all pairs done 8 Nov) |
| **S8-J Part 2** S8-J joint Spiral on the full DES Y3 shear likelihood (same locked Part 2 rule, equal effort: 7 tries each side) | Δ_WL +0.79 / +2.01 / +1.38 (P+ / Dovekie / Union3; limit +2) | **MIXED: PASSES 2 of 3, Dovekie OVER by 0.01** (8 Nov; minimiser spread between tries ~1 unit, reported as is) |
| **S8-J on KiDS-Legacy** full shear (PREREG_KIDS_LEGACY_SHEAR.md, locked 8 Nov; gate passed 124.266 vs 124.291; KiDS baseline HMcode-2020 + feedback on both sides, D1) | Δ_KiDS −0.41 / −0.26 / −0.47 (P+ / Dovekie / Union3; limit +2; equal effort, 5 tries each side) | **PASSES on KiDS-Legacy, 3 of 3** (S8-J fits KiDS slightly better than ΛCDM). |
| **Spiral on KiDS-Legacy** (same rule and settings) | Δ_KiDS +0.46 / +0.57 / +1.15 (limit +2; 5 tries each side) | **PASSES on KiDS-Legacy, 3 of 3.** It was OVER on the full DES Y3 shear (+2.6 to +4.0): by the rule, passing KiDS but not DES is reported as a question about survey systematics, not as a fix |
| **S8-L on KiDS-Legacy** (same rule; both sides axionHMcode basic + BAO damping, no baryon feedback, logT_AGN fixed 8.0, the limitation the rule anticipates) | Δ_KiDS +6.80 / +7.98 / +7.81 (limit +2; 5 tries each side, spread ≤ 0.014) | **OVER, 0 of 3.** Fails both surveys (S8-LNL on DES Y3 also NOT FIXED): by the rule, S8-L's lensing tension reads as real |
| Stage-3 P-ACT bracket | after BR |

## Where things are
- Run and score every test: `field_tests/` (`STATUS.md`, `score.py`, `run_pc.sh`). PC results merged 7 Nov (PR #13).
- Locked rules: `field_tests/rules/` and `cmb-fit/PREREG*`; theory checks: `theory/` (audit `THEORY_AUDIT_2026-11-07.md`).
- Cloud refits and tournament: `aegis-Kronos-syndyr/research/refit/`.

## Superseded (do not use these numbers)
f_EDE = 0.078 / H₀ = 70.6 (withdrawn, unconverged engine); the N = 9 "width module" as a working model;
`MODEL_v2.md`, `ufe-v2/UFE_MODEL.md`, the Oct 30 FINISH_PLAN / MATH_SHEET on the Desktop; "TF-P never ran" (it ran
3 Nov; results were only on the PC until 7 Nov).
