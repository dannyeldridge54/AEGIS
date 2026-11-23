# PREREG PROM-8 ASH (23 Nov 2026 13:10 CT) — Prometheus cycle 6: SPARC composition and ash as the POPCON paper states them
Target: SPARC self-solved power balance 96/140 MW (D2201). Hints: tools/fusion/hints/cycle6.json (main source Creely et al. 2020, Sec. 4, Table 2).
## Change (inputs only; like-with-like)
SPARC: f_DT 0.85; He 6% FIXED (he_selfconsistent off: the paper fixes it, ash inside the 85%); W 1.5e-5; lumped Z = 8 (oxygen) for
quasi-neutrality: f_8 = (1 - 0.85 - 2*0.06 - 74*1.5e-5)/8 = 0.003611; Be 0, 3He 0 (this paper's mix). Line radiation from OPEN-ADAS for
He, O, W (oxygen file added to the line model). Heating 11.1 RF + 1.7 ohmic = 12.8 MW. nu_T 2.5, n0/<n> 1.3, n_ped 2.7e20, Ti = Te, H98 1.0,
<n_e> 3.1e20 (volume). Synchrotron kept (physics), reported separately.
## Goalposts (locked)
A1 SPARC power balance: P_fus within +-25% of 140 MW AND <T> within +-20% of 7.3 keV (Creely Table 2).
A2 can-fail: the same run with self-consistent ash ON (as D2201) must differ in P_fus by > 15%.
A3 (consistency, reported) prescribed P_fus at <T> 7.3 keV with this composition.
A4 ITER-400 held-out unchanged (389.5 MW, 3.41 s).
Referee after; DEVIATIONS before any fix; one rerun.
