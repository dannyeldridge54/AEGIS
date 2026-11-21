# PREREG_RW15_AXION_VS_D1810 — DEVIATIONS
## D1 (21 Nov 2026) — lock-order note (procedural, no rerun)
- The lock was committed (51e70308, 10:59:41 −06:00) before the script ran (result file 10:59:43). The push in the same
  command returned "remote rejected … cannot lock ref" (a concurrent ref update), and the script then ran without waiting.
  A fetch afterwards shows origin/unify-bg at 51e70308, so the lock did reach the remote, but I cannot show it was pushed
  BEFORE the run. The rule "pushed before computing" is therefore not demonstrably met.
- Mitigation: the computation is a fixed two-number arithmetic estimate with no free choices after the lock (2x·m₃/₂ vs the
  window), and the verdict is 47 decades from the threshold. No rerun; result kept as is.
