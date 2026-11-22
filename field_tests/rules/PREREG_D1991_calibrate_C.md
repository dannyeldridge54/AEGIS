# PREREG D1991: detector C gets its own null calibration (D1990 FAILed only its calibration bar: false-alarm rate 7.0e-5 against 1e-5). Locked before code and runs.
- D1990's FAIL stands.
- **Procedure,** identical to D1987 for detector B: training null seeds 1–5, 7 s each, 2 s warm-up.
  - Grid k ∈ {0.08, 0.16, 0.25} × h ∈ {12, 20, 30, 40, 60}.
  - Probes of 2 sd in z (0.32 per pulse in w) for 400 pulses, every 1,000 pulses, on a random stream.
  - Admissible if the false-alarm rate is ≤ 1e-5 per stream-pulse and ≤ 20 % of probes are missed.
  - Start = the admissible config with the lowest mean delay. **Detector C is then fixed** at that config; it no longer follows detector B's live config.
- **Held-out tests**, with bars as in D1990:
  1. replay on seed **2031**: recall = 1 on the detectable releases, specificity ≥ 6/7;
  2. synthetic scored run on seed **2032**: A1–A5.
- If no config is admissible: FAIL, and detector C stays unadopted.
- If PASS: detector C is adopted in loomd auto, and the self-driving pulses run again until a STALL or the endpoint.
