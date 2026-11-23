# PREREG JET-1 BEAM-TARGET (23 Nov 2026 14:40 CT) — measured JET D-T record pulses as held-out; beam-target fusion added
Hints tools/fusion/hints/jet1.json. New tool tools/fusion/beam_target.py: classical slowing down (H6) of D beam ions in a T-rich plasma, Bosch-Hale
D-T cross section at E_cm = E_b m_T/(m_D+m_T) (target at rest), yield per ion Y (H7), P_bt = sum over energy components (P_k/E_k) Y_k 17.589 MeV.
Inputs for #99971: P_dep 26.5 MW, E_b 108 keV (fractions 0.53/0.33/0.14 at E, E/2, E/3), f_T = n_T/(n_D+n_T) 0.85, n_i/n_e 0.85 (Z_eff ~1.5, Be proxy;
not published), n_e 6e19 (only enters lnL), T_e at the beam deposition = 6.5 keV central estimate (H5: Te0 8 keV in the same scenario; the
deposition-weighted Te is lower) with the band 5-8 keV reported. Thermonuclear part from the existing engine is NOT recomputed (profiles absent):
TRANSP's 7% is used only to form the target.
Goalposts (locked):
J1 #99971: NBI beam-target power at Te 6.5 keV within +-40% of the TRANSP-implied NBI beam-target power 10.1 x (1 - 0.07 thermal - 0.07 RF) = 8.7 MW.
J2 #104522 analog (30 MW D-NBI, f_T 0.80, Te 6.5 keV, same model) within +-40% of 13.5 x 0.86 = 11.6 MW.
J3 can-fail: f_T 0.5 instead of 0.85 must lower P_bt by > 30% (H4 linear in f_T).
J4 sanity: the optimum D-beam energy of our yield-per-energy curve lies within 90-140 keV (H8).
Referee after; DEVIATIONS before any fix; one rerun.
