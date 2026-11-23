# JET-1 DEVIATIONS (written before the rerun). Locked run: J1 PASS (+32%), J2 PASS (+4%), J3 PASS, J4 FAIL (191 keV).
Referee R102 (sonnet; /tmp): slowing-down physics correct (tau_s 0.65 s, E_c 99 keV, lnL 16.9, units, limits).
- J4: the locked metric (max of Y(E)/E) peaks at 184-197 keV; H8's 100-120 keV is the sigma(E_cm) peak (108 keV in our code; sigma*v peak 119 keV).
  Locked-metric vs hint-semantics mismatch: J4 FAIL stands; the sigma-peak value 108 keV is reported separately (not a pass of J4).
- DEV-1 (fair, physics completeness) target thermal motion: Maxwellian T targets at T_i ~ 9 keV (Ti > Te, H5) raise <sigma v_rel>; R102 scratch +12.5%.
  Rerun includes it (rate coefficient averaged over Maxwellian targets) for J1/J2/J3.
- Open, NOT fixed (would be tuning or needs a source): 0.53/0.33/0.14 read as POWER fractions - if they are current fractions the power fractions
  are 0.71/0.22/0.06 and P_bt rises to ~14.8 MW; fast-ion losses/ripple/orbit (downward) not modelled; n_i/n_e 0.75-0.95 -> 10.0-13.0 MW; E_b 100-114 keV
  -> 9.9-12.6 MW; the 7%/7% subtraction mixes TRANSP times (ETS RF 20% -> target 7.4 MW).
