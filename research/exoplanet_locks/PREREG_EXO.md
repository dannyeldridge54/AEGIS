# Sigil Model exam: do planets lock more than chance? (rules written 2026-10-26, before looking)

Data: NASA Exoplanet Archive, Planetary Systems Composite table (pscomppars), all systems with >= 2 planets with
measured orbital periods. Adjacent pairs only (sorted by period), period ratio P_out/P_in in (1, 4].
Prediction A (locks): adjacent ratios fall within 1% above the first-order resonances 2:1, 3:2, 4:3, 5:4 more often than in
  a null where each system's period ratios are drawn from a smooth (log-uniform-ish, kernel-smoothed) version of the
  observed ratio distribution. Statistic: fraction of pairs with ratio in [p/q, 1.01 p/q] for those resonances.
Prediction B (mechanism): the excess is larger for compact pairs (inner period < 10 days, where tides and disc
  migration act strongest) than for wide pairs (inner period > 10 days).
Null for A: 10,000 smooth-distribution draws. Pass: p < 0.01. B: difference in excess with bootstrap 95% interval excluding 0.
Known caveat: transit surveys favour compact systems; this affects both groups' counts, not the resonance window test.
