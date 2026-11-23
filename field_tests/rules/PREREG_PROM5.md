# PREREG PROM-5 — cycle 5: line radiation derived from ADAS (locked before computing), 2026-11-23 13:25 CT
Danny 12:01 approved public data. Data: OPEN-ADAS ADF11 89 sets (PLT, PRB, SCD, ACD) for Ar, Be, He, W (tools/fusion/adas/, mirror commit
recorded). Build: an ADF11 reader; coronal ionisation balance from SCD/ACD at each (n_e, T_e) (charge-exchange neglected); line power
L_line(T_e, n_e) = sum_z f_z PLT_z (PRB not added: recombination + impurity bremsstrahlung would double-count the Z_eff bremsstrahlung
already in S3; recorded as an approximation). Line radiation profile P_line(rho) = n_e n_imp L_line, integrated over the S3 profiles.
Goalposts:
 L1 reader/balance sanity: fractional abundances sum to 1 (<= 1e-10) at every grid point; Ar at 8 keV is >= 90% in the top two charge
    states (H- and He-like or bare); He fully stripped above 1 keV.
 L2 HELD-OUT PREDICTION (the 27 MW was an input until now): derived P_line at the ITER 500 MW point with f_Be 2.0%, f_Ar 0.14% (axis
    values used as averages, as before) and the derived f_He vs the table 27 MW, +- 40% (the f_Be/f_Ar axis-vs-average uncertainty).
 L3 rerun S3 with derived line radiation (input removed): report P1 (500 MW) and P2 (400 MW) as in PROM-1; ACCEPT if the 400 MW held-out
    still passes and the 500 MW distance does not get worse. Sensitivity (F2): P_line moves when f_Ar is changed by 10%.
 L4 W: report L_line(W) at 1-10 keV vs Puetterich's statement that c_W,max ~ 1.9e-4 for DEMO (order-of-magnitude consistency only).
Referee after; DEVIATIONS first; one rerun.
