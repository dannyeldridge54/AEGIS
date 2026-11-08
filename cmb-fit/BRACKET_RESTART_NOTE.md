# Bracket restart note (8 Nov 2026)

Rule: aegis-Kronos-syndyr `research/refit/PREREG_BRACKET.md`, **unchanged**.

- 2 of the 6 stage-1 jobs finished (θ = 2.41421, F8 and F9; scores 2430.00 and 2430.72 vs the locked fit 2428.83).
- The other 4 (θ 2.41421 F10; θ 2.777 F8, F9, F10) stopped part-way at about 04:40–05:00 UTC on 8 Nov, when their
  windows were closed to free the PC for UB-2. They did not fail (no error in their logs); they were interrupted.
- The rule says failed jobs are listed as missing and not re-run. Whether an interrupted job counts as failed was left
  to Danny. On 8 Nov 05:47 CT he asked "Is the bracket needed if so restart them".
- Action: the 4 jobs restart from scratch after the S8-J / S8-L fits finish (`cmb-fit/after_s8_pc.sh`). Their old logs
  are kept as `*_log_interrupted.txt`. No partial result from the interrupted runs is used.
