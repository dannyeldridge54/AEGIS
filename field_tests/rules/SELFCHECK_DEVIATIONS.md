# PREREG_SELFCHECK: deviation log

- **D1 (11 Nov 2026, before any V1 run).** The rule says the real-data anchor uses "the same compressed likelihood"
  but does not name the real compressed-CMB data vector. It is set to (100θ*, ω_b, ω_b + ω_c) computed from the
  ΛCDM+S8 Pantheon+ full fit (`cmp_ax_spa_lcdm_halofit_s8y6`), the same vector as the mock truth's CMB. τ is fixed at
  that fit's 0.0636 for the background calls. Nothing else changes.

- **D2 (11 Nov 2026, V3, written before any fσ_s8 prediction or χ² was computed).** The V3 conversion, from
  DESI 2024 V (arXiv:2411.12021v5). The paper defines σ_s8 through ShapeFit Eqs. 10–12 and the fiducial values of
  Appendix C, Table 11, but leaves three implementation details open. They are fixed here; the alternatives are
  also computed and reported.
  - **Template.** Planck 2018 ΛCDM, Table 6 row 1 (ω_b 0.02237, ω_cdm 0.1200, h 0.6736, n_s 0.9649, 10⁹A_s 2.0830).
    r_d^fid = 99.0792 Mpc/h (Table 11). σ_s8^fid(z) is taken as printed in Table 11.
  - **Pivot and constants.** k_p = π/r_d^fid; a = 0.6; s_8 = 8 h⁻¹ Mpc (Eq. 11).
  - **Formulas for each model X, at each tracer's z_eff** (Table 1: 0.295, 0.510, 0.706, 0.919, 1.317, 1.491).
    The ratio is ρ = r_d^fid/r_d, with both in Mpc.
    - A_sp = ρ³ P_nw(k_p ρ), with k in Mpc⁻¹ and P in Mpc³ (Eq. 12).
    - A = A_sp(X)/A_sp(template).
    - m = d ln[P_nw,X(kρ_X) ρ_X³ / P_nw,fid(k)] / d ln k at k_p. This is the slope of Eq. 10 at the pivot, i.e. the
      paper's "maximum slope at the pivot".
    - σ_s8 = σ_s8^fid · A^½ · exp{(m/2a) tanh[a ln(r_d^fid/s_8)]} (Eq. 11).
    - fσ_s8 = f(z_eff) · σ_s8, where f is the build's scale-independent growth rate.
  - **Open detail 1: P_nw.** Primary: the CLASS linear cold+baryon P(k) times EH98's no-wiggle/wiggle ratio for the
    same cosmology. Alternative: the raw linear P(k). The r_d rescaling already aligns the BAO phases.
  - **Open detail 2: units.** As above; the paper's Eq. 12 does not print them.
  - **Gate.** Before any model is compared with data, the template computed this way must reproduce Table 11's
    fσ_s8 to within 1% at all six z_eff, and A = 1, m = 0 must hold for the template.
  - **Outcomes.** If the gate fails, V3 is NO VERDICT. If the primary and alternative P_nw give different readings for
    either model, V3 is NO VERDICT.
  - **Data.** ShapeFit+BAO means and the fσ_s8 diagonal of each printed covariance (Appendix A, units 10⁻⁴):
    | Tracer | fσ_s8 mean | diagonal (10⁻⁴) |
    |---|---|---|
    | BGS | 0.396326 | 80.924891 |
    | LRG1 | 0.547632 | 35.284297 |
    | LRG2 | 0.479541 | 23.061044 |
    | LRG3 | 0.438454 | 17.011310 |
    | ELG2 | 0.372661 | 11.811326 |
    | QSO | 0.436849 | 21.028703 |
