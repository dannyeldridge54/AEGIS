# DATA-GEN: does the flagship's preference hold on older generations of data?

**Status: LOCKED** on Danny's word ("Yes I want to see if we use old sets if it holds", 11 Nov 2026, 10:12 CT). He
was answering a proposal to run this as a locked rule. Time and fingerprint are in the .sha256 file. AI-assisted.

**Question.** FLAG-1 was found on the newest data (DESI DR2 BAO + Pantheon+). If the coupling is real, refitting on
older, independent generations of late-time data should still prefer it, or at least not oppose it. If the preference
belongs to one dataset, it should vanish or reverse on the older ones.

**Not blind.** Known at writing:
- DESI DR1 already showed an evolving-dark-energy preference, weaker than DR2's.
- Pre-DESI BAO (SDSS) showed little preference.

Prior expectation, stated before any run: G1 and G2 weak or none, G3 intermediate. Generations share some supernovae
(JLA ⊂ Pantheon ⊂ Pantheon+ in part), so the SN axis is not fully independent. SDSS and DESI BAO are independent
surveys.

## Fits (PC; FLAG-1 κ = 1 with β_eff free, and ΛCDM halofit)

All fits:
- keep the current CMB set (Planck low-ℓ, ACT DR6 + P-ACT cut, ACT DR6 lensing, SPT-3G D1), except fit C;
- keep the DES Y6 S8 term;
- keep the same priors and build, best of 4;
- start each model from its own stored Pantheon+ s8y6 minimum.

Only the late-time data change:

| Gen | Era | BAO (Cobaya names) | SNe |
|---|---|---|---|
| G1 | ~2016 | `bao.sixdf_2011_bao`, `bao.sdss_dr7_mgs`, `bao.sdss_dr12_consensus_bao` | JLA (`sn.jla`) |
| G2 | ~2020 | `bao.sdss_dr7_mgs`, `bao.sdss_dr12_lrg_bao_dmdh`, `bao.sdss_dr16_lrg_bao_dmdh`, `bao.sdss_dr16_bao_elg`, `bao.sdss_dr16_qso_bao_dmdh`, `bao.sdss_dr16_baoplus_lyauto`, `bao.sdss_dr16_baoplus_lyxqso` | Pantheon (`sn.pantheon`) |
| G3 | 2024 | `bao.desi_2024_bao_all` | Pantheon+ |
| G4 | 2025 | stored fits (DESI DR2 + Pantheon+); no refit | Pantheon+ |
| C | CMB swap | DESI DR2 | Pantheon+ |

Fit C uses the Planck-only CMB (`_planckfull`: Planck 2018 low-ℓ, high-ℓ TTTEEE lite and Planck lensing) in place of
ACT/SPT.

**Fit names:** `ax_spa_spiraltwist_kappa1_nlfix_gen<1|2|3>_s8y6`, `ax_spa_lcdm_halofit_gen<1|2|3>_s8y6`, and `..._cmbplanck_s8y6` for C.

- If a listed likelihood's data are missing on the PC, they are copied from the cloud packages (same Cobaya
  versions); nothing is downloaded from outside without Danny's permission.
- Runs only after SELFCHECK V2 on the PC.

## Readings

Δ_g = χ²(FLAG-1) − χ²(ΛCDM) and β_g, for g = G1, G2, G3, G4 (stored: −4.71, β 0.041) and C.
- **DOES NOT HOLD:** Δ > +2 in any generation (FLAG-1 is disfavoured there).
- **HOLDS AND STRENGTHENS:** Δ ≤ 0 in every generation, β_eff > 0.01 in G3 and G4, and Δ_G4 ≤ Δ_G1 − 2.
- **HOLDS (FLAT):** Δ ≤ 0 everywhere and β_eff > 0.01 in G3 and G4, but no strengthening.
- **NEWEST-DATA ONLY:** Δ > −1 in both G1 and G2 while Δ ≤ −2 in G3 and G4. The preference appears only with DESI.
  Reported as a question about DESI-era data, not as a failure.
- **MIXED:** otherwise.

Fit C is reported separately: Planck-only CMB vs ACT/SPT, the same Δ and β.

**Also reported:** β_g, H0, S8 and per-likelihood χ² for every fit; the β_g track across generations.

## What may not happen

- No change of dataset lists, generation boundaries, bands or starts after any result.
- No dropping of a generation.
- Each fit is reported once; deviations are logged before any rerun.
- Counted +1 in V7.
