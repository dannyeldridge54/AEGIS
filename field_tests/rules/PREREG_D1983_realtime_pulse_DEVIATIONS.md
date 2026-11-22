# D1983 DEVIATIONS: design details fixed BEFORE the first run (22 Nov 2026 ~00:55Z)
These are details the lock did not specify. They are written down before any run, so no result can have influenced them.
1. **Self-move compensation.** Each pulse, every margin's baseline is moved by J_L·Δx for the knob changes the engine itself applied. A referee therefore flags only **unexplained** changes (data, external kicks), not the engine's own balancing. Without this, every 0.2 % balancing step would be a false alarm on the fixed-bound margins, whose sd floor is 1e-6.
2. **Events are rising edges.** An event fires when |m − baseline| first exceeds 4 sd. It re-arms only after the deviation falls back within 2 sd. The baseline variance is not updated while the detector is in the exceeded state.
3. **Balancing cushion.** The balancing step is taken only while the layer's minimum margin is below 0.05, so a comfortably resonant layer spends no fits.
4. **Not enforced in this run (stated):** N0's rule "L5–L9 may not move until L4 locks" is not applied. This is an engine test, and its knob moves are a consistency map counted as fits, not physics.
- 5. (00:59Z, after a 3 s dry run with no events) Added a **report-only** counter of opposing pulls on the same knob in the same pulse (the tug of war). It changes no rule or bar. The dry run showed L5 and L7 pulling m3/2 in opposite directions.
