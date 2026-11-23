# PREREG D2188: "Aion", a Zee-Babu prediction engine, a gift for Prof. K. S. Babu (OSU)
Locked 2026-11-23 ~07:50 CT, before code is written or run. Aion: the Greek figure of unbounded, cyclic time
(Weave time-god naming; chosen for the tool, not for anyone's heritage).

## What it computes (all fixed by neutrino oscillation data in the minimal Zee-Babu model)
Formulas transcribed from Herrero-Garcia, Nebot, Rius, Santamaria, arXiv:1402.4491 (Eqs. 3, 10, 13 and the
null-vector relations): f antisymmetric (h+), g symmetric (k++), det M_nu = 0 so m_lightest = 0 at this order.
P1 f-ratios f_etau/f_mutau and f_emu/f_mutau for NO and IO.
P2 h+ -> l nu branching fractions e : mu : tau, from Gamma(h+ -> l_a nu) proportional to sum_b |f_ab|^2.
P3 m_betabeta band (one Majorana phase free, m_lightest = 0) and sum m_nu, both orderings; sum m_nu compared with
   DESI DR2 + CMB (LCDM) bound 0.0642 eV (95%) as literature context.
P4 mu -> e gamma from h+: BR = alpha |f_etau* f_mutau|^2 /(48 pi G_F^2 m_h^4) (consistent with 1402.4491's
   combined bound at the old MEG limit); with the MEG II limit 1.5e-13 (arXiv:2504.15711) and the P1 ratio this gives
   a ceiling on |f_mutau| vs m_h.
Inputs: NuFIT 6.0 (arXiv:2410.05380), IC19 without SK-atm (both orderings available in our fetch):
NO s12^2 .307(+12-11) s23^2 .561(+12-15) s13^2 .02195(+54-58) delta 177(+19-20) dm21 7.49(19)e-5 dm3l +2.534(+25-23)e-3
IO s12^2 .308 s23^2 .562 s13^2 .02224(+56-57) delta 285(+25-28) dm21 7.49e-5 dm3l -2.510(+24-25)e-3
Uncertainty: Monte Carlo with split-Gaussian 1-sigma (approximation; flagged; delta is non-Gaussian).

## Locked tests
T1 (convention check): with U in PDG convention and M = U* diag(m) U^dagger, the vector (f_mutau, -f_etau, f_emu)
   built from the 1402.4491 ratios must be a null vector of M to |M v|/(|M||v|) < 1e-10 for NO and IO at best fit.
   If it fails only up to complex conjugation of delta, record as a convention difference and use the version that
   passes (stated in the output); not silently.
T2 (literature sanity): best-fit m_bb band must lie within NO [1.0, 4.5] meV and IO [15, 50] meV.
T3 (report): P2 ratios with 1-sigma bands; P3 sum m_nu vs DESI; P4 |f_mutau| ceiling at m_h = 0.5, 1, 2, 5 TeV
   for |f_etau/f_mutau| at best fit.
## Honesty rules
Minimal Zee-Babu only: the SU(5) embedding of arXiv:2412.14562 (coloured scalars contribute comparably) is NOT
covered and is stated. g-sector LFV (mu -> 3e etc.) depends on free g couplings and is not predicted. Referee
ping-pong until NULL before anything is sent.
