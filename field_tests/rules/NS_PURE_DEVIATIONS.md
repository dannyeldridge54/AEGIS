# NS_PURE deviations

D1 (2026-11-13 04:50 CT, written before any rerun; no NS-PURE result exists). The first PC run (started 21:47,
gate step 02:28) crashed with RecursionError before fitting: ns_pure_fit.py replaced V.setup with _setup, and _setup
called V.setup (itself). Fix: keep the original as _V6_SETUP before patching and call that. Code-only; the rule, data,
priors, gate and readings are unchanged. The run is restarted once from the gate step (the V6 LCDM fit it reuses is
unchanged). The crash log is kept in cmb-fit/results/ns_pure_log.txt on the PC.
