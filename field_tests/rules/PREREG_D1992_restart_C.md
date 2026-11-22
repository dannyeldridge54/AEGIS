# PREREG D1992: detector C restarts after a change. Locked before code and runs.
- **Defect** (auto round 10, a 20 s field run): A3 FAIL, with L8 at 5.5e-3 and L6 at 7.9e-4 false alarms per pulse in the quiet windows. Detector C re-fires while its slow baseline (α = 0.002) catches up after a stream step ends.
- **Fix** (standard restart after a detected change): when detector C alarms on stream s, set s's baseline to the current estimate and reset its whitening memory and its CUSUM. Nothing else changes. The calibration config (0.08, 40) is kept.
- **Tests**, on new held-out seeds. Bars as locked: A1–A5; replay recall = 1 and specificity ≥ 6/7.
  1. 60 s scored run, seed 2033;
  2. **20 s scored run, seed 2034**, where the defect showed;
  3. replay, seed 2035.
- **PASS needs all three.** Then the self-driving pulses run once more.
