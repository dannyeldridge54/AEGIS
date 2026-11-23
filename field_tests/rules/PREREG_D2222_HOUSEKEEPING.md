# PREREG D2222 (ping-pong round 4 housekeeping; written before computing, 23 Nov 2026)
Referee round 4 minors: (1) alpha_s base 0.11446 hard-coded at three places in tools/rings/hex.py -> one named constant AS_ENGINE (no value
change); (2) Y_p pull lacks the omega_b error that D2221 gave D/H -> same propagation (Planck +-0.00015, PRIMAT-table derivative). Expected:
Y_p stays IN (|pull| <= 1); any status change is reported as is. No other change. Map rerun as map7.
Item checks closed without computation (recorded in D2222): ITER tau goalpost 3.4 s = ITER FDR 500 MW column (W 353 MJ / P_loss 104 MW) -
the 3.7 s of the Physics Basis is the 400 MW column (hint cycle1 H7) -> no goalpost error, EDGE final. N10 He/dpa band is Fe-matrix and the
locked metric is already Fe-only (DEV-1); EUROFER (Cr, W) would need a new MC run and a new lock - not a non-tuning fix of the locked metric.
