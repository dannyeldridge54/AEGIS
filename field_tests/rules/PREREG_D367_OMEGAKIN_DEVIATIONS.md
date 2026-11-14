# Deviations for PREREG_D367_OMEGAKIN

D1 (08:40 CT, before the scored run; location only): the cloud cores are busy (D360 T1) and background jobs there are capped at 2 h, so the
locked script runs unchanged on the PC's Linux VM ($HOME/d367, packaged from the cloud repo: chain_d22.py, sugra_mirror*.py, and
omegakin_d367.py with only its sys.path line pointed at the package; sha256 of the locked script in the cloud repo is unchanged). A
175-second timed foreground trial reached N − N_e = 8.5 before the timeout (exit 124). It is not scored; the scored output is the full
setsid-nohup run. The rule, statistic and reading are unchanged.
