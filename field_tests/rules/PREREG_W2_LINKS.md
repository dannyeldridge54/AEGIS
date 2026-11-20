# PREREG_W2_LINKS — Weave Control cross-level links (locked 20 Nov 2026, before any computation)
Item W2 of tools/weave_control/LOOP_STATE.md. Each link is a display or test inside the Weave Control engine. Rules are fixed here; any later change goes in PREREG_W2_LINKS_DEVIATIONS.md first.

## L1 wino gamma line (Galaxy level) — the exact D1322 / smoke-test recipe, replacing W1's shortcut
- σv_line(M): LO Sommerfeld, v = 1e-3, off_factor √2, σ_γγ + ½σ_Zγ (tools/janus_astro/hyperion_smoketest.py check 5, 1/M² general).
- J ratio: J_ann(halo) / J_ann(bench), annulus ψ ∈ [0.5°, 3°], no b-mask, r☉ = 8.178 kpc; bench = Einasto(r_s 20, α 0.17) at ρ☉ 0.39.
- f_max = √(2.3e-28 / (σv_line × 0.794 × J ratio)), the D1322 form. Applies at M = 1 TeV only (±50 GeV): the only quoted limit point.
- f_pred = wino_fraction(M) bracket (D1152). PASS if f_pred_high ≤ f_max; TENSION if f_pred_low ≤ f_max < f_pred_high; FAIL if f_max < f_pred_low. Elsewhere: 'open (no limit stored)'.
- Check: for Burkert(3.37) at ρ☉ 0.40 the recipe must give f_max = 0.286 ± 1% (smoke test D1322), else the link is not shown.

## L2 negative space vs DESI DR2 Lyα BAO (Late-universe level) — DISPLAY ONLY
- Data: z_eff 2.33, D_H/r_d = 8.632 ± 0.101, D_M/r_d = 38.99 ± 0.53, ρ = −0.431 (arXiv:2503.14739).
- These points are ALREADY inside the DESI DR2 BAO likelihood used in the D1713/D1725 fits, so they are not an independent test. Shown as context with the 2-D χ² of each locked best fit, if those fits' D_H, D_M are available; no pass/fail is attached.

## L3 Arthur-field G_eff → S₈ (Late-universe level)
- Model S₈ = the s8 value stored in each locked D1725 best fit (score_d1713 output), per SN set. No new fits.
- Data: KiDS-Legacy 0.815 +0.016/−0.021 (arXiv:2503.19441; use σ = 0.021 when model > data, 0.016 when model < data); CMB lensing combination 0.828 ± 0.012 (Qu et al. 2026, via arXiv:2602.12238).
- Pull = (model − data)/σ. PASS |pull| < 2, TENSION 2–3, FAIL ≥ 3. Lensing and KiDS are reported separately (not combined).

## L4 N*/T_rh → BBN
- Stated, not computed: T_rh = 9 × 10⁸ GeV is far above BBN, so reheating has no direct BBN effect; the only BBN link is ΔN_eff from the dark sector (W1, D1646/D1648/C5). Shown as a label.

## L5 Galactic-centre line region → Sky level
- The Sky level gets a second target: the Galactic centre (RA 266.4168, Dec −29.0078, J2000) with the 3° annulus as the region, so the Mapper can draw it and make a finder chart. Engineering only.

## Not allowed
No refits; no tuning of halo or ρ☉ to change a verdict; every number shown carries its source.
