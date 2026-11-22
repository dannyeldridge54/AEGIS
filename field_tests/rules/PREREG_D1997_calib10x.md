# PREREG D1997: powered calibration of the confirmed false-alarm rate (D1996 test 1 was underpowered: 0.75 expected events). Locked before running.
- Same procedure as D1996's calib_confirmed: null streams, virtual clock, detector configs as adopted (B (0.16, 20) with online tuning off; A exact; C (0.08, 40)), confirmation by persistence at 200 pulses.
- **10× the data:** training seeds 1–50, 7 s each, 2 s warm-up excluded. That gives about 7.5e6 layer-pulses, so 7.5 expected events at the 1e-6 bar.
- **Bar:** a one-sided Poisson test. PASS if the confirmed count k satisfies P(K ≥ k \| λ = 1e-6 × N) ≥ 0.05, meaning the count is consistent with a rate ≤ 1e-6. Report k, N, the rate, and its 95 % upper limit.
- Run as 2 parallel workers (seeds split odd and even). The result is final, with no rerun.
