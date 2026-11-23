# PREREG D2184 — pulse test of Loom qsim against Liu group data (Hardesty-Shaw et al., arXiv:2301.02707)
Locked 2026-11-23 06:34 CT before computing. Danny 06:26: "Ping pong pulse test with ref. Get some data she's seeking." Referee running in parallel on D2183.
Published facts used (from the paper, as read): Na spin-1 BEC, M = 0, ρ0(0) = 0.5, θ(0) = 0; static sSMA fit c2/h = 23.7(1) Hz; paper states sSMA gives q* ≈ c2 for this state (separatrix); 1D GP gives q*/h ≈ 22 Hz; periods T ≈ 5–40 ms over q/h = 10–70 Hz with T diverging near q*.
Mapping: our mean-field energy per atom e = c[ρ0(1−ρ0) + 2Re(ζ1*ζ−1*ζ0²)] − qρ0 with c ↔ c2 (to be CHECKED, not assumed: the test below fails if the factor is wrong). h = 1, frequencies in Hz, times in ms.
Tests:
 P1 separatrix: our q* (where T diverges, scanned 10–70 Hz in 0.25 Hz steps) within 10% of 23.7 Hz.
 P2 period range: our T(q) at q/h = 15, 42, 65 Hz falls in 5–40 ms, with T(65) < T(42) and T diverging toward q*.
 P3 exact-vs-mean-field for N = 1e5 is not computed exactly (too large); report the √N-scaled break time from D2183 L3 as an estimate, labelled.
Output: field_tests/results/d2184_qsim_vs_liu2023.json, including the full predicted T(q) curve (data she can compare against her Fig. 1g).
