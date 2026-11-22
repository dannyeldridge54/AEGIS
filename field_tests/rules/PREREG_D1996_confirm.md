# PREREG D1996: every alarm is confirmed by persistence (triangulation in time). Locked before code and runs.
## D1995 verdict: FAIL
- 20 s runs: 3 of 4 failed full-window precision (seeds 2040–2042).
- 60 s runs (2044, 2045) and the replay (2046): PASS.
- Auto round 11 (60 s, seeds 2048 and 2049): FAIL on full-window precision.
- **Diagnosis (exact replay of seed 2042, pulse 21567): genuine noise excursions.** For example, the Y_B estimate swung 0.78σ in 41 pulses. These fire at the detectors' calibrated false-alarm rate, which was admissible up to 1e-5 per pulse: about 4 strays per 20 s run. That is incompatible with the precision bar. It is not a code bug.

## Rule
A raw alarm at pulse p on layer L becomes an **event** only if it persists 200 pulses later (p + 200). Otherwise it is RETRACTED (logged as noise).
| alarm source | persists if |
|---|---|
| margin i (detectors A, B) | \|M_i − (pre-alarm baseline_i + cumulative self-moves on i since p)\| > max(2 sd_i, 1e-3 for the deterministic margins) |
| stream s (detector C) | \|est_s − pre-alarm baseline_s\| ≥ 0.5 σ_release (MATERIAL) |

- An event's time is the raw alarm time. The confirmation latency (200 pulses ≈ 47 ms) is reported.
- The controller still sees raw alarms (more conservative).

## Tests (new seeds; all bars as locked: A1–A5 on events; replay MATERIAL recall = 1 and specificity ≥ 6/7)
1. Null calibration on training seeds 1–5 (7 s each, 2 s warm-up): **confirmed** false-alarm rate ≤ 1e-6 per layer-pulse.
2. 20 s × 4 (seeds 2050–2053).
3. 60 s × 2 (seeds 2054, 2055).
4. Replay (seed 2056).
5. One auto pulse (60 s field, 2 parallel seeds).

**PASS needs tests 1–4 all to pass.** Test 5 is reported.
