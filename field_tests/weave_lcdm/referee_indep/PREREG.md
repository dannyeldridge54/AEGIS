# PREREG (referee, independent): reverse-thread w(a) re-derivation + cheap CMB(compressed)+DESI DR2+DES-Dovekie fit

Written before any run. Author: referee pole. No reading of rt_wtable / weave_lcdm*.py source.

## T1: thread w(a) from the potential alone
- Units 8piG = 1, N = ln a, H0 = 1 today. rho_m = 3 Om a^-3, rho_r = 3 Or a^-4.
- V(phi) = V_L (1 - A e^{-beta phi}), A = 16 zeta(2)/(3 zeta(3)), beta = 2 sqrt(2).
- Initial: a_i = 1e-3, dphi/dN = 0, A e^{-beta phi_i} = u_i.
- EOM: x = dphi/dN; H^2 = (rho_m + rho_r + V)/(3 - x^2/2); eps = (rho_m + 4 rho_r/3 + H^2 x^2)/(2 H^2);
  dx/dN = -(3 - eps) x - V'(phi)/H^2. V_L shot so that H(a=1) = 1 (flatness).
- w = (H^2 x^2/2 - V)/(H^2 x^2/2 + V).
- Comparison to rt_wtable(u_i, Om, Or) via input/output only, Om = 0.30, h = 0.68,
  Or = 2.4728e-5 (1 + 0.2271*3.044)/h^2, at u_i = 0.013, 0.109, 0.173.
- PASS: max |w_mine - w_rt| <= 0.01 over 1e-3 <= a <= 1 for all three u_i. Otherwise report the difference (FLAG).

## T2: cheap fit, background only (CAMB get_background, PPF with my own w(a) table)
- Data: CHW 2019 4-parameter compressed Planck 2018 (R, l_A, omega_b, n_s; Hu-Sugiyama z*), DESI DR2 from
  bao_data/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_{mean,cov}.txt (full 13x13 cov as shipped),
  DES-Dovekie from sn_data/DES-Dovekie (shipped inverse covariance, packed upper triangle), d_L = (1+z_hel) D_M(z_HD),
  analytic marginalisation over the magnitude offset: chi2 = A - B^2/E.
- Models: L = flat LCDM, free (omega_b, omega_c, H0, n_s), Sum m_nu = 0.06 (1 massive).
  W = Weave: n_s = 0.9706 fixed, Sum m_nu = 0.0587 (3 nu normal), my thread w(a) with u_i profiled on
  u_i in {1e-3, 0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4}, free (omega_b, omega_c, H0) at each node (Nelder-Mead, 2 starts).
- Report: chi2 per node, min over nodes (plus a local parabolic refinement around the best node), Delta chi2 (W - L),
  Delta AIC with k_W = 4 (incl. u_i), k_L = 4; number of local minima in the u_i profile.
- Reading fixed now: W - L <= -6 -> "Dovekie supports the thread"; -6 < W - L < -2 -> "mild"; |W - L| <= 2 -> "consistent";
  > +2 -> "disfavoured".
- Untestable here: A_s, tau, r, alpha_s, lensing.
