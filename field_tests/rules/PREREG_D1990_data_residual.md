# PREREG D1990: data-residual detector plus balancing freeze (fixes the D1989 replay masking). Locked at this commit, before code or runs.
## Change (engine v4.1, a flag in loom_rt4.py)
- **Detector C** runs on each data stream's own running estimate (n_s, α_s, lep, wino, Y): z_s = (est − slow baseline)/sd, whitened (φ = 0.95) and self-normalised exactly like detector B. A CUSUM with the **live config of detector B** (no separate tuning).
- An alarm on stream s is an event on s's layer (lep→4, wino→5, n_s→6, α_s→7, Y→8).
- **Freeze:** while stream s is in alarm, and for 2 s × (T/60) after it, s's layer does **not balance**. Data shifts can therefore no longer be absorbed as self-moves.

## Tests
1. **Replay** (P2 history, 70 s, new seed 2029). Bars:
   - recall = 1 on the detectable releases (|Δ|/σ ≥ 1, 6 releases);
   - specificity ≥ 6 of 7 on the quiet-expected releases (|Δ|/σ < 0.25).
2. **Synthetic scored run** (60 s, new seed 2030). Bars A1–A5 as locked in D1986/D1989. The freeze must not break them.
3. **Calibration check:** detector C's false-alarm rate on the 5 training null seeds (7 s each, 2 s warm-up) ≤ 1e-5 per stream-pulse.

**PASS needs 1–3.** If any fails: FAIL, reported, no retuning.
