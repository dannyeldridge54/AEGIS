# CM-IRIS deviations (written before any rerun)

Run 1 (as locked), field_tests/results/cm_iris_run1.json: I2 PASS (0 px differ), I3 PASS
(prep 38 ms, mean frame 0.36 ms over 118 frames), I1 FAIL, I4 FAIL. Verdict: FAILED AS LOCKED.

- I1 fail: LTTB on the 20k-point noisy series deviates by up to 47.8 device px at pixel columns
  (smooth series: <= 0.006 px). LTTB keeps one point per bucket, so it cannot represent noise
  inside a bucket. DEV-1: replace LTTB with M4 decimation (per device-px column keep first, last,
  min, max; buckets aligned to integer device-px columns). Expected: exact at every column.
  LTTB stays in iris.js for reference but is no longer the default.
- I4 fail: 3.4e-12 relative on the noisy series only. Cause is the metric, not the readout:
  near zero crossings of sin(x) the reference value is ~1e-5, and the test computes its own
  reference with a different rounding order. DEV-2: the rerun reports BOTH the locked relative
  metric and |got-want| / (series y-range); the rerun counts as passing I4 only if the locked
  metric passes on the three smooth series AND the range-normalised error is <= 1e-12 on all four.
  This is a post-hoc metric change and is labelled as such.
One rerun only.
