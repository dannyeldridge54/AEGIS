# N5 DEVIATIONS (written before the rerun). Locked run: P1-P4 PASS.
Referee R95 (sonnet; probes in /tmp): claim holds 1 eV-EH; test discriminates (T -1% or AWR+1 already fail p95); kernel normalisation correct.
- DEV-1 the second exponential (low-energy term) is never exercised above 1 eV, and P4 compared our 0 K with our 900 K (no NJOY reference).
  Rerun extends the comparison DOWN to 1e-5 eV against the NJOY 294/900 K curves (same metric) -> tests the second term and the thermal region.
- DEV-2 above-EH input (evaluated 0 K elastic / 294 K capture) reaches only the top ~100 eV via the kernel: rerun excludes the top 200 eV of the
  resolved range from the metric.
