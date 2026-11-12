# DRAFT for Danny's review: flagship note v5 section and Zenodo v5 description

AI-assisted draft, 12 Nov 2026. Nothing here is published. Every number comes from a committed result file, listed
under each item. Publishing to Zenodo or arXiv happens only on Danny's word.

---

## Proposed new section: "Self-checks of FLAG-1 (pre-registered)"

Before any further claims were made, FLAG-1 (κ = 1, β_eff ≈ 0.04) was put through a set of self-checks, each written
and locked before it was run (`field_tests/rules/PREREG_SELFCHECK.md`, `PREREG_DESI_MOCK.md`, `PREREG_DESI_MOCK_CMB.md`).
None of them was rerun or changed after its result.

**Is the quoted significance right? (V1, 200 simulated ΛCDM universes.)** Only 3 of 200 mock ΛCDM universes gave FLAG-1
an advantage as large as the real data (compressed likelihood, Δ_real = −5.32): p_emp = 0.015 (68%: 0.009–0.026), against
p = 0.021 from Wilks' theorem. They agree to within the pre-set factor of 2 (WILKS ADEQUATE), so the quoted local
significances (2.2–2.8σ) stand. After the look-elsewhere correction (N = 66 tests) the global significance is 0.2–1.0σ
(V7), or 0.5σ with V1's empirical p.
Limitation: background-only, with a compressed CMB. *(field_tests/results/selfcheck_v1.json)*

**Is the preference driven by supernovae? (V2.)** With every supernova likelihood removed, FLAG-1 still fits better,
but by less: Δχ² = −2.75 (−4.71 with Pantheon+), between the pre-set bands (WEAK). The remaining preference comes
mainly from DESI DR2 BAO; the DES Y6 S8 term pulls the other way. *(field_tests/results/selfcheck_v2.json)*

**Does FLAG-1 grow structure correctly? (V3, DESI DR1 full-shape fσ8, six tracers.)** Both FLAG-1 (χ² 5.25, p = 0.51)
and ΛCDM (χ² 5.10, p = 0.53) are CONSISTENT; the difference is 0.16 (Pantheon+), and 0.06 and 0.13 for Dovekie and
Union3. The data do not separate them. *(selfcheck_v3.json)*

**Cluster S8 (V4).** FLAG-1's S8 (0.825) is closer than ΛCDM's to eRASS1 (0.86 ± 0.01; Δpenalty −8.8) and slightly
further from SPT clusters (0.795 ± 0.029; +0.6). Both PASS the pre-set ≤ +2 bound. *(selfcheck_v4_v5.json)*

**Dark-matter fifth force (V5).** β_eff = 0.038–0.045 gives an extra dark-matter attraction of 2β² ≈ 0.3–0.4% of
gravity, inside the Sagittarius-stream bound (10%) and within 1σ of the Planck-era coupled-quintessence fit
(β = 0.036 ± 0.016, Pettorino 2013). PASSES. *(selfcheck_v4_v5.json)*

**Would DESI "see" evolving dark energy in a FLAG-1 universe? (DESI-MOCK, DESI-MOCK-CMB.)** A DESI-style ΛCDM vs w0wa
analysis of a noiseless FLAG-1 universe finds w0 = −0.83, wa = −0.46 at 2.9σ with BAO + CMB + SNe (DESI DR2 real:
2.8σ) and 1.0σ without SNe. The full CMB likelihoods agree with the compressed CMB to within 0.03σ. Reading:
REPRODUCES DESI'S SIGNAL. Caveat: FLAG-1 was fitted to DESI DR2, so this is a consistency check, not a prediction. A
held-out version (FLAG-1 fitted without DESI, then asked to predict it) is locked as `PREREG_DESI_HOLDOUT.md` and is
pending. *(field_tests/desi_mock/desi_mock_result.json, mock_cmb_result.json)*

**Does the preference hold on older data? (DATA-GEN.)** Refitting on earlier generations of late-time data, FLAG-1 is
disfavoured on the SDSS era (Δχ² +2.76 with 6dF/SDSS DR7/DR12 BAO + JLA; +6.46 with SDSS DR16 + Pantheon) and favoured
only with DESI (−2.47 DR1; −4.71 DR2). The coupling stays at β ≈ 0.04 throughout. With the Planck-only CMB the DESI-era
preference is −3.91. Reading: DOES NOT HOLD. *(field_tests/results/datagen.json)*

**Where in DESI does it live? (M1, bin jackknife, compressed likelihood.)** Dropping DESI's z ≈ 0.71 LRG bin takes the
preference from −5.32 to −2.10; every other single bin leaves it between −4.9 and −6.1. Reading: PARTLY CONCENTRATED.
This is the bin where DESI and SDSS differ in transverse distance (D_M about −0.9% vs +2.9% relative to ΛCDM, about
1.8σ apart), and the bin that published analyses find drives DESI's w0 > −1 signal (arXiv:2504.04417).
*(missing_piece_m1.json)*

**A direct fifth-force test (M2, E_G).** FLAG-1 predicts E_G (lensing compared with galaxy velocities) about 4.8% above
ΛCDM. Against ACT DR6 × BOSS (errors ~17%) the two cannot be told apart (Δχ² +0.81, NO DISCRIMINATION); about ±2.4% is
needed. The FLAG-1 E_G curve is frozen as a forecast (`PREREG_EG_FORECAST_FLAG1.md`). *(missing_piece_m2.json)*

**Summary.** FLAG-1 passes every check that could have ruled it out, and its local significance is correctly
calibrated, but it is not significant globally, its preference appears only with DESI-era data, and most of it sits in
one DESI redshift bin where DESI and SDSS disagree. Whether that is physics or a survey-level difference is set out
as frozen tests for DESI DR3 and the next independent survey (`PREREG_WATCH_DESI_SDSS_SPLIT.md`).

*Still to add when finished: DESI-HOLDOUT (FLAG-1 fitted without DESI, predicting it), M3 (DESI vs SDSS residual map),
the FLAG-1 MCMC error bars, and V6 (Planck PR4) if it is run.*

---

## Proposed Zenodo description for flagship note v5

> Version 5 adds pre-registered self-checks of FLAG-1, the coupled-dilaton "Spiral Twist" with κ = 1. A 200-mock
> calibration confirms the local significance (2.2–2.8σ; global 0.2–1.0σ after a 66-test look-elsewhere correction). The
> preference weakens without supernovae (Δχ² −2.75), is absent on SDSS-era data (+2.76, +6.46), and sits mostly in
> DESI's z ≈ 0.71 bin, where DESI and SDSS disagree. DESI DR1 full-shape growth, E_G, cluster S8 and dark-matter
> fifth-force bounds are all consistent. A DESI-style analysis of a FLAG-1 universe recovers DESI's evolving-dark-energy
> signal (w0 −0.83, wa −0.46, 2.9σ), as a consistency check, because FLAG-1 was fitted to DESI. Conclusion: FLAG-1 is a
> viable, honestly tested alternative that the data do not prefer over ΛCDM; its frozen predictions for DESI DR3,
> E_G and the next independent BAO survey will decide it. Every rule was locked before its test was
> run; the code, rules and results are at github.com/dannyeldridge54/AEGIS. AI-assisted.

## Note on the stale v3 record
The v3 Zenodo record's description still reads as of 11 Nov 04:30 CT. If Danny wants it corrected, the smallest honest
fix is one line at the top: "Superseded by v4 (look-elsewhere correction) and v5 (self-checks); see the newest version."
