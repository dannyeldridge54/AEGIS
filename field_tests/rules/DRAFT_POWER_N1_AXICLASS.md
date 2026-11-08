# DRAFT: running the deferred n = 1 test of PREREGISTRATION_POWER_N.md on AxiCLASS

**Status: DRAFT, not locked.** Written 8 Nov 2026 with AI assistance at Danny's request ("Yes", to drafting the n = 1 rule).
It is a run plan for an **already locked** rule, not a new rule. It becomes active only when Danny says to lock it.

## Background (all already on record)
- `cubemind/STEP2_RESULT.md` (31 Oct): the natural sources of a potential for the BI angle (instanton-type series, or a
  chiral anomaly) all have a mass term at the minimum, so they **behave like n = 1**. n = 3 needs two exact
  cancellations of harmonics. The 8 Nov literature check (Kaul & Sengupta 2014, Nieh–Yan instantons → cos η) agrees.
- `PREREGISTRATION_POWER_N.md` (locked 31 Oct 21:02 CT) asks how much the combined data penalise n = 1 and n = 2,
  with D_n = χ²(n) − χ²(n = 3): **D_n < 2** n = 3 not required; **D_n > 4** data require a flat-bottomed potential;
  2–4 not decisive.
- n = 2 ran: 10.35 worse (poorly converged), so n = 3 favoured (CLAIMS_INDEX E10).
- **n = 1 never ran.** Deviation 1 of 31 Oct 21:05 (`PREREGISTRATION_SPT3G_DEVIATIONS.md`): CAMB's EarlyQuintessence
  solver fails for n = 1 at every tested point; "an n = 1 test needs another engine (AxiCLASS supports n = 1) and is
  deferred." This draft carries out that deferral.

## Plan (fixed when locked)
- **Engine:** AxiCLASS, `cmb-fit/axiclass/early_late_spa.py`, exactly as the stored `ax_spa_edelock` (n = 3, χ² 2396.94)
  and `ax_spa_lcdm` (χ² 2402.99): same data (Planck low-ℓ + ACT DR6 + Planck-cut + ACT lensing + SPT-3G + DESI DR2 +
  Pantheon+), same priors, same lock of the switch-on to matter–radiation equality, best of 4.
- **One change:** `n_axion = 1` instead of 3. Run name `ax_spa_edelock_n1`.
- **Comparison:** D_1 = χ²(ax_spa_edelock_n1) − χ²(ax_spa_edelock), both on AxiCLASS, read with the locked thresholds.
  Also reported: Δχ² against `ax_spa_lcdm`, f_EDE, H0, θ_i.
- **Engine check before the fit:** at the `ax_spa_edelock` best point, AxiCLASS must compute n = 1 without error over the
  θ_i prior range (cloud smoke test, results below). If it cannot, the test stays deferred and that is reported.
- Expected (literature, not our result): n = 1 decays like matter and should fail as an early boost (Poulin et al. 2018).
  If it fails, the early role's n = 3 shape still has no quantum derivation, and that gap is stated plainly.

## Engine smoke test (8 Nov, cloud, no data)
_(filled in below when it finishes)_
