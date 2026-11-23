# PREREG D2135: second PR4 high-ℓ likelihood (CamSpec NPIPE 12.6) from the PC data tables
Locked 2026-11-22 ~19:05 CT, before any fit.

**Why.** D2132 uses HiLLiPoP as the only PR4 high-ℓ likelihood. CamSpec NPIPE (Rosenberg, Gratton & Efstathiou 2022) is the independent PR4 high-ℓ likelihood. Both are PR4 (newest Planck), so this does not mix data releases. A Weave-vs-ΛCDM verdict that holds on both is robust to the choice of CMB likelihood.

**Data.**
- Files come from Danny's PC (ufe_data/packages/data/planck_NPIPE_CamSpec, version v1).
- cov.bin was split and rejoined. The SHA-256 of the cloud copy, f788df64…dd82, equals the PC original.
- The other file hashes are in /tmp/claude-0/camspec_sha.txt, copied below.
- Smoke test at a fiducial point: chi2 = 11116.6 over 9915 points, with nuisances at their reference values (not a fit).

**Runs.** These are identical to D2132 (same script, same priors, models L/W/C, SN ∈ {desdovekie, pantheonplus, union3}, BOBYQA best_of 2). The only change is planck_2020_hillipop.TTTEEE_bin → planck_NPIPE_highl_CamSpec.TTTEEE, with its nuisance parameters free under Cobaya's default priors. Run once each.

**Verdict rules (fixed now).**
- ΔAIC(W−L) = Δχ²_eff − 2, since W has 1 fewer free parameter: W fixes n_s and adds u_i, and L frees n_s. **The count must be re-checked from the actual free-parameter lists before scoring.**
- The combined ΔAIC from HiLLiPoP (D2132) and CamSpec (D2135) is called **"likelihood-robust"** only if both have the same sign on a given SN set and differ by less than 3.
- If they differ by 3 or more, the result is labelled **"CMB-likelihood dependent"**.
- No reruns to chase results. Code fixes go in DEVIATIONS, written before any rerun.
2c1f3a37e2e310b1 CamSpec_NPIPE/100x100_10.5_dust.dat
045a3bcaa0b4debf CamSpec_NPIPE/143x143_10.5_dust.dat
9ebff4056bb45970 CamSpec_NPIPE/143x217_10.5_dust.dat
35b990801f88af38 CamSpec_NPIPE/217x217_10.5_dust.dat
2cdc9435e3d62c2e CamSpec_NPIPE/CamSpecHM.paramnames
9adc3d2cba43c314 CamSpec_NPIPE/CamSpec_NPIPE_12_6_cl.dataset
16239eaed345956a CamSpec_NPIPE/CamSpec_NPIPE_12_6_cl_covinv_7ca1326fc793dc0c41bc8bbcbd8a148a.npy
ff9b1ea3b177eaf8 CamSpec_NPIPE/README.md
eeca4d3b07ca41de CamSpec_NPIPE/cib217.txt
f154d6d001dfdbc6 CamSpec_NPIPE/cl_ksz_148_trac.dat
11e194aa01a9a62d CamSpec_NPIPE/like_NPIPE_12.6_unified_data_ranges.txt
640a8f58fadbc730 CamSpec_NPIPE/like_NPIPE_12.6_unified_spectra.txt
3d7f8408c5931354 CamSpec_NPIPE/sz_x_cib_template.dat
c4cc9cff1f0b3ca4 CamSpec_NPIPE/tsz_143_eps0.50.dat
