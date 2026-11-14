# Deviations for PREREG_D367_OMEGAKIN

D1 (08:40 CT, before the scored run; location only): the cloud cores are busy (D360 T1) and background jobs there are capped at 2 h, so the
locked script runs unchanged on the PC's Linux VM ($HOME/d367, packaged from the cloud repo: chain_d22.py, sugra_mirror*.py, and
omegakin_d367.py with only its sys.path line pointed at the package; sha256 of the locked script in the cloud repo is unchanged). A
175-second timed foreground trial reached N − N_e = 8.5 before the timeout (exit 124). It is not scored; the scored output is the full
setsid-nohup run. The rule, statistic and reading are unchanged.

D2 (08:48 CT, before any scored output): the PC VM kills background processes when a call ends, and a call is capped at 180 s. The locked
script is therefore run in segments by theory/review/omegakin_d367_ckpt.py. This is identical to omegakin_d367.py except that it pickles the
loop state (z, N, Y, peak, dilution) after 150 s and resumes from it. The state is exact (the loop already restarts solve_ivp every step from z).
The validation rule (n_B/s at N − N_e = 11 within 1% of 1.090×10⁻¹⁰) guards against any restart effect. The rule and reading are unchanged.
D3 (09:00 CT, operational): late steps are slow (single step > 25 s), so segments timed out before checkpointing; the checkpoint time limit is now an environment variable (D367_TLIM, used at 90 s). No physics change.
