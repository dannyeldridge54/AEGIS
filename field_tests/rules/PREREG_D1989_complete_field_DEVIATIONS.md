# D1989 DEVIATIONS
1. **(01:50Z) P4 defect.** The 20 s auto field runs ended before the locked 60 s event schedule (E2 at 25–35 s, E3 at 45–55 s). Recall therefore failed by construction, and n_s was scored while E1's shift was still active. That gave a spurious FDR "tension" on A1.
   - Auto rounds 6–8 are kept as recorded, marked **DEFECTIVE (schedule)**. Round 8 was also cut off when the run was stopped.
   - **Fix:** the event times, quiet windows and recovery windows scale with T/60.
   - The bars are unchanged. The fdr_ledger entries from rounds 6–8 are removed as artefacts.
   - Auto restarts from the next round.
