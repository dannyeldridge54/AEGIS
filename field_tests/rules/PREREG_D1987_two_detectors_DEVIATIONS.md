# D1987 DEVIATIONS (before any calibration)
1. **Warm-up.** A development null run (seed 99, not a training or held-out seed) put **all** of its alarms in the first 0.01 s: baselines settling, plus the split FIT switch. There were none afterwards.
   - The calibration's false-alarm and probe counts now start after **2 s of warm-up**. This is the same exclusion as A3's quiet windows, which start at 2 s.
   - Each training run is therefore 7 s long (2 s warm-up + 5 s counted). The scored-run bars are unchanged.
