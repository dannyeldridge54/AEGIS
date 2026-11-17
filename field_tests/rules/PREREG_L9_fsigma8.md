# PREREG L9 — Janus-LT growth vs DESI DR1 full-shape fσ8 (ShapeFit compressed ratios)
Locked 2026-11-17 before any L9 number. Data [literature, fetched arXiv html 2411.12021v5]: Table 9 ShapeFit-only fσ_s8/(fσ_s8)_fid —
BGS 0.80±0.20 (z 0.295), LRG1 1.09+0.12−0.14 (0.510), LRG2 1.05±0.12 (0.706), LRG3 0.96+0.11−0.10 (0.919), ELG2 0.95+0.11−0.08 (1.317),
QSO 1.16±0.12 (1.491); Table 11 fiducial fσ8: 0.4723, 0.4733, 0.4608, 0.4398, 0.3944, 0.3750. Mock/fiducial cosmology (stated for mocks; App. C
says "Planck-ΛCDM", Table 6 row 1 not fetched — assumption that they are the same): ω_c 0.1200, ω_b 0.02237, h 0.6736, σ8 0.811355, n_s 0.9649.
Model: fσ8(z) = f(z)·σ8,0·D(z)/D(0), f, D from tools/janus_lt/growth.py (Janus-LT, validated D1027), mν = 0. Amplitude σ8,0: [referee] CAMB 2.0.5
for the tested cosmology with A_s = 2.1e-9, n_s = 0.9649 (stated choice; only the shape of growth is Janus-LT's own). Errors symmetrised
(mean of ±); bins treated as independent (separate tracers; stated simplification).
C0 (self-check): Janus-LT at the fiducial cosmology with σ8,0 = 0.811355 reproduces Table 11 within 1% at all six z (1% allows for the
unstated mν/N_eff of the fiducial). C1 (data): χ² of DESI ratios vs Janus-LT/fid for the L8b best-fit ΛCDM (h 0.6864, ω_b 0.02252, ω_c 0.11903)
≤ 12.59 (95% for 6 dof) → CONSISTENT, else TENSION. Also report χ² for the fiducial itself (ratio 1). C0 fail → L9 not claimed.
Results: field_tests/results/janus_lt_l9_fs8.txt.
