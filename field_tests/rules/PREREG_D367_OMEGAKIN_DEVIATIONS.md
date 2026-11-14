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
D4 (09:02 CT, before scoring): late steps slow to ~0.1 e-fold per 3-minute segment (stiff σ oscillations), so reaching N − N_e = 16 would take ~2 h of segments. The run is stopped at N − N_e = 11 (the validation point); the 'is x still rolling at the end' item is reported at N − N_e = 11 instead of 16. The Ω_kin reading at 2×10¹³ GeV and the validation are unchanged.
D5 (16:45 UTC 14 Nov, location only, before any scored output past N − N_e = 10.36): on the PC VM, single steps at N − N_e ≈ 10.4 now take longer than the 180 s call cap, so segments 25–28 timed out with no progress. The run moves back to the cloud (D360 T1 is finished, so cores are free) as one background job with D367_TLIM=6600 s, resuming from the VM checkpoint ck.pkl (sha256 1798f3b2aaecbe19aeb45ca560f9e309ca5e125f703bae58dda625b152f3ecba, state at N − N_e = 10.36), using the cloud copy of omegakin_d367_ckpt.py (same code; only the sys.path line differs from the VM package, as in D1). The scored series is the VM segment lines up to 10.0 plus the cloud lines from 10.5 to 11.0. Rule, statistic and reading unchanged.
